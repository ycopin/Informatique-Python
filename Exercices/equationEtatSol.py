#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2014-10-03 16:56:47 alicari>


from __future__ import division  # division reelle de type python 3, admis
import pytest                    # pytest importe pour les tests unitaires
import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import lines as mlines

"""
Construction d'un système d'extraction et d'analyse de fichiers de sortie de
dynamique moléculaire afin d'extraire les grandeurs thermodynamiques.
On affichera les ensuite isothermes.
"""

__author__ = "Adrien Licari <adrien.licari@ens-lyon.fr>"


tolerance = 1e-8  # Un seuil de tolérance pour les égalités sur réels


##############################
##### A Simulation class #####
##############################

class Simulation(object):
    """
    La classe Simulation représente une simulation de dynamique
    moléculaire, donc un point de l'équation d'état. Son constructeur
    doit impérativement être appelé avec le chemin du fichier output
    correspondant. Elle possède des méthodes pour extraire les grandeurs
    thermodynamiques et afficher la run, en pouvant enlever certains pas
    de temps en début de simulation.
    """

    def __init__(self, temp, dens, path=""):
        """
        Le construcuteur doit impérativement être appelé avec le chemin du
        fichier décrivant la simulation, ainsi que ses conditions
        thermodynamiques.

        Args :
                temp,dens(float): La température et la densité de la simulation
                path(string): Le chemin vers le fichier décrivant la simulation

        Raises :
                TypeError si path n'est pas un objet string, ou si temp ou dens
                        ne sont pas des réels, ou si moins de 3 arguments sont
                        donnés
                IOError si le fichier n'existe pas
        """
        try:
            self.temp = float(temp)
            self.dens = float(dens)
        except (ValueError, TypeError):
            raise TypeError("Temperature and density must be floats")
        try:
            assert isinstance(path, basestring)
        except AssertionError:
            raise TypeError("path must be a string object")
        else:
            tmp = np.loadtxt(path, skiprows=1).T
            self.pot = tmp[0]
            self.kin = tmp[1]
            self.tot = self.pot+self.kin
            self.press = tmp[2]

    def __str__(self):
        """
        Surcharge de l'opérateur str.
        """
        return "Simulation at {:.0f} g/cc and {:.0f} K ; {:d} timesteps". \
            format(self.dens, self.temp, len(self.pot))

    def thermo(self, skipSteps=0):
        """
        Calcule l'énergie et la pression moyenne au cours de la simulation.
        Renvoie un dictionnaire.

        Args:
                skipSteps(int): Pas de temps à enelevr en début de simulation.

        Returns:
                {'T':temperature, 'rho':density,
                 'E':energy, 'P':pressure,
                 'dE':dEnergy, 'dP':dPressure}

        Raises:
                TypeError si skipSteps n'est pas un entier.
        """
        try:
            skip = int(skipSteps)
            if skip < 0:
                skip = 0
        except (ValueError, TypeError, AttributeError):
            raise TypeError("The given coordinates must be numbers")
        return {'T': self.temp,
                'rho': self.dens,
                'E': self.tot[skip:None].mean(),
                'P': self.press[skip:None].mean(),
                'dE': self.tot[skip:None].std(),
                'dP': self.press[skip:None].std()}

    def plot(self, skipSteps=0):
        """
        Affiche l'évolution de la Pression et l'énergie interne au cours de
        la simulation.

        Args:
                skipSteps(int): Pas de temps à enelevr en début de simulation.

        Raises:
                TypeError si skipSteps n'est pas un entier.
        """
        try:
            skip = int(skipSteps)
            if skip < 0:
                skip = 0
        except (ValueError, TypeError, AttributeError):
            raise TypeError("The given coordinates must be numbers")
        f, (en, press) = plt.subplots(2, sharex=True)
        en.plot(range(skip, len(self.tot)), self.tot[skip:None], 'rd--')
        en.set_title("Internal energy (Ha)")
        press.plot(range(skip, len(self.press)), self.press[skip:None],
                   'rd--')
        press.set_title("Pressure (GPa)")
        plt.xlabel("Timesteps")
        plt.show()


##### Tests pour Simulation #####

def test_Simulation_init():
    with pytest.raises(TypeError):
        Simulation(1, 1, path=32)
        Simulation(1, 1, path=[])
        Simulation(temp="", dens={})
        Simulation([], 3, Simulation())
    with pytest.raises(IOError):
        Simulation(10, 10)
    s = Simulation(10, 10, "equationEtat_simuTest.out")
    assert len(s.kin) == 5
    assert abs(s.kin[2]-0.7755612311) < tolerance
    assert abs(s.pot[1]+668.2118514558) < tolerance


def test_Simulation_str():
    s = Simulation(10, 20, "equationEtat_simuTest.out")
    assert str(s) == "Simulation at 20 g/cc and 10 K ; 5 timesteps"


def test_Simulation_thermo():
    s = Simulation(10, 20, "equationEtat_simuTest.out")
    with pytest.raises(TypeError):
        s.thermo("test")
        s.thermo([])
    assert abs(s.thermo()['T']-10) < tolerance
    assert abs(s.thermo()['rho']-20) < tolerance
    assert abs(s.thermo()['E']+667.56897157674) < tolerance
    assert abs(s.thermo()['P']-9241.0504034731) < tolerance
    assert abs(s.thermo(3)['E']+667.7007122865) < tolerance
    assert abs(s.thermo(3)['P']-9191.8574820856) < tolerance


def test_Simulation_all():
    print "Testing the Simulation class "
    test_Simulation_init()
    test_Simulation_str()
    test_Simulation_thermo()
    print "\t --> Simulation class tested : everything is ok"


###################
### Main script ###
###################

if __name__ == '__main__':
    """
    On définit un certain nombre de pas de temps à sauter, puis on
    charge chaque simulation et extrait les informaions thermodynamiques
    associées. On affiche enfin les isothermes normalisées (E/NkT et P/nkT).
    """

    ### Definitions ###
    a0 = 0.52918      # Bohr radius in angstrom
    amu = 1.6605      # atomic mass unit in e-24 g
    k_B = 3.16681e-6  # Boltzmann's constant in Ha/K
    nk_GPa = a0**3 * k_B * 2.942e4 / 6 / amu  # normalization factor for P/nkT
    nsteps = 200  # define skipped timesteps (should be done for
                  # each simulation...)
    temps = [6000, 20000, 50000]    # define temperatures
    colors = {6000: 'r', 20000: 'b', 50000: 'k'}
    denss = [7, 15, 25, 30]  # define densities
    keys = ['T', 'rho', 'E', 'dE', 'P', 'dP']
    eos = {k: v for k in keys for v in len(keys)*[np.zeros(0)]}

    ### Extract the EOS out of the source files ###
    for t, rho in [(t, rho) for t in temps for rho in denss]:
        filenm = "outputs/{}K_{:0>2d}gcc.out".format(t, rho)
        s = Simulation(t, rho, filenm)
        for k in keys:
            eos[k] = np.append(eos[k], s.thermo(nsteps)[k])

    ### Plot isotherms ###
    f, (en, press) = plt.subplots(2, sharex=True)
    plt.title("High-pressure equation of state for water")
    en.set_title("Energy")
    en.set_ylabel("U / NkT")
    press.set_title("Pressure")
    press.set_ylabel("P / nkT")
    plt.xlabel("rho (g/cc)")
    legend_lines = []
    legend_labels = []
    for t in temps:
        en.errorbar(x=eos['rho'][eos['T'] == t],
                    y=eos['E'][eos['T'] == t]/k_B/t,
                    yerr=eos['dE'][eos['T'] == t]/k_B/t,
                    fmt=colors[t]+'--')
        press.errorbar(x=eos['rho'][eos['T'] == t],
                       y=eos['P'][eos['T'] == t] /
                       eos['rho'][eos['T'] == t]/nk_GPa/t,
                       yerr=eos['dP'][eos['T'] == t] /
                       eos['rho'][eos['T'] == t]/nk_GPa/t,
                       fmt=colors[t]+'--')
        legend_lines.append(mlines.Line2D([], [], color=colors[t]))
        legend_labels.append("{} K".format(str(t)))
    plt.legend(legend_lines, legend_labels, loc='best')
    plt.show()
