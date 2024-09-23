from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QSpacerItem, \
    QSizePolicy

class WindowMessage(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(WindowMessage, self).__init__(parent)
        self.setMinimumHeight(400)
        self.setMinimumWidth(1100)
        self.setWindowTitle("AptaNext")
        self.message_group_box = QGroupBox()
        self.create_message_group_box()
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.addWidget(self.message_group_box, 0, 0)


    def create_message_group_box(self):
        layout = QVBoxLayout()
        create_ok_button = QPushButton('OK')
        label = QLabel()
        layout.addWidget(label)
        layout.addWidget(create_ok_button)

        self.message_group_box.setLayout(layout)
        #create_ok_button.clicked.connect(self.open_file_select_GUI)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = WindowMessage()

    w.show()
    sys.exit(app.exec_())
