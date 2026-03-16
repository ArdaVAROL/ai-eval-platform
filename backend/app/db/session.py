from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


connect_args = {"check_same_thread": False} if settings.sqlalchemy_database_uri.startswith("sqlite") else {}

engine = create_engine(settings.sqlalchemy_database_uri, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
