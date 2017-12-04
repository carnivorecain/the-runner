
import pygame
import math
import random
import sys
from pygame.locals import *


pygame.init()
pygame.font.init

WIDTH = 800
HEIGHT = 600

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('THAT WHICH RUNS DOES NOT FALL')

clock = pygame.time.Clock()
tick = clock.tick(60)


class Random():
    def Height():
        return random.randint(1,6)*50

    def Width():
        return random.randint(4,7)*100

    def Gap():
       return random.randint(50,200)

    def YPos():
        return random.randint(200,550)

class Data():
    def __init__(self):
        pass
    
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
    Building_Speed = 15
    Gravity = -2



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
        gameDisplay.blit(TextSurf,TextRect)
        #pygame.display.flip()




class Building():
    def __init__(self,BuildX,BuildY,BuildW,BuildH,color):
        self.BuildX = BuildX
        self.BuildY = BuildY
        self.BuildW = BuildW
        self.BuildH = BuildH
        self.color = color
    
    def Draw(self):
        pygame.draw.rect(gameDisplay,self.color,(self.BuildX, self.BuildY, self.BuildW, self.BuildH))
    
    def Rect(self):
        return pygame.Rect(self.BuildX, self.BuildY,self.BuildW,self.BuildH)

    def CrashRect(self):
        return pygame.Rect(self.BuildX, self.BuildY,5,self.BuildH)
    
    def ShowCrashRect(self):
        pygame.draw.rect(gameDisplay,BLUE,(self.BuildX, self.BuildY,5,self.BuildH))


class Robot():
    def __init__(self, Robot_XPos, Robot_YPos, Robot_Width, Robot_Height, color):
        self.Robot_XPos = Robot_XPos
        self.Robot_YPos = Robot_YPos
        self.Robot_Width = Robot_Width
        self.Robot_Height = Robot_Height
        self.color = color
        
    def Draw(self):
        pygame.draw.rect(gameDisplay,self.color,(self.Robot_XPos,self.Robot_YPos,self.Robot_Width,self.Robot_Height))

    def Rect(self):
        return pygame.Rect(self.Robot_XPos,self.Robot_YPos,self.Robot_Width,self.Robot_Height)

def frames():
    Data.Metres += 1
    gameDisplay.fill(WHITE)
    Score = Text(str(Data.Metres) + "m",'freesansbold.ttf',30,750,50,BLACK)  #prints the score on the screen
    Score.Write()

    Data.Build_A_XPos -= Data.Building_Speed  #Moves the Buildings one to the left
    Data.Build_B_XPos -= Data.Building_Speed
    Data.Build_C_XPos -= Data.Building_Speed
    
    A = Building(Data.Build_A_XPos, Data.Build_A_YPos, Data.Build_A_Width, Data.Build_A_Height, BLACK) #creates the Buildings
    B = Building(Data.Build_B_XPos, Data.Build_B_YPos, Data.Build_B_Width, Data.Build_B_Height, GREEN)
    C = Building(Data.Build_C_XPos, Data.Build_C_YPos, Data.Build_C_Width, Data.Build_C_Height, RED)
    
    if Data.Build_A_XPos < -Data.Build_A_Width: 
        Data.Build_A_XPos = Data.Build_C_XPos + Data.Build_C_Width + Random.Gap() #moves rects to the back of the queue
        Data.Build_A_YPos = Random.YPos()
        Data.Build_A_Width = Random.Width()
        
    if Data.Build_B_XPos < -Data.Build_B_Width:
        Data.Build_B_XPos = Data.Build_A_XPos + Data.Build_A_Width + Random.Gap()
        Data.Build_B_YPos = Random.YPos()
        Data.Build_B_Width = Random.Width()
        
    if Data.Build_C_XPos< -Data.Build_C_Width:
        Data.Build_C_XPos = Data.Build_B_XPos + Data.Build_B_Width + Random.Gap()
        Data.Build_C_YPos = Random.YPos()
        Data.Build_C_Width = Random.Width()

    ABR = A.Rect() #collision boxes for buldings - stands for ABuildingRect
    BBR = B.Rect()
    CBR = C.Rect()
    
    ACR = A.CrashRect() #collision boxes for the side of the buildings for side of bulding crashes - stands for ACrashRect
    BCR = B.CrashRect()
    CCR = C.CrashRect()

    Data.T += 1
    Data.Y_Change = (Data.Initial_Velocity*Data.T) + (Data.Gravity*Data.T*Data.T)
    a = Robot(Data.Robot_XPos,Data.Robot_YPos-Data.Y_Change,Data.Robot_Width,Data.Robot_Height,BLUE)
    RR = a.Rect()          # robot's collision box - stands for RobotRect
    
    if RR.colliderect(ABR):
        #print("collision")
        Data.Robot_YPos = Data.Build_A_YPos-Data.Robot_Height-1
        Data.T = 0
        Data.Initial_Velocity = 0

    elif RR.colliderect(BBR):
        #print("collision")
        Data.Robot_YPos = Data.Build_B_YPos-Data.Robot_Height-1
        Data.T = 0
        Data.Initial_Velocity = 0

    elif RR.colliderect(CBR):
        #print("collision")
        Data.Robot_YPos = Data.Build_C_YPos-Data.Robot_Height-1
        Data.T = 0
        Data.Initial_Velocity = 0

    if Data.T==0 and event.type == pygame.KEYDOWN and event.key == pygame.K_UP: #makes the robot jump
                Data.T = 0
                Data.Initial_Velocity = 50
    if event.type == pygame.KEYDOWN and event.key == pygame.K_p: #if we need to retreive the robot goes off screen
                Data.T = 0
                Data.Initial_Velocity = 50

 #   if RR.colliderect(ACR) or RR.colliderect(BCR) or RR.colliderect(CCR) : #my attempt at side wall collision but it causes the program to freeze
        
 #       gameDisplay.fill(WHITE)
 #       YouLose = Text("You Lose, Press R to retry",'freesansbold.ttf',30,400,300,BLACK)
 #       YouLose.Write()
 #      pygame.display.flip()
 #       p = False
 #       while not p:
 #           if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
 #               Data.Robot_YPos = 100
 #               Data.T = 0
 #               Data.Metres = 0
 #               p = True
                
    A.Draw() #draws the Robot and Buildings
    B.Draw()
    C.Draw()
    a.Draw()
    A.ShowCrashRect()
    B.ShowCrashRect()
    C.ShowCrashRect()
    
    
            
    pygame.display.flip()
    
    
crashed = False

while not crashed:
    for event in pygame.event.get() :
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
