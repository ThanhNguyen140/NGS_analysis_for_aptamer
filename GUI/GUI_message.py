# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 10:45:16 2023

@author: NGSAKMayer
"""

import sys
# ? import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets

  
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(713, 511)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(20, 30, 671, 461))
        self.tabWidget.setObjectName("tabWidget")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        font = QtGui.QFont()
        font.setPointSize(7)
        self.groupBox_Carga = QtWidgets.QGroupBox(self.tab1)
        self.groupBox_Carga.setEnabled(True)
        self.groupBox_Carga.setGeometry(QtCore.QRect(10, 90, 641, 161))
        self.groupBox_Carga.setObjectName("groupBox_Carga")
        self.toolButton = QtWidgets.QToolButton(self.groupBox_Carga)
        self.toolButton.setGeometry(QtCore.QRect(40, 30, 561, 31))
        self.toolButton.setObjectName("toolButton")
        self.groupBox_ConfMatcheo_4 = QtWidgets.QGroupBox(self.tab1)
        self.groupBox_ConfMatcheo_4.setEnabled(True)
        self.groupBox_ConfMatcheo_4.setGeometry(QtCore.QRect(10, 360, 641, 61))
        self.groupBox_ConfMatcheo_4.setFont(font)
        self.groupBox_ConfMatcheo_4.setObjectName("groupBox_ConfMatcheo_4")
        self.label = QtWidgets.QLabel(self.groupBox_ConfMatcheo_4)
        self.label.setGeometry(QtCore.QRect(80, 20, 521, 31))
        self.label.setObjectName("label")
        self.tabWidget.addTab(self.tab1, "")

        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.toolButton.setText(_translate("Dialog", "Load payments"))
        self.label.setText(_translate("Dialog", ""))


class Thread(QtCore.QThread):                                         # +++
    updateSignal = QtCore.pyqtSignal(int)                             # <----

    def __init__(self, value):                        
        super().__init__()  
        self.value = value

    def run(self):
        #it takes several minutes to execute this function
        for i in range(self.value):
            self.msleep(50)
            self.updateSignal.emit(i+1)                                # <----


class MainWindow(QtWidgets.QDialog, Ui_Dialog):                        # +++
    def __init__(self):                                      
        super().__init__()                                 
        
        self.setupUi(self)                                    
        
        value = 500
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setMaximum(value)
        self.progressBar.setGeometry(QtCore.QRect(20, 2, 700, 25))
        
        self.label.setText("Label")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("background-color: #D98C00;")
        
        self.toolButton.clicked.connect(self.press_button)
 
        self.thread = Thread(value)                               # <----
        self.thread.updateSignal.connect(self.update_progressBar) # <----
        self.thread.finished.connect(
            lambda: self.toolButton.setEnabled(True))

#    def complicated_function(self):
#        #it takes several minutes to execute this function
#        pass
        
    def update_progressBar(self, value):                           # <----     
        self.progressBar.setValue(value)

    def press_button(self):
        #omitted multiple lines of code
        #I'd like to initialize the progress bar here,
        #so the user knows the % of completion of complicated_function()
#        variable = self.complicated_function()

        self.thread.start()
        self.toolButton.setEnabled(False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
#    Dialog = QtWidgets.QMainWindow()
#    ui = Ui_Dialog()
#    ui.setupUi(Dialog)
#    Dialog.show()

    w = MainWindow()                                           # +++
    w.show()                                                   # +++
    
    sys.exit(app.exec_())