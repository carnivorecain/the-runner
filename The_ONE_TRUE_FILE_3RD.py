import pygame
import math
import random
import sys
from pygame.locals import *

WIDTH = 800
HEIGHT = 600

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

pygame.mixer.pre_init(44100, -16, 2, 2048) # connects audio
pygame.init()
pygame.font.init

screen = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('THAT WHICH RUNS DOES NOT FALL')

clock = pygame.time.Clock()

# Global Attributes 
##################################

class Data():
    currentScreen = 0 # 0 is Start Screen, 1 is Playing, 2 is Game Over, 3 is Paused (Move paused to StartGame?)
    isGameOver = False
    pause = False

    Buildings = []
    explosion_group = pygame.sprite.Group()
    robotRect = pygame.Rect(0,0,0,0)
    
    robotYOrgin = 0 # JASON HERE 
    Y_Change = 0
    time = 0
    Jump_Velocity = 25
    
    T = 0
    Metres = 0
    Building_Speed = 600
    Gravity = -75
    Highscore = 0 

    MaxBuildingHeightDifference = 100
#KEY FUNCTIONS
    ############################################################
def rotate(lst): # rotates the buildings via a list
    lst[:] = lst[1:] + [lst[0]]

def getImage(path): # the point of this is?
    image = pygame.image.load(path)
    return image
    global _image_library
    image = _image_library.get(path)
    if image == None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path)
            _image_library[path] = image
    return image

def playSound(filename): # plays the sfx
    soundObj = pygame.mixer.Sound(filename)
    soundObj.play()

def playMusic(filename): # plays the music soundtrack
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
class Random(): # randomixer for building proportions
    def Height():
        return random.randint(1,6)*45 # may want to adjust numbers as there are times can't make the jump

    def Width():
        return random.randint(8,15)*40

    def Gap():
       return random.randint(10,20)*5

    def YPos(MaxHeight):
        newPos = random.randint(20,55)*10
        if newPos < MaxHeight:
            newPos = MaxHeight
        return newPos
            
# Visible Objects
############################################################

class Background(pygame.sprite.Sprite): # class for Background image
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file) # loading image
        self.rect = self.image.get_rect() # background rect
        self.rect.left, self.rect.top = location # alignment? position?

class Text():
    def __init__(self, text, fnt, size, xcoord, ycoord,color):
        self.text = text
        self.fnt = fnt
        self.size = size
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.color = color
        
    def text_objects(self,font): # making a space for text?
        textSurface = font.render(self.text, True, self.color)
        return textSurface, textSurface.get_rect()
    
    def Write(self):# assuming writing for text need to explain?
        Texty = pygame.font.Font(self.fnt,self.size)
        TextSurf, TextRect = self.text_objects(Texty)
        TextRect.topright = ((self.xcoord,self.ycoord))
        screen.blit(TextSurf,TextRect)


class Building(pygame.sprite.Sprite): # Class for building
    def __init__(self, x, y, width, height):
        super().__init__() # calling sprite init
        self.rect = pygame.Rect(x, y, width, height)
        self.gap = Random.Gap() # assigns random gap size
        self.tileWidth = 40
        self.name = 0
        self.setup(x, y, width, height)

    def setup(self, x, y, width, height):
        tileStart = 0
        tileWidth = self.tileWidth
        #if width > tileWidth:
        self.image = pygame.Surface([width, height])
        while tileStart < width:
            if tileStart == 0:
                self.image.blit(getImage('building_left.png'), (tileStart, 0))
            elif tileStart > width - tileWidth - 1:
                self.image.blit(getImage('building_right.png'), (tileStart, 0))
            else:
                self.image.blit(getImage('building_center.png'), (tileStart, 0))
            tileStart += tileWidth

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def CrashRect(self): # rectangle for collisions 
        return pygame.Rect(self.rect.x, self.rect.y, 10 ,self.rect.height)

    # debug visualisation
    # def ShowCrashRect(self):
    #     pygame.draw.rect(screen,BLACK,self.CrashRect())

class Robot(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height): # standard construction of robot 
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.Initial_Velocity = 0.0 

        self.runImages = [] # list for the running animation 
        self.runImages.append(getImage('run_1.png'))
        self.runImages.append(getImage('run_2.png'))
        self.runImages.append(getImage('run_3.png'))
        self.runImages.append(getImage('run_2.png'))

        self.jumpImages = [] # list for the jumping animation
        self.jumpImages.append(getImage('jump_1.png'))
        self.jumpImages.append(getImage('jump_2.png'))
        self.jumpImages.append(getImage('jump_3.png'))
        self.jumpImages.append(getImage('jump_4.png'))
        self.jumpImages.append(getImage('jump_5.png'))
        self.jumpImages.append(getImage('jump_6.png'))
        self.jumpImages.append(getImage('jump_7.png'))
        self.jumpImages.append(getImage('jump_8.png'))

        self.index = 0
        self.image = self.runImages[self.index]

    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''

        imageList = self.runImages
        if self.Initial_Velocity > 0 :
            imageList = self.jumpImages
            # when you jump, you need to reset the index to 0 # 
        
        imageTicks = 5 # number of loops each animation frame shows for
        self.index += 1
        if self.index >= len(imageList)*imageTicks:
            self.index = 0
        imageCount = int(self.index/imageTicks)
        self.image = imageList[imageCount]

        if self.rect.width < self.image.get_rect().width:
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

        if self.rect.y>= 600:# this checks for falling game over
            print("robot has fallen down")
            showGameOver()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height): # standard construction of robot 
        super().__init__()
        
        self.deathImages = [] # list for the explosion animation
        self.deathImages.append(getImage('explosion_1.png'))
        self.deathImages.append(getImage('explosion_2.png'))
        self.deathImages.append(getImage('explosion_3.png'))
        self.deathImages.append(getImage('explosion_4.png'))
        self.deathImages.append(getImage('explosion_5.png'))
        self.deathImages.append(getImage('explosion_6.png'))
        self.deathImages.append(getImage('explosion_7.png'))
        
        self.index = 0
        self.image = self.deathImages[self.index]

        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width/2 + 20
        self.rect.y = y - self.rect.height/2

    def update(self):
        print("updating boom at " + str(self.rect))
        imageList = self.deathImages
        imageTicks = 3 # number of loops each animation frame shows for
        self.index += 1
        if self.index >= len(imageList)*imageTicks:
            self.index = 0
        imageCount = int(self.index/imageTicks)
        self.image = imageList[imageCount]       

def showExplosion():
    #add sound effect
    if len(Data.explosion_group) < 1:
        explosion = Explosion(Data.robotRect.x, Data.robotRect.y, Data.robotRect.width, Data.robotRect.height)
        Data.explosion_group = pygame.sprite.Group(explosion)
    
def showGameOver(): # sprites for death and stops map
    # stop map
    # death animation sequence
    print("GAME OVER")
    Data.currentScreen = 2
    Data.isGameOver = True

def resetVariables():# no touch
    running = True
    Data.Building_Speed = 600
    Data.Metres = 0
    Data.robotYOrign = 0 # dont touch
    Data.explosion_group.empty()

def showPause():
    
    print("Pause")
    Data.Building_Speed=0
    screen.fill(WHITE)
    pausescreen = Text("Paused. Q to quit or SPACE to continue",'freesansbold.ttf',30,600,300,BLACK)
    pausescreen.Write()
    pygame.display.flip()

    while Data.pause == True:
        for event in pygame.event.get():
            print("in pause loop")
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE):
                print("break pause loop back to game")
                Data.pause = False
                Data.Building_Speed =600
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                print("quit from pause loop")
                pygame.quit()
                sys.quit()
                  
def runGame():
    #resetVariables() not needed here it is in the reset loop 
    

    # calculation functions
    ############################################################


    def calcBuildingsPos(tick):
        # move first building to the back if it has gone offscreen
        firstBuilding = Data.Buildings[0] # retrieves the first building in a list
        if firstBuilding.rect.x < -firstBuilding.rect.width: #if x position of building is its entire width offscreen...
            maxHeight = Data.Buildings[0].rect.y - Data.MaxBuildingHeightDifference
            firstBuilding.setup(800, Random.YPos(maxHeight), Random.Width(), 600)
            firstBuilding.gap = Random.Gap() # ... set a new random gap
            rotate(Data.Buildings)  #moves rects to the back of the queue

        previousBuilding = Data.Buildings[0] # variable to compare previous building to new one
        for building in Data.Buildings: #loop through all buildings
            if building == Data.Buildings[0]: # if building is 1st building...
                building.rect.x -= Data.Building_Speed * tick / 1000.0 # move building based off time
            else:
                building.rect.x = previousBuilding.rect.x + previousBuilding.rect.width + previousBuilding.gap # reposition buildings based off the one before
            previousBuilding = building # set current building to previous building

    def collision2() :
        for building in Data.Buildings:
            if robot.rect.colliderect(building.CrashRect()) :        
                print("hits wall game over")
                robot.rect.x = building.rect.x - building.tileWidth
                Data.Building_Speed = 0
                # death animation
                    # death animation must delete robot
                    #and also run showgameover then does the gameover
                #showGameOver()
                showExplosion()
            elif robot.rect.colliderect(building.rect) and robot.rect.y:
                print("collision with building " + str(building.name))
                Data.robotYOrgin = robot.rect.y ########################
                robot.rect.y = building.rect.y-robot.rect.height
                Data.T = 0
                robot.Initial_Velocity = 0

    def calcRobotPos(tick):
        Data.T += tick / 1000.0
        print(Data.robotYOrgin)
        #robotYOrig = robot.rect.y  # makes variable for robot intial Y postion per tick  # JASON CHANGES EQUATION 
        Data.Y_Change = (robot.Initial_Velocity) + (Data.Gravity*Data.T)
        # print("Data T:" + str(Data.T) + ", y-change:" + str(Data.Y_Change))
        robot.rect.y -= Data.Y_Change
        Data.robotRect = robot.rect
        # print("Robot:" + str(robot.rect.y))



        


    # Object creation
    ############################################################
    background = Background('background.png', [0,0])

    building = Building(0, 400, 1520, 600) #hardcode first building with runway width
    Data.Buildings.append(building)        
    lastY = building.rect.y #for calculating if building height is too high to jump
    for i in range(0,4):
        lastBuilding = Data.Buildings[-1] #get last building we made     
        startX = lastBuilding.rect.x + lastBuilding.rect.width + Random.Gap() #new X position is where last building starts 


        building = Building(startX + Random.Gap(), Random.YPos(lastY - Data.MaxBuildingHeightDifference), Random.Width(), 600) #creates the Buildings
        #check if building can be jumped to
        lastY = building.rect.y
        building.name = i
        Data.Buildings.append(building)

    building_group = pygame.sprite.Group(Data.Buildings)


    #robot = Robot(5,0,60,60)
    robot = Robot(5, lastBuilding.rect.y-60,60,60)

    robot_group = pygame.sprite.Group(robot)
    clock.tick(60) # resets clock after restart

    while not Data.isGameOver:
        print("inside loop")
        
        tick = clock.tick(60) # gives time since last frame in ms
  
        calcBuildingsPos(tick) # calculate positions using tick to account for processing lag
        calcRobotPos(tick) # same as above
        collision2()
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if Data.T < 0.0001 and event.type == pygame.KEYDOWN and event.key == pygame.K_UP: #makes the robot jump
                print("jump")
                playSound("Jump.wav")
                robot.Initial_Velocity = Data.Jump_Velocity
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
                Data.pause = True
                print("pause")
                showPause()  
                #Data.currentScreen = 3 ?? maybe its not working as intended 
                #pause the meter counter
                #pause running animatoin
                # show pause screen
                 
                #pauseScreen stops and 
                #animatoin continues
                #meter counter continues

        screen.fill(BLACK)
        screen.blit(background.image, background.rect)

        
        building_group.update()
        building_group.draw(screen)
        robot_group.update()
        robot_group.draw(screen)
        Data.explosion_group.update()
        Data.explosion_group.draw(screen)
        
        Data.Metres += 1 # score section
        if Data.Highscore < Data.Metres :
            Data.Highscore = Data.Metres
        Score = Text("Highscore: " + str(Data.Highscore) + "m  / "+"Current Run: " +
                     str(Data.Metres) + "m",'freesansbold.ttf',30,750,50,WHITE)  #prints the score on the screen
        Score.Write()
                
        pygame.display.flip()

    building_group.empty()
    robot_group.empty()
    Data.Buildings = []

# Run loop(s)
#################################################################    
    
playMusic("MortalMachine.ogg")

running = True

flicker = 0.0 # Counter for changing the start screen background
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            sys.quit() # This is causing an error : module 'sys' has no attribute 'quit'
            
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_r) :
            Data.isGameOver = False
            resetVariables()
            runGame()
            
        while Data.pause == True:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
                Data.pause = False   
                #pauseScreen stops and 
                #animatoin continues
                #meter counter continues
            
            # Data.currentScreen = 1

    if Data.currentScreen == 0:
        flicker += clock.tick(60) # gives time since last frame in ms
        backgroundImage = 'Start_1.png'
        if flicker > 1000:
            backgroundImage = 'Start_2.png'
        if flicker > 2000:
            flicker = 0
        startScreen = Background(backgroundImage, [0,0])
        screen.fill(BLACK)
        screen.blit(startScreen.image, startScreen.rect)
        pygame.display.flip()

    elif Data.currentScreen == 2:
        screen.fill(WHITE)
        gameover = Text("Game Over. Q to quit R to restart",'freesansbold.ttf',30,600,300,BLACK)
        gameover.Write()
        pygame.display.flip()
        
    elif Data.currentScreen == 3:
        screen.fill(WHITE)
        pausescreen = Text("Paused. Q to quit or P to continue",'freesansbold.ttf',30,600,300,BLACK)
        pausescreen.Write()
        pygame.display.flip()

pygame.quit()

# gameover = Text("Game Over. Q to quit R to restart",'freesansbold.ttf',30,400,300,BLACK)
