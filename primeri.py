from poplocavanje import *


m = []


pol1 = Polygon([(0.1,0.1),(0.5, 0.2), (1.5,1), (1.8,1.9), (1.3,1.7)])
pol2 = Polygon([(0.1,0.1),(0.5, 0.23),(0.9,0.2),(0.7,1), (0.3,1.7),(0.2,1.9)])
pol3 = Polygon([(0.1,0.1),(0.5, -0.25), (0.9,0.1), (0.5,0.7)])
pol3m = Polygon([(0.1,0.05),(0.4, 0.25), (0.9,0.05), (0.5,0.75)])
pol_tr3 = Polygon([(0.05,0.05),(0.8, 0.3), (1.3,0.05), (0.8,0.45)])
pol_tr6 = Polygon([(0.15,0.05),(0.8, 0.1), (0.95,0.5), (0.5,0.15)])
pol_kv= Polygon([(0.1,0.1),(0.5, 0.23),(0.9,0.2),(0.7,0.9), (0.3,0.5)])
pol_tr4= Polygon([(0.1,0.05),(0.6, 0.1),(0.8,0.3),(0.7,0.6), (0.4,0.3)])


# In[149]:

okvir = [-5,-5,5,5]


xmin,ymin,xmax,ymax = okvir

def nacrtaj(izomgen,p,ime,i):
  #  bx = fig.add_subplot(9,2,i)
    fig = plt.figure(figsize=[5,5])
    bx = plt.axes()
    bx.set_xlim(xmin,xmax)
    bx.set_xticks(range(xmin,xmax+1))
    bx.set_ylim(ymin,ymax)
    bx.set_yticks(range(ymin,ymax+1))
    bx.set_title("grupa "+ime) 
    crtaj(izomgen,p,bx,'#00FFFF')
    fig.savefig('slike/'+ime+'.svg')
    plt.close(fig)

ir = izomrazne(okvir)

nacrtaj(ir.izomgen_p1,pol1,"p1",1)
nacrtaj(ir.izomgen_p2,pol2,"p2",2)
nacrtaj(ir.izomgen_pm, pol1,"pm",3)
nacrtaj(ir.izomgen_pmm,pol2,"pmm",4)
nacrtaj(ir.izomgen_p3,pol3, "p3",5)
nacrtaj(ir.izomgen_p3m1,pol3m,"p3m1",6)
nacrtaj(ir.izomgen_p31m,pol_tr3,"p31m",7) 
nacrtaj(ir.izomgen_p6,pol_tr3,"p6",9)
nacrtaj(ir.izomgen_p6m,pol_tr6,"p6m",10)
nacrtaj(ir.izomgen_p4, pol_kv, "p4",11)
nacrtaj(ir.izomgen_p4m, pol_tr4, "p4m",12)
nacrtaj(ir.izomgen_p4g, pol_tr4, "p4g",13)
nacrtaj(ir.izomgen_cmm, pol_tr4, "cmm",14)
nacrtaj(ir.izomgen_cm,pol_tr4,"cm",15) 
nacrtaj(ir.izomgen_pg,pol2,"pg",16)
