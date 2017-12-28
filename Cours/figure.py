#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2017-12-28 09:11 ycopin@lyonovae03.in2p3.fr>

"""
Exemple un peu plus compexe de figure, incluant 2 axes, légendes, axes, etc.
"""

import numpy as N
import matplotlib.pyplot as P

x = N.linspace(-N.pi, 3*N.pi, 2*360)

# Signal carré
y = N.sign(N.sin(x))            # = ± 1

# 3 premiers termes de la décomposition en série de Fourier
y1 = 4/N.pi * N.sin(x)          # Fondamentale
y2 = 4/N.pi * N.sin(3*x) / 3    # 1ère harmonique
y3 = 4/N.pi * N.sin(5*x) / 5    # 2nde harmonique
# Somme des 3 premières composantes
ytot = y1 + y2 + y3

# Figure
fig = P.figure()                # Création de la Figure

# 1er axe: composantes
ax1 = fig.add_subplot(2, 1, 1,  # 1er axe d'une série de 2 × 1
                      ylabel="Composantes",
                      title="Décomposition en série de Fourier")
ax1.plot(x, y1, label="Fondamental")
ax1.plot(x, y2, label="1ère harmonique")
ax1.plot(x, y3, label="2nde harmonique")
ax1.legend(loc="upper left", fontsize="x-small")

# 2nd axe: décomposition
ax2 = fig.add_subplot(2, 1, 2,  # 2nd axe d'une série de 2 × 1
                      ylabel="Décomposition",
                      xlabel="x [rad]")
ax2.plot(x, y, lw=2, color='k', label="Signal carré")
ax2.plot(x, ytot, lw=2, ls=':', color='k', label="Somme des composantes")
ax2.legend(loc="upper left", fontsize="x-small")

# Sauvegarde de la figure (pas d'affichage intéractif)
fig.savefig("figure.png")
