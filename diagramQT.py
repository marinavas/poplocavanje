from matplotlib import pyplot as plt
from shapely.geometry import Polygon, Point, MultiPoint
from shapely.affinity import affine_transform
from descartes.patch import PolygonPatch
import numpy as np
from math import sin, cos, pi
from scipy.spatial import Voronoi, voronoi_plot_2d
from poplocavanje import *
from voronoi import v_cell, v_cell_n




def T(A):
    return (A.x,A.y)

def generisi_t(izl,p,okvir):
    r = []
    for i in izl:
        q = affine_h(p,i)
        x,y = q.x,q.y
        if(x<okvir[1]*1.3 and x>okvir[0]*1.3 and y<okvir[3]*1.3 and y>okvir[2]*1.3):
            r.append(q)
    return r


def voronoi_1_qt(A,okvir,okvir2,izoms):
    slike_A = generisi_t(izoms,A,okvir)
    tacke1 = [T(s) for s in slike_A]
    xmin,xmax,ymin,ymax = okvir
    #vor = Voronoi(tacke1)

    #koordinate = [vor.vertices[p] for p in vor.regions[vor.point_region[0]]]
    koordinate = v_cell(0,tacke1)
   

    poli = Polygon(koordinate)  

    p = generisi_Qpol(izoms,poli,okvir,okvir2)
    
    #t = crtaj([I],poli,ax,'#CC0099',1)
    return (p,tacke1)

def voronoi_qt(M,okvir,okvir2,izoms):
    slike_M = [generisi_t(izoms,A,okvir) for A in M]
    tacke_n=[]
    n = min([len(slike_j) for slike_j in slike_M])

    for i in range(n):
        for s in [T(slike_j[i]) for slike_j in slike_M]:
            tacke_n.append(s)
 #   vor = Voronoi(tacke_n)

    pol_U = v_cell_n(len(M),tacke_n)
    
    if pol_U.geom_type == 'MultiPolygon':
        p = [generisi_Qpol(izoms,pol,okvir,okvir2) for pol in pol_U]
    else:
        p = [generisi_Qpol(izoms,pol_U,okvir,okvir2)]
    return (p,tacke_n)

def voronoi_qt_pol(M,okvir,okvir2,izoms):
    
    (x0,y0) = (M[0].x,M[0].y)
    tacke = [Point(x0,y0)]
    d=10
    for i in range(1,len(M)):
        (x1,y1) = (M[i].x,M[i].y)
        for k in range(1,d):
            a = (d-k)/d
            b = k/d
            tacke.append(Point(a*x0+b*x1, a*y0+b*y1))        
        x0,y0 = x1,y1
    return voronoi_qt(tacke,okvir,okvir2,izoms)

if __name__ == '__main__':
    okvir = [-2,2,-2,2]
    xmin,ymin,xmax,ymax = okvir
    sve_slike = []
    ir = izomrazne(okvir)
    #voronoi_qt(Point(1,1),[-2,2,-2,2],ir.izomgen_p6)