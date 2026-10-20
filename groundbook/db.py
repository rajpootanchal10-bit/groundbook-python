from collections.abc import Iterator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from .models import Base

def make_engine(database_url: str):
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    engine = create_engine(database_url, connect_args=connect_args)
    
    if database_url.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def _fk_on(dbapi_conn, _record):
            dbapi_conn.execute("PRAGMA foreign_keys=ON")
            
    return engine

def init_db(engine) -> None:
    Base.metadata.create_all(bind=engine)

def make_sessionmaker(engine) -> sessionmaker:
    return sessionmaker(bind=engine, expire_on_commit=False)

from .settings import settings
engine = make_engine(settings.database_url)
SessionLocal = make_sessionmaker(engine)