#!/usr/bin/env python3
# coding: utf-8

# Time-stamp: <2020-11-16 21:52 ycopin@lyonovae03>

"""
Calcul du PGCD de deux entiers 0 < b < a.
"""

# Entiers dont on calcule le PGCD (avec 0 < b < a)
a = 756
b = 306

# Vérification des conditions d'application de l'algorithme: 0 < b < a
assert 0 < b < a, "Les conditions d'application ne sont pas vérifiées."

a0, b0 = a, b                     # On garde une copie des valeurs originales

# On boucle jusqu'à ce que le reste soit nul, d'où la boucle while. Il faut
# être sûr que l'algorithme converge dans tous les cas!
while True:
    r = a % b
    if r == 0:                  # Reste de la division euclidienne
        break                   # en sortie, PGCD = b
    else:
        a, b = b, r             # Itération

# On aurait pu écrire directement:
# while b != 0:
#     a, b = b, a % b             # en sortie, PGCD = a!

print('Le PGCD de', a0, 'et', b0, 'vaut', b)  # On affiche le résultat
# Vérifications
print(a0 // b, '×', b, '=', (a0 // b * b))  # a//b: division euclidienne
print(b0 // b, '×', b, '=', (b0 // b * b))
