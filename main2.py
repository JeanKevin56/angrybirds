# Example file showing a circle moving on screen
import pygame
import math
import pymunk
import pymunk.pygame_util
import random

# _____pygame setup_____
pygame.init()
screen = pygame.display.set_mode((1600, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Les oiseaux pas très content")

#_____ Variable initialisation_____
running = True

birds_status = 1
#1 : red
#2 : chuck
#3 : bomb
#4 : terence
#5 : the blues
#6 : matilda

explosion_center = (0,0)
explosion_timer =0
dragging = False
launching = False
velocity = [0,0]
friction_factor = 2/3
#2/3; 7/12; 3/4; 1/2
dt = 0
bird_pos = pygame.Vector2(144, 547)
origin_bird_pos = (144,547)
radius = 10
ball = None
ball2, ball3 = None, None
egg = None
capacity = False
mouse_B4 = False
weight = 10
d_prop_info = {
    "shape": [],
    "last_vel": [],
    "hp": [],
    "material": []
}

d_pig = {
    "shape": [],
    "last_vel": []

}

#d_prop_info["shape"] = prop shape (pymunk stuff)
#d_prop_info["last_vel"] = velocity of last frame (used to calculate the difference in velocity to calculate if a structures breaks or not)
#d_prop_info["hp"] = health of a prop
d_prop_info["last_vel"] = []

#________ Charge les images pour le jeu ________
red = pygame.image.load('red.png').convert_alpha()
red = pygame.transform.scale_by(red, 0.04)

chuck = pygame.image.load('chuck.png').convert_alpha()
chuck = pygame.transform.scale_by(chuck, 0.04)

bomb = pygame.image.load('bomb.png').convert_alpha()
bomb = pygame.transform.scale_by(bomb, 0.06)

terence = pygame.image.load('terence.png').convert_alpha()
terence = pygame.transform.scale_by(terence, 0.1)

blues = pygame.image.load('blues.png').convert_alpha()
blues = pygame.transform.scale_by(blues, 0.05)

matilda = pygame.image.load('matilda.png').convert_alpha()
matilda = pygame.transform.scale_by(matilda, 0.1)

king_pig = pygame.image.load('king_pig.png').convert_alpha()
king_pig = pygame.transform.scale_by(king_pig, 0.04)

pig = pygame.image.load('pig.png').convert_alpha()
pig = pygame.transform.scale_by(pig, 0.04)

bird = red
bird_original = bird

w, h = bird.get_size()

cata = pygame.image.load("catapult.png").convert_alpha()
cata = pygame.transform.scale_by(cata, 0.25)

explosion_image = terence

background_image = pygame.image.load("background.jpg").convert()
background_image = pygame.transform.scale(background_image, (1600, 870))
#________________________________________________________________________


space = pymunk.Space()
space.gravity = (0, 0)
draw_options = pymunk.pygame_util.DrawOptions(screen)
#handler = space.add_collision_handler()
def clicking():#Send True if the mouse is pressed
    return pygame.mouse.get_pressed()[0]

def mouse_event(mouse_B4): 
    """
    Return 1 at THE exact frame the mouse button is pressed
    Return -1 at THE exact frame the mouse button is unpressed
    Return 0 otherwise
    """
    #________________Check when mouse button is clicked/realeased________________
    if mouse_B4 == False and clicking() == True: 
        return 1
    elif mouse_B4 == True and clicking() == False:
        return -1
    return 0

def scalar(v1, v2):
    """
    Return the scalar of 2 vector
    """
    if len(v1) != len(v2):
        raise ValueError("2 vec différents lors d'un scalire est impossible")
    summ =0
    for i in range(len(v1)):
        summ+=v1[i]*v2[i]
    return summ
def norm(vector):
    #Return the norm of a vector
    summ = 0
    for val in vector:
        summ +=val*val
    return math.sqrt(summ)

def draw(screen, space, draw_options, bird, bird_pos, w,h, ball, ball2 = None, ball3 = None):
    """
    This function draw everything needed for the game
    """
    screen.blit(background_image, (0, 0)) #Place the background image
    space.debug_draw(draw_options)        #Debug options to allow pymunk to show 
    screen.blit(cata, (150,550))          #Spawn the catapulte 
    if ball:#If there is already a ball on screen (a rigid body so the bird azs been launched)
            #We reotate the bird acording to the body rotation,       convert radian in degre \/
        blitRotate(screen, bird, (bird_pos.x, bird_pos.y), (w/2, h/2), -1*ball.body.angle*180/math.pi)
    else:
        #Is there is no ball we show the bird without azny roation
        blitRotate(screen, bird, (bird_pos.x, bird_pos.y), (w/2, h/2), 0)
    if ball2 and ball3:
        blitRotate(screen, bird, (ball2.body.position[0], ball2.body.position[1]), (w/2, h/2), -1*ball2.body.angle*180/math.pi)
        blitRotate(screen, bird, (ball3.body.position[0], ball3.body.position[1]), (w/2, h/2), -1*ball3.body.angle*180/math.pi)
    pygame.draw.line(screen, "black", (0,0), (50, 50), 4)#Draw a line 
    pygame.draw.line(screen, "red", (50,0), (100, 50), 4)#Draw a line
    #Command use: pygame.draw.line(screen, "color", (x1,y1), (x2, y2), size)
    
    for oink in d_pig["shape"]:
        blitRotate(screen, pig, (oink.body.position[0], oink.body.position[1]), (pig.get_size()[0]/2, pig.get_size()[1]/2), -1*oink.body.angle*180/math.pi)
    #Show the diffenrent bird on top for the user to choose from
    screen.blit(red, (150,0))
    screen.blit(chuck, (200,0))
    screen.blit(bomb, (300,-10))
    screen.blit(terence, (400,0))
    screen.blit(blues, (500,0))
    screen.blit(matilda, (600,0))
    #Command use: screen.blit(image, (x,y)) the x and y of the image needs to be it's top left corner's coordinates
    
    #Draw lines to show the separation between the birds 
    pygame.draw.line(screen, "black", (50,0), (50, 50), 4)
    for i in range(1, 8):
        pygame.draw.line(screen, "black", (100*i,0), (100*i, 50), 4)
    
def create_structure(space, width, height):
    """
    Create all the diffenrents structure of the game
    """
    l_prop = []
    #________Color setup________
    brown = (139, 69, 19, 100)
    gray = (128,128,128,100)

    #List of all props of the game
    #use: [(x, y), (width, height), color, mass]
    #The x and y are the center's coordinates
    rects = [
    [(900, height - 150), (40, 200), gray, 300],
    [(1200, height - 150), (40, 200), gray, 300],
    [(1050, height - 270), (340, 40), gray, 400],

    [(900, height - 410), (40, 200), brown, 150],
    [(1200, height - 410), (40, 200), brown, 150],
    [(1050, height - 540), (340, 40), brown, 220],


    [(500, height - 120), (40, 130), gray, 30],
    [(800, height - 120), (40, 130), gray, 30],
    [(650, height - 200), (340, 40), gray, 50],

    [(500, height - 270), (40, 70), brown, 5],
    [(800, height - 270), (40, 70), brown, 5],
    [(650, height - 330), (340, 40), brown, 10]
    ]
    # For each props, gets it position, size, color and mass
    for pos, size, color, mass in rects:
        body = pymunk.Body() #Create a new body (by default is a dynamic body)
        body.position = pos  #Sets the position of the body to it's assigned position
        shape = pymunk.Poly.create_box(body, size, radius=5)    #Create a rectangle shape with the previoulsy created body
                                                                #the size given and a radius to round up the edges
        shape.color = color #Set up it's color
        shape.mass = mass   #Set up it's mass
        shape.elasticity = 0.4  #Give it an arbitrary elasticity
        shape.friction = 0.3    #Give it an arbitrary frition
        l_prop.append(shape) #Add the shape to a list of all props
        space.add(body, shape)  #Add the newly created props to the game
    return l_prop
def map_limit(space, w=1600, h=720):
    #A list of rectangle that will be used to act as map limit
    rec=[
        [(w/2, h-20), (w, 40)],
        [(w/2, 25), (w, 50)],
        [(10, h/2), (20, h)],
        [(w-10, h/2), (20, h)]
    ]
    #Similar to the previous function "create_structure", refer to it if you have question about this code
    for r in rec:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = r[0]
        shape = pymunk.Poly.create_box(body, r[1])
        shape.elasticity = 0.4
        shape.friction = 0.3
        space.add(body, shape)
def add_object(space, x, y,radius, mass):
    """
    Adds an ball to the space with:
        Some coordinates
        A radius
        A mass
    """
    body = pymunk.Body(1,1) #Create the body
    body.position = (x, y) #Setup it's position according to given coordinates
    shape = pymunk.Circle(body, radius) #Creating a circle shape with the body and radius
    shape.mass = mass #We give it the given mass
    shape.color = (0,0,0,100)
    shape.elasticity = 2/3
    shape.friction = 3/4
    space.add(body, shape)
    return shape


def blitRotate(screen, bird, pos, originPos, angle):

    # offset from pivot to center
    bird_rect = bird.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))#Create a rectangle
    offset_center_to_pivot = pygame.math.Vector2(pos) - bird_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd bird center
    rotated_bird_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated bird
    rotated_bird = pygame.transform.rotate(bird, angle)
    rotated_bird_rect = rotated_bird.get_rect(center = rotated_bird_center)

    screen.blit(rotated_bird, rotated_bird_rect) #Show the rotated bird to the screen
 

def launch(v, weight, radius):
    ball = add_object(space, bird_pos.x, bird_pos.y, radius, weight) #Add the ball to the screen
    ball.body.apply_impulse_at_local_point((-10*v[0]*weight,-10*v[1]*weight),(0,0)) #Add an impulse relative 
                                                                                    #to how far the bird was dragged
    return ball

def rectRect(r1x, r1y, r1w, r1h, r2x, r2y, r2w, r2h):
    return r1x + r1w >= r2x and r1x <= r2x + r2w and r1y + r1h >= r2y and r1y <= r2y + r2h

def gravity_formula(shape, dt, small_g=9.81, aditionnal_multiplier=100):
    return [aditionnal_multiplier*dt*small_g*shape.body.mass*math.sin(shape.body.angle) , aditionnal_multiplier*dt*small_g*shape.body.mass*math.sin(shape.body.angle+math.pi/2)]

def apply_gravity(d_prop_info, ball, ball2, ball3, egg ,dt):
    for prop in d_prop_info["shape"]:
        g = gravity_formula(prop, dt)
        #print(g, prop.body.angle)
        prop.body.apply_impulse_at_local_point((g[0],g[1]),(0,0))
    for shape in [ball, ball2, ball3, egg]:
        if shape:
            g = gravity_formula(shape, dt)
            shape.body.apply_impulse_at_local_point((g[0],g[1]),(0,0))
    for guy in d_pig["shape"]:
        g = gravity_formula(guy, dt)
        guy.body.apply_impulse_at_local_point((g[0],g[1]),(0,0))
def remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching):
    if ball:
        space.remove(ball, ball.body)
        ball = None
        bird_pos.x = origin_bird_pos[0]
        bird_pos.y = origin_bird_pos[1]
        launching = False
        if ball2 and ball3:
            space.remove(ball2, ball2.body)
            space.remove(ball3, ball3.body)
            ball2, ball3 = None, None
        elif egg:
            space.remove(egg, egg.body)
            egg = None
    return (ball, bird_pos, launching, ball2, ball3, egg)
#Place the props
d_prop_info["shape"] = create_structure(space, 1600, 720)
for prop in d_prop_info["shape"]:
    d_prop_info["last_vel"].append(prop.body.kinetic_energy)
#Create the limit of the map
map_limit(space)
d_pig["shape"].append(add_object(space, 1050, 100, 30, 10))

while running:

    keys = pygame.key.get_pressed()
    # pygame.QUIT event means the user clicked X to bod.close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    apply_gravity(d_prop_info, ball, ball2, ball3, egg ,dt)
    for guy, last_vel in zip(d_pig["shape"], d_pig["last_vel"]):
        if abs(guy.body.kinetic_energy-last_vel) > 100000*guy.body.mass:
            print("________________DEAD_PIG________________") 

    #Affiche 
    draw(screen, space, draw_options, bird, bird_pos, w,h, ball, ball2, ball3)
    l_to_remove = []
    for prop, last_vel in zip(d_prop_info["shape"], d_prop_info["last_vel"]):
        #print(prop.body.velocity, end=" - ")
        if abs(prop.body.kinetic_energy-last_vel) < 10*prop.body.mass:
            pygame.draw.rect(screen, "black", pygame.Rect(prop.body.position[0], prop.body.position[1], 10, 10))
        elif abs(prop.body.kinetic_energy-last_vel) < 1000*prop.body.mass:
            pygame.draw.rect(screen, "yellow", pygame.Rect(prop.body.position[0], prop.body.position[1], 10, 10))
        elif abs(prop.body.kinetic_energy-last_vel) < 10000*prop.body.mass:
            pygame.draw.rect(screen, "orange", pygame.Rect(prop.body.position[0], prop.body.position[1], 10, 10))
        elif abs(prop.body.kinetic_energy-last_vel) < 20000*prop.body.mass:
            pygame.draw.rect(screen, "red", pygame.Rect(prop.body.position[0], prop.body.position[1], 10, 10))
        else:
            pygame.draw.rect(screen, "purple", pygame.Rect(prop.body.position[0], prop.body.position[1], 10, 10))
            if (prop.body.kinetic_energy)> 50000*prop.body.mass:
                pygame.draw.rect(screen, "white", pygame.Rect(prop.body.position[0], prop.body.position[1], 10, 10))
            if abs(prop.body.kinetic_energy-last_vel) > 50000*prop.body.mass:
                space.remove(prop, prop.body)
                l_to_remove.append(prop)
            l_prop_memo = d_prop_info["shape"]
            d_prop_info["shape"] = []
            for prop in l_prop_memo:
                if prop not in l_to_remove:
                    d_prop_info["shape"].append(prop)
    event = mouse_event(mouse_B4) #get mouse event (check if mouse just got pressed/unpressed)
    #pygame.draw.rect(screen, "black", pygame.Rect(bird_pos.x-60, bird_pos.y-60, 120, 120))
    if event == 1: #If mouse just got pressed
        if abs(pygame.mouse.get_pos()[0]-bird_pos.x) < 30 and abs(pygame.mouse.get_pos()[1]-bird_pos.y) < 30 and not launching:
            dragging = True
            origin_coo = pygame.mouse.get_pos()
        if pygame.mouse.get_pos()[1] < 50:
            if pygame.mouse.get_pos()[0] < 50:
                ball, bird_pos, launching, ball2, ball3, egg = remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching)
            elif 50<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 100:
                for props in d_prop_info["shape"]:
                    space.remove(props, props.body)
                d_prop_info["shape"] = create_structure(space, 1600, 720)
            elif 100<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 200 and not launching:
                bird = red
                birds_status = 1
                weight = 10
                radius = 20
                w, h = bird.get_size()
            elif 200<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 300 and not launching:
                bird = chuck
                birds_status = 2
                weight = 17
                radius = 20
                w, h = bird.get_size()
            elif 300<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 400 and not launching:
                bird = bomb
                birds_status = 3
                weight = 25
                radius = 25
                w, h = bird.get_size()
            elif 400<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 500 and not launching:
                bird = terence
                birds_status = 4
                weight = 100
                radius = 35
                w, h = bird.get_size()
            elif 500<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 600 and not launching:
                bird = blues
                birds_status = 5
                weight = 6
                radius = 13
                w, h = bird.get_size()
            elif 600<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 700 and not launching:
                bird = matilda
                birds_status = 6
                weight = 20
                radius = 25
                w, h = bird.get_size()
        elif launching:
            if birds_status == 2:
                ball.body.apply_impulse_at_local_point((25000,0),(0,0))
            elif birds_status == 3:
                #pygame.draw.line(screen, "black", (0,0), (50, 50), 4)
                l_to_remove = []
                for i, prop in enumerate(d_prop_info["shape"]):
                    sommets_du_polygone = prop.get_vertices()
                    position = prop.body.position
                    lenght = max(sommets_du_polygone, key=lambda x: x[1])[1] - min(sommets_du_polygone, key=lambda x: x[1])[1]
                    width = max(sommets_du_polygone, key=lambda x: x[0])[0] - min(sommets_du_polygone, key=lambda x: x[0])[0]
                    explosion_image = pygame.Surface((width, lenght))
                    image = explosion_image.copy()
                    rec = image.get_rect()
                    rec.center = position
                    old_center = rec.center
                    new_image = pygame.transform.rotate(explosion_image, prop.body.angle*-180/math.pi)
                    rec = new_image.get_rect()
                    rec.center = old_center
                    pygame.draw.rect(screen, "brown", pygame.Rect(rec[0], rec[1], rec[2], rec[3]))
                    pygame.draw.rect(screen, "black", pygame.Rect(bird_pos.x-160, bird_pos.y-160,320,320))
                    if rectRect(bird_pos.x-160, bird_pos.y-160,320,320 ,rec[0], rec[1], rec[2], rec[3]):
                        space.remove(prop, prop.body)
                        l_to_remove.append(prop)
                        #l_to_pop.append(i)
                    explosion_timer = 1
                    explosion_center = (bird_pos.x, bird_pos.y)
                    l_prop_memo = d_prop_info["shape"]
                    d_prop_info["shape"] = []
                    for prop in l_prop_memo:
                        if prop not in l_to_remove:
                            d_prop_info["shape"].append(prop)
                    ball.body.apply_impulse_at_local_point((velocity[0], -50000000),(0,0))
                    """poped_item=0
                    for val in l_to_pop:
                    d_prop_info["shape"].pop(i-poped_item)
                    poped_item+=1"""

                    #angle = prop.body.angle
                    #print(sommets_du_polygone, i)
                    #for v in sommets_du_polygone:
                    #    a = norm(v)
                    #    print(a)
                    #pygame.draw.line(screen, "black", ((sommets_du_polygone[0][0]+position[0]), (sommets_du_polygone[0][1]+position[1])), ((sommets_du_polygone[1][0]+position[0]), (sommets_du_polygone[1][1]+position[1])), 4)

                    # x =-1 * (a/c) * cos(omega) * (xB - xA) - (a/c) * sin(omega) * (yB-yA) + xB
                    # y = 1 * (a/c) * sin(omega) * (xB - xA) - (a/c) * cos(omega) * (yB-yA) + yB
                    #   How to get each variables:
                    #       c = normeAB => (xB-xA,yB-yB))
                    #       b = c
                    #       a = norm(BC =(a**2 = b**2 + c**2 - 2 * b) 
                    #       omega = (180-angle)/2
                    #       xA = position[0]
                    #       yA = position[1]
                    #       xB = (sommets_du_polygone[0][0]+position[0])
                    #       yB = (sommets_du_polygone[0][0]+position[0])
                    #
                    #
                    """
                    lenght = max(sommets_du_polygone, key=lambda x: x[1])[1] - min(sommets_du_polygone, key=lambda x: x[1])[1]
                    width = max(sommets_du_polygone, key=lambda x: x[0])[0] - min(sommets_du_polygone, key=lambda x: x[0])[0]
                    pygame.draw.rect(screen, "brown", pygame.Rect(prop.body.position[0]-width/2, prop.body.position[1]-lenght/2, width, lenght))
                    if rectRect(bird_pos.x-80, bird_pos.y-80,160, 120,prop.body.position[0]-width/2, prop.body.position[1]-lenght/2, width, lenght):
                        space.remove(d_prop_info["shape"][i-nb_poped_item], d_prop_info["shape"][i-nb_poped_item].body)
                        d_prop_info["shape"].pop(i-nb_poped_item)
                        nb_poped_item +=1
                    """
            elif birds_status == 4:
                pass
            elif birds_status == 5:
                velocity2 = [velocity[0], velocity[1]*4/3+15]
                ball2 = launch(velocity2, weight, radius)
                velocity3 = [velocity[0], velocity[1]*1/4-15]
                ball3 = launch(velocity3, weight, radius)
            elif birds_status == 6:
                velocity_egg = [velocity[0], velocity[1]]
                egg = launch(velocity_egg, weight, radius)
                egg.body.apply_impulse_at_local_point((velocity[0], 85000),(0,0))#Add an impulse relative 
                ball.body.apply_impulse_at_local_point((velocity[0], -50000000),(0,0))
    elif event == -1: #If mouse just got unpressed
        if dragging: #If the user was dragging the bird from the cata
            #We launch it
            dragging = False
            launching = True
            
            #The velocity applied is the distance dragged from origin point were the mouse was clicked
            velocity = [(pygame.mouse.get_pos()[0]-origin_coo[0]), (pygame.mouse.get_pos()[1]-origin_coo[1])]

            #If there is already a ball(reminder, ball = dynamic body) we remove it
            ball, bird_pos, launching, ball2, ball3, egg = remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching)
                

            ball = launch(velocity, weight, radius)

    if explosion_timer >0:
        for i in range(300):
            pygame.draw.circle(screen, random.choice(["grey", "red", "red", "red", "orange", "orange"]), (explosion_center[0]+random.randint(-160, 160), explosion_center[1]+random.randint(-160, 160)), 5)
        explosion_timer -= dt*3    
    if keys[pygame.K_r]:#If we press R key we reset bird's position
        ball, bird_pos, launching, ball2, ball3, egg = remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching)
    if dragging: #While we're dragging the bird:

        #We adjust the bird's postion for it stay under the mouse but not to teleport if the bird's wasn't clicked in it's center
        bird_pos.x = origin_bird_pos[0] + pygame.mouse.get_pos()[0] - origin_coo[0] 
        bird_pos.y = origin_bird_pos[1] + pygame.mouse.get_pos()[1] - origin_coo[1]

        #We draw the rubber band of the stone launcher
        pygame.draw.line(screen, "black", (bird_pos.x+5, bird_pos.y+25), (165, 565), 4)
        pygame.draw.line(screen, "black", (bird_pos.x+35, bird_pos.y+35), (190, 565), 4)
        #pygame.draw.line(screen, "black", (bird_pos.x+5, bird_pos.y+5), (bird_pos.x-25, bird_pos.y-5), 3)
    
    elif launching and ball: #If the bird is being launched and there is a ball:

        #We set it's position to be glued to the ball's position
        bird_pos.x = ball.body.position[0]
        bird_pos.y = ball.body.position[1]

    
    
    d_pig["last_vel"] = []
    for guy in d_pig["shape"]:
        d_pig["last_vel"].append(guy.body.kinetic_energy)

    d_prop_info["last_vel"] = []
    for prop in d_prop_info["shape"]:
        d_prop_info["last_vel"].append(prop.body.kinetic_energy)
    
    #We remember the status of the mouse for the next when we will use mouse_event()
    mouse_B4 = clicking()

    #Display the game on the screen
    pygame.display.flip()

    #limits FPS to 60
    #dt is delta time in seconds since last frame, used for framerate-independent physics.
    #In simpler terms, dt is the time between each frame
    dt = clock.tick(60) / 1000
    if dt > 1/30:
        dt = 1/30

    space.step(dt) #We advance the simulation by dt so it stays logical even in case of higher/lower fps
    clock.tick(60)
pygame.quit()
