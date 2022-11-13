import pickle
import time
from socket import socket
from threading import Thread

from chat import Client, Message


def rec():
    while True:
        socke.receive_message()


socke = Client()
t = Thread(target=rec)
t.start()
time.sleep(0.5)
while True:
    login = input('Введите свой логин: ')
    psw = input('Введите пароль: ')
    socke.authorization(login, psw)
    time.sleep(1)
    if socke.auth:
        socke.add_contact('bob')
        time.sleep(1)

        socke.get_contacts()
        print('*' * 50)
        print("Приветствуем Вас в нашем чате!")
        print("Для отправки сообщения всем активным учасникам наберите текст сообщения и отправьте\n"
              "Чтоб отправить сообщение конкретному(ным) получателям необходимо указать их логины, напр\n"
              "<user1, user2, user3> my_message")
        print('*' * 50)
        break
while True:
    text_msg = input()
    if text_msg == 'q':
        break
    mess = Message(action='msg', text=text_msg)
    socke.send_message(mess)
socke.socket.close()
