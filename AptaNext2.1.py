from GUI import GUI_start
from PyQt5 import QtWidgets
from constants import *
import os

if __name__ == '__main__':
    import sys
    try:
        os.mkdir(TEMP_FOLDER)
        os.mkdir(NGS_TEMP_FOLDER)
    except:
        pass
    app = QtWidgets.QApplication(sys.argv)
    w = GUI_start.StartGUI()

    w.show()
    sys.exit(app.exec_())
    