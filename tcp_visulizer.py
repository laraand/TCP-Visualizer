import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout,QLabel, QSizePolicy, QMessageBox, QWidget
from PyQt5.QtWidgets import QFormLayout, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
import array



class App(QDialog):
 
    def __init__(self):
        super().__init__()
        self.title = "TCP Visualizer"
        self.screen = QtWidgets.QDesktopWidget().setGeometry(800,700,800,700)
        self.screen = QtWidgets.QDesktopWidget().screenGeometry(-1)

        
        #self.initUI()
        
    #def initUI(self):
        #logo icon for window
        self.setWindowIcon(QtGui.QIcon("C:\\Users\\Andrea\\Documents\\GitHub\\TCP-Visualizer\\TCPupdatedlogo.png"))
        self.setWindowTitle(self.title)
        
       
        RTTlabel = QLabel('RTT',self)
        RTTlabel.move(1000,50)
        RTTlabel.setStyleSheet("font: 20pt Comic Sans MS")

        HandShakeLabel = QLabel('Handshake', self)
        HandShakeLabel.setStyleSheet("font: 20pt Comic Sans MS")
        HandShakeLabel.move(200,55)

        

        inc = 0
        inc2 = 0
        
        self.image2 = QLabel(self)
        self.image3 = QLabel(self)
        
        groupBox = QGroupBox()
        formLayout = QFormLayout()
        
        #create widget for handshake vertical lines
        for x in range(3):
            inc = inc + 100
            inc2 = inc2 + 200
            
            #self.image2 = QLabel(self)
            self.image2.setPixmap(QPixmap('C:\\Users\\Andrea\\Documents\\GitHub\\TCP-Visualizer\\right.png'))
            self.image2.setGeometry(1350,0+inc,700,400)

            #self.image3 = QLabel(self)
            self.image3.setPixmap(QPixmap('C:\\Users\\Andrea\\Documents\\GitHub\\TCP-Visualizer\\left.png'))
            self.image3.setGeometry(1350,0+inc2,600,400)

            formLayout.addRow(self.image2)
            formLayout.addRow(self.image3)

        

        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(700)
        scroll.setFixedWidth(510)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        
        #call handshake definition, in order to obtain data
        #self.handshake()
        
        self.show()

    def handshake(self):
        #open file in which parsed information is stored in 
        file = open("pckts.txt", "r")
        
        #read the contents of the file
        contents = file.readlines()
        

        #variables to hold searching content within parsed file
        ack = 'Acknowledgment number: '
        seq = 'Next sequence number: '
        window = 'Window size value: '
        
        #array's to store acknowledgment,sequence numbers and window size
        seqPk = []
        ackPk = []
        wndwSize = [] 
        
        with open("C:\\Users\\Andrea\\Desktop\\pckts.txt", "r") as pack:
            
            for line in pack:
                #condition to search for acknowledgment number
                if(ack in line):
                    #obtain acknowledgment number
                    ackLength = line[23:(len(line)-26)]
                    #print ('acknowledge: ' + ackLength)
                    ackPk.append(ackLength)

                #condition to search for sequence number
                if(seq in line):
                    #obtain sequence number
                    seqLength = line[22:(len(line)-30)]
                    #append value to sequence array
                    seqPk.append(seqLength)

                #condition to obtain window size
                if(window in line):
                    #obtain window size value
                    windowLength = line[19:]
                    #append value to sequence array
                    wndwSize.append(windowLength)
		
                #close file
                file.close()

            
            for i in range(len(ackPk)):
                print( ackPk[i] + seqPk[i] + wndwSize[i])
            
        self.show()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
