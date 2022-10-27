import os.path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import stat

from database.entities import models

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

SQLALCHEMY_DATABASE_URL = "sqlite:///./clothe_store.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Base.metadata.create_all(bind=engine)
#os.chmod('./clothe_store.db', stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
