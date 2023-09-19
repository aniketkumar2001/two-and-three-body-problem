import pygame
from sys import exit
pygame.init()
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((1550, 800))
p1 = pygame.Surface((2,2))
p1.fill((255,0,0))
p2 = pygame.Surface((2,2))
p2.fill((0,255,0))
p3 = pygame.Surface((2,2))
p3.fill((0,0,255))
frate = 60

# gravity
g_x = lambda k, x, y : (k*x)/((x*x + y*y)**(3/2))
g_y = lambda k, x, y : (k*y)/((x*x + y*y)**(3/2))



# updating
def getAccelerationOf(x2,y2,x1,y1,x3,y3,k1,k3):
    #### effect on 2 due to 1 ###########
    x21 = x1-x2        
    y21 = y1-y2
    
    #### effect on 2 due to 3 ############
    x23 = x3-x2        
    y23 = y3-y2

    ax2 = g_x(k1,x21,y21)+g_x(k3,x23,y23)
    ay2 = g_y(k1,x21,y21)+g_y(k3,x23,y23)

    return [ax2,ay2]


p1_x = 601.794919 ; p1_y = 400

p2_x = 948.205081 ; p2_y = 400

p3_x = 775 ; p3_y = 400


vy1 = 10                      # intitial speed in y
vx1 = 10                             # intitial speed in x
vy2 = -10                     # intitial speed in y
vx2 = -10.1                              # intitial speed in x
vx3 = 30
vy3 = 30
k1 = 150000
k2 = 150000                         # 1000000
k3 = 1000



dt = 1/(frate)                        # the real time is equal to (the time taken in simulation/n); where n = frate*n,
while True :
    #SCREEN.fill((0,0,0))             # to refresh the screen
    for e in pygame.event.get():
        if (e.type == pygame.QUIT):
            pygame.quit()
            exit()
    SCREEN.blit(p1,(p1_x,p1_y))
    SCREEN.blit(p2,(p2_x,p2_y))
    SCREEN.blit(p3,(p3_x,p3_y))
    
    a1 = getAccelerationOf(p1_x,p1_y,p2_x,p2_y,p3_x,p3_y,k2,k3)
    vx1 += a1[0]*dt
    vy1 += a1[1]*dt
    p1_x += vx1*dt
    p1_y += vy1*dt

    a2 = getAccelerationOf(p2_x,p2_y,p1_x,p1_y,p3_x,p3_y,k1,k3)
    vx2 += a2[0]*dt
    vy2 += a2[1]*dt
    p2_x += vx2*dt
    p2_y += vy2*dt

    a3 = getAccelerationOf(p3_x,p3_y,p1_x,p1_y,p2_x,p2_y,k1,k2)
    vx3 += a3[0]*dt
    vy3 += a3[1]*dt
    p3_x += vx3*dt
    p3_y += vy3*dt
    
    pygame.display.update()
    clock.tick(frate)