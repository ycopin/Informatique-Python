#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2014-09-17 19:30:18 ycopin>

# Division réelle de type Python 3 - ligne admise
from __future__ import division

"""
Définition de la fonction carré et calcul de son intégrale entre 0
et 1 dans le main par la méthode des rectangles (subdivision en 100
pas)
"""

__author__ = "Adrien Licari <adrien.licari@ens-lyon.fr>"

# Définition de la fonction sq, admise au stade du TD 1


def sq(x):
    return x * x

# Début du programme principal (main)

# On définit les bornes d'intégration a et b, le nombre de pas n
a = 0
b = 1
n = 100

# Largeur des rectangles dx
h = (b - a) / n      # Division réelle!

integ = 0         # Cette variable accumulera les aires des rectangles

# On sait déjà que l'on va calculer n aires de rectangles, donc une
# boucle for est appropriée
for i in range(n):            # Boucle de 0 à n-1
    x = a + (i + 0.5) * h         # Abscisse du rectangle
    integ += sq(x) * h        # On ajoute au total l'aire du rectangle

print "Intégrale de x**2 entre a =", a, "et b =", b, "avec n =", n
# On affiche le résultat numérique
print "Résultat numérique: ", integ
theorie = (b ** 3 - a ** 3) / 3                     # Résultat analytique
# On affiche le résultat analytique
print "Résultat analytique:", theorie
print "Erreur relative:", (integ / theorie - 1)  # On affiche l'erreur
