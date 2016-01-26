#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2015-01-13 14:57:37 ycopin>

import random

nmin, nmax = 1, 100
nsol = random.randint(nmin, nmax)

print "Vous devez deviner un nombre entre {} et {}.".format(nmin, nmax)
ncoups = 0
try:
    while True:
        proposition = raw_input("Votre proposition: ")
        try:
            ntest = int(proposition)
            if not nmin <= ntest <= nmax:
                raise ValueError("Proposition invalide")
        except ValueError:
            print "Votre proposition {!r} n'est pas un entier " \
                "compris entre {} et {}.".format(proposition, nmin, nmax)
            continue
        ncoups += 1
        if nsol > ntest:
            print "C'est plus."
        elif nsol < ntest:
            print "C'est moins."
        else:
            print "Vous avez trouvé en {} coup{}!".format(
                ncoups, 's' if ncoups > 1 else '')
            break  # Interrompt la boucle while
except (KeyboardInterrupt, EOFError):  # Interception de Ctrl-C et Ctrl-D
    print "\nVous abandonnez après seulement {} coup{}!".format(
        ncoups, 's' if ncoups > 1 else '')
