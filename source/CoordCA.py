#Main CoordCA Engine
#Can actually simulate CA
import copy

class Pattern(set):
    def toggle(self, coord):
        # if coord in self then remove else add
        self ^= {coord}


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

    def needCheckCells(self,cells,neighborhood): #Finds the coordinates of cells that need to be checked when calculating birth. For this reason, there will be no B0.
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
        checkB = self.needCheckCells(live,[tuple(x*-1 for x in y) for y in self.neighborhood])
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
