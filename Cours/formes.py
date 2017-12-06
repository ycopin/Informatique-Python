#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exemple de Programmation Orientée Objet.
"""


# Définition d'une classe ==============================

class Forme(object):  # *object* est la classe dont dérivent toutes les autres

    """Une forme plane, avec éventuellement une couleur."""

    def __init__(self, couleur=None):
        """Initialisation d'une Forme, sans couleur par défaut."""

        if couleur is None:
            self.couleur = 'indéfinie'
        else:
            self.couleur = couleur

    def __str__(self):
        """
        Surcharge de la fonction `str()`: l'affichage *informel* de
        l'objet dans l'interpréteur, p.ex. `print(a)` sera résolu comme
        `a.__str__()`

        Retourne une chaîne de caractères.
        """

        return "Forme encore indéfinie de couleur {}".format(self.couleur)

    def change_couleur(self, newcolor):
        """Change la couleur de la Forme."""

        self.couleur = newcolor

    def aire(self):
        """
        Renvoie l'aire de la Forme.

        L'aire ne peut pas être calculée dans le cas où la forme n'est
        pas encore spécifiée: c'est ce que l'on appelle une méthode
        'abstraite', qui pourra être précisée dans les classes filles.
        """

        raise NotImplementedError(
            "Impossible de calculer l'aire d'une forme indéfinie.")


class Rectangle(Forme):

    """
    Un Rectangle est une Forme particulière.

    La classe-fille hérite des attributs et méthodes de la
    classe-mère, mais peut les surcharger (i.e. en changer la
    définition), ou en ajouter de nouveaux:

    - les méthodes `Rectangle.change_couleur()` et
      `Rectangle.__cmp__()` dérivent directement de
      `Forme.change_couleur()` et `Forme.__cmp__()`;
    - `Rectangle.__str__()` surcharge `Forme.__str__()`;
    - `Rectangle.aire()` définit la méthode jusqu'alors abstraite
      `Forme.aire()`;
    - `Rectangle.allonger()` est une nouvelle méthode propre à
      `Rectangle`.
    """

    def __init__(self, longueur, largeur, couleur=None):
        """
        Initialisation d'un Rectangle longueur × largeur, sans couleur par
        défaut.
        """

        # Initialisation de la classe parente (nécessaire pour assurer
        # l'héritage)
        Forme.__init__(self, couleur)

        # Attributs propres à la classe Rectangle
        self.longueur = longueur
        self.largeur = largeur

    def __str__(self):
        """Surcharge de `Forme.__str__()`."""

        return "Rectangle {}x{}, de couleur {}".format(
            self.longueur, self.largeur, self.couleur)

    def aire(self):
        """
        Renvoi l'aire du Rectangle.

        Cette méthode définit la méthode abstraite `Forme.area()`,
        pour les Rectangles uniquement.
        """

        return self.longueur * self.largeur

    def allonger(self, facteur):
        """Multiplie la *longueur* du Rectangle par un facteur"""

        self.longueur *= facteur


if __name__ == '__main__':

    s = Forme()                       # Forme indéfinie et sans couleur
    print("s:", str(s))               # Interprété comme `s.__str__()`
    s.change_couleur('rouge')         # On change la couleur
    print("s après change_couleur:", str(s))
    try:
        print("Aire de s:", s.aire())  # La méthode abstraite lève une exception
    except NotImplementedError as err:
        print(err)

    q = Rectangle(1, 4, 'vert')       # Rectangle 1×4 vert
    print("q:", str(q))
    print("Aire de q:", q.aire())

    r = Rectangle(2, 1, 'bleu')       # Rectangle 2×1 bleu
    print("r:", str(r))
    print("Aire de r:", r.aire())

    print("Allongement de r d'un facteur 2")
    r.allonger(2)                     # r devient un rectangle 4×1
    print("r:", str(r))
