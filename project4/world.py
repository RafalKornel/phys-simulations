import numpy as np
import matplotlib.pyplot as pl
from matplotlib.patches import Circle
from planet import Planet

class World:
    def __init__(self, planets, static_objects = [], count = 4, size = 8, G = 0.01, temp = 2.5, temp_ext = 5, k = 1, dt = 0.0001):
        self.G = G
        self.planets = planets
        self.statics = static_objects
        self.dt = dt
        self.count = count
        self.size = size
        self.temp = temp
        self.press = 0
        self.density = self.count**2 / self.size**2
        self.temp_hist = []
        self.press_hist = []
        self.density_hist = []
        self.temp_ext = temp_ext
        self.k = k
        self.eps = 1
        self.sig = 1
        self.def_mass = 1
        self.radius = 2.5 * self.sig
        self.index = int(np.random.uniform(0, self.count**2))
        print(self.index)


    def initialize_world(self):
        wall_len = self.count
        for x in range(wall_len):
            for y in range(wall_len):
                #mom = np.sqrt(self.temp * self.k)
                pos = np.array([x*self.size/wall_len + self.size/(wall_len*2), y*self.size/wall_len + self.size/(wall_len*2)])
                mom = np.random.uniform(-0.5, 0.5, 2)
                self.planets.append(Planet(pos, mom, self.def_mass))

        v_cm = np.array([0., 0.])
        e_kin = 0

        for p in self.planets:
            v_cm += p.mom/p.m
            
        v_cm /= len(self.planets)

        for p in self.planets:
            p.mom -= v_cm * p.m

        for p in self.planets:
            e_kin += np.dot(p.mom, p.mom)/(2 * p.m**2)

        e_kin /= len(self.planets)
        fs = np.sqrt(self.temp/e_kin)

        for p in self.planets:
            p.mom *= fs
 

    def bound_planets(self):
        for p in self.planets:
            p.pos[0] = p.pos[0] % self.size
            p.pos[1] = p.pos[1] % self.size


    def evolve_verlet(self):
        for p in self.planets:
            f = self.calculate_force_gravity(p)

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
        v = []
        for p in self.planets:
            f = self.calculate_force_lennard_jones(p)
            if len(p.vel_history) == 0:
                p.vel_history.append(p.mom/p.m - f*self.dt/(2*p.m))

            v_u = p.vel_history[-1] + f*self.dt/(2*p.m)
            v.append(v_u)
            p.f_tot = f

        self.calculate_temp_v(v)
        
        eta = np.sqrt(self.temp_ext/self.temp)

        for p in self.planets:
            f = p.f_tot

            p.pos_history.append(p.pos)
            p.vel_history.append((2*eta-1)*p.vel_history[-1] + eta*f*self.dt/p.m)

            #kin, pot = self.calculate_energy(p)
            #p.kin.append(kin)
            #p.pot.append(pot)
            
            p.mom_next = p.m*(p.vel_history[-1] + p.vel_history[-2])/2
            p.pos_next = p.pos + p.vel_history[-1]*self.dt

        for p in self.planets:
            p.pos = p.pos_next
            p.mom = p.mom_next


    def calculate_force_gravity(self, planet):
        f = np.array([0., 0.])

        selected = self.select_closest(planet)

        for other in selected:
            if planet is not other:
                d = World.d(other.pos, planet.pos)
                f +=  ( self.G * planet.m * other.m / d**3 )\
                     * (other.pos - planet.pos)

        return f


    def calculate_force_lennard_jones(self, planet):
        f = np.array([0., 0.])
        planet.f = []
        #print(planet)
        selected = self.select_closest(planet)

        for other, d, r in selected:
            a = -48*self.eps/self.sig**2 * ( (self.sig/d)**14 - 0.5*(self.sig/d)**8 )
            temp_f = a * r #(other.pos - planet.pos)
            planet.f.append(np.dot(temp_f, (other.pos - planet.pos)))
            f += temp_f
            #print(f"a:{a}, d:{d}")   

        #print(f)
        return f

    
    def calculate_temp(self):
        avg_energy = 0
        for p in self.planets:
            avg_energy += np.dot(p.mom, p.mom) / 2*p.m

        self.temp = avg_energy / ( len(self.planets) * self.k )
        self.temp_hist.append(self.temp)

    
    def calculate_temp_v(self, v):
        avg_energy = 0
        for i, p in enumerate(self.planets):
            avg_energy += np.dot(v[i], v[i]) / (2*p.m)

        self.temp = avg_energy / ( len(self.planets) * self.k )
        self.temp_hist.append(self.temp)


    def calculate_pressure(self):
        _sum = 0
        n = len(self.planets)
        for p in self.planets:
            _sum += sum(p.f)

        self.press = n*self.k*self.temp/self.size**2 + _sum/n*3*self.size**2
        self.press_hist.append(self.press)


    def calculate_energy(self, p):
        pot = 0
        selected = self.select_closest(p)
        for o in selected:
            if p is not o:
                pot += (-1) * self.G * o.m * p.m / World.d(o.pos, p.pos)
        kin = 0.5 * np.linalg.norm(p.mom) ** 2 / p.m
        return (kin, pot)

    
    def select_closest(self, planet):
        selected = []
        for other in self.planets:
            d, r = self.d_torus(other.pos, planet.pos)
            if d < self.radius and planet is not other:
                selected.append((other, d, r))
        
        #print(selected)
        return selected


    @staticmethod
    def d(r1, r2):
        dist = ( (r1[0] - r2[0])**2 + (r1[1] - r2[1])**2  )**0.5
        return dist

    def d_torus(self, r1, r2):
        if abs(r1[0] - r2[0]) < self.size - abs(r1[0] - r2[0]):
            x = r1[0] - r2[0]
        else:
            s = np.sign(r1[0] - r2[0])
            x = (self.size - (r1[0] - r2[0])) % (self.size * s)

        if abs(r1[1] - r2[1]) < self.size - abs(r1[1] - r2[1]):
            y = r1[1] - r2[1]
        else:
            s = np.sign(r1[1] - r2[1])
            y = (self.size - (r1[1] - r2[1])) % (self.size * s)

        min_x = min( abs(r1[0] - r2[0]), self.size - abs(r1[0] - r2[0]))
        min_y = min( abs(r1[1] - r2[1]), self.size - abs(r1[1] - r2[1]))

        return ( ( min_x**2 + min_y**2 )**0.5, np.array([x, y]) )


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


    def draw2(self, i):
        #for _ in self.planets:
        #    print (_.pos)

        pl.clf()
        F = pl.gcf()
        for j, p in enumerate(self.planets):
            a = pl.gca()
            if j == self.index:
                a.add_patch(Circle(p.pos, radius=p.r, color=pl.cm.summer(255)))  
            else:  
                a.add_patch(Circle(p.pos, radius=p.r))
            pl.plot()
        pl.xlim((0, self.size))
        pl.ylim((0, self.size))
        F.set_size_inches((6,6))
        pl.title(f"t:{self.temp:.4f} | p:{self.density:.3f}")
        i = str(i).rjust(6, '0')
        pl.savefig(f"v1/{i}.png")
    


        # #pl.close()        
        # fig, ax = pl.subplots()

        # ax.set_xlim(left = -self.size, right = self.size)
        # ax.set_ylim(bottom = -self.size, top = self.size)

        # for c in self.planets:
        #     ax.add_artist(c.fig)

        # pl.show() 

    
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

    def evolve_leapfrog_old(self):
        for p in self.planets:
            f = self.calculate_force_lennard_jones(p)

            if len(p.vel_history) == 0:
                p.vel_history.append(p.mom/p.m - f*self.dt/(2*p.m))

            p.pos_history.append(p.pos)
            p.vel_history.append(p.vel_history[-1] + f*self.dt/p.m)

            #kin, pot = self.calculate_energy(p)
            #p.kin.append(kin)
            #p.pot.append(pot)
            
            p.mom_next = p.m*(p.vel_history[-1] + p.vel_history[-2])/2
            p.pos_next = p.pos + p.vel_history[-1]*self.dt

        for p in self.planets:
            p.pos = p.pos_next
            p.mom = p.mom_next