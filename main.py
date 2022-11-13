from datetime import datetime
from os.path import exists

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

class ServerDB:

    engine = create_engine(f'sqlite:///server_db.sqlite', echo=True)
    Session = sessionmaker(bind=engine)
    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, autoincrement=True)
        login = Column(String, unique=True)
        password = Column(String)
        created_at = Column(DateTime, default=datetime.now)
        # book = relationship('Book', backref='users')

        def __repr__(self):
            return f'{self.login}'
    Base.metadata.create_all(engine)
    session = Session()


class ClientDB:

    engine = create_engine(f'sqlite:///client_db.sqlite', echo=True)
    Session = sessionmaker(bind=engine)
    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, autoincrement=True)
        login = Column(String, unique=True)
        password = Column(String)
        # book = relationship('Book', backref='users')

        def __repr__(self):
            return f'{self.login}'
    Base.metadata.create_all(engine)
    session = Session()

# d = ServerDB()
# c = ClientDB()

# user_s = d.User(login='alex', password=123)
# d.session.add(user_s)
# d.session.commit()
# print(d.session.query(d.User).all())
# user_c = c.User(login='bob', password=123)
# c.session.add(user_c)
# c.session.commit()
# print(d.session.query(d.User).filter(d.User.login=='alex').first().id)
# print([i for i in d.session.execute('Select * from users')])
