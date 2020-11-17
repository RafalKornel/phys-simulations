import numpy as np
import matplotlib.pyplot as pl
from particle import Particle

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size+1, size+1), dtype=np.int32)
        self.cm_x = int(size/2)
        self.cm_y = int(size/2)
        self.grid[self.cm_x][self.cm_y] = 1
        self.dif = int(self.size/16)
        self.p = 0.0
        self.m = 10
        self.threshold = 1000
        self.r_a = 0
        self.r_in = max(self.r_a + 2, 5)
        self.r_out = self.r_in + int(self.size/4)    #this value should be modified maybe
    

    def start_particle(self):
        theta = np.random.uniform(0, 2*np.pi)

        p = Particle(self.cm_x + int(self.r_in * np.cos(theta)), self.cm_y + int(self.r_in * np.sin(theta)))

        while True:

            is_near_cell = False
            if p.x <= 1 or p.x >= self.size - 2 or p.y <= 1 or p.y >= self.size - 2:
                del p
                break

            dir = -1
            for i in range(0, 4):
                if i == 0: 
                    if self.grid[p.x + 1][p.y    ] == 1: 
                        is_near_cell = True
                        dir = i
                if i == 1: 
                    if self.grid[p.x    ][p.y + 1] == 1: 
                        is_near_cell = True
                        dir = i
                if i == 2: 
                    if self.grid[p.x - 1][p.y    ] == 1: 
                        is_near_cell = True
                        dir = i
                if i == 3: 
                    if self.grid[p.x,   ][p.y - 1] == 1: 
                        is_near_cell = True
                        dir = i


            p.calc_r(self.cm_x, self.cm_y)
            if is_near_cell and np.random.uniform() > self.p: 
                self.grid[p.x][p.y] -= 1
                if self.grid[p.x][p.y] == -self.m:
                    self.grid[p.x][p.y] = 1
                    self.update_r(p.r)
                del p
                break
 
            if p.r >= self.r_out:
                #self.update_r(p.r)
                del p
                break


            directions = [0, 1, 2, 3]
            if dir != -1:
                directions.remove(dir)
            dir = np.random.choice(directions)
            if dir == 0: next = (p.x + 1, p.y    )
            if dir == 1: next = (p.x,     p.y + 1)
            if dir == 2: next = (p.x - 1, p.y    )
            if dir == 3: next = (p.x,     p.y - 1)

            p.x = next[0]
            p.y = next[1]
        #print(self.grid)
            #self.draw()
            #print(self.r_in, self.r_out, self.r_a)

        #for x in range(self.size):
        #    for y in range(self.size):
        #        if self.grid[x][y] == -self.m: self.grid[x][y] = 1

    
    def evolve(self, n):
        for _ in range(n):
            print(_)
            if _ % self.threshold == 0:
                self.draw(_)
            self.start_particle()


    def update_r(self, new):
        self.r_a = max(self.r_a, new)
        self.r_in = max(self.r_a + 2, 5)
        self.r_out = self.r_in + self.dif

    
    def draw(self, i = -1, show=False):
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] != 1:
                    self.grid[x][y] = 0
        pl.ylim((self.cm_y - self.r_a, self.cm_y + self.r_a))
        pl.xlim((self.cm_x - self.r_a, self.cm_x + self.r_a))
        pl.imshow(self.grid)
        pl.savefig(f'{i}_out_p_{self.p}_n_{self.size}.png')
        if show: pl.show()
