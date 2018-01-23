#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2018-01-23 12:15:37 ycopin>

"""
Calcul de π par l'algorithme de Gauss-Legendre.

Essayer:

* eps = 1e-16
* p = 1.

Réf: https://en.wikipedia.org/wiki/Gauss–Legendre_algorithm
"""

from __future__ import division, print_function

from math import pi as PI       # Valeur vraie

__author__ = "Yannick Copin <y.copin@ipnl.in2p3.fr>"

eps = 1e-15        # Critère de précision (essayer aussi avec 1e-16)

print("Algorithme de Gauss-Legendre, eps={:g}".format(eps))

# Initialisation
a = 1            # Élement a_0
b = 2**(-0.5)
t = 1 / 4        # Division réelle grace au "from __future__ ..."
p = 1            # Essayer aussi 1.0

niter = 0                       # Compteur d'itération

while abs(a - b) >= eps:        # Boucle sans filet!

    pi = (a + b)**2 / (4 * t)   # Estimation courante de pi
    er = pi / PI - 1            # Erreur relative (fraction)

    print("Iter #{:d} (|diff|={:7.2g}): pi={:.15f} (er={:+8.2g})"
          .format(niter, abs(a - b), pi, er))

    # Prépare la prochaine itération
    anext = (a + b) / 2         # a_{n+1} = fonction(a_n, b_n)
    bnext = (a * b)**(0.5)
    tnext = t - p * (a - anext)**2
    pnext = 2 * p

    a = anext                   # a_n → a_{n+1}
    b = bnext
    t = tnext
    p = pnext

    niter += 1

print("Valeur vraie:             pi={:.15f}".format(PI))
