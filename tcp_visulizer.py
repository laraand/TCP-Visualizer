import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout,QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
 
class App(QDialog):
 
    def __init__(self):
        super().__init__()
        self.title = 'TCP Visualizer'
        self.left = 0
        self.top = 0
        self.width = 1520
        self.height = 970
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

       
        button = QPushButton('1', self)
        button.resize(70,70)
        button.move(450,900)
        '''button.clicked.connect(self.on_click)'''

        button2 = QPushButton('2', self)
        button2.setToolTip('Window size')
        button2.resize(70,70)
        button2.move(518,900)
        '''button2.clicked.connect(self.on_click)'''

        button3 = QPushButton('3', self)
        button3.setToolTip('Window size')
        button3.resize(70,70)
        button3.move(586,900)
        '''button3.clicked.connect(self.on_click)'''

        button4 = QPushButton('4', self)
        button4.setToolTip('Window size')
        button4.resize(70,70)
        button4.move(654,900)
        '''button4.clicked.connect(self.on_click)'''

        button5 = QPushButton('5', self)
        button5.setToolTip('Window size')
        button5.resize(70,70)
        button5.move(722,900)
        '''button5.clicked.connect(self.on_click)'''

        button6 = QPushButton('6', self)
        button6.setToolTip('Window size')
        button6.resize(70,70)
        button6.move(790,900)
        '''button6.clicked.connect(self.on_click)'''

        button7 = QPushButton('7', self)
        button7.setToolTip('Window size')
        button7.resize(70,70)
        button7.move(858,900)
        '''button7.clicked.connect(self.on_click)'''

        button8 = QPushButton('8', self)
        button8.setToolTip('Window size')
        button8.resize(70,70)
        button8.move(926,900)
        '''button3.clicked.connect(self.on_click)'''

        button9 = QPushButton('9', self)
        button9.setToolTip('Window size')
        button9.resize(70,70)
        button9.move(994,900)
        '''button3.clicked.connect(self.on_click)'''

        button10 = QPushButton('10', self)
        button10.setToolTip('Window size')
        button10.resize(70,70)
        button10.move(1062,900)
        '''button3.clicked.connect(self.on_click)'''

        label = QLabel('Window Size',self)
        label.move(700,850)
        label.setStyleSheet("font: 20pt Comic Sans MS")

        RTTlabel = QLabel('RTT',self)
        RTTlabel.move(200,50)
        RTTlabel.setStyleSheet("font: 20pt Comic Sans MS")

        PktLosslabel = QLabel('Dropped packet count: ',self)
        PktLosslabel.move(900,800)
        PktLosslabel.setStyleSheet("font: 10pt Comic Sans MS")

        Successlabel = QLabel('Successful packet transfer rate: ',self)
        Successlabel.move(1180,800)
        Successlabel.setStyleSheet("font: 10pt Comic Sans MS")

        self.show()

    
            
    @pyqtSlot()
    def on_click(self):
        print('button clicked')
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
