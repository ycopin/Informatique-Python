#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2014-09-24 16:55:12 ycopin>

"""
Crible d'Ératosthène.

Source: http://fr.wikibooks.org/wiki/Exemples_de_scripts_Python#Implémentation_du_crible_d'Ératosthène
"""

__author__ = "Yannick Copin <y.copin@ipnl.in2p3.fr>"

# start-sys
# Gestion simplifiée d'un argument entier sur la ligne de commande
import sys

if sys.argv[1:]:  # Présence d'au moins un argument sur la ligne de commande
    try:
        n = int(sys.argv[1])  # Essayer de lire le 1er argument comme un entier
    except ValueError:
        raise ValueError("L'argument '{}}' n'est pas un entier"
                         .format(sys.argv[1]))
else:                        # Pas d'argument sur la ligne de commande
    n = 101                  # Valeur par défaut
# end-sys

# Liste des entiers *potentiellement* premiers. Les nb non-premiers
# seront étiquetés par 0 au fur et à mesure.
l = range(n + 1)                          # <0,...,n>, 0 n'est pas premier
l[1] = 0                                # 1 n'est pas premier

i = 2                                   # Entier à tester
while i ** 2 <= n:                        # Inutile de tester jusqu'à n
    if l[i] != 0:                       # Si i n'est pas étiqueté (=0)...
        # ...étiqueter tous les multiples de i
        l[2 * i::i] = [0] * len(l[2 * i::i])
    i += 1                              # Passer à l'entier à tester suivant

# Afficher la liste des entiers premiers (c-à-d non-étiquetés)
print "Liste des entiers premiers <=", n
print [i for i in l if i != 0]
