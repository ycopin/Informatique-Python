#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Yannick Copin <y.copin@ipnl.in2p3.fr>"
__version__ = "Time-stamp: <2014-01-08 22:01:24 ycopin>"

"""
Calcul du cercle circonscrit à 3 points du plan.
"""

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
            raise ValueError("Incompatible input coordinates")

    def __str__(self):
        """Surcharge de l'opérateur `str`: l'affichage *informel* de
        l'objet dans l'interpréteur, p.ex. `print self` sera résolu
        comme `self.__str__()`

        Retourne une chaîne de caractères.
        """

        return "Point (x=%f, y=%f)" % (self.x, self.y)

    def isOrigin(self):
        """Méthode booléenne, vrai si le point est à l'origine."""

        return ((self.x == 0) and (self.y == 0))

    def distance(self, other):
        """Méthode de calcul de la distance du point (`self`) à un
        autre (`other`)."""

        return hypot(self.x - other.x, self.y - other.y) # sqrt(dx² + dy²)
# end-classPoint

# Définition du point origine O
O = Point(0,0)

# Héritage de classe ==============================

# start-classVector
class Vector(Point):
    """Un `Vector` hérite de `Point` avec des méthodes additionnelles
    (p.ex. l'addition)."""

    def __init__(self, A, B=O):
        """Définit le vecteur :math:`\vec{AB}` si B!=O, ou
        :math:`\vec{OA}` sinon."""

        # Initialisation de la classe parente
        if B.isOrigin():                # B = O
            Point.__init__(self, A.x, A.y)
        else:                           # B != O
            Point.__init__(self, B.x-A.x, B.y-A.y)
            
        # Attribut propre à la classe dérivée
        self.norm2 = self.x**2 + self.y**2 # Norme du vecteur au carré

    def __str__(self):
        """Surcharge de la fonction `str()`: ainsi, `print self` sera
        résolu comme `Vector.__str__(self)` (et non pas comme
        `Point.__str__(self)`)
        """

        return "Vector (x=%f, y=%f)" % (self.x, self.y)

    def __add__(self, other):
        """Surcharge de l'opérateur `+`: l'instruction `self + other`
        sera résolue comme `self.__add__(other)`.

        On construit une nouvelle instance de `Vector` à partir des
        coordonnées propres à l'objet `self`, et à l'autre opérande
        `other`."""

        return Vector((self.x + other.x, self.y + other.y))

    isNull = Point.isOrigin       # Vector.isNull() = Point.isOrigin()

    def __abs__(self):
        """Surcharge de la fonction `abs()`"""

        # Il vaudrait mieux sqrt(self.norm2), mais c'est pour
        # l'exemple d'utilisation d'une méthode héritée...
        return Point.distance(self, O)
# end-classVector


def circumCircle(M,N,P):
    """Calcule le centre et le rayon du cercle circonscrit aux
    points M,N,P.

    Retourne: centre (Point),rayon (float)"""

    MN = Vector(M,N)
    NP = Vector(N,P)
    PM = Vector(P,M)
    
    # Diamètre
    m = abs(NP)                         # |NP|
    n = abs(PM)                         # |PM|
    p = abs(MN)                         # |MN|

    d = (m+n+p)*(-m+n+p)*(m-n+p)*(m+n-p)
    if d>0: 
        diam = 2*m*n*p / sqrt(d)
    else:
        raise ValueError("Undefined circumscribed circle diameter.")

    # Centre
    d = -2*( M.x*NP.y + N.x*PM.y + P.x*MN.y )
    if d==0:
        raise ValueError("Undefined circumscribed circle center.")
    
    om2 = Vector(O,M).norm2             # |OM|²
    on2 = Vector(O,N).norm2             # |ON|²
    op2 = Vector(O,P).norm2             # |OP|²

    x0 = -( om2*NP.y + on2*PM.y + op2*MN.y ) / d
    y0 =  ( om2*NP.x + on2*PM.x + op2*MN.x ) / d

    return Point(x0,y0),diam/2.         # Centre,R


if __name__=='__main__':

    # start-optparse
    from optparse import OptionParser

    description = "Calcul du cercle circonscrit à 3 points du plan."

    parser = OptionParser(usage="%prog [-p/--plot] "
                          "[-i/--input coordfile | x1,y1 x2,y2 x3,y3]",
                          version=__version__, description=description)
    parser.add_option("-i", "--input",
                      help="Input coordinate file (one 'x,y' per line)")
    parser.add_option("-p", "--plot",
                      action="store_true", default=False,
                      help="Plot circumscribed circle")

    opts,args = parser.parse_args()
    # end-optparse

    if opts.input:                      # Lecture du fichier d'entrée
        try:
            args = file(opts.input).readlines()
        except IOError:
            parser.error("Cannot read coordinates from %s" % opts.input)
            
    if len(args) != 3:                  # Vérifie le nb de points
        parser.error("Specify 3 input points by their 'x,y' coordinates")

    points = [None]*3                   # Génère la liste de 3 points
    for i,arg in enumerate(args):
        try:                            # Déchiffrage de l'argument 'x,y'
            x,y = ( float(t) for t in arg.split(',') )
        except ValueError:
            parser.error("Cannot parse x,y coordinates '%s'" % arg)

        points[i] = Point(x,y)          # Création du point
        print "#%d: %s" % (i+1,str(points[i]))

    # Calcul du cercle cisconscrit
    try:
        center,radius = circumCircle(*points) # Délistage
        print "Circumscribed circle: %s, radius=%f" % (str(center),radius)
    except ValueError:
        raise ValueError("Undefined circumscribed circle")

    if opts.plot:
        # Figure
        import matplotlib.pyplot as P
        
        fig = P.figure()
        ax = fig.add_subplot(1,1,1, aspect='equal', adjustable='datalim')
        # Point
        ax.plot([ p.x for p in points], [ p.y for p in points ], 'ko')
        # Cercle circonscrit
        c = P.matplotlib.patches.Circle((center.x,center.y), radius=radius,
                                        fc='none')
        ax.add_patch(c)
        ax.plot(center.x,center.y,'r+')
        
        P.show()
