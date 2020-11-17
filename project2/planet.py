import matplotlib.pyplot as pl

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

        self.fig = pl.Circle( self.pos, self.r, color=pl.cm.summer(self.m))
        