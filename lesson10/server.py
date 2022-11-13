from chat import Server, Connection
from threading import Thread

if __name__ == "__main__":
    s = Server()

    def rec():
        while True:
            conn.receive_msg()


    while True:
        conn = Connection(*s.socket.accept())
        t = Thread(target=rec)
        t.daemon = True
        t.start()
        try:
            print('[*] new connection:', conn.addr)
        except Exception:
            print('cli go away')
