import numpy as np
import random, sys, time, pygame
from pygame.locals import *


DISPLAYSURF = None
#                R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
LIGHTGRAY    = (100, 100, 100)
bgColour = DARKGRAY

W_HEIGHT = 640
W_WIDTH = 640

colours = [RED, BLACK, WHITE]
mousex = 0
mousey = 0

class Cell():
    size = 0
    xPos = 0
    yPos = 0
    u = False
    d = False
    r = False
    l = False
    mainRect = None
    uRect = None
    dRect = None
    rRect = None
    lRect = None
    active = False
    def __init__(self, u, d, l, r, size, xPos, yPos):
        self.u = u
        self.d = d
        self.r = r
        self.l = l
        self.size = size
        self.xPos = xPos
        self.yPos = yPos
        print xPos, yPos, size
        self.mainRect = pygame.Rect(xPos*size, yPos*size, size, size)
        self.updateRects()

    def updateRects(self):
        if self.u:
            self.uRect = pygame.Rect(self.mainRect.x+(self.mainRect.width/2-2), self.mainRect.y+0, 4, 4)
            print "Setting uRect"
        else:
            self.uRect = pygame.Rect(self.mainRect.x+0, self.mainRect.y+0, 0, 0)
        
        if self.d:
            self.dRect = pygame.Rect(self.mainRect.x+(self.mainRect.width/2-2), self.mainRect.y+(self.mainRect.height-2), 4, 4)
            print "Setting dRect"
        else:
            self.dRect = pygame.Rect(self.mainRect.x+0, self.mainRect.y+0, 0, 0)

        if self.r:
            self.rRect = pygame.Rect(self.mainRect.x+(self.mainRect.width-2), self.mainRect.y+(self.mainRect.height/2-2), 4, 4)
            print "Setting rRect"
        else:
            self.rRect = pygame.Rect(self.mainRect.x+0, self.mainRect.y+0, 0, 0)

        if self.l:
            self.lRect = pygame.Rect(self.mainRect.x+0, self.mainRect.y+(self.mainRect.height/2-2), 4, 4)
            print "Setting lRect"
        else:
            self.lRect = pygame.Rect(self.mainRect.x+0, self.mainRect.y+0, 0, 0)

class Grid():
    array = []
    cellSize = 0
    width = 0
    height = 0
    def __init__(self, width, height):
        global W_WIDTH, W_HEIGHT
        a = []
        self.width = width
        self.height = height
        self.cellSize = W_WIDTH/width
        for i in xrange(0, width):
            b = []
            for j in xrange(0, height):
                print "New cell!", i, j
                tempU = random.choice([True, False])
                tempD = random.choice([True, False])
                tempR = random.choice([True, False])
                tempL = random.choice([True, False])
                b.append(Cell(tempU, tempD, tempR, tempL, self.cellSize, i, j))
            a.append(b)
        self.array = a # The self keyword is essential to the array access
    
    def printGrid(self):
        print self.array

    def displayGrid(self):
        global colours, DISPLAYSURF
        for row in self.array:
            for cell in row:
                if cell.active:
                    pygame.draw.rect(DISPLAYSURF, colours[0], cell.mainRect)
                else:
                    pygame.draw.rect(DISPLAYSURF, colours[2], cell.mainRect)
                #only draw these at all if they're true \/
                #Are they even necessary though?
                #if cell.u:
                #    pygame.draw.rect(DISPLAYSURF, colours[1], cell.uRect)
                #if cell.d:
                #    pygame.draw.rect(DISPLAYSURF, colours[1], cell.dRect)
                #if cell.r:
                #    pygame.draw.rect(DISPLAYSURF, colours[1], cell.rRect)
                #if cell.l:
                #    pygame.draw.rect(DISPLAYSURF, colours[1], cell.lRect)
                #print "Drawing at", i.xPos, i.yPos
                #print colours[0]

    def activateCell(self, xPos, yPos):
        cell = self.array[xPos][yPos]
        if not cell.active:
            cell.active = True
            if cell.u:
                if cell.yPos > 0:
                    self.activateCell(xPos, yPos-1)
            if cell.d:
                if cell.yPos < self.height-1:
                    self.activateCell(xPos, yPos+1)
            if cell.r:
                if cell.xPos < self.width-1:
                    self.activateCell(xPos+1, yPos)
            if cell.l:
                if cell.xPos > 0:
                    self.activateCell(xPos-1, yPos)
          
    def checkComplete(self):
        for row in self.array:
            for cell in row:
                if not cell.active:
                    return False
        return True

    def deactivateCells(self):
        for row in self.array:
            for cell in row:
                cell.active = False

    def updateGrid(self):
        print "UPDATING GRID"


def main():
    global DISPLAYSURF, mousex, mousey
    pygame.init()
    clicks = 0
    g = Grid(80, 80)
    DISPLAYSURF = pygame.display.set_mode((W_HEIGHT, W_WIDTH))
    g.displayGrid()
    while True:
        DISPLAYSURF.fill(bgColour)
        g.displayGrid()
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_q:
                    raise SystemExit
            if e.type == MOUSEMOTION:
                mousex, mousey = e.pos
            if e.type == MOUSEBUTTONUP:
                mousex, mousey = e.pos
                for row in g.array:
                    for cell in row:
                        if cell.mainRect.collidepoint( (mousex, mousey) ):
                            print "Cell at", cell.xPos, cell.yPos, "hit!"
                            if e.button == 1:
                                #cell.active = True
                                if not cell.active:  
                                    g.activateCell(cell.xPos, cell.yPos)
                                    clicks += 1

                            elif e.button == 3:
                                if cell.active:
                                    cell.active = False
                                    clicks += 1
                            if g.checkComplete():
                                print "You filled the grid in", clicks, "clicks!"
                                clicks = 0
                                g.deactivateCells()
                                #raise SystemExit

        pygame.display.update()
        
                    


if __name__ == '__main__':
    main()
