#!/usr/bin/python3.7

from grid import Grid

test = Grid(1001)
test.evolve(10000)

test.draw(show=True)