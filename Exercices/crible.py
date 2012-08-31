#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-08-31 19:00:41 ycopin>

"""
Crible d'Ératosthène.

Source: http://fr.wikibooks.org/wiki/Exemples_de_scripts_Python#Impl.C3.A9mentation_du_crible_d.27.C3.89ratosth.C3.A8ne
"""

# Gestion simplifiée d'un argument sur la ligne de commande
# start-sys
import sys

if sys.argv[1:]: # Présence d'au moins un argument sur la ligne de commande
    try:
        n = int(sys.argv[1]) # Essayer de lire le 1er argument comme un entier
    except ValueError:
        raise ValueError("L'argument '%s' n'est pas un entier" % sys.argv[1])
else:                        # Pas d'argument sur la ligne de commande
    n = 101                  # Valeur par défaut
# end-sys

# Liste des entiers *potentiellement* premiers. Les nb non-premiers
# seront remplacés par 'None'.
l = range(n+1)                          # <0,...,n>
l[0],l[1] = None,None                   # 0 et 1 ne sont pas premiers

i = 2                                   # Entier à tester
while i**2 <= n:                        # Inutile de tester jusqu'à n
    l[2*i::i] = [None]*len(l[2*i::i])   # Étiqueter tous les multiples de i
    i += 1                              # Passer à l'entier test suivant

# Afficher la liste des entiers premiers (non-étiquetés)
print "Liste des entiers premiers <=", n
print [ i for i in l if i is not None ]
