import json
import os
from datetime import datetime

from pathlib import Path

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QThread,pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QCheckBox, QVBoxLayout, QLineEdit,\
    QGroupBox, QTextEdit, QHBoxLayout, QLabel, QProgressBar
#from qtconsole.qt import QtCore, QtGui
import pandas as pd
import control_panel.manage_params as mp
import control_panel.manage_db as mdb
import control_panel.manage_ngs as mngs
import control_panel.manage_files as mf
import tools.misc_tools as mt
from GUI import GUI_check_tools, GUI_start, GUI_file_upload, GUI_adv_options, \
    GUI_post_analysis
from constants import *
from win import win_string_error
import traceback


home = str(Path.home())
print(home)

class ParametersNoSplitGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        #self.motif_disc = GUI_motif_disc_win.MotifDiscWinGUI()
        self.temp_dict = {}
        self.setMinimumHeight(400)
        self.setMinimumWidth(500)
        self.setWindowTitle("Parameters")
        app_icon = QtGui.QIcon()
        app_icon.addFile("AptaNext_Small-icon.png", QtCore.QSize(16, 16))
        self.setWindowIcon(app_icon)
        self.input_files = []
        self.continue_group_box = QGroupBox()
        self.output_path_group_box = QGroupBox('Output Directory')

        self.name_group_box = QGroupBox('Enter Project Name')
        self.options_group_box = QGroupBox("Advanced Options")

        #self.motif_button = QPushButton("Motif Search")
        self.advanced_button = QPushButton("Advanced Options")

        self.name_line_edit = QLineEdit()
        self.output_line_edit = QLineEdit()
        self.round_box = QGroupBox('Rounds')
        self.round_info = QLabel()
        self.round_info.setText('A list of rounds you want to do further analysis')
        self.round_info.setFont(QFont('Arial',8, italic = True))
        self.round_edit = QLineEdit()
    

        if os.path.exists(os.path.join(NGS_TEMP_FOLDER, 'project_name.ngs')):
            proj_name = mp.get_project_name_tmp()
            self.name_line_edit.setText(proj_name)
        

        # self.create_merge_group_box()
        self.create_continue_group_box()
        self.create_output_group_box()

        self.create_option_group_box()
        self.create_name_group_box()
        self.set_output_path()

        main_layout = QtWidgets.QGridLayout(self)

        main_layout.addWidget(self.name_group_box, 0, 0)
        main_layout.addWidget(self.options_group_box, 4, 0)
        main_layout.addWidget(self.output_path_group_box, 5, 0)
        main_layout.addWidget(self.continue_group_box, 6, 0)

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
        self.continue_button = QPushButton('Continue')
        self.back_button = QPushButton("Back")
        layout = QHBoxLayout()
        layout.addWidget(self.back_button)
        layout.addWidget(self.continue_button)
        self.continue_group_box.setLayout(layout)
        self.continue_button.clicked.connect(self.store_metadata)
        self.back_button.clicked.connect(self.open_file_select_GUI)

    def create_name_group_box(self):
        layout = QVBoxLayout()
        layout.addWidget(self.name_line_edit)
        layout.addWidget(self.round_box)
        layout.addWidget(self.round_info)
        layout.addWidget(self.round_edit)
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
        
    def open_continue_analyze_GUI(self):
        #control_panel.delete_all_ngs_files()
        self.open_analyze = Continue_analyze(self.temp_dict)
        self.open_analyze.show()
        self.close()


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            mf.delete_all_ngs_files()
            self.close()


    def get_project_name(self):
        name = self.name_line_edit.text()
        return name

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
            csv_files = mp.get_last_files()
            output_path = mp.get_last_output_path()
            update_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

            mp.set_project_name_tmp(project_name)
            
            rounds = self.round_edit.text().split(',')

            self.temp_dict['project'] = [{
                "project_name": project_name,
                "files": csv_files,
                "output": output_path,
                "update_date": update_date,
                "for_primers": None,
                "rev_primers": None,
                "rounds": rounds,
                "split": False
            }]
            temp_dict2 = json.dumps(self.temp_dict)
            #print(self.temp_dict)

            with open(TEMP_FILE, 'w') as f:
                f.write(str(temp_dict2))
            
            self.open_continue_analyze_GUI()

            #self.open_motif_disc()

    def read_temp_metadata(self):
        print(self.temp_dict)
        return self.temp_dict['project']

    def open_adv_options_GUI(self):
        self.open_adv_options = GUI_adv_options.AdvancedOptionsGUI()
        self.open_adv_options.show()


class Continue_analyze(QtWidgets.QWidget):
    def __init__(self, temp_dict):
        super().__init__()
        self.para = temp_dict['project'][0]
        self.setMinimumHeight(400)
        self.setMinimumWidth(500)
        self.setWindowTitle("Analysis options")
        
        # Create buttons for the Widget
        self.option_group_box = QGroupBox('Options')
        self.unique_plot = QCheckBox('Plot unique sequences')
        self.uni_seq_info = QLabel()
        self.uni_seq_info.setText('Plot of unique sequences (number of sequences with copy number of 1 over all sequences)')
        self.uni_seq_info.setFont(QFont('Arial', 8, italic = True))
        
        self.family_analysis = QCheckBox('Check family analysis')
        self.fam_info = QLabel()
        self.fam_info.setFont(QFont('Arial', 8, italic = True))
        self.fam_info.setText('{proj_name}_NGS_families.csv is given with family analysis for the abundancy number of sequences.')
        
        self.plot_nucleotides = QCheckBox('Plot nucleotide distribution')
        self.nuc_info = QLabel()
        self.nuc_info.setText('Graphs and {proj_name}_nucleotide_distributions.csv file of nucleotide distributions in each position')
        self.nuc_info.setFont(QFont('Arial', 8, italic = True))
        
        self.control_group_box = QGroupBox()
        self.back_button = QPushButton('Back')
        self.continue_button = QPushButton('Continue')
        
       
        # Arrangement main layout
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.addWidget(self.option_group_box, 1, 0)
        main_layout.addWidget(self.control_group_box, 2, 0)
        
        # Vertical layout for group check box
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.unique_plot)
        self.layout1.addWidget(self.uni_seq_info)
        self.layout1.addWidget(self.family_analysis)
        self.layout1.addWidget(self.fam_info)
        self.layout1.addWidget(self.plot_nucleotides)
        self.layout1.addWidget(self.nuc_info)
        self.option_group_box.setLayout(self.layout1)
        
        # Horizontal layout for continue and back button
        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.back_button)
        self.layout2.addWidget(self.continue_button)
        self.control_group_box.setLayout(self.layout2)
        
        # Connect buttons
        self.continue_button.clicked.connect(self.analyze)
        self.back_button.clicked.connect(self.open_parameter_no_split_GUI)
        
        # Import csv file as Pandas Dataframe
        print(self.para['files'][0])
        self.df = pd.read_csv(self.para['files'][0])
        
    def analyze(self):
        
        self.continue_button.setEnabled(False)
        self.back_button.setEnabled(False)
        try:
            if self.family_analysis.checkState():
                msgBox1 = QtWidgets.QMessageBox()
                msgBox1.setText('Family analysis will be carried out')
                msgBox1.setInformativeText('Please press OK to continue')
                msgBox1.exec_()
                mut_num = 1
                mp.save_group_family_mut_num(str(mut_num))
                mngs.create_count_freq_table_xlsx(self.df)
        
            if self.plot_nucleotides.checkState():
                msgBox2 = QtWidgets.QMessageBox()
                msgBox2.setText('Nucleotide distributions will be plotted')
                msgBox2.setInformativeText('Please press OK to continue')
                msgBox2.exec_()
                mngs.create_nucleotide_graphs(self.df)
    
            if self.unique_plot.checkState():
                msgBox2 = QtWidgets.QMessageBox()
                msgBox2.setText('Unique sequences will be plotted')
                msgBox2.setInformativeText('Please press OK to continue')
                msgBox2.exec_()
                mngs.export_unique_seqs_all_rounds(self.df)
        except Exception as error:
                failed = QtWidgets.QMessageBox()
                failed.setText(f"{type(error)} - {error}.\n \n"
                                f"{traceback.format_exc()} \n \n")
                failed.exec_()
            
        self.open_post_analysis()
        
    
    def open_parameter_no_split_GUI(self):
        self.open_no_split_GUI = ParametersNoSplitGUI()
        self.open_no_split_GUI.show()
        self.close()
        
    def open_post_analysis(self):
        self.post_analysis = GUI_post_analysis.PostAnalysisGUI()
        self.post_analysis.show()
        self.close()
            
