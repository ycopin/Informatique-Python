#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2014-01-08 22:01:23 ycopin>

import random

class Life(object):

    cells = {False:".", True:"#"} # Dead and living cell representations
    
    def __init__(self, h, w, periodic=False):
        """
        Create a 2D-list (the game grid *G*) with the wanted size (*h*
        rows, *w* columns) and initialize it with random booleans
        (dead/alive). The world is periodic if *periodic* is True.
        """
    
        self.h = int(h)
        self.w = int(w)
        assert self.h > 0 and self.w > 0
        # Random initialization of a h×w world
        self.world = [ [ random.choice([True,False])
                         for j in range(self.w) ]
                       for i in range(self.h) ] # h rows of w elements
        self.periodic = periodic

    def get(self,i,j):
        """
        This method returns the state of cell (*i*,*j*) safely, even
        if the (*i*,*j*) is outside the grid.
        """
        
        if self.periodic:
            return self.world[i%self.h][j%self.w] # Periodic conditions
        else:
            if 0<=i<self.h and 0<=j<self.w:       # Inside grid
                return self.world[i][j]
            else:                       # Outside grid
                return False            # There's nobody out there...

    def __str__(self):
        """
        Convert the grid to a visually handy string.
        """

        return '\n'.join([ ''.join([ self.cells[val] for val in row ])
                           for row in self.world ])
    
    def evolve_cell(self,i,j):
        """Tells if cell (*i*,*j*) will survive during game iteration,
        depending on the number of living neighboring cells."""

        alive = self.get(i,j)           # Current cell status
        # Count living cells *around* current one (excluding current one)
        count = sum( self.get(i+ii,j+jj)
                     for ii in [-1,0,1]
                     for jj in [-1,0,1]
                     if (ii,jj)!=(0,0) )

        if count==3:
            # A cell w/ 3 neighbors will either stay alive or resuscitate
            future = True
        elif count<2 or count>3:
            # A cell w/ too few or too many neighbors will die
            future = False
        else:
            # A cell w/ 2 or 3 neighbors will stay as it is (dead or alive)
            future = alive             # Current status

        return future

    def evolve(self):
        """
        Evolve the game grid by one step.
        """

        # Update the grid
        self.world = [ [ self.evolve_cell(i,j)
                         for j in range(self.w) ]
                       for i in range(self.h) ] 
        
if __name__=="__main__":

    import time

    h,w = (20,60)                       # (nrows,ncolumns)
    n = 100                             # Nb of iterations

    life = Life(h, w, periodic=True) # Instantiation (including initialization)

    for i in range(n):                  # Iterations
        print life                      # Print current world
        print "\n"
        time.sleep(0.1)                 # Pause a bit
        life.evolve()                   # Evolve world
        
