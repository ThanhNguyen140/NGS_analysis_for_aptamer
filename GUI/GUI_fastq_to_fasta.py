import os
import sys
from pathlib import Path
from Bio import SeqIO
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QGroupBox, QFileDialog, QApplication, \
    QHBoxLayout, QLabel, QMessageBox

import control_panel.manage_params as mp
#import control_panel.manage_db as mdb


from GUI import GUI_start

home = str(Path.home())


class FastqToFasta(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(FastqToFasta, self).__init__(parent)
        self.setMinimumHeight(500)
        self.setMinimumWidth(900)
        self.setWindowTitle("AptaNext-FASTA/FASTQ Conversion")

        self.upload_group_box = QGroupBox()
        self.output_group_box = QGroupBox()
        self.back_group_box = QGroupBox()

        self.upload_button = QPushButton("Upload File Path")
        self.convert_button = QPushButton("Convert File")
        self.description = QLabel("Automatically detects the file type and saves the converted file to the same folder as the original.")
        self.upload_line_edit = QLineEdit()
        self.output_line_edit = QLabel()


        main_layout = QtWidgets.QGridLayout(self)

        main_layout.addWidget(self.upload_group_box, 0, 0)
        main_layout.addWidget(self.output_group_box, 1, 0)
        main_layout.addWidget(self.back_group_box, 2, 0)

        self.create_back_group_box()
        self.create_output_group_box()
        self.create_upload_group_box()

    def create_upload_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.description)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.upload_line_edit)
        self.upload_group_box.setLayout(layout)
        self.upload_button.clicked.connect(self.open_file_browser)

    def create_output_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.convert_button)
        layout.addWidget(self.output_line_edit)
        self.output_group_box.setLayout(layout)
        self.convert_button.clicked.connect(self.run_conversion)

    def create_back_group_box(self):
        back_button = QPushButton("Back")
        layout = QHBoxLayout()
        layout.addWidget(back_button)
        self.back_group_box.setLayout(layout)
        back_button.clicked.connect(self.open_start_GUI)

    def open_file_browser(self, input_or_output: str):
        my_filter = "fastq file (*.fastq);;fasta file (*.fasta)"
        filename = QFileDialog()
        filename.setFileMode(QFileDialog.ExistingFiles)

        if mp.get_last_files():
            home = os.path.dirname(mp.get_last_files()[0])

        file_path = filename.getOpenFileName(self, 'Open file', home, my_filter)[0]
        print(file_path)
        self.upload_line_edit.setText(file_path)

    def run_conversion(self):
        try: 
            if '.fastq' in self.upload_line_edit.text():
                self.fastq_to_fasta(self.upload_line_edit.text())

            elif '.fasta' in self.upload_line_edit.text():
                self.fasta_to_fastq(self.upload_line_edit.text())
        except Exception as error:
                failed = QMessageBox()
                failed.setText(f"{type(error)} - {error}.\n")
                failed.exec_()


    def fastq_to_fasta(self, fastq_file: str, fasta_file: str = None):
        if fasta_file == None:
            fasta_file = fastq_file.replace(".fastq", ".fasta")

        SeqIO.convert(fastq_file, "fastq", fasta_file, "fasta")
        self.output_line_edit.setText("Done: FASTA File Created")

    def fasta_to_fastq(self, fasta_file: str, fastq_file: str = None):
        if fastq_file == None:
            fastq_file = fasta_file.replace(".fasta", ".fastq")

        # make fastq
        with open(fasta_file, "r") as fasta, open(fastq_file, "w") as fastq:
            for record in SeqIO.parse(fasta, "fasta"):
                record.letter_annotations["phred_quality"] = [40] * len(record)
                SeqIO.write(record, fastq, "fastq")

        self.output_line_edit.setText("Done: FASTQ File Created")

    def open_start_GUI(self):
        self.open_start = GUI_start.StartGUI()
        self.open_start.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FastqToFasta()
    window.show()
    sys.exit(app.exec_())