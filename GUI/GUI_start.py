from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QGroupBox, QHBoxLayout, QLabel
#from qtconsole.qt import QtCore, QtGui
import control_panel.manage_files as mf
# GUI_single_motif, GUI_file_motif
from GUI import GUI_scramble_seq,  GUI_complementary, GUI_file_upload, GUI_fastq_to_fasta, \
     GUI_post_analysis


class StartGUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(StartGUI, self).__init__(parent)
        mf.set_primer_library_list()
        mf.delete_all_ngs_files()
        #mf.delete_all_ms_files()
        self.setMinimumHeight(400)
        self.setMinimumWidth(1600)
        self.setWindowTitle("AptaNext")
        app_icon = QtGui.QIcon()
        app_icon.addFile("AptaNext_Small-icon.png", QtCore.QSize(16, 16))
        self.setWindowIcon(app_icon)

        self.ngs_group_box = QGroupBox()
        #self.file_motif_group_box = QGroupBox()
        #self.single_motif_group_box = QGroupBox()
        self.conv_complement_group_box = QGroupBox()
        self.scramble_group_box = QGroupBox()
        self.file_conv_group_box = QGroupBox()

        self.create_ngs_group_box()
        #self.create_file_motif_group_box()
        #self.create_single_motif_group_box()
        self.create_conv_complement_group_box()
        self.create_scramble_group_box()
        self.create_file_conv_group_box()

        main_layout = QtWidgets.QGridLayout(self)

        main_layout.addWidget(self.ngs_group_box, 0, 0)
        #main_layout.addWidget(self.file_motif_group_box,1 ,0)
        #main_layout.addWidget(self.single_motif_group_box, 2, 0)
        main_layout.addWidget(self.conv_complement_group_box, 3, 0)
        main_layout.addWidget(self.scramble_group_box, 4, 0)
        main_layout.addWidget(self.file_conv_group_box, 5, 0)



    def create_ngs_group_box(self):
        layout = QHBoxLayout()
        create_ngs_button = QPushButton('Run NGS Analysis')
        #h_spacer = QSpacerItem(200, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        label = QLabel('Run a detailed NGS analysis:'
                       '\n\t- Import sequences from FASTQ/CSV/FATSQ.gz'
                       '\n\t- Split Sequences into Rounds'
                       '\n\t- Get sequence counts/frequencies'
                       # Does this need to be deleted
                       '\n\t- Export result to .xlsx and .csv'
                       # Double check if this is necessary
                       '\n\t- Export rounds to txt file'
                       )
        layout.addWidget(create_ngs_button)
        #layout.addItem(h_spacer)
        layout.addWidget(label)
        self.ngs_group_box.setLayout(layout)
        create_ngs_button.clicked.connect(self.open_file_select_GUI)



    #def create_single_motif_group_box(self):
        #layout = QHBoxLayout()
        #single_motif_button = QPushButton("Single Motif Search")
        #label = QLabel("Find motif in a single sequence")
        #layout.addWidget(single_motif_button)
        #layout.addWidget(label)
        #self.single_motif_group_box.setLayout(layout)
        #single_motif_button.clicked.connect(self.open_single_motif)


    def create_scramble_group_box(self):
        layout = QHBoxLayout()
        scramble_seq_button = QPushButton('Scramble')
        #h_spacer = QSpacerItem(200, 0, QSizePolicy.Minimum, QSizePolicy.Preferred)
        label = QLabel('Scramble a given sequence')
        layout.addWidget(scramble_seq_button)
        #layout.addItem(h_spacer)
        layout.addWidget(label)

        self.conv_complement_group_box.setLayout(layout)
        scramble_seq_button.clicked.connect(self.open_scramble)
        #scramble_seq_button.clicked.connect(self.test)

    def create_conv_complement_group_box(self):
        layout = QHBoxLayout()
        complement_conv_button = QPushButton('Convert to Complementary')
        #h_spacer = QSpacerItem(100, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        label = QLabel('Convert a sequence to complementary\n or reverse complementary sequence')
        layout.addWidget(complement_conv_button)
        #layout.addItem(h_spacer)
        layout.addWidget(label)
        self.scramble_group_box.setLayout(layout)
        complement_conv_button.clicked.connect(self.open_comp_GUI)

    def create_file_conv_group_box(self):
        layout = QHBoxLayout()
        file_conv_button = QPushButton('FASTA <=> FASTQ')
        # h_spacer = QSpacerItem(100, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        label = QLabel('Converts .fastq <=> .fasta files')
        layout.addWidget(file_conv_button)
        # layout.addItem(h_spacer)
        layout.addWidget(label)
        self.file_conv_group_box.setLayout(layout)
        file_conv_button.clicked.connect(self.open_file_conv)

    def open_file_select_GUI(self):
        self.open_file_select_GUI = GUI_file_upload.FileBrowserGUI()
        self.open_file_select_GUI.show()
        self.close()

    def open_comp_GUI(self):
        self.open_comp_GUI = GUI_complementary.SequenceComplementGUI()
        self.open_comp_GUI.show()
        self.close()

    def open_scramble(self):
        self.open_scramble_seq = GUI_scramble_seq.ScrambleSeqGUI()
        self.open_scramble_seq.show()
        self.close()

    def open_file_conv(self):
        self.open_file_conv = GUI_fastq_to_fasta.FastqToFasta()
        self.open_file_conv.show()
        self.close()

    #def open_single_motif(self):
        #self.open_single_motif = GUI_single_motif.SingleMotifGUI()
        #self.open_single_motif.show()
        #self.close()

    #def open_file_motif(self):
        #self.open_file_motif = GUI_file_motif.FileMotifGUI()
        #self.open_file_motif.show()
        #self.close()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


    def test(self):
        self.post_analysis = GUI_post_analysis.PostAnalysisGUI()
        self.post_analysis.show()
        self.close()
        


