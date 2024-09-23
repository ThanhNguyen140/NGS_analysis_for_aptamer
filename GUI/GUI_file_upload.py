import os
from functools import partial
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QGroupBox, QTextEdit, QFileDialog, QHBoxLayout, \
    QMessageBox, QLabel

import control_panel.manage_params as mp
#import control_panel.manage_db as mdb
#import control_panel.manage_motif_file as mmf
from GUI import GUI_check_tools, GUI_start, GUI_parameters, GUI_parameters_no_split
from win import win_no_file


home = str(Path.home())
#print(home)


class FileBrowserGUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.check_GUI = GUI_check_tools.CheckToolsGUI()
        self.temp_dict = {}
        self.setMinimumHeight(600)
        self.setMinimumWidth(800)
        self.setWindowTitle("File Management")
        self.input_files = []
        self.continue_group_box = QGroupBox()
        self.swap_dir_group_box = QGroupBox()
        self.swap_dir_group_box.setStyleSheet('border:none')
        self.merge_group_box = QGroupBox()
        self.output_contents_group_box = QGroupBox("Output Folder Contents")
        self.output_path_group_box = QGroupBox("Output File\Folder Path")
        self.output_file_group_box = QGroupBox()
        self.upload_contents_group_box = QGroupBox("Upload Folder Contents")
        self.upload_path_group_box = QGroupBox("Upload File\Folder Path")
        self.upload_files_group_box = QGroupBox()
        self.reverse_primers_group_box = QGroupBox('Reverse Primers')
        self.forward_primers_group_box = QGroupBox('Forward Primers')
        self.random_len_group_box = QGroupBox('Random Read Length')
        self.round_group_box = QGroupBox('Rounds')
        self.name_group_box = QGroupBox('Enter Project Name')
        self.back_group_box = QGroupBox()

        self.output_contents_text_edit = QTextEdit()
        self.upload_contents_text_edit = QTextEdit()
        self.reverse_primers_text_edit = QTextEdit()
        self.forward_primers_text_edit = QTextEdit()

        if mp.get_last_output_path():
            self.output_path_line_edit = QLineEdit(mp.get_last_output_path())
        else:
            self.output_path_line_edit = QLineEdit('Path preview here')

        self.upload_path_line_edit = QLineEdit('Path preview here')
        self.random_len_line_edit = QLineEdit()
        self.round_line_edit = QLineEdit()
        self.name_line_edit = QLineEdit()

        self.upload_files_button = QPushButton('Upload CSV File')
        self.csv_label = QLabel()
        self.csv_label.setText('Upload count_all_rounds.csv file')
        self.csv_label.setAlignment(Qt.AlignCenter)
        self.csv_label.setFont(QFont('Arial',8))
        
        self.upload_fastq_button = QPushButton('Upload FASTQ File(s)')
        self.fastq_label = QLabel()
        self.fastq_label.setText('Upload one or more .fastq files (decompressed)')
        self.fastq_label.setAlignment(Qt.AlignCenter)
        self.fastq_label.setFont(QFont('Arial',8))
        
        self.upload_gz_button = QPushButton('Upload FASTQ.gz File(s)')
        self.gz_label = QLabel()
        self.gz_label.setText('Upload one or more .gz.fastq files (compressed)')
        self.gz_label.setAlignment(Qt.AlignCenter)
        self.gz_label.setFont(QFont('Arial',8))
        
        self.output_files_button = QPushButton('Select Output Folder')
        self.same_as_input_button = QPushButton('Use Input Folder as Output')

        self.create_upload_contents_group_box()
        self.create_upload_files_group_box()

        self.create_upload_path_group_box()
        self.create_output_path_group_box()

        self.create_output_contents_group_box()
        self.create_output_folder_group_box()

        # self.create_merge_group_box()
        self.create_continue_group_box()
        self.create_back_group_box()
        self.create_swap_dir_group_box()

        self.create_rounds_group_box()
        self.create_random_len_group_box()

        self.create_forward_primers_group_box()
        self.create_reverse_primers_group_box()

        self.create_name_group_box()

        main_layout = QtWidgets.QGridLayout(self)

        main_layout.addWidget(self.upload_files_group_box, 0, 0)
        main_layout.addWidget(self.upload_contents_group_box, 2, 0)

        main_layout.addWidget(self.output_file_group_box, 0, 2)
        main_layout.addWidget(self.output_path_group_box, 1, 2)
        main_layout.addWidget(self.output_contents_group_box, 2, 2)

        main_layout.addWidget(self.swap_dir_group_box, 2, 1)

        main_layout.addWidget(self.continue_group_box, 7, 2)
        main_layout.addWidget(self.back_group_box, 7, 0)

    def create_rounds_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.round_line_edit)
        self.round_group_box.setLayout(layout)

    def create_random_len_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.random_len_line_edit)
        self.random_len_group_box.setLayout(layout)

    def create_forward_primers_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.forward_primers_text_edit)
        self.forward_primers_group_box.setLayout(layout)

    def create_reverse_primers_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.reverse_primers_text_edit)
        self.reverse_primers_group_box.setLayout(layout)

    def open_file_browser(self, input_or_output: str):
        if input_or_output == 'in':
            my_filter = "CSV file (*.csv)"
            filename = QFileDialog()
            filename.setFileMode(QFileDialog.ExistingFiles)

            if mp.get_last_files():
                path = os.path.dirname(mp.get_last_files()[0])

            else:
                path = str(Path.home())

            #print(mp.get_last_files(), 'last')

            filenames = filename.getOpenFileNames(self, 'Open file', path, my_filter)

        elif input_or_output =='out':
            filename = QFileDialog()

            if mp.get_last_output_path():
                path = mp.get_last_output_path()

            else:
                path = str(Path.home())

            #print(mp.get_last_output_path(), "out")
            filenames = filename.getExistingDirectory(self, 'Open file', path)


        if filenames:
            if input_or_output == 'in':
                #print(filenames[0][0])
                split_path = filenames[0][0].split('/')
                #print(split_path)
                dir_path = '/'.join(split_path[:-1])
                #print(dir_path)
                self.set_left_path_preview(filenames[0][0])
                #self.set_left_dir_preview(dir_path)

            elif input_or_output == 'out':
                self.set_right_path_preview(filenames)
                self.set_right_dir_preview(filenames)

    def get_fastq(self):
        self.no_split_button.setEnabled(False)
        self.split_button.setEnabled(True)
        my_filter = "Fastq files (*.fastq)"
        filename = QFileDialog()
        filename.setFileMode(QFileDialog.ExistingFiles)

        if mp.get_last_files():
            home = os.path.dirname(mp.get_last_files()[0])

        names = filename.getOpenFileNames(self, 'Open file', home, my_filter)
        #print(names)
        # names = '\n'.join(names[0])
        # print(names)
        self.set_left_dir_preview(names[0])

    def get_csv(self):
        self.split_button.setEnabled(False)
        self.no_split_button.setEnabled(True)
        my_filter = "CSV files (*.csv)"
        filename = QFileDialog()
        filename.setFileMode(QFileDialog.ExistingFiles)

        if mp.get_last_files():
            home = os.path.dirname(mp.get_last_files()[0])

        names = filename.getOpenFileNames(self, 'Open file', home, my_filter)
        #print(names)
        # names = '\n'.join(names[0])
        # print(names)
        self.set_left_dir_preview(names[0])
    
    def get_gz(self):
        self.no_split_button.setEnabled(False)
        self.split_button.setEnabled(True)
        my_filter = "FATQ.gz files (*.gz)"
        filename = QFileDialog()
        filename.setFileMode(QFileDialog.ExistingFiles)

        if mp.get_last_files():
            home = os.path.dirname(mp.get_last_files()[0])

        names = filename.getOpenFileNames(self, 'Open file', home, my_filter)
        #print(names)
        # names = '\n'.join(names[0])
        # print(names)
        self.set_left_dir_preview(names[0])


    def create_upload_files_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.upload_files_button)
        layout.addWidget(self.csv_label)
        layout.addWidget(self.upload_fastq_button)
        layout.addWidget(self.fastq_label)
        layout.addWidget(self.upload_gz_button)
        layout.addWidget(self.gz_label)
        self.upload_files_group_box.setLayout(layout)

        self.upload_files_button.clicked.connect(partial(self.get_csv))
        self.upload_fastq_button.clicked.connect(partial(self.get_fastq))
        self.upload_gz_button.clicked.connect(partial(self.get_gz))

    def create_upload_path_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.upload_path_line_edit)
        self.upload_path_group_box.setLayout(layout)

    def create_upload_contents_group_box(self):
        layout = QVBoxLayout()
        self.upload_contents_text_edit.setReadOnly(True)
        layout.addWidget(self.upload_contents_text_edit)
        self.upload_contents_group_box.setLayout(layout)
        self.upload_contents_group_box.setLayout(layout)

    def create_output_folder_group_box(self):
        layout = QVBoxLayout()
        #layout.addWidget(self.same_as_input_button)
        layout.addWidget(self.output_files_button)
        self.output_file_group_box.setLayout(layout)
        self.output_files_button.clicked.connect(partial(self.open_file_browser, 'out'))
        #self.same_as_input_button.clicked.connect(self.use_input_as_output)

    def create_output_path_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.output_path_line_edit)
        self.output_path_group_box.setLayout(layout)

    def create_output_contents_group_box(self):
        layout = QVBoxLayout()
        self.output_contents_text_edit.setReadOnly(True)
        layout.addWidget(self.output_contents_text_edit)
        self.output_contents_group_box.setLayout(layout)


    def create_swap_dir_group_box(self):
        swap_button = QPushButton()

        layout = QVBoxLayout()
        layout.addWidget(swap_button)

        self.swap_dir_group_box.setLayout(layout)
        swap_button.clicked.connect(self.swap_directories)

    def create_continue_group_box(self):
        self.split_button = QPushButton('Split Rounds')
        self.no_split_button = QPushButton('No Split')
        layout = QHBoxLayout()
        layout.addWidget(self.no_split_button)
        layout.addWidget(self.split_button)
        self.continue_group_box.setLayout(layout)

        self.split_button.clicked.connect(self.store_temp_metadata_split)
        self.no_split_button.clicked.connect(self.store_temp_metadata_no_split)



    def create_back_group_box(self):
        back_button = QPushButton("Back")
        layout = QHBoxLayout()
        layout.addWidget(back_button)
        self.back_group_box.setLayout(layout)
        back_button.clicked.connect(self.open_start_GUI)


    def create_name_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.name_line_edit)
        self.name_group_box.setLayout(layout)


    def open_fastq_warning(self):
        MessageBox = QMessageBox.about(self, "Warning", "Please Select a FASTQ File")


    def open_start_GUI(self):
        self.open_start = GUI_start.StartGUI()
        self.open_start.show()
        self.close()

    def open_parameters_GUI(self):
        self.open_parameters = GUI_parameters.ParametersGUI()
        self.open_parameters.show()
        self.close()
    
    def open_parameters_no_split_GUI(self):
        self.open_no_split = GUI_parameters_no_split.ParametersNoSplitGUI()
        self.open_no_split.show()
        self.close()

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()

    def set_left_path_preview(self, path):
        self.upload_path_line_edit.setText(path)

    def set_left_dir_preview(self, path):
        if type(path) is list:
            paths = '\n'.join(path)
            self.upload_contents_text_edit.setText(paths)

        elif type(path) is str:
            files = os.listdir(path)
            self.upload_contents_text_edit.setText('\n'.join(files))

        else:
            print("Path is not a list or string")

    def set_right_path_preview(self, path):
        self.output_path_line_edit.setText(path)

    def set_right_dir_preview(self, path):
        files = os.listdir(path)
        self.output_contents_text_edit.setText('\n'.join(files))

    def swap_directories(self):

        if self.output_path_line_edit.text() == 'Path preview here' and self.upload_path_line_edit.text() == 'Path preview here':
            pass
        else:
            org_dir = self.upload_contents_text_edit.toPlainText()
            org_path = self.upload_path_line_edit.text()
            self.upload_contents_text_edit.setText(self.output_contents_text_edit.toPlainText())
            self.output_contents_text_edit.setText(org_dir)
            self.upload_path_line_edit.setText(self.output_path_line_edit.text())
            self.output_path_line_edit.setText(org_path)

    def use_input_as_output(self):
        if self.output_path_line_edit.text() == 'Path preview here' and self.upload_path_line_edit.text() == 'Path preview here':
            pass
        else:
            org_dir = self.upload_contents_text_edit.toPlainText()
            org_path = self.upload_path_line_edit.text()
            self.output_contents_text_edit.setText(org_dir)
            self.output_path_line_edit.setText(org_path)

    def get_files(self):
        files = self.upload_contents_text_edit.toPlainText()

        self.input_files = files.split('\n')

        fastq_files = [x for x in self.input_files if '.fastq' in x or '.csv' in x or '.gz']
 

        if len(fastq_files) == 0:
            print(len(fastq_files))
            self.open_fastq_warning
        else:
            return fastq_files


    def get_output_path(self):
        output_path = self.output_path_line_edit.text()
        return output_path


    def open_check_GUI(self):
        self.check_GUI.show()
        self.close()

    def open_no_file_win(self):
        self.open_no_file = win_no_file.NoFileMessage()
        self.open_no_file.show()
        self.close()

    def open_parameters_GUI(self):
        self.open_parameters = GUI_parameters.ParametersGUI()
        self.open_parameters.show()
        self.close()

    def store_temp_metadata_split(self):
 
        if self.upload_contents_text_edit.toPlainText():
            print(self.upload_contents_text_edit.toPlainText())

        else:
            return self.open_no_file_win()


        fastq_files = self.get_files()
        output_path = self.get_output_path()

        mp.save_last_files(fastq_files)

        mp.save_output_path(output_path)

        self.open_parameters_GUI()


    def store_temp_metadata_no_split(self):

        if self.upload_contents_text_edit.toPlainText():
            print(self.upload_contents_text_edit.toPlainText())
            #print("yes")
        else:
            return self.open_no_file_win()


        csv_files = self.get_files()
        output_path = self.get_output_path()

        mp.save_last_files(csv_files)

        mp.save_output_path(output_path)

        self.open_parameters_no_split_GUI()