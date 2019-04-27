import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout,QLabel, QSizePolicy, QMessageBox, QLineEdit, QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFormLayout, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap, QImage
import numpy as np
import array
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
plt.style.use('bmh')

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

        #logo icon for window
        self.setWindowIcon(QtGui.QIcon("C:\\Users\\Mayra Ochoa\\Documents\\GitHub\\TCP-Visualizer\\TCPupdatedlogo.png"))
        self.setWindowTitle(self.title)
        
        #Creating graph on main class
        m = PlotCanvas(self, width=6, height=7)
        m.move(750,140)
        
        handlabel = QLabel('Handshake', self)
        handlabel.move(250,50)
        handlabel.setStyleSheet("font: 12pt Comic Sans MS")

        UDPlabel = QLabel('TCP vs GQU  ', self)
        UDPlabel.move(850,80)
        UDPlabel.setStyleSheet("font: 11pt Comic Sans MS")
        
        UDPlabel2 = QLabel('IC(UDP)', self)
        UDPlabel2.move(948,80)
        UDPlabel2.setStyleSheet("font: 11pt Comic Sans MS")

        inc = 0
        inc2 = 0
        
        self.image2 = QLabel(self)
        self.image3 = QLabel(self)
        
        groupBox = QGroupBox()
        form_wid = QWidget()
        formLayout = QFormLayout()
       
        
        #create widget for handshake vertical lines
        for x in range(10):
            imageLabel = QLabel()
            image = QImage('C:\\Users\\Mayra Ochoa\\Documents\\GitHub\\TCP-Visualizer\\right.png')
            imageLabel.setPixmap(QPixmap.fromImage(image))

            imageLabel2 = QLabel()
            image2 = QImage('C:\\Users\\Mayra Ochoa\\Documents\\GitHub\\TCP-Visualizer\\left.png')
            imageLabel2.setPixmap(QPixmap.fromImage(image2))

            
            #self.image2 = QLabel(self)
            '''self.image2.setPixmap(QPixmap('C:\\Users\\Mayra Ochoa\\Documents\\GitHub\\TCP-Visualizer\\right.png'))
            #self.image2.setGeometry(1350,0+inc,700,400)

            #self.image3 = QLabel(self)
            self.image3.setPixmap(QPixmap('C:\\Users\\Mayra Ochoa\\Documents\\GitHub\\TCP-Visualizer\\left.png'))
            self.image3.setGeometry(1350,0+inc2,600,400)
            inc = inc + 100
            inc2 = inc2 + 200
            print(inc)
            print(inc2)

            #formLayout.addRow(QImage(self.image2))'''
            formLayout.addRow(imageLabel2)
            formLayout.addRow(imageLabel)
    
           
        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(700)
        scroll.setFixedWidth(510)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        scroll.setFixedHeight(700)
        scroll.setFixedWidth(510)
            

        scrollArea = QScrollArea()
        scrollArea.setWidget(imageLabel)

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
        #if e.key() == QtCore.Qt.Key_F11:
           #if self.isMaximized():
               #self.showNormal()
           #else:
               #self.showMaximized()


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
        ax = self.figure.add_subplot(111)
        #TCP calculation
        with open("C:\\Users\\Mayra Ochoa\\Documents\\GitHub\\TCP-Visualizer\\pcktsTCP.txt", 'r') as pckts:
             for pck in pckts:
                if "Time since previous frame" in pck:
                   num = len(pck)-8
                   y_value = y_value + float(pck[47:num])
        yList.append(y_value)
        
        #UDP calculation
        with open("C:\\Users\\Mayra Ochoa\\Documents\\GitHub\\TCP-Visualizer\\pcktsUDP.txt", 'r') as pckts:
             for pck in pckts:
                 if "Time since previous frame" in pck:
                    num = len(pck)-8
                    y_value2 = y_value2 + float(pck[47:num])
        yList.append(y_value2)

        x = np.arange(len(xList))
        n_modes = 1
        width = 0.35
        for i in range(n_modes):
            x_offset = i * width
            ax.bar(x+x_offset, yList, width, color=plt.rcParams['axes.color_cycle'][i])
        ax.set_xticks(x)
        ax.set_xticklabels(yList)
        ax.set_xticklabels(('TCP', 'GQUIC(UDP)'))
        ax.set_ylabel("Time in seconds")  
        #ax.set_xlabel("Number of packets captured: ")
        ax.legend()
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
