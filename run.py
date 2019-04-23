import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout,QLabel, QSizePolicy, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
plt.style.use('seaborn-pastel')
import array

class App(QDialog):
 
    def __init__(self):
        super().__init__()
        self.title = 'TCP Visualizer'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 900
        self.initUI()
        #self.keyPressEvent()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #set(QDialog, 'units', 'normalized', 'position', [0.05 0.15 0.9 0.8])
        #RTTGraph
        m = PlotCanvas(self, width=6, height=7)
        m.move(60,140)
        
        #UDP
        u = PlotCanvas(self, width=6, height=7)
        u.move(700,140)

        label = QLabel('RTT',self)
        label.move(700,850)
        label.setStyleSheet("font: 20pt Comic Sans MS")

        RTTlabel = QLabel('RTT',self)
        RTTlabel.move(200,50)
        RTTlabel.setStyleSheet("font: 20pt Comic Sans MS")

        PktLosslabel = QLabel('Dropped packet count: ',self)
        #PktLosslabel = QLabel(numberOfdrop,self)
        PktLosslabel.move(900,800)
        PktLosslabel.setStyleSheet("font: 10pt Comic Sans MS")

        Successlabel = QLabel('Successful packet transfer rate: ',self)
        Successlabel.move(1180,800)
        Successlabel.setStyleSheet("font: 10pt Comic Sans MS")

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
        xList = []
        yList = []
        numberOfdrop = 0
        numPackets = 0
        m = "Packet"
        time = "The RTT"
        ax = self.figure.add_subplot(111)
        with open("C:\\Users\\Mayra Ochoa\\Documents\\GitHub\\TCP-Visualizer\\pcktsTCP.txt", 'r') as pckts:
             for pck in pckts:
                if m in pck:
                   num = len(pck)-2
                   x_value = int(pck[16:num])
                   numberOfdrop += 1
                   #print(pck[16:num])
                   
                if "Time since previous frame" in pck:
                   num = len(pck)-8
                   print(pck[47:num])
                   y_value = float(pck[47:num])
                   yList.append(y_value)
                   xList.append(x_value)
                   numPackets += 1

        print(numberOfdrop-numPackets)
        ax.set_title('TCP') 
        ax.set_xlabel('Smarts')
        ax.set_ylabel('Probability')           
        ax.clear()
        ax.plot(xList, yList)
        self.draw()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
   
    ex = App()
    sys.exit(app.exec_())


