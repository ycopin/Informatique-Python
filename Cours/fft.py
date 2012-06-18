#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as N
from matplotlib import pyplot as P

x = N.linspace(-2*N.pi,2*N.pi,2048)

s = N.sinc(x)

y = N.zeros_like(x)
y[N.abs(x)<=1] = 1    # y est la fonction porte: +1 entre ±1, 0 ailleurs

z = N.fft.fft(s)      # Transformée de Fourier (repliée)
z = N.fft.fftshift(z) # TF (dépliée)

f = N.fft.fftfreq(len(x), d=1/(2*N.pi))
f = N.fft.fftshift(f)
