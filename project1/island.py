import random
import numpy as np
from citizen import Citizen

class Island:
    def __init__(self, n, c):
        self.citizens = np.array([ Citizen(c) for _ in range(n) ])

    def evolve(self):
        i, j = np.random.choice(self.citizens, 2)
        self.confront(i, j)

    def confront(self, first, other):
        win = random.choice([True, False])

        if win:
            if other.coconuts > 0:
                first.add_coconut()
                other.dec_coconut()
        else:
            if first.coconuts > 0:
                first.dec_coconut()
                other.add_coconut()

    def return_zeros(self):
        result = 0
        for c in self.citizens:
            if c.coconuts == 0:
                result += 1

        return result


    def __repr__(self):
        return [ c.coconuts for c in self.citizens ]