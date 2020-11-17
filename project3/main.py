#!/usr/bin/python3.7

from planet import Planet
from world import World
import matplotlib.pyplot as pl

g = 0.01

test = World([], size=16, dt=0.001, temp=0)
test.initialize_world(8)

for i in range(10000):
    test.evolve_leapfrog()
    test.bound_planets()
    test.calculate_temp()
    test.calculate_pressure()
    test.temp_hist.append(test.temp)
    test.press_hist.append(test.press)

    if i % 50 == 0:
        test.draw2(i)
        print(f"temp: {test.temp} \t press: {test.press}")

pl.clf()
pl.cla()
pl.plot(test.temp_hist)
pl.xlabel('Iteration')
pl.ylabel('Temperature')
pl.savefig('temp.png')
pl.clf()
pl.plot(test.press_hist)
pl.xlabel('Iteration')
pl.ylabel('Pressure')
pl.savefig('pressure.png')