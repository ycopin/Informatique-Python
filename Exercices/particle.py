#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2018-07-19 10:29 ycopin@lyonovae03.in2p3.fr>


import pytest                    # pytest importé pour les tests unitaires
import math

"""
Définition d'une classe point matériel, avec sa masse, sa position et sa
vitesse, et des méthodes pour le déplacer.  Le main test applique cela à un
problème à force centrale gravitationnel ou électrostatique.

Remarque : Toutes les unités ont été choisies adimensionnées.
"""

__author__ = "Adrien Licari <adrien.licari@ens-lyon.fr>"


# Un critère pour déterminer l'égalité entre réels
tolerance = 1e-8


#############################################################################
### Définition de la classe Vector, utile pour la position et la vitesse. ###
#############################################################################

class Vector:
    """
    Une classe-structure simple contenant 3 coordonnées.
    Une méthode est disponible pour en calculer la norme et
    une surcharge des opérateurs ==, !=, +, - et * est proposée.
    """

    def __init__(self, x=0, y=0, z=0):
        """
        Constructeur de la classe vector.
        Par défaut, construit le vecteur nul.

        Args:
                x,y,z(float): Les composantes du vecteur à construire.

        Raises:
                TypeError en cas de composantes non réelles
        """
        try:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
        except (ValueError, TypeError, AttributeError):
            raise TypeError("The given coordinates must be numbers")

    def __str__(self):
        """
        Surcharge de l'opérateur `str`.

        Returns :
                "(x,y,z)" avec 2 décimales
        """
        return "({:.2f},{:.2f},{:.2f})".format(self.x, self.y, self.z)

    def __eq__(self, other):
        """
        Surcharge de l'opérateur `==` pour tester l'égalité
        entre deux vecteurs.

        Args :
                other(Vector): Un autre vecteur

        Raises :
                TypeError si other n'est pas un objet Vector
        """
        try:
            return abs(self.x - other.x) < tolerance and \
                abs(self.y - other.y) < tolerance and \
                abs(self.z - other.z) < tolerance
        except (ValueError, TypeError, AttributeError):
            raise TypeError("Tried to compare Vector and non-Vector objects")

    ### À implémenter ###
    def __ne__(self, other):
        """
        Surcharge de l'opérateur `!=` pour tester l'inégalité
        entre deux vecteurs.

        Args :
                other(Vector): Un autre vecteur

        Raises :
                TypeError si other n'est pas un objet Vector
        """
        raise NotImplementedError("You have to implement Vector.__ne__")

    def __add__(self, other):
        """
        Surcharge de l'opérateur `+` pour les vecteurs.

        Args :
                other(Vector): Un autre vecteur

        Raises :
                TypeError si other n'est pas un objet Vector
        """
        try:
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        except (ValueError, TypeError, AttributeError):
            raise TypeError("Tried to add Vector and non-Vector objects")

    ### À implémenter ###
    def __sub__(self, other):
        """
        Surcharge de l'opérateur `-` pour les vecteurs.

        Args :
                other(Vector): Un autre vecteur

        Raises :
                TypeError si other n'est pas un objet Vector
        """
        raise NotImplementedError("You have to implement Vector.__sub__")

    ### À implémenter ###
    def __mul__(self, number):
        """
        Surcharge de l'opérateur `*` pour la multiplication entre
        un vecteur et un nombre.

        Args :
                number(float): Un nombre à multiplier par le Vector.

        Raises :
                TypeError si other n'est pas un nombre
        """
        raise NotImplementedError("You have to implement Vector.__mul__")

    __rmul__ = __mul__  # Ligne pour autoriser la multiplication à droite

    ### À implémenter ###
    def norm(self):
        """
        Calcul de la norme 2 d'un vecteur.

        Returns :
                sqrt(x**2 + y**2 + z**2)
        """
        raise NotImplementedError("You have to implement Vector.norm")

    def clone(self):
        """
        Méthode pour construire un nouveau Vecteur, copie de self.
        """
        return Vector(self.x, self.y, self.z)


###############################################
##### Quelques test pour la classe Vector #####
###############################################

def test_VectorInit():
    with pytest.raises(TypeError):
        vec = Vector('Test', 'avec', 'strings')
        vec = Vector(Vector())
        vec = Vector([])
    vec = Vector(0, -53.76, math.pi)
    assert vec.x == 0
    assert vec.y == -53.76
    assert vec.z == math.pi


def test_VectorStr():
    vec = Vector(0, 600, -2)
    assert str(vec) == '(0.00,600.00,-2.00)'


def test_VectorEq():  # teste aussi l'opérateur !=
    vec = Vector(2, 3, -5)
    vec2 = Vector(2, 3, -4)
    assert vec != vec2
    assert vec != Vector(0, 3, -5)
    with pytest.raises(TypeError):
        Vector(2, 1, 4) == "Testing strings"
        Vector(2, 1, 4) == 42
        Vector(2, 1, 4) == ['list']


def test_VectorAdd():
    vec = Vector(2, 3, -5)
    vec2 = Vector(2, -50, 5)
    assert (vec + vec2) == Vector(4, -47, 0)


def test_VectorSub():
    vec = Vector(1, -7, 9)
    vec2 = Vector()
    assert (vec - vec) == Vector()
    assert (vec - vec2) == vec


def test_VectorMul():
    vec = Vector(1, -7, 9) * 2
    vec2 = 6 * Vector(1, -1, 2)
    assert vec == Vector(2, -14, 18)
    assert vec2 == Vector(6, -6, 12)


def test_VectorNorm():
    assert Vector().norm() == 0
    assert Vector(1, 0, 0).norm() == 1
    assert Vector(2, -5, -4).norm() == 45 ** (1 / 2)


def test_VectorClone():
    vec = Vector(3, 2, 9)
    vec2 = vec.clone()
    assert vec == vec2
    vec2.x = 1
    assert vec != vec2


############################################################
##### Une classe point matériel qui se gère en interne #####
############################################################

class Particle:

    """
    La classe Particle représente un point matériel doté d'une masse,
    d'une position et d'une vitesse. Elle possède également une méthode
    pour calculer la force gravitationnelle exercée par une autre particule.
    Enfin, la méthode update lui permet de mettre à jour sa position et
    sa vitesse en fonction des forces subies.
    """

    ### À implémenter; ne pas oublier de définir un attribut force ###
    def __init__(self, mass=1, position=Vector(), speed=Vector()):
        """
        Le constructeur de la classe Particle.
        Définit un point matériel avec une position et une vitesse initiales.

        Args :
                mass(float): La masse de la particule (doit être
                        strictement positive)
                position(Vector): La position initiale de la particule
                speed(Vector): La vitesse initiale de la particule

        Raises :
                TypeError si la masse n'est pas un nombre, ou si la position ou
                        la vitesse ne sont pas des Vector
                ValueError si la masse est négative ou nulle
        """
        raise NotImplementedError("You have to implement Particle.__init__")

    ### À implémenter ###
    def __str__(self):
        """
        Surcharge de l'opérateur `str`.

        Returns :
                "Particle with mass m, position (x,y,z) and speed (vx,vy,vz)"
                        avec 2 décimales
        """
        raise NotImplementedError("You have to implement Particle.__str__")

    def computeForce(self, other):
        """
        Calcule la force gravitationnelle exercée par une Particule
        other sur self.

        Args :
                other(Particle): Une autre particule, source de l'interaction

        Raises :
                TypeError si other n'est pas un objet Vector
        """
        try:
            r = self.position - other.position
            self.force = -self.mass * other.mass / r.norm() ** 3 * r
        except AttributeError:
            raise TypeError("Tried to compute the force created by "
                            "a non-Particle object")

    ### À implémenter ###
    def update(self, dt):
        """
        Mise à jour de la position et la vitesse au cours du temps.

        Args :
                dt(float): Pas de temps d'intégration.
        """


#############################################
##### Des tests pour la classe Particle #####
#############################################

def test_ParticleInit():
    with pytest.raises(TypeError):
        p = Particle("blabla")
        p = Particle(2, position='hum')  # on vérifie les erreurs sur Vector
        p = Particle([])
    p = Particle(3, Vector(2, 1, 4), Vector(-1, -1, -1))
    assert p.mass == 3
    assert p.position == Vector(2, 1, 4)
    assert p.speed == Vector(-1, -1, -1)
    assert p.force == Vector()


def test_ParticleStr():
    p = Particle(3, Vector(1, 2, 3), Vector(-1, -2, -3))
    assert str(p) == "Particle with mass 3.00, position (1.00,2.00,3.00) " \
        "and speed (-1.00,-2.00,-3.00)"


def test_ParticleForce():
    p = Particle(1, Vector(1, 0, 0))
    p2 = Particle()
    p.computeForce(p2)
    assert p.force == Vector(-1, 0, 0)
    p.position = Vector(2, -3, 6)
    p.mass = 49
    p.computeForce(p2)
    assert p.force == Vector(-2 / 7, 3 / 7, -6 / 7)


def test_ParticleUpdate():
    dt = 0.1
    p = Particle(1, Vector(1, 0, 0), Vector())
    p.computeForce(Particle())
    p.update(dt)
    assert p.speed == Vector(-0.1, 0, 0)
    assert p.position == Vector(0.99, 0, 0)


#######################################################
##### Une classe Ion qui hérite de point matériel #####
#######################################################

class Ion(Particle):
    """
    Un Ion est une particule ayant une charge en plus de sa masse et
    intéragissant électrostatiquement plutôt que gravitationnellement.
    La méthode computeForce remplace donc le calcul de la force
    gravitationnelle de Newton par celui de la force électrostatique de
    Coulomb.
    """

    ### À implémenter ###
    def __init__(self, mass=1, charge=1, position=Vector(), speed=Vector()):
        """
        Le constructeur de la classe Ion.

        Args :
                mass(float): La masse de l'ion (doit être strictement positive)
                charge(float): La charge de l'ion (doit être entière et
                        strictement positive)
                position(Vector): La position initiale de la particule
                speed(Vector): La vitesse initiale de la particule

        Raises :
                ValueError si charge < 0
                TypeError si la masse n'est pas un réel,
                        si la charge n'est pas un entier,
                        si position ou speed ne sont pas des Vector
        """
        raise NotImplementedError("You must implement Ion.__init__")

    ### À implémenter ###
    def __str__(self):
        """
        Surcharge de l'opérateur `str`.

        Returns :
                "Ion with mass m, charge q, position (x,y,z)
                and speed (vx,vy,vz)" avec q entier et le reste à 2 décimales
        """
        raise NotImplementedError("You have to implement Ion.__str__")

    def computeForce(self, other):
        """
        Calcule la force électrostatique de Coulomb exercée par un Ion other
        sur self. Masque la méthode de Particle.

        Args :
                other(Ion): Un autre Ion, source de l'interaction.
        Raises :
                TypeError si other n'est pas un objet Ion
        """
        raise NotImplementedError("You have to implement Ion.computeForce")


#######################################
##### Des test pour la classe Ion #####
#######################################

def test_IonInit():
    with pytest.raises(TypeError):
        ion = Ion("blabla")
        ion = Ion(2, position='hum')  # on vérifie une erreur sur Vector
        ion = Ion(2, 'hum')           # on vérifie une erreur sur la charge
    ion = Ion(2, 3, Vector(2, 1, 4), Vector(-1, -1, -1))
    assert ion.mass == 2
    assert ion.charge == 3
    assert ion.position == Vector(2, 1, 4)
    assert ion.speed == Vector(-1, -1, -1)
    assert ion.force == Vector()


def test_IonStr():
    ion = Ion(3, 2, Vector(1, 2, 3), Vector(-1, -2, -3))
    assert str(ion) == "Ion with mass 3.00, charge 2, " \
        "position (1.00,2.00,3.00) and speed (-1.00,-2.00,-3.00)"


def test_IonForce():
    ion = Ion(mass=1, charge=1, position=Vector(1, 0, 0))
    ion2 = Ion(charge=3)
    ion.computeForce(ion2)
    assert ion.force == Vector(3, 0, 0)
    ion = Ion(charge=49, position=Vector(2, -3, 6))
    ion.computeForce(ion2)
    assert ion.force == Vector(6 / 7, -9 / 7, 18 / 7)


###########################
##### Un main de test #####
###########################

if __name__ == '__main__':

    # On lance tous les tests en bloc pour commencer
    print(" Test functions ".center(50, "*"))
    print("Testing Vector class...", end=' ')
    test_VectorInit()
    test_VectorStr()
    test_VectorEq()
    test_VectorAdd()
    test_VectorSub()
    test_VectorMul()
    test_VectorNorm()
    test_VectorClone()
    print("ok")
    print("Testing Particle class...", end=' ')
    test_ParticleInit()
    test_ParticleStr()
    test_ParticleForce()
    test_ParticleUpdate()
    print("ok")
    print("Testing Ion class...", end=' ')
    test_IonInit()
    test_IonStr()
    test_IonForce()
    print("ok")
    print(" Test end ".center(50, "*"), "\n")

    # Un petit calcul physique
    print(" Physical computations ".center(50, "*"))
    dt = 0.0001

    # Problème à force centrale gravitationnelle, cas circulaire
    ntimesteps = int(10000 * math.pi)  # durée pour parcourir pi
    center = Particle()
    M = Particle(mass=1, position=Vector(1, 0, 0), speed=Vector(0, 1, 0))
    print("** Gravitationnal computation of central-force motion for a {}" \
        .format(str(M)))
    for i in range(ntimesteps):
        M.computeForce(center)
        M.update(dt)
    print("\t => Final system : {}".format(str(M)))

    # problème à force centrale électrostatique, cas rectiligne
    center = Ion()
    M = Ion(charge=4, position=Vector(0, 0, 1), speed=Vector(0, 0, -1))
    print("** Electrostatic computation of central-force motion for a {}" \
        .format(str(M)))
    for i in range(ntimesteps):
        M.computeForce(center)
        M.update(dt)
    print("\t => Final system : {}".format(str(M)))

    print(" Physical computations end ".center(50, "*"))
