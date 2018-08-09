from matplotlib import pyplot as plt
from shapely.geometry import Polygon, Point, MultiPoint
from shapely.affinity import affine_transform
from descartes.patch import PolygonPatch
import numpy as np
from math import sin, cos, pi
from scipy.spatial import Voronoi, voronoi_plot_2d
from poplocavanje import *





def T(A):
    return (A.x,A.y)

def generisi_t(izl,p,okvir):
    r = []
    for i in izl:
        q = affine_h(p,i)
        x,y = q.x,q.y
        if(x<okvir[1] and x>okvir[0] and y<okvir[3] and y>okvir[2]):
            r.append(q)
    return r


def voronoi_qt(A,okvir,izoms):
    slike_A = generisi_t(izoms,A,okvir)
    tacke1 = [T(s) for s in slike_A]
    xmin,xmax,ymin,ymax = okvir
    vor = Voronoi(tacke1)

    koordinate = [vor.vertices[p] for p in vor.regions[vor.point_region[0]]]

    poli = Polygon(koordinate)  
    p = generisi_Qpol(izoms,poli,okvir,400,300)
    
    #t = crtaj([I],poli,ax,'#CC0099',1)
    return [p,tacke1]

if __name__ == '__main__':
    okvir = [-2,2,-2,2]
    xmin,ymin,xmax,ymax = okvir
    sve_slike = []
    ir = izomrazne(okvir)
    #voronoi_qt(Point(1,1),[-2,2,-2,2],ir.izomgen_p6)