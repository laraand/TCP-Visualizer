
import warnings
import matplotlib.cbook
import pyshark
import webbrowser
import time
import sys
import re
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout,QLabel, QSizePolicy, QMessageBox, QLineEdit, QWidget, QFormLayout, QScrollArea, QInputDialog, QLineEdit
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
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screenwidth = user32.GetSystemMetrics(0)
screenheight = user32.GetSystemMetrics(1)
numPackets = 0

class App(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'TCP Visualizer'
        self.left = 10
        self.top = 10
        self.width = screenwidth - 100
        self.height = screenheight - 100
        self.numPackets = 0
        self.initUI()
        #self.keyPressEvent()

    def getInteger(self):
        i, okPressed = QInputDialog.getInt(self, "Get integer","Number of Packets:", 0, 0, 10000, 1)
        if okPressed:
            print(i)
        self.numPackets = i
        #print("Num packets: ", i)
        start(self.numPackets)

    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Continue","Press Enter to continue:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
        start2(self.numPackets)
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

        #logo icon for window
        self.setWindowIcon(QtGui.QIcon("imgs\\TCPupdatedlogo.png"))
        self.setWindowTitle(self.title)

        self.getInteger()

        self.getText()
        
        #Creating graph on main class
        m = PlotCanvas(self, width=4.5, height=4.5)
        m.move(screenwidth / 2, 100)

        button = QPushButton('TCP', self)
        button.resize(100,50)
        button.move(screenwidth /2 ,screenheight - 200)
        button.clicked.connect(self.on_clickTCP)
        
        button = QPushButton('GQUIC(UDP)', self)
        button.resize(100,50)
        button.move(screenwidth /2 + 100,screenheight - 200)
        button.clicked.connect(self.on_clickUDP)
        
        button = QPushButton('TCP vs GQUIC(UDP)', self)
        button.resize(140,50)
        button.move(screenwidth /2 + 200,screenheight - 200)
        button.clicked.connect(self.on_clickBoth)
        
        
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
        #formLayout.move( 250, 250)


        #create widget for handshake vertical lines
        source = packetSeqAck[0][3]
        
        print(source)

        for x in range(len(packetSeqAck)):
            tL = QLabel("Sequence Number = " + packetSeqAck[x][0] + ", Acknowledgment Number = " + packetSeqAck[x][1] + ", Size of Packet: " + str(packetSeqAck[x][2]))

            if(packetSeqAck[x][3] == source):
                imageLabel = QLabel()
                image = QImage('imgs\\right.png')
                imageLabel.setPixmap(QPixmap.fromImage(image))
                formLayout.addRow(tL)
                formLayout.addRow(imageLabel)
            else:
                imageLabel = QLabel()
                image = QImage('imgs\\left.png')
                imageLabel.setPixmap(QPixmap.fromImage(image))
                formLayout.addRow(tL)
                formLayout.addRow(imageLabel)

            # imageLabel = QLabel()
            # image = QImage('imgs\\left.png')
            # imageLabel.setPixmap(QPixmap.fromImage(image))

            # imageLabel2 = QLabel()
            # image2 = QImage('imgs\\right.png')
            # imageLabel2.setPixmap(QPixmap.fromImage(image2))

            # formLayout.addRow(tL)
            # formLayout.addRow(imageLabel2)
            # formLayout.addRow(imageLabel)
    
           
        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout(self)

        scroll.setFixedHeight(screenheight /2)
        scroll.setFixedWidth(screenwidth /2 - 125)
        layout.addWidget(scroll)
        
        #self.setLayout(layout)

        #call handshake definition, in order to obtain data
        #self.handshake()

        self.show()

            
    @pyqtSlot()
    def on_clickUDP(self):
        print('UDP button clicked')

    def on_clickTCP(self):
        print('TCP button clicked')

    def on_clickBoth(self):
        #print('button clicked')
        self.PC = PlotCanvas()
        #self.PC = PlotCanvas(self, width=4.5, height=4.5)
        #self.PC.move(screenwidth / 2, 100)
        self.PC.show()

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
        with open("pcktsTCP.txt", 'r') as pckts:
             
             for pck in pckts:
                if "<LiveCapture" in pck:
                   total_packet_numberTCP = pck[14:(len(pck)-10)]
                   
                elif "Time since previous frame in this TCP stream:" in pck:
                    #print(pck[20:(len(pck)-8)])
                    y_value = y_value + float(pck[47:(len(pck)-8)])
                    
        yList.append(y_value)
        print(y_value)
        
        #UDP calculation

        # with open("pcktsUDP.txt", 'r') as pckts:
        #     for pck in pckts:

        with open("pcktsUDP.txt", 'r') as pcktss:
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

# SNIFFY PORTION

#Variables
#filename = "c:\\Users\\Mytchell\\Desktop\\pckts.txt"
packetSeqAck = []
# loopCount = 0  
seqAck = (0,0) 
# Windows - This can be used to open the chrome browser from this script with a specified link
# url = 'http://docs.python.org/'
# chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
# webbrowser.get(chrome_path).open(url)
##################################################################################################

def parseUDP():
    #array holding parsed data
    timeBetweenUDP = []
    totalTimeUDP = 0
    file = open("pcktsUDP.txt", "r")
    #content is an array that contains each line of the "pckts.txt" as its own element 
    contents = file.readlines()
    for line in contents:
        # if "Time since first frame:" in line:
        #   totalTimeUDP += re.findall(r'[-+]?\d*\.\d+|\d+', line)
        
        if "Time since previous frame:" in line:
            timeBetweenUDP += re.findall(r'[-+]?\d*\.\d+|\d+', line)

    file.close()

    for i in timeBetweenUDP:
        totalTimeUDP += float(i)

    print("UDP time data :")
    print(timeBetweenUDP)
    print("total time: \n")
    print(totalTimeUDP)

def parseSeqAck(sequence,acknowledgment,size,src,dest):
    # store tuple
    seqAck = ((str(sequence)),(str(acknowledgment)),size,src,dest)
    # print (str(seq) + " , " + str(ack))
    packetSeqAck.append(seqAck)

    return(packetSeqAck)


def parse():
    #array holding parsed data
    timeBetweenTCP = []
    totalTimeTCP = 0
    seq = 0
    ack = 0
    src = 0
    dest = 0
    size = 0
    file = open("pcktsTCP.txt", "r")
    #content is an array that contains each line of the "pckts.txt" as its own element 
    contents = file.readlines()

        #Parse
    for line in contents:

        if "Source:" in line:
            src = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)

        if "Destination:" in line:
            dest = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)

    

        if "TCP Segment Len:" in line:
            size = re.findall(r'\d+', line)

        if "Sequence number:" in line:
            seq = re.findall(r'\d+', line)

        if "Acknowledgment number:" in line:
            ack = re.findall(r'\d+', line)

            parseSeqAck(seq,ack,size,src,dest)

        if "Time since previous frame in this TCP stream:" in line:
            timeBetweenTCP += re.findall(r'[-+]?\d*\.\d+|\d+', line)

        # # store tuple
        #     seqAck = (seq,ack)
        # # print (str(seq) + " , " + str(ack))
        #     packetSeqAck.append(seqAck)
    loopCount = len(packetSeqAck)
    print(packetSeqAck)
    for i in timeBetweenTCP:
        totalTimeTCP += float(i)

    print("TCP time timeBetweenTCP")
    print(timeBetweenTCP)

    print("total time TCP: \n")
    print(totalTimeTCP)
    #Parse
    # for line in contents:
    #     firstParse.append(line.strip()) # add line to array as we pass through (strip removes newline)
    #     print(line.strip()) # print lines as we're going through file

    file.close()

def start(numPackets):
    print("Number of packets: ", numPackets)
    # Main starts here
    print("Starting with TCP")

    #numPackets = int(input("Enter # packets to capture : "))
    print("Please wait while packets accumulate...")

    #Redirect all output from "prints" to a file called "pckts.txt" (change the path to work on your machine)
    file = open("pcktsTCP.txt", "w")
    sys.stdout = file

    #LiveCapture with the selected interface : 'Wi-Fi'
    capture = pyshark.LiveCapture(interface='Wi-Fi')
    capture.sniff(packet_count=numPackets)

    #Printing (stdout being directed to file 'pckts.txt')
    print(capture)
    for pkt in capture:
        #this allows for the for loop to be exectued until the counter reaches our desired time limit
        #if(time.time() < t_end):
        print (pkt)

    file.close()
    sys.stdout = sys.__stdout__

    print ("Capture Data Finished")
    parse()
    print("parse finished running")

def start2(numPackets):
    print("Number of packets: ", numPackets)
    print("Now parsing UDP")

    #numPackets = int(input("Enter # of UDP packets to capture : "))
    print("Please wait while packets accumulate...")

    #Redirect all output from "prints" to a file called "pckts.txt" (change the path to work on your machine)
    file = open("pcktsUDP.txt", "w")
    sys.stdout = file

    #LiveCapture with the selected interface : 'Wi-Fi'
    capture = pyshark.LiveCapture(interface='Wi-Fi')
    capture.sniff(packet_count=numPackets)

    print(capture)
    for pkt in capture:
        #this allows for the for loop to be exectued until the counter reaches our desired time limit
        #if(time.time() < t_end):
        print (pkt)

    file.close()
    sys.stdout = sys.__stdout__


    print ("Capture Data Finished")
    parseUDP()
    print("UDP parse finished running")

if __name__ == '__main__':
    #start()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

