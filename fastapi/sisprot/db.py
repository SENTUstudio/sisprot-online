from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sisprot.pagination import BaseQuery


_settings = dotenv_values()

def _create_session(uri=None):
    if "postgresql" in uri:
        _bind = create_engine(uri)
    else:
        _bind = create_engine(
            uri, pool_size=20, max_overflow=0, pool_recycle=5 * 60, pool_pre_ping=True
        )
    _session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=_bind,
        query_cls=BaseQuery,
    )
    # _session = scoped_session(_session_factory)
    return _session_factory


def _build_uri(driver, username, password, host, port, db):
    return "{driver}://{username}:{password}@{host}:{port}/{db}".format(
        driver=driver, username=username, password=password, host=host, port=port, db=db
    )


db_session = _create_session(_settings["DB_URI"])

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
        # db_session.remove()

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    def __repr__(self) -> str:
        columns = ", ".join(
            [
                f"{k}={repr(v)}"
                for k, v in self.__dict__.items()
                if not k.startswith("_")
            ]
        )
        return f"<{self.__class__.__name__}({columns})>"


