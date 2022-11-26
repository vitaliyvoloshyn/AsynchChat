import pickle
import queue
import re
import threading
from datetime import datetime
from socket import socket

from lesson10.storage.create_database import create_server_database, create_client_database


class Message:
    def __init__(self, **kwargs):
        self.response = kwargs.get('response')
        self.code = kwargs.get('code')
        self.time = kwargs.get('time') or datetime.now()
        self.action = kwargs.get('action')
        self.text = kwargs.get('text')
        self.acc_to = kwargs.get('acc_to')
        self.acc_from = kwargs.get('acc_from')
        self.user = kwargs.get('user')
        self.add_client = kwargs.get('add_client')
        self.del_client = kwargs.get('del_client')

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


class Connection:

    def __init__(self, *args, **kwargs):
        self.conn: socket = args[0]
        self.addr = args[1]
        self.quene = queue.Queue()
        self.client_name = None
        self.connect_time = datetime.now()
        self.client_pswd = None
        self.in_message = None
        self.observer: object = kwargs.get('observer')
        self.__send_response(Message(response='OK', code=200, action='connecting', acc_to=[self.conn]))
        self.db = create_server_database()
        threading.Thread(target=self.receive_msg).start()
        threading.Thread(target=self.processing_message).start()
        self.__add_obj_to_connections_list()

    def notify(self):
        self.observer.update_table_active_users(Server.connections)

    def remove_instance_from_list(self):
        Server.connections.pop(self)
        self.notify()

    def __add_obj_to_connections_list(self):
        Server.connections.update({self: 0})
        self.notify()

    def _update_statistic(self, conn):
        Server.connections[conn] += 1
        self.observer.update_statistic(Server.connections)

    def __send_response(self, obj_resp: Message) -> None:
        """создание ответа на подключение"""
        self.send_message(obj_resp)

    def send_message(self, msg: Message):
        """Отправка сообшения"""
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
                self.quene.put(msg)
            except ConnectionResetError as e:
                print(f"Клиент {self.client_name} отключился")
                self.remove_instance_from_list()
                self.observer.update_statistic(Server.connections)
                break

    def processing_message(self):
        while True:
            self.in_message = pickle.loads(self.quene.get())
            if self.in_message.action == 'msg':
                resp = Message(response='OK', code=200, action='msg', acc_to=[self.conn])
                print(f'[*] <{self.client_name}>: {self.in_message.text}')
                self._update_statistic(self)
                self.__forward_msg()
            elif 'auth' == self.in_message.action:
                if self.auth(self.in_message):
                    self.client_name = self.in_message.user['login']
                    self.notify()
                    resp = Message(action='auth', response='OK', code=200, acc_to=[self.conn])
                else:
                    resp = Message(action='auth', code=400, response='Invalid password', acc_to=[self.conn])
            elif self.in_message.action == "get_contacts":
                try:
                    clients = self.db.get_contacts_by_user_name(user_name=self.in_message.acc_from)
                    resp = Message(action='get_contacts', code=202, response=clients, acc_to=[self.conn])
                except Exception:
                    resp = Message(action='get_contacts', code=500, response='Internal error', acc_to=[self.conn])
            elif self.in_message.action == "add_contact":
                try:
                    self.db.add_contact(owner=self.in_message.acc_from, user=self.in_message.add_client)
                    clients = self.db.get_contacts_by_user_name(user_name=self.in_message.acc_from)
                    resp = Message(action='add_contact', code=202, response=clients, acc_to=[self.conn])
                except Exception:
                    resp = Message(action='add_contact', code=500, response="user does not exist", acc_to=[self.conn])
            elif self.in_message.action == 'del_contact':
                try:
                    self.db.del_contact(owner=self.in_message.acc_from, contact=self.in_message.del_client)
                    clients = self.db.get_contacts_by_user_name(user_name=self.in_message.acc_from)
                    resp = Message(action='del_contact', code=202, response=clients, acc_to=[self.conn])
                except Exception:
                    resp = Message(action='del_contact', code=500, response="user does not exist", acc_to=[self.conn])
            self.send_message(resp)

    def __forward_msg(self):
        if self.in_message.acc_to:
            receivers = []
            for acc_to in self.in_message.acc_to:
                for client in Server.connections:
                    if acc_to == client.client_name:
                        receivers.append(client.conn)
                        break
            if not receivers:
                return
            self.in_message.acc_to = receivers
        self.in_message.acc_from = self.client_name
        self.send_message(self.in_message)

    def __getstate__(self) -> dict:
        """редактирует словарь обьекта под сериализацию"""
        attr = self.__dict__.copy()
        attr['conn'] = attr['conn'].__repr__()
        return attr

    def __register_client(self, msg: Message):
        """Внесение пользователя в БД (таблицу User)"""
        self.db.add_user(login=msg.user.get('login'), password=msg.user.get('password'))

    def __check_user_connect(self, ip: str, user: str):
        """Фиксация подключения пользователя - внесение данных в таблицу UserHistory"""
        self.db.add_history(ip=ip, user=user)

    def auth(self, msg: Message):
        users = self.db.get_users()
        if msg.user['login'] in users:
            if self.db.check_password(user=msg.user['login'], password=msg.user['password']):
                self.__check_user_connect(ip=self.conn.getpeername()[0], user=msg.user['login'])
                return True
            else:
                return False
        self.__register_client(msg)
        self.__check_user_connect(ip=self.conn.getpeername()[0], user=msg.user['login'])
        return True


class Server:
    listen = 5
    connections: dict = {}  # список подключенных клиентов
    observer: object = None
    register_clients = 'users.json'

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, host, port):
        self.socket = socket()
        self.host = host
        self.port = port

        try:
            self.socket.bind((host, port))
            self.socket.listen(self.listen)
            print(f'Сервер запущен на порту {self.port}')
        except OSError as e:
            print(e)
            exit(-1)


class Client:
    def __init__(self, host, port, login, password, window):
        self.socket = socket()
        self.socket.connect((host, port))
        self.form = window
        self.client_name = login
        self.password = password
        self.auth = False
        self.db = create_client_database()
        self.receive_thread = threading.Thread(target=self.receive_message, daemon=True)
        self.receive_thread.start()
        self.authorization(login, password)

    def send_message(self, msg: Message):
        msg = self.__parse_message(msg)
        self.socket.send(pickle.dumps(msg))

    def receive_message(self):
        while True:
            msg = self.socket.recv(1024)
            msg = Message(**pickle.loads(msg).__dict__)
            if msg.action == 'connecting':
                self.form.print_incoming_message(f'response: {msg.response}', '>>>connecting to server')
            if msg.action == 'auth':
                self.form.print_incoming_message(f'response: {msg.response}', '>>>authorization')
                if msg.response == 'OK':
                    self.auth = True
                    self.get_contacts()
            if msg.action == 'get_contacts':
                if msg.code == 202:
                    self.form.print_incoming_message(f'response: successful', '>>>get contacts')
                self.form.update_contacts_list(msg.response)
            if msg.action == 'add_contact':
                if msg.code == 202:
                    self.form.update_contacts_list(msg.response)
                    self.form.print_incoming_message(f'response: successful', '>>>add contact')
                else:
                    self.form.print_incoming_message(f'response: user does not exist', '>>>add contact')
            if msg.action == 'del_contact':
                if msg.code == 202:
                    self.form.update_contacts_list(msg.response)
                    self.form.print_incoming_message(f'response: successful', '>>>del contact')
                else:
                    self.form.print_incoming_message(f'response: user does not exist', '>>>del contact')

            if msg.action == 'msg':
                if not msg.response:
                    print(f'<<{msg.acc_from}>>: {msg.text}')
                    self.db.add_message(msg.acc_from, msg.text)
                    self.form.print_incoming_message(msg.text, msg.acc_from)
            print(f'[*] action: {msg.action}, response: {msg.response}')

    def authorization(self, login: str, psw: str):
        user = {'login': login, 'password': psw}
        msg = Message(action='auth', user=user, acc_from=login)
        self.client_name = login
        self.send_message(msg)

    def get_contacts(self):
        msg = Message(action='get_contacts', acc_from=self.client_name)
        self.send_message(msg)

    def add_contact(self, client):
        msg = Message(action='add_contact', acc_from=self.client_name, add_client=client)
        self.send_message(msg)

    def del_contact(self, client):
        msg = Message(action='del_contact', acc_from=self.client_name, del_client=client)
        self.send_message(msg)

    def __parse_message(self, msg: Message):
        if msg.text:
            re_acc_to = re.search(r'<.*>', msg.text)
            if re_acc_to:
                acc_to = re_acc_to.group()
                msg.text = msg.text.replace(acc_to, '').strip()
                msg.acc_to = acc_to[1:-1].replace(' ', '').split(',')
            self.db.add_message(self.client_name, msg.text)
        if self.client_name:
            msg.acc_from = self.client_name
        return msg
