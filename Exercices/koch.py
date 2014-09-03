#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division         # Pas de division euclidienne par défaut

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
    """Tracé du flocon de Koch de niveau 'niveau', de taille 'taille'
    (px).

    Cette fonction récursive permet d'initialiser le flocon (iter=0,
    par défaut), de tracer les branches fractales (0<iter<=niveau) ou
    bien juste de tracer un segment (iter>niveau).
    """

    if iter==0:                         # Dessine le triangle de niveau 0
        T.title("Flocon de Koch - niveau %d" % niveau)
        koch(iter=1, niveau=niveau, taille=taille, delta=delta)
        T.right(120)
        koch(iter=1, niveau=niveau, taille=taille, delta=delta)
        T.right(120)
        koch(iter=1, niveau=niveau, taille=taille, delta=delta)
    elif iter<=niveau:                  # Trace une section _/\_ du flocon
        koch(iter=iter+1, niveau=niveau, taille=taille, delta=delta)
        T.left(60 + delta)
        koch(iter=iter+1, niveau=niveau, taille=taille, delta=delta)
        T.right(120 + 2*delta)
        koch(iter=iter+1, niveau=niveau, taille=taille, delta=delta)
        T.left(60 + delta)
        koch(iter=iter+1, niveau=niveau, taille=taille, delta=delta)
    else:                               # Trace le segment de dernier niveau
        T.forward(taille/3**(niveau+1))

if __name__=='__main__':

    # start-optparse
    # Exemple d'utilisation de la librairie de gestion d'arguments 'optparse'
    from optparse import OptionParser

    desc = u"Tracé (via 'turtle') d'un flocon de Koch d'ordre arbitraire."

    # Définition des options
    parser = OptionParser(usage="%prog [options] ordre",
                          version=__version__, description=desc)
    parser.add_option("-t", "--taille", type=int, 
                      help="Taille [%default px]",
                      default=500)
    parser.add_option("-d", "--delta", type=float, 
                      help="Delta [%default deg]",
                      default=0.)
    parser.add_option("-f", "--figure",
                      help="Figure de sortie (format EPS)")
    parser.add_option("-T", "--turbo", 
                      action="store_true", default=False,
                      help="Mode Turbo")

    # Déchiffrage des options et arguments
    opts,args = parser.parse_args()

    # Quelques tests sur les args et options
    try:
        niveau = int(args[0])
        assert niveau >= 0
    except (IndexError,                 # Pas d'argument
            ValueError,                 # Argument non-entier
            AssertionError):            # Argument entier < 0
        parser.error("Niveau d'entrée %s invalide" % args)

    if opts.taille < 0:
        parser.error("La taille de la figure doit être positive")
    # end-optparse

    if opts.turbo:
        T.hideturtle()
        T.speed(0)

    # Tracé du flocon de Koch de niveau 3
    koch(niveau=niveau, taille=opts.taille, delta=opts.delta)
    if opts.figure:
        # Sauvegarde de l'image
        print "Sauvegarde de la figure dans '%s'" % opts.figure
        T.getscreen().getcanvas().postscript(file=opts.figure)
        
    T.exitonclick()
