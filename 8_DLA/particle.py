import numpy as np

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 0 #int(np.sqrt(x**2 + y**2))

    def calc_r(self, cm_x, cm_y):
        self.r = int(np.sqrt((self.x-cm_x)**2 + (self.y-cm_y)**2))
        return self.r