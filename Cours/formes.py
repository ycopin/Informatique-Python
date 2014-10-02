#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Forme(object): # *object* est la classe dont dérivent toutes les autres
    """Une forme plane"""
    
    # initialisation d’un objet
    # définition des attributs avec des valeurs par défaut
    def __init__(self, couleur="blanc"):
        self.couleur = couleur
        
    def aire(self):
        """Renvoi l'aire de la Forme"""
        return 0
        
    def __lt__(self, other):
        """Surcharge l'opérateur '<' pour comparer deux Formes par leur aire"""
        return self.aire() < other.aire()


class Rectangle(Forme)
    """Un Rectangle est une forme particulière"""
    # initialisation d’un objet
    # définition des attributs avec des valeurs par défaut
    def __init__(self, longueur = 0.0, largeur = 0.0, couleur = "blanc"):
        #initialisation de la classe parent
        Forme.__init__(self, couleur)
        self.longueur = longueur
        self.largeur = largeur
        
    #redéfini la méthode aire, pour les Rectangles seulement
    def aire(self):
        """Renvoi l'aire de la Forme"""
        #cette fois-ci on a une formule
        return self.longueur * self.largeur
        
    #méthode qui n'existe que pour les Rectangles
    def allonger(self, facteur):
        """multiplie la longueur"""
        self.longueur *= facteur
        
    #pas besoin de redéfinir __lt__, le méchanisme général de Forme est très bien
        

