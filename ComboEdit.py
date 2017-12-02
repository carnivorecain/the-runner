
import pygame
import math
import random
import sys
from pygame.locals import *


pygame.init()

WIDTH = 800
HEIGHT = 600

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('Runningting')

clock = pygame.time.Clock()




    
##def BUILDING(XBuild,YBuild):
##    XBuild = WIDTH
##    HBuild = 30
##    YBuild = HEIGHT - HBuild
##
##    pygame.draw.rect(gameDisplay,BLACK,(XBuild,YBuild,WIDTH/2,HBuild))
##    rect.move(-1, 0)
##
##def MOVEBUILDING(x,y):
##    pass



crashed = False
def BUILDING(BuildX,BuildY,BuildW,BuildH,color):
    #XBuild = WIDTH
    #HBuild = 30
    #YBuild = HEIGHT - HBuild
    pygame.draw.rect(gameDisplay,color,(BuildX, BuildY,BuildW,BuildH))
    BuildingRect = pygame.Rect(BuildX, BuildY,BuildW,BuildH)
Original_Height_A = random.randint(50,200)
Original_Height_B = random.randint(50,200) 
Original_Height_C = random.randint(50,200) 

Build_A_StartX = 0
Build_A_StartY = HEIGHT-Original_Height_A
Build_A_Width = random.randint(400,700) 
Build_A_Height = Original_Height_A

Build_B_StartX = Build_A_StartX + Build_A_Width + random.randint(50,200)
Build_B_StartY = HEIGHT-Original_Height_B
Build_B_Width = random.randint(400,700) 
Build_B_Height = Original_Height_B

Build_C_StartX = Build_B_StartX + Build_B_Width + random.randint(50,200)
Build_C_StartY = HEIGHT-Original_Height_C
Build_C_Width = random.randint(400,700) 
Build_C_Height = Original_Height_C

Bulding_Speed = 10

####### Sprite Stuffs:
RADIUS = 20
Y_Change = 0
XLoc = 20
YLoc = 100 #HEIGHT - Original_Height_A - (RADIUS)
SWidth = 30
SHeight = 30
def SPRITE(XLoc,YLoc,SWidth,SHeight,color):
    pygame.draw.rect(gameDisplay,color,(XLoc,YLoc,SWidth,SHeight))
    SpriteRect = pygame.Rect(XLoc,YLoc,SWidth,SHeight)
    

Initial_Velocity = 0 
Gravity = -1
Time = 2*(-Initial_Velocity//Gravity)
time = 0
T = 0


#def SPRITE(XLoc,YLoc):
    #pygame.draw.circle(gameDisplay,BLUE,(XLoc, YLoc),RADIUS, 0)

#BUILDING(Build_StartX, Build_StartY, Build_Width, Build_Height, BLACK)
a = Build_A_StartY
b = Build_B_StartY
c = Build_C_StartY
d = a
def frames():
    global Build_A_StartX
    global Build_B_StartX
    global Build_C_StartX
    global Build_A_Height
    global Build_B_Height
    global Build_C_Height
    global Build_A_StartY
    global Build_B_StartY
    global Build_C_StartY
    global Build_A_Width
    global Build_B_Width
    global Build_C_Width
    global Y_Change
    global time
    global Initial_Velocity
    global T
    global d
    
    gameDisplay.fill(WHITE)
    #pygame.draw.rect(gameDisplay,BLACK,(0,YLoc+RADIUS,WIDTH,10))
    #x = pygame.draw.rect(gameDisplay,BLACK,(WIDTH/2,HEIGHT-30,WIDTH/2,30))
    #SPRITE(XLoc,YLoc-Y_Change)
    #BUILDING(WIDTH/2,HEIGHT-30,30)
    #MOVEBUILDING(-100,0)
    #x.move_ip(-100,0)
    BuildingA = BUILDING(Build_A_StartX, Build_A_StartY, Build_A_Width, Build_A_Height, BLACK)
    BuildingB = BUILDING(Build_B_StartX, Build_B_StartY, Build_B_Width, Build_B_Height, GREEN)
    BuildingC = BUILDING(Build_C_StartX, Build_C_StartY, Build_C_Width, Build_C_Height, BLUE)
    Build_A_StartX -= Bulding_Speed
    Build_B_StartX -= Bulding_Speed
    Build_C_StartX -= Bulding_Speed
    if Build_A_StartX < -Build_A_Width:
        Build_A_StartX = Build_C_StartX + Build_C_Width + random.randint(50,200)
        Build_A_Height = random.randint(50,200)
        Build_A_StartY = HEIGHT - Build_A_Height
        Build_A_Width = random.randint(400,700)
        
    if Build_B_StartX < -Build_B_Width:
        Build_B_StartX = Build_A_StartX + Build_A_Width + random.randint(50,200)
        Build_B_Height = random.randint(50,200)
        Build_B_StartY = HEIGHT - Build_B_Height
        Build_B_Width = random.randint(400,700)
        
    if Build_C_StartX < -Build_C_Width:
        Build_C_StartX = Build_B_StartX + Build_B_Width + random.randint(50,200)
        Build_C_Height = random.randint(50,200)
        Build_C_StartY = HEIGHT - Build_C_Height
        Build_C_Width = random.randint(400,700)
        
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                T = 0
                Initial_Velocity = 40
    T += 1
    Y_Change = (Initial_Velocity*T) + (Gravity*T*T)
    Robot = SPRITE(XLoc,YLoc-Y_Change,SWidth,SHeight,BLUE)
    if Robot.SpriteRect.colliderect(BuildingA.BuildingRect):
        print("collision")
    
    #SPRITE(XLoc,YLoc-Y_Change)
    pygame.display.flip()
    clock.tick(30)
    

while not crashed:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                for T in range(Time):
                    Y_Change = (Initial_Velocity*T) + (Gravity*T*T)
                    frames()
                    #if (YLoc + RADIUS) > d :
                        #Y_Change = YLoc - d
                        #break
                    
                    
        print(event)
    frames()
    
pygame.quit()
quit()
