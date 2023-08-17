import numpy as np
import pygame
from sys import exit
pygame.init()
clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((1550, 800))          
f_rate = 60

p1 = pygame.Surface((10, 10), pygame.SRCALPHA)
pygame.draw.circle(p1, (255, 255, 0), (5, 5), 5)

p2 = pygame.Surface((4, 4), pygame.SRCALPHA)
pygame.draw.circle(p2, (255, 255, 255), (2, 2), 2)

dt = 1/(f_rate)


#############################################################################
# Parameters

# for 1st object (yellow obj)
vy1 = 0.0                             # intitial speed in y            
vx1 = 0.0                             # intitial speed in x 
k1 = 500000                         # k = G*M

# for 2nd object (white obj)    
vy2 = -20.0                           # intitial speed in y           
vx2 = 0.0                             # intitial speed in x                  
k2 = 0                              # k = G*M

r = 300.0                             # initial separation 

###############################################################################


obj0=[]
obj0.append([np.array([750.0,400.0]),np.array([vx1,vy1])])                # object 1
obj0.append([np.array([750.0+r,400.0]),np.array([vx2,vy2])])             # object 2
k = np.array([k1,k2])                                                  # GM [obj1,obj2]


def addG(obj,i):
    j=0
    while j<2:
        if j==i:
            j+=1
            continue
        
        s=obj0[j][0]-obj[0]
        sMod=np.linalg.norm(s)
        acc=(k[j]*s)/(sMod**3)

        obj[1]+=[acc[0]*dt,acc[1]*dt]
        obj[0]+=obj[1]*dt

        j+=1

    return obj   


while True :
    for e in pygame.event.get():
        if (e.type == pygame.QUIT):
            pygame.quit()
            exit()

    SCREEN.fill((0,0,0))                    # to refresh the screen, try commenting this line.
    SCREEN.blit(p1,obj0[0][0]) 
    SCREEN.blit(p2,obj0[1][0]) 
    
    i=0
    while i<2: 
        obj0[i] = addG(obj0[i],i)
        i+=1

    pygame.display.update()
    clock.tick(f_rate)
