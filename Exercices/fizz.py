#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2017-05-28 21:42 ycopin@lyonovae03.in2p3.fr>

"""
Jeu du Fizz Buzz
"""

__author__ = "Yannick Copin <y.copin@ipnl.in2p3.fr>"


for i in range(1, 100):                    # Entiers de 1 à 99
    if ((i % 3) == 0) and ((i % 5) == 0):  # Multiple de 3 et 5
        print 'Fizz Buzz!',                # Affichage sans retour à la ligne
    elif ((i % 3) == 0):                   # Multiple de 3 uniquement
        print 'Fizz!',
    elif ((i % 5) == 0):                   # Multiple de 5 uniquement
        print 'Buzz!',
    else:
        print i,
