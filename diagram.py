
# coding: utf-8

# In[1]:
from matplotlib import pyplot as plt
from shapely.geometry import Polygon, Point, MultiPoint
from shapely.affinity import affine_transform
from descartes.patch import PolygonPatch
import numpy as np
from math import sin, cos, pi
from scipy.spatial import Voronoi, voronoi_plot_2d
from poplocavanje import *





# In[2]:




# In[3]:

okvir = [-5,-5,5,5]
xmin,ymin,xmax,ymax = okvir
sve_slike = []
ir = izomrazne(okvir)

# In[4]:


def T(A):
    return (A.x,A.y)


# In[5]:


def generisi_t(izl,p):
    r = []
    for i in izl:
        q = affine_h(p,i)
        x,y = q.x,q.y
        if(x<4 and x>-4 and y<4 and y>-4):
            r.append(q)
    return r


# In[6]:


#pol = Polygon([(0.25,0.1),(0.45, 0.1), (0.45,1), (0.25,1)])
#pol = Polygon([(0.4,0.05),(0.9, 0.15),(0.7,0.7), (0.3,0.4)])
#pol = Polygon([(0.4,0.1),(0.5, 0.1), (0.6,0.7),(0.3,1), (0.2,0.9),(0.4,0.7)])
#pol =dopuni(izomgen,pol)
pol = Polygon([(0.3,0.1),(0.4, 0.1), (0.45,0.7),(0.2,1), (0.1,0.9),(0.3,0.7)])
#pol = Polygon([(0.3,0.4),(0.35, 0.4), (0.4,0.7),(0.7,0.8), (0.8,0.9),(0.3,0.9)])
tr = Polygon([(0.1,0.02),(1.9, 0.02), (1,0.5)])
izomgen = ir.izomgen_p6
xmin,xmax,ymin,ymax = (-3,3,-3,3)
okvir = [-3,3,-3,3]
bx = plt.axes()  
bx.set_xlim(xmin,xmax)
bx.set_xticks(range(xmin,xmax+1))
bx.set_ylim(ymin,ymax)
bx.set_yticks(range(ymin,ymax+1))
bx.set_aspect(1)
crtaj(izomgen,tr,bx,'#00FFFF')
crtaj(izomgen,pol,bx,'#CC0099', 0.3)
crtaj([I],pol,bx,'#CC0099', 1)
plt.show()


# In[7]:


bx = plt.axes()  
bx.set_xlim(xmin,xmax)
bx.set_xticks(range(xmin,xmax+1))
bx.set_ylim(ymin,ymax)
bx.set_yticks(range(ymin,ymax+1))
bx.set_aspect(1)
#crtaj(izomgen,tr,bx,'#00FFAA')
crtaj(izomgen,pol,bx,'#CC0099', 0.3)
crtaj([I],pol,bx,'#CC0099', 1)
plt.show()


# In[8]:


slike = generisi_pol(izomgen,pol)


# In[9]:


def dopuni(izom_gen, pol):
    pol1 = pol
    slike = generisi_pol(izomgen,pol)
    for s in slike:
        if(s.intersects(pol)):
            pol1 = pol.union(s)
    return pol1


# In[10]:


def namesti(ax,xmin,xmax,ymin,ymax):
    ax.set_xlim(xmin,xmax)
    ax.set_xticks(range(xmin,xmax+1))
    ax.set_ylim(ymin,ymax)
    ax.set_yticks(range(ymin,ymax+1))
    ax.set_aspect(1)


# In[11]:


tacke1 = []

A = Point(1.2,1.39)
slike_A = generisi_t(izomgen,A)
tacke1 = [T(s) for s in slike_A]

vor = Voronoi(tacke1)

poli = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[0]]])  
ax = plt.axes()
ax.set_xlim(xmin,xmax)
ax.set_xticks(range(xmin,xmax+1))
ax.set_ylim(ymin,ymax)
ax.set_yticks(range(ymin,ymax+1))
ax.set_aspect(1)


crtaj(izomgen,poli,ax,'#00FFFF')
plt.plot([T(s)[0] for s in slike_A],[T(s)[1] for s in slike_A],'C9.')
plt.plot([A.x],[A.y],'b.')
crtaj([I],poli,ax,'#CC0099',1)
plt.show()


# In[12]:


tacke1 = []

A = Point(1,1)
slike_A = generisi_t(izomgen,A)
tacke1 = [T(s) for s in slike_A]

vor = Voronoi(tacke1)
#fig = voronoi_plot_2d(vor)

poli = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[0]]])  
ax = plt.axes()
ax.set_xlim(xmin,xmax)
ax.set_xticks(range(xmin,xmax+1))
ax.set_ylim(ymin,ymax)
ax.set_yticks(range(ymin,ymax+1))
ax.set_aspect(1)


crtaj(izomgen,poli,ax,'#00FFFF')
plt.plot([T(s)[0] for s in slike_A],[T(s)[1] for s in slike_A],'C9.')
plt.plot([A.x],[A.y],'b.')
crtaj([I],poli,ax,'#CC0099',1)
plt.show()


# In[13]:


tacke1 = []

A = Point(pol.exterior.coords[3])
slike_A = generisi_t(izomgen,A)
tacke1 = [T(s) for s in slike_A]

vor = Voronoi(tacke1)
#fig = voronoi_plot_2d(vor)

poli = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[0]]])  
ax = plt.axes()
ax.set_xlim(xmin,xmax)
ax.set_xticks(range(xmin,xmax+1))
ax.set_ylim(ymin,ymax)
ax.set_yticks(range(ymin,ymax+1))
ax.set_aspect(1)


crtaj(izomgen,poli,ax,'#00FFFF')
plt.plot([T(s)[0] for s in slike_A],[T(s)[1] for s in slike_A],'C9.')
plt.plot([A.x],[A.y],'b.')
crtaj([I],poli,ax,'#CC0099',1)
plt.show()


# In[14]:


tacke1 = []

A = Point(pol.exterior.coords[0])
slike_A = generisi_t(izomgen,A)
tacke1 = [T(s) for s in slike_A]

vor = Voronoi(tacke1)
#fig = voronoi_plot_2d(vor)

poli = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[0]]])  
ax = plt.axes()
ax.set_xlim(xmin,xmax)
ax.set_xticks(range(xmin,xmax+1))
ax.set_ylim(ymin,ymax)
ax.set_yticks(range(ymin,ymax+1))
ax.set_aspect(1)


crtaj(izomgen,poli,ax,'#00FFFF')
plt.plot([T(s)[0] for s in slike_A],[T(s)[1] for s in slike_A],'C9.')
plt.plot([A.x],[A.y],'b.')
crtaj([I],poli,ax,'#CC0099',1)
plt.show()


# In[15]:


tacke2 = []

pol_n=0
A = Point(pol.exterior.coords[0])
B = Point(pol.exterior.coords[3])
slike_A = generisi_t(izomgen,A)
slike_B = generisi_t(izomgen,B)
for i in range(min(len(slike_B),len(slike_A))):
    tacke2.append(T(slike_A[i]))
    tacke2.append(T(slike_B[i]))

vor = Voronoi(tacke2)

pol_A = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[0]]])
pol_B = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[1]]])
pol_U=pol_A.union(pol_B)

ax = plt.axes()
namesti(ax,-3,3,-3,3)

crtaj(izomgen,pol_U,ax,'#00FFFF')
crtaj([I],pol_U,ax,'#CC0099',1)
plt.plot([T(s)[0] for s in slike_A],[T(s)[1] for s in slike_A],'C9.')
plt.plot([T(s)[0] for s in slike_B],[T(s)[1] for s in slike_B],'C1.')
plt.show()


# In[16]:


tacke3 = []
A = Point(pol.exterior.coords[0])
B = Point(pol.exterior.coords[3])
C = Point(pol.exterior.coords[2])
#D = Point(pol.exterior.coords[2])
slike_A = generisi_t(izomgen,A)
slike_B = generisi_t(izomgen,B)
slike_C = generisi_t(izomgen,C)
#slike_D = generisi_t(izomgen,D)
n = min([len(slike_j) for slike_j in [slike_A, slike_B, slike_C]])
for i in range(n):
    tacke3.append(T(slike_A[i]))
    tacke3.append(T(slike_B[i]))
    tacke3.append(T(slike_C[i]))
    #tacke4.append(T(slike_D[i]))

vor = Voronoi(tacke3)

pol_A = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[0]]])
pol_B = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[1]]])
pol_C = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[2]]])
#pol_D = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[2]]])
pol_U=pol_A.union(pol_B).union(pol_C)

ax = plt.axes()
namesti(ax,-3,3,-3,3)



crtaj(izomgen,pol_U,ax,'#00FFFF')
crtaj([I],pol_U,ax,'#CC0099',1)
plt.plot([T(s)[0] for s in slike_A],[T(s)[1] for s in slike_A],'C9.')
plt.plot([T(s)[0] for s in slike_B],[T(s)[1] for s in slike_B],'C1.')
plt.plot([T(s)[0] for s in slike_C],[T(s)[1] for s in slike_C],'C2.')
#plt.plot([T(s)[0] for s in slike_D],[T(s)[1] for s in slike_D],'C0.')
plt.show()


# In[17]:


ax = plt.axes()
namesti(ax,-3,3,-3,3)
crtaj([I],pol_U,ax,'#0000FF',0.7)


crtaj(izomgen,pol_U,ax,'#00FFFF')
crtaj([I], pol,ax,'#0000FF',1)
crtaj([I],pol_U,ax,'#CC0099',1)
crtaj([I], pol,ax,'#0000FF',0.2)
crtaj(izomgen, pol,ax,'#0000FF',0.2)
plt.plot([t[0] for t in tacke3],[t[1] for t in tacke3],'C0.')
plt.show()


# In[18]:


tacke4 = []
A = Point(pol.exterior.coords[3])
B = Point(pol.centroid)
C = Point(pol.exterior.coords[1])
D = Point(pol.exterior.coords[2])
slike_A = generisi_t(izomgen,A)
slike_B = generisi_t(izomgen,B)
slike_C = generisi_t(izomgen,C)
slike_D = generisi_t(izomgen,D)
n = min([len(slike_j) for slike_j in [slike_A, slike_B, slike_C, slike_D]])
for i in range(n):
    tacke4.append(T(slike_A[i]))
    tacke4.append(T(slike_B[i]))
    tacke4.append(T(slike_C[i]))
    tacke4.append(T(slike_D[i]))

vor = Voronoi(tacke4)

pol_A = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[0]]])
pol_B = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[1]]])
pol_C = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[3]]])
pol_D = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[2]]])
pol_U=pol_A.union(pol_B).union(pol_C).union(pol_D)

ax = plt.axes()
namesti(ax,-3,3,-3,3)



crtaj(izomgen,pol_U,ax,'#00FFFF')
crtaj([I],pol_U,ax,'#CC0099',1)
plt.plot([T(s)[0] for s in slike_A],[T(s)[1] for s in slike_A],'C1.')
plt.plot([T(s)[0] for s in slike_B],[T(s)[1] for s in slike_B],'C9.')
plt.plot([T(s)[0] for s in slike_C],[T(s)[1] for s in slike_C],'C8.')
plt.plot([T(s)[0] for s in slike_D],[T(s)[1] for s in slike_D],'C2.')
plt.show()


# In[19]:


ax = plt.axes()
namesti(ax,-3,3,-3,3)
crtaj([I],pol_U,ax,'#0000FF',0.7)


crtaj(izomgen,pol_U,ax,'#00FFFF')
crtaj([I], pol,ax,'#0000FF',1)
crtaj([I],pol_U,ax,'#CC0099',1)
crtaj([I], pol,ax,'#0000FF',0.2)
crtaj(izomgen, pol,ax,'#0000FF',0.2)
plt.plot([t[0] for t in tacke4],[t[1] for t in tacke4],'C0.')
plt.show()


# In[20]:



M = [Point(p) for p in pol.exterior.coords]
x0,y0 = pol.exterior.coords[0]
d=1
for i in range(1,len(pol.exterior.coords)):
    x1,y1 = pol.exterior.coords[i]
    for k in np.arange(0,1,1.0/d):
        M.append(Point((1-k)*x0+k*x1, (1-k)*y0+k*y1))        
    x0,y0 = x1,y1
    
M.append(Point(pol.centroid))
slike_M = [generisi_t(izomgen,A) for A in M]
tacke_n=[]
n = min([len(slike_j) for slike_j in slike_M])

for i in range(n):
    for s in [T(slike_j[i]) for slike_j in slike_M]:
        tacke_n.append(s)
vor = Voronoi(tacke_n)

pol_U = Polygon()
for i in range(len(M)):
    pol_I = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[i]]])
    pol_U = pol_U.union(pol_I)

ax = plt.axes()
namesti(ax,-3,3,-3,3)
plt.plot([t[0] for t in tacke_n],[t[1] for t in tacke_n],'C0.')
sve_slike.append([izomgen, pol_U,pol])

crtaj(izomgen,pol_U,ax,'#00FFFF')
crtaj([I],pol_U,ax,'#CC0099',1)
crtaj(izomgen, pol,ax,'#0000FF',0.2)
#crtaj([I], pol,ax,'#0000FF',1)
plt.show()


# In[21]:



M = [Point(p) for p in pol.exterior.coords]
x0,y0 = pol.exterior.coords[0]
d=2
for i in range(1,len(pol.exterior.coords)):
    x1,y1 = pol.exterior.coords[i]
    for k in np.arange(0,1,1.0/d):
        M.append(Point((1-k)*x0+k*x1, (1-k)*y0+k*y1))        
    x0,y0 = x1,y1
    
M.append(Point(pol.centroid))
slike_M = [generisi_t(izomgen,A) for A in M]
tacke_n=[]
n = min([len(slike_j) for slike_j in slike_M])

for i in range(n):
    for s in [T(slike_j[i]) for slike_j in slike_M]:
        tacke_n.append(s)
vor = Voronoi(tacke_n)

pol_U = Polygon()
for i in range(len(M)):
    pol_I = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[i]]])
    pol_U = pol_U.union(pol_I)

ax = plt.axes()
namesti(ax,-3,3,-3,3)
plt.plot([t[0] for t in tacke_n],[t[1] for t in tacke_n],'C0.')
sve_slike.append([izomgen, pol_U,pol])

crtaj(izomgen,pol_U,ax,'#00FFFF')
crtaj([I],pol_U,ax,'#CC0099',1)
crtaj(izomgen, pol,ax,'#0000FF',0.2)
#crtaj([I], pol,ax,'#0000FF',1)
plt.show()


# In[22]:


M = [Point(p) for p in pol.exterior.coords]
x0,y0 = pol.exterior.coords[0]
d=50
for i in range(1,len(pol.exterior.coords)):
    x1,y1 = pol.exterior.coords[i]
    for k in np.arange(0,1,1.0/d):
        M.append(Point((1-k)*x0+k*x1, (1-k)*y0+k*y1))        
    x0,y0 = x1,y1
    
M.append(Point(pol.centroid))
slike_M = [generisi_t(izomgen,A) for A in M]
tacke_n=[]
n = min([len(slike_j) for slike_j in slike_M])

for i in range(n):
    for s in [T(slike_j[i]) for slike_j in slike_M]:
        tacke_n.append(s)
vor = Voronoi(tacke_n)

pol_U = Polygon()
for i in range(len(M)):
    pol_I = Polygon([vor.vertices[p] for p in vor.regions[vor.point_region[i]]])
    pol_U = pol_U.union(pol_I)

ax = plt.axes()
namesti(ax,-3,3,-3,3)
#plt.plot([t[0] for t in tacke_n],[t[1] for t in tacke_n],'C0.')
sve_slike.append([izomgen, pol_U,pol])

crtaj(izomgen,pol_U,ax,'#00FFFF')
crtaj([I],pol_U,ax,'#CC0099',1)
crtaj(izomgen, pol,ax,'#0000FF',0.2)
crtaj([I], pol,ax,'#0000FF',1)
plt.show()


# In[23]:


for s in sve_slike:
    ax = plt.axes()
    namesti(ax,-3,3,-3,3)
    crtaj(s[0],s[1],ax,'#00FFFF')
    crtaj([I],s[1],ax,'#CC0099',1)
    crtaj(s[0], s[2],ax,'#0000FF',0.2)
    crtaj([I], s[2],ax,'#0000FF',1)
    plt.show()

