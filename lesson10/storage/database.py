from os.path import exists

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from .config import BASE_DIR, DB_NAME


engine = create_engine(f'sqlite:///{BASE_DIR+"/"+DB_NAME}')
Session = sessionmaker(bind=engine)
Base = declarative_base()

def create_db():
    if not exists(BASE_DIR+"/"+DB_NAME):
        Base.metadata.create_all(engine)
