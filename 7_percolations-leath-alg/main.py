#!/usr/bin/python3.7

import numpy as np
import matplotlib.pyplot as pl
from copy import copy
import sys
from time import time

sys.setrecursionlimit(10000)


def draw(model):
    for l in model:
        s = ''
        for e in l:
            s += str(e) + ' '
        print(s)


def leath_alg(node, count):
    x = node[0]
    y = node[1]
    node_to_check = node
    queue = []

    if out_list[y][x] == 1:
        count += 1
        out_list[y][x] += 1
    
    for i in range(4):
        if i == 0:
            _x = x + 1
            _y = y
            if _x < l:
                node_to_check = (_x, _y)
        if i == 1:
            _x = x
            _y = y + 1
            if _y < l:
                node_to_check = (_x, _y)
        if i == 2:
            _x = x - 1
            _y = y
            if _x >= 0:
                node_to_check = (_x, _y)
        if i == 3:
            _x = x
            _y = y - 1
            if _y >= 0:
                node_to_check = (_x, _y)
        
        if node_to_check == node or out_list[node_to_check[1]][node_to_check[0]] == 2: continue

        _x = node_to_check[0]
        _y = node_to_check[1]

        if out_list[_y][_x] == 1: 
            count += 1
            queue.append(node_to_check)
            out_list[_y][_x] = 2


    for el in queue:
        count = leath_alg(el, count)

    return count 

def calculate_borders(b):
    borders = copy(b)
    for x in range(l):
        for y in range(l):
            hit = (out_list[y][x] == 2)
            
            if x == 0   and hit:
                borders['left'] += 1
            if y == 0   and hit:
                borders['up']   += 1
            if x == l-1 and hit:
                borders['right'] += 1
            if y == l-1 and hit:
                borders['down'] += 1

    return borders

def percolation(borders):
    count = 0
    for i in borders.values():
        if i > 0:
            count += 1

    return count > 0

def cool():
    lists = []
    for i in range(100):
        out_list = copy(in_list)
        coords = list(np.random.choice(l, size=2))
        count = leath_alg(coords, 0)
        lists.append(np.array(out_list))

    total_out = np.zeros((l,l))

    for _list in lists:
        total_out += _list
    
    return total_out


def z2(p, n):
    count = 0
    size = 0
    for _ in range(n):
        np.random.seed(int( (time()- 1.5*10**9)*10 ))
        global out_list
        out_list = [ [ np.random.choice(2, p=[1-p, p]) for _ in range(l)] for _ in range(l) ]
        cur_size = leath_alg(( int(l/2), int(l/2) ), 0)
        #print(calculate_borders(borders))
        if percolation(calculate_borders(borders)): count += 1
        else: size += cur_size

    avg_size = size / n*1.0
    print(f"count:{count} | n:{n} | avg size:{avg_size}")
    return count / (n*1.0), avg_size, p



l = 100
p = 0.59
in_list = [ [ np.random.choice(2, p=[1-p, p]) for _ in range(l)] for _ in range(l) ]
out_list = copy(in_list)

borders = { 'left'  : 0, 
            'right' : 0,
            'up'    : 0,
            'down'  : 0     }


#print(z2(p, 100))

#out_list = copy(in_list)
#leath_alg(( int(l/2), int(l/2) ), 0)
#pl.imshow(out_list)
#pl.show()

res = []

#for i in range(1, 17):
#    res.append(z2(p + 0.01*i, 25))
#    print(res[-1])

#P = [ i[0] for i in res ]
#S = [ i[1] for i in res ]
#x = [ i[2] for i in res ]

#pl.plot(x, P, 'ro', markersize = 2.4)
#pl.title('P')
#pl.savefig('P.png')
#pl.show()

#pl.plot(x, S, 'ro', markersize = 2.4)
#pl.title('S')
#pl.savefig('S.png')
#pl.show()



#total_out = cool()
#pl.imshow(total_out)
#pl.show()


first = ( int(l/2), int(l/2) )
#print(first)
result = leath_alg(first, 0)
#print(result)
#print(calculate_borders(borders))
#print(borders)

pl.imshow(out_list)
pl.show()

#draw(out_list)