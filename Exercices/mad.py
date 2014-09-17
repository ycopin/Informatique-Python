#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as N

def mad(a, axis=None):
    """
    Compute *Median Absolute Deviation* of an array along given axis.
    """

    med = N.median(a, axis=axis)                # Median along given axis
    if axis is None:
        umed = med                              # med is a scalar
    else:
        umed = N.expand_dims(med, axis)         # Bring back the vanished axis
    mad = N.median(N.absolute(a - umed), axis=axis) # MAD along given axis

    return mad

if __name__=='__main__':

    x = N.arange(5*7, dtype=float).reshape(5,7)

    print "x =\n", x
    print "MAD(x, axis=None) =", mad(x)
    print "MAD(x, axis=0)    =", mad(x, axis=0)
    print "MAD(x, axis=1)    =", mad(x, axis=1)
