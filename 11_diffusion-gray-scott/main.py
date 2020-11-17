#!/usr/bin/python3.7

import numpy as np
import matplotlib.pyplot as pl

def evolve(u, v, Du, Dv, F, k):
    u_next = Du*(np.roll(u, 1) + np.roll(u, -1) -2 * u)/(0.02)**2 - u * v * v + F*(np.ones(N) - u) + u
    v_next = Dv*(np.roll(v, 1) + np.roll(v, -1) -2 * v)/(0.02)**2 + u * v * v - (F + k) * v + v

    return u_next, v_next


def forceAspect(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)


N = 100
x = np.linspace(0, 2, N)
u = np.ones(N)
v = np.zeros(N)
xs = np.arange(N)
for i in range(int(N/4), int(3*N/4)):
    u[i] = np.random.random() * 0.2 + 0.4
    v[i] = np.random.random() * 0.2 + 0.2

Du = 2e-5
Dv = 1e-5
F = 0.025
k = 0.055

u_hist = [u]
v_hist = [v]

for i in range(1500):
    u, v = evolve(u, v, Du, Dv, F, k)

    u_hist.append(u)
    v_hist.append(v)

    #if i % 5 == 0:
    #    pl.plot(x, u)
    #    pl.plot(x, v)
    #    pl.show()

#pl.plot(np.arange(len(u_hist)), u_hist)
#pl.show()


fig = pl.figure()
ax = fig.add_subplot(111)
ax.imshow(np.array(u_hist))
ax.set_xlabel('xlabel')
forceAspect(ax,aspect=1)
pl.show()


fig = pl.figure()
ax = fig.add_subplot(111)
ax.imshow(np.array(v_hist))
ax.set_xlabel('xlabel')
forceAspect(ax,aspect=1)
pl.show()