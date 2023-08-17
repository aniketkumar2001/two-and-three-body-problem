import math
import pygame
from sys import exit
pygame.init()
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((1550, 800))

p1 = pygame.Surface((10, 10), pygame.SRCALPHA)
pygame.draw.circle(p1, (255, 255, 0), (5, 5), 5)

p2 = pygame.Surface((4, 4), pygame.SRCALPHA)
pygame.draw.circle(p2, (255, 255, 255), (2, 2), 2)

p1_y = 400
p2_y = p1_y
frate = 60

#############################################################################
# Parameters

# for 1st object (yellow obj)
vy1 = 0                             # intitial speed in y            
vx1 = 0                             # intitial speed in x 
k1 = 500000                         # k = G*M

# for 2nd object (white obj)    
vy2 = -20                           # intitial speed in y           
vx2 = 0                             # intitial speed in x                  
k2 = 0                              # k = G*M

r = 150                             # initial separation 


###############################################################################
g = lambda k, x, y : -k/((math.sqrt(x*x + y*y))**2)
p1_x = 775-r 
p2_x = 775+r
dt = 1/(frate)
while True :
    SCREEN.fill((0,0,0))            # to refresh the screen, try commenting this line.
    for e in pygame.event.get():
        if (e.type == pygame.QUIT):
            pygame.quit()
            exit()
    SCREEN.blit(p1,(p1_x,p1_y))
    SCREEN.blit(p2,(p2_x,p2_y))
    x2 = p2_x-p1_x
    y2 = p2_y-p1_y
    x1=-x2; y1=-y2
    g2 = g(k1, x2, y2)
    g1 = g(k2, x1, y1) 
    if x2<0:
        g2 = -g2
    if x1<0:
        g1 = -g1
    theta1 = math.atan(y1/x1)
    theta2 = math.atan(y2/x2)
    ax1 = g1*math.cos(theta1)
    ay1 = g1*math.sin(theta1)
    ax2 = g2*math.cos(theta2)
    ay2 = g2*math.sin(theta2)
    vx1 += ax1*dt
    vy1 += ay1*dt
    vx2 += ax2*dt
    vy2 += ay2*dt
    p2_x += vx2*dt
    p2_y += vy2*dt
    p1_x += vx1*dt
    p1_y += vy1*dt
    pygame.display.update()
    clock.tick(frate)