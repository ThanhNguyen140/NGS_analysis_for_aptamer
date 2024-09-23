from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel

from GUI import GUI_start
import control_panel.manage_params as mp
import control_panel.manage_db as mdb
import control_panel.manage_ngs as mngs
import control_panel.manage_motif_file as mmf


class FinishWindowMessage(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(FinishWindowMessage, self).__init__(parent)
        self.setMinimumHeight(400)
        self.setMinimumWidth(1100)
        self.setWindowTitle("AptaNext")
        self.message_group_box = QGroupBox()
        self.button_group_box = QGroupBox()
        self.create_message_group_box()
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.addWidget(self.message_group_box, 0, 0)
        main_layout.addWidget(self.button_group_box, 1, 0)



    def create_message_group_box(self):
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        back_button = QPushButton('Run another analysis')
        create_ok_button = QPushButton('Quit Program')
        label_1 = QLabel('Finished Analysis')
        layout1.addWidget(label_1)
        layout2.addWidget(back_button)
        layout2.addWidget(create_ok_button)

        self.message_group_box.setLayout(layout1)
        self.button_group_box.setLayout(layout2)

        create_ok_button.clicked.connect(self.end_program)
        back_button.clicked.connect(self.open_start_GUI)


    def open_start_GUI(self):
        self.open_start = GUI_start.StartGUI()
        self.open_start.show()
        self.close()

    def end_program(self):
        mdb.close_connection()
        self.close()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = FinishWindowMessage()

    w.show()
    sys.exit(app.exec_())
