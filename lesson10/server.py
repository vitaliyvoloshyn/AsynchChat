from chat import Server, Connection

if __name__ == "__main__":
    s = Server()
    while True:
        conn = Connection(*s.socket.accept())
        print('[*] new connection:', conn.addr)
