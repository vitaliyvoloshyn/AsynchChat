from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

from lesson10.storage.server_database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True)
    password = Column(String)

    def __repr__(self):
        return f'{self.login}'


class UserContacts(Base):
    __tablename__ = 'users_contacts'
    owner_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    def __repr__(self):
        return f'{self.owner_id} {self.user_id}'


class UserHistory(Base):
    __tablename__ = 'history_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    enter_date = Column(DateTime)
    ip = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return f'{self.enter_date} {self.ip} {self.user_id}'
