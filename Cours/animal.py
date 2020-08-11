#!/usr/bin/env python3
# coding: utf-8

"""
Exemple (tragique) de Programmation Orientée Objet.
"""


# Définition d'une classe ==============================

class Animal:
    """
    Un animal, défini par sa masse.
    """

    def __init__(self, masse):
        """
        Initialisation d'un Animal, a priori vivant.

        :param float masse: masse en kg (> 0)
        :raise ValueError: masse non réelle ou négative
        """

        self.estVivant = True

        self.masse = float(masse)
        if self.masse < 0:
            raise ValueError("La masse ne peut pas être négative.")


    def __str__(self):
        """
        Surcharge de la fonction `str()`.

        L'affichage *informel* de l'objet dans l'interpréteur, p.ex. `print(a)`
        sera résolu comme `a.__str__()`

        :return: une chaîne de caractères
        """

        return f"Animal {'vivant' if self.estVivant else 'mort'}, " \
            f"{self.masse:.0f} kg"


    def meurt(self):
        """
        L'animal meurt.
        """

        self.estVivant = False


    def grossit(self, masse):
        """
        L'animal grossit (ou maigrit) d'une certaine masse (valeur algébrique).

        :param float masse: prise (>0) ou perte (<0) de masse.
        :raise ValueError: masse non réelle.
        """

        self.masse += float(masse)


# Définition d'une classe héritée ==============================

class AnimalFeroce(Animal):
    """
    Un animal féroce est un animal qui peut dévorer d'autres animaux.

    La classe-fille hérite des attributs et méthodes de la
    classe-mère, mais peut les surcharger (i.e. en changer la
    définition), ou en ajouter de nouveaux:

    - la méthode `AnimalFeroce.__init__()` dérive directement de
      `Animal.__init__()` (même méthode d'initialisation);
    - `AnimalFeroce.__str__()` surcharge `Animal.__str__()`;
    - `AnimalFeroce.devorer()` est une nouvelle méthode propre à
      `AnimalFeroce`.
    """

    def __str__(self):
        """
        Surcharge de la fonction `str()`.
        """

        return "Animal féroce " \
            f"{'bien vivant' if self.estVivant else 'mais mort'}, " \
            f"{self.masse:.0f} kg"

    def devore(self, other):
        """
        L'animal (self) devore un autre animal (other).

        * Si other est également un animal féroce, il faut que self soit plus
          gros que other pour le dévorer. Sinon, other se défend et self meurt.
        * Si self dévore other, other meurt, self grossit de la masse de other
          (jusqu'à 10% de sa propre masse) et other maigrit d'autant.

        :param Animal other: animal à dévorer
        :return: prise de masse (0 si self meurt)
        """

        if isinstance(other, AnimalFeroce) and (other.masse > self.masse):
            # Pas de chance...
            self.meurt()
            prise = 0.
        else:
            other.meurt()             # Other meurt
            prise = min(other.masse, self.masse * 0.1)
            self.grossit(prise)       # Self grossit
            other.grossit(-prise)     # Other maigrit

        return prise


# Définition d'une autre classe héritée ==============================

class AnimalGentil(Animal):
    """
    Un animal gentil est un animal avec un petit nom.

    La classe-fille hérite des attributs et méthodes de la
    classe-mère, mais peut les surcharger (i.e. en changer la
    définition), ou en ajouter de nouveaux:

    - la méthode `AnimalGentil.__init__()` surcharge l'initialisation originale
      `Animal.__init__()`;
    - `AnimalGentil.__str__()` surcharge `Animal.__str__()`;
    """

    def __init__(self, masse, nom='Youki'):
        """
        Initialisation d'un animal gentil, avec son masse et son nom.
        """

        # Initialisation de la classe parente (nécessaire pour assurer
        # l'héritage)
        Animal.__init__(self, masse)

        # Attributs propres à la classe AnimalGentil
        self.nom = nom

    def __str__(self):
        """
        Surcharge de la fonction `str()`.
        """

        return f"{self.nom}, un animal gentil " \
            f"{'bien vivant' if self.estVivant else 'mais mort'}, " \
            f"{self.masse:.0f} kg"

    def meurt(self):
        """
        L'animal gentil meurt, avec un éloge funéraire.
        """

        Animal.meurt(self)
        print(f"Pauvre {self.nom} meurt, paix à son âme...")


if __name__ == '__main__':

    # Exemple d'utilisation des classes définies ci-dessus

    print("Une tragédie en trois actes".center(70, '='))

    print("Acte I: la vache prend 10 kg.".center(70, '-'))
    vache = Animal(500.)        # Instantiation d'un animal de 500 kg
    vache.grossit(10)           # La vache grossit de 10 kg
    print(vache)

    print("Acte II: Dumbo l'éléphant".center(70, '-'))
    elephant = AnimalGentil(1000., "Dumbo")  # Instantiation d'un animal gentil
    print(elephant)

    print("Acte III: le féroce lion".center(70, '-'))
    lion = AnimalFeroce(200)    # Instantiation d'un animal féroce
    print(lion)

    print("Scène tragique: le lion dévore l'éléphant...".center(70, '-'))
    lion.devore(elephant)       # Le lion dévore l'éléphant

    print(elephant)
    print(lion)
