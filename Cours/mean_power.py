#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemple de script (shebang, docstring, etc.) permettant une
utilisation en module (`import mean_power`) et en exécutable (`python
mean_power.py -h`);
"""


def mean_power(alist, power=1):
    """
    Retourne la racine `power` de la moyenne des éléments de `alist` à
    la puissance `power`:

    .. math:: \mu = (\frac{1}{N}\sum_{i=0}^{N-1} x_i^p)^{1/p}

    `power=1` correspond à la moyenne arithmétique, `power=2` au *Root
    Mean Squared*, etc.

    Exemples:
    >>> mean_power([1,2,3])
    2.0
    >>> mean_power([1,2,3], power=2)
    2.160246899469287
    """

    s = 0.                  # Initialisation de la variable *s* comme *float*
    for val in alist:       # Boucle sur les éléments de *alist*
        s += val ** power     # *s* est augmenté de *val* puissance *power*
    s /= len(alist)         # = somme valeurs / nb valeurs
    # *mean* = (somme valeurs / nb valeurs)**(1/power)
    mean = s ** (1. / power)

    return mean


if __name__ == '__main__':

    # start-argparse
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('list', nargs='*', type=float, metavar='nombres',
                        help="Liste de nombres à moyenner")
    parser.add_argument('-i', '--input', nargs='?', type=file,
                        help="Fichier contenant les nombres à moyenner")
    parser.add_argument('-p', '--power', type=float, default=1.,
                        help="'Puissance' de la moyenne (%default)")

    args = parser.parse_args()
    # end-argparse

    if args.input:              # Lecture des coordonnées du fichier d'entrée
        # Le fichier a déjà été ouvert en lecture par argparse (type=file)
        try:
            args.list = [float(x) for x in args.input
                         if not x.strip().startswith('#')]
        except ValueError:
            parser.error(
                "Impossible de déchiffrer la ligne '{}' du fichier '{}'".format(
                    x, args.input))

    # Vérifie qu'il y a au moins un nombre dans la liste
    if not args.list:
        parser.error("La liste doit contenir au moins un nombre")

    # Calcul
    moyenne = mean_power(alist, args.power)

    # Affichage du résultat
    print "La moyenne des {} nombres à la puissance {} est {}".format(
        len(alist), args.power, moyenne)
