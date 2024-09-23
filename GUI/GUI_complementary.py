from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QGroupBox, QPushButton, QCheckBox, QHBoxLayout, QMessageBox
#from qtconsole.qt import QtGui, QtCore
from GUI import GUI_start


class SequenceComplementGUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SequenceComplementGUI, self).__init__(parent)

        self.setMinimumHeight(300)
        self.setMinimumWidth(1500)

        self.setWindowTitle("AptaNext - Convert Sequence")
        app_icon = QtGui.QIcon()
        app_icon.addFile("AptaNext_Small-icon.png", QtCore.QSize(16, 16))
        self.setWindowIcon(app_icon)

        self.check_group_box = QGroupBox('Conversion Type')
        self.complement_check_box = QCheckBox('Complement Sequence')
        self.rev_complement_check_box = QCheckBox('Reverse Complement Sequence')
        self.create_check_group_box()

        self.input_seq_group_box = QGroupBox('Input Sequence')
        self.input_seq_line_edit = QLineEdit()
        self.run_button = QPushButton('Run')
        self.back_button = QPushButton('Back')
        self.create_input_seq_group_box()


        self.output_seqs_group_box = QGroupBox("Output Sequence")
        self.output_seqs_line_edit = QLineEdit()
        self.create_output_seqs_group_box()

        main_layout = QtWidgets.QGridLayout(self)

        main_layout.addWidget(self.check_group_box, 0, 0)
        main_layout.addWidget(self.input_seq_group_box, 1, 0)
        main_layout.addWidget(self.output_seqs_group_box, 2, 0)

    def create_check_group_box(self):
        layout = QHBoxLayout()
        self.complement_check_box.setChecked(True)
        layout.addWidget(self.complement_check_box)
        layout.addWidget(self.rev_complement_check_box)
        self.check_group_box.setLayout(layout)
        self.complement_check_box.toggled.connect(self.uncheck_rev_comp)
        self.rev_complement_check_box.toggled.connect(self.uncheck_comp)

    def uncheck_rev_comp(self):
        if self.rev_complement_check_box.isChecked() and self.complement_check_box.isChecked():
            self.rev_complement_check_box.setCheckState(False)

    def uncheck_comp(self):
        if self.complement_check_box.isChecked() and self.rev_complement_check_box.isChecked():
            self.complement_check_box.setCheckState(False)

    def create_input_seq_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.input_seq_line_edit)
        layout.addWidget(self.run_button)
        self.input_seq_group_box.setLayout(layout)
        self.run_button.clicked.connect(self.convert_sequence)


    def create_output_seqs_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.output_seqs_line_edit)
        layout.addWidget(self.back_button)
        self.output_seqs_group_box.setLayout(layout)
        self.back_button.clicked.connect(self.open_start_GUI)

    def convert_sequence(self):
        try: 
            replacements = {"A": "T", "T": "A", "C": "G", "G": "C"}
            seq = self.input_seq_line_edit.text().upper()
            comp = "".join([replacements.get(c, c) for c in seq])

            if self.complement_check_box.isChecked() and not self.rev_complement_check_box.isChecked():
                self.output_seqs_line_edit.setText(comp)

            elif self.rev_complement_check_box.isChecked() and not self.complement_check_box.isChecked():
                self.output_seqs_line_edit.setText(comp[::-1])
        except Exception as error:
                failed = QMessageBox()
                failed.setText(f"{type(error)} - {error}.\n")
                failed.exec_()


    def open_start_GUI(self):
        self.open_start = GUI_start.StartGUI()
        self.open_start.show()
        self.close()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = SequenceComplementGUI()

    w.show()
    sys.exit(app.exec_())