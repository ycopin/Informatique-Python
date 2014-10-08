#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2014-10-02 16:27:23 ycopin>

"""
Exemple de POO.
"""

__author__ = "Yannick Copin <y.copin@ipnl.in2p3.fr>"
__version__ = "Time-stamp: <2014-01-12 22:19 ycopin@lyonovae03.in2p3.fr>"


class Shape(object): # *object* est la classe dont dérivent toutes les autres
    """Une forme plane, avec éventuellement une couleur."""
    
    def __init__(self, color=None):
        """Initialisation d'une Shape, sans couleur par défaut."""

        if color is None:
            self.color = 'undefined'
        else:
            self.color = color

    def __str__(self):
        """
        Surcharge de la fonction `str()`: l'affichage *informel* de
        l'objet dans l'interpréteur, p.ex. `print self` sera résolu
        comme `self.__str__()`

        Retourne une chaîne de caractères.
        """

        return "Undefined shape, with {} color".format(self.color)

    def set_color(self, newcolor):
        """
        Change la couleur de la Shape.
        """

        self.color = newcolor

    def area(self):
        """
        Renvoi l'aire de la Shape.

        Ne peut pas être calculé dans le cas où la forme n'est pas
        spécifiée: c'est ce que l'on appelle une méthode 'abstraite',
        qui pourra être précisée dans les classes filles.
        """
        
        raise NotImplementedError("Undefined shape has no area.")
        
    def __cmp__(self, other):
        """
        Comparaison de deux Shapes sur la base de leur aire. 

        Surcharge des opérateurs de comparaison de type `{self} <
        {other}`: la comparaison sera résolue comme
        `self.__cmp__(other)` et le résultat sera correctement
        interprété.
        """

        return cmp(self.area(),other.area()) # Opérateur de comparaison


class Rectangle(Shape):
    """
    Un Rectangle est une Shape particulière.

    La classe-fille hérite des attributs et méthodes de la
    classe-mère, mais peut les surcharger (i.e. en changer la
    définition), ou en ajouter de nouveaux:
    
    - les méthodes `Rectangle.set_color()` et `Rectangle.__cmp__()`
      dérivent directement de `Shape.set_color()` et
      `Shape.__cmp__()`;
    - `Rectangle.__str__()` surcharge `Shape.__str__()`;
    - `Rectangle.area()` définit la méthode jusqu'alors abstraite
      `Shape.area()`;
    - `Rectangle.stretch()` est une nouvelle méthode propre à `Rectangle`.
    """

    def __init__(self, length, width, color=None):

        # Initialisation de la classe parente
        Shape.__init__(self, color)

        # Attributs propres
        self.length = length
        self.width = width
        
    def __str__(self):
        """Surcharge de `Shape.__str__()`."""

        return "Rectangle {}x{}, with {} color".format(
            self.length, self.width, self.color)

    def area(self):
        """
        Renvoi l'aire du Rectangle.

        Cette méthode définit la méthode abstraite `Shape.area()`.
        """

        return self.length * self.width
        
    def stretch(self, s):
        """Multiplie la *longueur* du Rectangle par un facteur `s`."""

        self.length *= s
        
if __name__=='__main__':

    s = Shape()                      # Forme indéfinie et sans couleur
    print "s:", str(s)               # Interprété comme `s.__str__()`
    s.set_color('red')               # On change la couleur
    print "s after set_color:", str(s)
    try:
        print "Area of s:", s.area() # La méthode abstraite lève une exception
    except NotImplementedError as err:
        print err

    q = Rectangle(1,4,'green')       # Rectangle 1×4 vert
    print "q:", str(q)
    print "Area of q:", q.area()

    r = Rectangle(2,1,'blue')        # Rectangle 2×1 bleu
    print "r:", str(r)
    print "Area of r:", r.area()

    print "q <= r:", (q <= r)        # Interprété comme q.__cmp__(r)

    r.stretch(2)                     # r devient un rectangle 4×1
    print "Area of r after stretch x2:", r.area()
    print "q <= r:", (q <= r)

