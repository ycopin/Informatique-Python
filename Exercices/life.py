import random
import copy
import time


class life:
    def __init__(self,h,w,toric=False):
        """
        create a double list (the game grid) with the wanted size and initialize it with random
        O (dead) and 1 (alive)
        l is the number of lines
        w is the number of columns
        """
    
        self.G=[[random.randint(0,1) for j in range(w)] for i in range(h)]
        self.h=h
        self.w=w
        self.toric=toric

#    for i in range(w):
 #       for j in range(l):
  #          self.G[i][j]=random.randint(0,1)
   # return G

    def get_value(self,x,y):
        """
        This method return the cell state safely.
        Even if the cell is outside the grid
        """
        if (self.toric==True):
    
            if (x<0):
                x+=self.h
            if (y<0):
                y+=self.w
            if((x/self.h)>=1):
                x-=self.h
            if(y/self.w>=1):
                y-=self.w
            v=self.G[x][y]
        else:
            if((x<0) or (y<0) or (x/self.h)>=1 or (y/self.w)>=1):
                v=0
            else:
                v=self.G[x][y]
        return v

    def __repr__(self):
        """
        Convert the list to a visually 
        handy string
        """

        s=""
        D={0:" ",1:"#"}
        j=0
    
        for i in self.G:
            for j in i:
                s+=D[j]
            s+="\n"
        return s
    
    def will_survive(self,x,y):
        """ tell if a cell will be alive at the next game step"""
        s=-self.G[x][y]
        a=self.G[x][y]
        for i in range(-1,2):
            for j in range(-1,2):
                s+=self.get_value(x+i,y+j)

        if s==3:
            a=1
        if s<2 or s>3:
            a=0
        return a

    def update_grid(self):
        """
        make the grid G go a step further into the game
        """
        T=copy.deepcopy(self)
        #On clone le jeu a l'instant t
        #Cela permet de modifier la grille du jeu
        #en gardant toujours la meme reference
        
        for i in range(self.h):
            for j in range(self.w):
                self.G[i][j]=T.will_survive(i,j)
        
if __name__=="__main__":

    #nombre d'iteration
    N=100
    #instanciation du jeu
    L=life(20,60,toric=True)

    #boucle qui itere le jeu et
    #l'affiche dans le terminal
    for i in range(N):
        print L
        print "\n"
        time.sleep(0.1)
        L.update_grid()
        
