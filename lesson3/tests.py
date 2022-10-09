import socket
import unittest


class ServerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.SERVER_HOST = "127.0.0.1"
        self.SERVER_PORT = 5002
        self.s = socket.socket()
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.s.listen(5)


    def test_create_socket(self):
        sock = socket.socket()
        sock.connect((self.SERVER_HOST, self.SERVER_PORT))
        client_socket, client_address = self.s.accept()
        self.assertIsNotNone(client_socket)
        self.assertIsNotNone(client_address)
        sock.close()
        self.s.close()
