
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

pygame.mixer.pre_init(44100, -16, 2, 2048) # warms up the sound tubes
pygame.init()
pygame.font.init

screen = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('THAT WHICH RUNS DOES NOT FALL')

clock = pygame.time.Clock()
tick = clock.tick(60) # this doesn't anything here, try it in the game loop

# Helper functions
############################################################

def rotate(lst):
    lst[:] = lst[1:] + [lst[0]]

def getImage(path):
    image = pygame.image.load(path)
    return image
    global _image_library
    image = _image_library.get(path)
    if image == None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path)
            _image_library[path] = image
    return image

def playSound(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

class Random():
    def Height():
        return random.randint(1,6)*50

    def Width():
        return random.randint(8,15)*40

    def Gap():
       return random.randint(4,8)*20

    def YPos():
        return random.randint(20,55)*10

class Data():
    def __init__(self):
        pass

    Buildings = []

    Y_Change = 0
    time = 0
    Initial_Velocity = 0
    
    T = 0
    Metres = 0
    Building_Speed = 15
    Gravity = -2

# Visible Objects
############################################################

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Text():
    def __init__(self, text, fnt, size, xcoord, ycoord,color):
        self.text = text
        self.fnt = fnt
        self.size = size
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.color = color
    def text_objects(self,font):
        textSurface = font.render(self.text, True, self.color)
        return textSurface, textSurface.get_rect()
    
    def Write(self):
        Texty = pygame.font.Font(self.fnt,self.size)
        TextSurf, TextRect = self.text_objects(Texty)
        TextRect.topright = ((self.xcoord,self.ycoord))
        screen.blit(TextSurf,TextRect)


class Building(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = getImage('building_left.png')
        self.rect = pygame.Rect(x, y, height, width)
        self.color = color
        self.gap = Random.Gap()
        self.name = 0

        self.tileStart = 0
        tileWidth = 40
        if width <= tileWidth:
            self.image = pygame.transform.scale(self.image, (w, height))
        elif width > tileWidth:
            self.image = pygame.Surface([width, height])
            while self.tileStart < width:
                if self.tileStart == 0:
                    self.image.blit(getImage('building_left.png'), (self.tileStart, 0))
                elif self.tileStart > width - tileWidth - 1:
                    self.image.blit(getImage('building_right.png'), (self.tileStart, 0))
                else:
                    self.image.blit(getImage('building_center.png'), (self.tileStart, 0))
                self.tileStart += tileWidth

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def CrashRect(self):
        return pygame.Rect(self.rect.x, self.rect.y, 5 ,self.rect.height)
    
    def ShowCrashRect(self):
        pygame.draw.rect(screen,BLUE,self.CrashRect())

class Robot(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.rect = pygame.Rect(x, y, height, width)
        self.color = color

        self.images = []
        self.images.append(getImage('sprites/run_1.png'))
        self.images.append(getImage('sprites/run_2.png'))
        self.images.append(getImage('sprites/run_3.png'))
        self.images.append(getImage('sprites/run_2.png'))

        self.jumpImages = []
        self.jumpImages.append(getImage('sprites/jump_1.png'))
        self.jumpImages.append(getImage('sprites/jump_2.png'))
        self.jumpImages.append(getImage('sprites/jump_3.png'))
        self.jumpImages.append(getImage('sprites/jump_4.png'))
        self.jumpImages.append(getImage('sprites/jump_5.png'))
        self.jumpImages.append(getImage('sprites/jump_6.png'))
        self.jumpImages.append(getImage('sprites/jump_7.png'))
        self.jumpImages.append(getImage('sprites/jump_8.png'))
        
        self.index = 0
        self.image = self.images[self.index]

    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''

        imageList = self.images
        if Data.Initial_Velocity > 0 :
            imageList = self.jumpImages
            
        
        imageTicks = 5 # number of loops each animation frame shows for
        self.index += 1
        if self.index >= len(imageList)*imageTicks:
            self.index = 0
        imageCount = int(self.index/imageTicks)
        self.image = imageList[imageCount]

        if self.rect.width < self.image.get_rect().width:
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))



# Object creation
############################################################

# TODO: make into a function to facilitate restart

background = Background('background.png', [0,0])

for i in range(0,5):
    startX = 0
    if len(Data.Buildings) > 0:
        lastBuilding = Data.Buildings[-1]        
        startX = lastBuilding.rect.x + lastBuilding.rect.width

    building = Building(startX + Random.Gap(), Random.YPos(), Random.Width(), 600, BLACK) #creates the Buildings
    building.name = i
    Data.Buildings.append(building)

building_group = pygame.sprite.Group(Data.Buildings)


robot = Robot(20,100,60,60,BLUE)
robot_group = pygame.sprite.Group(robot)

# calculation functions
############################################################

def calcBuildingsPos():
    # move first building to the back if it has gone offscreen
    firstBuilding = Data.Buildings[0]
    if firstBuilding.rect.x < -firstBuilding.rect.width: 
        firstBuilding.gap = Random.Gap()
        rotate(Data.Buildings)  #moves rects to the back of the queue

    previousBuilding = Data.Buildings[0]
    for building in Data.Buildings:
        # print("building " + str(building.name) + " at " + str(building.rect))
        if building == previousBuilding:
            building.rect.x -= Data.Building_Speed
        else:
            building.rect.x = previousBuilding.rect.x + previousBuilding.rect.width + previousBuilding.gap
        previousBuilding = building

def calcRobotPos():
    Data.T += 1
    Data.Y_Change = (Data.Initial_Velocity) + (Data.Gravity*Data.T)
    #print("Data T:" + str(Data.T) + ", y change:" + str(Data.Y_Change))
    robot.rect.y -= Data.Y_Change
    #print("Robot:" + str(robot.rect))

def checkCollisions():
    for building in Data.Buildings:
        if robot.rect.colliderect(building.rect):
            print("collision with building " + str(building.name))
            robot.rect.y = building.rect.y-robot.rect.height-1
            Data.T = 0
            Data.Initial_Velocity = 0

def frames():
    Data.Metres += 1
    Score = Text(str(Data.Metres) + "m",'freesansbold.ttf',30,750,50,BLACK)  #prints the score on the screen
    Score.Write()

    calcBuildingsPos()

    calcRobotPos()

    checkCollisions()

    if Data.T==0 and event.type == pygame.KEYDOWN and event.key == pygame.K_UP: #makes the robot jump
        print("jump")
        Data.T = 0
        Data.Initial_Velocity = 25
    if event.type == pygame.KEYDOWN and event.key == pygame.K_p: #if we need to retreive the robot goes off screen
        print("reset")
        robot.rect = pygame.Rect(20,100,30,30)
        Data.T = 0
        Data.Initial_Velocity = 25
         
    screen.fill(BLACK)
    screen.blit(background.image, background.rect)

    robot_group.update()
    robot_group.draw(screen)
    building_group.update()
    building_group.draw(screen)
    for building in Data.Buildings:
        building.ShowCrashRect()
            
    pygame.display.flip()

# Run loop(s)
############################################################    
    
crashed = False

while not crashed:
    # TODO: make another loop for the gameplay, so you can pause
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    frames()
    
pygame.quit()
quit()



# Side wall collision
# put in images
# Start screen
# Death screen
# Pause screen
# Restart Function
# 
