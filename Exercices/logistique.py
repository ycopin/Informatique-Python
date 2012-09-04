# -*- coding: utf-8 -*-
import matplotlib.pyplot as pl
import numpy as np
import random as rd

def iter(r,niter=100):
    x=rd.uniform(0,1)
    i=0
    while(i<niter and x < 1):
        x=r*x*(1-x)
        i+=1
    if x<1:
        return x
    else:
        return -1

def generate_diagram(ntrials=50):
    """
    cette fonction fait varier r sur la ligne des réels
    elle renvoit un tuple:
    le premier élément est la liste des valeurs prises par le paramètre r
    le second est la liste des points d'équilibre correspondants
    
    """
    rrange=np.linspace(0,4,1000)
    r_v=[]
    x_v=[]
    
    for r in rrange:
        i=0
        while(i<ntrials):
            x=iter(r)
            if(x!=-1):
                r_v.append(r)
                x_v.append(x)
            i+=1
    return (r_v,x_v)

T=generate_diagram()
pl.plot(T[0],T[1],'r,')
pl.xlabel('r')
pl.ylabel('x')
pl.show()
