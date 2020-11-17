#!/usr/bin/python3.7

import numpy as np
from numba import jit
import matplotlib.pyplot as pl

L = 5
T = 1

@jit(nopython=True)
def sweep(grid, T):
    l = len(grid)
    for _ in range(grid.size):
        x = np.random.randint(l)
        y = np.random.randint(l)

        '''
        s = sum([   grid[(x + 1)%l, y], 
                    grid[x, (y + 1)%l], 
                    grid[(x - 1)%l, y], 
                    grid[x, (y - 1)%l] ]) '''

        _sum = grid[(x + 1)%l, y] + grid[x, (y + 1)%l] + grid[(x - 1)%l, y] + grid[x, (y - 1)%l]
        
        #print(_sum)

        E = 2*grid[x,y]*_sum*1.0
        #print(E)
        if E <= 0:
            grid[x,y] *= -1
        else:
            p0 = np.exp(-E/T)
            p  = np.random.random()

            if p < p0:
                grid[x,y] *= -1

def run():
    n1 = 1500
    n2 = 1500
    m = 0

    for _ in range(n1):
        sweep(grid, T)

    for _ in range(n2):
        sweep(grid, T)
        m += abs(np.sum(grid))/grid.size

    print(f"T:{T} | mag:{m / n2}")
    return m/n2


def m_ons(t):
    return (1 - 1/(np.sinh(2/t)**4))**(1/8)

temps10 = []
mags10 = []
temps20 = []
mags20 = []

L = 10
grid = np.random.choice([-1, 1], size=(L, L))
print(grid)

for i in np.arange(1, 6, 0.75):
    T = i
    mag = run()
    temps10.append(T)
    mags10.append(mag)

L = 50
grid = np.random.choice([-1, 1], size=(L, L))

for i in np.arange(1, 6, 0.5):
    T = i
    mag = run()
    temps20.append(T)
    mags20.append(mag)

pl.plot(temps10, mags10, 'og', markersize=1.6, label=f'L=10')
pl.plot(temps20, mags20, 'or', markersize=1.6, label=f'L=50')

x = np.arange(1, 2.27, 0.05)
pl.plot(x, m_ons(x), linewidth=0.8, label="Dopasowanie Onsagera")

pl.xlabel("Temperatura")
pl.ylabel("Średni moduł magnetyzacji")
pl.legend()
pl.show()