from sqlalchemy import Column, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session
from contextlib import contextmanager

from ...config import UpbitConfig
from typing import Any, Dict, List

config = UpbitConfig()
connection_string = config.mysql_connection_string('bitcoin')
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        
def upsert(
    session: Session,
    model,
    instance,
    filter_columns: List[str]=[],
    update_columns: List[str]=[]
):
    filter = {column: getattr(instance, column) for column in filter_columns}
    try:
        q = session.query(model).filter_by(**filter)
        existing_default = q.one()
        
    except NoResultFound:
        session.add(instance)
        
    else:
        assert isinstance(existing_default, model)
        for column in update_columns:
            setattr(existing_default, column, getattr(instance, column))
        
    session.flush()