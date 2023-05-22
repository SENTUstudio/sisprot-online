from sqlalchemy import orm
from math import ceil
from sisprot.utils import row2dict
from fastapi import HTTPException


class Pagination:
    """Internal helper class returned by :meth:`BaseQuery.paginate`.  You
    can also construct it from any other SQLAlchemy query object if you are
    working with other libraries.  Additionally it is possible to pass `None`
    as query object in which case the :meth:`prev` and :meth:`next` will
    no longer work.
    """

    def __init__(self, query, page, per_page, total, items):
        #: the unlimited query object that was used to create this
        #: pagination object.
        self.query = query
        #: the current page number (1 indexed)
        self.page = page
        #: the number of items to be displayed on a page.
        self.per_page = per_page
        #: the total number of items matching the query
        self.total = total
        #: the items for the current page
        self.items = items

    @property
    def pages(self):
        """The total number of pages"""
        if self.per_page == 0 or self.total is None:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    def prev(self, error_out=False):
        """Returns a :class:`Pagination` object for the previous page."""
        assert (
            self.query is not None
        ), "a query object is required for this method to work"
        return self.query.paginate(self.page - 1, self.per_page, error_out)

    @property
    def prev_num(self):
        """Number of the previous page."""
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    def next(self, error_out=False):
        """Returns a :class:`Pagination` object for the next page."""
        assert (
            self.query is not None
        ), "a query object is required for this method to work"
        return self.query.paginate(self.page + 1, self.per_page, error_out)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        if not self.has_next:
            return None
        return self.page + 1

    def as_dict(self):
        return {
            'data': [row2dict(item) for item in self.items],
            'pages': self.pages,
            'total': self.total,
            'has_prev': self.has_prev,
            'has_next': self.has_next,
            'pageSize': self.per_page
        }
    
    def as_query(self):
        return {
            'data': self.items,
            'pages': self.pages,
            'total': self.total,
            'has_prev': self.has_prev,
            'has_next': self.has_next,
            'pageSize': self.per_page
        }
    
class BaseQuery(orm.Query):
    """SQLAlchemy :class:`~sqlalchemy.orm.query.Query` subclass with
    convenience methods for querying in a web application.
    This is the default :attr:`~Model.query` object used for models, and
    exposed as :attr:`~SQLAlchemy.Query`. Override the query class for
    an individual model by subclassing this and setting
    :attr:`~Model.query_class`.
    """

    def get_or_404(self, ident, description=None):
        """Like :meth:`get` but aborts with 404 if not found instead of
        returning ``None``.
        """
        rv = self.get(ident)
        if rv is None:
            raise HTTPException(status_code=404, detail=description)
        return rv

    def first_or_404(self, description=None):
        """Like :meth:`first` but aborts with 404 if not found instead
        of returning ``None``.
        """
        rv = self.first()
        if rv is None:
            raise HTTPException(status_code=404, detail=description)
        return rv

    def paginate(
        self, page=None, per_page=None, error_out=True, max_per_page=None, count=True, request=None
    ):
        """Returns ``per_page`` items from page ``page``.
        If ``page`` or ``per_page`` are ``None``, they will be retrieved from
        the request query. If ``max_per_page`` is specified, ``per_page`` will
        be limited to that value. If there is no request or they aren't in the
        query, they default to 1 and 20 respectively. If ``count`` is ``False``,
        no query to help determine total page count will be run.
        When ``error_out`` is ``True`` (default), the following rules will
        cause a 404 response:
        * No items are found and ``page`` is not 1.
        * ``page`` is less than 1, or ``per_page`` is negative.
        * ``page`` or ``per_page`` are not ints.
        When ``error_out`` is ``False``, ``page`` and ``per_page`` default to
        1 and 20 respectively.
        Returns a :class:`Pagination` object.
        """

        if request:
            if page is None:
                try:
                    page = int(request.args.get("page", 1))
                except (TypeError, ValueError):
                    if error_out:
                        raise HTTPException(status_code=404)
                    page = 1

            if per_page is None:
                try:
                    per_page = int(request.args.get("per_page", 20))
                except (TypeError, ValueError):
                    if error_out:
                        raise HTTPException(status_code=404)
                    per_page = 20
        else:
            if page is None:
                page = 1

            if per_page is None:
                per_page = 20

        if max_per_page is not None:
            per_page = min(per_page, max_per_page)

        if page < 1:
            if error_out:
                raise HTTPException(status_code=404)
            else:
                page = 1

        if per_page < 0:
            if error_out:
                raise HTTPException(status_code=404)
            else:
                per_page = 20

        items = self.limit(per_page).offset((page - 1) * per_page).all()

        if not items and page != 1 and error_out:
            raise HTTPException(status_code=404)


        if not count:
            total = None
        else:
            total = self.order_by(None).count()

        return Pagination(self, page, per_page, total, items)
