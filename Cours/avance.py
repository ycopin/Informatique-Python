#!/usr/bin/env python3
# coding: utf-8

"""
Fonctionnalités et POO *avancées*.
"""


def add_attrs(**kwargs):
    """
    Decorator adding attributes to a function, e.g.
    ::

      @attrs(source='NIST/IAPWS')
      def func(...):
          ...
    """

    def decorate(f):
        for key, val in kwargs.iteritems():
            setattr(f, key, val)
        return f

    return decorate


def make_method(obj):
    """
    Decorator to make the function a method of `obj` (*monkey patching*), e.g.
    ::

      @make_method(MyClass)
      def func(myClassInstance, ...):
          ...

    makes `func` a method of `MyClass`, so that one can directly use::

      myClassInstance.func()
    """

    def decorate(f):
        setattr(obj, f.__name__, f)
        return f

    return decorate


# Méthodes statique et de classe ==============================

class Date:
    "Source: https://stackoverflow.com/questions/12179271"

    def __init__(self, day=0, month=0, year=0):
        """Initialize from day, month and year values (no verification)."""

        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, astring):
        """Initialize from (verified) 'day-month-year' string."""

        if cls.is_valid_date(astring):
            day, month, year = map(int, astring.split('-'))

            return cls(day, month, year)
        else:
            raise IOError(f"{astring!r} is not a valid date string.")

    @staticmethod
    def is_valid_date(astring):
        """Check validity of 'day-month-year' string."""

        try:
            day, month, year = map(int, astring.split('-'))
        except ValueError:
            return False
        else:
            return (0 < day <= 31) and (0 < month <= 12) and (0 < year <= 2999)


# Définition d'une classe avec attributs semi-privés ==============================

class AnimalPrive:

    def __init__(self, mass):

        self.set_mass(mass)

    def set_mass(self, mass):
        """Setter de l'attribut privé `mass`."""

        if float(mass) < 0:
            raise ValueError("Mass should be a positive float.")

        self._mass = float(mass)

    def get_mass(self):
        """Getter de l'attribut privé `mass`."""

        return self._mass


# Définition d'une classe avec attributs privés ==============================

class AnimalTresPrive:

    def __init__(self, mass):

        self.set_mass(mass)

    def set_mass(self, mass):
        """Setter de l'attribut privé `mass`."""

        if float(mass) < 0:
            raise ValueError("Mass should be a positive float.")

        self.__mass = float(mass)

    def get_mass(self):
        """Getter de l'attribut privé `mass`."""

        return self.__mass


# Définition d'une classe avec propriété ==============================

class AnimalProperty:

    def __init__(self, mass):

        self.mass = mass        # Appelle le setter de la propriété

    @property
    def mass(self):             # Propriété mass (= getter)

        return self._mass

    @mass.setter
    def mass(self, mass):       # Setter de la propriété mass

        if float(mass) < 0:
            raise ValueError("Mass should be a positive float.")

        self._mass = float(mass)


class Interval:

    def __init__(self, minmax):
        """Initialisation à partir d'un 2-tuple."""

        self._range = _, _ = minmax  # Test à la volée

    @property
    def min(self):
        """La propriété min est simplement _range[0]. Elle n'a pas de setter."""

        return self._range[0]

    @property
    def max(self):
        """La propriété max est simplement _range[1]. Elle n'a pas de setter."""

        return self._range[1]

    @property
    def middle(self):
        """La propriété middle est calculée à la volée. Elle n'a pas de setter."""

        return (self.min + self.max) / 2
