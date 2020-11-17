import matplotlib.pyplot as pl
from matplotlib.patches import Circle


class Planet:
    def __init__(self, pos, mom, m, r = 0.5):
        self.pos = pos
        self.mom = mom
        self.pos_next = pos
        self.mom_next = mom
        self.m = m
        self.r = r
        self.pos_history = []
        self.vel_history = []
        self.pot = []
        self.kin = []
        self.f = []

        self.fig = Circle( self.pos, radius=self.r) #, color=pl.cm.summer(self.m))
        