#!/usr/bin/python3.7

import numpy as np
from world import World
from planet import Planet

g = 1
dt = 0.001

planets = [Planet(np.array([0.97000436,-0.24308753]), -0.5*np.array([0.93240737,0.86473146]), 1), \
         Planet(np.array([-0.97000436,0.24308753]), -0.5*np.array([0.93240737,0.86473146]), 1), \
         Planet(np.array([0., 0.]), np.array([0.93240737,0.86473146]), 1)]
statics = []

# planets = [Planet(np.array([2., 0.]), np.array([0., 0.1]), 0.1), \
#           Planet(np.array([-3., 0.]), np.array([0., -0.1]), 0.2), \
#           Planet(np.array([1., 2.]), np.array([-0.12, 0.]), 0.15), \
#           Planet(np.array([3., -3.]), np.array([0.2, -0.1]), 0.3)]
# statics = [Planet(np.array([0.6, 1.3]), np.array([0., 0.2]), 500, static = True)]

#planets = [Planet(np.array([2., 0.]), np.array([0., 0.1]), 0.1)]
#statics = [Planet(np.array([0., 0.]), np.array([0., 0]), 500.0, static = True)]


test_euler = World(g, planets, statics, dt)
test_verlet = World(g, planets, statics, dt)
test_leapfrog = World(g, planets, statics, dt)

#for _ in range(100000):
#    test_euler.evolve_euler()
#test_euler.draw()    

#for _ in range(10000):
#    test_verlet.evolve_verlet()
#test_verlet.draw()

for _ in range(10000):
    test_leapfrog.evolve_leapfrog()
test_leapfrog.draw()

