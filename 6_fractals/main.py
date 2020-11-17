#!/usr/bin/python3.7

import numpy as np
import matplotlib.pyplot as pl

''' 
#PAPROTKA
prop = [0.73, 0.13, 0.11, 0.03]
coeffs = [  [ 0.85, 0.04,-0.04, 0.85, 0.0, 1.6], 
            [  0.2,-0.26, 0.23, 0.22, 0.0, 1.6], 
            [-0.15, 0.28, 0.26, 0.24, 0.0, 0.44],
            [0.001,  0.0,  0.0, 0.16, 0.0, 0.0] ]
'''


 
#SMOK
prop = [0.787473, 0.212527]
coeffs = [  [0.824074, 0.281482, -0.212346,  0.864198, -1.882290,-0.110607],
            [0.088272, 0.520988, -0.463889, -0.377778,  0.785360, 8.095795] ]


''' 
#KRZYWA LEVIEGO
prop = [0.5, 0.5]
coeffs = [  [0.5, -0.5, 0.5, 0.5, 0.0, 0.0], 
            [0.5, 0.5, -0.5, 0.5, 0.5, 0.5]]
'''


def step(x_0, y_0):
    i = np.random.choice(len(prop), p=prop)
    c = coeffs[i]

    cur_x = c[0]*x_0 + c[1]*y_0 + c[4]
    cur_y = c[2]*x_0 + c[3]*y_0 + c[5]

    return cur_x, cur_y

def cycle(N, draw=False):
    x = [0]
    y = [0]

    cur_x = 0
    cur_y = 0

    for i in range(N):
        cur_x, cur_y = step(cur_x, cur_y)

        x.append(cur_x)
        y.append(cur_y)

    if draw:
        pl.plot(x, y, 'og', markersize=0.5)
        pl.gca().set_facecolor('black')
        pl.show()

    return x, y    
    
N = 100000
r_max = 8

x1, y1 = cycle(N, draw=True)
x2, y2 = cycle(int(N/4))

def calc_N(r, x, y):
    H, xaux, yaux = np.histogram2d(x, y, 2**r)
    Nr = np.sum(H>0)
    print(Nr, r)
    return Nr

a = []
Na1 = []
Na2 = []

for r in range(1, r_max):
    a.append(r)
    Na1.append(calc_N(r, x1, y1))
    Na2.append(calc_N(r, x2, y2))


pl.plot(a, np.log(Na1), 'b', label='N iterations', linewidth=0.6)
pl.plot(a, np.log(Na2), 'g', label='N/4 iterations', linewidth=0.6)
pl.xlabel("r")
pl.ylabel("log(Nr)")
pl.title(f"Zależność log(Nr) od r, dla N = {N}")
pl.legend()
pl.show()