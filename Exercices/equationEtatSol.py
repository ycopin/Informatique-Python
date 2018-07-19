#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2018-07-19 10:38 ycopin@lyonovae03.in2p3.fr>


import numpy as N
import matplotlib.pyplot as P

import pytest                    # pytest importe pour les tests unitaires

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

class Simulation:
    """
    La classe Simulation représente une simulation de dynamique
    moléculaire, donc un point de l'équation d'état. Son constructeur
    doit impérativement être appelé avec le chemin du fichier output
    correspondant. Elle possède des méthodes pour extraire les grandeurs
    thermodynamiques et afficher la run, en pouvant enlever certains pas
    de temps en début de simulation.
    """

    def __init__(self, temp, dens, path):
        """
        Le constructeur doit impérativement être appelé avec le chemin du
        fichier décrivant la simulation, ainsi que ses conditions
        thermodynamiques.

        Args :
                temp,dens(float): La température et la densité de la simulation
                path(string): Le chemin vers le fichier décrivant la simulation

        Raises :
                TypeError si temp ou dens ne sont pas des réels
                IOError si le fichier n'existe pas
        """
        self.temp = float(temp)
        self.dens = float(dens)
        tmp = N.loadtxt(path, skiprows=1).T
        self.pot = tmp[0]
        self.kin = tmp[1]
        self.tot = self.pot + self.kin
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
                skipSteps(int): Nb de pas à enlever en début de simulation.

        Returns:
                {'T':temperature, 'rho':density,
                 'E':energy, 'P':pressure,
                 'dE':dEnergy, 'dP':dPressure}
        """
        return {'T': self.temp,
                'rho': self.dens,
                'E': self.tot[skipSteps:].mean(),
                'P': self.press[skipSteps:].mean(),
                'dE': self.tot[skipSteps:].std(),
                'dP': self.press[skipSteps:].std()}

    def plot(self, skipSteps=0):
        """
        Affiche l'évolution de la Pression et l'énergie interne au cours de
        la simulation.

        Args:
                skipSteps(int): Pas de temps à enelevr en début de simulation.

        Raises:
                TypeError si skipSteps n'est pas un entier.
        """
        fig, (axen, axpress) = P.subplots(2, sharex=True)
        axen.plot(list(range(skipSteps, len(self.tot))), self.tot[skipSteps:],
                  'rd--')
        axen.set_title("Internal energy (Ha)")
        axpress.plot(list(range(skipSteps, len(self.press))), self.press[skipSteps:],
                     'rd--')
        axpress.set_title("Pressure (GPa)")
        axpress.set_xlabel("Timesteps")

        P.show()

##### Tests pour Simulation #####


def mimic_simulation(filename):
    with open(filename, 'w') as f:
        f.write("""Potential energy (Ha)	Kinetic Energy (Ha)	Pressure (GPa)
-668.2463567264        	0.7755612311   		9287.7370229824
-668.2118514558        	0.7755612311		9286.1395903265
-668.3119088218        	0.7755612311		9247.6604398856
-668.4762735176        	0.7755612311		9191.8574820856
-668.4762735176        	0.7755612311		9191.8574820856
""")


def test_Simulation_init():
    mimic_simulation("equationEtat_simuTest.out")
    s = Simulation(10, 10, "equationEtat_simuTest.out")
    assert len(s.kin) == 5
    assert abs(s.kin[2] - 0.7755612311) < tolerance
    assert abs(s.pot[1] + 668.2118514558) < tolerance


def test_Simulation_str():
    mimic_simulation("equationEtat_simuTest.out")
    s = Simulation(10, 20, "equationEtat_simuTest.out")
    assert str(s) == "Simulation at 20 g/cc and 10 K ; 5 timesteps"


def test_Simulation_thermo():
    mimic_simulation("equationEtat_simuTest.out")
    s = Simulation(10, 20, "equationEtat_simuTest.out")
    assert abs(s.thermo()['T'] - 10) < tolerance
    assert abs(s.thermo()['rho'] - 20) < tolerance
    assert abs(s.thermo()['E'] + 667.56897157674) < tolerance
    assert abs(s.thermo()['P'] - 9241.0504034731) < tolerance
    assert abs(s.thermo(3)['E'] + 667.7007122865) < tolerance
    assert abs(s.thermo(3)['P'] - 9191.8574820856) < tolerance

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
    # normalization factor for P/nkT
    nk_GPa = a0 ** 3 * k_B * 2.942e4 / 6 / amu
    nsteps = 200  # define skipped timesteps (should be done for
    # each simulation...)
    temps = [6000, 20000, 50000]    # define temperatures
    colors = {6000: 'r', 20000: 'b', 50000: 'k'}
    denss = [7, 15, 25, 30]  # define densities
    keys = ['T', 'rho', 'E', 'dE', 'P', 'dP']
    eos = dict.fromkeys(keys, N.zeros(0))   # {key:[]}

    ### Extract the EOS out of the source files ###
    for t, rho in [(t, rho) for t in temps for rho in denss]:
        filenm = "outputs/{}K_{:0>2d}gcc.out".format(t, rho)
        s = Simulation(t, rho, filenm)
        for key in keys:
            eos[key] = N.append(eos[key], s.thermo(nsteps)[key])

    ### Plot isotherms ###
    fig, (axen, axpress) = P.subplots(2, sharex=True)
    fig.suptitle("High-pressure equation of state for water", size='x-large')
    axen.set_title("Energy")
    axen.set_ylabel("U / NkT")
    axpress.set_title("Pressure")
    axpress.set_ylabel("P / nkT")
    axpress.set_xlabel("rho (g/cc)")
    for t in temps:
        sel = eos['T'] == t
        axen.errorbar(x=eos['rho'][sel], y=eos['E'][sel] / k_B / t,
                      yerr=eos['dE'][sel] / k_B / t, fmt=colors[t] + '-')
        axpress.errorbar(x=eos['rho'][sel],
                         y=eos['P'][sel] / eos['rho'][sel] / nk_GPa / t,
                         yerr=eos['dP'][sel] / eos['rho'][sel] / nk_GPa / t,
                         fmt=colors[t] + '-',
                         label="{} K".format(t))
    axpress.legend(loc='best')
    P.show()
