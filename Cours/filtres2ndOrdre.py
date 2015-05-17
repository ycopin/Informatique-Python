#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2015-05-17 23:44 ycopin@lyonovae03.in2p3.fr>

import numpy as N
import matplotlib.pyplot as P


def passeBas(x, Q=1):
    """
    Filtre passe-bas en pulsation réduite *x* = omega/omega0, facteur de
    qualité *Q*.
    """

    return 1 / (1 - x ** 2 + x / Q * 1j)


def passeHaut(x, Q=1):

    return -x ** 2 / (1 - x ** 2 + x / Q * 1j)


def passeBande(x, Q=1):

    return 1 / (1 + Q * (x - 1 / x) * 1j)


def coupeBande(x, Q=1):

    return (1 - x ** 2) / (1 - x ** 2 + x / Q * 1j)


def gainNphase(f, dB=True):
    """
    Retourne le gain (éventuellement en dB) et la phase [rad] d'un
    filtre de fonction de transfert complexe *f*.
    """

    g = N.abs(f)                        # Gain
    if dB:                              # [dB]
        g = 20 * N.log10(g)
    p = N.angle(f)                      # [rad]

    return g, p


def asympGain(x, pentes=(0, -40)):

    lx = N.log10(x)
    return N.where(lx < 0, pentes[0] * lx, pentes[1] * lx)


def asympPhase(x, phases=(0, -N.pi)):

    return N.where(x < 1, phases[0], phases[1])


def diagBode(x, filtres, labels,
             title='', plim=None, gAsymp=None, pAsymp=None):
    """
    Trace le diagrame de Bode -- gain [dB] et phase [rad] -- des filtres
    de fonction de transfert complexe *filtres* en fonction de la pulsation
    réduite *x*.
    """

    fig = P.figure()
    axg = fig.add_subplot(2, 1, 1,        # Axe des gains
                          xscale='log',
                          ylabel='Gain [dB]')
    axp = fig.add_subplot(2, 1, 2,        # Axe des phases
                          sharex=axg,
                          xlabel=r'x = $\omega$/$\omega_0$', xscale='log',
                          ylabel='Phase [rad]')

    lstyles = ['--', '-', '-.', ':']
    for f, label, ls in zip(filtres, labels, lstyles):  # Tracé des courbes
        g, p = gainNphase(f, dB=True)       # Calcul du gain et de la phase
        axg.plot(x, g, lw=2, ls=ls, label="Q=" + str(label))  # Gain
        axp.plot(x, p, lw=2, ls=ls)                           # Phase

    # Asymptotes
    if gAsymp is not None:              # Gain
        axg.plot(x, asympGain(x, gAsymp), 'k:', lw=2, label='_')
    if pAsymp is not None:              # Phase
        #axp.plot(x, asympPhase(x,pAsymp), 'k:')
        pass

    axg.legend(loc='best', prop=dict(size='small'))

    # Labels des phases
    axp.set_yticks(N.arange(-2, 2.1) * N.pi / 2)
    axp.set_yticks(N.arange(-4, 4.1) * N.pi / 4, minor=True)
    axp.set_yticklabels([r'$-\pi$', r'$-\pi/2$', r'$0$', r'$\pi/2$', r'$\pi$'])
    # Domaine des phases
    if plim is not None:
        axp.set_ylim(plim)

    # Ajouter les grilles
    for ax in (axg, axp):
        ax.grid()                           # x et y, majors
        ax.grid(which='minor')              # x et y, minors

    # Ajustements fins
    gmin, gmax = axg.get_ylim()
    axg.set_ylim(gmin, max(gmax, 3))

    fig.subplots_adjust(hspace=0.1)
    axg.xaxis.set_major_formatter(P.matplotlib.ticker.ScalarFormatter())
    P.setp(axg.get_xticklabels(), visible=False)

    if title:
        axg.set_title(title)

    return fig

if __name__ == '__main__':

    #P.rc('mathtext', fontset='stixsans')

    x = N.logspace(-1, 1, 1000)              # de 0.1 à 10 en 1000 pas

    # Facteurs de qualité
    qs = [0.25, 1 / N.sqrt(2), 5]            # Valeurs numériques
    labels = [0.25, r'$1/\sqrt{2}$', 5]      # Labels
    
    # Calcul des fonctions de transfert complexes
    pbs = [ passeBas(x, Q=q) for q in qs ]
    phs = [ passeHaut(x, Q=q) for q in qs ]
    pcs = [ passeBande(x, Q=q) for q in qs ]
    cbs = [ coupeBande(x, Q=q) for q in qs ]

    # Création des 4 diagrames de Bode
    figPB = diagBode(x, pbs, labels, title='Filtre passe-bas',
                     plim=(-N.pi, 0),
                     gAsymp=(0, -40), pAsymp=(0, -N.pi))
    figPH = diagBode(x, phs, labels, title='Filtre passe-haut',
                     plim=(0, N.pi),
                     gAsymp=(40, 0), pAsymp=(N.pi, 0))
    figPC = diagBode(x, pcs, labels, title='Filtre passe-bande',
                     plim=(-N.pi / 2, N.pi / 2),
                     gAsymp=(20, -20), pAsymp=(N.pi / 2, -N.pi / 2))
    figCB = diagBode(x, cbs, labels, title='Filtre coupe-bande',
                     plim=(-N.pi / 2, N.pi / 2),
                     gAsymp=(0, 0), pAsymp=(0, 0))

    P.show()
