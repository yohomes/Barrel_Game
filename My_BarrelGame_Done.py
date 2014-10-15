__author__ = 'Scott'
#First real game made on my own. Was supposed to be modular, but it doesn't work well once you change variables
#Changed barreldiameter to make it bigger, but it can be smaller and still work
#12 red, 12 blue, 36 ( 6 x 6 )
#After a row is destroyed, put 3 of each in
#Try having redbarrel and player as sprites and blueplayer/bluebarrel as rects/circles?
import pygame, random, sys, os
import pygame.locals
pygame.init()

# ---------- CONSTANTS ----------
WINDOWWIDTH  = 640 #DEFAULT 640
WINDOWHEIGHT = 480 #DEFAULT 480
FPS = 30 # frames per second, the general speed of the program
BOARDWIDTH = 6
BOARDHEIGHT = 6


#              R    G    B
GRAY       = (100, 100, 100)
NAVYBLUE   = ( 60,  60, 100)
WHITE      = (255, 255, 255)
RED        = (255,   0,   0)
GREEN      = (  0, 255,   0)
BLUE       = (  0,   0, 255)
YELLOW     = (255, 255,   100)
ORANGE     = (255, 128,   0)
PURPLE     = (255,   0, 255)
CYAN       = (  0, 255, 255)
BROWN      = (170,  70,   0)
LIGHTBROWN = (255,  240,   110)
BLACK      = (  0,   0,   0)


REDBARREL  = "redbarrel"
BLUEBARREL = "bluebarrel"
FONT = pygame.font.SysFont('name', 48)
'''
try:
    FONT = pygame.font.Font("C:/Windows/Fonts/PER_____.ttf", 48)
except:
    FONT = pygame.font.SysFont(48)

'''


# ---------- FUNCTIONS (WORKING)----------
def makeText(text, color, bgcolor, left, top):
    """Create a surface with text on it and a rectangle. Return them"""
    textSurface = FONT.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.topleft = (left, top)
    return (textSurface, textRect)
def terminate():
    pygame.quit()
    sys.exit()
# ---------- FUNCTIONS (UNFINISHED)----------

# ---------- INITIALIZATION ----------

clock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

background = pygame.Surface(DISPLAYSURF.get_size())
background.fill(LIGHTBROWN)
DISPLAYSURF.blit(background, (0, 0))


# ---------- CLASSES ----------
#Each class is a different state of the game (screens)
# ==================== GAME ====================
class Game(object):
    class redPlayer(pygame.sprite.Sprite): #Probably should have made a base player class and inherited from it, oh well
        def __init__(self, XMARGIN, YMARGIN, GRIDSIZE, OUTSIDEPADDING, FROMBOARD): #GRIDSIZE is the barrel diameter
            pygame.sprite.Sprite.__init__(self)
            self.OUTSIDEPADDING = OUTSIDEPADDING
            self.XMARGIN = XMARGIN
            self.YMARGIN = YMARGIN
            self.FROMBOARD = FROMBOARD
            self.GRIDSIZE = GRIDSIZE
            self.x = XMARGIN + OUTSIDEPADDING
            self.y = YMARGIN - self.FROMBOARD
            self.image = pygame.Surface([ GRIDSIZE * 0.8, GRIDSIZE * 0.8])
            self.image.fill(RED)
            self.rect = pygame.Rect(self.x, self.y, GRIDSIZE, GRIDSIZE)
            self.update = False
            self.MOVERIGHT = False
            self.MOVELEFT = False
        def updaterect(self):
            if self.update== True and self.MOVERIGHT == True:
                self.rect.left += 5
            if self.update== True and self.MOVELEFT == True:
                self.rect.left -= 5
            #Check if out of the board bounds
            if self.rect.left < self.XMARGIN:
                self.rect.left = self.XMARGIN
            if self.rect.right > WINDOWWIDTH - self.XMARGIN:
                self.rect.right = WINDOWWIDTH - self.XMARGIN
    class bluePlayer(pygame.sprite.Sprite):
        def __init__(self, XMARGIN, YMARGIN, GRIDSIZE, OUTSIDEPADDING, FROMBOARD): #GRIDSIZE is the barrel diameter
            pygame.sprite.Sprite.__init__(self)
            self.OUTSIDEPADDING = OUTSIDEPADDING
            self.XMARGIN = XMARGIN
            self.YMARGIN = YMARGIN
            self.FROMBOARD = FROMBOARD
            self.GRIDSIZE = GRIDSIZE
            self.x = XMARGIN - self.FROMBOARD
            self.y = YMARGIN + OUTSIDEPADDING
            self.image = pygame.Surface([ GRIDSIZE * 0.8, GRIDSIZE * 0.8])
            self.image.fill(BLUE)
            self.rect = pygame.Rect(self.x, self.y, GRIDSIZE, GRIDSIZE)
            self.update = False
            self.MOVEUP = False
            self.MOVEDOWN = False
        def update(self):
            self.updaterect()
        def updaterect(self):
            if self.update == True and self.MOVEUP == True:
                self.rect.top -= 5
            if self.update == True and self.MOVEDOWN == True:
                self.rect.top += 5
            #Check if out of the board bounds
            if self.rect.top < self.YMARGIN:
                self.rect.top = self.YMARGIN
            if self.rect.bottom > WINDOWHEIGHT - self.YMARGIN:
                self.rect.bottom = WINDOWHEIGHT - self.YMARGIN
    class blueRowRect(pygame.sprite.Sprite):
        def __init__(self, blueplayer, barreldiameter, gapsize, outsidepadding):
            pygame.sprite.Sprite.__init__(self)
            self.BLUEPLAYER = blueplayer
            self.GAPSIZE = gapsize
            self.OUTSIDEPADDING = outsidepadding
            self.BARRELDIAMETER = barreldiameter
            print(blueplayer.rect)
            self.ROW = 1
            self.image = pygame.Surface((BOARDWIDTH * (barreldiameter + gapsize) + outsidepadding * 2, (barreldiameter + gapsize + 2))) #Add two for extra thickness
            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
            #1.25 because the player is timesed by 0.8 of gridsize. Outsidepadding /2 because the line must be even between top/bottom
            self.rect = pygame.Rect(blueplayer.rect.left + blueplayer.FROMBOARD - gapsize - outsidepadding ,
                                    blueplayer.rect.top - (gapsize * 1.25) - (outsidepadding / 2),BOARDWIDTH *
                                    (barreldiameter + gapsize) + outsidepadding , (barreldiameter + gapsize))
            self.originalrect = self.rect.copy()
            pygame.draw.rect(self.image , BLUE, (0, 0, self.rect[2], self.rect[3]),2)
        def update(self):
            for y in range(0,BOARDHEIGHT + 1):
                if self.BLUEPLAYER.rect.center[1] > ((gameObj.YMARGIN - self.OUTSIDEPADDING / 2)
                                                   + (self.GAPSIZE  + self.BARRELDIAMETER) * y):
                    #self.rect.top = 20 * y
                    self.rect.top = gameObj.YMARGIN - gameObj.OUTSIDEPADDING * 2 + (gameObj.GAPSIZE + gameObj.BARRELDIAMETER) * y
                    self.ROW = y


    class redColRect(pygame.sprite.Sprite):
        def __init__(self, redplayer, barreldiameter, gapsize, outsidepadding):
            pygame.sprite.Sprite.__init__(self)
            #self.REDPLAYER = redplayer
            self.GAPSIZE = gapsize
            self.REDPLAYER = redplayer
            self.OUTSIDEPADDING = outsidepadding
            self.BARRELDIAMETER = barreldiameter
            self.COL = 0
            self.image = pygame.Surface((barreldiameter + gapsize + 2, BOARDHEIGHT * (barreldiameter + gapsize) + 4)) # add two and four so edges aren't thin

            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
            #1.25 because the player is timesed by 0.8 of gridsize. Outsidepadding /2 because the line must be even between top/bottom
            #self.rect = pygame.Rect(blueplayer.rect.left + blueplayer.FROMBOARD - gapsize - outsidepadding ,
            #                        blueplayer.rect.top - (gapsize * 1.25) - (outsidepadding / 2),
            #                        BOARDWIDTH * (barreldiameter + gapsize) + outsidepadding,
            #                       (barreldiameter + gapsize))
            self.rect = pygame.Rect((redplayer.rect.left - gapsize * 1.25,
                                     redplayer.rect.top + redplayer.FROMBOARD - self.OUTSIDEPADDING * 2,
                                     (barreldiameter + gapsize),
                                     (BOARDHEIGHT) * (barreldiameter + gapsize) + outsidepadding))

            self.originalrect = self.rect.copy()
            pygame.draw.rect(self.image , RED, (0, 0, self.rect[2], self.rect[3]),2)
        def update(self):
            for x in range(0,BOARDWIDTH + 1):
                if self.REDPLAYER.rect.center[0] > ((gameObj.XMARGIN - gameObj.OUTSIDEPADDING / 2 )
                                                   + (self.GAPSIZE  + self.BARRELDIAMETER) * x):
                    self.rect.left = gameObj.XMARGIN - gameObj.OUTSIDEPADDING * 2  + (gameObj.GAPSIZE + gameObj.BARRELDIAMETER) * x
                    #self.rect.top = gameObj.YMARGIN - gameObj.OUTSIDEPADDING * 2 + (gameObj.GAPSIZE + gameObj.BARRELDIAMETER) * y
                    self.COL = x
        def returnCol(self):
            return self.COL


    def __init__(self):
        self.board = self.getBoard()
        self.initialBarrels()
        self.BGCOLOR = LIGHTBROWN
        self.TEXTCOLOR = WHITE
        self.BARRELDIAMETER = 50 #DEFAULT 36. Works good with any number really
        self.GAPSIZE = 4 #DEFAULT 4. CAUSES ERRORS IF IT IS CHANGED FROM 4. NEED TO FIX THAT :(
        self.XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (self.BARRELDIAMETER + self.GAPSIZE))) / 2)
        self.YMARGIN = int(( WINDOWHEIGHT - (BOARDHEIGHT * (self.BARRELDIAMETER + self.GAPSIZE))) / 2)
        self.OUTSIDEPADDING = 2 #DEFAULT 2.Keep this at 1 or 2, otherwise messes up the whole board
        self.GRIDWIDTH = 1 #DEFAULT 1
        self.FROMBOARD = self.BARRELDIAMETER + 4 #DEFAULT 40. Distance the players will be from the board
        self.REDPLAYER = self.redPlayer(self.XMARGIN, self.YMARGIN, self.BARRELDIAMETER, self.OUTSIDEPADDING, self.FROMBOARD)
        self.BLUEPLAYER = self.bluePlayer(self.XMARGIN, self.YMARGIN, self.BARRELDIAMETER, self.OUTSIDEPADDING, self.FROMBOARD)
        self.PLAYERS = pygame.sprite.Group()
        self.PLAYERS.add(self.REDPLAYER)
        self.PLAYERS.add(self.BLUEPLAYER)
        self.BLUEROW = self.blueRowRect(self.BLUEPLAYER, self.BARRELDIAMETER, self.GAPSIZE, self.OUTSIDEPADDING)
        self.REDCOL = self.redColRect(self.REDPLAYER, self.BARRELDIAMETER, self.GAPSIZE, self.OUTSIDEPADDING)
        self.SELECTIONS = pygame.sprite.Group()
        self.SELECTIONS.add(self.BLUEROW)
        self.SELECTIONS.add(self.REDCOL)
        for x in self.board:
            print(x)
        self.HOLDINGSPACE = False
        self.score = 0
    def get_input(self):
        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and self.HOLDINGSPACE == False:
                    self.REDPLAYER.update = True
                    self.REDPLAYER.MOVERIGHT = True
                if event.key == pygame.K_LEFT and self.HOLDINGSPACE == False:
                    self.REDPLAYER.update = True
                    self.REDPLAYER.MOVELEFT = True
                if event.key == pygame.K_UP and self.HOLDINGSPACE == False:
                    self.BLUEPLAYER.update = True
                    self.BLUEPLAYER.MOVEUP = True
                if event.key == pygame.K_DOWN and self.HOLDINGSPACE == False:
                    self.BLUEPLAYER.update = True
                    self.BLUEPLAYER.MOVEDOWN = True
                if event.key == pygame.K_SPACE:
                    self.HOLDINGSPACE = True
                    self.BLUEPLAYER.MOVEDOWN = False
                    self.BLUEPLAYER.MOVEUP =False
                    self.REDPLAYER.MOVELEFT = False
                    self.REDPLAYER.MOVERIGHT = False
                    self.REDPLAYER.update = False
                    self.BLUEPLAYER.update = False
                if event.key == pygame.K_UP and self.HOLDINGSPACE == True:
                    times = 0
                    while times<6:
                        self.shiftColUp()
                        times += 1
                if event.key == pygame.K_DOWN and self.HOLDINGSPACE == True:
                    times = 0
                    while times < 6:
                        self.shiftColDown()
                        times += 1
                if event.key == pygame.K_RIGHT and self.HOLDINGSPACE == True:
                    times = 0
                    while times < 6:
                        self.shiftRowRight()
                        times += 1
                if event.key == pygame.K_LEFT and self.HOLDINGSPACE == True:
                    times = 0
                    while times < 6:
                        self.shiftRowLeft()
                        times += 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.REDPLAYER.update = False
                    self.REDPLAYER.MOVERIGHT = False
                if event.key == pygame.K_LEFT:
                    self.REDPLAYER.update = False
                    self.REDPLAYER.MOVELEFT = False
                if event.key == pygame.K_UP:
                    self.BLUEPLAYER.update = False
                    self.BLUEPLAYER.MOVEUP = False
                if event.key == pygame.K_DOWN:
                    self.BLUEPLAYER.update = False
                    self.BLUEPLAYER.MOVEDOWN = False
                if event.key == pygame.K_SPACE:
                    self.HOLDINGSPACE = False

    def process_events(self):
        pass
    def run_logic(self):

        self.BLUEPLAYER.updaterect()
        self.BLUEROW.update()
        self.REDPLAYER.updaterect()
        self.REDCOL.update()
        for col in range(0,BOARDHEIGHT):
            self.checkColorColumn(BLUEBARREL, col)
            self.checkColorColumn(REDBARREL,  col)
        for row in range(0,BOARDWIDTH):
            self.checkColorRow(BLUEBARREL, row)
            self.checkColorRow(REDBARREL, row)

        return GAME
    def checkColorColumn(self, color, col):
        for y in range(0,BOARDHEIGHT):
            if y != 6:
                if self.board[col][y] != color:
                    return False
        pygame.time.delay(1500)
        self.score += 1
        self.newCol(col)
    def newCol(self, col):
        newcolors = [BLUEBARREL, BLUEBARREL, BLUEBARREL, REDBARREL, REDBARREL, REDBARREL]
        random.shuffle(newcolors)
        random.shuffle(newcolors)
        for y in range(0, BOARDHEIGHT):
            if y != 6:
                self.board[col][y] = newcolors[y]
    def checkColorRow(self,color, row):
        for x in range(0, BOARDWIDTH):
            if x != 6:
                if self.board[x][row] != color:
                    return  False
        pygame.time.delay(1500)
        self.score += 1
        self.newRow(row)
    def newRow(self, row):
        newcolors = [BLUEBARREL, BLUEBARREL, BLUEBARREL, REDBARREL, REDBARREL, REDBARREL]
        random.shuffle(newcolors)
        random.shuffle(newcolors)
        for x in range(0, BOARDWIDTH):
            if x != 6:
                self.board[x][row] = newcolors[x]

    def drawscreen(self):
        pygame.display.set_caption("Barrel Game. Game State")
        DISPLAYSURF.fill(self.BGCOLOR)
        self.drawBarrels()
        self.drawGrid()
        self.PLAYERS.draw(DISPLAYSURF)
        self.SELECTIONS.draw(DISPLAYSURF)
        scoreSurf, scoreRect = makeText(str(self.score), BLACK, self.BGCOLOR, 10, 10)

        DISPLAYSURF.blit(scoreSurf, scoreRect)
    def shiftColUp(self):
        COL = self.redColRect.returnCol(self.REDCOL)
        for con in range(0, BOARDHEIGHT): #BOARDHEIGHT OR BOARDWIDTH?
            if con != 0:
                if self.board[COL][con] != None and self.board[COL][con-1] == None:
                    self.board[COL][con-1] = self.board[COL][con]
                    self.board[COL][con] = None
    def shiftColDown(self):
        COL = self.redColRect.returnCol(self.REDCOL)
        for Y in range(0, BOARDHEIGHT - 1):
            if self.board[COL][Y] != None and self.board[COL][Y+1] == None:
                self.board[COL][Y+1] = self.board[COL][Y]
                self.board[COL][Y] = None
    def shiftRowRight(self):
        ROW = self.BLUEROW.ROW
        for X in range(0, BOARDWIDTH):
            if X != 5:
                if self.board[X][ROW] != None and self.board[X+1][ROW] == None:
                    self.board[X+1][ROW] = self.board[X][ROW]
                    self.board[X][ROW] = None
    def shiftRowLeft(self):
        ROW = self.BLUEROW.ROW
        for X in range(0, BOARDWIDTH):
            if X != 5:
                if self.board[X][ROW] == None and self.board[X+1][ROW] != None:
                    self.board[X][ROW] = self.board[X+1][ROW]
                    self.board[X+1][ROW] = None

    def drawBarrels(self):
        for barrelx in range(BOARDWIDTH):
            for barrely in range(BOARDHEIGHT):
                if self.board[barrelx][barrely] != None:
                    left, top = self.topLeftOfBarrel(barrelx, barrely)
                    if self.board[barrelx][barrely] == BLUEBARREL:
                        self.drawBarrel(left, top, BLUE)
                    else:
                        self.drawBarrel(left, top, RED)
    def drawBarrel(self, left, top, color):
        pygame.draw.circle(DISPLAYSURF, color, (int(left + self.BARRELDIAMETER /2), int(top + self.BARRELDIAMETER / 2)), int(self.BARRELDIAMETER / 2))
    def drawGrid(self):
        left, top = self.topLeftOfBarrel(0,0)
        left -= self.OUTSIDEPADDING
        top -= self.OUTSIDEPADDING
        pygame.draw.rect(DISPLAYSURF, BLACK, (left - self.OUTSIDEPADDING, top - self.OUTSIDEPADDING , BOARDWIDTH * (self.GAPSIZE + self.BARRELDIAMETER) + self.OUTSIDEPADDING,BOARDHEIGHT * (self.GAPSIZE + self.BARRELDIAMETER) + self.OUTSIDEPADDING ), self.GRIDWIDTH)
        for barrelx in range(1, BOARDWIDTH):
            pygame.draw.line(DISPLAYSURF, BLACK, ((self.XMARGIN + (self.GAPSIZE + self.BARRELDIAMETER) * barrelx) - self.GAPSIZE / 2 - 1, self.YMARGIN - self.OUTSIDEPADDING * 2), (((self.XMARGIN + (self.GAPSIZE + self.BARRELDIAMETER) * barrelx) - self.GAPSIZE / 2 - 1) , self.YMARGIN + (self.BARRELDIAMETER + self.GAPSIZE) * BOARDHEIGHT - self.OUTSIDEPADDING * 2) , self.GRIDWIDTH)
        for barrely in range(1, BOARDHEIGHT):
            pygame.draw.line(DISPLAYSURF, BLACK, ((self.XMARGIN - self.OUTSIDEPADDING * 2, self.YMARGIN + ( self.GAPSIZE + self.BARRELDIAMETER) * barrely - self.GAPSIZE / 2 - 1)),((WINDOWWIDTH - self.XMARGIN - self.OUTSIDEPADDING * 2, self.YMARGIN + ( self.GAPSIZE + self.BARRELDIAMETER) * barrely - (self.GAPSIZE / 2) - 1 )) , self.GRIDWIDTH)
        #left = barrelx * (self.BARRELDIAMETER + self.GAPSIZE) + self.XMARGIN
        #top = barrely * (self.BARRELDIAMETER + self.GAPSIZE) + self.YMARGIN
        #return (left, top)
    def topLeftOfBarrel(self, barrelx, barrely):
        left = barrelx * (self.BARRELDIAMETER + self.GAPSIZE) + self.XMARGIN
        top = barrely * (self.BARRELDIAMETER + self.GAPSIZE) + self.YMARGIN
        return (left, top)
    def initialBarrels(self):
        """Randomly places 12 red and 12 blue barrels"""
        toPlaceRed  = 12
        toPlaceBlue = 12
        while toPlaceBlue != 0:
            for x in range(BOARDWIDTH):
                for y in range(BOARDHEIGHT):
                    #oneTenth makes a random variable and compares it to 5, that way there is a 10% chance of
                    #It being placed and it is 'random'
                    oneTenth = random.randint(0,10)


                    if self.board[x][y] == None and oneTenth == 5:
                        if toPlaceBlue != 0:
                            self.board[x][y] = BLUEBARREL
                            toPlaceBlue -= 1

        #For some reason using toPlaceRed in the above code didn't work, so I had to split it up
        while toPlaceRed != 0:
            for x in range(BOARDWIDTH):
                for y in range(BOARDHEIGHT):
                    oneTenth = random.randint(0,10)


                    if self.board[x][y] == None and oneTenth == 5:
                        if toPlaceRed != 0:
                            self.board[x][y] = REDBARREL
                            toPlaceRed -= 1
    def getBoard(self):
        """Create our initial board and return it"""
        board = []
        for x in range(BOARDWIDTH):
            row = []
            for y in range(BOARDHEIGHT):
                row.append(None)
            board.append(row)
        return board
# ==================== MENU ====================
class Menu(object):
    def __init__(self):
        self.BGCOLOR = YELLOW
        self.TEXTCOLOR = BLACK
        pygame.display.set_caption("Barrel Game. Menu Screen.")
        self.playText, self.playRect = makeText("Play game", self.TEXTCOLOR, self.BGCOLOR, 150, 100)
        self.instructionsText, self.instructionsRect = makeText("Instructions", self.TEXTCOLOR, self.BGCOLOR, 150, 200)
        self.quitText, self.quitRect = makeText("Quit", self.TEXTCOLOR, self.BGCOLOR, 150, 300)
        self.mousex = 0
        self.mousey = 0
        self.drawButton = False #Draw a rectangle around the 'button'?
        self.currentrect = None
        self.changeState = False
        self.newstate = 'menu'
    def get_input(self):
        self.changeState = False
        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                terminate()
            if event.type == pygame.MOUSEMOTION:
                self.mousex, self.mousey = event.pos
            self.changeState = False #Reset so they can't click in another button, Make a new function to reset all vars?
            if event.type == pygame.MOUSEBUTTONDOWN and self.currentrect != None:
                self.changeState = True
    def process_events(self):
        #self.currentrect = None
        #If a rect is returned by checkInRect, store it in currentrect, if the mouse isn't in a rect, return None
        self.currentrect = self.checkInRect()
        if self.currentrect != None:
            self.drawButton = True
        else:
            self.drawButton = False
    def run_logic(self):
        if self.changeState == True:
            if self.currentrect == self.playRect:
                return GAME
            if self.currentrect == self.instructionsRect:
                return INSTRUCTIONS
            if self.currentrect == self.quitRect:
                terminate()
        return MENU
    def drawscreen(self):
        pygame.display.set_caption("Barrel Game. Menu State")
        DISPLAYSURF.fill(self.BGCOLOR)
        DISPLAYSURF.blit(self.playText, self.playRect)
        DISPLAYSURF.blit(self.instructionsText, self.instructionsRect)
        DISPLAYSURF.blit(self.quitText, self.quitRect)
        if self.drawButton == True:
            #Draw a rectangle around the text for our button
            copyrect = self.currentrect
            pygame.draw.rect(DISPLAYSURF, BLACK, (copyrect[0] - 6, copyrect[1] - 6, copyrect[2] + 6, copyrect[3] + 6) ,  2)

    def checkInRect(self):
        """Used to check if the mouse has entered a 'button' to draw a box around the button"""
        for rect in [self.playRect, self.instructionsRect, self.quitRect]:
            if rect.collidepoint((self.mousex, self.mousey)):
                return rect
        return None

class Instructions(object):
    def __init__(self):

        self.BGCOLOR = YELLOW
        self.TEXTCOLOR = BLACK

        self.backText, self.backRect = makeText("Back", self.TEXTCOLOR, self.BGCOLOR, 5, WINDOWHEIGHT * 0.85  )

        self.mousex = 0
        self.mousey = 0
        self.drawButton = False #Draw a rectangle around the 'button'?
        self.currentrect = None
        self.changeState = False
        self.INSTRUCTIONS= self.InstructImage()
        self.SPRITES = pygame.sprite.Group()
        self.SPRITES.add(self.INSTRUCTIONS)
    class InstructImage(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("Instructions.png")
            self.rect = self.image.get_rect()
    def get_input(self):
        self.changeState = False
        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                terminate()
            if event.type == pygame.MOUSEMOTION:
                self.mousex, self.mousey = event.pos
            self.changeState = False #Reset so they can't click in another button, Make a new function to reset all vars?
            if event.type == pygame.MOUSEBUTTONDOWN and self.currentrect != None:
                self.changeState = True
    def process_events(self):

        #If a rect is returned by checkInRect, store it in currentrect, if the mouse isn't in a rect, return None
        self.currentrect = self.checkInRect()
        if self.currentrect != None:
            self.drawButton = True
        else:
            self.drawButton = False

    def run_logic(self):
        if self.changeState == True:
            if self.currentrect == self.backRect:
                return MENU


        return INSTRUCTIONS

    def drawscreen(self):
        pygame.display.set_caption("Barrel Game. Instructions Screen.")
        DISPLAYSURF.fill(self.BGCOLOR)
        DISPLAYSURF.blit(self.backText, self.backRect)
        self.SPRITES.draw(DISPLAYSURF)
        if self.drawButton == True:
            #Draw a rectangle around the text for our button
            copyrect = self.currentrect
            pygame.draw.rect(DISPLAYSURF, BLACK, (copyrect[0] - 6, copyrect[1] - 6, copyrect[2] + 6, copyrect[3] + 6) ,  2)
    def checkInRect(self):
        """Used to check if the mouse has entered a 'button' to draw a box around the button"""

        if self.backRect.collidepoint((self.mousex, self.mousey)):
            return self.backRect
        return None
gameObj = Game()
menuObj = Menu()
insObj = Instructions()
#States is a dictionary of our three different screens, the main menu, instructions, and than the game screen
MENU = "menu"
GAME = "game"
INSTRUCTIONS = "instructions"
states = {"menu": menuObj, "game": gameObj, "instructions": insObj}

# ---------- MAIN GAME LOOP ----------

def main():

    state = states[MENU]


    while True:
        state.get_input()
        state.process_events()
        #Theres an era here I can't explain. Can not have state.run_logic() return a new state to be used or it will crash
        #Must actually send back a string and use the dictionary.
        newstate = state.run_logic()
        state = states[newstate]
        state.drawscreen()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()

pygame.quit()
sys.exit()
