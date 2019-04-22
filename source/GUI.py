import tkinter as tk
import tkinter.filedialog
import CoordCA as cca
import math as m
import random as r
import copy
import pathlib
import re

gens = 0
viewx = 0
viewy = 0
auto = 0
mode = 0 #0: Draw, 1: Move, 2: Select, 3: Paste
mouseX = 0
mouseY = 0
lines = 1
viewStartX = 0
viewStartY = 0
mouseNonB1X = 0
mouseNonB1Y = 0
selC1 = ()
selC2 = ()
cSize = 10
b1 = 0
paste = 0
dragStart = None
initPatt = []
filePath = str(pathlib.Path(__file__).parent)
fillPercent = 50

def foo(): #Debug function
    print(display.Viewer.pattern)

########################
# Welcome to FuncWorld #
# (Define functions    #
########################

#View functions
def moveUp(event=None,amount=1):
    global viewy
    viewy += amount

def moveDown(event=None,amount=1):
    global viewy
    viewy -= amount

def moveLeft(event=None,amount=1):
    global viewx
    viewx += amount

def moveRight(event=None,amount=1):
    global viewx
    viewx -= amount

#Step
def step(event=None,a=1):
    global auto
    global gens
    if a:
        auto = 0
    display.Viewer.step()
    gens += 1

#Reset
def resetPatt(event=None):
    global gens
    global auto
    gens = 0
    auto = 0
    display.Viewer.pattern = initPatt

#Mousepos
def mousePos(event):
    global mouseX
    global mouseY
    mouseX,mouseY=event.x, event.y

#Mouse drag handling
def mouseDrag(event):
    global mouseNonB1X
    global mouseNonB1Y
    global viewx
    global viewy
    global viewStartX
    global viewStartY
    global selC1
    global selC2
    global dragStart
    appPosX = m.floor(mouseX/cSize)
    appPosY = m.floor(mouseY/cSize)
    if dragStart is None:
        dragStart = (appPosX-viewx,appPosY-viewy) not in display.Viewer.pattern
    if event.type=='4':
        mouseNonB1X,mouseNonB1Y = round(event.x/cSize),round(event.y/cSize)
        viewStartX = viewx
        viewStartY = viewy
    if event.type=='6':
        mousePos(event)
        x,y=round(event.x/cSize), round(event.y/cSize)
        if mode==0:
            display.Viewer.pattern.toggleAllFromLast((appPosX-viewx,appPosY-viewy), to=dragStart)
        elif mode==1:
            viewx = viewStartX+x-mouseNonB1X
            viewy = viewStartY+y-mouseNonB1Y
        elif mode==2:
            selC2 = (x*cSize-(viewx*cSize),y*cSize-(viewy*cSize))

def dragOff(event):
    global dragStart
    dragStart = None

#Toggle whatever
def toggleAuto(event=None):
    global auto
    auto = not auto

def toggleLines():
    global lines
    lines = not lines

def autoYes():
    global auto
    auto = 1

def autoNo():
    global auto
    auto = 0

#Clear
def clear(event = None):
    global auto
    global gens
    global viewx
    global viewy
    global cSize
    global selC1
    global selC2
    display.Viewer.pattern = cca.Pattern()
    auto = 0
    gens = 0
    viewx = 0
    viewy = 0
    cSize = 10
    selC1 = ()
    selC2 = ()

#Modes
def drawMode():
    global mode
    mode = 0
    display.Viewer.grid.config(cursor='pencil')

def moveMode():
    global mode
    mode = 1
    display.Viewer.grid.config(cursor='fleur')

def selectMode():
    global mode
    mode = 2
    display.Viewer.grid.config(cursor='tcross')

#Zoom
def zoomIn():
    global cSize
    global selC1
    global selC2
    global auto
    cSize += 1
    selC1 = ()
    selC2 = ()
    auto = 0

def zoomOut():
    global cSize
    global selC1
    global selC2
    global auto
    if cSize > 1:
        cSize -= 1
    selC1 = ()
    selC2 = ()
    auto = 0

def center(event=None):
    global viewy
    viewy = 0
    global viewx
    viewx = 0

def mouseZoom(event):
    delt = event.delta
    if delt > 0:
        zoomIn()
    if delt < 0:
        zoomOut()

def refreshMouse():
    global mouseX
    global mouseY
    mouseX = 0
    mouseY = 0

#Menu buttons
def getNewRule():
    drawMode()
    r = ruleMenu()

def openPatt():
    drawMode()
    r = pattMenu()

def savePatt():
    drawMode()
    r = saveMenu()

def goto():
    drawMode()
    r = gotoMenu()

def setColors():
    drawMode()
    r = colorMenu()

def about():
    drawMode()
    r = aboutMenu()

def credit():
    drawMode()
    r = creditsMenu()

def testRule(rule):
    patt = re.compile('[0-9A-F]+-\d+_(?:\d+-)*\d+_(?:\d+-)*\d+')
    return patt.match(rule)

def getNeighborsList():
    root.clipboard_clear()
    root.clipboard_append(str(display.Viewer.universe.rule.neighborhood))

def genTable():
    neigh = str([(0,0)]+display.Viewer.universe.rule.neighborhood+[(0,0)])
    ncells = len(display.Viewer.universe.rule.neighborhood)
    birth = display.Viewer.universe.rule.birth
    surv = display.Viewer.universe.rule.survival
    table ='''n_states:2
neighborhood:'''+neigh+'''
symmetries:permute'''
    #Make birth transitions
    for i in birth:
        bline = '0,'
        for k in range(i):
            bline += '1,'
        for k in range(ncells-i):
            bline += '0,'
        bline += '1'
        table += '\n'+bline
    for i in range(0,ncells+1):
        sline = '1,'
        for k in range(i):
            sline += '1,'
        for k in range(ncells-i):
            sline += '0,'
        sline += '0'
        if i not in surv:
            table += '\n'+sline
    file = tk.filedialog.asksaveasfilename(initialdir=filePath+'/',
                                            title="Save APGtable as...",
                                            filetypes=[("Table File","*.table"),("All","*.*")],
                                            defaultextension=".table")
    opfile = open(file,'w+')
    opfile.write(table)

def copy(event=None):
    if selC2 and event != None:
        patt = getSelectedPatt()
    else:
        patt = display.Viewer.pattern
    cl = [x for t in patt for x in t]
    rle = giveRLE(cl)
    root.clipboard_clear()
    root.clipboard_append(rle)

def copyCoords():
    patt = display.Viewer.pattern
    root.clipboard_clear()
    root.clipboard_append(patt)

def isWithin(c,c1,c2): #Is c (coord) within coords c1 and c2 (Inclusive)?
    return (c1[0]<=c[0]<=c2[0])and(c1[1]<=c[1]<=c2[1])

def getSelectedPatt():
    global selC1
    global selC2
    global cSize
    patt = display.Viewer.pattern
    selpat = [c for c in patt if isWithin(tuple(cSize*x for x in c),selC1,tuple(x-1 for x in selC2))]
    return selpat

def clearSelection(event=None):
    selpat = getSelectedPatt()
    for c in selpat:
        display.Viewer.pattern.remove(c)

def unSel():
    global selC1
    global selC2
    selC1 = ()
    selC2 = ()
    
def randFill(event=None):
    rX = [c for c in range(int(selC1[0]/cSize),int(selC2[0]/cSize))]
    if not rX:
        rX = [c for c in range(int(selC2[0]/cSize),int(selC1[0]/cSize))]

    rY = [c for c in range(int(selC1[1]/cSize),int(selC2[1]/cSize))]
    if not rY:
        rY = [c for c in range(int(selC2[1]/cSize),int(selC1[1]/cSize))]
    a = [(x,y) for x in rX for y in rY]
    fill = [c for c in a if r.randrange(100) < fillPercent]
    clearSelection()
    display.Viewer.pattern.update(fill)

def fillPercentm():
    drawMode()
    r = fillMenu()
    
def rle2coords(rle):
    n = ''
    e = ''
    x = 0
    y = 0
    r = cca.Pattern()
    for c in rle:
        if c.isdigit():
            n += c
        else:
            if n=='':
                n = 1
            e += c*int(n)
            n = ''
    for c in e:
        if c=='o' or c=='b':
            if c=='o':
                r.add((x,y))
            x += 1
        elif c=='$':
            y += 1
            x = 0
    return r

# Python function to convert a cell list to RLE
# Author: Nathaniel Johnston (nathaniel@nathanieljohnston.com), June 2009.
#           DMG: Refactored slightly so that the function input is a simple cell list.
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def giveRLE(clist):
    clist_chunks = list(chunks(clist, 2))
    clist_chunks.sort(key=lambda l:(l[1], l[0]))
    mcc = min(clist_chunks)
    rl_list = [[x[0]-mcc[0],x[1]-mcc[1]] for x in clist_chunks]
    rle_res = ""
    rle_len = 1
    rl_y = rl_list[0][1] - 1
    rl_x = 0
    for rl_i in rl_list:
        if rl_i[1] == rl_y:
            if rl_i[0] == rl_x + 1:
                rle_len += 1
            else:
                if rle_len == 1: rle_strA = ""
                else: rle_strA = str (rle_len)
                if rl_i[0] - rl_x - 1 == 1: rle_strB = ""
                else: rle_strB = str (rl_i[0] - rl_x - 1)
                
                rle_res = rle_res + rle_strA + "o" + rle_strB + "b"
                rle_len = 1
        else:
            if rle_len == 1: rle_strA = ""
            else: rle_strA = str (rle_len)
            if rl_i[1] - rl_y == 1: rle_strB = ""
            else: rle_strB = str (rl_i[1] - rl_y)
            if rl_i[0] == 1: rle_strC = "b"
            elif rl_i[0] == 0: rle_strC = ""
            else: rle_strC = str (rl_i[0]) + "b"
            
            rle_res = rle_res + rle_strA + "o" + rle_strB + "$" + rle_strC
            rle_len = 1
            
        rl_x = rl_i[0]
        rl_y = rl_i[1]
    
    if rle_len == 1: rle_strA = ""
    else: rle_strA = str (rle_len)
    rle_res = rle_res[2:] + rle_strA + "o"
    
    return rle_res+"!"
# --------------------------------------------------------------------

#Open clipboard
def openCl(event=None):
    clip = root.clipboard_get()
    if clip[0]=='1':
        p = clip.split(':')
        display.Viewer.rule = p[0]
        display.Viewer.universe.rule = cca.Rule(p[0])
        display.Viewer.pattern = eval(p[1])
    else:
        p = clip.split('\n')
        rule = p[0].split(',')[2].split('=')[1].strip()
        display.Viewer.rule = rule
        display.Viewer.universe.rule = cca.Rule(rule)
        display.Viewer.pattern = rle2coords(''.join(p[1:]))
    
############################################
# Make the classes for the get value menus #
############################################

class ruleMenu():
    def okay(self):
        if testRule(self.field.get()):
            display.Viewer.rule = self.field.get()
            display.Viewer.universe.rule = cca.Rule(self.field.get())
        else:
            tk.messagebox.showerror("Error","Invalid rule \""+self.field.get()+"\", using current rule instead.")
        self.rm.destroy()

    def cancel(self):
        self.rm.destroy()
        
    def __init__(self):
        self.rm = tk.Toplevel()
        self.rm.title("Set rule")
        self.rm.iconbitmap("icon.icon")
        self.rm.resizable(False,False)
        self.text1 = tk.Label(self.rm,text="Set rule:")
        self.text1.pack()
        self.field = tk.Entry(self.rm,bd=3)
        self.field.insert(0,str(display.Viewer.rule))
        self.field.pack(padx=10,pady=10)
        self.ok = tk.Button(self.rm,text='Okay',command=self.okay)
        self.ok.pack(side='left',pady = 10,padx = 10)
        self.cancel = tk.Button(self.rm,text='Cancel',command=self.cancel)
        self.cancel.pack(side='right',pady = 10,padx  =10)

class fillMenu():
    def okay(self):
        global fillPercent
        if not self.field.get().isdigit():
            tk.messagebox.showerror("Error","Invalid number.")
        elif int(self.field.get()) < 0:
            fillPercent = 0
        elif int(self.field.get()) > 100:
            fillPercent = 100
        else:
            fillPercent = int(self.field.get())
        self.rm.destroy()

    def cancel(self):
        self.rm.destroy()
        
    def __init__(self):
        self.rm = tk.Toplevel()
        self.rm.title("Change Random Fill %")
        self.rm.iconbitmap("icon.icon")
        self.rm.resizable(False,False)
        self.text1 = tk.Label(self.rm,text="Fill %:")
        self.text1.pack()
        self.field = tk.Entry(self.rm,bd=3)
        self.field.pack(padx=10,pady=10)
        self.ok = tk.Button(self.rm,text='Okay',command=self.okay)
        self.ok.pack(side='left',pady = 10,padx = 10)
        self.cancel = tk.Button(self.rm,text='Cancel',command=self.cancel)
        self.cancel.pack(side='right',pady = 10,padx  =10)

class aboutMenu():        
    def __init__(self):
        self.rm = tk.Toplevel()
        self.rm.title("About")
        self.rm.iconbitmap("icon.icon")
        self.rm.resizable(False,False)
        self.name = tk.Label(self.rm,text='CoordCA')
        self.name.pack(pady=10)
        self.ver = tk.Label(self.rm,text='Version: 1.0.2 or something. Sat, April 6rd, 2019')
        self.ver.pack()
        self.credit = tk.Label(self.rm,text='Created by Saka in 2019')
        self.credit.pack(padx=20,pady=10)

class creditsMenu():        
    def __init__(self):
        self.rm = tk.Toplevel()
        self.rm.title("Credits")
        self.rm.iconbitmap("icon.icon")
        self.rm.resizable(False,False)
        self.text = tk.Text(self.rm,width=100)
        self.text.insert(tk.END,'''
CoordCA was coded by Dary Saka Fitrady.
But he got help from various sites because he's not good at Python.

Also thanks to the developers of Python, Tkinter, pip, and pyinstaller.

Thanks to the support from many people, especially from the ConwayLife Lounge Discord.
https://discord.gg/BCuYCEn

Thanks to John Conway for creating CGoL,

and Nathaniel Johnston, who created the Cellular Automata Forums and the cell-list to RLE function:
https://conwaylife.com/forums

Thanks to Adam P. Goucher who created Catagolue and apgluxe, which helped with finding patterns.
https://catagolue.appspot.com/home

Thanks to Andrew Trevorrow for creating Golly, another, much better, CA Simulator.
http://golly.sourceforge.net/

Thanks to Wildmyron / Arie Paap for suggesting the use of sets.

Other Contributors: Wright, kivattt, AforAmpere.

Also random shoutout to 77topaz and Goldtiger997. Thanks for existing!

...no thanks to whoever vandalised my Catagolue page though...''')
        self.text.config(state=tk.DISABLED)
        self.text.pack(padx=10,pady=10)
        
class gotoMenu():
    def okay(self):
        global viewx
        global viewy
        viewx = int(self.x.get())
        viewy = int(self.y.get())
        self.rm.destroy()

    def cancel(self):
        self.rm.destroy()
        
    def __init__(self):
        self.rm = tk.Toplevel()
        self.rm.title("Goto...")
        self.rm.iconbitmap("icon.icon")
        self.rm.resizable(False,False)
        self.text1 = tk.Label(self.rm,text="Coords: (Top left)")
        self.text1.pack()
        self.x = tk.Entry(self.rm,bd=3)
        self.x.pack(padx=10,pady=10)
        self.y = tk.Entry(self.rm,bd=3)
        self.y.pack(padx=10,pady=10)
        self.ok = tk.Button(self.rm,text='Okay',command=self.okay)
        self.ok.pack(side='left',pady = 10,padx = 10)
        self.cancel = tk.Button(self.rm,text='Cancel',command=self.cancel)
        self.cancel.pack(side='right',pady = 10,padx  =10)

class colorMenu():
    def okay(self):
        display.Viewer.grid.config(bg=self.dead.get())
        display.Viewer.color = self.live.get()
        self.rm.destroy()

    def cancel(self):
        self.rm.destroy()
        
    def __init__(self):
        self.rm = tk.Toplevel()
        self.rm.title("Colours")
        self.rm.iconbitmap("icon.icon")
        self.rm.resizable(False,False)
        self.text2 = tk.Label(self.rm,text="Dead:")
        self.text2.pack()
        self.dead = tk.Entry(self.rm,bd=3)
        self.dead.pack(padx=10,pady=10)
        self.text3 = tk.Label(self.rm,text="Live:")
        self.text3.pack()
        self.live = tk.Entry(self.rm,bd=3)
        self.live.pack(padx=10,pady=10)
        self.ok = tk.Button(self.rm,text='Okay',command=self.okay)
        self.ok.pack(side='left',pady = 10,padx = 10)
        self.cancel = tk.Button(self.rm,text='Cancel',command=self.cancel)
        self.cancel.pack(side='right',pady = 10,padx  =10)

class pattMenu():
    def okay(self):
        if self.selType.get()=='Cell Coords':
            display.Viewer.pattern = eval(self.field.get("1.0",tk.END))
        print(self.selType.get())
        print(self.field.get("1.0",tk.END))
        self.rm.destroy()

    def cancel(self):
        self.rm.destroy()
        
    def __init__(self):
        self.file = tk.filedialog.askopenfilename(initialdir=filePath+'/examples',
                                                  title="Open pattern...",
                                                  filetypes=[("Supported pattern files","*.rle *.cca"),("All","*.*")])
        if self.file != '':            
            self.file = open(self.file,'r').read()
        else:
            self.file = 'wright stinky'
        if self.file[0]=='1':
            self.p = self.file.split(':')
            display.Viewer.rule = self.p[0]
            display.Viewer.universe.rule = cca.Rule(self.p[0])
            display.Viewer.pattern = eval(self.p[1])
        else:
            self.p = self.file.split('\n')
            self.rule = self.p[0].split(',')[2].split('=')[1].strip()
            display.Viewer.rule = self.rule
            display.Viewer.universe.rule = cca.Rule(self.rule)
            display.Viewer.pattern = rle2coords(''.join(self.p[1:]))

class saveMenu():
    def okay(self):
        pass
    def cancel(self):
        self.rm.destroy()
        
    def __init__(self):
        self.file = tk.filedialog.asksaveasfilename(initialdir=filePath+'/',
                                                    title="Save pattern as...",
                                                    filetypes=[("Run Length Encoded","*.rle"),("Coordinates","*.cca"),("All","*.*")],
                                                    defaultextension=".rle")
        extension = self.file.split('.')[-1]
        if extension == 'rle':
            patt = display.Viewer.pattern
            cl = [x for t in patt for x in t]
            data = 'x=0,y=0,rule='+display.Viewer.rule+'\n'+giveRLE(cl)
        elif extension == 'cca':
            data = display.Viewer.rule+':'+str(display.Viewer.pattern)
        self.opfile = open(self.file,'w+')
        self.opfile.write(data)

##################################
# Define the patternWindow class #
##################################

class PatternWindow():
    def __init__(self,root):
        self.universe = cca.Universe(rule='1891891-2_3_2-3')
        self.pattern = cca.Pattern()
        self.rule = '1891891-2_3_2-3'
        self.pop = len(self.pattern)
        self.grid = tk.Canvas(root,bg='black',relief='sunken')
        self.grid.bind('<Button-1>',self.click)
        self.grid.pack(fill='both',expand='yes',padx=10,pady=10)
        self.cSize = 10
        self.color = 'white'
        
    def renderGrid(self):
        cSize = self.cSize
        wwidth = display.Viewer.grid.winfo_width()
        wheight = display.Viewer.grid.winfo_height()
        for x in range(0,wwidth,cSize):
            self.grid.create_line(x,0,x,wheight,fill='#222')
        for y in range(0,wheight,cSize):
            self.grid.create_line(0,y,wwidth,y,fill='#222')

    def calcCurrView(self): #Returns tuple of length and height in cells
        cSize = self.cSize
        wwidth = display.Viewer.grid.winfo_width()
        wheight = display.Viewer.grid.winfo_height()
        viewWidth = m.ceil(wwidth/cSize)
        viewHeight = m.ceil(wheight/cSize)
        return (viewWidth,viewHeight)

    def renderCells(self,x,y): #x and y are the coordinates of the cell at the top left corner
        cSize = self.cSize
        view = self.calcCurrView()
        maxX = x*-1+view[0]
        maxY = y+view[1]
        patt = self.pattern
        for c in patt:
            if c <= (maxX,maxY):
                self.grid.create_rectangle((c[0]*cSize)+x*cSize,(c[1]*cSize)+y*cSize,((c[0]*cSize)+x*cSize)+cSize,((c[1]*cSize+y*cSize)+cSize),fill=self.color)
        #Render selection box
        if bool(selC2):
            self.grid.create_rectangle(selC1[0]+x*cSize,selC1[1]+y*cSize,selC2[0]+x*cSize,selC2[1]+y*cSize,fill='green',stipple='gray50')

    def paste(self,event=None):
        global mode
        global auto
        global paste
        paste = 1
        mode = 3
        auto = 0

        #Gets clipboard and gets the coords
        clip = root.clipboard_get()
        if clip[0]=='1' and clip[-1]=='}':
            p = clip.split(':')
            display.Viewer.rule = p[0]
            display.Viewer.universe.rule = cca.Rule(p[0])
            ppatt = eval(p[1])
        elif clip[0]=='x':
            p = clip.split('\n')
            rule = p[0].split(',')[2].split('=')[1].strip()
            display.Viewer.rule = rule
            display.Viewer.universe.rule = cca.Rule(rule)
            ppatt = rle2coords(''.join(p[1:]))
        else:
            ppatt = rle2coords(clip)

        paste = ppatt
        display.Viewer.grid.config(cursor='bottom_side')

    def pasteRender(self,patt):
        #Render the pattern that is going to be pasted
        #English needs a future tense suffix
        cSize = self.cSize
        appPosX = lambda : m.floor(mouseX/cSize)
        appPosY = lambda : m.floor(mouseY/cSize)
        
        for c in patt:
            self.grid.create_rectangle((c[0]*cSize)+appPosX()*cSize,(c[1]*cSize)+appPosY()*cSize,((c[0]*cSize)+appPosX()*cSize)+cSize,((c[1]*cSize+appPosY()*cSize)+cSize),fill=self.color)
        
    def step(self):
        simulator = cca.Simulator(self.pattern,self.universe.rule.neighborhood,self.universe.rule.birth,self.universe.rule.survival)
        new = simulator.step()
        self.pattern = new

    def click(self,event):
        global selC1
        global selC2
        global mode
        global dragStart
        global auto
        cSize = self.cSize
        appPosX = m.floor(mouseX/cSize)
        appPosY = m.floor(mouseY/cSize)
        if dragStart is None:
            dragStart = (appPosX-viewx,appPosY-viewy) not in display.Viewer.pattern
        if mode==0:
            auto = 0
            if (appPosY,appPosX) >= (0,0):
                self.pattern.toggle((appPosX-viewx,appPosY-viewy))
        elif mode==2:
            selC1 = (round(event.x/cSize)*cSize-(viewx*cSize),round(event.y/cSize)*cSize-(viewy*cSize))
            selC2 = ()

        elif mode==3:
            for c in paste:
                if c not in self.pattern:
                    self.pattern.add((c[0]+appPosX,c[1]+appPosY))
            drawMode()
    def updateStats(self):
        self.pop = len(self.pattern)

########################       
# Define the app class #
########################

class App():
    def __init__(self,root):
        self.menubar = tk.Menu(root)
        self.pattmenu = tk.Menu(self.menubar,tearoff=0)
        self.pattmenu.add_command(label='New Universe',command=clear)
        self.pattmenu.add_command(label='Read Pattern',command=openPatt)
        self.pattmenu.add_command(label='Save Pattern',command=savePatt)
        self.pattmenu.add_command(label='Copy Pattern (RLE)',command=copy)
        self.pattmenu.add_command(label='Copy Pattern (Coords)',command=copyCoords)
        self.pattmenu.add_separator()
        self.pattmenu.add_command(label='Draw',command=drawMode)
        self.menubar.add_cascade(label='Pattern',menu=self.pattmenu)

        self.viewmenu = tk.Menu(self.menubar,tearoff=0)
        self.viewmenu.add_command(label='Zoom In',command=zoomIn)
        self.viewmenu.add_command(label='Zoom Out',command=zoomOut)
        self.viewmenu.add_command(label='Go to',command=goto)
        self.viewmenu.add_separator()
        self.viewmenu.add_command(label='Colors',command=setColors)
        self.viewmenu.add_command(label='Toggle Lines',command=toggleLines)
        self.menubar.add_cascade(label='Viewing',menu=self.viewmenu)

        self.simulationmenu = tk.Menu(self.menubar,tearoff=0)
        self.simulationmenu.add_command(label='Next Generation',command=step)
        self.simulationmenu.add_command(label='Start',command=autoYes)
        self.simulationmenu.add_command(label='Stop',command=autoNo)
        self.simulationmenu.add_command(label='Reset',command=resetPatt)
        self.simulationmenu.add_separator()
        self.simulationmenu.add_command(label='Set Rule',command=getNewRule)
        self.simulationmenu.add_command(label='Get Neighborhood List',command=getNeighborsList)
        self.simulationmenu.add_command(label='Generate APGtable',command=genTable)
        self.menubar.add_cascade(label='Simulation',menu=self.simulationmenu)

        self.selectionmenu = tk.Menu(self.menubar,tearoff=0)
        self.selectionmenu.add_command(label='Remove selection',command=unSel)
        self.selectionmenu.add_command(label='Clear inside selection',command=clearSelection)
        self.selectionmenu.add_command(label='Random Fill',command=randFill)
        self.selectionmenu.add_command(label='Set Random Fill %',command=fillPercentm)
        self.menubar.add_cascade(label='Selection',menu=self.selectionmenu)

        self.helpmenu = tk.Menu(self.menubar,tearoff=0)
        self.helpmenu.add_command(label='About',command=about)
        self.helpmenu.add_command(label='Credits',command=credit)
        self.helpmenu.add_command(label='Secret Debug Button',command=foo)
        self.menubar.add_cascade(label='Help',menu=self.helpmenu)

        #Set up gens and status bar
        self.info = tk.StringVar()
        self.infobar = tk.Label(root,textvariable=self.info,anchor='w',relief=tk.SUNKEN,bg='#ffffcc',padx=10,pady=10)
        self.info.set("Generation: "+str(gens)+"     Population: "+"foo"+"     Rule: "+'foobar')
        self.infobar.pack(fill='both')

        #Set up buttons
        self.buttonbar = tk.Frame(root)
        self.buttonbar.pack(side=tk.TOP)
        self.stepbutton = tk.Button(root, text='Step', command=step,padx=10)
        self.runbutton = tk.Button(root, text='Run', command=toggleAuto,padx=10)
        self.resetbutton = tk.Button(root, text='Reset', command=resetPatt,padx=10)
        self.drawbutton = tk.Button(root, text='Draw', command=drawMode,padx=10)
        self.movebutton = tk.Button(root, text='Move', command=moveMode,padx=10)
        self.selbutton = tk.Button(root, text='Select', command=selectMode,padx=10)
        self.zoominbutton = tk.Button(root, text='Zoom In', command=zoomIn,padx=10)
        self.zoomoutbutton = tk.Button(root, text='Zoom Out', command=zoomOut,padx=10)
        self.stepbutton.pack(in_=self.buttonbar,side=tk.LEFT,padx=10,pady=10)
        self.resetbutton.pack(in_=self.buttonbar,side=tk.LEFT,padx=10,pady=10)
        self.runbutton.pack(in_=self.buttonbar,side=tk.LEFT,padx=10,pady=10)
        self.drawbutton.pack(in_=self.buttonbar,side=tk.LEFT,padx=10,pady=10)
        self.movebutton.pack(in_=self.buttonbar,side=tk.LEFT,padx=10,pady=10)
        self.selbutton.pack(in_=self.buttonbar,side=tk.LEFT,padx=10,pady=10)
        self.zoominbutton.pack(in_=self.buttonbar,side=tk.LEFT,padx=10,pady=10)
        self.zoomoutbutton.pack(in_=self.buttonbar,side=tk.LEFT,padx=10,pady=10)

        #Make pattern window
        self.Viewer = PatternWindow(root)
        self.info.set("Generation: "+str(gens)+"     Population: "+str(self.Viewer.pop)+"     Rule: "+self.Viewer.rule)

        root.update()

#################
# Run the thing #
#################

root = tk.Tk()
display = App(root)
wwidth = display.Viewer.grid.winfo_width()
wheight = display.Viewer.grid.winfo_height()
display.Viewer.grid.config(cursor='pencil')
root.iconbitmap('icon.icon')
root.title("CoordCA")
root.config(menu=display.menubar)
root.minsize(640,485)
display.Viewer.grid.bind_all('<Up>',moveUp)
display.Viewer.grid.bind_all('<Left>',moveLeft)
display.Viewer.grid.bind_all('<Down>',moveDown)
display.Viewer.grid.bind_all('<Right>',moveRight)

root.bind('<space>',step)
root.bind('<Control-c>',copy)
root.bind('<Control-v>',display.Viewer.paste)
root.bind('<Delete>',clearSelection)
root.bind('<Return>',toggleAuto)
root.bind('<Control-r>',resetPatt)
root.bind('<Control-n>',clear)
root.bind('<m>',center)
root.bind('<MouseWheel>',mouseZoom)

display.Viewer.grid.bind_all('<Control-Key-5>',randFill)
display.Viewer.grid.bind_all('<Control-Shift-Key-O>',openCl)
display.Viewer.grid.bind_all('<Motion>',mousePos)
display.Viewer.grid.bind_all('<B1-Motion>',mouseDrag)
display.Viewer.grid.bind_all('<Button-1>',mouseDrag)
display.Viewer.grid.bind_all('<ButtonRelease-1>', dragOff)
while 1:
    try:
        display.Viewer.grid.delete('all')
        display.Viewer.renderCells(viewx,viewy)
        if mode==3:
            display.Viewer.pasteRender(paste)
        if lines:
            display.Viewer.renderGrid()
        if auto:
            step(a=0)
        display.info.set("Generation: "+str(gens)+"     Population: "+str(display.Viewer.pop)+"     Rule: "+display.Viewer.rule+'     View X: '+str(viewx)+'     View Y: '+str(viewy))
        display.Viewer.updateStats()
        if gens==0 and display.Viewer.pattern != initPatt:
            initPatt = display.Viewer.pattern
        display.Viewer.cSize = cSize
        root.update()
    except tk.TclError:
        break
