"""Nodify Beta Version - Still in Development
The project to give the power of simple 3D animation to everyone."""

#TO ADD: display lists, opening files, cancel and delete buttons, splitting polygons, automobs, color coding nodes/mobs, selecting nodes (and pols?), editing stuff, speed indicator


import pygame, math, random, time, os
try:
        from mss import mss
        screenshot = True
except:
        screenshot = False
from pygame.locals import *
pygame.init()

winW = 1358
winY = 700
ms1 = int(winW/2)
ms2 = int(winY/2)
screen = pygame.display.set_mode((winW,winY))



#Splash screen
screen.fill((0,75,255))

pygame.draw.polygon(screen, (255,0,0),[(ms1-100,ms2-100),(ms1+100,ms2+100),(ms1-100,ms2+100)])
pygame.draw.rect(screen, (255,0,0), pygame.Rect(ms1+66, ms2-100, 34, 200)) 
pygame.draw.circle(screen, (0,75,255), (ms1-33,ms2+75), 40)

pygame.display.update()
pygame.time.wait(2000)

lon = []
lom = []
nodeSize = 8
row = 1
paMethod = 1
edit = 0
sbX = winW-20
f1pos = [5,8]
f2pos = [3,10]
try:
        font = pygame.font.Font("C:\Windows\Fonts\segoeui.ttf",16)
        fpos = f1pos
except:
        font = pygame.font.Font(None,19)
        fpos = f2pos
fill = True
pygame.display.set_caption("Nodify")
connecting = False
n = False
rain = True
polColors = []
mult = 1
holding = 0
useRadian = False
multiply = True
clicking = False
rotating = False
polyDraw = True
blinking = 0
blink = False
polEdit = 0
mobEdit = 0
mode = 1
subMode = 0
buttonLoc = [0,0,0,0,0,0,0]
start = 0
finish = 0
programSpeed = 0
should = 0
cannot = pygame.Rect(winW-150, winY-125,100,75)
error = False
errorCount = 0
plane = 0
speedList = []
itera = 0
speedAverage = 0
speedColor = (0,255,0)

#Remember, each of these lists have frame sublists. 
fNodes = [[]]
fLol = [[]]
fPolColors = [[]]
fMobs = [[]]
fRots = [[0,0,0]]
f = 0

addRect = pygame.Rect(winW-200, winY-200,100,100)

#COLORS:
BLACK = (0,0,0)
WHITE = (255,255,255)
PINK = (255,0,255)
PURPLE = (127,0,255)
INDIGO = (75,0,255)
BLUE = (0,0,255)
SKY_BLUE = (0,100,255)
CYAN = (0,255,255)
GREEN = (0,255,150)
MOSTLY_GREEN = (0,255,50)
YELLOW_GREEN = (100,255,0)
JADE_GREEN = (0,255,100)
YELLOW = (255,255,0)
GOLDEN_YELLOW = (255,200,0)
YELLOW_ORANGE = (255,200,0)
ORANGE = (255,150,0)
RED_ORANGE = (255,100,0)
RED = (255,0,0)
MAGENTA = (255,0,200)
screenColor = WHITE
GRAY = (127,127,127)
bigLimit = 100
littleLimit = 600
tesMes = "Not Working"

def readFile(fileName):
        dude = open(fileName,"r")
        fil = dude.read()
        dude.close()
        #You're gonna use a string and copy each number to a new list.
        #Make a list with the numbers in the string
        #Nodes, Pols, Colors, Mobs, Rots, Anims, Views
        newFile = [[[[]]],[[[]]],[[[]]],[[[]]],[[[]]],[[[]]],[[[]]]]
        stage = 0
        frameStage = 0
        elemist = 0
        huh = ''
        index = 0
        for char in fil:
                if char == "*":
                        stage += 1
                        frameStage = 0
                        elemist = 0
                        index = 0
                elif char == "^":
                        newFile[stage].append([[]])
                        frameStage += 1
                        elemist = 0
                        index = 0
                elif char == "[" and index != 0:
                        newFile[stage][frameStage].append([])
                        elemist += 1
                        huh = ""
                elif char == ",":
                        newFile[stage][frameStage][elemist].append(int(huh))
                        huh = ""
                elif char == "]":
                        newFile[stage][frameStage][elemist].append(int(huh))
                        huh = ""
                elif char != "[" and char != " " and char != "]":
                        huh = huh + char
                index += 1

        #Take out the empty brackets (null elements in empty frames)
        in1 = 0
        for stage in newFile:
                in2 = 0
                for frame in stage:
                        in3 = 0
                        for element in frame:
                                if len(element) == 0:
                                        newFile[in1][in2].remove(element)
                        in2 += 1
                in1 += 1
        return newFile
        
def clickingButton():
        ret = False
        for button in bRects:
                if mouseHovering(button):
                        ret = True
        for button in rows:
                if mouseHovering(button):
                        ret = True
        return ret

class scrollbar(object):
        def __init__(self,x,ind,color):
                #x is the x-position of the scrollbar on the screen.
                #ind is the indice it uses on buttonLoc to find the y-position of the little scroller square.
                #color changes the scrollbar background color.
                self.x = x
                self.y = buttonLoc[ind]
                self.backRect = pygame.Rect(self.x,100,10,500)
                self.button = pygame.Rect(self.x-2,self.y+343,15,15)
                self.color = color
        def draw(self):
                pygame.draw.rect(screen,self.color,self.backRect)
                pygame.draw.rect(screen,BLACK,self.button)
                
class cScrollbar(object):
        def __init__(self,x,ind,color):
                #Uses a little weird math to change colors with RGB values.
                self.x = x
                self.y = buttonLoc[ind]+300
                self.backRect = pygame.Rect(self.x,300,10,255)
                self.button = pygame.Rect(self.x-2,self.y,15,15)
                self.color = color
        def draw(self):
                pygame.draw.rect(screen,self.color,self.backRect)
                pygame.draw.rect(screen,BLACK,self.button)
                
def text(message,pos,c):
        if type(message) != "string":
                message = str(message)
        text = font.render(message, True, c)
        textRect = text.get_rect()
        textRect.x = pos[0]
        textRect.y = pos[1]
        screen.blit(text, textRect)
        
#This is a scrollbar display list class.
class Display(object):
        def __init__(self,color,collist):
                self.color = color
                self.shift = 0
                self.num = 0
                self.collist = collist
        def draw(self):
                pygame.draw.rect(screen,self.color,pygame.Rect(winW-200,0,200,400),2)
                pygame.draw.rect(screen,self.collist[self.num],pygame.Rect(winW-200,0,200,40-10*self.shift))
                pygame.draw.rect(screen,self.collist[self.num+1],pygame.Rect(winW-200,40-self.shift*10,200))
                pygame.draw.rect(screen,self.collist[self.num+2],pygame.Rect(winW-200,80-self.shift*10,200))
                pygame.draw.rect(screen,self.collist[self.num+3],pygame.Rect(winW-200,120-self.shift*10,200))
                pygame.draw.rect(screen,self.collist[self.num+4],pygame.Rect(winW-200,160-self.shift*10,200))
                pygame.draw.rect(screen,self.collist[self.num+5],pygame.Rect(winW-200,200-self.shift*10,200))
                pygame.draw.rect(screen,self.collist[self.num+6],pygame.Rect(winW-200,240-self.shift*10,200))
                pygame.draw.rect(screen,self.collist[self.num+7],pygame.Rect(winW-200,280-self.shift*10,200))
                pygame.draw.rect(screen,self.collist[self.num+8],pygame.Rect(winW-200,320-self.shift*10,200))
                pygame.draw.rect(screen,self.collist[self.num+9],pygame.Rect(winW-200,360-self.shift*10,200))
                if self.shift != 0:
                        pygame.draw.rect(screen,self.collist[self.num+10],pygame.Rect(winW-200,400-self.shift*10,self.shift*10))

                pygame.draw.rect(screen,BLUE,pygame.Rect(50,200,50,50))

def Zrotate(x,y,mx,my,angle):
        """Rotates point (x, y) around the Z-directed axis at (mx,my) of the given angle counterclockwise."""
        x1 = x - mx
        y1 = y - my
        xp = (x1*math.cos(angle)) - (y1*math.sin(angle))
        yp = (x1*math.sin(angle)) + (y1*math.cos(angle))
        x2 = xp + mx
        y2 = yp + my
        return [x2,y2,0]
def mouseHovering(rect):
        if event.pos[0] < rect.right and event.pos[0] > rect.left and event.pos[1] > rect.top and event.pos[1] < rect.bottom:
                return True

def createVideo():
        #^^ Line 200 ^^     (you can use alt-G)

        #Warning and What to Do
        screen.fill(WHITE)
        pygame.draw.line(screen, (0,255,1), (0,0),(winW,0))
        pygame.draw.line(screen, (0,255,1), (0,0),(0,winY))
        pygame.draw.line(screen, (0,255,1), (0,winY-1),(winW,winY-1))
        pygame.draw.line(screen, (0,255,1), (winW-1,0),(winW-1,winY))
        text("Please center the window without any edges cut off. Saving your (.png) frames to the same directory as Nodify. Prepare for screenshot in 5 seconds!",(ms1-500,ms2),BLUE)
        pygame.display.update()
        pygame.time.wait(500)
        pygame.time.wait(500)
        pygame.time.wait(500)
        pygame.time.wait(500)
        pygame.time.wait(500)
        pygame.time.wait(500)
        pygame.time.wait(500)
        pygame.time.wait(500)
        pygame.time.wait(500)
        pygame.time.wait(500)
        f = 0
        for frame in fLol:
                screen.fill(WHITE)
                #Draw pols
                s = 1
                for l in fLol[f]:
                        #For each polygon, make a list containing the nodes...
                        newL = []
                        for coor in l:
                                appended = [fNodes[f][coor][0]-ms1,fNodes[f][coor][1]-ms2,fNodes[f][coor][2]]
                                appended = statRot(appended)
                                appended = (appended[0]+ms1,appended[1]+ms2)
                                newL.append(appended)
                        #And then draw a polygon with that list of nodes.
                        pygame.draw.polygon(screen,fPolColors[f][s-1],newL)
                        s += 1
                pygame.draw.line(screen, (0,255,1), (0,0),(winW,0))
                pygame.draw.line(screen, (0,255,1), (0,0),(0,winY))
                pygame.draw.line(screen, (0,255,1), (0,winY-1),(winW,winY-1))
                pygame.draw.line(screen, (0,255,1), (winW-1,0),(winW-1,winY))
                pygame.display.update()
                with mss() as sct:
                        sct.shot()
                oldzFile = open("monitor-1.png","rb")
                newzFile = open(str(f)+".png","wb")
                newzFile.write(oldzFile.read())
                oldzFile.close()
                newzFile.close()
                f += 1
        mode = 1
        subMode = 1

#NODE ROTATING FUNCTIONS

def rotateZ3D(angle):
        if useRadian == True:
                rad = angle * math.pi / 180
        else:
                rad = angle
        if type(rad) != "float":
                rad = float(rad)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        indice = 0
        for node in drawNodes:
                x = node[0] - ms1
                y = node[1] - ms2
                drawNodes[indice][0] = x * cosa - y * sina + ms1
                drawNodes[indice][1] = x * sina + y * cosa + ms2
                indice += 1
                
def staticRotateZ3D(node,angle):
        if useRadian == True:
                rad = angle * math.pi / 180
        else:
                rad = angle
        if type(rad) != "float":
                rad = float(rad)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = node[0]
        y = node[1]
        node[0] = x * cosa - y * sina
        node[1] = x * sina + y * cosa
        return [node[0],node[1],node[2]]

def rotateY3D(angle):
        if useRadian == True:
                rad = angle * math.pi / 180
        else:
                rad = angle
        if type(rad) != "float":
                rad = float(rad)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        indice = 0
        for node in drawNodes:
                x = node[0]
                z = node[2]
                drawNodes[indice][2] = z * cosa - x * sina
                drawNodes[indice][0] = z * sina + x * cosa
                indice += 1
def staticRotateY3D(nnode,angle):
        if useRadian == True:
                rad = angle * math.pi / 180
        else:
                rad = angle
        if type(rad) != "float":
                rad = float(rad)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = nnode[0]
        z = nnode[2]
        nnode[2] = z * cosa - x * sina
        nnode[0] = z * sina + x * cosa
        return [nnode[0],nnode[1],nnode[2]]

def rotateX3D(angle):
        if useRadian == True:
                rad = angle * math.pi / 180
        else:
                rad = angle
        if type(rad) != "float":
                rad = float(rad)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        indice = 0
        for node in drawNodes:
                y = node[1] - ms2
                z = node[2]
                drawNodes[indice][1] = y * cosa - z * sina + ms2
                drawNodes[indice][2] = y * sina + z * cosa
                indice += 1
def staticRotateX3D(node,angle):
        if useRadian == True:
                rad = angle * math.pi / 180
        else:
                rad = angle
        if type(rad) != "float":
                rad = float(rad)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = node[1]
        z = node[2]
        node[1] = y * cosa - z * sina
        node[2] = y * sina + z * cosa
        return [node[0],node[1],node[2]]

def statRot(node):
        node2 = staticRotateX3D(node,fRots[f][0])
        node3 = staticRotateY3D(node2,fRots[f][1])
        node4 = staticRotateZ3D(node2,fRots[f][2])
        return node4

def perspective(A,Z,l,div):
        sx = A[0]-Z[0]
        sx = sx/div
        sy = A[1]-Z[1]
        sy = sy/div
        k = (A[0]+sx*l, A[1]+sy*l)
        return k


def rainbow(colorz):
        c1 = colorz[0]
        c2 = colorz[1]
        c3 = colorz[2]
        changing = True
        
        #Magenta to Blue
        if c1 <= 255 and c1 > 0 and c2 == 0 and c3 == 255:
                c1 -= 1
        #Blue to Cyan
        elif c1 == 0 and c2 >= 0 and c2 < 255 and c3 == 255:
                c2 += 1
        #Cyan to Green
        elif c1 == 0 and c2 == 255 and c3 <= 255 and c3 > 0:
                c3 -= 1
        #Green to Yellow
        elif c1 >= 0 and c1 < 255 and c2 == 255 and c3 == 0:
                c1 += 1
        #Yellow to Red
        elif c1 == 255 and c2 <= 255 and c2 > 0 and c3 == 0:
                c2 -= 1
        #Red to Magenta
        elif c1 == 255 and c2 == 0 and c3 >= 0 and c3 < 255:
                c3 += 1
        else:
                changing = False
        if changing == False:
                return (0,0,0)
        else:
                return (c1,c2,c3)
        
def order(lql,nqdes,polCqlors):
        newList = []
        averages = []
        comp = []
        compCol = []
        #Create a list of averages
        for pol in lql:
                myList = 0
                for indice in pol:
                        
                        #First rotate the Z-coordinate around the X-axis
                        rotnot = nqdes[indice]                        
                        #Znot = statRot(rotnot)[2]
                        #drawNode = staticRotateX3D(rotnot,fRots[f][0])
                        #drawNode2 = staticRotateY3D(drawNode,fRots[f][1])
                        #rotnot = staticRotateZ3D(drawNode2,fRots[f][2])
                        
                        cosa = math.cos(fRots[f][0])
                        sina = math.sin(fRots[f][0])
                        x = rotnot[0]-ms1
                        y = rotnot[1]-ms2
                        z = rotnot[2]
                        Znode = [x+ms1, y * cosa - z * sina + ms2, y*sina+z*cosa]

                        #Then rotate the Z-coordinate around the Y-axis
                        cosa = math.cos(fRots[f][1])
                        sina = math.sin(fRots[f][1])
                        j = Znode[0]-ms1
                        k = Znode[1]-ms2
                        l = Znode[2]
                        Znot = l * cosa - j * sina
                        myList += Znot
                        
                #Divide by the length of the list to find the average
                myList /= len(pol)
                averages.append(myList)
                #Append placeholders to empty list (these placeholders will be needed later)
                comp.append([])
                compCol.append([])
                
        #text("The first rotation with ordering brings: " + str(that), (100,ms2+120),BLACK)
        #Compare averages and rank accordingly
        ind = 0
        for average in averages:
                rank = 0
                for average2 in averages:
                        if average > average2:
                                rank += 1
                #Append the node indice corresponding to the current average in the list selecting the placeholder by its rank
                comp[rank].append(lql[ind])
                compCol[rank].append(polCqlors[ind])
                ind += 1
        #Remove troublemaking brackets from the lists
        for item in comp:
                for thing in item:
                        newList.append(thing)
        newListCol = []
        for item in compCol:
                for thing in item:
                        newListCol.append(thing)
        #We're done!
        return [newList,newListCol]
        
#Buttons
row1 = pygame.Rect(0,0,80,30)
row2 = pygame.Rect(80,0,80,30)
row3 = pygame.Rect(80*2,0,80,30)
row4 = pygame.Rect(80*3,0,80,30)
row5 = pygame.Rect(80*4,0,80,30)
row6 = pygame.Rect(80*5,0,80,30)
row7 = pygame.Rect(80*6,0,80,30)
row8 = pygame.Rect(80*7,0,80,30)
rows = [row1,row2,row3,row4,row5,row6,row7,row8]
rowColors = [RED,PINK,BLUE,ORANGE,GREEN,PURPLE,YELLOW,GRAY]
#rowText is the list of texts for the main menu.
rowText = ['Nodes','Pols','Mobs','Autos','Transform','File','Frames','Make']

bRect1 = pygame.Rect(80*8,0,80,30)
bRect2 = pygame.Rect(80*9,0,80,30)
bRect3 = pygame.Rect(80*10,0,80,30)
bRect4 = pygame.Rect(80*11,0,80,30)
bRect5 = pygame.Rect(80*12,0,80,30)
bRect6 = pygame.Rect(80*13,0,80,30)
bRect7 = pygame.Rect(80*14,0,80,30)
bRect8 = pygame.Rect(80*15,0,80,30)
bRects = [bRect1,bRect2,bRect3,bRect4,bRect5,bRect6,bRect7,bRect8]
#bRects is the list of mode dependent buttons.

bRow1 = ['Add','Remove','Edit','Select','Display']
bc1 = [GREEN,RED,YELLOW,ORANGE,PINK]
bRow2 = ['Add','Remove','Edit','Color','Display']
bc2 = [GREEN,RED,YELLOW,PURPLE,PINK]
bRow3= ['Group','Ungroup','Edit','+AutoMob','Display', 'Rotate','Scale','Glide']
bc3 = [BLUE,GREEN,YELLOW,RED,PINK, PURPLE, ORANGE, CYAN]
bRow4 = ['Add','Remove','Edit','Display']
bc4 = [GREEN,RED,YELLOW,PINK]
bRow5 = ['Rotate','Scale','Glide']
bc5 = [PURPLE,ORANGE,CYAN]
bRow6 = ['Save','Save As','Open','Previous','Next']
bc6 = [RED,BLUE,PURPLE,GREEN,ORANGE]
bRow7 = ['Previous','Next','Add','Delete','Display']
bc7 = [BLUE,PURPLE,GREEN,RED,PINK]
bRow8 = [] #Used to be "Show" ['Timing','Make!']
bc8 = [GREEN,PURPLE,RED,PINK]
bRows = [bRow1,bRow2,bRow3,bRow4,bRow5,bRow6,bRow7,bRow8]
#bRows is the list of lists of button text displayed for each mode.
bcs = [bc1,bc2,bc3,bc4,bc5,bc6,bc7,bc8]
#bcs is the list of the lists of rectangle colors displayed for each mode.

myDisplay = Display(RED,fPolColors[f])

editedF= 0

while True:
        theClock = pygame.time.Clock()
        if should == 5:
                start = pygame.time.get_ticks()
        
        if should < 10:
                should += 1
        elif should == 10:
                should = 0
        
        if fill == True:
                screen.fill(screenColor)

        if error == True:
                if errorCount < 200:
                        errorCount += 1
                elif errorCount == 200:
                        error = False
                        errorCount = 0

        #myDisplay.draw()

        xScrollbar = scrollbar(winW-100,0,YELLOW)
        yScrollbar = scrollbar(winW-75,1,GREEN)
        zScrollbar = scrollbar(winW-50,2,BLUE)

        rScrollbar = cScrollbar(winW-100,3,RED)
        gScrollbar = cScrollbar(winW-75,4,(0,255,0))
        bScrollbar = cScrollbar(winW-50,5,BLUE)

        pScrollbar = scrollbar(winW-75,6,BLUE)
        

        blinking += 1
        if blinking > 100:
                blinking = 0
        if blinking >= 50:
                blink = True
        elif blinking < 50:
                blink = False

        #Draw node numbers
        i = 1
        for node in fNodes[f]:
                if n == True:
                        text(str(i),(node[0],node[1]),BLACK)
                i += 1
        
                
        prelist = order(fLol[f],fNodes[f],fPolColors[f])
        fLol[f] = prelist[0]
        fPolColors[f] = prelist[1]
        
        
        #Draw pols
        tester = []
        s = 1
        for l in fLol[f]:
                tester.append(l)
                #For each polygon, make a list containing the nodes...
                newL = []
                for coor in l:
                        appended = [fNodes[f][coor][0]-ms1,fNodes[f][coor][1]-ms2,fNodes[f][coor][2]]
                        appended = statRot(appended)
                        appended = (appended[0]+ms1,appended[1]+ms2)
                        newL.append(appended)
                #And then draw a polygon with that list of nodes.
                try:
                        if s == polEdit+1 and blink == False and mode == 2:
                                pygame.draw.polygon(screen,BLACK,newL,4)
                        pygame.draw.polygon(screen,fPolColors[f][s-1],newL)
                except TypeError:
                        text("ERROR: Invalid pol color data. Try opening a different file, and if that doesn't work, reinstall Nodify."+str(fPolColors[f]),(ms1,ms2),ORANGE)
                s += 1
        
        #Draw nodes
        i = 1
        for drawNode in fNodes[f]:
                #Make sure the nodes are rotated around the center of the screen
                drawNode = [drawNode[0]-ms1,drawNode[1]-ms2,drawNode[2]]
                #Rotate the nodes
                drawNode = staticRotateX3D(drawNode,fRots[f][0])
                drawNode = staticRotateY3D(drawNode,fRots[f][1])
                drawNode = staticRotateZ3D(drawNode,fRots[f][2])
                
                #Put the nodes in the right format
                drawNode = [drawNode[0]+ms1,drawNode[1]+ms2,drawNode[2]]
                
                #Normally draw nodes
                pygame.draw.circle(screen,(0,255,127),(int(drawNode[0]),int(drawNode[1])),nodeSize)
                #Draw blue connect nodes for making pols
                for number in lon:
                        if i-1 == number:
                                pygame.draw.circle(screen,(0,0,255),(int(drawNode[0]),int(drawNode[1])),nodeSize)
                #Draw purple connect nodes for making mobs
                for number in lom:
                        if i-1 == number:
                                pygame.draw.circle(screen,(150,0,255),(int(drawNode[0]),int(drawNode[1])),nodeSize)
                if len(fMobs[f]) > 0 and mode == 3:
                        for ed in fMobs[f][mobEdit]:
                                if ed == i-1:
                                        pygame.draw.circle(screen,(0,127,255),(int(drawNode[0]),int(drawNode[1])),nodeSize)
                #Draw the blinking node that is being edited
                if i == edit+1 and (subMode == 1 or (mode == 1 and subMode == 3)) and blink == False and mode != 5:
                        pygame.draw.circle(screen,(255,255,0),(int(drawNode[0]),int(drawNode[1])),nodeSize)
                i += 1
        
        #SUB MODE DRAWING RECTANGLES/SCROLLBARS
        if mode == 1 and subMode == 1:
                pygame.draw.rect(screen,GREEN,bRect1)
                pScrollbar.draw()
                text(str(plane),(winW-80,75),BLUE)
        if mode == 5 and subMode == 1:
                pygame.draw.rect(screen,PURPLE,bRect1)
        if mode == 2 and subMode == 1:
                pygame.draw.rect(screen,GREEN,bRect1)
                pygame.draw.rect(screen,PINK,addRect)
                text("Add Point",(addRect.x+10,addRect.y+10),BLACK)
        if mode == 1 and subMode == 3:
                pygame.draw.rect(screen,YELLOW,bRect3)
        if mode == 1 and subMode == 3:
                zScrollbar.draw()
                yScrollbar.draw()
                xScrollbar.draw()
        if mode == 2 and subMode == 4:
                tesMes = "Working"
                rScrollbar.draw()
                gScrollbar.draw()
                bScrollbar.draw()
        if mode == 3 and subMode == 1:
                pygame.draw.rect(screen,BLUE,bRect1)
                pygame.draw.rect(screen,BLUE,addRect)
                
        #Draw Main Menu
        indice = 0
        for button in rows:
                #Draw Rectangle
                pygame.draw.rect(screen,rowColors[indice],button)
                #Draw Text
                text(rowText[indice],(button.x+fpos[0],button.y+fpos[1]),BLACK)
                indice += 1

        """rows is the list of main menu buttons.
        rowText is the list of texts for the main menu.
        bRects is the list of the mode dependent button rectangles.
        bRows is the list of lists of button text displayed for each dependent mode.
        bcs is the list of the lists of rectangle colors displayed for each dependent mode.
        If it has a "b", it's dependent - otherwise, it's not!"""
        
        #Draw dependent mode buttons
        indice = 0
        indice2 = 0
        for button in bRects:
                if indice2 < len(bRows[mode-1]):
                        pygame.draw.rect(screen,bcs[mode-1][indice2],button,2)
                        text(bRows[mode-1][indice],(button.x+fpos[0],button.y+fpos[1]),BLACK)
                indice += 1
                if indice2 < len(bcs[mode-1]):
                        indice2 += 1
        
        if speedAverage <= 75:
                speedColor = GREEN
        elif speedAverage <= 126:
                speedColor = ((speedAverage-75)*5,255,0)
        elif speedAverage <= 177:
                speedColor = (255,speedAverage-126,0)
        else:
                speedColor = (255,0,0)
        
        pygame.draw.rect(screen,(0,255,255),pygame.Rect((mode-1)*80,30,80,5))
        pygame.draw.rect(screen,speedColor,pygame.Rect(8,winY-27,speedAverage,20))
        
        text("Speed: " + str(speedAverage),(10,winY-30),BLACK)

        if error == True:
                pygame.draw.rect(screen, (240,10,10), cannot)
                text("No can do!", (winW-140,winY-110),WHITE)
                
        pygame.display.update()

        """///////////////////////////////////////////////////////////// Events //////////////////////////////////////////////////////////"""
        for event in pygame.event.get():
                if event.type == QUIT:
                        pygame.quit()
                        
                if event.type == MOUSEMOTION:
                        if rotating == True and subMode == 1 and mode == 5:
                                pos = event.rel
                                fRots[f][0] += pos[1]*.005
                                fRots[f][1] += pos[0]*.005

                        #SCROLLBAR MOVING:
                        if holding == 1:
                                buttonLoc[0] += event.rel[1]
                                fNodes[f][edit][0] += event.rel[1] * 5
                        if holding == 2:
                                buttonLoc[1] += event.rel[1]
                                fNodes[f][edit][1] += event.rel[1] * 5
                        if holding == 3:
                                buttonLoc[2] += event.rel[1]
                                fNodes[f][edit][2] += event.rel[1] * 5
                        
                        if holding == 4 and (fPolColors[f][polEdit][0] + event.rel[1]) >= 0 and (fPolColors[f][polEdit][0] + event.rel[1]) <= 255:
                                buttonLoc[3] += event.rel[1]
                                fPolColors[f][polEdit][0] += event.rel[1]
                        if holding == 5 and (fPolColors[f][polEdit][1] + event.rel[1]) >= 0 and (fPolColors[f][polEdit][1] + event.rel[1]) <= 255:
                                buttonLoc[4] += event.rel[1]
                                fPolColors[f][polEdit][1] += event.rel[1]
                        if holding == 6 and (fPolColors[f][polEdit][2] + event.rel[1]) >= 0 and (fPolColors[f][polEdit][2] + event.rel[1]) <= 255:
                                buttonLoc[5] += event.rel[1]
                                fPolColors[f][polEdit][2] += event.rel[1]
                        if holding == 7 and (plane+(event.rel[1]*5) >= -500) and (plane+(event.rel[1]*5) <= 500):
                                plane += event.rel[1] * 5
                                buttonLoc[6] += event.rel[1]

                                
                if event.type == MOUSEBUTTONDOWN:
                        
                        #testVar = clickingButton()
                        if mode == 1 and subMode == 1 and not mouseHovering(bRect1) and not mouseHovering(pScrollbar.button): #and (not testVar):
                                fNodes[f].append([event.pos[0],event.pos[1],plane])
                                edit = len(fNodes[f])-1
                        
                        indice = 1
                        for button in rows:
                                if mouseHovering(button) == True:
                                        mode = indice
                                        subMode = 0
                                indice += 1
                        if mouseHovering(bRect1) == True and mode == 1:
                                if subMode != 1:
                                        subMode = 1
                                elif subMode == 1:
                                        subMode = 0
                        if mouseHovering(bRect1) and mode == 5 and subMode != 1:
                                subMode = 1
                        elif mouseHovering(bRect1) and mode == 5 and subMode == 1:
                                subMode = 0
                        if not mouseHovering(bRect1) and mode == 5 and subMode == 1:
                                rotating = True
                        if mouseHovering(bRect1) and mode == 2 and subMode != 1:
                                subMode = 1
                        elif mouseHovering(bRect1) and mode == 2 and subMode == 1:
                                subMode = 0
                                if len(lon) > 2:
                                        fLol[f].append(lon)
                                        polEdit = len(fLol[f])-1
                                        fPolColors[f].append([random.randint(0,255),random.randint(0,255),random.randint(0,255)])
                                        buttonLoc[3] = fPolColors[f][polEdit][0]
                                        buttonLoc[4] = fPolColors[f][polEdit][1]
                                        buttonLoc[5] = fPolColors[f][polEdit][2]
                                lon = []
                        if mouseHovering(addRect) and mode == 2 and subMode == 1:
                                lon.append(edit)
                        if mouseHovering(bRect3) and mode == 1 and subMode != 3:
                                subMode = 3
                        elif mouseHovering(bRect3) and mode == 1 and subMode == 3:
                                subMode = 0
                        if mouseHovering(bRect4) and mode == 2 and subMode != 4:
                                subMode = 4
                        elif mouseHovering(bRect4) and mode == 2 and subMode == 4:
                                subMode = 0
                        if mouseHovering(bRect3) and mode == 7:
                                fLol.append([])
                                fNodes.append([])
                                fPolColors.append([])
                                fMobs.append([])
                                fRots.append([0,0,0])
                                f = len(fLol)-1
                                edit = 0
                                polEdit = 0
                                buttonLoc[0] = 0
                                buttonLoc[1] = 0
                                buttonLoc[2] = 0
                                buttonLoc[3] = 0
                                buttonLoc[4] = 0
                                buttonLoc[5] = 0
                        if mouseHovering(bRect2) and mode == 7 and f < len(fLol)-1:
                                f += 1
                                edit = 0
                                polEdit = 0
                                buttonLoc[0] = fNodes[f][edit][0] / 5
                                buttonLoc[1] = fNodes[f][edit][1] / 5
                                buttonLoc[2] = fNodes[f][edit][2] / 5
                                buttonLoc[3] = fPolColors[f][polEdit][0]
                                buttonLoc[4] = fPolColors[f][polEdit][1]
                                buttonLoc[5] = fPolColors[f][polEdit][2]
                        if mouseHovering(bRect1) and mode == 7 and f > 0:
                                f -= 1
                                edit = 0
                                polEdit = 0
                                buttonLoc[0] = fNodes[f][edit][0] / 5
                                buttonLoc[1] = fNodes[f][edit][1] / 5
                                buttonLoc[2] = fNodes[f][edit][2] / 5
                                buttonLoc[3] = fPolColors[f][polEdit][0]
                                buttonLoc[4] = fPolColors[f][polEdit][1]
                                buttonLoc[5] = fPolColors[f][polEdit][2]
                        if mouseHovering(bRect2) and mode == 6:
                                
                                #fNodes = [ frames [ nodes [x, y, z] ] ]
                                #   to:   LISTS sepby *  -   FRAMES sepby ^  -  NODES sepby []  -  X-Y-Z sepby ,

                                fileInt = 1
                                works = True
                                while works == True:
                                        try:
                                                testedFile = open(str(fileInt) + ".ndf","r")
                                                testedFile.close()
                                        except:
                                                works = False
                                                break
                                        fileInt += 1
                                        if fileInt > 50:
                                                print "Either you have more than fifty files, or something went wrong!"
                                                works = False
                                                break
                                with file(str(fileInt)+".ndf","w") as savedAsFile:
                                        
                                        WfNodes = ""
                                        i = 0
                                        for frame in fNodes:
                                                if i != 0:
                                                        WfNodes = WfNodes + "^"
                                                for node in frame:
                                                        WfNodes = WfNodes + str(node)
                                                i += 1

                                        WfLol = ""
                                        i = 0
                                        for frame in fLol:
                                                if i != 0:
                                                        WfLol = WfLol + "^"
                                                for node in frame:
                                                        WfLol = WfLol + str(node)
                                                i += 1
                                                
                                        WfPolColors = ""
                                        i = 0
                                        for frame in fPolColors:
                                                if i != 0:
                                                        WfPolColors = WfPolColors + "^"
                                                for node in frame:
                                                        WfPolColors = WfPolColors + str(node)
                                                i += 1

                                        WfMobs = ""
                                        i = 0
                                        for frame in fMobs:
                                                if i != 0:
                                                        WfMobs = WfMobs + "^"
                                                for node in frame:
                                                        WfMobs = WfMobs + str(node)
                                                i += 1

                                        WfRots = ""
                                        i = 0
                                        for frame in fRots:
                                                if i != 0:
                                                        WfRots = WfRots + "^"
                                                for node in frame:
                                                        WfRots = WfRots + str(node)
                                                i += 1
                                        
                                        savedAsFile.write(WfNodes+'*'+WfLol+'*'+WfPolColors+"*"+WfMobs + "*" + WfRots)

                                        #savedAsFile.write(WfNodes)
                        if mouseHovering(bRect3) and mode == 6:
                                try:
                                        the_file = readFile("1.ndf")
                                        #Translate that into the program's variables
                                        fNodes = the_file[0]
                                        fLol = the_file[1]
                                        fPolColors = the_file[2]
                                        fMobs = the_file[3]
                                        fRots = the_file[4]
                                        editedF = 1
                                except:
                                        pass
                        if mouseHovering(row8) and screenshot == True:
                                createVideo()

                        if mouseHovering(bRect1) and mode == 3 and subMode != 1:
                                subMode = 1
                        elif mouseHovering(bRect1) and mode == 3 and subMode == 1:
                                subMode = 0
                                if len(lom) > 1:
                                        fMobs[f].append(lom)
                                        lom = []
                                        mobEdit = len(fMobs[f])-1
                        if mouseHovering(addRect) and mode == 3 and subMode == 1:
                                lom.append(edit)
                        if mouseHovering(bRect4) and mode == 6 and editedF > 1:
                                try:
                                        the_file = readFile(str(editedF-1)+".ndf")
                                        #Translate that into the program's variables
                                        fNodes = the_file[0]
                                        fLol = the_file[1]
                                        fPolColors = the_file[2]
                                        fMobs = the_file[3]
                                        fRots = the_file[4]
                                        editedF -= 1
                                except:
                                        pass
                        if mouseHovering(bRect5) and mode == 6 and editedF < 50:
                                try:
                                        the_file = readFile(str(editedF+1)+".ndf")
                                        #Translate that into the program's variables
                                        fNodes = the_file[0]
                                        fLol = the_file[1]
                                        fPolColors = the_file[2]
                                        fMobs = the_file[3]
                                        fRots = the_file[4]
                                        editedF += 1
                                except:
                                        pass
                        
                        if mouseHovering(bRect1) and mode == 6 and editedF > 0:
                                os.remove(str(editedF)+".ndf")
                                with file(str(editedF)+".ndf","w") as savedAsFile:
                                        
                                        WfNodes = ""
                                        i = 0
                                        for frame in fNodes:
                                                if i != 0:
                                                        WfNodes = WfNodes + "^"
                                                for node in frame:
                                                        WfNodes = WfNodes + str(node)
                                                i += 1

                                        WfLol = ""
                                        i = 0
                                        for frame in fLol:
                                                if i != 0:
                                                        WfLol = WfLol + "^"
                                                for node in frame:
                                                        WfLol = WfLol + str(node)
                                                i += 1
                                                
                                        WfPolColors = ""
                                        i = 0
                                        for frame in fPolColors:
                                                if i != 0:
                                                        WfPolColors = WfPolColors + "^"
                                                for node in frame:
                                                        WfPolColors = WfPolColors + str(node)
                                                i += 1

                                        WfMobs = ""
                                        i = 0
                                        for frame in fMobs:
                                                if i != 0:
                                                        WfMobs = WfMobs + "^"
                                                for node in frame:
                                                        WfMobs = WfMobs + str(node)
                                                i += 1
                                                
                                        WfRots = ""
                                        i = 0
                                        for frame in fRots:
                                                if i != 0:
                                                        WfRots = WfRots + "^"
                                                for node in frame:
                                                        WfRots = WfRots + str(node)
                                                i += 1
                                        
                                        savedAsFile.write(WfNodes+'*'+WfLol+'*'+WfPolColors+"*"+WfMobs + "*" + WfRots)
                                
                        #SCROLLBAR CLICKING BUTTONS
                        if mouseHovering(xScrollbar.button) and mode == 1 and subMode == 3:
                                holding = 1
                        if mouseHovering(yScrollbar.button) and mode == 1 and subMode == 3:
                                holding = 2
                        if mouseHovering(zScrollbar.button) and mode == 1 and subMode == 3:
                                holding = 3
                        if mouseHovering(rScrollbar.button) and mode == 2 and subMode == 4:
                                holding = 4
                        if mouseHovering(gScrollbar.button) and mode == 2 and subMode == 4:
                                holding = 5
                        if mouseHovering(bScrollbar.button) and mode == 2 and subMode == 4:
                                holding = 6
                        if mouseHovering(pScrollbar.button) and mode == 1 and subMode == 1:
                                holding = 7
                        
                if event.type == MOUSEBUTTONUP:
                        clicking = False
                        clickingButton = False
                        rotating = False
                        holding = 0
                        
                if event.type == KEYDOWN:
                        if event.key == ord(' '):
                                fill = not fill
                        if event.key == K_UP and edit < len(fNodes[f])-1 and (mode == 1 or ((subMode == 1 and mode == 2) or (subMode == 1 and mode == 3))):
                                edit += 1
                                buttonLoc[0] = fNodes[f][edit][0] / 5
                                buttonLoc[1] = fNodes[f][edit][1] / 5
                                buttonLoc[2] = fNodes[f][edit][2] / 5
                        elif event.key == K_UP and polEdit < len(fLol[f])-1 and (mode == 2 and subMode != 1):
                                polEdit += 1
                                buttonLoc[3] = fPolColors[f][polEdit][0]
                                buttonLoc[4] = fPolColors[f][polEdit][1]
                                buttonLoc[5] = fPolColors[f][polEdit][2]
                        elif event.key == K_UP and mobEdit < len(fMobs[f])-1 and mode == 3:
                                mobEdit += 1
                                
                        if event.key == K_DOWN and edit > 0 and (mode == 1 or ((subMode == 1 and mode == 2) or (subMode == 1 and mode == 3))):
                                edit -= 1
                                buttonLoc[0] = fNodes[f][edit][0] / 5
                                buttonLoc[1] = fNodes[f][edit][1] / 5
                                buttonLoc[2] = fNodes[f][edit][2] / 5
                        elif event.key == K_DOWN and polEdit > 0 and (mode == 2 and subMode != 1):
                                polEdit -= 1
                                buttonLoc[3] = fPolColors[f][polEdit][0]
                                buttonLoc[4] = fPolColors[f][polEdit][1]
                                buttonLoc[5] = fPolColors[f][polEdit][2]
                        elif event.key == K_DOWN and mobEdit > 0 and mode == 3:
                                mobEdit -= 1
        
        if should == 5:
                finish = pygame.time.get_ticks()
                speedList.append(finish-start)
                if itera == 25:
                        speedAverage = 0
                        for num in speedList:
                                speedAverage += num
                        speedAverage = speedAverage/25
                        speedList = []
                        itera = 0
                else:
                        itera += 1
