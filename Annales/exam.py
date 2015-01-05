#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Proposition d'examen final "Outils numériques et programmation", janvier 2015.
"""

from __future__ import division

import numpy as N
import pytest

N.random.seed(123)
TAILLE = 50

class Ville(object):

    """
    Ville, contient une liste (non-ordonnée) de destinations.
    """

    def __init__(self):
        """Initialisation d'une ville sans destination."""

        self.destinations = N.array([]).reshape(-1, 2)

    def aleatoire(self, n=20):
        """Création de *n* destinations aléatoires."""

        raise NotImplementedError

    def lecture(self, nomfichier="ville.dat"):
        """
        Lecture d'un fichier ASCII donnant les coordonnées des destinations.
        """

        raise NotImplementedError

    def ecriture(self, nomfichier="ville.dat"):
        """
        Écriture d'un fichier ASCII avec les coordonnées des destinations.
        """

        raise NotImplementedError

    def nb_trajets(self):
        """Retourne le nombre total (entier) de trajets: (n-1)!/2."""

        raise NotImplementedError

    def distance(self, i, j):
        """
        Retourne la distance Manhattan-L1 entre les destinations numéro
        *i* et *j*.
        """

        raise NotImplementedError

    def plus_proche(self, i, exclus=[]):
        """
        Retourne la destination la plus proche de la destination *i*, hors les
        destinations de la liste `exclus`.
        """

        raise NotImplementedError

    def trajet_voisins(self, depart=0):
        """
        Retourne un `Trajet` déterminé selon l'heuristique des plus proches
        voisins (i.e. l'étape suivante est la destination la plus proche hors
        les destinations déjà visitées) en partant de l'étape initiale
        `depart`.
        """

        raise NotImplementedError

    def optimisation_trajet(self, trajet):
        """
        Retourne le trajet le plus court de tous les trajets « voisins » à
        `trajet` (i.e. résultant d'une simple interversion de 2 étapes).
        """

        raise NotImplementedError

    def trajet_opt2(self, trajet=None, maxiter=100):
        """
        À partir d'un `trajet` initial (par défaut le trajet des plus proches
        voisins), retourne un `Trajet` optimisé de façon itérative par
        interversion successive de 2 étapes.  Le nombre maximum d'itération est
        `maxiter`.
        """

        raise NotImplementedError


class Trajet(object):

    """
    Trajet, contient une liste ordonnée des destinations (étapes) d'une
    Ville.
    """

    def __init__(self, ville, etapes=None):
        """
        Initialisation sur une `ville`.  Si `etapes` n'est pas spécifié, le
        trajet par défaut est celui suivant les destinations de `ville`.
        """

        raise NotImplementedError

    def longueur(self):
        """
        Retourne la longueur totale du trajet *bouclé* (i.e. revenant à son
        point de départ).
        """

        raise NotImplementedError

    def interversion(self, i, j):
        """
        Retourne un nouveau `Trajet` résultant de l'interversion des 2 étapes
        *i* et *j*.
        """

        raise NotImplementedError


# TESTS ==============================

def test_ville_aleatoire():

    ville = Ville()
    ville.aleatoire(10)
    assert ville.destinations.shape == (10, 2)
    assert N.issubdtype(ville.destinations.dtype, int)

def test_ville_lecture():

    ville = Ville()
    ville.lecture("ville.dat")
    assert ville.destinations.shape == (20, 2)
    assert (ville.destinations[:3] == [[45, 2], [28, 34], [38, 17]]).all()

@pytest.fixture
def ville_test():

    ville = Ville()
    ville.destinations = N.array([[0, 0], [1, 1], [3, 0], [2, 2]])
    return ville

def test_ville_ecriture(ville_test):

    ville_test.ecriture("test_ecriture.dat")
    ville = Ville()
    ville.lecture("test_ecriture.dat")
    assert (ville_test.destinations == ville.destinations).all()

def test_ville_trajets(ville_test):

    assert ville_test.nb_trajets() == 3

def test_ville_distance(ville_test):

    assert ville_test.distance(0, 1) == 2
    assert ville_test.distance(1, 2) == 3
    assert ville_test.distance(2, 0) == 3

def test_trajet_init(ville_test):

    trajet = Trajet(ville_test)
    assert (trajet.etapes == range(4)).all()

@pytest.fixture
def trajet_test(ville_test):

    return Trajet(ville_test)

def test_trajet_longueur(trajet_test):

    assert trajet_test.longueur() == 12

def test_ville_plus_proche(ville_test):

    assert ville_test.plus_proche(0) == 1
    assert ville_test.plus_proche(0, [1, 2]) == 3

def test_ville_trajet_voisins(ville_test):

    assert (ville_test.trajet_voisins(depart=0).etapes == [0, 1, 3, 2]).all()

def test_trajet_interversion(trajet_test):

    assert (trajet_test.interversion(0, 1).etapes == [1, 0, 2, 3]).all()

def test_ville_optimisation_trajet(ville_test, trajet_test):

    assert (ville_test.optimisation_trajet(trajet_test).etapes ==
            [1, 0, 2, 3]).all()
