import bcrypt
from datetime import timedelta
from sqlalchemy import union_all, case
from sqlalchemy.orm import aliased
from datetime import datetime

def flatten(l):
    return [item for sublist in l for item in sublist]

def row2dict(row, exclude=''):
    """ Convierte un objecto en diccionario"""
    return {c.name: getattr(row, c.name) for c in row.__table__.columns if c.name not in exclude}

def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt()).decode('utf-8')

def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())

def get_closest(session, cls, col, the_time):
    greater = session.query(cls).filter(col > the_time).\
        order_by(col.asc()).limit(1).subquery().select()

    lesser = session.query(cls).filter(col <= the_time).\
        order_by(col.desc()).limit(1).subquery().select()

    the_union = union_all(lesser, greater).alias()
    the_alias = aliased(cls, the_union)
    the_diff = getattr(the_alias, col.name) - the_time
    abs_diff = case([(the_diff < timedelta(0), -the_diff)],
                    else_=the_diff)

    return session.query(the_alias).\
        order_by(abs_diff.asc()).\
        first()

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def config(session, key, default=""):
    from sisprot.models import Configuracion
    item = session.query(Configuracion).filter_by(key=key).first()

    if item:
        return item.value
    return default

class Default(dict):
    def __missing__(self, key):
        return key.join("{}")