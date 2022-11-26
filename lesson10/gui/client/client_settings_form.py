import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


class Ui_SettingsWindow():
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 250)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 25, 48, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 65, 50, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 70, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 150, 73, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.txt_host = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_host.setGeometry(QtCore.QRect(67, 22, 300, 30))
        self.txt_host.setObjectName("txt_host")
        self.txt_port = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_port.setGeometry(QtCore.QRect(67, 62, 300, 30))
        self.txt_port.setObjectName("txt_port")
        self.txt_login = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_login.setGeometry(QtCore.QRect(88, 106, 279, 30))
        self.txt_login.setObjectName("txt_login")
        self.txt_password = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_password.setGeometry(QtCore.QRect(88, 146, 279, 30))
        self.txt_password.setObjectName("txt_password")

        self.btn_save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(105, 195, 110, 35))
        self.btn_save.setObjectName("btn_save")
        self.btn_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cancel.setGeometry(QtCore.QRect(240, 195, 110, 35))
        self.btn_cancel.setObjectName("btn_cancel")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.connect_signals_slots()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Настройки соединения"))
        self.label.setText(_translate("MainWindow", "Хост:"))
        self.label_2.setText(_translate("MainWindow", "Порт:"))
        self.txt_host.setPlaceholderText(_translate("MainWindow", "хост..."))
        self.txt_port.setPlaceholderText(_translate("MainWindow", "порт..."))
        self.label_3.setText(_translate("MainWindow", "Логин:"))
        self.label_4.setText(_translate("MainWindow", "Пароль:"))
        self.txt_login.setPlaceholderText(_translate("MainWindow", "Ваш логин..."))
        self.txt_password.setPlaceholderText(_translate("MainWindow", "Ваш пароль..."))

        self.btn_save.setText(_translate("MainWindow", "Сохранить"))
        self.btn_cancel.setText(_translate("MainWindow", "Отменить"))

    def connect_signals_slots(self):
        self.btn_cancel.clicked.connect(self._close_settings)
        self.btn_save.clicked.connect(self._save_settings)

    def _close_settings(self):
        self.instance.close()

    def _save_settings(self):
        self.parent_window.login = self.txt_login.text()
        self.parent_window.password = self.txt_password.text()
        self.parent_window.host = self.txt_host.text()
        self.parent_window.port = int(self.txt_port.text())

        self._close_settings()


class SettingsWindow(QMainWindow, Ui_SettingsWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.instance = self
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.parent_window = None
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SettingsWindow()
    sys.exit(app.exec_())
