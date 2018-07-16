#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2018-07-16 18:31:01 ycopin>

__author__ = "Adrien Licari <adrien.licari@ens-lyon.fr>; Yannick Copin <y.copin@ipnl.in2p3.fr>"


def suite_syracuse(n):
    """
    Retourne la suite de Syracuse pour l'entier n.

    >>> suite_syracuse(15)
    [15, 46, 23, 70, 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1]
    """

    seq = [n]                     # La suite de Syracuse sera complétée...
    while (seq[-1] != 1):         # ...jusqu'à tomber sur 1
        if seq[-1] % 2 == 0:      # u_n est pair
            seq.append(seq[-1] // 2)  # Division euclidienne par 2
        else:                     # u_n est impair
            seq.append(seq[-1] * 3 + 1)

    return seq


def temps_syracuse(n, altitude=False):
    """
    Calcule le temps de vol (éventuellement en altitude) de la suite
    de Syracuse pour l'entier n.

    >>> temps_syracuse(15)
    17
    >>> temps_syracuse(15, altitude=True)
    10
    """

    seq = suite_syracuse(n)
    if not altitude:            # Temps de vol total
        return len(seq) - 1
    else:                       # Temps de vol en altitude
        # Construction de la séquence en altitude
        alt = []
        for i in seq:
            if i >= n:
                alt.append(i)
            else:
                break
        return len(alt) - 1

if __name__ == '__main__':

    n = 15
    print("Suite de Syracuse pour n =", n)
    print(suite_syracuse(n))
    print("Temps de vol total:      ", temps_syracuse(n))
    print("Temps de vol en altitude:", temps_syracuse(n, altitude=True))
