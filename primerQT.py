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
from diagramQT import voronoi_qt, voronoi_qt_pol,voronoi_1_qt, PODELA

okvir = [-3,3,-2.25,2.25]
w = 800
h = 600

ir = izomrazne([-4.8,4.8,-3.6,3.6])
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Poplocavanje'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 700
        self.smooth = 0
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.combo = QComboBox(self)

        self.combo.addItems(ir.izomgen.keys())
        self.combo.activated[str].connect(self.onActivated)  

        # Create a button in the window
        self.button = QPushButton('obrisi', self)
        self.button.move(220,20)
        self.button.resize(80,40)

        self.button1 = QPushButton('umeksaj', self)
        self.button1.move(320,20)
        self.button1.resize(80,40)

        self.pbx = PictureBox(self)
        self.pbx.move(20,70)
        self.pbx.resize(w,h)
        self.pbx.grupa = "p1"
        self.button.clicked.connect(self.on_click)
        self.button1.clicked.connect(self.on_click1)
        self.show()

        self.combo.move(50,20)
        self.combo.resize(80,40)
        
        
        self.show()


    def onActivated(self, text):     
        self.pbx.grupa = text
        self.pbx.repaint()
    
    @pyqtSlot()
    def on_click(self):
        self.pbx.tacke=[Point(0,0)]
        self.pbx.repaint()

    @pyqtSlot()
    def on_click1(self):
        self.pbx.smooth = 1
        self.pbx.repaint()
        self.pbx.smooth = 0

class PictureBox(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.smooth = 0
        self.pen = QPen(QColor(0,0,0))                  
        self.pen.setWidth(3)                                        
        self.brush = QBrush(QColor(255,255,255,0))        
        self.x0 = 70
        self.y0 = 70
        self.vp = Point(0,0)
        self.tacke = [self.vp]
         
    
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
        #pol_vor, tacke_vor = voronoi_qt_pol(self.tacke,okvir,[0,w,0,h],ir.izomgen[self.grupa])
        if(self.smooth ==1):
             pol_vor, tacke_vor = voronoi_qt_pol(self.tacke,okvir,[0,w,0,h],ir.izomgen[self.grupa],5)
        else:
             pol_vor, tacke_vor = voronoi_qt_pol(self.tacke,okvir,[0,w,0,h],ir.izomgen[self.grupa],1)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        painter.setPen(QPen(QColor(0,125,125)))
        painter.setBrush(QBrush(QColor(200,0,120,200)))
        for p in pol_vor:
            painter.drawPolygon(p[0])
        
        painter.setPen(self.pen)
        #painter.setBrush(self.brush) 
        painter.setBrush(QBrush(QColor(255,255,255,50)))
        for p in pol_vor:
            for q in p:
                painter.drawPolygon(q)
        
        for i in range(len(self.tacke)):
            if i % 1 == 0:
                p = self.tacke[i]
                painter.drawPoint(ptq(p,okvir,[0,w,0,h]))          
        

        
       
            
        #PictureBox.update(self)
    
    def mousePressEvent(self, event):
        x,y = okok([event.pos().x(),event.pos().y()],[0,w,0,h],okvir)
        self.vp = Point(x,y)
        self.tacke.append(self.vp)
        self.update()
        

 


if __name__ == '__main__':
   
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())