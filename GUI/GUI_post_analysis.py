from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QPushButton, QSplashScreen, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QSpacerItem, \
    QSizePolicy
# GUI_motif_search_ngs
from GUI import GUI_start

class PostAnalysisGUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(PostAnalysisGUI, self).__init__(parent)
        self.setMinimumHeight(200)
        self.setMinimumWidth(800)
        self.setWindowTitle("Post Analysis")

        #self.post_analysis_gb = QGroupBox()
        self.quit_gb = QGroupBox()
        #self.create_post_analysis_gb()
        self.create_quit_gb()

        main_layout = QtWidgets.QGridLayout(self)

        #main_layout.addWidget(self.post_analysis_gb, 0, 0)
        main_layout.addWidget(self.quit_gb, 1, 0)

    #def create_post_analysis_gb(self):
        #layout = QHBoxLayout()
        #xlsx_label = QLabel("Create .xlsx files of all input patterns")
        #xlsx_button = QPushButton('MOTIFS TO XLSX FILES')

        #layout.addWidget(xlsx_button)
        #layout.addWidget(xlsx_label)
        
        
        #self.post_analysis_gb.setLayout(layout)
        #xlsx_button.clicked.connect(self.open_motif_search)

    def create_quit_gb(self):
        layout = QHBoxLayout()
        quit_button = QPushButton('Quit Program')
        back_button = QPushButton('Back to Menu')
        layout.addWidget(quit_button)
        layout.addWidget(back_button)
        self.quit_gb.setLayout(layout)
        
        quit_button.clicked.connect(self.close_window)
        back_button.clicked.connect(self.open_menu)
        

    def close_window(self):
        self.close()

    def open_menu(self):
        self.open_menu_win = GUI_start.StartGUI()
        self.open_menu_win.show()
        self.close()

    #def open_motif_search(self):
        #self.motif_src_GUI = GUI_motif_search_ngs.MotifOptionGUI()
        #self.motif_src_GUI.show()
        #self.close()


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = PostAnalysisGUI()

    w.show()
    sys.exit(app.exec_())
