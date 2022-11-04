import datetime
import hashlib

from sqlalchemy.exc import IntegrityError

from lesson10.storage.database import create_db, Session, engine
from .models import User, UserContacts, UserHistory
from os import urandom


def create_database():
    create_db()
    return Storage

class Storage:
    @staticmethod
    def _enter_client(user: str, ip: str):
        with Session() as s:
            s.add(UserHistory(user_id=user, ip=ip, enter_date=datetime.datetime.now()))
            s.commit()

    @staticmethod
    def add_client(login: str, pswd: str, ip: str):
        """Добавляет пользователя в БД"""
        password = Storage.__hash_password(pswd)
        with Session()as s:
            user = User(login=login, password=password)
            s.add(user)
            try:
                s.commit()
            except IntegrityError as er:
                return False
            user = s.query(User).filter(User.login == login).first()
            Storage._enter_client(user=user.id, ip=ip[0])
            return True

    @staticmethod
    def check_password(login, pswd=None, ip=None):
        with Session() as session:
            res = session.query(User).filter(User.login == login).first()
            if res.password == Storage.__hash_password(pswd=pswd, salt=res.password[:32]):
                if ip:
                    Storage._enter_client(res.id, ip)
                return True
            else:
                return False

    @staticmethod
    def get_clients():
        with Session() as s:
            return s.query(User).all()

    @staticmethod
    def __hash_password(pswd: str, salt = None):
        if not salt:
            salt=urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', pswd.encode('utf-8'), salt, 100000)
        return salt+key
