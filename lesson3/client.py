import json
import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init
import time
import re

# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
          Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
          Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
          Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
          ]

# choose a random color for the client
client_color = random.choice(colors)

# подключаемся к серверу
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

name = '' # имя пользователя, присваивается в процессе авторизации

# отправка сообщения
def send_message(**kwargs)->None:
    """
    отправляет сообщение, предварительно создавая обьект сообщения в виде словаря, сериализует этот обьект,
    переводит в байтовый тип
    """
    # создание объекта сообщения
    msg_obj = {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    msg_obj.update(kwargs)
    if msg_obj.get('message'):
        # пробуем вытащить из сообщения конкретного получателя
        re_acc_to = re.search(r'<.*>', msg_obj.get('message'))
        if re_acc_to:
            acc_to = re_acc_to.group()
            msg_obj['message'] = msg_obj['message'].replace(acc_to, '').strip()
            acc_to = acc_to[1:-1]

            msg_obj['account_to'] = acc_to
        msg_obj['message'] = f'{client_color}{msg_obj["message"]}{Fore.RESET}'
    # сериализация
    msg_str = json.dumps(msg_obj)
    # перевод в байтовый тип
    msg_str = msg_str.encode()
    # отправка
    s.send(msg_str)
    print('')


def auth()-> None:
    """Авторизация"""
    global name
    # запрашиваем у пользователя его имя и пароль
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    user = {'account_name': name, 'password': password}
    # отправляем данные на сервер
    send_message(action='authenticate', user=user)
    # получаем ответ от сервера
    resp = s.recv(1024)
    # print(resp)
    # отправляем ответ на обработку
    proceccing_message(resp)


def proceccing_message(msg: bytes)->None:
    """Обработка входящих сообщений"""
    # перевод в строчный тип
    message = msg.decode()
    # десериализация
    message = json.loads(message)
    # переводим время в объект
    message['time'] = datetime.strptime(message['time'], '%Y-%m-%d %H:%M:%S')
    # дальнейшая обработка в зависимости от action
    if message.get('action') == 'authenticate':
        if message.get('response') == 200:
            print("Приветствуем Вас в нашем чате")
        else:
            print("Неправильный логин/пароль")
            auth()
    if message.get('action') == 'msg':
        if message.get('response') != 200 and message.get('response') is not None:
            print("Ошибка при доставке сообщения на сервер")
        elif message.get('response') is None:
            print(f"[{message['time']}] {message.get('account_from')}: {message.get('message')}")


def listen_for_messages()->None:
    """Прием входящих сообщений"""
    while True:
        message = s.recv(1024)
        # print(message)
        # отправляем ответ на обработку
        proceccing_message(message)

# запуск процесса авторизации
auth()

# создание отдельного потока на приём сообщений
t = Thread(target=listen_for_messages)
# сделать демон потока, чтобы он заканчивался всякий раз, когда заканчивается основной поток
t.daemon = True
# запускаем поток
t.start()


while True:
    # ждем, пока пользователь введет сообщение
    to_send = input()
    # выход из цикла и отключение от сервера
    if to_send.lower() == 'q':
        break

    send_message(action='msg', message=to_send, account_from=name)
    time.sleep(0.5)

# закрываем сокет
s.close()
