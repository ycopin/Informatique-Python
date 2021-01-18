#!/usr/bin/env python3
# coding: utf-8

import random

nmin, nmax = 1, 100
nsol = random.randint(nmin, nmax)

print(f"Vous devez deviner un nombre entre {nmin} et {nmax}.")
ncoups = 0                      # Compteur de coups

while True:                     # Boucle infinie: sortie explicite par break
    try:
        proposition = input("Votre proposition: ")
        ntest = int(proposition)       # Exception ValueError potentielle
        if not nmin <= ntest <= nmax:
            raise ValueError()

    except ValueError:
        print(f"Votre proposition {proposition!r} "
              f"n'est pas un entier compris entre {nmin} et {nmax}.")
        continue                # Nouvel essai

    except (KeyboardInterrupt, EOFError):  # Interception de Ctrl-C et Ctrl-D
        print("\nVous abandonnez après seulement "
              f"{ncoups} coup{'s' if ncoups > 1 else ''}!")
        break                   # Interrompt la boucle while

    # Si la proposition est valide, le jeu peut continuer.
    ncoups += 1
    if nsol > ntest:
        print("C'est plus.")
    elif nsol < ntest:
        print("C'est moins.")
    else:
        print(f"Vous avez trouvé en {ncoups} coup{'s' if ncoups > 1 else ''}!")
        break                   # Interrompt la boucle while
