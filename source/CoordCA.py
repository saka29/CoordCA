#Main CoordCA Engine
#Can actually simulate CA
import copy
import math

def _range(a, b):
    if a > b:
        yield from range(a, b, -1)
    else:
        yield from range(a, b)
    yield b

class Pattern(set):
    def __init__(self):
        self.last = None  # last-toggled coord
    
    def toggle(self, coord, *, to=None):
        if to is None:
            # if coord in self then remove else add
            self ^= {coord}
        elif to:
            # 'toggle *to* true'
            self.add(coord)
        else:
            # 'toggle *to* false'
            self.discard(coord)
        self.last = coord
    
    def add(self, coord):
        super().add(coord)
        self.last = coord
    
    def discard(self, coord):
        super().discard(coord)
        self.last = coord
    
    def remove(self, coord):
        super().remove(coord)
        self.last = coord
    
    def _generate_intermediate_coords(self, coord):
        # generate intermediates between self.last and coord
        (x0, y0), (x1, y1) = self.last, coord
        slope = 0 if x0 == x1 else (y0 - y1) / (x0 - x1)
        def f(x):
            return slope * (x - x0) + y0
        x, last_y = x0, int(f(x0))
        for x in _range(x0, coord[0]):
            y = int(f(x))
            for intermediate_y in _range(last_y, y):
                yield (x, intermediate_y)
            last_y = y
        for intermediate_y in _range(last_y, coord[1]):
            yield (x, intermediate_y)
        yield coord
    
    def toggleAllFromLast(self, coord, *, to=None):
        for coord in self._generate_intermediate_coords(coord):
            self.toggle(coord, to=to)


class Universe:
    def __init__(self,rule='1FF-1_3_2-3',pattern=set()):
        self.pattern = pattern
        self.rule = Rule(rule)
        self.population = len(self.pattern)


class Rule:
    def __init__(self,ruleStr):
        self.ruleStr = ruleStr
        self.range = int(ruleStr.split('_')[0].split('-')[1])
        self.neighborhood = self.uncompress(ruleStr.split('_')[0].split('-')[0],self.range)
        self.birth = list(map(int,ruleStr.split('_')[1].split('-')))
        self.survival = list(map(int,ruleStr.split('_')[2].split('-')))

    def uncompress(self,r,rang): #Expands hex neighborhood format to tuple format
        r = bin(int(r,16))[3:]
        w = rang*2+1
        r = r[:w*rang+rang]+'o'+r[w*rang+rang:]
        r = [r[i:i + w] for i in range(0, len(r), w)]
        newr = []
        for i in r:
            newr.append(list(i))
        r = newr
        tupler = []
        yc = rang
        xc = rang*-1
        for y in r:
            for x in y:
                if x == '1':
                    tupler.append((xc,yc))
                xc += 1
            yc -= 1
            xc = rang*-1
        return tupler
        
class Simulator:
    def __init__(self,patt,neighborhood,birth,survival): #SLEEPY CODING
        self.neighborhood = neighborhood
        self.birth = birth
        self.survival = survival
        self.cells = patt

    DEF NeedCheckCells(self,cells,neighborhood): #Finds the coordinates of cells that need to be checked when calculating birth. For this reason, there will be no B0.
        needCheck = set()
        ch = 'cool easter egg'
        for c in cells:
            for k in neighborhood:
                ch = tuple(map(sum,zip(c,k)))
                needCheck.add(ch)

        return needCheck

    def countNeighbors(self,coord,neighborhood): #Self-explanatory
        live = self.cells
        neighbors = 0
        for k in neighborhood:
            if tuple(map(sum,zip(coord,k))) in live:
                neighbors += 1

        return neighbors

    def step(self): #oh boy
        live = self.cells
        checkB = self.needCheckCells(live,[tuple(-x for x in y) for y in self.neighborhood])
        birth = self.birth
        survival = self.survival
        new = set() #The next gen

        #Lets do birth first
        
        for c in checkB:
            if self.countNeighbors(c,self.neighborhood) in birth:
                new.add(c)

        #Survival
                
        for c in live:
            if self.countNeighbors(c,self.neighborhood) in survival:
                new.add(c)

        return new

    #Hey, that wasnt so bad!
