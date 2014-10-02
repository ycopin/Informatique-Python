#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pytest

class Animal(object): # *object* est la classe dont dérivent toutes les autres
    """Classe définissant un `Animal`, caractérisé par son nom et son poids.
    """

    def __init__(self, nom, masse):
        """Méthode d'instanciation à partir d'un nom et d'un poids."""
        # Ici, convertir les paramètres pour être sûr qu'il ont le bon type, on utilisera str et float
        self.nom = nom
        self.masse = masse
        # On peut aussi faire des choses qui n'ont rien à voir avec les paramètres
        self.vivant = True
        self.empoisonne = False

    def __str__(self):
        """Surcharge de l'opérateur `str`: l'affichage *informel* de
        l'objet dans l'interpréteur, p.ex. `print self` sera résolu
        comme `self.__str__()`

        Retourne une chaîne de caractères.
        """

        return "{0}".format(self.nom)

    def estVivant(self):
        """Méthode booléenne, vrai si l'animal est vivant."""
        return False
        
    def mourir(self):
        #change l'état interne de l'objet
        #pas besoin de retourner quoi que ce soit
        pass

    def __lt__(self, other):
        """Surcharge de l'opérateur '<', vrai si l'animal (`self`) est plus leger qu'un autre (`other`). L'instruction `self < other` sera résolue comme `self.__lt__(other)."""
        return False
            
    def __call__(self, other):
        """Surcharge de l'opérateur '()' qui consite à manger un autre animal et augmenter son poids. L'instruction `self(other)` sera résolue comme `self.__call__(other)."""
        #l'autre animal meurt (s'il était encore vivant)
        #self prend du poids, mais pas plus que la masse de other ou 10% de son propre poids
        pass
        
        
 
class Chien(Animal):
    """Un `Chien` hérite de `Animal` avec des méthodes additionnelles
    (p.ex. l'aboyement et l'odorat)."""

    def __init__(self, nom, masse=20, odorat=0.5):
        """Définit un chien plus ou moins fin limier."""

        # Initialisation de la classe parente
        Animal.__init__(self, nom, masse)
            
        # Attribut propre à la classe dérivée
        self.odorat = float(odorat)

    def aboyer(self):
        """Une méthode bien spécifique aux chiens"""
        print("Ouaf ! Ouaf !")
        
    def estVivant(self):
        """Quand on vérifie qu'un chien est vivant, il aboie"""
        if self.vivant: self.aboyer()
        return Animal.estVivant(self)
        
        
def test_empty_init():
    with pytest.raises(TypeError):
        bidule = Animal()

def test_wrong_init():
    with pytest.raises(ValueError):
        bidule = Animal('Bidule', 'lalala')
        
def test_init():
    bidule = Animal('Bidule', 600)
    assert bidule.masse == 600
    assert bidule.vivant
    assert bidule.estVivant()
    assert not bidule.empoisonne

def test_str():
    bidule = Animal('Bidule', 600)
    assert str(bidule) == 'Bidule (600.0 kg)'
    
def test_mort():
    bidule = Animal('Bidule', 600)
    assert bidule.estVivant()
    bidule.mourir()
    assert not bidule.estVivant()
    
def test_lt():
    m = Animal('Medor', 600)
    k = Animal('Kiki', 20)
    assert k<m
    with pytest.raises(AttributeError):
        m<1

def test_mange():
    m = Animal('Medor', 600)
    k = Animal('Kiki', 20)
    m(k)
    assert m.estVivant()
    assert not k.estVivant()
    assert k.masse == 0
    assert m.masse == 620
    k = Animal('Kiki2', 20)
    k(m)
    assert not m.estVivant()
    assert k.estVivant()
    assert k.masse == 22
    assert m.masse == 618
    
def test_init_chien():
    m = Chien('Medor', 600)
    assert isinstance(m, Animal)
    assert isinstance(m, Chien)
    assert m.odorat == 0.5
    assert str(m) == 'Medor (Chien, 600.0 kg)'
    assert m.estVivant()

