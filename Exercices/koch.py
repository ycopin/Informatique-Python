#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division  # Pas de division euclidienne par défaut

"""
Tracé (via 'turtle') d'un flocon de Koch d'ordre arbitraire.

Dans le même genre:

- courbe de Peano (http://fr.wikipedia.org/wiki/Courbe_de_Peano)
- courbe de Hilbert (http://fr.wikipedia.org/wiki/Courbe_de_Hilbert)
- île de Gosper (http://fr.wikipedia.org/wiki/Île_de_Gosper)

Voir également:

- L-système: http://fr.wikipedia.org/wiki/L-système
- Autres exemples: http://natesoares.com/tutorials/python-fractals/
"""

__version__ = "Time-stamp: <2013-01-14 00:49 ycopin@lyopc469>"
__author__ = "Yannick Copin <y.copin@ipnl.in2p3.fr>"

import turtle as T


def koch(niveau=3, iter=0, taille=100, delta=0):
    """
    Tracé du flocon de Koch de niveau 'niveau', de taille 'taille'
    (px).

    Cette fonction récursive permet d'initialiser le flocon (iter=0,
    par défaut), de tracer les branches fractales (0<iter<=niveau) ou
    bien juste de tracer un segment (iter>niveau).
    """

    if iter == 0:                         # Dessine le triangle de niveau 0
        T.title("Flocon de Koch - niveau {}".format(niveau))
        koch(iter=1, niveau=niveau, taille=taille, delta=delta)
        T.right(120)
        koch(iter=1, niveau=niveau, taille=taille, delta=delta)
        T.right(120)
        koch(iter=1, niveau=niveau, taille=taille, delta=delta)
    elif iter <= niveau:                  # Trace une section _/\_ du flocon
        koch(iter=iter + 1, niveau=niveau, taille=taille, delta=delta)
        T.left(60 + delta)
        koch(iter=iter + 1, niveau=niveau, taille=taille, delta=delta)
        T.right(120 + 2 * delta)
        koch(iter=iter + 1, niveau=niveau, taille=taille, delta=delta)
        T.left(60 + delta)
        koch(iter=iter + 1, niveau=niveau, taille=taille, delta=delta)
    else:                               # Trace le segment de dernier niveau
        T.forward(taille / 3 ** (niveau + 1))

if __name__ == '__main__':

    # start-argparse
    # Exemple d'utilisation de la bibliothèque de gestion d'arguments 'argparse'
    import argparse

    desc = "Tracé (via 'turtle') d'un flocon de Koch d'ordre arbitraire."

    # Définition des options
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('ordre', nargs='?', type=int,
                        help="Ordre du flocon, >0 [%(default)s]",
                        default=3)
    parser.add_argument('-t', '--taille', type=int,
                        help="Taille de la figure, >0 [%(default)s px]",
                        default=500)
    parser.add_argument('-d', '--delta', type=float,
                        help="Delta [%(default)s deg]",
                        default=0.)
    parser.add_argument('-f', '--figure', type=str,
                        help="Nom de la figure de sortie (format EPS)")
    parser.add_argument('-T', '--turbo',
                        action="store_true", default=False,
                        help="Mode Turbo")

    # Déchiffrage des options et arguments
    args = parser.parse_args()

    # Quelques tests sur les args et options
    if not args.ordre > 0:
        parser.error("Ordre requis '{}' invalide".format(args.ordre))

    if not args.taille > 0:
        parser.error("La taille de la figure doit être positive")
    # end-argparse

    if args.turbo:
        T.hideturtle()
        T.speed(0)

    # Tracé du flocon de Koch de niveau 3
    koch(niveau=args.ordre, taille=args.taille, delta=args.delta)
    if args.figure:
        # Sauvegarde de l'image
        print("Sauvegarde de la figure dans '{}'".format(args.figure))
        T.getscreen().getcanvas().postscript(file=args.figure)

    T.exitonclick()
