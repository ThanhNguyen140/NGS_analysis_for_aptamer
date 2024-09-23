from random import sample

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QGroupBox, QTextEdit, QPushButton, QMessageBox
#from qtconsole.qt import QtGui, QtCore

from GUI import GUI_start


class ScrambleSeqGUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ScrambleSeqGUI, self).__init__(parent)

        self.setMinimumHeight(600)
        self.setMinimumWidth(800)

        self.setWindowTitle("AptaNext - Scramble Sequence")
        app_icon = QtGui.QIcon()
        app_icon.addFile("AptaNext_Small-icon.png", QtCore.QSize(16, 16))
        self.setWindowIcon(app_icon)

        self.input_seq_group_box = QGroupBox('Input Sequence')
        self.input_seq_line_edit = QLineEdit()
        self.create_input_seq_group_box()

        self.num_of_seqs_group_box = QGroupBox('Number of Sequences')
        self.num_of_seqs_line_edit = QLineEdit()
        self.run_button = QPushButton('Scramble')
        self.back_button = QPushButton('Back')
        self.create_num_of_seqs_group_box()

        self.output_seqs_group_box = QGroupBox("Output Sequences")
        self.output_seqs_text_edit = QTextEdit()
        self.create_output_seqs_group_box()

        main_layout = QtWidgets.QGridLayout(self)

        main_layout.addWidget(self.input_seq_group_box, 0, 0)
        main_layout.addWidget(self.num_of_seqs_group_box, 1, 0)
        main_layout.addWidget(self.output_seqs_group_box, 2, 0)

    def create_input_seq_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.input_seq_line_edit)
        self.input_seq_group_box.setLayout(layout)

    def create_num_of_seqs_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.num_of_seqs_line_edit)
        layout.addWidget(self.run_button)
        self.num_of_seqs_group_box.setLayout(layout)

        self.run_button.clicked.connect(self.scramble_the_sequence)

    def create_output_seqs_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.output_seqs_text_edit)
        layout.addWidget(self.back_button)
        self.output_seqs_group_box.setLayout(layout)
        self.back_button.clicked.connect(self.open_start_GUI)

    def scramble_the_sequence(self):
        try: 
            number_of_seqs = int(self.num_of_seqs_line_edit.text())
            seq = self.input_seq_line_edit.text()

            scrambled_seqs = []

            for i in range(0, number_of_seqs):
                S = "".join(sample(seq, len(seq)))
                scrambled_seqs.append(S)

            scrambled_seqs = '\n'.join(scrambled_seqs)
            self.output_seqs_text_edit.setText(scrambled_seqs)
        except Exception as error:
                failed = QMessageBox()
                failed.setText(f"{type(error)} - {error}.\n")
                failed.exec_()

    def open_start_GUI(self):
        self.open_start = GUI_start.StartGUI()
        self.open_start.show()
        self.close()


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = ScrambleSeqGUI()

    w.show()
    sys.exit(app.exec_())