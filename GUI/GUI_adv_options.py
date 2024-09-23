from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QSpacerItem, \
    QSizePolicy, QLineEdit

from GUI import GUI_file_upload, GUI_parameters
from control_panel import manage_params as mp

class AdvancedOptionsGUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(AdvancedOptionsGUI, self).__init__(parent)
        self.threshold_line_edit = QLineEdit('200')
        self.setMinimumHeight(400)
        self.setMinimumWidth(1100)
        self.setWindowTitle("AptaNext")
        self.message_group_box = QGroupBox("Advanced Options")
        self.create_message_group_box()
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.addWidget(self.message_group_box, 0, 0)


    def create_message_group_box(self):
        layout = QVBoxLayout()
        ok_button = QPushButton('OK')
        label = QLabel("Set a threshold to for data analysis."
                       "\n- What is your interested number of enriched sequences for later analysis")
        layout.addWidget(label)
        layout.addWidget(self.threshold_line_edit)
        layout.addWidget(ok_button)
        self.message_group_box.setLayout(layout)
        ok_button.clicked.connect(self.store_threshold_value)

    def store_threshold_value(self):
        thresh = self.threshold_line_edit.text()
        mp.save_seq_count_threshold(thresh)
        self.close()






if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = AdvancedOptionsGUI()

    w.show()
    sys.exit(app.exec_())
