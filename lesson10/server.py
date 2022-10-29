from chat import Server, Connection
from threading import Thread

if __name__ == "__main__":
    s = Server()

    while True:
        conn = Connection(*s.socket.accept())
        try:
            print('[*] new connection:', conn.addr)
        except Exception:
            print('cli go away')
