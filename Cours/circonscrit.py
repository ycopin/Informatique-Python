#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Calcul du cercle circonscrit à 3 points du plan.
"""

__author__ = "Yannick Copin <y.copin@ipnl.in2p3.fr>"
__version__ = "Time-stamp: <2014-01-12 22:19 ycopin@lyonovae03.in2p3.fr>"

from math import sqrt, hypot

# Définition d'une classe ==============================

# start-classPoint
class Point(object): # *object* est la classe dont dérivent toutes les autres
    """Classe définissant un `Point` du plan, caractérisé par ses
    coordonnées `x`,`y`.
    """

    def __init__(self, x, y):
        """Méthode d'instanciation à partir de deux coordonnées."""

        try:                            # Convertit les coords en `float`
            self.x = float(x)
            self.y = float(y)
        except ValueError:
            raise ValueError("Coordonnées d'entrée invalides")

    def __str__(self):
        """Surcharge de la fonction `str()`: l'affichage *informel* de
        l'objet dans l'interpréteur, p.ex. `print self` sera résolu
        comme `self.__str__()`

        Retourne une chaîne de caractères.
        """

        return "Point (x=%f, y=%f)" % (self.x, self.y)

    def __nonzero__(self):
        """Surcharge de la fonction `bool()`: `bool(self)` retourne
        vrai si le point n'est pas à l'origine."""

        return ((self.x != 0) and (self.y != 0))

    def distance(self, other):
        """Méthode de calcul de la distance du point (`self`) à un
        autre (`other`)."""

        return hypot(self.x - other.x, self.y - other.y) # sqrt(dx**2 + dy**2)
# end-classPoint

# Définition du point origine O
O = Point(0,0)

# Héritage de classe ==============================

# start-classVector
class Vecteur(Point):
    """Un `Vecteur` hérite de `Point` avec des méthodes additionnelles
    (p.ex. l'addition)."""

    def __init__(self, A, B):
        """Définit le vecteur :math:`\vec{AB}` à partir des 2 points
        `A` et `B`."""

        # Initialisation de la classe parente
        Point.__init__(self, B.x-A.x, B.y-A.y)

        # Attribut propre à la classe dérivée
        self.norm2 = self.x**2 + self.y**2 # Norme du vecteur au carré

    def __str__(self):
        """Surcharge de la fonction `str()`: ainsi, `print self` sera
        résolu comme `Vecteur.__str__(self)` (et non pas comme
        `Point.__str__(self)`)
        """

        return "Vecteur (x=%f, y=%f)" % (self.x, self.y)

    def __add__(self, other):
        """Surcharge de l'opérateur `+`: l'instruction `self + other`
        sera résolue comme `self.__add__(other)`.

        On construit une nouvelle instance de `Vecteur` à partir des
        coordonnées propres à l'objet `self`, et à l'autre opérande
        `other`."""

        return Vecteur(O, Point(self.x + other.x, self.y + other.y))

    def __abs__(self):
        """Surcharge de la fonction `abs()`"""

        # Il vaudrait utiliser sqrt(self.norm2), mais c'est pour
        # l'exemple d'utilisation d'une méthode héritée...
        return Point.distance(self, O)
# end-classVector


def cercleCirconscrit(M,N,P):
    """Calcule le centre et le rayon du cercle circonscrit aux
    points M,N,P.

    Retourne: (centre [Point],rayon [float])"""

    MN = Vecteur(M,N)
    NP = Vecteur(N,P)
    PM = Vecteur(P,M)

    # Rayon
    m = abs(NP)                         # |NP|
    n = abs(PM)                         # |PM|
    p = abs(MN)                         # |MN|

    d = (m+n+p)*(-m+n+p)*(m-n+p)*(m+n-p)
    if d>0:
        rad = m*n*p / sqrt(d)
    else:
        raise ValueError("Rayon du cercle circonscrit indéfini.")

    # Centre
    d = -2*( M.x*NP.y + N.x*PM.y + P.x*MN.y )
    if d==0:
        raise ValueError("Centre du cercle circonscrit indéfini.")

    om2 = Vecteur(O,M).norm2             # |OM|**2
    on2 = Vecteur(O,N).norm2             # |ON|**2
    op2 = Vecteur(O,P).norm2             # |OP|**2

    x0 = -( om2*NP.y + on2*PM.y + op2*MN.y ) / d
    y0 =  ( om2*NP.x + on2*PM.x + op2*MN.x ) / d
    
    return (Point(x0,y0), rad)           # (Centre,R)


if __name__=='__main__':

    # start-optparse
    from optparse import OptionParser

    usage = "%prog [-p/--plot] [-i/--input coordfile | x1,y1 x2,y2 x3,y3]"
    description = u"Calcul du cercle circonscrit à 3 points du plan."

    parser = OptionParser(usage=usage, description=description,
                          version=__version__)
    parser.add_option("-i", "--input",
                      help=u"Fichier de coordonnées (un 'x,y' par ligne)")
    parser.add_option("-p", "--plot",
                      action="store_true", default=False,
                      help="Trace le cercle circonscrit")

    opts,args = parser.parse_args()
    # end-optparse

    if opts.input:                      # Lecture du fichier d'entrée
        try:
            args = file(opts.input).readlines()
        except IOError:
            parser.error("Impossible de lire le fichier '%s'" % opts.input)

    if len(args) != 3:                  # Vérifie le nb de points
        parser.error("Spécifier 3 points par leurs coordonnées 'x,y'")

    points = [None]*3                   # Génère la liste de 3 points
    for i,arg in enumerate(args):
        try:                            # Déchiffrage de l'argument 'x,y'
            x,y = ( float(t) for t in arg.split(',') )
        except ValueError:
            parser.error("Impossible de déchiffrer les coordonnées '%s'" % arg)

        points[i] = Point(x,y)          # Création du point
        print "#%d: %s" % (i+1,str(points[i]))

    # Calcul du cercle cisconscrit
    try:
        centre,rayon = cercleCirconscrit(*points) # Délistage
        print "Cercle circonscrit: %s, rayon=%f" % (str(centre),rayon)
    except ValueError:
        raise ValueError("Circle circonscrit indéfini")

    if opts.plot:                       # Figure
        import matplotlib.pyplot as P

        fig = P.figure()
        ax = fig.add_subplot(1,1,1, aspect='equal')
        # Points
        ax.plot([ p.x for p in points], [ p.y for p in points ], 'ko')
        for i,p in enumerate(points):
            ax.annotate("#%d" % (i+1), (p.x,p.y),
                        xytext=(5,5), textcoords='offset points')
        # Cercle circonscrit
        c = P.matplotlib.patches.Circle((centre.x,centre.y), radius=rayon,
                                        fc='none')
        ax.add_patch(c)
        ax.plot(centre.x,centre.y,'r+')

        P.show()
