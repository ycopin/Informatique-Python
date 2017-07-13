#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Calcule le cercle circonscrit à 3 points du plan.

Ce script sert d'illustration à plusieurs concepts indépendants:

- un exemple de script (shebang, docstring, etc.) permettant une
  utilisation en module (`import circonscrit`) et en exécutable
  (`python circonscrit.py -h`);
- des exemples de Programmation Orientée Objet: classe `Point` et la
  classe héritière `Vector`;
- un exemple d'utilisation du module `argparse` de la bibliothèque
  standard, permettant la gestion des arguments de la ligne de
  commande;
- l'utilisation de tests unitaires sous la forme de `doctest` (tests
  inclus dans les *docstrings* des éléments à tester).

  Pour exécuter les tests unitaires du module:

  - avec doctest: `python -m doctest -v circonscrit.py`
  - avec pytests: `py.test --doctest-modules -v circonscrit.py`
  - avec nose:    `nosetests --with-doctest -v circonscrit.py`
"""

__author__ = "Yannick Copin <y.copin@ipnl.in2p3.fr>"
__version__ = "Time-stamp: <2014-01-12 22:19 ycopin@lyonovae03.in2p3.fr>"

# Définition d'une classe ==============================


class Point(object):  # *object* est la classe dont dérivent toutes les autres

    """
    Classe définissant un `Point` du plan, caractérisé par ses
    coordonnées `x`,`y`.
    """

    def __init__(self, x, y):
        """
        Méthode d'instanciation à partir de deux coordonnées réelles.

        >>> Point(0,1)          # doctest: +ELLIPSIS
        <circonscrit.Point object at 0x...>
        >>> Point(1+3j)
        Traceback (most recent call last):
        ...
        TypeError: __init__() takes exactly 3 arguments (2 given)
        """

        try:  # Convertit les coords en `float`
            self.x = float(x)
            self.y = float(y)
        except (ValueError, TypeError):
            raise TypeError("Invalid input coordinates ({},{})".format(x, y))

    def __str__(self):
        """
        Surcharge de la fonction `str()`: l'affichage *informel* de l'objet
        dans l'interpréteur, p.ex. `print self` sera résolu comme
        `self.__str__()`

        Retourne une chaîne de caractères.

        >>> print Point(1,2)
        Point (x=1.0, y=2.0)
        """

        return "Point (x={p.x}, y={p.y})".format(p=self)

    def isOrigin(self):
        """
        Test si le point est à l'origine en testant la nullité des deux
        coordonnées.

        Attention aux éventuelles erreurs d'arrondis: il faut tester
        la nullité à la précision numérique près.

        >>> Point(1,2).isOrigin()
        False
        >>> Point(0,0).isOrigin()
        True
        """

        import sys

        eps = sys.float_info.epsilon  # Le plus petit float non nul

        return ((abs(self.x) <= eps) and (abs(self.y) <= eps))

    def distance(self, other):
        """
        Méthode de calcul de la distance du point (`self`) à un autre point
        (`other`).

        >>> A = Point(1,0); B = Point(1,1); A.distance(B)
        1.0
        """

        from math import hypot

        return hypot(self.x - other.x, self.y - other.y)  # sqrt(dx**2 + dy**2)


# Définition du point origine O
O = Point(0, 0)


# Héritage de classe ==============================


class Vector(Point):

    """
    Un `Vector` hérite de `Point` avec des méthodes additionnelles
    (p.ex. la négation d'un vecteur, l'addition de deux vecteurs, ou
    la rotation d'un vecteur).
    """

    def __init__(self, A, B):
        """
        Définit le vecteur `AB` à partir des deux points `A` et `B`.

        >>> Vector(Point(1,0), Point(1,1)) # doctest: +ELLIPSIS
        <circonscrit.Vector object at 0x...>
        >>> Vector(0, 1)
        Traceback (most recent call last):
        ...
        AttributeError: 'int' object has no attribute 'x'
        """

        # Initialisation de la classe parente
        Point.__init__(self, B.x - A.x, B.y - A.y)

        # Attribut propre à la classe dérivée
        self.sqnorm = self.x ** 2 + self.y ** 2  # Norme du vecteur au carré

    def __str__(self):
        """
        Surcharge de la fonction `str()`: `print self` sera résolu comme
        `Vector.__str__(self)` (et non pas comme
        `Point.__str__(self)`)

        >>> A = Point(1,0); B = Point(1,1); print Vector(A,B)
        Vector (x=0.0, y=1.0)
        """

        return "Vector (x={v.x}, y={v.y})".format(v=self)

    def __add__(self, other):
        """
        Surcharge de l'opérateur binaire `{self} + {other}`: l'instruction
        sera résolue comme `self.__add__(other)`.

        On construit une nouvelle instance de `Vector` à partir des
        coordonnées propres à l'objet `self` et à l'autre opérande
        `other`.

        >>> A = Point(1,0); B = Point(1,1)
        >>> print Vector(A,B) + Vector(B,O) # = Vector(A,O)
        Vector (x=-1.0, y=0.0)
        """

        return Vector(O, Point(self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        """
        Surcharge de l'opérateur binaire `{self} - {other}`: l'instruction
        sera résolue comme `self.__sub__(other)`.

        Attention: ne surcharge pas l'opérateur unaire `-{self}`, géré
        par `__neg__`.

        >>> A = Point(1,0); B = Point(1,1)
        >>> print Vector(A,B) - Vector(A,B) # Différence
        Vector (x=0.0, y=0.0)
        >>> -Vector(A,B)                    # Négation
        Traceback (most recent call last):
        ...
        TypeError: bad operand type for unary -: 'Vector'
        """

        return Vector(O, Point(self.x - other.x, self.y - other.y))

    def __eq__(self, other):
        """
        Surcharge du test d'égalité `{self}=={other}`: l'instruction sera
        résolue comme `self.__eq__(other)`.

        >>> Vector(O,Point(0,1)) == Vector(Point(1,0),Point(1,1))
        True
        """

        # On teste ici la nullité de la différence des 2
        # vecteurs. D'autres tests auraient été possibles -- égalité
        # des coordonnées, nullité de la norme de la différence,
        # etc. -- mais on tire profit de la méthode héritée
        # `Point.isOrigin()` testant la nullité des coordonnées (à la
        # précision numérique près).
        return (self - other).isOrigin()

    def __abs__(self):
        """
        Surcharge la fonction `abs()` pour retourner la norme du vecteur.

        >>> abs(Vector(Point(1,0), Point(1,1)))
        1.0
        """

        # On pourrait utiliser sqrt(self.sqnorm), mais c'est pour
        # illustrer l'utilisation de la méthode héritée
        # `Point.distance`...
        return Point.distance(self, O)

    def rotate(self, angle, deg=False):
        """
        Rotation (dans le sens trigonométrique) du vecteur par un `angle`,
        exprimé en radians ou en degrés.

        >>> Vector(Point(1,0),Point(1,1)).rotate(90,deg=True) == Vector(O,Point(-1,0))
        True
        """

        from cmath import rect  # Bibliothèque de fonctions complexes

        # On calcule la rotation en passant dans le plan complexe
        z = complex(self.x, self.y)
        phase = angle if not deg else angle / 57.29577951308232  # [rad]
        u = rect(1., phase)  # exp(i*phase)
        zu = z * u  # Rotation complexe

        return Vector(O, Point(zu.real, zu.imag))


def circumscribedCircle(M, N, P):
    """
    Calcule le centre et le rayon du cercle circonscrit aux points
    M,N,P.

    Retourne: (centre [Point],rayon [float])

    Lève une exception `ValueError` si le rayon ou le centre du cercle
    circonscrit n'est pas défini.

    >>> M = Point(-1,0); N = Point(1,0); P = Point(0,1)
    >>> C,r = circumscribedCircle(M,N,P) # Centre O, rayon 1
    >>> print C.distance(O), r
    0.0 1.0
    >>> circumscribedCircle(M,O,N)       # Indéfini
    Traceback (most recent call last):
    ...
    ValueError: Undefined circumscribed circle radius.
    """

    from math import sqrt

    MN = Vector(M, N)
    NP = Vector(N, P)
    PM = Vector(P, M)

    # Rayon du cercle circonscrit
    m = abs(NP)  # |NP|
    n = abs(PM)  # |PM|
    p = abs(MN)  # |MN|

    d = (m + n + p) * (-m + n + p) * (m - n + p) * (m + n - p)
    if d > 0:
        rad = m * n * p / sqrt(d)
    else:
        raise ValueError("Undefined circumscribed circle radius.")

    # Centre du cercle circonscrit
    d = -2 * (M.x * NP.y + N.x * PM.y + P.x * MN.y)
    if d == 0:
        raise ValueError("Undefined circumscribed circle center.")

    om2 = Vector(O, M).sqnorm  # |OM|**2
    on2 = Vector(O, N).sqnorm  # |ON|**2
    op2 = Vector(O, P).sqnorm  # |OP|**2

    x0 = -(om2 * NP.y + on2 * PM.y + op2 * MN.y) / d
    y0 = (om2 * NP.x + on2 * PM.x + op2 * MN.x) / d

    return (Point(x0, y0), rad)  # (centre [Point], R [float])


if __name__ == '__main__':

    # start-argparse
    import argparse

    parser = argparse.ArgumentParser(
        usage="%(prog)s [-p/--plot] [-i/--input coordfile | x1,y1 x2,y2 x3,y3]",
        description=__doc__)
    parser.add_argument('coords', nargs='*', type=str, metavar='x,y',
                        help="Coordinates of point")
    parser.add_argument('-i', '--input', nargs='?', type=file,
                        help="Coordinate file (one 'x,y' per line)")
    parser.add_argument('-p', '--plot', action="store_true", default=False,
                        help="Draw the circumscribed circle")
    parser.add_argument('--version', action='version', version=__version__)

    args = parser.parse_args()
    # end-argparse

    if args.input:  # Lecture des coordonnées du fichier d'entrée
        # Le fichier a déjà été ouvert en lecture par argparse (type=file)
        args.coords = [coords for coords in args.input
                       if not coords.strip().startswith('#')]

    if len(args.coords) != 3:  # Vérifie le nb de points
        parser.error("Specify 3 points by their coordinates 'x,y' (got {})"
                     .format(len(args.coords)))

    points = []  # Liste des points
    for i, arg in enumerate(args.coords, start=1):
        try:  # Déchiffrage de l'argument 'x,y'
            x, y = (float(t) for t in arg.split(','))
        except ValueError:
            parser.error(
                "Cannot decipher coordinates #{}: '{}'".format(i, arg))

        points.append(Point(x, y))  # Création du point et ajout à la liste
        print "#{:d}: {}".format(i, points[-1])  # Affichage du dernier point

    # Calcul du cercle cisconscrit (lève une ValueError en cas de problème)
    center, radius = circumscribedCircle(*points)  # Délistage
    print "Circumscribed circle: {}, radius: {}".format(center, radius)

    if args.plot:  # Figure
        import matplotlib.pyplot as P

        fig = P.figure()
        ax = fig.add_subplot(1, 1, 1, aspect='equal')
        # Points
        ax.plot([p.x for p in points], [p.y for p in points], 'ko')
        for i, p in enumerate(points, start=1):
            ax.annotate("#{}".format(i), (p.x, p.y),
                        xytext=(5, 5), textcoords='offset points')
        # Cercle circonscrit
        c = P.matplotlib.patches.Circle((center.x, center.y), radius=radius,
                                        fc='none', ec='k')
        ax.add_patch(c)
        ax.plot(center.x, center.y, 'r+')

        P.show()
