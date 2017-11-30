import pygame
import math

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

crashed = False

RADIUS = 20
XLoc = 30
YLoc = HEIGHT-100

Initial_Velocity = 30
Gravity = -1
Time = 2*(-Initial_Velocity//Gravity)
Y_Change = 0

def SPRITE(XLoc,YLoc):
    pygame.draw.circle(gameDisplay,BLUE,(XLoc, YLoc),RADIUS, 0)
    

#pygame.draw.rect(gameDisplay,WHITE,Rect(0,0,BORDER,HEIGHT))
#pygame.draw.rect(gameDisplay,WHITE,Rect(0,HEIGHT-BORDER,WIDTH,BORDER))


while not crashed:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                
                for T in range(Time):
                    Y_Change = (Initial_Velocity*T) + (Gravity*T*T)
                    if Y_Change > -1:
                        gameDisplay.fill(WHITE)
                        pygame.draw.rect(gameDisplay,BLACK,(0,YLoc+RADIUS,WIDTH,10))
                        SPRITE(XLoc,YLoc-Y_Change)
                        pygame.display.flip()
                        clock.tick(30)
                    else :
                        Y_Change = 0
                    
               
       # if event.type == pygame.KEYUP:
 #           if event.key == pygame.K_UP:
 #               Y_Change = 0
            
                
        print(event)
    gameDisplay.fill(WHITE)
    pygame.draw.rect(gameDisplay,BLACK,(0,YLoc+RADIUS,WIDTH,10))
    SPRITE(XLoc,YLoc-Y_Change)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
quit()
