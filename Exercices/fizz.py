#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2018-07-26 16:46 ycopin@lyonovae03.in2p3.fr>

"""
Jeu du Fizz Buzz
"""

__author__ = "Yannick Copin <y.copin@ipnl.in2p3.fr>"


for i in range(1, 100):                    # Entiers de 1 à 99
    if ((i % 3) == 0) and ((i % 5) == 0):  # Multiple de 3 *et* de 5
        print('FIZZ BUZZ!', end=' ')       # Affichage sans retour à la ligne
    elif (i % 3) == 0:                     # Multiple de 3 uniquement
        print('Fizz!', end=' ')
    elif (i % 5) == 0:                     # Multiple de 5 uniquement
        print('Buzz!', end=' ')
    else:
        print(i, end=' ')
print()                                    # Retour à la ligne final
