#!/usr/bin/env python


class AbstractBuddy(object):

    genre = None

    def __init__(self, name):
        self.name = name
        if self.genre is None:
            raise TypeError("'%s' should not be instanciated directly" %
                            self.__class__.__name__)

    def __str__(self):
        return "%s: %s (%s)" % \
               (self.__class__.__name__, self.name, self.genre)


def friendFactory(genre=None):

    class Friend(AbstractBuddy):
        pass

    Friend.genre = genre
    if genre == 'male':
        Friend.__name__ = 'Boyfriend'
    elif genre == 'female':
        Friend.__name__ = 'Girlfriend'
    else:
        Friend.__name__ = 'Pet'

    return Friend

if __name__ == '__main__':

    calvin = friendFactory('male')('Calvin')
    susie = friendFactory('female')('Susie')
    hobbes = friendFactory('tiger')('Hobbes')

    print calvin
    print susie
    print hobbes
