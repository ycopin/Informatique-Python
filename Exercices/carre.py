#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2013-11-05 16:56:47 ycopin>

"""
Création et affichage d'un carré magique d'ordre impair.
"""

__author__ = "Yannick Copin <y.copin@ipnl.in2p3.fr>"

n = 5                                   # Ordre du carré magique

# On vérifie que l'ordre est bien impair
assert n%2 == 1, "L'ordre %d n'est pas impair" % n

# Le carré sera stocké dans une liste de n listes de n entiers
# Initialisation du carré: liste de n listes de n zéros.
array = [ [ 0 for j in range(n) ] for i in range(n) ]

# Initialisation de l'algorithme
i,j = n,(n+1)/2           # Indices de l'algo (1-indexation)
array[i-1][j-1] = 1       # Attention: python utilise une 0-indexation
# Boucle sur valeurs restant à inclure dans le carré (de 2 à n**2)
for k in range(2,n**2+1): 
    # Test de la case i+1,j+1 (modulo n)
    i2 = (i+1) % n
    j2 = (j+1) % n
    if not array[i2-1][j2-1]: # La case est vide: l'utiliser
        i,j = i2,j2
    else:                     # La case est déjà remplie: utiliser la case i-1,j
        i = (i-1) % n
    array[i-1][j-1] = k       # Remplissage de la case

# Affichage, avec vérification des sommes par ligne et par colonne
print "Carré magique d'ordre %d:" % n
for row in array:
    print '  '.join( '%2d' % k for k in row ), '=', sum(row)
print '  '.join( '==' for k in row )
print '  '.join( str(sum( array[i][j] for i in range(n) )) for j in range(n) )
