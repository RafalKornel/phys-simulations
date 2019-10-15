#!/usr/bin/python3.7

import matplotlib.pyplot as pl
import numpy as np

x = [ x**3 for x in range(100) ]

pl.hist(x, bins = 'auto', density = True, alpha = 0.75)
pl.show()