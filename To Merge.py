
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



def H_random():
    return random.randint(1,6)*50

def W_random():
    return random.randint(4,7)*100

def G_random():
    return random.randint(50,200)

def Y_random():
    return random.randint(HEIGHT-400,HEIGHT-50)

Metres = 0

class Data():
    def __init__(self):
        pass
    
    Build_A_StartX = 0
    Build_A_Height = 600
    Build_A_StartY = Y_random()
    Build_A_Width = W_random()

    Build_B_StartX = Build_A_StartX + Build_A_Width + G_random()
    Build_B_Height = 600
    Build_B_StartY = Y_random()
    Build_B_Width = W_random()


    Build_C_StartX = Build_B_StartX + Build_B_Width + G_random()
    Build_C_Height = 600
    Build_C_StartY = Y_random()
    Build_C_Width = W_random ()
    Y_Change = 0
    time = 0
    Initial_Velocity = 0
    YLoc = 100 #HEIGHT - Original_Height_A - (RADIUS)
    XLoc = 20
    SWidth = 30
    SHeight = 30
    T = 0
    Metres = 0
    
    Bulding_Speed = 15
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


#randomise the position instead of height H600 W40
def H_random():
    return random.randint(1,6)*50

def W_random():
    return random.randint(4,7)*100

def G_random():
    return random.randint(50,200)

def Y_random():
    return random.randint(HEIGHT-400,HEIGHT-50)


class Sprite():
    def __init__(self, XLoc, YLoc, SWidth, SHeight, color):
        self.XLoc = XLoc
        self.YLoc = YLoc
        self.SWidth = SWidth
        self.SHeight = SHeight
        self.color = color
    
    def Draw(self):
        pygame.draw.rect(gameDisplay,self.color,(self.XLoc,self.YLoc,self.SWidth,self.SHeight))

    def Rect(self):
        return pygame.Rect(self.XLoc,self.YLoc,self.SWidth,self.SHeight)

def frames():
    Data.Metres += 1
    gameDisplay.fill(WHITE)
    Score = Text(str(Data.Metres) + "m",'freesansbold.ttf',30,750,50,BLACK)
    Score.Write()

    Data.Build_A_StartX -= Data.Bulding_Speed
    Data.Build_B_StartX -= Data.Bulding_Speed
    Data.Build_C_StartX -= Data.Bulding_Speed
    
    A = Building(Data.Build_A_StartX, Data.Build_A_StartY, Data.Build_A_Width, Data.Build_A_Height, BLACK)
    B = Building(Data.Build_B_StartX, Data.Build_B_StartY, Data.Build_B_Width, Data.Build_B_Height, GREEN)
    C = Building(Data.Build_C_StartX, Data.Build_C_StartY, Data.Build_C_Width, Data.Build_C_Height, RED)
    
    if Data.Build_A_StartX < -Data.Build_A_Width: 
        Data.Build_A_StartX = Data.Build_C_StartX + Data.Build_C_Width + G_random() #moves rect to the back of the queue
        Data.Build_A_Height = H_random()
        Data.Build_A_StartY = HEIGHT - Data.Build_A_Height
        Data.Build_A_Width = W_random()
        
    if Data.Build_B_StartX < -Data.Build_B_Width:
        Data.Build_B_StartX = Data.Build_A_StartX + Data.Build_A_Width + G_random()
        Data.Build_B_Height = H_random()
        Data.Build_B_StartY = HEIGHT - Data.Build_B_Height
        Data.Build_B_Width = W_random()
        
    if Data.Build_C_StartX < -Data.Build_C_Width:
        Data.Build_C_StartX = Data.Build_B_StartX + Data.Build_B_Width + G_random()
        Data.Build_C_Height = H_random()
        Data.Build_C_StartY = HEIGHT - Data.Build_C_Height
        Data.Build_C_Width = W_random()

    ABR = A.Rect()
    BBR = B.Rect()
    CBR = C.Rect()
    ACR = A.CrashRect()
    BCR = B.CrashRect()
    CCR = C.CrashRect()

    Data.T += 1
    Data.Y_Change = (Data.Initial_Velocity*Data.T) + (Data.Gravity*Data.T*Data.T)
    a = Sprite(Data.XLoc,Data.YLoc-Data.Y_Change,Data.SWidth,Data.SHeight,BLUE)
    SR = a.Rect()          
            
    if SR.colliderect(ABR):
        #print("collision")
        Data.YLoc = Data.Build_A_StartY-Data.SHeight-1
        Data.T = 0
        Data.Initial_Velocity = 0

    elif SR.colliderect(BBR):
        #print("collision")
        Data.YLoc = Data.Build_B_StartY-Data.SHeight-1
        Data.T = 0
        Data.Initial_Velocity = 0

    elif SR.colliderect(CBR):
        #print("collision")
        Data.YLoc = Data.Build_C_StartY-Data.SHeight-1
        Data.T = 0
        Data.Initial_Velocity = 0

    if Data.T==0 and event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                Data.T = 0
                Data.Initial_Velocity = 50
    if event.type == pygame.KEYDOWN and event.key == pygame.K_p: #if we need to retreive the robot goes off screen
                Data.T = 0
                Data.Initial_Velocity = 50
    
    A.Draw()
    B.Draw()
    C.Draw()
    a.Draw()
    A.ShowCrashRect()
    B.ShowCrashRect()
    C.ShowCrashRect()
    #if SR.colliderect(ACR) or SR.colliderect(BCR) or SR.colliderect(CCR) :
 #       p = False
 #       while not p:
 #           YouLose = Text("You Lose",'freesansbold.ttf',70,400,300,BLACK)
 #           YouLose.Write()
 #           pygame.display.flip()
    pygame.display.flip()
    
    
crashed = False

while not crashed:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            crashed = True
    frames()
    
pygame.quit()
quit()
