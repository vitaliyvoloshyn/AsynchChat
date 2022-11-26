import sys
from typing import List

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, qApp

from lesson10.chat import Client, Message
from lesson10.config import LOGIN, PASSWORD, CLIENT_HOST, PORT
from lesson10.gui.client.add_contact_window import AddContactWindow
from lesson10.gui.client.client_settings_form import SettingsWindow
from lesson10.gui.client.del_contact_window import DelContactWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(855, 540)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 60, 80, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 60, 80, 16))
        self.label_2.setObjectName("label_2")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 80, 151, 380))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setSelectionMode(2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(180, 360, 170, 16))
        self.label_3.setObjectName("label_3")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(180, 380, 661, 51))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(740, 440, 101, 32))
        self.pushButton.setObjectName("pushButton")

        self.btn_connect = QtWidgets.QPushButton(self.centralwidget)
        self.btn_connect.setGeometry(QtCore.QRect(10, 10, 200, 32))
        self.btn_connect.setObjectName("pushButton")
        self.btn_disconnect = QtWidgets.QPushButton(self.centralwidget)
        self.btn_disconnect.setGeometry(QtCore.QRect(220, 10, 200, 32))
        self.btn_disconnect.setObjectName("pushButton")
        self.btn_add_contact = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add_contact.setGeometry(QtCore.QRect(530, 10, 150, 32))
        self.btn_add_contact.setObjectName("pushButton")
        self.btn_del_contact = QtWidgets.QPushButton(self.centralwidget)
        self.btn_del_contact.setGeometry(QtCore.QRect(690, 10, 150, 32))
        self.btn_del_contact.setObjectName("pushButton")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(180, 80, 661, 271))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 855, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Контакты:"))
        self.label_2.setText(_translate("MainWindow", "Окно чата:"))
        self.label_3.setText(_translate("MainWindow", "Отправка сообщений:"))
        self.pushButton.setText(_translate("MainWindow", "Отправить"))
        self.btn_connect.setText(_translate("MainWindow", "Подключиться к серверу"))
        self.btn_disconnect.setText(_translate("MainWindow", "Отключиться от сервера"))
        self.btn_add_contact.setText(_translate("MainWindow", "Добавить контакт"))
        self.btn_del_contact.setText(_translate("MainWindow", "Удалить контакт"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.action.setText(_translate("MainWindow", "Настройки соединения"))
        self.action_2.setText(_translate("MainWindow", "Выход"))


class HtmlMessage:
    def __init__(self):
        self._html = ''

    def add_out_message(self, text: str):
        self._html = f'<p align=\"left\">&#60;&#8722;&#8722;&#8722; {text}<br></p>'

    def add_in_message(self, text: str, author: str):
        self._html = f'<p align=\"right\">&#8722;&#8722;&#8722;&#62; ({author}): {text}<br></p>'

    def get_html(self):
        return self._html


class ClientWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ClientWindow, self).__init__()
        self.text_message = HtmlMessage()
        self.login = LOGIN
        self.password = PASSWORD
        self.host = CLIENT_HOST
        self.port = PORT
        self.cl_socket = None
        self.setupUi(self)
        self.initui()

    def initui(self):
        self.btn_disconnect.setEnabled(False)
        self.btn_add_contact.setEnabled(False)
        self.btn_del_contact.setEnabled(False)
        self.pushButton.setEnabled(False)

        self.action.triggered.connect(self._open_settings_window)
        self.action_2.triggered.connect(qApp.quit)
        self.pushButton.clicked.connect(self._send_user_message)
        self.btn_connect.clicked.connect(self._connect_to_server)
        self.btn_disconnect.clicked.connect(self._disconnect)
        self.btn_add_contact.clicked.connect(self._open_add_contact_window)
        self.btn_del_contact.clicked.connect(self._open_del_contact_window)

        self.statusbar.showMessage('disconnect...')

    def _open_add_contact_window(self):
        self.add_contact_window = AddContactWindow(parent=self)

    def _open_del_contact_window(self):
        self.del_contact_window = DelContactWindow(parent=self)

    def add_contact(self, user_name: str):
        self._send_to_server(Message(action='add_contact', add_client=user_name))

    def del_contact(self, user_name: str):
        self._send_to_server(Message(action='del_contact', del_client=user_name))

    def _get_user_text(self):
        message = self.plainTextEdit.toPlainText().strip('\n')
        self._clear_window_message()
        return message

    def _clear_window_message(self):
        self.plainTextEdit.clear()

    def _update_text_edit(self):
        self.textEdit.insertHtml(self.text_message.get_html())
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textEdit.setTextCursor(cursor)

    def _send_user_message(self):
        message = self._get_user_text()
        message = self._processing_message(message)
        self.text_message.add_out_message(message)
        self._update_text_edit()
        self._send_to_server(Message(action='msg', text=message))

    def _processing_message(self, text_message: str):
        """Вставка в сообщение пользователя контактов получателей"""
        receivers = self._get_selected_contacts()
        if receivers:
            receivers = ', '.join(receivers)  # преобразовываем в строку
            return f'<{receivers}> {text_message}'
        return text_message

    def _get_selected_contacts(self):
        selected_items = [item.text() for item in self.listWidget.selectedItems()]
        return selected_items

    def _send_to_server(self, msg: Message):
        self.cl_socket.send_message(msg)

    def update_contacts_list(self, contacts: List[str]):
        self.listWidget.clear()
        for contact in contacts:
            self.listWidget.insertItem(0, contact)

    def print_incoming_message(self, message: str, author: str):
        self.text_message.add_in_message(message, author)
        self._update_text_edit()

    def _open_settings_window(self):
        self.settings_window = SettingsWindow()
        self.settings_window.parent_window = self
        self.settings_window.txt_host.setText(self.host)
        self.settings_window.txt_port.setText(str(self.port))
        self.settings_window.txt_login.setText(self.login)
        self.settings_window.txt_password.setText(self.password)

    def _disconnect(self):
        self.cl_socket.socket.close()
        self.btn_connect.setEnabled(True)
        self.btn_disconnect.setEnabled(False)
        self.btn_add_contact.setEnabled(False)
        self.btn_del_contact.setEnabled(False)
        self.pushButton.setEnabled(False)
        self.statusbar.showMessage('disconnect...')

    def _connect_to_server(self):
        print(self.login)
        self.cl_socket = Client(self.host, self.port, self.login, self.password, self)

        self.btn_disconnect.setEnabled(True)
        self.btn_add_contact.setEnabled(True)
        self.btn_del_contact.setEnabled(True)
        self.pushButton.setEnabled(True)
        self.btn_connect.setEnabled(False)
        self.statusbar.showMessage('connect...')

        while self.cl_socket.auth:
            pass


def run_main_window():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = ClientWindow()  # We set the form to be our ExampleApp (design)
    form.show()  # Show the form
    sys.exit(app.exec())  # and execute the app


if __name__ == '__main__':  # if we're running file directly and not importing it
    run_main_window()  # run the main function
