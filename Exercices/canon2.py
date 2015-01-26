#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as N
import scipy.integrate as SI
import matplotlib.pyplot as P

# Quelques valeurs numériques pour un boulet de canon de [36
# livres](http://fr.wikipedia.org/wiki/Canon_de_36_livres):

g = 9.81 # Pesanteur [m/s2]
cx = 0.45 # Coefficient de frottement d'une sphère
rhoAir = 1.2 # Masse volumique de l'air [kg/m3] au niveau de la mer, T=20°C
rad = 0.1748/2 # Rayon du boulet [m]
rho = 6.23e3 # Masse volumique du boulet [kg/m3]
mass = 4./3.*N.pi*rad**3 * rho # Masse du boulet [kg]
alpha = 0.5*cx*rhoAir*N.pi*rad**2 / mass # Coefficient de frottement par unité de masse
print "Masse du boulet: %.2f kg" % mass
print "Coefficient de frottement par unité de masse: %f S.I." % alpha

# Conditions initiales:

v0 = 450. # Vitesse initiale [m/s]
alt = 45. # Inclinaison du canon [deg]
alt *= N.pi/180. # Inclinaison [rad]
z0 = (0.,0.,v0*N.cos(alt),v0*N.sin(alt))

# Temps caractéristique du système

dt = N.sqrt(mass/(g * alpha))
print "Temps caractéristique: %.1f s" % dt
t = N.linspace(0, dt, 200)

def zdot_turb(z, t):
    """Cas turbulent (non linéaire)."""
    
    x,y,vx,vy = z
    alphav = alpha * N.hypot(vx, vy)
    
    return (vx,vy,-alphav*vx,-g-alphav*vy) # dz/dt

# Intégration numérique des équations du mouvement:

zs_turb = SI.odeint(zdot_turb, z0, t, printmessg=True)

ypos = zs_turb[:,1]>=0 # y>0?
print "Avec frottement:"
print "t(y~0) = %.0f s" % t[ypos][-1] # Dernier instant pour lequel y>0
print "x(y~0) = %.0f m" % zs_turb[ypos,0][-1] # Portée du canon
#print "y(y~0) = %.0f m" % zs[ypos,1][-1] # ~0
print "vitesse(y~0): %.0f m/s" % \
      (N.hypot(zs_turb[ypos,2][-1],zs_turb[ypos,3][-1]))

# Cas sans frottement
xs = v0*N.cos(alt) * t
ys = v0*N.sin(alt) * t - g/2 * t**2
print "Sans frottement:"
print "t(y=0) = %.0f s" % (2*v0*N.sin(alt)/g)
print "x(y=0) = %.0f m" % (v0**2*N.sin(2*alt)/g)

fig,ax = P.subplots()

ax.plot(xs[ys>0]/1e3,ys[ys>0]/1e3,
        ls='--', label=u'Sans frottement')
ax.plot(zs_turb[ypos,0]/1e3,zs_turb[ypos,1]/1e3,
        ls='-', label=u'Avec frottement (v²)')

ax.set_xlabel("x [km]")
ax.set_ylabel("y [km]")
ax.set_title("Trajectoire d'un boulet de 36")
ax.legend()

P.show()
