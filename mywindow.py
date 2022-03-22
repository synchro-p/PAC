import sys

import pandas as pd
import scanpy as sc
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMainWindow


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
        filedialog = QFileDialog()
        filedialog.show()
        if filedialog.exec_():
            self.lineEdit.setText(filedialog.selectedFiles()[0])

    def proceed(self):
        self.select = self.lineEdit.text()
        self.fetched.emit()
        self.close()

    def selectedfile(self):
        return self.select


class Fetcher:
    def __init__(self):
        self.fetchedFile = 0
        self.ui = UiMainWindow()
        self.ui.fetched.connect(lambda: self.dostuff())

    def getfilefromuser(self):
        self.ui.show()

    def dostuff(self):
        adata = sc.read_csv(self.ui.selectedfile(), delimiter='\t')
        adata = adata.T

        pdata = pd.read_csv(self.ui.selectedfile(), delimiter='\t')

        sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
        sc.settings.set_figure_params(dpi=100, facecolor='white')

        sc.pl.highest_expr_genes(adata, n_top=15)

        sc.pp.filter_cells(adata, min_genes=500)
        sc.pp.filter_genes(adata, min_cells=200)

        sc.pp.normalize_total(adata, target_sum=1e4)

        sc.pp.log1p(adata)

        sc.pp.highly_variable_genes(adata)
        sc.pl.highly_variable_genes(adata)

        sc.pp.scale(adata)

        (adata.var.highly_variable == True).sum()

        sc.tl.pca(adata, n_comps=100)
        sc.pl.pca(adata)

        sc.pl.pca_variance_ratio(adata, n_pcs=100, log=True)

        sc.pl.pca_loadings(adata)

        sc.pl.pca(adata, color=['ML07214a', 'ML25764a', 'ML14383a'], ncols=3, hspace=0.1, wspace=0.2)

        sc.pl.pca(adata, color=['ML07214a', 'ML25764a', 'ML14383a'], ncols=3, hspace=20, wspace=0.2, projection='3d')

        sc.pp.neighbors(adata, n_neighbors=20, n_pcs=40)

        sc.tl.umap(adata)

        sc.tl.leiden(adata)
        sc.pl.umap(adata, color='leiden', palette='gist_ncar')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    fetcher = Fetcher()
    fetcher.getfilefromuser()
    sys.exit(app.exec_())
