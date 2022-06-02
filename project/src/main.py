import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from controller import Controller


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

        self.genes_per_cell_min = QtWidgets.QLineEdit(self.centralwidget)
        self.genes_per_cell_min.setGeometry(QtCore.QRect(30, 90, 411, 22))
        self.genes_per_cell_min.setObjectName("lineParameters1")

        self.but_2 = QtWidgets.QPushButton(self.centralwidget)
        self.but_2.setGeometry(QtCore.QRect(30, 180, 93, 28))
        self.but_2.setObjectName("pushButton_2")
        #------------------------v-link to backend-v--------------------------
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

    def initui(self):
        self.setWindowTitle("MainWindow")
        self.but_1.setText("Browse...")
        self.but_2.setText("OK")
        self.but_3.setText("Cancel")
        self.label.setText("Choose file to process")

    def cancel(self):
        self.close()

    def browse(self):
        str = QFileDialog.getOpenFileName()[0]
        print(str)
        self.lineEdit.setText(str)

    def proceed(self):
        self.close()
        controller = Controller()
        controller.run_back(self.lineEdit.text(), int(self.genes_per_cell_min.text()), 200, 0.0125, 3, 20)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UiMainWindow()
    window.show()
    sys.exit(app.exec_())
