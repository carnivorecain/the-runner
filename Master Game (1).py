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

# Key Functions
############################################################

def rotate(lst): # rotates the buildings in a list
    lst[:] = lst[1:] + [lst[0]]

def getImage(path): # what does this do ? seems pointless? 
    image = pygame.image.load(path)
    return image
    global _image_library
    image = _image_library.get(path)
    if image == None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path)
            _image_library[path] = image
    return image

def playSound(filename): # plays sound 
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

class Random(): # random building height width etc generator 
    def Height():
        return random.randint(1,6)*50

    def Width():
        return random.randint(8,15)*40

    def Gap():
       return random.randint(4,8)*20

    def YPos():
        return random.randint(20,55)*10

class Data(): # global variables? do we need? in a class can we no create when used?
    def __init__(self):
        pass
    
    Buildings = []
    Build_A_XPos = 0
    Build_A_Height = 600
    Build_A_YPos= Random.YPos()
    Build_A_Width = Random.Width()

    Build_B_XPos = Build_A_XPos + Build_A_Width + Random.Gap()
    Build_B_Height = 600
    Build_B_YPos = Random.YPos()
    Build_B_Width = Random.Width()

    Build_C_XPos = Build_B_XPos + Build_B_Width + Random.Gap()
    Build_C_Height = 600
    Build_C_YPos = Random.YPos()
    Build_C_Width = Random.Width()

    Y_Change = 0
    time = 0
    Initial_Velocity = 0
    Robot_YPos = 100 #HEIGHT - Original_Height_A - YLoc
    Robot_XPos = 20
    Robot_Width = 30
    Robot_Height = 30
    
    T = 0
    Metres = 0
    Building_Speed = 10
    Gravity = -2

# Visible Objects
############################################################

class Background(pygame.sprite.Sprite): # Background image class
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location # ?? this line?

class Text():
    def __init__(self, text, fnt, size, xcoord, ycoord,color):
        self.text = text
        self.fnt = fnt # font?
        self.size = size
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.color = color
        
    def text_objects(self,font): # this is?
        textSurface = font.render(self.text, True, self.color)
        return textSurface, textSurface.get_rect()
    
    def Write(self): # assumibily the write funtion for text 1 is there not already
        #               one and 2 what are these attributes
        Texty = pygame.font.Font(self.fnt,self.size)
        TextSurf, TextRect = self.text_objects(Texty)
        TextRect.topright = ((self.xcoord,self.ycoord))
        screen.blit(TextSurf,TextRect)


class Building(pygame.sprite.Sprite): # buidling class
    def __init__(self, x, y, width, height, color):# constructor
        super().__init__()
        self.image = getImage('building_left.png') # linking to image
        self.rect = pygame.Rect(x, y, height, width) # making it a rect
        self.color = color # color
        self.gap = Random.Gap()# gap from last building
        self.name = 0 #? point of this

        self.tileStart = 0 # location of start?
        tileWidth = 40 # size of tiles
        if width <= tileWidth:
            self.image = pygame.transform.scale(self.image, (w, height))
        elif width > tileWidth: # with an explainatoin of what tiles are makes sense
            self.image = pygame.Surface([width, height])# however we need to show where we learnt this
            while self.tileStart < width:
                if self.tileStart == 0:
                    self.image.blit(getImage('building_left.png'), (self.tileStart, 0))
                elif self.tileStart > width - tileWidth - 1:
                    self.image.blit(getImage('building_right.png'), (self.tileStart, 0))
                else:
                    self.image.blit(getImage('building_center.png'), (self.tileStart, 0))
                self.tileStart += tileWidth

        self.rect = self.image.get_rect() # possition of the building?
        self.rect.x = x 
        self.rect.y = y
    
    def CrashRect(self): # crash rectangle for wall game over 
        return pygame.Rect(self.rect.x, self.rect.y, 2 ,self.rect.height)
    
    def ShowCrashRect(self): # need to make this invisible
        pygame.draw.rect(screen,BLACK,self.CrashRect())

 

    

class Robot(pygame.sprite.Sprite): # robot class
    def __init__(self, x, y, width, height, color): # constructor
        super().__init__()
        self.rect = pygame.Rect(x, y, height, width) # roborect sizw
        self.color = color

        self.images = [] # sprites in a list to animate
        self.images.append(getImage('sprites/run_1.png'))
        self.images.append(getImage('sprites/run_2.png'))
        self.images.append(getImage('sprites/run_3.png'))
        self.images.append(getImage('sprites/run_2.png'))
        
        self.index = 0 # list index 
        self.image = self.images[self.index] # how we animate 

    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''

        imageTicks = 5 # number of loops each animation frame shows for
        self.index += 1 # +1 to index
        if self.index >= len(self.images)*imageTicks: # why * imageticks?
            self.index = 0
        imageCount = int(self.index/imageTicks)
        self.image = self.images[imageCount]#???

        if self.rect.width < self.image.get_rect().width:# scaling but is it needed?
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

"""
    def find_collisions (self, rect):
        self.collision[0] = rect.collidepoint(self.rect.bottomleft)
        self.collision[1] = rect.collidepoint(self.rect.bottomright)
        self.collision[2] = rect.collidepoint(self.rect.midbottom)

        self.collision[3] = rect.collidepoint(self.rect.topright)
        self.collision[4] = rect.collidepoint(self.rect.midright)
        self.collision[5] = rect.collidepoint(self.rect.bottomright)

    def collision_result(self):
        if self.collision[0] or self.collision[1] or self.collision[2]:
            print("collision with building " + str(building.name))
            robot.rect.y = building.rect.y-robot.rect.height
            Data.T = 0
            Data.Initial_Velocity = 0

        if self.collision[3] or self.collision[4] or self.collision[5]:
            print("GAME OVER")
            screen.fill(WHITE)
            gameover = Text("Game Over. Q to quit R to restart",'freesansbold.ttf',30,400,300,BLACK)
            gameover.Write()
            pygame.display.flip()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_Q :
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_R:
                    frames()
"""           
    # Object creation - put into 1 function??
############################################################

# TODO: make into a function to facilitate restart

background = Background('background.png', [0,0])

for i in range(0,5):
    startX = 0
    if len(Data.Buildings) > 0:
        lastBuilding = Data.Buildings[-1]        
        startX = lastBuilding.rect.x + lastBuilding.rect.width

    building = Building(startX + Random.Gap(), Random.YPos(), Random.Width(),
                        600, BLACK) #creates the Buildings
    building.name = i
    Data.Buildings.append(building)

building_group = pygame.sprite.Group(Data.Buildings)# this makes the building list a group of sprites


robot = Robot(20,100,60,60,BLUE) # make robo
robot_group = pygame.sprite.Group(robot) # make the sprite group for robo

# calculation functions
############################################################

def calcBuildingsPos():
    # move first building to the back if it has gone offscreen
    firstBuilding = Data.Buildings[0]
    if firstBuilding.rect.x < -firstBuilding.rect.width: #??
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

"""
def collisions():
 
    for building in Data.Buildings:
        robot.find_collisions(building.rect)
        robot.collision_result(building.rect)
"""        


def collision():  
    for building in Data.Buildings:

        if robot.rect.colliderect(building.CrashRect()): # wall collison end game       
            print("hits wall game over")
            screen.fill(WHITE)
            gameover = Text("Game Over. Q to quit R to restart",'freesansbold.ttf',30,400,300,BLACK)
            gameover.Write()
            pygame.display.flip()
            global crashed
            crashed = True
            
        elif robot.rect.colliderect(building.rect): # roof collison stand on rect
            print("collision with building " + str(building.name))
            robot.rect.y = building.rect.y-robot.rect.height
            Data.T = 0
            Data.Initial_Velocity = 0
            
        
            

def gapGameOver(): # this works need to tidy up the
            # end game so when you hit the ground will just quit the game 
    for building in Data.Buildings:
        #print("testopen")
        #print(building.rect.y)
        #print(robot.rect.y)
        #print(building.rect.y + building.rect.height)
        #print("testclosed")
        if robot.rect.y >= (building.rect.y + building.rect.height):
            print("fell through gap game over")
            screen.fill(WHITE)
            gameover = Text("Game Over. Q to quit R to restart",'freesansbold.ttf',30,400,300,BLACK)
            gameover.Write()
            pygame.display.flip()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_Q :
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_R:
                frames()
            
           
                    
def frames():

    
    
    Data.Metres += 1#??
    Score = Text(str(Data.Metres) + "m",'freesansbold.ttf',30,750,50,BLACK)  #prints the score on the screen
    Score.Write()

    calcBuildingsPos()

    calcRobotPos()
    
    collision()
    gapGameOver()
    
    
    
# should this be in its own jump function maybe in robot class?
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

        
            
           
                    

            
            
    #startScreen
    frames()
screen.fill(WHITE)
gameover = Text("Game Over. Q to quit R to restart",'freesansbold.ttf',30,400,300,BLACK)
gameover.Write()
pygame.display.flip()
if event.type == pygame.KEYDOWN and event.key == pygame.K_Q :
        pygame.quit()
elif event.type == pygame.KEYDOWN and event.key == pygame.K_R:
        frames()   




# Side wall collision done
# put in images done
# Start screen
# Death screen
# Pause screen
# Restart Function
# 

Blog
