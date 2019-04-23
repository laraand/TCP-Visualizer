import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout,QLabel, QSizePolicy, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
import array


class App(QDialog):
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TCP Visualizer")
        self.screen = QtWidgets.QDesktopWidget().setGeometry(50,50,600,400)
        self.screen = QtWidgets.QDesktopWidget().screenGeometry(-1)

        self.handshake()
        self.initUI()
        
    def initUI(self):
        
       
        RTTlabel = QLabel('RTT',self)
        RTTlabel.move(200,50)
        RTTlabel.setStyleSheet("font: 20pt Comic Sans MS")

        HndShakelabel = QLabel('Handshake',self)
        HndShakelabel.move(1300,50)
        HndShakelabel.setStyleSheet("font: 20pt Comic Sans MS")

        buttonPlay = QPushButton('',self)
        buttonPlay.setIcon(QtGui.QIcon('C:\\Users\\Andrea\\Documents\\GitHub\\TCP-Visualizer\\play.jpg'))
        buttonPlay.setIconSize(QtCore.QSize(62,62))
        buttonPlay.move(1286, 898)

        buttonRewind = QPushButton('',self)
        buttonRewind.setIcon(QtGui.QIcon('C:\\Users\\Andrea\\Documents\\GitHub\\TCP-Visualizer\\backward.png'))
        buttonRewind.setIconSize(QtCore.QSize(62,62))
        buttonRewind.move(1212, 898)

        buttonForward = QPushButton('',self)
        buttonForward.setIcon(QtGui.QIcon('C:\\Users\\Andrea\\Documents\\GitHub\\TCP-Visualizer\\forward.png'))
        buttonForward.setIconSize(QtCore.QSize(62,62))
        buttonForward.move(1354, 898)


               
        self.show()

    def handshake(self):
        print('handshake def working to this point')
        
        #open file in which parsed information is stored in 
        file = open("pckts.txt", "r")
        print('file was opened')
        #read the contents of the file
        contents = file.readlines()
        print('file was read')

        #variables to hold searching content within parsed file
        a = 'Acknowledgment number: '
        s = 'Next sequence number: '
        #array's to store acknowledgment and sequence numbers
        seqPk = []
        ackPk = []
        
        with open("C:\\Users\\Andrea\\Desktop\\pckts.txt", "r") as pack:
            
            for line in pack:
                #condition to search for acknowledgment number
                if(a in line):
                    #obtain acknowledgment number
                    ackLength = line[23:(len(line)-26)]
                    #print ('acknowledge: ' + ackLength)
                    ackPk.append(ackLength)

                #condition to search for sequence number
                if(s in line):
                    #obtain sequence number
                    seqLength = line[22:(len(line)-30)]
                    #print ('seq: ' + seqLength)
                    seqPk.append(seqLength)
                file.close()
                
            print(seqPk[0])
            for i in range(len(ackPk)):
                print('Downarrow' + ackPk[i] + seqPk[i])
            
        self.show()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
