#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compute the circumscribed circle to 3 points in the plan.
"""

__author__ = "Yannick Copin <y.copin@ipnl.in2p3.fr>"
__version__ = "Time-stamp: <2014-01-12 22:19 ycopin@lyonovae03.in2p3.fr>"

# Définition d'une classe ==============================

# start-classPoint
class Point(object): # *object* est la classe dont dérivent toutes les autres
    """
    Classe définissant un `Point` du plan, caractérisé par ses
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
        """
        Surcharge de la fonction `str()`: l'affichage *informel* de l'objet
        dans l'interpréteur, p.ex. `print self` sera résolu comme
        `self.__str__()`

        Retourne une chaîne de caractères.
        """

        return "Point (x={p.x}, y={p.y})".format(p=self)

    def __nonzero__(self):
        """
        Surcharge de la fonction `bool()`: `bool(self)` retourne vrai si le
        point n'est pas à l'origine.
        """

        return ((self.x != 0) and (self.y != 0))

    def distance(self, other):
        """
        Méthode de calcul de la distance du point (`self`) à un autre point
        (`other`).
        """

        from math import hypot

        return hypot(self.x - other.x, self.y - other.y) # sqrt(dx**2 + dy**2)
# end-classPoint


# Définition du point origine O
O = Point(0,0)


# Héritage de classe ==============================

# start-classVector
class Vector(Point):
    """
    Un `Vector` hérite de `Point` avec des méthodes additionnelles
    (p.ex. l'addition de deux vecteurs, ou la rotation d'un vecteur).
    """

    def __init__(self, A, B):
        """
        Définit le vecteur :math:`\vec{AB}` à partir des 2 points `A` et
        `B`.
        """

        # Initialisation de la classe parente
        Point.__init__(self, B.x-A.x, B.y-A.y)

        # Attribut propre à la classe dérivée
        self.sqnorm = self.x**2 + self.y**2 # Norme du vecteur au carré

    def __str__(self):
        """
        Surcharge de la fonction `str()`: ainsi, `print self` sera résolu
        comme `Vector.__str__(self)` (et non pas comme
        `Point.__str__(self)`)
        """

        return "Vector (x={v.x}, y={v.y})".format(v=self)

    def __add__(self, other):
        """
        Surcharge de l'opérateur `+`: l'instruction `self + other` sera
        résolue comme `self.__add__(other)`.

        On construit une nouvelle instance de `Vector` à partir des
        coordonnées propres à l'objet `self`, et à l'autre opérande
        `other`.
        """

        return Vector(O, Point(self.x + other.x, self.y + other.y))

    def __abs__(self):
        """Surcharge de la fonction `abs()`"""

        # Il vaudrait utiliser sqrt(self.sqnorm), mais c'est pour
        # l'exemple d'utilisation d'une méthode héritée...
        return Point.distance(self, O)

    def rotate(self, angle, deg=False):
        """
        Rotation du vecteur par un `angle`, exprimé en radians ou en
        degrés.
        """

        from cmath import rect # Bibliothèque de fonctions complexes

        # On calcule la rotation en passant dans le plan complexe
        z = complex(self.x, self.y)
        phase = angle if not deg else angle/57.29577951308232 # [rad]
        u = cmath.rect(1., phase)                             # exp(i*phase)
        zu = z*u                # Rotation complexe

        return Vector(O, Point(zu.real, zu.imag))
# end-classVector


def circumscribedCircle(M,N,P):
    """
    Calcule le centre et le rayon du cercle circonscrit aux points
    M,N,P.

    Retourne: (centre [Point],rayon [float])

    Lève une exception `ValueError` si le rayon ou le centre du cercle
    circonscrit n'est pas défini.
    """

    from math import sqrt

    MN = Vector(M,N)
    NP = Vector(N,P)
    PM = Vector(P,M)

    # Rayon du cercle circonscrit
    m = abs(NP)                         # |NP|
    n = abs(PM)                         # |PM|
    p = abs(MN)                         # |MN|

    d = (m+n+p)*(-m+n+p)*(m-n+p)*(m+n-p)
    if d>0:
        rad = m*n*p / sqrt(d)
    else:
        raise ValueError("Undefined circumscribed circle radius.")

    # Centre du cercle circonscrit
    d = -2*( M.x*NP.y + N.x*PM.y + P.x*MN.y )
    if d==0:
        raise ValueError("Undefined circumscribed circle center.")

    om2 = Vector(O,M).sqnorm            # |OM|**2
    on2 = Vector(O,N).sqnorm            # |ON|**2
    op2 = Vector(O,P).sqnorm            # |OP|**2

    x0 = -( om2*NP.y + on2*PM.y + op2*MN.y ) / d
    y0 =  ( om2*NP.x + on2*PM.x + op2*MN.x ) / d
    
    return (Point(x0,y0), rad)           # (centre [Point], R [float])


if __name__=='__main__':

    # start-argparse
    import argparse

    parser = argparse.ArgumentParser(
        usage="%(prog)s [-p/--plot] [-i/--input coordfile | x1,y1 x2,y2 x3,y3]",
        description=__doc__)
    parser.add_argument('coords', nargs='*', type=str, metavar='x,y',
                        help="Coordinates of point")
    parser.add_argument('-i', '--input', nargs='?', type=file,
                        help="Coordinate file (one 'x,y' per line)")
    parser.add_argument('-p', '--plot',
                        action="store_true", default=False,
                        help="Draw the circumscribed circle")
    parser.add_argument('--version', action='version', version=__version__)

    args = parser.parse_args()
    # end-argparse

    if args.input:              # Lecture des coordonnées du fichier d'entrée
        # Le fichier a déjà été ouvert en lecture par argparse (type=file)
        args.coords = [ coords for coords in args.input 
                        if not coords.strip().startswith('#') ]

    if len(args.coords) != 3:   # Vérifie le nb de points
        parser.error("Specify 3 points by their coordinates 'x,y' (got {})"
                     .format(len(args.coords)))

    points = [None]*3                   # Génère la liste de 3 points
    for i,arg in enumerate(args.coords):
        try:                            # Déchiffrage de l'argument 'x,y'
            x,y = ( float(t) for t in arg.split(',') )
        except ValueError:
            parser.error("Cannot decipher coordinates #{}: '{}'"
                         .format(i+1, arg))

        points[i] = Point(x,y)          # Création du point
        print "#{:d}: {}".format(i+1,str(points[i]))

    # Calcul du cercle cisconscrit (lève une ValueError en cas de problème)
    center,radius = circumscribedCircle(*points) # Délistage
    print "Circumscribed circle: {}, radius: {}".format(center,radius)

    if args.plot:                       # Figure
        import matplotlib.pyplot as P

        fig = P.figure()
        ax = fig.add_subplot(1,1,1, aspect='equal')
        # Points
        ax.plot([ p.x for p in points ], [ p.y for p in points ], 'ko')
        for i,p in enumerate(points):
            ax.annotate("#{}".format(i+1), (p.x,p.y),
                        xytext=(5,5), textcoords='offset points')
        # Cercle circonscrit
        c = P.matplotlib.patches.Circle((center.x,center.y), radius=radius,
                                        fc='none')
        ax.add_patch(c)
        ax.plot(center.x, center.y, 'r+')

        P.show()
