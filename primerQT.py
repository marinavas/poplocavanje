import sys
import math
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
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
ir = izomrazne([-3,3,-3,3])
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 textbox - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)

        # Create a button in the window
        self.button = QPushButton('Show text', self)
        self.button.move(20,80)

        self.slk = MyWidget(self)
        self.slk.move(20,120)
        self.slk.resize(350,250)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        self.slk.x0 += 10
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")

class MyWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.pen = QPen(QColor(0,0,0))                      # set lineColor
        self.pen.setWidth(3)                                            # set lineWidth
        self.brush = QBrush(QColor(255,255,255,255))        # set fillColor  
                              # polygon with n points, radius, angle of the first point
        self.x0 = 70
        self.y0 = 70
         
    
    def createPoly(self, n, r):
        polygon = QPolygonF() 
        w = 2 * math.pi / n                                                       # angle per step
        for i in range(n):                                              # add the points of polygon
            t = w * i
            x = r * math.cos(t)
            y = r * math.sin(t)
            polygon.append(QPointF(self.x0+ x, self.y0 + y))

        return polygon

    def paintEvent(self, event):
        pol = Polygon([(0.3,0.1),(0.4, 0.1), (0.45,0.7),(0.2,1), (0.1,0.9),(0.3,0.7)])
        grupa = "p3"
     #   if(grupa != ""):
        pol_qt = generisi_Qpol(ir.izomgen[grupa],pol,[-4,4,-3,3],350,280)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(self.pen)
        painter.setBrush(self.brush) 
        for p in pol_qt:
            painter.drawPolygon(p)
 
 
if __name__ == '__main__':
   
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())