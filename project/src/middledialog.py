from PyQt5 import QtCore, QtWidgets


class UiMiddleDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setObjectName("Dialog")
        self.resize(383, 112)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.No | QtWidgets.QDialogButtonBox.Yes)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(50, 20, 201, 16))
        self.label.setObjectName("label")

        self.retranslate_ui()
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self):
        self.setWindowTitle("Dialog")
        self.label.setText("Do you want to change anything?")

    def on_accept(self):
        print("Yes was pressed")
        self.close()

    def on_reject(self):
        print("No was pressed")
        self.close()
