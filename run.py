import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout,QLabel, QSizePolicy, QMessageBox, QWidget
from PyQt5.QtCore import pyqtSlot
import numpy as np
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
        
        #Creating graph on main class
        m = PlotCanvas(self, width=6, height=7)
        m.move(750,140)
        
        UDPlabel = QLabel('TCP vs UDP', self)
        UDPlabel.move(950,80)
        UDPlabel.setStyleSheet("font: 20pt Comic Sans MS")

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
        ax.set_xticklabels(('TCP', 'UDP'))
        ax.set_ylabel("Time in seconds")  
        #ax.set_xlabel("Number of packets captured: ")
        ax.legend()
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())