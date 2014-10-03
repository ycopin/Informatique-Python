#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Exemple de script (shebang, docstring, etc.) permettant une
  utilisation en module (`import mean_power`) et en exécutable
  (`python mean_power.py -h`);"""


def mean_power(alist, power=1):
     """Retourne la racine `power` de la moyenne des éléments de
     `alist` à la puissance `power`: 
 
     .. math:: \mu = (\frac{1}{N}\sum_{i=0}^{N-1} x_i^p)^{1/p}
 
     `power=1` correspond à la moyenne arithmétique, `power=2` au
     *Root Mean Squared*, etc.
 
     Exemples:
     >>> mean_power([1,2,3])
     2.0
     >>> mean_power([1,2,3], power=2)
     2.160246899469287
     """
 
     s = 0.                  # Initialisation de la variable *s* comme *float*
     for val in alist:       # Boucle sur les éléments de *alist*
         s += val**power     # *s* est augmenté de *val* puissance *power*
     s /= len(alist)         # = somme valeurs / nb valeurs
     mean = s**(1./power)    # *mean* = (somme valeurs / nb valeurs)**(1/power)
 
     return mean
     
     
if __name__ == '__main__':
    # start-argparse
    import argparse

    #comme on n'utilise qu'une seule fonction, on se permet de reprendre la description 
    #de la fonction comme aide du script
    parser = argparse.ArgumentParser(description=mean_power.__doc__)
    parser.add_argument('list', nargs='*', type=float, help="liste de nombre")
    parser.add_argument('-i', '--input', nargs='?', type=file,
                        help="fichier contenant la liste (un nombre par ligne)")
    parser.add_argument('-p', '--power', type=float, default=1.0,
                        help="la puissance à laquelle élever les éléments de la liste")

    args = parser.parse_args()
    # end-argparse
    
    if args.input:              # Lecture des coordonnées du fichier d'entrée
        # Le fichier a déjà été ouvert en lecture par argparse (type=file)
        args.list = [ float(x) for x in args.input 
                        if not x.strip().startswith('#') ]
                        
    #verifie qu'il y a au moins un nombre
    if not args.list or len(args.list)==0:
        parser.error("La liste ou le fichier doit contenir au moins un nombre")
    
    #calcul
    reponse = mean_power(alist, args.power)
    
    #affiche le résultat
    print('La moyenne des {:d} nombres à la puissance {} est {}'.format(len(alist), args.power, reponse))
    
