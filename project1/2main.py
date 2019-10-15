#!/usr/bin/python3.7

import matplotlib.pyplot as pl
import random
import numpy as np

count = 16
radius = 0.05

def collision(r1, r2, radius):
    d = ( (r1[0] - r2[0])**2 + (r1[1] - r2[1])**2  )**0.5
    print(d)
    return d < 2 * radius

class Circle:
    def __init__(self, radius, pos):
        self.r = radius
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.v = random.random()

        self.circle = pl.Circle( self.pos, self.r, color=pl.cm.summer(self.v) )

class Plane:
    def __init__(self, n, r):
        self.n = n
        self.r = r
        self.circles = [] #[ Circle(self.r, np.random.rand(2)) for _ in range(self.n) ]
        for _ in range(n): self.add_circle()

    def add_circle(self):
        pos = np.random.rand(2)
        control = False
        while True:
            for c in self.circles:
                control = collision(pos, c.pos, c.r)
                if control: break
            
            if control:
                pos = np.random.rand(2)
            if not control:
                break
            print('Opps, this place is occupied!!')

        self.circles.append( Circle(self.r, pos) )


plane = Plane(count, radius)
fig, ax = pl.subplots()

for c in plane.circles:
    ax.add_artist(c.circle)

pl.show() 