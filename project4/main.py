#!/usr/bin/python3.7

from planet import Planet
from world import World
import matplotlib.pyplot as pl

g = 0.01

test = World([], count=4,  size=8, dt=0.001, temp_ext=0.9, temp = 0.9)
test.initialize_world()

for i in range(20000):
    test.evolve_leapfrog()
    test.bound_planets()
    #test.calculate_temp()
    #test.calculate_pressure()

    if i % 100 == 0:
        test.draw2(i)
        print(f"temp: {test.temp} \t press: {test.press} \t density: {test.density}")

pl.clf()
pl.cla()
pl.plot(test.press_hist)
pl.xlabel('Iteration')
pl.ylabel('Pressure')
pl.savefig('press.png')

pl.clf()
pl.cla()
pl.plot(test.temp_hist)
pl.xlabel('Iteration')
pl.ylabel('Temperature')
pl.savefig('temp.png')