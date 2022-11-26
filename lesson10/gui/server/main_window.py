import sys
import threading
from typing import List

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, qApp

from lesson10.chat import Server, Connection
from lesson10.config import SERVER_HOST, PORT
from lesson10.gui.server.main_form import Ui_MainWindow
from lesson10.gui.server.modal_window import SettingsWindow


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.thread_server = None
        self.setupUi(self)
        self.initUi()
        self.host = SERVER_HOST
        self.port = PORT

    def initUi(self):
        self.pushButton.clicked.connect(self.thread_run_server)
        self.close_server.setEnabled(False)
        self.close_server.clicked.connect(qApp.quit)
        self.action.triggered.connect(self.open_settings)
        self.action_2.triggered.connect(qApp.quit)

    def open_settings(self):
        self.window_settings = SettingsWindow(parent=self)

    def thread_run_server(self):
        self.thread_server = threading.Thread(target=self.run_server, daemon=True).start()

    def run_server(self):
        s = Server(self.host, self.port)
        self.pushButton.setEnabled(False)
        self.close_server.setEnabled(True)
        self.statusbar.showMessage(f'Server is running on port {s.port}')
        while True:
            conn = Connection(*s.socket.accept(), observer=self)
            print('[*] new connection:', conn.addr)

    def update_table_active_users(self, client_list: List[Connection]):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        for client in client_list:
            self.tableWidget.insertRow(0)
            self.tableWidget.setItem(0, 0, QTableWidgetItem(str(client.client_name)))
            self.tableWidget.setItem(0, 1, QTableWidgetItem(str(client.addr[0])))
            self.tableWidget.setItem(0, 2, QTableWidgetItem(str(client.connect_time.strftime('%Y.%m.%d %H:%M:%S'))))

    def update_statistic(self, dct_stat: dict):
        self.tableWidget_stat.clearContents()
        self.tableWidget_stat.setRowCount(0)
        for key, value in dct_stat.items():
            self.tableWidget_stat.insertRow(0)
            self.tableWidget_stat.setItem(0, 0, QTableWidgetItem(key.client_name))
            self.tableWidget_stat.setItem(0, 1, QTableWidgetItem(str(value)))


def run_main_window():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()  # We set the form to be our ExampleApp (design)
    form.show()  # Show the form
    app.exec_()  # and execute the app


if __name__ == '__main__':  # if we're running file directly and not importing it
    run_main_window()  # run the main function
