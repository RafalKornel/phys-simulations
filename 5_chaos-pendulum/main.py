#!/usr/bin/python3.7

from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as pl
import os


def eq(y, t, a = 1, b = 1, c = 0.2, f = 0.2, ve = 0.2):
    x, v = y
    dydt = [v,  b*x - a*x**3 - c*v + f*np.cos(2*np.pi*ve*t)]
    return dydt


def pot(x, t, a, b, f, ve):
    return 0.5*b*x**2 - 0.25*a*x**4 + f * x * np.cos(np.pi*2*ve*t)

a = 1
b = 1
c = 0.2
f = 0.3
ve = 0.2
t_range = 1000

y0 = [0, 0.08]
t = np.arange(0, t_range, 0.1)

sol = odeint(eq, y0, t, args=(a, b, c, f, ve), rtol=1e-4, atol=1e-4)

d = f"out_f{f}_a{a}_b{b}_c{c}_ve{ve}"
try:    os.mkdir(f'out/{d}')
except: pass

points = False
if points:
    control = 'go'
else:
    control = 'g'

snap = 5

def plot3():
    a = 1
    b = 1
    c = 0.2
    ve = 0.2
    t_range = 1000
    for f in np.arange(0.1, 0.3, 0.005):
        #print(f)
        sol = odeint(eq, y0, t, args=(a, b, c, f, ve), rtol=1e-4, atol=1e-4)
        sol = sol [t > 200]
        pl.plot(sol[:, 0], sol[:, 1], control, markersize=0.6, linewidth=0.8, label=['x', 'dx/dt'])
        pl.title(f'f:{f:.4f}')
        pl.xlabel("x")
        pl.ylabel("dx/dt")
        f = f * 1000
        pl.savefig(f"ekstra/phase/{int(f)}.png")
        pl.clf()


def plot2():
    for i, y in enumerate(sol[:, 0]):
        if i % snap == 0:
            pl.plot(y, pot(y, t[i], a, b, f, ve), 'go', markersize=1.5, linewidth=0.8, label="Solution")
            x = np.arange(min(-2, min(sol[:,0])), max(2, max(sol[:,0])), 0.05)
            pl.plot(x, pot(x, t[i], a, b, f, ve), 'r', linewidth=0.8, label="Potential")
            pl.gca().invert_yaxis()
            pl.xlabel("x")
            pl.legend()
            i = str(i).rjust(6, '0')
            pl.savefig(f"ekstra/pot/{i}.png")
            pl.clf()


def plot1():
    pl.plot(sol[:, 0], sol[:, 1], control, markersize=0.6, linewidth=0.8, label=['x', 'dx/dt'])
    pl.title(f'a:{a} b:{b} c:{c} f:{f} ve:{ve}')
    pl.xlabel("x")
    pl.ylabel("dx/dt")
    pl.savefig(f"out/{d}/phase.png")
    pl.clf()


    pl.plot(t, sol[:, 0], 'r', linewidth=0.4)
    pl.xlabel('t')
    pl.ylabel('x')
    pl.savefig(f"out/{d}/trajectory.png")
    pl.clf()


    pl.plot(sol[:, 0], pot(sol[:, 0], a, b), 'go', markersize=0.6, linewidth=0.8, label="Solution")
    x = np.arange(min(-2, min(sol[:,0])), max(2, max(sol[:,0])), 0.05)
    pl.plot(x, pot(x, a, b), 'r', linewidth=0.8, label="Potential")
    pl.gca().invert_yaxis()
    pl.xlabel("x")
    pl.legend()
    pl.savefig(f"out/{d}/pot.png")
    pl.clf()


    sol = sol[t > 200]
    pl.plot(sol[:, 0], sol[:, 1], control, markersize=0.6, linewidth=0.8, label=['x', 'dx/dt'])
    pl.title(f'a:{a} b:{b} c:{c} f:{f} ve:{ve}')
    pl.xlabel("x")
    pl.ylabel("dx/dt")
    pl.title("Solution with t > 200")
    pl.savefig(f"out/{d}/phase_after_200.png")



plot3()
