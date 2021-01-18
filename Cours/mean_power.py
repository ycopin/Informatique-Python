#!/usr/bin/env python3
# coding: utf-8

"""
Exemple de script (shebang, docstring, etc.) permettant une
utilisation en module (`import mean_power`) et en exécutable (`python
mean_power.py -h`);
"""


def mean_power(alist, power=1):
    r"""
    Retourne la racine `power` de la moyenne des éléments de `alist` à
    la puissance `power`:

    .. math:: \mu = (\frac{1}{N}\sum_{i=0}^{N-1} x_i^p)^{1/p}

    `power=1` correspond à la moyenne arithmétique, `power=2` au *Root
    Mean Squared*, etc.

    Exemples:
    >>> mean_power([1, 2, 3])
    2.0
    >>> mean_power([1, 2, 3], power=2)
    2.160246899469287
    """

    # *mean* = (somme valeurs**power / nb valeurs)**(1/power)
    mean = (sum( val ** power for val in alist ) / len(alist)) ** (1 / power)

    return mean


if __name__ == '__main__':

    # start-argparse
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('list', nargs='*', type=float, metavar='nombres',
                        help="Liste de nombres à moyenner")
    parser.add_argument('-i', '--input', nargs='?', type=argparse.FileType('r'),
                        help="Fichier contenant les nombres à moyenner")
    parser.add_argument('-p', '--power', type=float, default=1.,
                        help="'Puissance' de la moyenne (par défaut: %(default)s)")

    args = parser.parse_args()
    # end-argparse

    if args.input:       # Lecture des coordonnées du fichier d'entrée
        # Le fichier a déjà été ouvert en lecture par argparse (type=file)
        try:
            args.list = [float(x) for x in args.input
                         if not x.strip().startswith('#')]
        except ValueError:
            parser.error("Impossible de déchiffrer la ligne "
                         f"{x!r} du fichier {args.input!r}")

    # Vérifie qu'il y a au moins un nombre dans la liste
    if not args.list:
        parser.error("La liste doit contenir au moins un nombre")

    # Calcul
    moyenne = mean_power(args.list, args.power)

    # Affichage du résultat
    print("La moyenne puissance 1/{0} des {1} nombres à la puissance {0}"
          " est {2}.".format(args.power, len(args.list), moyenne))
