#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Proposition d'examen final "Outils numériques et programmation", janvier 2015.
"""

from __future__ import division

__author__ = 'Yannick Copin <y.copin@ipnl.in2p3.fr>'

import math
import numpy as N
import pytest

import matplotlib.pyplot as P
try:
    import seaborn
    seaborn.set_style("white")
    seaborn.set_palette("cubehelix_r", 4)
except ImportError:
    pass

N.random.seed(123)
TAILLE = 50

class Ville(object):

    """
    Ville, contient une liste (non-ordonnée) de destinations.
    """

    def __init__(self):
        """Initialisation d'une ville sans destination."""

        self.destinations = N.array([]).reshape(-1, 2)

    def __str__(self):

        return "Ville: {} destinations ({} trajets)".format(
            len(self.destinations), self.nb_trajets())

    def aleatoire(self, n=20):
        """Création de *n* destinations aléatoires."""

        self.destinations = N.random.randint(TAILLE, size=2*n).reshape(n, 2)

    def lecture(self, nomfichier="ville.dat"):
        """
        Lecture d'un fichier ASCII donnant les coordonnées des destinations.
        """

        try:
            self.destinations = N.loadtxt(nomfichier, dtype=int)
            if self.destinations.ndim != 2 or self.destinations.shape[1] != 2:
                raise IOError
        except IOError:
            raise IOError("Le fichier {!r} est invalide".format(nomfichier))

    def ecriture(self, nomfichier="ville.dat"):
        """
        Écriture d'un fichier ASCII avec les coordonnées des destinations.
        """

        N.savetxt(nomfichier, self.destinations, fmt='%d')

    def nb_trajets(self):
        """Retourne le nombre total (entier) de trajets: (n-1)!/2."""

        ndest = len(self.destinations)
        if ndest > 2:
            return int(math.factorial(ndest - 1) / 2)
        elif ndest > 0:
            return 1
        else:
            return 0

    def distance(self, i, j):
        """
        Retourne la distance Manhattan-L1 entre les destinations numéro
        *i* et *j*.
        """

        return N.abs(self.destinations[i] - self.destinations[j]).sum()

    def plus_proche(self, i, exclus=[]):
        """
        Retourne la destination la plus proche de la destination *i*, hors les
        destinations de la liste `exclus`.
        """

        voisins = [ j for j in range(len(self.destinations))
                    if j != i and j not in exclus ]
        distances = [ self.distance(i, j) for j in voisins ]

        return voisins[N.argmin(distances)]

    def trajet_voisins(self, depart=0):
        """
        Retourne un `Trajet` déterminé selon l'heuristique des plus proches
        voisins (i.e. l'étape suivante est la destination la plus proche hors
        les destinations déjà visitées) en partant de l'étape initiale
        `depart`.
        """

        ndest = len(self.destinations)
        if depart is None:     # Boucle sur tous les départs possibles
            trajets = [ self.trajet_voisins(depart=i) for i in range(ndest) ]
            longueurs = [ t.longueur() for t in trajets ]

            return trajets[N.argmin(longueurs)]
        else:                  # Départ imposé
            etapes = [depart]
            while len(etapes) < ndest:
                i = etapes[-1]
                j = self.plus_proche(i, exclus=etapes[:-1])
                etapes.append(j)

            return Trajet(self, etapes)

    def optimisation_trajet(self, trajet):
        """
        Retourne le trajet le plus court de tous les trajets « voisins » à
        `trajet` (i.e. résultant d'une simple interversion de 2 étapes).
        """

        ndest = len(self.destinations)
        trajets = [ trajet.interversion(i, j)
                    for i in range(ndest) for j in range(i+1, ndest) ]
        longueurs = [ t.longueur() for t in trajets ]
        opt = trajets[N.argmin(longueurs)]
        if opt.longueur() > trajet.longueur():
            opt = trajet

        return opt

    def trajet_opt2(self, trajet=None, maxiter=100):
        """
        À partir d'un `trajet` initial (par défaut le trajet des plus proches
        voisins), retourne un `Trajet` optimisé de façon itérative par
        interversion successive de 2 étapes.  Le nombre maximum d'itération est
        `maxiter`.
        """

        if trajet is None:
            trajet = self.trajet_voisins()

        for i in range(maxiter):
            opt = self.optimisation_trajet(trajet)
            if opt.longueur() == trajet.longueur():
                break
            else:
                print "Optimisation: L={} -> {}".format(
                    trajet.longueur(), opt.longueur())
                trajet = opt
        print "opt2: optimisation en {} iterations".format(i+1)

        return opt

    def figure(self, trajet=None, ax=None, offset=0):
        """
        Visualisation d'une ville et d'un trajet.
        """

        if ax is None:
            fig = P.figure(figsize=(6,6))
            ax = fig.add_subplot(1,1,1, aspect='equal',
                                 xlim=(0, TAILLE), ylim=(0, TAILLE),
                                 title="{} destinations".format(
                                     len(self.destinations)))
            minor_loc = P.matplotlib.ticker.MultipleLocator(1)
            ax.xaxis.set_minor_locator(minor_loc)
            ax.yaxis.set_minor_locator(minor_loc)
            ax.autoscale(False)

        if trajet is None:
            ax.plot(self.destinations[:, 0], self.destinations[:, 1],
                    'ko', zorder=10)
            for i,(x,y) in enumerate(self.destinations):
                #ax.text(x, y, ' '+str(i))
                ax.annotate(str(i), xy=(x, y), xytext=(x+0.5, y+0.5), zorder=10)
        else:
            boucle = N.concatenate((trajet.etapes, [trajet.etapes[0]]))
            ax.step(self.destinations[boucle, 0] + offset,
                    self.destinations[boucle, 1] + offset,
                    label="L={}".format(trajet.longueur()))

        return ax


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

        assert isinstance(ville, Ville)
        self.ville = ville
        if etapes is None:                     # Trajet par défaut
            self.etapes = N.arange(len(self.ville.destinations))
        else:
            self.etapes = N.array(etapes)

    def __str__(self):

        return "{}-trajet L={}: {}".format(
            len(self.etapes), self.longueur(), self.etapes)

    def longueur(self):
        """
        Retourne la longueur totale du trajet *bouclé* (i.e. revenant à son
        point de départ).
        """

        l = sum( self.ville.distance(self.etapes[i], self.etapes[i+1])
                 for i in range(len(self.etapes)-1) )
        l += self.ville.distance(self.etapes[-1], self.etapes[0])

        return l

    def interversion(self, i, j):
        """
        Retourne un nouveau `Trajet` résultant de l'interversion des 2 étapes
        *i* et *j*.
        """

        etapes = self.etapes.copy()
        etapes[[i, j]] = etapes[[j, i]]

        return Trajet(self.ville, etapes)


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

# def test_ville_ppv():

#     ville = Ville()
#     ville.lecture("ville.dat")
#     assert ville.trajet_voisins(depart=0).longueur() == 288

# def test_ville_opt2():

#     ville = Ville()
#     ville.lecture("ville.dat")
#     assert ville.trajet_opt2().longueur() == 276

if __name__ == '__main__':

    ville = Ville()
    ville.aleatoire(n=20)
    print ville
    ville.ecriture()

    ville2 = Ville()
    ville2.lecture()
    assert (ville.destinations == ville2.destinations).all()

    ax = ville.figure()

    trajet = Trajet(ville)
    print trajet
    ville.figure(trajet, ax=ax, offset=-0.3)

    trajet_voisins = ville.trajet_voisins(depart=0)
    print "Trajet PPV:", trajet_voisins
    ville.figure(trajet_voisins, ax=ax)

    trajet_opt2 = ville.trajet_opt2(trajet_voisins)
    print "Trajet PPV + opt2:", trajet_opt2
    ville.figure(trajet_opt2, ax=ax, offset=0.3)

    h, l = ax.get_legend_handles_labels()
    ax.figure.legend(h, l, fontsize='small', loc='upper right')
    P.show()
