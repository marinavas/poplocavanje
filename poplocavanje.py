
from matplotlib import pyplot as plt
from shapely.geometry import Polygon, Point, MultiPoint
from shapely.affinity import affine_transform
from descartes.patch import PolygonPatch
import numpy as np
from math import sin, cos, pi
from scipy.spatial import Voronoi, voronoi_plot_2d
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QPen, QColor, QBrush, QPolygonF, QPainter
from PyQt5.QtCore import pyqtSlot, QPointF
from geom import rtreeset



def affine_h(geom, m):
    return affine_transform(geom, [m[0,0],m[0,1],m[1,0],m[1,1],m[0,2],m[1,2]])

I = np.array([
        [ 1,  0,  0],
        [ 0,  1,  0],
        [ 0,  0,  1]])
def inv(x):
    return np.linalg.inv(x)




def transl(tx,ty):
    return np.array([
        [ 1,  0,  tx],
        [ 0,  1,  ty],
        [ 0,  0,  1]])


# Funkcija `rot0` konstruiše matricu za rotaciju oko koordinatnog početka za zadati ugao:

# In[4]:


def rot0(fi):
    return np.array([
        [ cos(fi),  sin(fi),  0],
        [-sin(fi),  cos(fi),  0],
        [       0,        0,  1] ])


# Funkcija `reflX` konstruiše matricu za refleksiju oko x-ose:

# In[5]:


def reflX():
    return np.array([
        [ 1,  0,  0],
        [ 0,  -1,  0],
        [ 0,  0,  1] ])


# Prednost korišćenja homogenih koordinata je u tome što slaganje izometrija računamo kao množenje matrica. Na taj način funkciju `rot`, koja konstruiše matricu za rotaciju oko zadate tačke, možemo definisati kao:

# In[6]:


def rot(fi, cx, cy):
    return transl(cx, cy) @  rot0(fi) @ transl(-cx, -cy)
def sim0(cx,cy):
    return rot(pi,cx,cy)


# Slično konstruišemo refleksiju oko proizvoljne ose zadate koordinatama jedne tačke na toj osi i uglom koji ona pravi sa x-osom:

# In[7]:


def refl(ax,ay,fi):
    return transl(ax,ay) @ rot0(fi) @ reflX() @ rot0(-fi) @ transl(-ax,-ay)


# Ukoliko osa prolazi kroz koordinatni početak i tačku a, matricu osne refleksije možemo i direktno konstruisati bez primene trigonometrijskih funkcija  na sledeći način:

# In[8]:


def refl1(ax,ay):
    r = (ax*ax+ay*ay) 
    return np.array([
        [ (ax*ax-ay*ay)/r,  2*ax*ay/r,  0],
        [ 2*ax*ay/r, (ay*ay-ax*ax)/r ,  0],
        [         0,                0,  1] ])


# Koristeći to možemo konstruisati refleksiju oko ose zadate dvema tačkama

# In[9]:


def refl2(ax,ay,bx,by):
    return transl(ax,ay)@refl1(bx-ax,by-ay)@transl(-ax,-ay)


# Klizajuću refleksiju predstavljamo kao kompozicija translacije i refleksije

# In[105]:


def glref(ax,ay,bx,by):
    return refl2(ax,ay,bx,by)@transl((bx-ax),(by-ay))


def p1(x1,y1,x2,y2):
    tr1 = transl(x1, y1)
    tr2 = transl(x2, y2)
    return [I,tr1,tr2,inv(tr1), inv(tr2)]


# Grupu **p2** čine tri centralne simetrije. Fundamentalni domen može biti trougaoni ili četvorougaoni. Radi lakšeg implementiranja, posmatraćemo kao jednu simetriju (kojom fundamentalni domen proširujemo do paralelograma) i dve translacije. Generiše se vektorima tih translacija (stranice dobijenog paralelograma) i jednim temenom. 
# 
# $$\begin{Bmatrix}\begin{bmatrix}-1 & 0 & 2a_x +v_x+u_x\\ 0 & -1& 2a_y +v_y+u_y \\ 0 & 0 & 1\end{bmatrix}&,& \begin{bmatrix}1 & 0 & v_x\\ 0 & 1&v_y \\ 0 & 0 & 1\end{bmatrix}&,& \begin{bmatrix}1 & 0 & u_x\\ 0 & 1&u_y \\ 0 & 0 & 1\end{bmatrix}  \end{Bmatrix}$$
# 

# In[12]:


def p2(ax,ay,x1,y1,x2,y2):
    sym = rot(pi,ax,ay)
    return p1(2*x1,2*x2,y1,y2) + [sym, inv(sym)]


# Grupu **pm** čine refleksije i translacije. Fundamentalni domen je pravougaonik* . Generišu ga jedno teme i dva vektora.
# 
# $$\begin{Bmatrix}\begin{bmatrix} \frac{v_{x}^{2}-v_{y}^{2} }{v_{x}^{2}+v_{y}^{2}}& \frac{2v_{x}v_{y}}{v_{x}^{2}+v_{y}^{2}}& \frac{2a_yv_{x}v_{y} + a_x(v_{x}^{2}-v_{y}^{2}-1)}{v_{x}^{2}+v_{y}^{2}}\\\frac{2v_{x}v_{y}}{v_{x}^{2}+v_{y}^{2}}&\frac{v_{y}^{2}-v_{x}^{2} }{v_{x}^{2}+v_{y}^{2}}& \frac{2a_xv_{x}v_{y} + a_y(v_{x}^{2}-v_{y}^{2}-1)}{v_{x}^{2}+v_{y}^{2}} \\ 0 & 0 & 1\end{bmatrix} & ,& \begin{bmatrix}1 & 0 & 2v_x\\ 0 & 1&2v_y \\ 0 & 0 & 1\end{bmatrix}& ,& \begin{bmatrix}1 & 0 & u_x\\ 0 & 1&u_y \\ 0 & 0 & 1\end{bmatrix}  \end{Bmatrix}$$
# 

# In[13]:


def pm(ax,ay,x1,y1,x2,y2):
    ref = refl2(ax,ay, ax+x1,ay+y1)
    return p1(x1,y1,2*x2,2*y2) +[ref]


# Grupu **pmm** čine refleksije u normalnim pravcima i centralne simetrije u temenima. Za implementaciju dovoljno je gledati npr samo refleksije
# ????
# Radi optimizacije mozemo koristiti samo refleksije i translacije??

# In[14]:


def pmm(ax,ay, x1,y1,x2,y2):
    ref1 = refl2(ax,ay, ax+x1, ay+y1)
    ref2 = refl2(ax,ay, ax+x2, ay+y2)
    return [ref1,ref2] + p1(2*x1,2*y1, 2*x2,2*y2)


# Grupu **pg** cine refleksija i klizajuca refleksija

# In[131]:


def pg(ax,ay,x1,y1,x2,y2):
    ref = refl2(ax,ay, ax+x1, ay+y1)
    gler = glref(ax + x2/2, ay + y2/2, ax + x1 + x2/2, ay + y1 + y2/2)
    trans = transl(-2*x1,-2*y1)
    return [I,ref,gler, trans]


# Grupu **cm** cine refleksija i klizajuca refleksija

# In[64]:


def cm(ax,ay,bx,by,cx,cy): 
    glref1 = glref((ax+cx)/2,(ay+cy)/2, (bx+cx)/2,(by+cy)/2)
    ref2 = refl2(ax,ay,bx,by)
    return [I,ref2,glref1, inv(glref1)]


# Grupu **p3** cine tri rotacije za ugao $\frac{2\pi}{3}$

# In[15]:


def p3(ax,ay,bx,by,cx,cy): 
    r1 = rot(2*pi/3, ax,ay)
    r2 = rot(2*pi/3,bx,by)
    r3 = rot(2*pi/3,cx,cy)
    return [I, r1,r2,r3]


# Grupu **p3m1** pored rotacija za ugao $\frac{2\pi}{3}$ ima refleksije

# In[16]:


def p3m1(ax,ay,bx,by,cx,cy): 
    r1 = rot(2*pi/3, ax,ay)
    r2 = rot(2*pi/3,bx,by)
    r3 = rot(2*pi/3,cx,cy)
    ref = refl2(ax,ay,bx,by)
    return [I, ref,r1,r2,r3]


# Grupu **p31m** sadrzi rotacije za ugao $\frac{2\pi}{3}$ oko svih temena i refleksiju preko osnovice

# In[17]:


def p31m(ax,ay,bx,by,cx,cy): 
    r1 = rot(2*pi/3,cx,cy)
    ref = refl2(ax,ay,bx,by)
    return [I,r1,ref]


# Grupu **p6** sadrzi rotacije za ugao $\frac{2\pi}{3}$ oko jednog i $\frac{\pi}{3}$ oko ostala dva temena i 

# In[18]:


def p6(ax,ay,bx,by,cx,cy): 
    r1 = rot(pi/3, ax,ay)
    r2 = rot(pi/3,bx,by)
    r3 = rot(2*pi/3,cx,cy)
    return [I,r1,r2,r3]


# Grupu **p6m** ima i refleksiju

# In[19]:


def p6m(ax,ay,bx,by,cx,cy): 
    r1 = rot(pi/3, ax,ay)
    r2 = rot(pi/3,2*bx,2*by)
    ref = refl2(bx,by,cx,cy)
    return [I,r1,r2,ref]


# Grupa **p4** 
# 

# In[20]:


def p4(ax,ay,bx,by,cx,cy): 
    r1 = rot(pi/2, ax,ay)
    r2 = rot(pi/2,cx,cy)
    r3 = rot(pi,bx,by)
    return [I,r1,r2,r3]


# Grupa **p4m** 

# In[21]:


def p4m(ax,ay,bx,by,cx,cy):
    r1 = rot(pi/2, ax,ay)
    r2 = rot(pi/2, cx,cy)
    ref = refl2(bx,by,cx,cy)
    return [I,r1,r2,ref]


# Grupa **cmm** 

# In[90]:


def cmm(ax,ay,bx,by,cx,cy):
    r1 = rot(pi, ax,ay)
    r2 = rot(pi/2, bx,by)
    r3 = rot(pi,(ax+cx)/2,(ay+cy)/2 )
    ref = refl2(bx,by,cx,cy)
    ref2 = refl2(ax,ay,bx,by)
    return [I,r1,r2,r3]


# Grupa **p4g** 

# In[38]:


def p4g(ax,ay,bx,by,cx,cy):
    r1 = rot(pi, ax,ay)
    r2 = rot(pi/2, bx,by)
    ref = refl2(ax,ay,cx,cy)
    return [I,r1,r2,ref]


# **

# ## Konstruisanje grupa izometrijskih transformacija

# **  uz teorijski uvod implementirati funkcije za konstruisanje grupa iz transformacija sa primerima crtanja i funkcije za svih 17 grupa

# In[23]:


def generisi(gen,okvir):
    xmin,xmax,ymin,ymax = okvir
    l = []
    rt = rtreeset(0.00001)
    def generisi_rek(iz): 
        x,y,_ = iz @ (0,0,1) 
        
        if(rt.add(x,y)):
            l.append(iz)
        else:
            return
        if(x>xmax*1.5 or x<xmin*1.5 or y>ymax*1.5 or y<ymin*1.5 ):
            return
        for i in gen:
            generisi_rek(i @ iz)
            
    generisi_rek(transl(0,0))
    
    return l
        



def crtaj(izl,p,axes,color = '#A901DB',a=0.3):
    for i in izl:
        q = affine_h(p,i)
        patch = PolygonPatch(q, facecolor=color, edgecolor='#000000', alpha=a, zorder=2)
        axes.add_patch(patch) 
        


# In[148]:




# In[36]:


def generisi_pol(izl,p):
    r = []

    for i in izl:
        q =affine_h(p,i)
        #x,y = q.exterior.coords[0] 
        #if(x<3 and x>-3 asnd y<3 and y>-3):
        r.append(q)
    return r


# # Bibliografija

# 1. Schattschneider, Doris. "The plane symmetry groups: their recognition and notation." *The American Mathematical Monthly* 85.6 (1978): 439-450.

class izomrazne:


    


    def __init__(self, okvir):
        self.izom_p1 = p1(1,0,0,1.5)
        self.izom_p2 = p2(-0.5,-0.5,1,0,0,1.5)
        self.izom_pm  = pm(-0.5,-0.5,1,0,0,1.5)
        self.izom_pmm = pmm(-0.5,-0.5,1,0,0,1.5)
        self.izom_p3 = p3(-0.5,-0.5,0.5,-0.5, 0,sin(pi/3)-0.5)
     #   self.izom_p3m1 = p3m1(-0.5,-0.5,0.5,-0.5, 0,sin(pi/3)-0.5)


        # In[27]:


        self.izomgen_p1 = generisi(self.izom_p1,okvir)
        self.izomgen_p2 = generisi(self.izom_p2,okvir)
        self.izomgen_pm = generisi(self.izom_pm,okvir)
        self.izomgen_pmm= generisi(self.izom_pmm,okvir)
        self.izomgen_p3 = generisi(self.izom_p3,okvir)
      #  self.izomgen_p3m1 = generisi(self.izom_p3m1,okvir)


        # In[132]:


        self.izom_pg = pg(-0.5,-0.5,1,0,0,2)
        self.izomgen_pg= generisi(self.izom_pg,okvir)


        # In[28]:


        self.izom_p31m = p31m(-0.5,-0.5,1.5,-0.5, 0.5, 2*sin(pi/3)/3-0.5)
        self.izomgen_p31m = generisi(self.izom_p31m,okvir)


        # In[29]:


        self.izom_p6 = p6(-0.5,-0.5,1.5,-0.5, 0.5, 2*sin(pi/3)/3-0.5)
        self.izomgen_p6 = generisi(self.izom_p6,okvir)
        print(len(self.izomgen_p6))

        # In[30]:


        #self.izom_p6m = p6m(-0.5,-0.5,0.5,-0.5, 0.5, 2*sin(pi/3)/3-0.5)
        #self.izomgen_p6m = generisi(self.izom_p6m,okvir)


        # In[31]:


        self.izom_p4= p4(-0.5,-0.5,0.5,-0.5, 0.5,0.5)
        self.izomgen_p4=generisi(self.izom_p4,okvir)


        # In[32]:


        self.izom_p4m= p4m(-0.5,-0.5,0.5,-0.5, 0.5,0.5)
        self.izomgen_p4m=generisi(self.izom_p4m,okvir)


        # In[39]:


        self.izom_p4g= p4g(-0.5,-0.5,0.5,-0.5, 0.5,0.5)
        self.izomgen_p4g=generisi(self.izom_p4g,okvir)


        # In[91]:


        self.izom_cmm= cmm(-0.5,-0.5,0.5,-0.5, 0.5,0.5)
        self.izomgen_cmm=generisi(self.izom_cmm,okvir)


        # In[106]:


        self.izom_cm = cm(-0.5,-0.5,1.5,-0.5, 0.5, 4*sin(pi/3)/3-0.5)
        self.izomgen_cm= generisi(self.izom_cm,okvir)
        
        self.izomgen = {"p1":self.izomgen_p1, 
        "p2":self.izomgen_p2,
        "p3":self.izomgen_p3,
        "p4":self.izomgen_p4,
        "p4m":self.izomgen_p4m, 
        "p4g":self.izomgen_p4g, 
        "pg":self.izomgen_pg,
        "pm":self.izomgen_pm,
        "pmm":self.izomgen_pmm,
        "p31m":self.izomgen_p31m, 
#        "p3m1":self.izomgen_p3m1,
        "p6":self.izomgen_p6,
        #"p6m":self.izomgen_p6m,
        "cm":self.izomgen_cm,
        "cmm":self.izomgen_cmm}
        
        # In[47]:

def sh_to_qt(slike,okvir,okvir2):
    slike_qt = []
    w = okvir2[1]
    h = okvir2[3]
    for s in slike:
        polygon = QPolygonF()
        for p in s.exterior.coords:
            polygon.append(QPointF((p[0]-okvir[0])*w/(okvir[1]-okvir[0]),h-(p[1]-okvir[2])*h/(okvir[3]-okvir[2])))
        slike_qt.append(polygon)
    return slike_qt

def okok(p,ok1,ok2):
    x1,y1 = p
    x2 = (x1 - ok1[0])/(ok1[1]-ok1[0])*(ok2[1]-ok2[0]) + ok2[0]
    y2 = ok2[3]- (y1 - ok1[2])/(ok1[3]-ok1[2])*(ok2[3]-ok2[2])
    return(x2,y2)

def ptq(p,ok1,ok2):
    return QPointF(okok((p.x,p.y),ok1,ok2)[0],okok((p.x,p.y),ok1,ok2)[1])

def stq(p,ok1,ok2):
    return QPointF(okok((p[0],p[1]),ok1,ok2)[0],okok((p[0],p[1]),ok1,ok2)[1])

def qts(q,ok1,ok2):
    return Point(okok(q,ok1,ok2))

def generisi_Qpol(izl,p,okvir,okvir2):
    return sh_to_qt(generisi_pol(izl,p),okvir,okvir2)

#if __name__ == '__main__':
    