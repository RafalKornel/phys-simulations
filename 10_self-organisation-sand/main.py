#!/usr/bin/python3.7

import numpy as np
import matplotlib.pyplot as pl
from scipy.optimize import curve_fit

class Grid:
    def __init__(self, size, critical = 3, random = True):
        self.grid = np.zeros( (size, size) )
        self.size = size
        self.critical = critical
        self.history = []
        self.avalances = []
        self.current_sum = 0
        self.random = random

    
    def iterate(self, i):

        t = np.full( (self.size, self.size), False)
        i1 = 0

        while True:

            if i1%15 == 1:
                pass
                #self.draw(i1, save=True)
            i1 += 1
            to_fall = self.grid > self.critical
            t = t | to_fall
            #print(t)
            a = np.sum(to_fall)
            '''
            if a == 0:
                if i > 1500:
                    self.avalances.append(self.current_sum)
                    self.current_sum = 0
                break
            self.current_sum += a
            '''

            if a == 0:
                break

            for x in range(self.size):
                for y in range(self.size):
                    if to_fall[x, y]:
                        self.fall(x, y)


        self.avalances.append(np.sum(t))
            
        

    
    def fall(self, x, y):
        if x > 0:
            self.grid[x - 1, y] += 1
        if x < self.size - 1:
            self.grid[x + 1, y] += 1
        if y > 0:
            self.grid[x, y - 1] += 1
        if y < self.size - 1:
            self.grid[x, y + 1] += 1
        self.grid[x, y] -= 4

    
    def run1(self, seeds, draw = False, gif = False, drop=True):
        for i in range(seeds):
            if self.random:
                x, y = np.random.choice(self.size, size=2)
            else:
                x = int(self.size/2)
                y = int(self.size/2)
            if drop:
                self.grid[x, y] += 1
            self.iterate(i)
            self.history.append(np.sum(self.grid))

            if draw:
                self.draw()

            if gif and i%5 == 0:
                pass
                #self.draw(i, save=True)

    
    def draw(self, i=0, save=False):
        pl.imshow(self.grid)
        if save:
            pl.savefig(f"gif/{i}.png")
        else:
            pl.show()


def fun(x, a, b):
    return a * x + b

def fun1(x, a, b):
    return np.exp(b) * x ** a




test = Grid(31, critical=3, random=True)
test.run1(5000, draw=False)
pl.plot(test.history)
pl.xlabel("Time [iterations]")
pl.ylabel("Number of seeds on table")
pl.show()

h = np.histogram(test.avalances, bins = 280) 
#print(h)
y = h[0]
x = np.array([ (h[1][i] + h[1][i + 1])/2 + 10e-2 for i in range(len(h[1]) - 1) ])

x = x[y>0]
y = y[y>0]
#print(x)
#print(y)

#print(x)
#print(y)

#print(np.log(x))
#print(np.log(y))

params, cor = curve_fit(fun, np.log(x), np.log(y), p0=[-1, 8])
#params, cor = curve_fit(fun, x, y, p0=[-1, 8])


pl.plot(np.log(x), np.log(y), 'ro', markersize=2.4)
#pl.plot(x, y, 'ro', markersize=2.4)
#pl.yscale('log')
#pl.xscale('log')
pl.plot(np.log(x), fun(np.log(x), *params), linewidth=0.6, label="Fitted parameters")
#pl.plot(x, fun(x, *params), linewidth=0.6, label="Fitted parameters")
pl.xlabel("log of avalance size")
pl.ylabel("log of occurances of given size avalance")
pl.legend()

pl.show()

print(f"Parameter a in relation N = C*S^a is:{params[0]}")

#test.draw()


'''
part2 = Grid(31, critical = 3, random=False)
part2.run1(2, gif=True)
'''

'''
part3 = Grid(201, critical = 3, random=False)
part3.grid = np.full( (part3.size, part3.size), 7 )
part3.run1(2500, gif=True, drop=True)
'''

'''
experiment = Grid(31, critical = 15, random=False)
experiment.run1(2500, gif=True)
'''