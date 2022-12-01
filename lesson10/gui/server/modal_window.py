from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow

from lesson10.config import SERVER_HOST, PORT

host = SERVER_HOST
port = PORT


class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.initUi()
        self.show()

    def initUi(self):
        self.resize(400, 150)
        self.setWindowTitle('Настройки сервера')
        self.label_host = QtWidgets.QLabel(self)
        self.label_host.setGeometry(QtCore.QRect(10, 20, 50, 20))
        self.label_host.setText('Хост:')
        self.label_port = QtWidgets.QLabel(self)
        self.label_port.setGeometry(QtCore.QRect(10, 60, 50, 20))
        self.label_port.setText('Порт:')
        self.txt_host = QtWidgets.QLineEdit(self)
        self.txt_host.setGeometry(QtCore.QRect(55, 20, 220, 25))
        self.txt_host.setPlaceholderText('host...')
        self.txt_host.setText(SERVER_HOST)
        self.txt_port = QtWidgets.QLineEdit(self)
        self.txt_port.setGeometry(QtCore.QRect(55, 60, 220, 25))
        self.txt_port.setPlaceholderText('port...')
        self.txt_port.setText(str(PORT))
        self.btn_save = QtWidgets.QPushButton(self)
        self.btn_save.setGeometry(70, 100, 90, 30)
        self.btn_save.setText('Сохранить')
        self.btn_save.clicked.connect(self.set_server_param)

        self.btn_cancel = QtWidgets.QPushButton(self)
        self.btn_cancel.setGeometry(180, 100, 90, 30)
        self.btn_cancel.setText('Отмена')
        self.btn_cancel.clicked.connect(self.hide)

    def set_server_param(self):
        self._parent.port = int(self.txt_port.text())
        self._parent.host = self.txt_host.text()
        self.close()
