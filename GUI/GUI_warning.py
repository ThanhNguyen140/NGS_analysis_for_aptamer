from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QCheckBox, QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QSpacerItem, \
    QSizePolicy


class WarningGUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(WarningGUI, self).__init__(parent)
        self.setMinimumHeight(400)
        self.setMinimumWidth(1100)
        self.setWindowTitle("Warning")

        self.warning_group_box = QGroupBox()
        self.create_warning_group_box()

        main_layout = QtWidgets.QGridLayout(self)

        main_layout.addWidget(self.warning_group_box, 0, 0)

    def create_warning_group_box(self):
        layout = QVBoxLayout()
        create_ok_button = QPushButton('Ok')
        #h_spacer = QSpacerItem(200, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        label = QLabel("Please Select a FASTQ File")
        layout.addWidget(label)
        layout.addWidget(create_ok_button)
        self.warning_group_box.setLayout(layout)
        #create_ok_button.clicked.connect()

    def close_window(self):
        self.close()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = WarningGUI()

    w.show()
    sys.exit(app.exec_())
