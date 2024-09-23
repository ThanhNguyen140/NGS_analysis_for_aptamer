from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel

from GUI import GUI_parameters
import control_panel.manage_params as mp
import control_panel.manage_db as mdb
import control_panel.manage_ngs as mngs


class StringError(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(StringError, self).__init__(parent)
        self.setMinimumHeight(400)
        self.setMinimumWidth(1100)
        self.setWindowTitle("AptaNext - No File")
        self.message_group_box = QGroupBox()
        self.button_group_box = QGroupBox()
        self.create_message_group_box()
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.addWidget(self.message_group_box, 0, 0)
        main_layout.addWidget(self.button_group_box, 1, 0)



    def create_message_group_box(self):
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        back_button = QPushButton('Back')
        #create_ok_button = QPushButton('Quit Program')
        label_1 = QLabel('NAME ERROR: Please enter only a-z and underscore characters')
        layout1.addWidget(label_1)
        layout2.addWidget(back_button)
        #layout2.addWidget(create_ok_button)

        self.message_group_box.setLayout(layout1)
        self.button_group_box.setLayout(layout2)

        #create_ok_button.clicked.connect(self.end_program)
        back_button.clicked.connect(self.close)

    def open_parameters_GUI(self):
        self.open_parameters = GUI_parameters.ParametersGUI()
        self.open_parameters.show()
        self.close()

    def end_program(self):
        mdb.close_connection()
        self.close()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = StringError()

    w.show()
    sys.exit(app.exec_())
