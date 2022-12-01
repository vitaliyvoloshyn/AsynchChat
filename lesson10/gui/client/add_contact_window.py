import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


class UiAddContactWindow:
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 150)
        MainWindow.setWindowTitle('Добавить контакт')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lbl_name = QtWidgets.QLabel(self.centralwidget)
        self.lbl_name.setGeometry(QtCore.QRect(10, 20, 105, 40))
        self.lbl_name.setObjectName("lbl_name")
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lbl_name.setFont(font)
        self.lbl_name.setText("Имя контакта:")

        self.txt_name = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_name.setGeometry(QtCore.QRect(120, 25, 200, 30))
        self.txt_name.setObjectName("txt_name")
        self.txt_name.setPlaceholderText("Введите имя пользователя...")

        self.btn_add = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add.setGeometry(QtCore.QRect(70, 80, 110, 35))
        self.btn_add.setObjectName("btn_save")
        self.btn_add.setText("Добавить")
        self.btn_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cancel.setGeometry(QtCore.QRect(200, 80, 110, 35))
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.setText("Отменить")

        MainWindow.setCentralWidget(self.centralwidget)


class AddContactWindow(QMainWindow, UiAddContactWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui(self)
        self._parent = parent
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.connect_signals_slots()
        self.show()

    def connect_signals_slots(self):
        self.btn_cancel.clicked.connect(self._close_window)
        self.btn_add.clicked.connect(self._add)

    def _add(self):
        name = self._get_name()
        self._parent.add_contact(name)
        self._close_window()

    def _close_window(self):
        self.close()

    def _get_name(self):
        return self.txt_name.text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddContactWindow()
    sys.exit(app.exec_())
