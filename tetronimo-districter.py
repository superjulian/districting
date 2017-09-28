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
                if random.random() > .3 or x == y == 0:
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
        for col in self.table:
            for space in col:
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
    return (math.abs(sq1[0] - sq2[0]) + math.abs(sq1[1] -sq2[1]))
 
def makeGraph (f):
    graph =  {}
    table = f.getTable()
    for y in range (f.hieght()):
        for x in range (f.width()):
            if table[y][x] == "X":
                graph[(x, y)] = []
                for i in [-1, 1]:
                    if 0 <= x + i < f.w and table[x + i] [y] == "X":
                        graph[(x,y)].append((x+i, y))
                    if 0 <= y + i < f.h and table[x] [y+i] == "X":
                        graph[(x,y)].append((x, y + i))
    return graph



f = field(10, 10)
print (sorted(list(makeGraph(f).items())))

print (f)
