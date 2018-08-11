from typing import List
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
from shapely.geometry import Polygon, Point, MultiPoint
from shapely.affinity import affine_transform
from shapely.ops import snap
import rtree as rt


def v_cell(i0:int,tacke:List[List[float]]) -> List[List[float]]:

    t0 = tacke[i0]
    half_spaces = []
    for i in range(len(tacke)):
        if i != i0:
            t = tacke[i]
            x1 = t[0]
            x2 = t0[0]
            y1 = t[1]
            y2 = t0[1]
            a = x1 - x2
            b = y1 - y2
            c = (-x1*x1 + x2*x2 - y1*y1 + y2*y2)/2
            #if(x1*a + y1*b + c > 0):
            bis_k = [a,b,c]
            half_spaces.append(bis_k)
    #print(np.array(half_spaces,dtype = float))        

    hs = HalfspaceIntersection(np.array(half_spaces),np.array(t0))


    ch = ConvexHull(hs.intersections)
    return Polygon([list(ch.points[i]) for i in ch.vertices])

def v_cell_n(n:int,tacke:List[List[float]]):
    
    pol_U = Polygon()
    for i in range(n):
        pol_i = v_cell(i,tacke)
        pol_i = snap(pol_i,pol_U, 0.01)
        pol_U = pol_U.union(pol_i)
    return pol_U


class rtreeset:
    def __init__(self, tolerance):
        self.rtindex = rt.index.Index(interleaved=False)
        self.tolerance = tolerance
        self.rbr = 0

    def add(self, x,y):
        if(self.contains(x,y)):
            return False
        self.rtindex.insert(self.rbr, (x,x,y,y))
        self.rbr += 1
        return True

    def contains(self,x,y):
        c = self.rtindex.intersection((x-self.tolerance, x+self.tolerance, y-self.tolerance, y+self.tolerance))
        return len(list(c))>0
    




if __name__ == '__main__':
    #hs = v_cell(0,[[0.,0.],[1.,1.],[-1.,-1.],[-1.,1.],[1.,-1.]])
    #print(hs)
    ps = rtreeset(0.1)
    ps.add(0,0)
    ps.add(0,0.7)
    print(ps.add(0.14,0.3))

    print(ps.add(0.2,1.0))
    print(ps.add(0.29,2.0))
    print(ps.add(0.3,2.01))


