import hashlib
from lesson10.storage.client_database import create_client_db, Session_cl, Message
from lesson10.storage.server_database import create_db, Session, User, UserContacts, UserHistory
from os import urandom


def create_server_database():
    create_db()
    return ServerDB()


def create_client_database():
    create_client_db()
    return ClientDB()


class ClientDB:
    # inputs
    def add_message(self, author_name: str, message: str):
        """Добавление пользователей"""
        with Session_cl() as session:
            session.add(Message(author=author_name, message=message))
            session.commit()

    # get
    def get_messages_by_author_name(self, author_name: str):
        """Возвращает список контактов для пользователя"""
        with Session_cl() as session:
            return session.query(Message).filter(Message.author == author_name).all()


class ServerDB:

    # inputs
    def add_user(self, login: str, password: str):
        """Добавление пользователей"""
        with Session() as session:
            password = self.__hash_password(password)
            session.add(User(login=login, password=password))
            session.commit()

    def add_history(self, ip: str, user: str):
        """Фиксирует подключение пользователя"""
        with Session() as session:
            user_id = session.query(User).filter(User.login == user).first().id
            session.add(UserHistory(ip=ip, user_id=user_id))
            session.commit()

    def add_contact(self, owner: str, user: str):
        """Добавление контакта для пользователя"""
        with Session() as session:
            owner_id = session.query(User).filter(User.login == owner).first().id
            user_id = session.query(User).filter(User.login == user).first().id
            session.add(UserContacts(owner_id=owner_id, user_id=user_id))
            session.commit()

    def del_contact(self, owner: str, contact: str):
        """Удаление контакта пользователя"""
        with Session() as session:
            owner_id = session.query(User).filter(User.login == owner).first().id
            user_id = session.query(User).filter(User.login == contact).first().id
            session.execute(f'DELETE FROM users_contacts WHERE owner_id = {owner_id} AND user_id = {user_id}')
            session.commit()

    # queries
    def get_users(self):
        """Все пользователи из модели User"""
        with Session() as session:
            return [user.login for user in session.query(User).all()]

    def get_contacts_by_user_name(self, user_name: str):
        """Возвращает список контактов для пользователя"""
        with Session() as session:
            user_id = session.query(User).filter(User.login == user_name).first().id
            contacts = session.execute(
                f'SELECT u.login FROM users u join users_contacts uc on u.id = uc.user_id WHERE uc.owner_id = {user_id}')
            return [contact.login for contact in contacts]

    # hash password
    @staticmethod
    def __hash_password(pswd: str, salt: bytes = None):
        if not salt:
            salt = urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', pswd.encode('utf-8'), salt, 100000)
        return salt + key

    def check_password(self, user: str, password: str = None):
        with Session() as session:
            user_pswd = session.query(User).filter(User.login == user).first().password
            if user_pswd == self.__hash_password(pswd=password, salt=user_pswd[:32]):
                return True
            else:
                return False
