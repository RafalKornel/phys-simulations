import numpy as np
import matplotlib.pyplot as pl

class World:
    def __init__(self, G, planets, static_objects, dt):
        self.G = G
        self.planets = planets
        self.statics = static_objects
        self.dt = dt
        self.size = 4


    def evolve_euler(self):
        for p in self.planets:
            f = self.calculate_force(p)

            p.pos_history.append(p.pos)

            kin, pot = self.calculate_energy(p)
            p.kin.append(kin)
            p.pot.append(pot)
            
            p.pos_next = p.pos + p.mom * self.dt/p.m + 1/(2*p.m) * f * (self.dt**2)
            p.mom_next = p.mom + f * self.dt

        for p in self.planets:
            p.pos = p.pos_next
            p.mom = p.mom_next


    def evolve_verlet(self):
        for p in self.planets:
            f = self.calculate_force(p)

            if len(p.pos_history) == 0:
                pos_prev = p.pos - p.mom * self.dt/p.m
                p.pos_history.append(pos_prev)

            p.pos_history.append(p.pos)

            kin, pot = self.calculate_energy(p)
            p.kin.append(kin)
            p.pot.append(pot)

            p.pos_next = 2*p.pos_history[-1] - p.pos_history[-2] + f*(self.dt)**2/p.m
            p.mom_next = p.m/(2*self.dt) * (p.pos - p.pos_history[-2])

        for p in self.planets:
            p.pos = p.pos_next
            p.mom = p.mom_next


    def evolve_leapfrog(self):
        for p in self.planets:
            f = self.calculate_force(p)

            if len(p.vel_history) == 0:
                p.vel_history.append(p.mom/p.m - f*self.dt/(2*p.m))

            p.pos_history.append(p.pos)
            p.vel_history.append(p.vel_history[-1] + f*self.dt/p.m)

            kin, pot = self.calculate_energy(p)
            p.kin.append(kin)
            p.pot.append(pot)
            
            p.mom_next = p.m*(p.vel_history[-1] + p.vel_history[-2])/2
            p.pos_next = p.pos + p.vel_history[-1]*self.dt

        for p in self.planets:
            p.pos = p.pos_next
            p.mom = p.mom_next


    def calculate_force(self, planet):
        f = np.array([0., 0.])

        for other in self.planets + self.statics:
            if planet is not other:
                d = World.d(other.pos, planet.pos)
                f +=  ( self.G * planet.m * other.m / d**3 )\
                     * (other.pos - planet.pos)

        return f


    def calculate_energy(self, p):
        pot = 0
        for o in self.planets + self.statics:
            if p is not o:
                pot += (-1) * self.G * o.m * p.m / World.d(o.pos, p.pos)
        kin = 0.5 * np.linalg.norm(p.mom) ** 2 / p.m
        return (kin, pot)


    @staticmethod
    def d(r1, r2):
        dist = ( (r1[0] - r2[0])**2 + (r1[1] - r2[1])**2  )**0.5
        return dist


    def draw(self):
        pl.figure()
        pl.clf()
        f = pl.gcf()
        a = pl.gca()
        if len(self.statics) != 0:
            a.add_patch(self.statics[0].fig)
        pl.xlim((-self.size, self.size))
        pl.ylim((-self.size, self.size))
        
        kin = []
        pot = []
        for planet in self.planets:
            x   = [ p[0] for p in planet.pos_history ]
            y   = [ p[1] for p in planet.pos_history ] 
            kin += [ k for k in planet.kin ]
            pot += [ p for p in planet.pot ]
            pl.plot(x, y)
    
        pl.show()

        pl.clf()

        tot = [ a[0] + a[1] for a in zip(kin, pot)]

        pl.plot(np.arange(len(pot)), pot)
        pl.plot(np.arange(len(kin)), kin)
        pl.plot(np.arange(len(tot)), tot)
        pl.xlabel("Iteration")
        pl.ylabel("Energy")
        pl.legend( ("Potential", "Kinetic", "Total") )
        pl.show()

        pl.close()
        
    
    def draw1(self, n):
        pl.clf()
        f = pl.gcf()
        a = pl.gca()
        #a.add_patch(o.fig)
        #fig, ax = pl.subplots()

        pl.xlim((-20, 20))
        pl.ylim((-20, 20))
        
        for o in self.planets + self.statics:
            a.add_patch(o.fig)
            #ax.add_patch(o.fig)
            #ax.add_artist(o.fig)
        pl.plot()

        #pl.savefig("img" + str(n) + ".png")
        pl.show()
        pl.clf()