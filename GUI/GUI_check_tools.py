import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCheckBox, QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout, QLineEdit, QProgressBar, QLabel
#from qtconsole.qt import QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from GUI import GUI_parameters, GUI_post_analysis
import control_panel.manage_params as mp
import control_panel.manage_ngs as mngs
from tools import ngs_tools as ngst
import traceback

class CheckToolsGUI(QtWidgets.QWidget):
    
    def __init__(self, parent=None):
        super(CheckToolsGUI, self).__init__(parent)
        #self.polar_df_origin = None
        self.setMinimumHeight(400)
        self.setMinimumWidth(800)
        self.setWindowTitle("AptaNext")
        app_icon = QtGui.QIcon()
        app_icon.addFile("AptaNext_Small-icon.png", QtCore.QSize(16, 16))
        self.setWindowIcon(app_icon)
        self.seq_analysis_check_group_box = QGroupBox('Additional Exports')
        self.group_families = QCheckBox('Group enriched sequences into families')
        self.fam_info = QLabel()
        self.fam_info.setFont(QFont('Arial', 8, italic = True))
        self.fam_info.setText('{proj_name}_NGS_families.csv is given with family analysis for the abundancy number of sequences. \n If this option is not chosen, {proj_name}_NGS_frequency.csv is given')
 
        self.quality_check = QCheckBox('Quality check of NGS data')
        self.quality_info = QLabel()
        self.quality_info.setText('Quality check provides information of length distributions and Phred scores of NGS sequences')
        self.quality_info.setFont(QFont('Arial', 8, italic = True))
        
        self.plot_unique_seqs_btn = QCheckBox('Plot unique sequences')
        self.uni_seq_info = QLabel()
        self.uni_seq_info.setText('Plot of unique sequences (number of sequences with copy number of 1 over all sequences)')
        self.uni_seq_info.setFont(QFont('Arial', 8, italic = True))
                          
        self.plot_nuc_dist_btn = QCheckBox('Plot nucleotide distribution')
        self.nuc_info = QLabel()
        self.nuc_info.setText('Graphs and {proj_name}_nucleotide_distributions.csv file of nucleotide distributions in each position')
        self.nuc_info.setFont(QFont('Arial', 8, italic = True))
        
        self.export_files_defaults = QGroupBox('Defaults')
        self.default_info = QLabel()
        self.default_info.setText('These files are given by defaults during NGS analysis')
        self.default_info.setFont(QFont('Arial', 8, italic = True))
        
        self.csv_file = QCheckBox('{proj_name}_count_all_rounds.csv')
        self.summary_file = QCheckBox('{proj_name}_summary.txt')
        self.csv_file.setChecked(True)
        self.csv_file.setEnabled(False)
        self.summary_file.setChecked(True)
        self.summary_file.setEnabled(False)
        
        
        self.seq_analysis_button_group_box = QGroupBox()

        self.create_seq_analysis_check_group_box()
        self.create_seq_analysis_button_group_box()

        main_layout = QtWidgets.QGridLayout(self)
        main_layout.addWidget(self.export_files_defaults,0,0)
        main_layout.addWidget(self.seq_analysis_check_group_box, 1, 0)
        main_layout.addWidget(self.seq_analysis_button_group_box, 2, 0)


    def create_seq_analysis_check_group_box(self, filenames=None):
        layout1 = QVBoxLayout()
        layout1.addWidget(self.default_info)
        layout1.addWidget(self.csv_file)
        layout1.addWidget(self.summary_file)
        
        layout2 = QVBoxLayout()
        layout2.addWidget(self.quality_check)
        layout2.addWidget(self.quality_info)
        layout2.addWidget(self.plot_nuc_dist_btn)
        layout2.addWidget(self.nuc_info)
        layout2.addWidget(self.plot_unique_seqs_btn)
        layout2.addWidget(self.uni_seq_info)
        layout2.addWidget(self.group_families)
        layout2.addWidget(self.fam_info)
        

        self.export_files_defaults.setLayout(layout1)
        self.seq_analysis_check_group_box.setLayout(layout2)
        
    def create_seq_analysis_button_group_box(self):
        self.prgb = QProgressBar(self)
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.continue_button = QPushButton('Run')
        self.back_button = QPushButton("Back")
        layout = QHBoxLayout()
        layout.addWidget(self.back_button)
        layout.addWidget(self.continue_button)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.label1)
        vlayout.addWidget(self.label2)
        vlayout.addWidget(self.prgb)
        vlayout.addLayout(layout)
        self.seq_analysis_button_group_box.setLayout(vlayout)
        self.back_button.clicked.connect(self.open_parameters_GUI)
        self.continue_button.clicked.connect(self.initialize_analysis)

    def process_seq(self,num):
        self.label1.setText(f'Processing {num} sequences.')

    def initialize_analysis(self):
        self.back_button.setEnabled(False)
        self.continue_button.setEnabled(False)
        print('STARTING NGS ANALYSIS')
        #self.open_upload_win()
        print('Open file')
        files = mp.get_current_files()
        
        self.opf = ngst.open_files(files)
        self.opf.updateSignal.connect(self.process_seq)
        self.opf.updateData.connect(self.data)
        self.opf.start()
        
    def initial_ana(self):
        try: 
            if self.quality_check.checkState():
                qc = Quality_check(self.polar_df_origin)
                if qc.exec_() == qc.Accepted:
                    len_threshold,score_threshold = qc.export_data()
                    qc.close_window()
                elif qc.exec_() == qc.Rejected:
                    len_threshold,score_threshold = (0,0)
                    qc.close_window()
                if len_threshold != 0 or score_threshold != 0:
                    new_df,message = ngst.remove_sequence(self.polar_df_origin,len_threshold,score_threshold)
                    
                    # Message box of remove sequences
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setText(message)
                    msgBox.setInformativeText('Please press OK to continue')
                    msgBox.exec_()
                    self.split_round_df = self.split_function(new_df)
                else:
                    self.split_round_df = self.split_function(self.polar_df_origin)
            else:
                self.split_round_df = self.split_function(self.polar_df_origin)
    
        except Exception as error:
                failed = QtWidgets.QMessageBox()
                failed.setText(f"{type(error)} - {error}.\n")
                failed.exec_()
            
    def final_ana(self):
        try:
            msgBox5 = QtWidgets.QMessageBox()
            msgBox5.setText('count_all_rounds.csv will be created')
            msgBox5.setInformativeText('Please press OK and wait')
            msgBox5.exec_()
            self.count_all_rounds = mngs.create_count_tables_rounds_all(self.split_round_df)
            
            if self.group_families.checkState():
                msgBox2 = QtWidgets.QMessageBox()
                msgBox2.setText('Family analysis will be carried out')
                msgBox2.setInformativeText('Please press OK to continue')
                msgBox2.exec_()
                mut_num = 1
                mp.save_group_family_mut_num(str(mut_num))
            
            mngs.create_count_freq_table_xlsx(self.count_all_rounds)
            mngs.write_summary_ngs(self.count_all_rounds)
            
            if self.plot_nuc_dist_btn.checkState():
                msgBox3 = QtWidgets.QMessageBox()
                msgBox3.setText('Nucleotide distributions will be plotted')
                msgBox3.setInformativeText('Please press OK to continue')
                msgBox3.exec_()
                mngs.create_nucleotide_graphs(self.count_all_rounds)
    
                
            if self.plot_unique_seqs_btn.checkState():
                msgBox4 = QtWidgets.QMessageBox()
                msgBox4.setText('Unique sequences will be plotted')
                msgBox4.setInformativeText('Please press OK to continue')
                msgBox4.exec_()
                mngs.export_unique_seqs_all_rounds(self.count_all_rounds)
            
            self.open_post_analysis()
        except Exception as error:
                failed = QtWidgets.QMessageBox()
                failed.setText(f"{type(error)} - {error}.\n \n"
                                f"{traceback.format_exc()} \n \n")
                failed.exec_()
        
    
    def data(self,df):
        self.polar_df_origin = df.clone()
        return self.initial_ana()
    
    def final_data(self,df):
        self.split_round_df = df.clone()
        return self.final_ana()  
      
    def split_function(self,polar_df):
        params = mp.get_parameters_ngs()
        rounds = [int(r) for r in params['rounds']]
        for_prms = params['for_primers']
        rev_prms = params['rev_primers']
        rr_len = int(params['rr_len'])
        primer_mut = int(params['primer_mutation'])
        print(type(params['min_len']))
        if int(params['min_len']):
            min_len = int(params['min_len'])
            max_len = int(params['max_len'])
        else:
            min_len = params['min_len']
            max_len = params['max_len']
        #print(rounds, for_prms, rev_prms)
        #print(rr_len)
        if rev_prms == ['']:
            rev_prms = [0]*len(rounds)
        print(rounds)
        print(type(rounds))
        #print(len(rounds))
        #print(rev_prms)
        print(min_len)
        print(max_len)
        self.split = ngst.create_round_table(polar_df,for_prms,rev_prms,rounds,rr_len, primer_mut, min_len, max_len)
        self.split.updateSignal.connect(self.split_progress)
        self.split.updateMaximum.connect(self.prgb.setMaximum)
        self.split.updateData.connect(self.final_data)
        self.split.start()
    
    def split_progress(self,value):
        self.prgb.setValue(value)
        self.label2.setText('Splitting rounds...')
    
        
    def open_parameters_GUI(self):
        self.open_parameters = GUI_parameters.ParametersGUI()
        self.open_parameters.show()
        self.close()

    def open_post_analysis(self):
        self.post_analysis = GUI_post_analysis.PostAnalysisGUI()
        self.post_analysis.show()
        self.close()
        
        
class Quality_check(QtWidgets.QDialog):
    def __init__(self,df):
        super().__init__()
        self.df = df
        self.setMinimumHeight(400)
        self.setMinimumWidth(800)
        self.setWindowTitle('Quality check plots')
        
          
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        
        self.remove_seq_button = QCheckBox('Do you want to remove sequences for later analysis')
        self.length_group_box = QGroupBox('What is your length threshold?')
        self.len_edit = QLineEdit('0')
        self.len_edit.setEnabled(False)
        self.score_group_box = QGroupBox('What is your Phred score threshold?')
        self.score_edit = QLineEdit('0')
        self.score_edit.setEnabled(False)
        self.remove_seq_button.toggled.connect(self.len_edit.setEnabled)
        self.remove_seq_button.toggled.connect(self.score_edit.setEnabled)
        
        self.ok = QPushButton('OK')
        self.ok.clicked.connect(self.accept)
        self.cancel = QPushButton('Cancel')
        self.cancel.clicked.connect(self.reject)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.ok)
        hbox.addWidget(self.cancel)
        
        layout = QVBoxLayout()
        # adding tool bar to the layout
        layout.addWidget(self.toolbar)
        # adding canvas to the layout
        layout.addWidget(self.canvas)
        # adding check box group to the layout
        layout.addWidget(self.remove_seq_button)
        layout.addWidget(self.length_group_box)
        layout.addWidget(self.len_edit)
        layout.addWidget(self.score_group_box)
        layout.addWidget(self.score_edit)
        layout.addLayout(hbox)
        
        # setting layout to the main window
        self.setLayout(layout)
        
        self.plot()
        self.show()
        
        self.len_thre,self.phred_thre = self.export_data()
        
        
        
        
    def plot(self):
        self.figure.clear()
        l = self.df['length'].to_numpy()
        p = self.df['phred_score'].to_numpy()
        ax1 = self.figure.add_subplot(121)
        ax1.hist(l,bins = 100, color = 'blue',log = True)
        ax1.set_xlabel('Length')
        ax1.set_ylabel('Count')
        ax1.set_title('Length of sequences')

        ax2 = self.figure.add_subplot(122)
        ax2.hist(p,bins = 100, color = 'blue',log = True)
        ax2.set_xlabel('Average phred score')
        ax2.set_ylabel('Count')
        ax2.set_title('Phred score of sequences')
        self.canvas.draw_idle()
        plt.close()
        
    
    def export_data(self):
        if self.remove_seq_button.checkState():
            len_thre = int(self.len_edit.text())
            phred_thre = int(self.score_edit.text())
        else:
            len_thre,phred_thre = (0,0)
        return len_thre,phred_thre
    
    def close_window(self):
        self.figure.clear()
        self.close()
        


if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    w = CheckToolsGUI()
    

    w.show()
    sys.exit(app.exec_())
