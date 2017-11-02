#!/usr/bin/python3
import random
import sys
import math
sys.setrecursionlimit(15000)
class field:
    def __init__(self, w, h, seed = None):
        self.table = [["u" for j in range (h)] for i in range (w)]
        self.w = w
        self.h = h
        self.generate (0, 0)
    
    def generate (self, x, y):
        if 0 <=  x < self.w and 0 <= y < self.h:
            if self.table[x][y] == "u":
                if random.random() > -1 or x == y == 0:
                    self.table[x][y]="X"
                    self.generate(x, y + 1)
                    self.generate(x, y - 1)
                    self.generate(x + 1, y)
                    self.generate(x - 1, y)
                    #for i in range (-1,2):
                    #    for j in range (-1, 2):
                    #        if i!=j:
                    #            self.generate(x+i, y+j)
                else:
                    self.table[x][y] = " "

    def hieght (self):
        return self.h
    def width (self):
        return self.w
    def getTable (self):
        return self.table
    def __str__ (self):
        string = "\n"
        for y in range (self.h):
            for x in range (self.w):
                space = self.table[x][y]
                if space == "u":
                    space = " "
                string = string + space
            string += "\n"
        return string

def eDist (sq1, sq2):
    xDiff = sq1 [0] - sq2 [0]
    yDiff = sq1 [1] -sq2 [1]
    d = xDiff * xDiff + yDiff * yDiff
    return math.sqrt(d)

def mDist (sq1, sq2):
    return (abs(sq1[0] - sq2[0]) + abs(sq1[1] -sq2[1]))
 
def makeGraph (f):
    graph =  {}
    table = f.getTable()
    for y in range (f.hieght()):
        for x in range (f.width()):
            if table[x][y] == "X":
                graph[(x, y)] = []
                for i in [-1, 1]:
                    if 0 <= x + i < f.w and table[x + i] [y] == "X":
                        graph[(x,y)].append((x+i, y))
                    if 0 <= y + i < f.h and table[x] [y+i] == "X":
                        graph[(x,y)].append((x, y + i))
    return graph

def makeDistricts (graph, size):
    districts =set()
    unusable = set()
    for x,y in graph.keys():
        dHelp(graph, size, districts, unusable, set(), x, y)
        unusable.add((x,y))
    return districts

def dHelp (graph, size, districts, unusable, district, x, y):
    if size == 1:
        district.add((x,y))
        districts.add(frozenset(district))
        district.remove((x,y))
    else:
        district.add((x,y))
        for neighbor in graph.get((x, y), []):
            if neighbor not in district and neighbor not in unusable:
                dHelp(graph, size - 1, districts, unusable, district, neighbor[0], neighbor[1])
        district.remove((x, y))

def cost (graph, district):
    def costHelp (center):
        s = 0
        for square in district:
            s += mDist(center, square)
        return s

    return min (map (costHelp, district))
def nameD (district):
    string="d"
    for t in sorted(district):
        string+=str(t[0])+str(t[1])
    return string
def outputGurobi(graph, districts):
    string ="Minimize"
    counter = 0
    out = open("districts.lp", "w")
    for district in districts:
        string += "\n+" + str (cost(graph, district)) + " " +nameD(district)
    out.write(string)
    string = "\nSubject To"
    for square in graph.keys():
        for district in districts:
            if square in district:
                string += "\n+ " +nameD(district)
        string+=" = 1\n"
    #for d in districts:
    #   string+="\n+ d" + str(id(d))
    #string+=" = \n"
    out.write(string)
    string = "Bounds"
    for d in districts:
        string += "\n0 <= "+nameD(d) + " <= 1"
    string += "\nIntegers"
    for d in districts:
        string += "\n"+nameD(d)
    string += "\nend"
    out.write(string)
    out.close()



f = field(10, 10)
g = makeGraph(f)
d = makeDistricts (g, 10) 
#print (f)
#for district in d:
#    print (district, "cost:", cost(g, district))
print (len(d))
outputGurobi(g, d)

#print (g)
#print (d)

#for l in d:
#    print (l)

