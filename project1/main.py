#!/usr/bin/python3.7

import random
import matplotlib.pyplot as pl
import numpy as np
from island import Island

coconuts = 15
count = 300
iterations = 100000
interval = 1000

zeros = [] 
test_isl = Island(count, coconuts)
for _ in range(iterations):
    test_isl.evolve()
    if _ % interval == 0:
        zeros.append(test_isl.return_zeros())


pl.hist(test_isl.__repr__(), bins='auto', density=True, alpha=0.75)
pl.xlabel("Liczba kokosów")
pl.ylabel("Procent mieszkańców")

f = lambda x : 1/(1 + coconuts) * np.exp(-x/(coconuts + 0.5))

x = np.arange(80)
pl.plot(x, f(x))
pl.legend(("Dopasowanie modelowe", "Histogram procentu mieszkańców"))
pl.grid(True)
pl.show()

x = [_*interval for _ in range(len(zeros))]
pl.plot(x, zeros)
pl.hlines(f(0)*count, 0, len(zeros)*interval)
pl.xlabel("Iteration")
pl.ylabel("Total number of citizens with 0 coconuts")
pl.legend( ("'Poor' citizens", "p(0)*N"))
pl.grid(True)
pl.show()
