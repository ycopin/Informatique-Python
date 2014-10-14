#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest                   # Module (non-standard) de tests


class Animal(object):  # *object* est la classe dont dérivent toutes les autres
    """
    Classe définissant un `Animal`, caractérisé par son nom et son
    poids.
    """

    def __init__(self, nom, masse):
        """Méthode d'instanciation à partir d'un nom et d'un poids."""

        # Ici, convertir les paramètres pour être sûr qu'il ont le bon
        # type. On utilisera `str` et `float`
        self.nom = nom
        self.masse = masse

        self.vivant = True       # Les animaux sont vivant à l'instantiation
        self.empoisonne = False  # Animal empoissoné?

    def __str__(self):
        """
        Surcharge de l'opérateur `str`: l'affichage *informel* de l'objet
        dans l'interpréteur, p.ex. `print self` sera résolu comme
        `self.__str__()`

        Retourne une chaîne de caractères.
        """

        return "{0}".format(self.nom)

    def estVivant(self):
        """Méthode booléenne, vraie si l'animal est vivant."""

        return False

    def mourir(self):
        """Change l'état interne de l'objet (ne retourne rien)."""

        pass

    def __cmp__(self, other):
        """
        Surcharge des opérateurs de comparaison, sur la base de la masse
        des animaux.
        """

        return False

    def __call__(self, other):
        """
        Surcharge de l'opérateur '()' pour manger un autre animal (qui
        meurt s'il est vivant) et prendre du poids (mais pas plus que
        la masse de l'autre ou 10% de son propre poids). Attention aux
        animaux empoisonnés!

        L'instruction `self(other)` sera résolue comme
        `self.__call__(other).
        """

        pass


class Chien(Animal):
    """
    Un `Chien` hérite de `Animal` avec des méthodes additionnelles
    (p.ex. l'aboyement et l'odorat).
    """

    def __init__(self, nom, masse=20, odorat=0.5):
        """Définit un chien plus ou moins fin limier."""

        # Initialisation de la classe parente
        Animal.__init__(self, nom, masse)

        # Attribut propre à la classe dérivée
        self.odorat = float(odorat)

    def aboyer(self):
        """Une méthode bien spécifique aux chiens."""

        print("Ouaf ! Ouaf !")

    def estVivant(self):
        """Quand on vérifie qu'un chien est vivant, il aboie."""

        vivant = Animal.estVivant(self)

        if vivant:
            self.aboyer()

        return vivant

# start-tests
def test_empty_init():
    with pytest.raises(TypeError):
        youki = Animal()

def test_wrong_init():
    with pytest.raises(ValueError):
        youki = Animal('Youki', 'lalala')

def test_init():
    youki = Animal('Youki', 600)
    assert youki.masse == 600
    assert youki.vivant
    assert youki.estVivant()
    assert not youki.empoisonne
# end-tests

def test_str():
    youki = Animal('Youki', 600)
    assert str(youki) == 'Youki (600.0 kg)'

def test_mort():
    youki = Animal('Youki', 600)
    assert youki.estVivant()
    youki.mourir()
    assert not youki.estVivant()

def test_lt():
    medor = Animal('Medor', 600)
    kiki = Animal('Kiki', 20)
    assert kiki < medor
    with pytest.raises(AttributeError):
        medor < 1

def test_mange():
    medor = Animal('Medor', 600)
    kiki = Animal('Kiki', 20)
    medor(kiki)                 # Médor mange Kiki
    assert medor.estVivant()
    assert not kiki.estVivant()
    assert kiki.masse == 0
    assert medor.masse == 620
    kiki = Animal("Kiki Jr.", 20)
    kiki(medor)                 # Kiki Jr. mange Médor
    assert not medor.estVivant()
    assert kiki.estVivant()
    assert kiki.masse == 22
    assert medor.masse == 618

def test_init_chien():
    medor = Chien('Medor', 600)
    assert isinstance(medor, Animal)
    assert isinstance(medor, Chien)
    assert medor.odorat == 0.5
    assert str(medor) == 'Medor (Chien, 600.0 kg)'
    assert medor.estVivant()
