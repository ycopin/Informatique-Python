#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Mathieu Leocmach <mathieu.leocmach@ens-lyon.fr>"
__version__ = "Time-stamp: <2014-10-03 10:54 mathieu.leocmach@ens-lyon.fr>"

# Définition d'une classe ==============================

class Forme(object): # *object* est la classe dont dérivent toutes les autres
    """Une forme plane, avec éventuellement une couleur."""
    

    def __init__(self, couleur=None):
        """Initialisation d'une Forme, sans couleur par défaut."""
        if couleur is None:
            self.couleur = 'indefinie'
        else:
            self.couleur = couleur
            
    def __str__(self):
        """
        Surcharge de la fonction `str()`: l'affichage *informel* de
        l'objet dans l'interpréteur, p.ex. `print a` sera résolu
        comme `a.__str__()`

        Retourne une chaîne de caractères.
        """

        return "Forme indefinie de couleur {}".format(self.couleur)
        
    def set_couleur(self, newcolor):
        """
        Change la couleur de la Forme.
        """

        self.couleur = newcolor
        
    def aire(self):
        """Renvoi l'aire de la Forme
        Ne peut pas être calculé dans le cas où la forme n'est pas
        spécifiée: c'est ce que l'on appelle une méthode 'abstraite',
        qui pourra être précisée dans les classes filles.
        """
        raise NotImplementedError("Impossible de calculer l'aire d'une forme indefinie.")
        
    def __cmp__(self, other):
        """
        Comparaison de deux Formes sur la base de leur aire. 

        Surcharge des opérateurs de comparaison de type `{self} <
        {other}`: la comparaison sera résolue comme
        `self.__cmp__(other)` et le résultat sera correctement
        interprété.
        """

        return cmp(self.aire(), other.aire()) # Opérateur de comparaison



class Rectangle(Forme):
    """Un Rectangle est une forme particulière
    
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
    
    def __init__(self, longueur, largeur, couleur = None):
        #initialisation de la classe parent
        Forme.__init__(self, couleur)
        
        # Attributs propres
        self.longueur = longueur
        self.largeur = largeur
        
    def __str__(self):
        """Surcharge de `Forme.__str__()`."""

        return "Rectangle {}x{}, de couleur {}".format(
            self.longueur, self.largeur, self.couleur)

    def aire(self):
        """
        Renvoi l'aire du Rectangle.

        Cette méthode définit la méthode abstraite `Forme.area()`, pour les Rectangles uniquement.
        """
        return self.longueur * self.largeur
        
    def allonger(self, facteur):
        """Multiplie la *longueur* du Rectangle par un facteur"""
        self.longueur *= facteur
        
if __name__=='__main__':

    s = Forme()                      # Forme indéfinie et sans couleur
    print "s:", str(s)               # Interprété comme `s.__str__()`
    s.set_couleur('rouge')               # On change la couleur
    print "s apres set_couleur:", str(s)
    try:
        print "Aire de s:", s.aire() # La méthode abstraite lève une exception
    except NotImplementedError as err:
        print err

    q = Rectangle(1,4,'vert')       # Rectangle 1×4 vert
    print "q:", str(q)
    print "Aire de q:", q.aire()

    r = Rectangle(2,1,'bleu')        # Rectangle 2×1 bleu
    print "r:", str(r)
    print "Aire de r:", r.aire()

    print "q <= r:", (q <= r)        # Interprété comme q.__cmp__(r)

    r.allonger(2)                     # r devient un rectangle 4×1
    print "Aire de r apres l'avoir allonge d'un facteur 2:", r.aire()
    print "q <= r:", (q <= r)

    
