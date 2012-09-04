import matplotlib.pyplot as pl
import numpy as np




def iter(x,y,c,niter=100):
    """
    On definit une fonction qui permet d'exploiter la puissance de numpy meshgrid
    Cela permet d'iterer la fonction pour le parametre c sur l'ensemble de la portion du plan complexe etudie.
    On évite ainsi d'écrire de laborieuses boucles for
    """
    i=0
    while(i<niter):
        # le produit complexe n'est pas défini pour une grille
        # on calcule explicitement parties réelle et imaginaire
        xv=x**2-y**2+c.real
        yv=2*x*y+c.imag
        x=xv
        y=yv
        i+=1
    return (x**2+y**2)**0.5


c=complex(0.284,0.0122)
xx,yy=np.meshgrid(np.linspace(1.5,-1.5,1000),np.linspace(1.5,-1.5,1000))
z=iter(xx,yy,c)
pl.imshow(z)
