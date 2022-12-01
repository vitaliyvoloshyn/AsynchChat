from datetime import datetime
from os import getcwd
from os.path import exists

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = getcwd()
DB_NAME = 'client_db.sqlite'

engine = create_engine(f'sqlite:///{BASE_DIR}/{DB_NAME}')
Session_cl = sessionmaker(bind=engine)
Base = declarative_base()


def create_client_db():
    if not exists(BASE_DIR + "/" + DB_NAME):
        print("createDB")
        Base.metadata.create_all(engine)


# models
class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String)
    enter_date = Column(DateTime, default=datetime.now)
    message = Column(String)

    def __repr__(self):
        return f'{self.enter_date} {self.message}'
