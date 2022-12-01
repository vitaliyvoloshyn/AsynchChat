from datetime import datetime
from os import getcwd
from os.path import exists

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

BASE_DIR = getcwd()
DB_NAME = 'server_db.sqlite'

engine = create_engine(f'sqlite:///{BASE_DIR}/{DB_NAME}')
Session = sessionmaker(bind=engine)
Base = declarative_base()


def create_db():
    if not exists(BASE_DIR + "/" + DB_NAME):
        Base.metadata.create_all(engine)


# models
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True)
    password = Column(String)
    history = relationship('UserHistory')

    def __repr__(self):
        return f'{self.login}'


class UserContacts(Base):
    __tablename__ = 'users_contacts'
    owner_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    def __repr__(self):
        return f'{self.owner_id} {self.user_id}'


class UserHistory(Base):
    __tablename__ = 'users_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    enter_date = Column(DateTime, default=datetime.now)
    ip = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return f'{self.enter_date} {self.ip}'
