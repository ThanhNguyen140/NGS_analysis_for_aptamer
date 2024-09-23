
import json
import os
from datetime import datetime

from pathlib import Path

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QLabel, QPushButton, QVBoxLayout, QLineEdit, QGroupBox, QTextEdit, QHBoxLayout,QMessageBox
#from qtconsole.qt import QtCore, QtGui

import control_panel.manage_params as mp
import control_panel.manage_db as mdb
import control_panel.manage_ngs as mngs
import control_panel.manage_files as mf
import tools.misc_tools as mt
from GUI import GUI_check_tools, GUI_start, GUI_file_upload, GUI_adv_options
from PyQt5.QtGui import QFont
from constants import *
from win import win_string_error


home = str(Path.home())
print(home)

class ParametersGUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()

        #self.motif_disc = GUI_motif_disc_win.MotifDiscWinGUI()
        self.temp_dict = {}
        #self.height = 1000
        #self.width = 1000
        self.setWindowTitle("Parameters")
        app_icon = QtGui.QIcon()
        app_icon.addFile("AptaNext_Small-icon.png", QtCore.QSize(16, 16))
        self.setWindowIcon(app_icon)
        self.input_files = []
        self.continue_group_box = QGroupBox()
        self.output_path_group_box = QGroupBox('Output Directory')

        self.reverse_primers_group_box = QGroupBox('Reverse Primers (Separated by comma or new line)')
        self.reverse_primer_info = QLabel()
        self.reverse_primer_info.setText("Primers should include barcodes for each round")
        self.reverse_primer_info.setFont(QFont('Arial', 8, italic = True))
        self.forward_primers_group_box = QGroupBox('Forward Primers (Separated by comma or new line)')
        self.forward_primer_info = QLabel()
        self.forward_primer_info.setText("Primers should include barcodes for each round")
        self.forward_primer_info.setFont(QFont('Arial', 8, italic = True))
        self.random_len_group_box = QGroupBox('Random Read Length')
        self.round_group_box = QGroupBox('Rounds (Separated by comma)')

    

        self.name_group_box = QGroupBox('Enter Project Name')
        self.options_group_box = QGroupBox("Advanced Options")
        self.forward_primers_text_edit = QTextEdit()
        self.reverse_primers_text_edit = QTextEdit()

        #self.motif_button = QPushButton("Motif Search")
        self.advanced_button = QPushButton("Set Abundance Threshold")
        #self.random_len_line_edit = QLineEdit()
        self.round_line_edit = QLineEdit()
        self.name_line_edit = QLineEdit()
        self.output_line_edit = QLineEdit()
        
        # Design buttons for editting random region lengths
        self.random_option = QGroupBox('Set random region')
        self.rr_length = QLineEdit('0')
        
        self.mutation = QGroupBox('Mutation in primers:')
        self.mut_label = QLabel()
        self.mut_label.setText("Please choose a mutation lower than 3")
        self.mut_label.setFont(QFont('Arial', 8, italic = True))
        self.mut = QLineEdit('0')
        
        self.length_option = QCheckBox('Min_max option: if you are interested to get a range of random region length')
        self.min_length = QLineEdit('0')
        self.max_length = QLineEdit('0')
        self.min_length.setEnabled(False)
        self.max_length.setEnabled(False)
        self.length_option.toggled.connect(self.min_length.setEnabled)
        self.length_option.toggled.connect(self.max_length.setEnabled)
            


        if os.path.exists(os.path.join(NGS_TEMP_FOLDER, 'project_name.ngs')):
            proj_name = mp.get_project_name_tmp()
            self.name_line_edit.setText(proj_name)

        if os.path.exists(os.path.join(NGS_TEMP_FOLDER, 'rounds.ngs')):
            rounds = mp.get_rounds_str_tmp()
            self.round_line_edit.setText(rounds)
            rr_len = mp.get_rr_length()
            self.rr_length.setText(str(rr_len))
            #if self.length_option.isChecked == True:
                #min_len = mp.get_min_length()
                #max_len = mp.get_max_length()
                #self.min_length.setText(str(min_len))
                #self.max_length.setText(str(max_len))

        if os.path.exists(os.path.join(NGS_TEMP_FOLDER, "forward_primers.ngs")):
            fp = mp.get_forward_primers_list_tmp()
            if len(fp) > 1 or fp[0] != '':
                self.forward_primers_text_edit.setText("\n".join(fp))

        if os.path.exists(os.path.join(NGS_TEMP_FOLDER, 'reverse_primers.ngs')):
            rp = mp.get_reverse_primers_list_tmp()
            if len(rp) > 1 or rp[0] != '':
                self.reverse_primers_text_edit.setText("\n".join(rp))
        


        # self.create_merge_group_box()
        self.create_continue_group_box()
        self.create_output_group_box()

        self.create_rounds_group_box()

        self.create_forward_primers_group_box()
        self.create_reverse_primers_group_box()
        self.create_option_group_box()
        self.create_name_group_box()
        self.set_output_path()
        self.create_random_region_group_box()

        main_layout = QtWidgets.QGridLayout(self)

        main_layout.addWidget(self.name_group_box, 0, 0)
        main_layout.addWidget(self.round_group_box, 1, 0)
        main_layout.addWidget(self.forward_primers_group_box, 2, 0)
        main_layout.addWidget(self.reverse_primers_group_box, 3, 0)
        main_layout.addWidget(self.random_len_group_box, 4, 0)
        main_layout.addWidget(self.options_group_box, 5, 0)
        main_layout.addWidget(self.output_path_group_box, 6, 0)
        main_layout.addWidget(self.continue_group_box, 7, 0)
        

    def create_rounds_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.round_line_edit)
        self.round_group_box.setLayout(layout)
        


    
    def create_forward_primers_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.forward_primer_info)
        layout.addWidget(self.forward_primers_text_edit)
        self.forward_primers_group_box.setLayout(layout)

    def create_reverse_primers_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.reverse_primer_info)
        layout.addWidget(self.reverse_primers_text_edit)
        self.reverse_primers_group_box.setLayout(layout)

    def create_random_region_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.random_option)
        layout.addWidget(self.rr_length)
        layout.addWidget(self.mutation)
        layout.addWidget(self.mut_label)
        layout.addWidget(self.mut)
        layout.addWidget(self.length_option)
        layout.addWidget(self.min_length)
        layout.addWidget(self.max_length)
        self.random_len_group_box.setLayout(layout)

    def create_option_group_box(self):
        layout = QHBoxLayout()
        layout.addWidget(self.advanced_button)
        self.options_group_box.setLayout(layout)
        self.advanced_button.clicked.connect(self.open_adv_options_GUI)

    def create_output_group_box(self):
        layout = QVBoxLayout()
        self.output_line_edit.setReadOnly(True)
        self.output_line_edit.setStyleSheet("background-color: lightgray")
        layout.addWidget(self.output_line_edit)
        self.output_path_group_box.setLayout(layout)

    def create_continue_group_box(self):
        continue_button = QPushButton('Continue')
        back_button = QPushButton("Back")
        layout = QHBoxLayout()
        layout.addWidget(back_button)
        layout.addWidget(continue_button)
        self.continue_group_box.setLayout(layout)
        continue_button.clicked.connect(self.store_metadata)
        back_button.clicked.connect(self.open_file_select_GUI)

    def create_name_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.name_line_edit)
        self.name_group_box.setLayout(layout)

    def set_output_path(self):
        out_path = mp.get_last_output_path()
        self.output_line_edit.setText(out_path)

    def open_start_GUI(self):
        self.open_start = GUI_start.StartGUI()
        self.open_start.show()
        self.close()

    def open_file_select_GUI(self):
        #control_panel.delete_all_ngs_files()
        self.open_file_select_GUI = GUI_file_upload.FileBrowserGUI()
        self.open_file_select_GUI.show()
        self.close()



    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            mf.delete_all_ngs_files()
            self.close()

    def split_parameter(self, para: str) -> list:
        para = para.strip()
        if ',' in para and '\n' in para:
            raise TypeError

        elif '\n' in para:
            para = para.split('\n')

        else:
            para = para.split(',')

        para = [x.replace(' ', '') for x in para]

        return para

    def get_project_name(self):
        name = self.name_line_edit.text()
        return name

    def get_rounds(self):
        rounds = self.split_parameter(self.round_line_edit.text())
        return rounds


    def get_forward_primers(self):
        #print('running')
        for_primers = self.forward_primers_text_edit.toPlainText()
        #print(for_primers)
        for_primers = self.split_parameter(for_primers)
        #print(type(for_primers), for_primers)
        return for_primers

    def get_reverse_primers(self):
        #print('running')
        rev_primers = self.reverse_primers_text_edit.toPlainText()
        #print(rev_primers)
        rev_primers = self.split_parameter(rev_primers)
        #print(type(rev_primers), rev_primers)
        return rev_primers

    def get_random_reg_len(self):
        random_len = int(self.rr_length.text())
        if self.length_option.isChecked() == False:
            min_len = False
            max_len = False
        else:
            min_len = int(self.min_length.text())
            max_len = int(self.max_length.text())

        primer_mut = int(self.mut.text())

        return random_len, min_len, max_len, primer_mut

    #def open_motif_disc(self):
        #self.motif_disc.show()
        #self.close()

    def open_str_error(self):
        self.open_string_error_win = win_string_error.StringError()
        self.open_string_error_win.show()

    def store_metadata(self):

        project_name = self.get_project_name()
        check_str = mt.string_check(project_name)

        if check_str: # if invalid string
            self.open_str_error()

        else:
            try: 
                random_len, min_len, max_len, primer_mut = self.get_random_reg_len()
                for_primers = self.get_forward_primers()
                rev_primers = self.get_reverse_primers()
                rounds = self.get_rounds()
                assert len(for_primers) == len(rev_primers),'First'
                assert len(for_primers) == len(rounds), 'Second'
                assert random_len > 0, 'Third'
            
            except TypeError: 
                warningBox = QtWidgets.QMessageBox()
                warningBox.setText('Please make sure only \',\' or only new line is used to separate between rounds and list of primers')
                warningBox.setInformativeText('Please press OK to check the input')
                warningBox.exec_()
                
            except AssertionError as e:
                assertBox = QtWidgets.QMessageBox()
                if str(e) == 'First':
                    assertBox.setText('Length of reverse and forward primers are not same')
                if str(e) == 'Second':    
                    assertBox.setText('Length of primers and rounds are not same')
                if str(e) == 'Third': 
                    assertBox.setText('Random length must be greater than 0')
                assertBox.exec_()
                
            else:
                fastq_files = mp.get_last_files()
                output_path = mp.get_last_output_path()
                update_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        
    
    
                mp.set_project_name_tmp(project_name)
                mp.set_rounds_str_tmp(rounds)
                mp.set_forward_primers_tmp(for_primers)
                mp.set_reverse_primers_tmp(rev_primers)
    
    
                self.temp_dict['project'] = [{
                    "project_name": project_name,
                    "files": fastq_files,
                    "output": output_path,
                    "update_date": update_date,
                    "for_primers": for_primers,
                    "rev_primers": rev_primers,
                    "primer_mutation":primer_mut,
                    "rr_len": random_len,
                    'max_len': max_len,
                    'min_len': min_len,
                    "rounds": rounds,
                    "split": True
                }]
                temp_dict = json.dumps(self.temp_dict)
                #print(temp_dict)
    
                with open(TEMP_FILE, 'w') as f:
                    f.write(str(temp_dict))
    
                self.open_check_tools()

    def read_temp_metadata(self):
        with open(TEMP_FILE, 'r') as f:
            x = f.read()
            # print(x)
        temp_dic = json.loads(x)
        #print('done', temp_dic)

    def open_adv_options_GUI(self):
        self.open_adv_options = GUI_adv_options.AdvancedOptionsGUI()
        self.open_adv_options.show()

    def open_check_tools(self):
        self.check_tools = GUI_check_tools.CheckToolsGUI()
        self.check_tools.show()
        self.close()