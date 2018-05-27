xx = 1
import pygame, math, random
from pygame.locals import *
pygame.init()

winW = 1358
winY = 700
screen = pygame.display.set_mode((winW,winY))
nodeSize = 8
rotateZ = 0
rotateY = 0
rotateX = 0
row = 1
angie = 60
edit = 0
spiralDraw = True
sbX = winW-20
#font = pygame.font.SysFont(None,19)
font = pygame.font.Font(None,19)
fill = True
pygame.display.set_caption("Nodify")
connecting = False
n = False
rain = True
polColors = [[0,255,0],[255,0,0],[0,0,255],[255,0,255],[255,255,0],[0,255,255],[255,255,255],[0,0,0]]
mult = 1
holding = 0
useRadian = False
multiply = True
clicking = False
rotating = False
circles = True
polyDraw = True
ms1 = int(winW/2)
ms2 = int(winY/2)
blinking = 0
blink = False
n10 = False
lowerCount = 100
shouldOrder = False
polEdit = 0
mode = 1
subMode = 0
buttonLoc = [0]
lon = []
dLol = []
nodes = [[500-75,560,-50],[500-75,500-60,-50],[575,500-60,-50],[575,560,-50],[560,575,50],[500-60,575,50],[500-60,500-75,50],[560,500-75,50]]
lol = [[0,1,2,3],[4,5,6,7]]
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
                self.y = (255-buttonLoc[ind])+300
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
        node2 = staticRotateX3D(node,rotateX)
        node3 = staticRotateY3D(node2,rotateY)
        node4 = staticRotateZ3D(node2,rotateZ)
        return node4

"""def order(lql, nqdes):
        newList = []
        averages = []
        comp = []
        #Create a list of averages
        for pol in lql:
                myList = 0
                for indice in pol:
                        myList += nqdes[indice][2]
                myList /= len(pol)
                averages.append(myList)
                comp.append([])
        #Determine rank
        ind = 0
        for average in averages:
                rank = 0
                for average2 in averages:
                        if average > average2:
                                rank += 1
                comp[rank].append(lql[ind])
                ind += 1
        for item in comp:
                for thing in item:
                        newList.append(thing)
        return newList"""

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
        
def order(lql,nqdes):
        newList = []
        averages = []
        comp = []
        #Create a list of averages
        testingList = []
        this = []
        that = []
        thing = []
        for pol in lql:
                myList = 0
                for indice in pol:
                        
                        #First rotate the Z-coordinate around the X-axis
                        rotnot = nqdes[indice]
                        thing.append(rotnot[2])
                        #rotnot[1] -= ms2
                        #rotnot[0] -= ms1
                        #Znot = statRot(rotnot)[2]
                        #drawNode = staticRotateX3D(rotnot,rotateX)
                        #drawNode2 = staticRotateY3D(drawNode,rotateY)
                        #rotnot = staticRotateZ3D(drawNode2,rotateZ)
                        #rotnot[0] += ms1
                        #rotnot[1] += ms2
                        
                        rad = rotateX * math.pi / 180
                        cosa = math.cos(rad)
                        sina = math.sin(rad)
                        x = rotnot[0]-ms1
                        y = rotnot[1]-ms2
                        z = rotnot[2]
                        Znode = [x+ms1, y * cosa - z * sina + ms2, y*sina+z*cosa]
                        that.append(Znode)

                        #Then rotate the Z-coordinate around the Y-axis
                        rad = rotateY * math.pi / 180
                        cosa = math.cos(rad)
                        sina = math.sin(rad)
                        j = Znode[0]-ms1
                        k = Znode[1]-ms2
                        l = Znode[2]
                        Znot = l * cosa - j * sina
                        myList += Znot
                        this.append(Znot)

                
                #Divide by the length of the list to find the average
                myList /= len(pol)
                averages.append(myList)
                #Append placeholders to empty list (these placeholders will be needed later)
                comp.append([])
        text("Ordering after Y coors: " + str(this),(ms1,ms2+90),PINK)
        text("Order before Y coors: " + str(that), (ms1,ms2+60), ORANGE)
        text("Order base Z coors: " + str(thing), (ms1,ms2+150),YELLOW)
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
                ind += 1
        #Remove troublemaking brackets from the list
        for item in comp:
                for thing in item:
                        newList.append(thing)
        #We're done!
        text(str(lql) + " was changed to " + str(newList),(ms1,ms2),RED)
        return newList
        
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
rowText = ['Nodes','Pols','Mobs','Autos','Transform','File','Show','Frames']

bRect1 = pygame.Rect(80*8,0,80,30)
bRect2 = pygame.Rect(80*9,0,80,30)
bRect3 = pygame.Rect(80*10,0,80,30)
bRect4 = pygame.Rect(80*11,0,80,30)
bRect5 = pygame.Rect(80*12,0,80,30)
bRects = [bRect1,bRect2,bRect3,bRect4,bRect5]
#bRects is the list of mode dependent buttons.

bRow1 = ['Add','Remove','Edit','Display']
bc1 = [GREEN,RED,YELLOW,PINK]
bRow2 = ['Add','Remove','Edit','Color','Display']
bc2 = [GREEN,RED,YELLOW,PURPLE,PINK]
bRow3= ['Group','Ungroup','Edit','Display','+AutoMob']
bc3 = [BLUE,GREEN,YELLOW,PINK,RED]
bRow4 = ['Add','Remove','Edit','Display']
bc4 = [GREEN,RED,YELLOW,PINK]
bRow5 = ['Rotate','Scale','Glide']
bc5 = [PURPLE,GREEN,BLUE]
bRow6 = ['Save','Save As','Open']
bc6 = [RED,BLUE,PURPLE]
bRow7 = ['Timing','Make!']
bc7 = [BLUE,YELLOW]
bRow8 = ['Next','Previous','Save','Display']
bc8 = [GREEN,PURPLE,RED,PINK]
bRows = [bRow1,bRow2,bRow3,bRow4,bRow5,bRow6,bRow7,bRow8]
#bRows is the list of lists of button text displayed for each mode.
bcs = [bc1,bc2,bc3,bc4,bc5,bc6,bc7,bc8]
#bcs is the list of the lists of rectangle colors displayed for each mode.


while True:
        if fill == True:
                screen.fill(screenColor)
                
        zScrollbar = scrollbar(winW-100,0,BLUE)

        blinking += 1
        if blinking > 100:
                blinking = 0
        if blinking >= 50:
                blink = True
        elif blinking < 50:
                blink = False
                
        #Other method of drawing nodes and pols that we don't need        
        """if polyDraw == True:
                #Draw polygons
                s = 0
                for l in lol:
                        # (Nodes have to be in the right format, not a three-coordinate-list!)
                        newL = []
                        for coor in l:
                                appended = (drawNodes[coor-1][0]+ms1,drawNodes[coor-1][1]+ms2)
                                newL.append(appended)
                        pygame.draw.polygon(screen,colors[s],newL)
                        s += 1

        #Draw nodes
        indice = 0                
        for node in drawNodes:
                pygame.draw.circle(screen, PURPLE, (int(node[0]),int(node[1])), nodeSize)
                if indice == edit and mode == 1 and (subMode == 1 or subMode == 2):
                        pygame.draw.circle(screen, GREEN, (int(node[0]),int(node[1])), nodeSize)
                indice += 1"""

        #Draw node numbers
        i = 1
        for node in nodes:
                if n == True:
                        text(str(i),(node[0],node[1]),BLACK)
                i += 1

        #pygame.time.wait(25)

        if shouldOrder == True:
                lol = order(lol,nodes)
        
        #Draw pols
        s = 1
        for l in lol:
                #For each polygon, make a list containing the nodes...
                newL = []
                for coor in l:
                        appended = [nodes[coor][0]-ms1,nodes[coor][1]-ms2,nodes[coor][2]]
                        appended = statRot(appended)
                        appended = (appended[0]+ms1,appended[1]+ms2)
                        newL.append(appended)
                #And then draw a polygon with that list of nodes.
                if s == polEdit+1 and blink == False and mode == 2:
                        pygame.draw.polygon(screen,BLACK,newL,4)
                pygame.draw.polygon(screen,polColors[s],newL)
                s += 1
                
        #Draw nodes
        zzz = []
        for node in nodes:
                zzz.append(node[2])
        text("The BASE nodes list Zs are currently: " + str(zzz),(ms1,ms2-30),BLACK)
        dLol = []
        well = []
        i = 1
        for drawNode in nodes:
                #Make sure the nodes are rotated around the center of the screen
                drawNode = [drawNode[0]-ms1,drawNode[1]-ms2,drawNode[2]]
                #Rotate the nodes
                drawNode = staticRotateX3D(drawNode,rotateX)
                well.append(drawNode[2])
                drawNode = staticRotateY3D(drawNode,rotateY)
                drawNode = staticRotateZ3D(drawNode,rotateZ)
                #statRot(drawNode)
                dLol.append(drawNode[2])
                #Put the nodes in the right format
                drawNode = [drawNode[0]+ms1,drawNode[1]+ms2,drawNode[2]]
                #Normally draw nodes
                pygame.draw.circle(screen,(0,255,127),(int(drawNode[0]),int(drawNode[1])),nodeSize)
                #Draw blue connect nodes for making pols
                for number in lon:
                        if i-1 == number:
                                pygame.draw.circle(screen,(0,0,255),(int(drawNode[0]),int(drawNode[1])),nodeSize)
                #Draw the blinking node that is being edited
                if i == edit+1 and (subMode == 1 or (mode == 1 and subMode == 3)) and blink == True and mode != 5:
                        pygame.draw.circle(screen,(255,255,0),(int(drawNode[0]),int(drawNode[1])),nodeSize)
                #elif i == edit+1 and (subMode == 1 or (mode == 1 and subMode == 3)) and blink == False and mode != 5:
                #        pygame.draw.circle(screen,(255,0,0),(int(drawNode[0]),int(drawNode[1])),nodeSize)
                i += 1
        text("Before Y Z-coors: "+str(well), (ms1,ms2+120),PURPLE)
        
        #SUB MODE DRAWING RECTANGLES
        if mode == 1 and subMode == 1:
                pygame.draw.rect(screen,GREEN,bRect1)
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
                
        #Draw Main Menu
        indice = 0
        for button in rows:
                #Draw Rectangle
                pygame.draw.rect(screen,rowColors[indice],button)
                #Draw Text
                text(rowText[indice],(button.x+7,button.y+10),BLACK)
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
                        text(bRows[mode-1][indice],(button.x+3,button.y+10),BLACK)
                indice += 1
                if indice2 < len(bcs[mode-1]):
                        indice2 += 1

        text("The drawn ROTATED Z-coordinates are: " + str(dLol),(ms1,ms2+30),BLACK)
        
        pygame.draw.rect(screen,(0,255,255),pygame.Rect((mode-1)*80,30,80,5))
                
        pygame.display.update()

        """///////////////////////////////////////////////////////////// Events //////////////////////////////////////////////////////////"""
        #Events
        for event in pygame.event.get():
                if event.type == QUIT:
                        pygame.quit()
                        
                if event.type == MOUSEMOTION:
                        if rotating == True and subMode == 1 and mode == 5:
                                pos = event.rel
                                rotateX += pos[1]*.005
                                rotateY += pos[0]*.005
                        if holding == 1:
                                buttonLoc[0] += event.rel[1]
                                nodes[edit][2] += event.rel[1]
                                
                if event.type == MOUSEBUTTONDOWN:
                        
                        #testVar = clickingButton()
                        if mode == 1 and subMode == 1 and not mouseHovering(bRect1): #and (not testVar):
                                nodes.append([event.pos[0],event.pos[1],0])
                                edit = len(nodes)-1
                        
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
                                        lol.append(lon)
                                        polEdit = len(lol)-1
                                lon = []
                        if mouseHovering(addRect) and mode == 2 and subMode == 1:
                                lon.append(edit)
                        if mouseHovering(bRect3) == True and mode == 1 and subMode != 3:
                                subMode = 3
                        elif mouseHovering(bRect3) == True and mode == 1 and subMode == 3:
                                subMode = 0
                        if mouseHovering(zScrollbar.button) and mode == 1 and subMode == 3:
                                holding = 1
                                
                if event.type == MOUSEBUTTONUP:
                        clicking = False
                        clickingButton = False
                        rotating = False
                        holding = 0
                        
                if event.type == KEYDOWN:
                        if event.key == ord(' '):
                                fill = not fill
                        if event.key == K_UP and edit < len(nodes)-1:
                                edit += 1
                                buttonLoc[0] = nodes[edit][2]
                        if event.key == K_DOWN and edit > 0:
                                edit -= 1
                                buttonLoc[0] = nodes[edit][2]
                        if event.key == ord("o"):
                                shouldOrder = not shouldOrder
