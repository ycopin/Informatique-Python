#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as N
import scipy.stats as SS
import matplotlib.pyplot as P

def printStats(x, y):

    assert N.shape(x)==N.shape(y), "Incompatible input arrays"

    print "x: mean=%.2f, variance=%.2f" % (N.mean(x), N.var(x))
    print "y: mean=%.2f, variance=%.2f" % (N.mean(y), N.var(y))
    print "y vs. x: corrcoeff=%.2f" % (SS.pearsonr(x, y)[0])
    # slope, intercept, r_value, p_value, std_err
    a,b,r,p,s = SS.linregress(x,y)
    print "y vs. x: y = %.2f x + %.2f" % (a, b)

def plotStats(ax, x, y, title=''):

    assert N.shape(x)==N.shape(y), "Incompatible input arrays"

    # slope, intercept, r_value, p_value, std_err
    a,b,r,p,s = SS.linregress(x, y)

    # Data + corrcoeff
    ax.plot(x, y, 'bo', label="r = %.2f" % r)

    # Add mean line ± stddev
    m = N.mean(x)
    s = N.std(x, ddof=1)
    ax.axvline(m, color='g', ls='--', label='_') # Mean 
    ax.axvspan(m-s, m+s, color='g', alpha=0.2, label='_') # Std-dev

    m = N.mean(y)
    s = N.std(y, ddof=1)
    ax.axhline(m, color='g', ls='--', label='_') # Mean 
    ax.axhspan(m-s, m+s, color='g', alpha=0.2, label='_') # Std-dev

    # Linear regression
    xx = N.array([0,20])
    yy = a*xx + b
    ax.plot(xx, yy, 'r-', label="y = %.2f x + %.2f" % (a, b)) 

    # Title and labels
    ax.set_title(title)
    if ax.is_last_row():
        ax.set_xlabel("x")
    if ax.is_first_col():
        ax.set_ylabel("y")
    leg = ax.legend(loc='best', fontsize='small')

if __name__=='__main__':

    quartet = N.genfromtxt("anscombe.dat") # Read Anscombe's Quartet

    fig = P.figure()

    for i in range(4):                  # Loop over quartet sets x,y
        ax = fig.add_subplot(2,2,i+1)
        print "Dataset %d " % (i+1) + "="*20
        x,y = quartet[:,2*i:2*i+2].T
        printStats(x, y)                # Print main statistics
        plotStats(ax, x, y, title=str(i+1)) # Plots

    fig.suptitle("Anscombe's Quartet", fontsize='x-large')

    P.show()
