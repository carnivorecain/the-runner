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

# Helper functions
############################################################

class Data():
#all the levers we can tinker with to make the game feel the way we want
    currentScreen = 0 # 0 is Start Screen, 1 is Playing, 2 is Game Over, 3 is Paused (Move paused to StartGame?)
    isGameOver = False

    Buildings = []

    Y_Change = 0
    time = 0
    Jump_Velocity = 25
    
    T = 0
    Metres = 0
    Building_Speed = 600
    Gravity = -75

    MaxBuildingHeightDifference = 150

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
    soundObj = pygame.mixer.Sound(filename)
    soundObj.play()

def playMusic(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
class Random():
    def Height():
        return random.randint(1,6)*50

    def Width():
        return random.randint(8,15)*40

    def Gap():
       return random.randint(10,20)*5

    def YPos():
        return random.randint(20,55)*10

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
        return pygame.Rect(self.rect.x, self.rect.y, 10 ,self.rect.height)
    
    # def ShowCrashRect(self):
    #     pygame.draw.rect(screen,BLACK,self.CrashRect())

class Robot(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.rect = pygame.Rect(x, y, height, width)
        self.color = color
        self.Initial_Velocity = 0.0

        self.images = []
        self.images.append(getImage('run_1.png'))
        self.images.append(getImage('run_2.png'))
        self.images.append(getImage('run_3.png'))
        self.images.append(getImage('run_2.png'))

        self.jumpImages = []
        self.jumpImages.append(getImage('jump_1.png'))
        self.jumpImages.append(getImage('jump_2.png'))
        self.jumpImages.append(getImage('jump_3.png'))
        self.jumpImages.append(getImage('jump_4.png'))
        self.jumpImages.append(getImage('jump_5.png'))
        self.jumpImages.append(getImage('jump_6.png'))
        self.jumpImages.append(getImage('jump_7.png'))
        self.jumpImages.append(getImage('jump_8.png'))
        
        self.index = 0
        self.image = self.images[self.index]

    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''

        imageList = self.images
        if self.Initial_Velocity > 0 :
            imageList = self.jumpImages
            # when you jump, you need to reset the index to 0
        
        imageTicks = 5 # number of loops each animation frame shows for
        self.index += 1
        if self.index >= len(imageList)*imageTicks:
            self.index = 0
        imageCount = int(self.index/imageTicks)
        self.image = imageList[imageCount]

        if self.rect.width < self.image.get_rect().width:
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            
def showGameOver():
    print("GAME OVER")
    Data.currentScreen = 2
    Data.isGameOver = True
                          
# Run loop(s)
############################################################  
# game loop lives in here, along with setup code

def startGame(): #KEEP THIS! makes restart possible

    # calculation functions
    ############################################################

    def calcBuildingsPos(tick):
    #MOVES BUILDING SPRITES BASED ON TIME
        # move first building to the back if it has gone offscreen
        firstBuilding = Data.Buildings[0] # retrieves the first building in a list
        if firstBuilding.rect.x < -firstBuilding.rect.width: #if x position of building is its entire width offscreen...
            firstBuilding.gap = Random.Gap() # ... set a new random gap
            rotate(Data.Buildings)  # moves buildings to the back of the queue

        previousBuilding = Data.Buildings[0] # variable to compare previous building to new one
        for building in Data.Buildings: #loop through all buildings
            # DEBUG CODE: print("building " + str(building.name) + " at " + str(building.rect))
            if building == Data.Buildings[0]: # if building is 1st building...
                building.rect.x -= Data.Building_Speed * tick / 1000.0 # move building based off time
            else:
                building.rect.x = previousBuilding.rect.x + previousBuilding.rect.width + previousBuilding.gap # reposition buildings based off the one before
            previousBuilding = building # set current building to previous building

    def calcRobotPos(tick):
    #MOVES ROBOT SPRITE BASED ON TIME
        Data.T += tick / 1000.0 # converts ticks into seconds
        Data.Y_Change = (robot.Initial_Velocity) + (Data.Gravity*Data.T) # calculates physics
        robot.rect.y -= Data.Y_Change # applies physics
            
    def collision(): # THIS IS NOT GOOD 
        for building in Data.Buildings:
            if robot.rect.colliderect(building.CrashRect()):        
                print("hits wall game over")
                showGameOver()
            
            elif robot.rect.colliderect(building.rect):
                print("collision with building " + str(building.name))
                robot.rect.y = building.rect.y-robot.rect.height
                Data.T = 0
                robot.Initial_Velocity = 0

    def gapGameOver(): # this works need to tidy up the
                # end game so when you hit the ground will just quit the game 
        for building in Data.Buildings:
            if robot.rect.y >= (building.rect.y + building.rect.height):
                print("fell through gap game over")
                showGameOver()

    # Object creation
    ############################################################
    background = Background('background.png', [0,0])

    lastY = 0 #for calculating if building height is too high to jump
    for i in range(0,5):
        startX = 0 #gives a starting X position, to make sure each building is drawn to the right of the previous
        if len(Data.Buildings) > 0: #if a building has been already created
            lastBuilding = Data.Buildings[-1] #get last building we made     
            startX = lastBuilding.rect.x + lastBuilding.rect.width + Random.Gap() #new X position is where last building starts 

        building = Building(startX, Random.YPos(), Random.Width(), 600, BLACK) #creates the Buildings
        #check if building can be jumped to
        if building.rect.y < lastY - Data.MaxBuildingHeightDifference: #if a building that is too tall is going to be generated...
            building.rect.y = lastY - Data.MaxBuildingHeightDifference #... set distance to the maximum we allow
        lastY = building.rect.y #current building is now the previous building
        # building.name = i <-- USED FOR DEBUGGING 
        Data.Buildings.append(building) #adds new building to list of buildings

    building_group = pygame.sprite.Group(Data.Buildings) #creates a group so you can call all the building sprites together

    robot = Robot(20,100,60,60,BLUE) #makes a robot
    robot_group = pygame.sprite.Group(robot) # makes a sprite group for the robot for "draw" calls
    Data.isGameOver = False # exit Boolean for while loop
    
    while not Data.isGameOver:
        print("inside loop") #debugging

        tick = clock.tick(60) # makes motion on screen consistent with time instead of frames
        #collisions() #Are we still using this

        calcBuildingsPos(tick) # calculate positions using tick to account for processing lag

        calcRobotPos(tick) # same as above

        collision()
        #gapGameOver()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if Data.T < 0.0001 and event.type == pygame.KEYDOWN and event.key == pygame.K_UP: #makes the robot jump
                print("jump")
                playSound("Jump.wav")
                robot.Initial_Velocity = Data.Jump_Velocity
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p: #if we need to retreive the robot goes off screen
                print("reset")
                robot.rect = pygame.Rect(20,100,30,30)
                Data.T = 0.0
                robot.Initial_Velocity = 0.0
                 
        screen.fill(BLACK)
        screen.blit(background.image, background.rect)

        robot_group.update()
        robot_group.draw(screen)
        building_group.update()
        building_group.draw(screen)

        Data.Metres += 1 #consider changing to match tick because tick is more regular than FPS
        Score = Text(str(Data.Metres) + "m",'freesansbold.ttf',30,750,50,WHITE)  #prints the score on the screen
        Score.Write()
                
        pygame.display.flip()

    # TODO : make sure buildings and everything resets properly
    building_group.empty()
    robot_group.empty()
    Data.Buildings = []
  

#############################################################################################################
#############################################################################################################
#############################################################################################################
#                                           START HERE                                                      #
#############################################################################################################
#############################################################################################################
#############################################################################################################

playMusic("MortalMachine.ogg")

running = True
flicker = 0.0 #counter that alternates between start screen images

#outer game loop: shows start and game over screens; accepts 'start game' and 'quit' keys
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit() 
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_r) :
            startGame()

    # when you aren't in the game, this display code runs based off the currentScreen variable
    if Data.currentScreen == 0:
         # flicker counts every other second to swap backgrounds, making the 'press space' text flash
        flicker += clock.tick(60)
        backgroundImage = 'start_1.png'
        if flicker > 1000:
            backgroundImage = 'start_2.png'
        if flicker > 2000:
            flicker = 0
        startScreen = Background(backgroundImage, [0,0])
        screen.fill(BLACK)
        screen.blit(startScreen.image, startScreen.rect)
        pygame.display.flip()

    elif Data.currentScreen == 2:
        screen.fill(WHITE)
        gameover = Text("Game Over. Q to quit R to restart",'freesansbold.ttf',30,400,300,BLACK)
        gameover.Write()
        pygame.display.flip()

pygame.quit() #probably unneccesary, as the game will close when it hits the end of file
