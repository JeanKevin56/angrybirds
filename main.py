# Example file showing a circle moving on screen
import pygame
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1600, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Le meilleur jeu de tt les temps")
running = True
dragging = False
launching = False
velocity = [0,0]
friction_factor = 2/3
#2/3; 7/12; 3/4; 1/2
dt = 0
king_pig_pos = pygame.Vector2(770, 400)
bird_pos = pygame.Vector2(164, 567)
origin_bird_pos = (164,567)
gravity = 10
#[position debut, poistion fin, materieau]
l_material = [[(700, 675), (700, 400), 2]]
#Materiaux:
#0: Aucun/Detruit
#1: Verre => Se traverse mais ralentis un peu
#2: Bois => Se casse mais fait rebondir
#3: Pierrre => S'abime et fait rebondir
#4: Pierre abimé => Se casse et fait rebondir
color= ["white", "gray", "brown", "red", "orange"]
mouse_B4 = False

king_pig = pygame.image.load("king_pig.png").convert_alpha()
king_pig = pygame.transform.scale_by(king_pig, 0.05)

red = pygame.image.load('red.png').convert_alpha()
red = pygame.transform.scale_by(red, 0.04)

cata = pygame.image.load("catapult.png").convert_alpha()
cata = pygame.transform.scale_by(cata, 0.25)

background_image = pygame.image.load("background.jpg").convert()
background_image = pygame.transform.scale(background_image, (1600, 870))

def clicking():
    return pygame.mouse.get_pressed()[0]

def mouse_event(mouse_B4):
    #________________Check when mouse button is clicked/realeased________________
    if mouse_B4 == False and clicking() == True: 
        return 1
    elif mouse_B4 == True and clicking() == False:
        return -1
    return 0

def scalar(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("2 vec différents lors d'un scalire est impossible")
    summ =0
    for i in range(len(v1)):
        summ+=v1[i]*v2[i]
    return summ
def norm(vector):
    summ = 0
    for val in vector:
        summ +=val*val
    return math.sqrt(summ)

def draw(screen, background_image, red, x_red, y_red, cata, king_pig, x_pig, y_pig):
    screen.blit(background_image, (0, 0))
    screen.blit(red, (bird_pos.x-20,bird_pos.y-20))
    screen.blit(king_pig, (king_pig_pos.x,king_pig_pos.y))
    screen.blit(cata, (150,550))


while running:
    draw(screen, background_image, red, bird_pos.x, bird_pos.y, cata, king_pig, king_pig_pos.x, king_pig_pos.y)
    rect = pygame.Rect(bird_pos.x-20, bird_pos.y-20, 41, 41)

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for material in l_material:
        if material[2]>0:
            pygame.draw.line(screen, color[material[2]], material[0], material[1], 5)
        if rect.clipline(material[0], material[1]):
            if material[2] ==1:
                material[2] = 0
                velocity[0] *= friction_factor
                velocity[1] *= friction_factor
            else:
                vec_line = [material[0][0]-material[1][0], material[0][1]-material[1][1]]
                normal_vec = [vec_line[1], -1*vec_line[0]]
                cos = scalar(velocity, normal_vec)/(norm(normal_vec)*norm(velocity))
                omega = math.acos(cos)
                v =[velocity[0]*math.cos(omega)-velocity[1]*math.sin(omega), velocity[0]*math.sin(omega)+velocity[1]*math.cos(omega)]
                print(velocity[0]*math.cos(omega)-velocity[1]*math.sin(omega), velocity[0]*math.sin(omega)+velocity[1]*math.cos(omega))
                print(velocity, v, omega)
                if material[2] ==2:
                    material[2] = 0
                    velocity[0] = velocity[0]*-1*friction_factor
                    velocity[1] = velocity[1]*-1*friction_factor

    if dragging:
        bird_pos.x = origin_bird_pos[0] + pygame.mouse.get_pos()[0] - origin_coo[0]
        bird_pos.y = origin_bird_pos[1] + pygame.mouse.get_pos()[1] - origin_coo[1]

        pygame.draw.line(screen, "black", (bird_pos.x-15, bird_pos.y+5), (165, 565), 4)
        pygame.draw.line(screen, "black", (bird_pos.x+15, bird_pos.y+15), (190, 565), 4)
        #pygame.draw.line(screen, "black", (bird_pos.x+5, bird_pos.y+5), (bird_pos.x-25, bird_pos.y-5), 3)
    elif launching:
        #On déplace red en fonction de sa vélocité
        bird_pos.x += -10*velocity[0]*dt
        bird_pos.y += -10*velocity[1]*dt
        pygame.draw.line(screen, "black", (0, 690), (1600, 690), 5)
        #On applique la gravité à sa vélocité sur l'axe des y (Haut/Bas)

        if bird_pos.y >=670:
            velocity[1] *= -1*friction_factor
            velocity[0] *= friction_factor
            while bird_pos.y >=670:
                bird_pos.y-=0.1
        else:
            velocity[1] += -10*dt*gravity
        if bird_pos.x >=1580 or bird_pos.x <=0:
            velocity[0] *= -1*friction_factor
            while bird_pos.x >=1580:
                bird_pos.x-=0.1
            while bird_pos.x <=0:
                bird_pos.x+=0.1
        if abs(velocity[0]) <0.01:
            velocity[0] = 0
    event = mouse_event(mouse_B4)
    if event == 1:
        if abs(pygame.mouse.get_pos()[0]-bird_pos.x) < 30 and abs(pygame.mouse.get_pos()[1]-bird_pos.y) < 30:
            dragging = True
            origin_coo = pygame.mouse.get_pos()
    elif event == -1:
        if dragging:
            dragging = False
            launching = True
            velocity = [(pygame.mouse.get_pos()[0]-origin_coo[0]), (pygame.mouse.get_pos()[1]-origin_coo[1])]

    mouse_B4 = clicking()
    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    
    clock.tick(60)
pygame.quit()