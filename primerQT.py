import sys
import math
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QComboBox
from PyQt5.QtGui import QIcon, QPen, QColor, QBrush, QPolygonF, QPainter
from PyQt5.QtCore import pyqtSlot, QPointF
from matplotlib import pyplot as plt
from shapely.geometry import Polygon, Point, MultiPoint
from shapely.affinity import affine_transform
from descartes.patch import PolygonPatch
import numpy as np
#from math import sin, cos, pi
from scipy.spatial import Voronoi, voronoi_plot_2d
from poplocavanje import *
from diagramQT import voronoi_qt

okvir = [-4,4,-3,3]
w = 400
h = 300
ir = izomrazne(okvir)
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Poplocavanje'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.combo = QComboBox(self)

        self.combo.addItems(ir.izomgen.keys())
        self.combo.activated[str].connect(self.onActivated)  

        # Create a button in the window
        self.button = QPushButton('Nacrtaj', self)
        self.button.move(220,20)
        self.button.resize(80,40)

        self.pbx = PictureBox(self)
        self.pbx.move(20,70)
        self.pbx.resize(350,300)
        self.pbx.grupa = "p1"
        self.button.clicked.connect(self.on_click)
        self.show()

        self.combo.move(50,30)
        self.combo.resize(80,40)
        
        
        self.show()


    def onActivated(self, text):     
        self.pbx.grupa = text
    
    @pyqtSlot()
    def on_click(self):
        self.pbx.x0 += 10
        textboxValue = self.textbox.text()
        self.pbx.grupa = textboxValue
        self.pbx.update()

class PictureBox(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.pen = QPen(QColor(0,0,0))                  
        self.pen.setWidth(3)                                        
        self.brush = QBrush(QColor(255,255,255,0))        
        self.x0 = 70
        self.y0 = 70
        self.vp = Point(0.8,1.2)
         
    
    def createPoly(self, n, r):
        polygon = QPolygonF() 
        w = 2 * math.pi / n                                                     
        for i in range(n):                                              
            t = w * i
            x = r * math.cos(t)
            y = r * math.sin(t)
            polygon.append(QPointF(self.x0+ x, self.y0 + y))

        return polygon

    def paintEvent(self, event):
        
        pol = Polygon([(0.3,0.1),(0.4, 0.1), (0.45,0.7),(0.2,1), (0.1,0.9),(0.3,0.7)])
        #pol_qt = generisi_Qpol(ir.izomgen[self.grupa],pol,[-4,4,-3,3],400,300)
        vor = voronoi_qt(self.vp,okvir,ir.izomgen[self.grupa])
        pol_qt = vor[0]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(self.pen)
        painter.setBrush(self.brush) 
        for p in pol_qt:
            painter.drawPolygon(p)
        for p in vor[1]:
            painter.drawPoint(ptq(p,okvir,[0,w,0,h]))
        PictureBox.update(self)
    
    def mousePressEvent(self, event):
        x,y = okok([event.pos().x(),event.pos().y()],[0,w,0,h],okvir)
        self.vp = Point(x,y)
        print(x,y)
        

 


if __name__ == '__main__':
   
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())