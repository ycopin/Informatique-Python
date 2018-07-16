#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2018-07-16 18:07:22 ycopin>

"""
Calcul de l'intégrale de x**2 entre 0 et 1 par la méthode des rectangles
(subdivision en 100 pas)
"""

def sq(x):
    "Définition de la fonction sq: x → x**2."

    return x**2

a, b = 0, 1                     # Bornes d'intégration
n = 100                         # Nombre de pas

h = (b - a) / n                 # Largeur des rectangles

total = 0                       # Cette variable accumulera les aires des rectangles
for i in range(n):              # Boucle de 0 à n - 1
    x = a + (i + 0.5) * h       # Abscisse du rectangle
    total += sq(x) * h          # On ajoute l'aire du rectangle au total

print("Intégrale de x**2 entre a =", a, "et b =", b, "avec n =", n, "rectangles")
# On affiche les résultats numérique et analytique, ainsi que l'erreur relative
print("Résultat numérique: ", total)
theorie = (b ** 3 - a ** 3) / 3
print("Résultat analytique:", theorie)
print("Erreur relative:", (total / theorie - 1))
