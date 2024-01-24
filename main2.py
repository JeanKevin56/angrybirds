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

#______________________________ Variable initialisation______________________________
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
l_rec = []
#2/3; 7/12; 3/4; 1/2
dt = 0
bird_pos = pygame.Vector2(144, 547)
origin_bird_pos = (144,547)
white = (255, 255, 255)
font = pygame.font.Font('freesansbold.ttf', 32)
score = 0
radius = 10
ball = None
ball2, ball3 = None, None
egg = None
capacity = False
mouse_B4 = False
weight = 10
l_timer_destruction = []
l_timer_death = []
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
#name_image = pygame.image.load('image.extension').convert_alpha() <- convert alpha makes images use much faster
#name_image = pygame.transform.scale_by(name_image, factor by which we multiply the size of the image)
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

hammer = pygame.image.load('hammer.png').convert_alpha()
hammer = pygame.transform.scale_by(hammer, 0.04)

bird = red
bird_original = bird

w, h = bird.get_size() #We get height and width of the current bird (red)

cata = pygame.image.load("catapult.png").convert_alpha()
cata = pygame.transform.scale_by(cata, 0.25)

background_image = pygame.image.load("background.jpg").convert()
background_image = pygame.transform.scale(background_image, (1600, 870)) 
#________________________________________________________________________


space = pymunk.Space() #Generate the pymunk space
space.gravity = (0, 0) #Sets its gravity to 0,0 so we calculate it manually
draw_options = pymunk.pygame_util.DrawOptions(screen) #Give the pygame screen to pymunk
def clicking():#Send True if the mouse is pressed
    return pygame.mouse.get_pressed()[0]

def mouse_event(mouse_B4): #Give info about the state of the mouse's buttons
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

def scalar(v1, v2):#Return the scalar of 2 vector
    """
    Return the scalar of 2 vector
    """
    if len(v1) != len(v2):
        raise ValueError("2 vec différents lors d'un scalire est impossible")
    summ =0
    for i in range(len(v1)):
        summ+=v1[i]*v2[i]
    return summ

def norm(vector):#Return the norm of a vector
    
    summ = 0
    for val in vector:
        summ +=val*val
    return math.sqrt(summ)

def draw(screen, space, draw_options, bird, bird_pos, w,h, ball, ball2 , ball3, font, score): #Draw everything for the game to render correctly
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
    text = font.render("Score : "+str(score), True, (255,255,255))

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()# GET REKT

    # set the center of the rectangular object.
    textRect.center = (1300, 20)
    screen.blit(text, textRect)
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
        [(0, h/2), (40, h)],
        [(w, h/2), (40, h)]
    ]
    #Similar to the previous function "create_structure", refer to it if you have question about this code
    for r in rec:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = r[0]
        shape = pymunk.Poly.create_box(body, r[1])
        shape.elasticity = 0.4
        shape.friction = 0.2
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
    shape.elasticity = 2/3 #Give an elasticity
    shape.friction = 3/4 #And a friction
    space.add(body, shape) #Then adds it to the pymnuk space
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
                                                                                    #to how far the bird was dragged and to the bird's weight
    return ball

def rectRect(r1x, r1y, r1w, r1h, r2x, r2y, r2w, r2h): #Say if 2 rectangle are touching each other
    """
    Input:
        r1x, r1y, = coordinates of the 1st rectangle
        r1w, r1h, = width and length of the 1st rectangle
        
        r2x, r2y, = coordinates of the 2nd rectangle
        r2w, r2h  = width and length of the 2nd rectangle
    Output:
        Bool: True => They are touching
              False =>They ain't touching 
    
    """
    return r1x + r1w >= r2x and r1x <= r2x + r2w and r1y + r1h >= r2y and r1y <= r2y + r2h

def gravity_formula(shape, dt, small_g=9.81, aditionnal_multiplier=100):
    #shorten lines that uses this formula
    return [aditionnal_multiplier*dt*small_g*shape.body.mass*math.sin(shape.body.angle) , aditionnal_multiplier*dt*small_g*shape.body.mass*math.sin(shape.body.angle+math.pi/2)]

def apply_gravity(d_prop_info, ball, ball2, ball3, egg ,dt):
    for prop in d_prop_info["shape"]: #For each prop
        g = gravity_formula(prop, dt) #We calculate the gravity formula related to it
        prop.body.apply_impulse_at_local_point((g[0],g[1]),(0,0)) #We apply an impulse depending on that gravity formula
    
    #We then do the same thing for the shape and guy(pig) so evry1 gets gravity YAY !
    for shape in [ball, ball2, ball3, egg]:
        if shape:
            g = gravity_formula(shape, dt)
            shape.body.apply_impulse_at_local_point((g[0],g[1]),(0,0))
    for guy in d_pig["shape"]:
        g = gravity_formula(guy, dt)
        guy.body.apply_impulse_at_local_point((g[0],g[1]),(0,0))

def remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching):
    if ball: #If there is currently a ball
        space.remove(ball, ball.body) #We remove it
        ball = None #We set it back to being None
        launching = False #If there is no ball then nothing is being launched

        #We reset the birds Position
        bird_pos.x = origin_bird_pos[0] 
        bird_pos.y = origin_bird_pos[1]

        #If we have a 2 other balls or if we have an egg, we remove them too
        if ball2 and ball3: 
            space.remove(ball2, ball2.body)
            space.remove(ball3, ball3.body)
            ball2, ball3 = None, None
        elif egg:
            space.remove(egg, egg.body)
            egg = None
    return (ball, bird_pos, launching, ball2, ball3, egg)

def explode_prop(space, d_prop_info, explosion_center, explosion_timer, score):
    l_to_remove = []
    for prop in d_prop_info["shape"]:#For each prop
        polygon_verticles = prop.get_vertices() #We get all the polygons verticles
        position = prop.body.position #We store it's position
        
        #We get the size of the said polygone
        length = max(polygon_verticles, key=lambda x: x[1])[1] - min(polygon_verticles, key=lambda x: x[1])[1]
        width = max(polygon_verticles, key=lambda x: x[0])[0] - min(polygon_verticles, key=lambda x: x[0])[0]

        explosion_image = pygame.Surface((width, length)) #We create a surface
        new_image = pygame.transform.rotate(explosion_image, prop.body.angle*-180/math.pi) #We rotate with the right angle
        rec = new_image.get_rect() #We get the rectangle of the image
        rec.center = position #We set the center of the new rectangle to the old position so it stays centered
        if rectRect(explosion_center[0]-160, explosion_center[1]-160,320*(1-explosion_timer),320*(1-explosion_timer),rec[0], rec[1], rec[2], rec[3]):#If the explosion collides with a prop:
            #We add score
            score += 1000
            #_____We remove it_____
            space.remove(prop, prop.body)
            l_to_remove.append(prop)
        
        
        l_prop_memo = d_prop_info["shape"]
        d_prop_info["shape"] = []
        for prop in l_prop_memo:
            if prop not in l_to_remove:
                d_prop_info["shape"].append(prop)
        #_________________________________________
    return (d_prop_info, score)
#Place the props
d_prop_info["shape"] = create_structure(space, 1600, 720)
for prop in d_prop_info["shape"]:
    d_prop_info["last_vel"].append(prop.body.kinetic_energy)
#Create the limit of the map
map_limit(space)

#Create a pig
d_pig["shape"].append(add_object(space, 1050, 100, 30, 10))


while running:

    keys = pygame.key.get_pressed()
    # pygame.QUIT event means the user clicked X to bod.close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    apply_gravity(d_prop_info, ball, ball2, ball3, egg ,dt)

    l_to_remove = []
    for guy, last_vel in zip(d_pig["shape"], d_pig["last_vel"]):
        if abs(guy.body.kinetic_energy-last_vel) > 100000*guy.body.mass:
            space.remove(guy, guy.body)
            l_to_remove.append(guy)
            l_timer_death.append([guy, 1])
            score += 10000
        l_pig_memo = d_pig["shape"]
        d_pig["shape"] = []
        for piggy in l_pig_memo:
            if piggy not in l_to_remove:
                d_pig["shape"].append(piggy)
    #Affiche 
    draw(screen, space, draw_options, bird, bird_pos, w,h, ball, ball2 , ball3, font, score)
    #print((1-explosion_timer))
    #pygame.draw.rect(screen, "black", pygame.Rect(bird_pos.x, bird_pos.y, round((1-explosion_timer)*3200), round((1-explosion_timer)*3200)))
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
                l_timer_destruction.append([prop, 1])
                score += 1000
            l_prop_memo = d_prop_info["shape"]
            d_prop_info["shape"] = []
            for prop in l_prop_memo:
                if prop not in l_to_remove:
                    d_prop_info["shape"].append(prop)
    event = mouse_event(mouse_B4) #get mouse event (check if mouse just got pressed/unpressed)

    if event == 1: #If mouse just got pressed
        if abs(pygame.mouse.get_pos()[0]-bird_pos.x) < 30 and abs(pygame.mouse.get_pos()[1]-bird_pos.y) < 30 and not launching:
            dragging = True
            origin_coo = pygame.mouse.get_pos()
        if pygame.mouse.get_pos()[1] < 50:
            if pygame.mouse.get_pos()[0] < 50:
                ball, bird_pos, launching, ball2, ball3, egg = remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching)
                capacity = False
            elif 50<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 100:
                for props in d_prop_info["shape"]:
                    space.remove(props, props.body)
                d_prop_info["shape"] = create_structure(space, 1600, 720)
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
        elif launching and not capacity:
            if birds_status == 2:
                capacity = True
                ball.body.apply_impulse_at_local_point((25000,0),(0,0))
                
            elif birds_status == 3:
                capacity = True
                ball.body.apply_impulse_at_local_point((velocity[0], -50000000),(0,0))
                explosion_timer = 1
                explosion_center = (bird_pos.x, bird_pos.y)
                d_prop_info, score = explode_prop(space, d_prop_info, bird_pos, explosion_timer, score)
            elif birds_status == 4:
                capacity = True
                pass
            elif birds_status == 5:
                capacity = True
                velocity2 = [velocity[0], velocity[1]*4/3+15]
                ball2 = launch(velocity2, weight, radius)
                velocity3 = [velocity[0], velocity[1]*1/4-15]
                ball3 = launch(velocity3, weight, radius)
            elif birds_status == 6:
                capacity = True
                velocity_egg = [velocity[0], velocity[1]]
                egg = launch(velocity_egg, weight, radius)
                egg.body.apply_impulse_at_local_point((velocity[0], 88000),(0,0))#Add an impulse relative 
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

    if explosion_timer > 0:
        d_prop_info = explode_prop(space, d_prop_info, explosion_center, explosion_timer, score)
        for i in range(350):            
            explo_co = [random.randint(-160, 160), random.randint(-160, 160)]
            k = 1/(math.sqrt(explo_co[0]**2+explo_co[1]**2)) if explo_co != [0, 0] else 1
            minDist = round((1-explosion_timer)*160)-30
            distance = random.randint(minDist if minDist >= 0 else 0, round((1-explosion_timer)*160))
            #distance = random.randint(0, round((1-explosion_timer)*160))
            explo_co[0] *= k*distance
            explo_co[1] *= k*distance
            explo_co[0] += explosion_center[0]
            explo_co[1] += explosion_center[1]
            pygame.draw.circle(screen, random.choice(["grey", "red", "red", "red", "orange", "orange"]), (explo_co[0], explo_co[1]), 5)
        explosion_timer -= dt*4
    
    for i in range(len(l_timer_destruction)):
        if l_timer_destruction[i][1] > 0:
            for j in range(45):
                pygame.draw.circle(screen, random.choice(["white", "white", "white", "red", "orange", "orange"]), (l_timer_destruction[i][0].body.position[0]+random.randint(-100, 100), l_timer_destruction[i][0].body.position[1]+random.randint(-100, 100)), 5)
        l_timer_destruction[i][1] -= dt*5
    if keys[pygame.K_r]:#If we press R key we reset bird's position
        ball, bird_pos, launching, ball2, ball3, egg = remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching)
        capacity = False
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
