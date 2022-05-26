import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from back import Back


class UiMainWindow(QMainWindow):
    fetched = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.select = ""

        self.setObjectName("MainWindow")
        self.resize(577, 264)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 120, 411, 22))
        self.lineEdit.setObjectName("lineEdit")

        self.but_1 = QtWidgets.QPushButton(self.centralwidget)
        self.but_1.setGeometry(QtCore.QRect(470, 120, 93, 31))
        self.but_1.setObjectName("pushButton")
        self.but_1.clicked.connect(self.browse)

        self.but_2 = QtWidgets.QPushButton(self.centralwidget)
        self.but_2.setGeometry(QtCore.QRect(30, 180, 93, 28))
        self.but_2.setObjectName("pushButton_2")
        self.but_2.clicked.connect(self.proceed)

        self.but_3 = QtWidgets.QPushButton(self.centralwidget)
        self.but_3.setGeometry(QtCore.QRect(470, 180, 93, 28))
        self.but_3.setObjectName("pushButton_3")
        self.but_3.clicked.connect(self.cancel)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 45, 171, 21))
        self.label.setObjectName("label")

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 577, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.initui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def initui(self):
        self.setWindowTitle("MainWindow")
        self.but_1.setText("Browse...")
        self.but_2.setText("OK")
        self.but_3.setText("Cancel")
        self.label.setText("Choose file to process")

    def cancel(self):
        self.close()

    def browse(self):
        self.lineEdit.setText(QFileDialog.getOpenFileName()[0])

    def proceed(self):
        self.select = self.lineEdit.text()
        self.close()
        Back.do_main(self.select)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UiMainWindow()
    window.show()
    sys.exit(app.exec_())
