import datetime
import json
import socket
from threading import Thread

SERVER_HOST = "0.0.0.0"  # IP- адрес сервера
SERVER_PORT = 5002  # порт сервера
# список зарегистрированных пользователей
registered_clients = {"john": "123", "jack": "1234"}

# инициализируем dict для всех подключенных клиентских сокетов
client_sockets = {}
# создаем TCP сокет
s = socket.socket()
# делаем порт многоразовым
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# привязать сокет к указанному адресу
s.bind((SERVER_HOST, SERVER_PORT))
# слушать предстоящие соединения
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


def send_message(sock: socket.socket, **kwargs) -> None:
    """Отправка сообщений"""
    # создание объекта сообщения
    msg_obj = {'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    msg_obj.update(kwargs)
    # сериализация
    msg_str = json.dumps(msg_obj)
    # перевод в байтовый тип
    msg_str = msg_str.encode()
    # отправка
    sock.send(msg_str)


def proceccing_message(sock: socket.socket, msg: bytes) -> None:
    """Обработка входящих сообщений"""
    print(msg)
    msg_sock = None
    # перевод в строчный тип
    message = msg.decode()
    # десериализация
    message = json.loads(message)
    # переводим время в объект
    message['time'] = datetime.datetime.strptime(message['time'], '%Y-%m-%d %H:%M:%S')
    # дальнейшая обработка в зависимости от action
    if message.get('action') == 'authenticate':  # авторизация
        __authenticate(sock=sock, login=message.get('user').get('account_name'),
                       password=message.get('user').get('password'))
    if message.get('action') == 'msg':  # сообщения от пользователей пользователям
        # отправка служебного сообщения
        send_message(sock=sock, action='msg', response=200)
        acc_from = message.get('account_from')
        msg = message.get('message')
        # определяем кому необходимо переслать сообщение
        acc_to = message.get('account_to')
        if acc_to:
            # если указан конкретный получатель, то из списка клиентских сокетов получаем его сокет и
            # отправляем ему сообщение
            for cl_sock, cl_name in client_sockets.items():
                if cl_name == acc_to:
                    msg_sock = cl_sock
                    break
            send_message(sock=msg_sock, action='msg', account_from=acc_from, account_to=acc_to, message=msg)
        # иначе, отправляем всем пользователям из client_sockets
        else:
            for cl_socket in client_sockets.keys():
                if sock != cl_socket:
                    send_message(sock=cl_socket, action='msg', account_from=acc_from, account_to=acc_to, message=msg)

def __authenticate(sock: socket.socket, login: [str, int], password: [str, int]) -> None:
    """
    Проверяет есть пользователь в client_sockets и совпадает ли пароль
    Если пользователя нет, то запускается процесс регистрации с добавлением пользователя и пароля в client_sockets
    """
    auth: bool = False
    if registered_clients.get(login):
        if registered_clients.get(login) != password:
            send_message(sock=sock, action='authenticate', response=402)
    else:
        __registration(login, password)
        auth = True
    if auth:
        send_message(sock=sock, action='authenticate', response=200)
        client_sockets[sock] = login


def __registration(login: [str, int], password: [str, int]) -> None:
    """Регистрация пользователя"""
    registered_clients[login] = password


def listen_for_client(cs):
    """
    Эта функция продолжает прослушивать сообщения из сокета `cs`
    """
    while True:
        try:
            msg = cs.recv(1024)
            proceccing_message(cs, msg)
        except Exception as e:
            # client no longer connected
            # remove it from the client_sockets
            print(f"[!] Error: {e}")
            client_sockets.pop(cs)


while True:
    # постоянно слушаем порт на наличие новых подключений
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # добавляем новый сокет в client_sockets
    client_sockets[client_socket] = ''
    # запустить новый поток, который прослушивает сообщения каждого клиента
    t = Thread(target=listen_for_client, args=(client_socket,))
    # сделать демон потока, чтобы он заканчивался всякий раз, когда заканчивается основной поток
    t.daemon = True
    # запускаем поток
    t.start()

# закрытие всех клиентских сокетов
for cs in client_sockets.keys():
    cs.close()
# закрытие серверного сокета
s.close()
