#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-09-05 02:37 ycopin@lyopc469>

import numpy as np
import random 
import matplotlib.pyplot as plt

def iteration(r, niter=100):

    x = random.uniform(0,1)
    i = 0
    while i < niter and x < 1:
        x = r*x*(1-x)
        i += 1

    return x if x<1 else -1

def generate_diagram(r, ntrials=50):
    """
    Cette fonction retourne (jusqu'à) *ntrials* valeurs d'équilibre
    pour les *r* d'entrée.  Elle renvoit un tuple:

    + le premier élément est la liste des valeurs prises par le paramètre *r*
    + le second est la liste des points d'équilibre correspondants
    """

    r_v = []
    x_v = []
    for rr in r:
        j = 0
        while j<ntrials:
            xx = iteration(rr)
            if xx > 0: # A convergé: il s'agit d'une valeur d'équilibre
                r_v.append(rr)
                x_v.append(xx)
            j += 1                      # Nouvel essai

    return r_v,x_v

r = np.linspace(0,4,1000)
x,y = generate_diagram(r)

plt.plot(x, y, 'r,')
plt.xlabel('r')
plt.ylabel('x')
plt.show()
