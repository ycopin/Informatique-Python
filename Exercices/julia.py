#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-09-05 02:10 ycopin@lyopc469>

"""Visualisation de l'`ensemble de julia
<http://fr.wikipedia.org/wiki/Ensemble_de_Julia>`_.

Exercice: proposer des solutions pour accélerer le calcul.
"""

import numpy as np
import matplotlib.pyplot as plt

c = complex(0.284,0.0122)           # Constante

xlim = 1.5                          # [-xlim,xlim] × i[-xlim,xlim]
nx = 1000                           # Nb de pixels
niter = 100                         # Nb d'itérations

x = np.linspace(-xlim, xlim, nx)    # nx valeurs de -xlim à +xlim
xx,yy = np.meshgrid(x, x)           # Tableaux 2D
z = xx + 1j*yy                      # Portion du plan complexe
for i in range(niter):              # Itération: z(n+1) = z(n)**2 + c
    z = z**2 + c

# Visualisation
plt.imshow(np.abs(z), extent=[-xlim,xlim,-xlim,xlim], aspect='equal')
plt.title(c)
plt.show()
    
