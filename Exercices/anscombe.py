#!/usr/bin/env python3
# coding: utf-8

import numpy as N
import scipy.stats as SS
import matplotlib.pyplot as P


def printStats(x, y):
    """
    Print out means and variances for x and y, as well as correlation
    coeff. (Pearson) and linear regression for y vs. x.
    """

    assert N.shape(x) == N.shape(y), "Incompatible input arrays"

    print(f"x: mean={N.mean(x):.2f}, variance={N.var(x):.2f}")
    print(f"y: mean={N.mean(y):.2f}, variance={N.var(y):.2f}")
    print(f"y vs. x: corrcoeff={SS.pearsonr(x, y)[0]:.2f}")
    # slope, intercept, r_value, p_value, std_err
    a, b, _, _, _ = SS.linregress(x, y)
    print(f"y vs. x: y = {a:.2f} x + {b:.2f}")


def plotStats(ax, x, y, title='', fancy=True):
    """
    Plot y vs. x, and linear regression.
    """

    assert N.shape(x) == N.shape(y), "Incompatible input arrays"

    # slope, intercept, r_value, p_value, std_err
    a, b, r, _, _ = SS.linregress(x, y)

    # Data + corrcoeff
    ax.plot(x, y, 'bo', label=f"r = {r:.2f}")

    # Linear regression
    xx = N.array([0, 20])
    yy = a * xx + b
    ax.plot(xx, yy, 'r-', label=f"y = {a:.2f} x + {b:.2f}")

    leg = ax.legend(loc='upper left', fontsize='small')

    if fancy:                   # Additional stuff
        # Add mean line ± stddev
        m = N.mean(x)
        s = N.std(x, ddof=1)
        ax.axvline(m, color='g', ls='--', label='_')    # Mean
        ax.axvspan(m - s, m + s, color='g', alpha=0.2)  # Std-dev

        m = N.mean(y)
        s = N.std(y, ddof=1)
        ax.axhline(m, color='g', ls='--', label='_')    # Mean
        ax.axhspan(m - s, m + s, color='g', alpha=0.2)  # Std-dev

        # Title and labels
        if title:
            ax.set_title(title)
        if ax.is_last_row():
            ax.set_xlabel("x")
        if ax.is_first_col():
            ax.set_ylabel("y")


if __name__ == '__main__':

    quartet = N.genfromtxt("anscombe.dat")  # Read Anscombe's Quartet

    fig = P.figure()

    for i in range(4):                  # Loop over quartet sets x,y
        ax = fig.add_subplot(2, 2, i + 1)
        print(f" Dataset #{i+1} ".center(40, '='))
        x, y = quartet[:, 2 * i:2 * i + 2].T
        printStats(x, y)                # Print main statistics
        plotStats(ax, x, y, title='#'+str(i + 1))  # Plots

    fig.suptitle("Anscombe's Quartet", fontsize='x-large')
    fig.tight_layout()

    P.show()
