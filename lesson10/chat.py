import json
import re
import threading
from json import JSONDecodeError
from socket import socket
from datetime import datetime
import pickle

from lesson10.storage.create_database import create_database


class Message:
    def __init__(self, *args, **kwargs):
        self.response = kwargs.get('response')
        self.code = kwargs.get('code')
        self.time = kwargs.get('time') or datetime.now()
        self.action = kwargs.get('action')
        self.text = kwargs.get('text')
        self.acc_to = kwargs.get('acc_to')
        self.acc_from = kwargs.get('acc_from')
        self.user = kwargs.get('user')

    def __getstate__(self) -> dict:
        """редактирует словарь обьекта под сериализацию"""
        attr = self.__dict__.copy()
        if self.acc_to:
            if isinstance(attr['acc_to'][0], socket):
                attr['acc_to'] = attr['acc_to'].__repr__()
        if self.acc_from:
            if isinstance(attr['acc_from'][0], socket):
                attr['acc_from'] = attr['acc_from'].__repr__()
        return attr


class Socket:
    host = ''
    port = 55555

    def __init__(self):
        self.socket = socket()


class Connection:
    def __init__(self, *args):
        self.conn: socket = args[0]
        self.addr = args[1]
        self.client_name = None
        self.client_pswd = None
        self.in_message = None
        self.db = create_database()
        threading.Thread(target=self.receive_msg).start()
        self.__add_obj_to_connections_list()
        self.__send_response(Message(response='OK', code=200, action='connecting', acc_to=[self.conn]))

    def __add_obj_to_connections_list(self):
        Server.connections.append(self)

    def __send_response(self, obj_resp: Message) -> None:
        """создание ответа на подключение"""
        self.send_message(obj_resp)

    def send_message(self, msg: Message):
        """"""

        if msg.acc_to:
            for client in msg.acc_to:
                client.send(pickle.dumps(msg))
        else:
            for cl in Server.connections:
                if cl.conn != self.conn:
                    cl.conn.send(pickle.dumps(msg))

    def receive_msg(self):
        while True:
            try:
                msg = self.conn.recv(1024)
            except ConnectionResetError as e:
                print(f'клиент {self.addr} отключился')
                Server.connections.remove(self)
            if not msg:
                Server.connections.remove(self)
                print(f'клиент {self.addr} отключился')
            else:
                self.in_message = Message(**pickle.loads(msg).__dict__)
                if self.in_message.action == 'msg':
                    self.__send_response(Message(response='OK', code=200, action='msg', acc_to=[self.conn]))
                    print(f'[*] <{self.client_name}>: {self.in_message.text}')
                    self.__forward_msg()
                elif 'auth' == self.in_message.action:
                    if self.auth(self.in_message):
                        self.client_name = self.in_message.user['login']
                        resp = Message(action='auth', response='OK', code=200, acc_to=[self.conn])
                    else:
                        resp = Message(action='auth', code=400, response='Invalid password', acc_to=[self.conn])
                    self.send_message(resp)

    def __forward_msg(self):
        if self.in_message.acc_to:
            receivers = []
            for acc_to in self.in_message.acc_to:
                for client in Server.connections:
                    if acc_to == client.client_name:
                        receivers.append(client.conn)
                        break
            self.in_message.acc_to = receivers
        self.in_message.acc_from = self.client_name
        self.send_message(self.in_message)

    def __getstate__(self) -> dict:
        """редактирует словарь обьекта под сериализацию"""
        attr = self.__dict__.copy()
        attr['conn'] = attr['conn'].__repr__()
        return attr

    def __register_client(self, msg: Message):
        self.db.add_client(login=msg.user.get('login'), pswd=msg.user.get('password'), ip=self.conn.getpeername())
        # users: dict = self.get_register_clients()
        # obj = {msg.user['login']: msg.user['password']}
        # users.update(obj)
        # with open(self.register_clients, 'w', encoding='utf-8') as f:
        #     json.dump(users, f)

    # def get_register_clients(self):
    #     with open(self.register_clients, 'r', encoding='utf-8') as f:
    #         try:
    #             return json.load(f)
    #         except JSONDecodeError:
    #             return {}

    def auth(self, msg: Message):
        users = self.db.get_clients()
        for user in users:
            if msg.user['login'] == user.login:
                if self.db.check_password(login=user.login, pswd=msg.user.get('password'), ip=self.conn.getpeername()[0]):
                    return True
                else:
                    return False
        self.__register_client(msg)
        return True




server_socket = socket()


# server_socket.bind(('', 55555)) # вызовет исключение Exception: Сокет используется
class ServerVerifier(type):
    def __init__(cls, name, bases, namespace):
        super(ServerVerifier, cls).__init__(name, bases, namespace)
        # проверка на отсутствие вызовов connect
        try:
            server_socket.getpeername()
            raise Exception('Сокет используется')
        except OSError:
            pass
        # проверка на использование сокетов для работы по TCP
        if server_socket.type.name != 'SOCK_STREAM':
            raise Exception('Сокет использует не TCP протокол')
        cls.socket = server_socket
        cls.host = ''
        cls.port = 55555

    def __call__(cls):
        return super(ServerVerifier, cls).__call__()


class Server(metaclass=ServerVerifier):
    listen = 5
    connections: list = []  # список подключенных клиентов
    register_clients = 'users.json'

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.listen)




client_socket = socket()


# client_socket.connect(('localhost', 55555)) # вызовет исключение Exception: Сокет используется
class ClientVerifier(type):
    def __init__(cls, name, bases, namespace):
        super(ClientVerifier, cls).__init__(name, bases, namespace)
        # проверка на отсутствие вызовов accept для сокетов
        try:
            client_socket.getsockname()
            raise Exception('Сокет используется')
        except OSError:
            pass
        # проверка на использование сокетов для работы по TCP
        if client_socket.type.name != 'SOCK_STREAM':
            raise Exception('Сокет использует не TCP протокол')
        cls.socket = client_socket

    def __call__(cls):
        return super(ClientVerifier, cls).__call__()


class Client(metaclass=ClientVerifier):
    host = 'localhost'
    port = 55555

    def __init__(self):
        self.socket.connect((self.host, self.port))
        self.client_name = None
        self.auth = False

    def send_message(self, msg: Message):
        msg = self.__parse_message(msg)
        self.socket.send(pickle.dumps(msg))

    def receive_message(self):
        msg = self.socket.recv(1024)
        msg = Message(**pickle.loads(msg).__dict__)
        if msg.action == 'auth':
            if msg.response == 'OK':
                self.auth = True
                self.client_name = msg.acc_from
        if msg.action == 'msg':
            if not msg.response:
                print(f'<<{msg.acc_from}>>: {msg.text}')
                return msg
        print(f'[*] action: {msg.action} [{msg.response}]')
        return msg

    def authorization(self, login: str, psw: str):
        user = {'login': login, 'password': psw}
        msg = Message(action='auth', user=user, acc_from=login)
        self.send_message(msg)

    def __parse_message(self, msg: Message):
        if msg.text:
            re_acc_to = re.search(r'<.*>', msg.text)
            if re_acc_to:
                acc_to = re_acc_to.group()
                msg.text = msg.text.replace(acc_to, '').strip()
                msg.acc_to = acc_to[1:-1].replace(' ', '').split(',')
        if self.client_name:
            msg.acc_from = self.client_name
        return msg
