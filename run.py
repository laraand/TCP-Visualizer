import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout,QLabel, QSizePolicy, QMessageBox, QLineEdit, QWidget, QFormLayout, QScrollArea
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QColor, QIcon, QPixmap, QImage
import numpy as np
import array
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
plt.style.use('bmh')
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

class App(QDialog):
 
    def __init__(self):
        super().__init__()
        self.title = 'TCP Visualizer'
        self.left = 10
        self.top = 10
        self.width = 1400
        self.height = 900
        self.initUI()
        #self.keyPressEvent()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

        #logo icon for window
        self.setWindowIcon(QtGui.QIcon("C:\\Users\\Mayra Ochoa\\Documents\\GitHub\\TCP-Visualizer\\imgs\\TCPupdatedlogo.png"))
        self.setWindowTitle(self.title)
        
        #Creating graph on main class
        m = PlotCanvas(self, width=6, height=7)
        m.move(750,100)

        button = QPushButton('TCP', self)
        button.resize(100,50)
        button.move(880,820)
        '''button.clicked.connect(self.clickMethod)'''
        button = QPushButton('GQUIC(UDP)', self)
        button.resize(100,50)
        button.move(980,820)
        '''button.clicked.connect(self.on_click)'''
        button = QPushButton('TCP vs GQUIC(UDP)', self)
        button.resize(140,50)
        button.move(1080,820)
        '''button.clicked.connect(self.on_click)'''
        
        
        handlabel = QLabel('Handshake', self)
        handlabel.move(230,50)
        handlabel.setStyleSheet("font: 12pt Proxima No")

        UDPlabel = QLabel('TCP vs GQU  ', self)
        UDPlabel.move(950,50)
        UDPlabel.setStyleSheet("font: 11pt Proxima Nova")
        
        UDPlabel2 = QLabel('IC(UDP)', self)
        UDPlabel2.move(1048,50)
        UDPlabel2.setStyleSheet("font: 11pt Proxima Nova")

    
        groupBox = QGroupBox()
        form_wid = QWidget()
        formLayout = QFormLayout()
        nameLabel = QLabel(self.tr("Client                                                                                                       Server"))
        nameLabel.setBuddy(nameLabel)
       
        formLayout.addRow(nameLabel)
        #create widget for handshake vertical lines
        for x in range(10):
            imageLabel = QLabel()
            image = QImage('imgs\\logo.png')
            imageLabel.setPixmap(QPixmap.fromImage(image))

            imageLabel2 = QLabel()
            image2 = QImage('imgs\\logo2.png')
            imageLabel2.setPixmap(QPixmap.fromImage(image2))

            
            formLayout.addRow(imageLabel2)
            formLayout.addRow(imageLabel)
    
           
        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        scroll.setFixedHeight(700)
        scroll.setFixedWidth(535)
            


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
        
        with open("C:\\Users\\Mayra Ochoa\\Desktop\\pckts.txt", "r") as pack:
            
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
            
    @pyqtSlot()
    def on_click(self):
        print('button clicked')

    def keyPressEvent(self, e):  
        if e.key() == QtCore.Qt.Key_Escape:
           self.close()
        if e.key() == QtCore.Qt.Key_F11:
           if self.isMaximized():
               self.showNormal()
           else:
               self.showMaximized()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        self.plot()
    def plot(self):
        xList = ["TCP", "UDP"]
        yList = []
        m = "Packet"
        y_value = 0.0
        y_value2 = 0.0
        total_packet_numberTCP = ""
        total_packet_numberUDP = ""
        ax = self.figure.add_subplot(111)
        #TCP calculation
        with open("C:\\Users\\Mayra Ochoa\\Documents\\GitHub\\TCP-Visualizer\\pcktsTCP.txt", 'r') as pckts:
             
             for pck in pckts:
                if "<LiveCapture" in pck:
                   total_packet_numberTCP = pck[14:(len(pck)-10)]
                   
                elif "Time since previous frame in this TCP stream:" in pck:
                    #print(pck[20:(len(pck)-8)])
                    y_value = y_value + float(pck[47:(len(pck)-8)])
                    
        yList.append(y_value)
        print(y_value)
        
        #UDP calculation
        with open("C:\\Users\\Mayra Ochoa\\Documents\\GitHub\\TCP-Visualizer\\pcktsUDP.txt", 'r') as pcktss:
             for pck in pcktss:
                 if "<LiveCapture" in pck:
                   total_packet_numberUDP = pck[14:(len(pck)-10)]
                 elif "Time since previous frame" in pck and "Time since previous frame in this TCP stream:" not in pck:
                      y_value2 = y_value2 + float(float(pck[27:(len(pck)-9)]))
                      
        yList.append(y_value2)

        x = np.arange(len(xList))
        n_modes = 1
        width = 0.35
        
        for i in range(n_modes):
            x_offset = i * width
            ax.bar(x+x_offset, yList, width)
        ax.set_xticks(x)
        ax.set_xticklabels(yList)
        ax.set_xticklabels(('TCP', 'GQUIC(UDP)'))
        ax.set_ylabel("Time in seconds")
        if total_packet_numberTCP == total_packet_numberUDP:
            ax.set_xlabel("Number of packets captured: " + total_packet_numberTCP)
        else:
            ax.set_xlabel("\n Number of packets captured: " + total_packet_numberTCP + "(TCP),  " + total_packet_numberUDP + "(GQuic).")
                    
    
        ax.legend()
        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
