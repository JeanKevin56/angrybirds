# Import
import pygame
import math
import pymunk
import pymunk.pygame_util
import random
from func import *

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

create_white_dot = True
l_white_dot=[]
explosion_center = (0,0)
explosion_timer =0
building_weight = 50
first_po_prop = None
dragging = False
launching = False
building = False
velocity = [0,0]
friction_factor = 2/3 
small_g = 9.81
l_rec = []
prop_dragged = None
dt = 0
bird_pos = pygame.Vector2(144, 547)
origin_bird_pos = (144,547)
white = (255, 255, 255)
font = pygame.font.Font('freesansbold.ttf', 32)
score = 0
radius = 20
ball = None
ball2, ball3 = None, None
paused = False
egg = None
capacity = False
mouse_B4 = False
placing = False
c_pressed = 0
weight = 10
frame_counter = 0
line_number = 0
gravity_multiplier = 100
l_timer_destruction = []
l_text = []
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
file_name = "map.txt"

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

terence_for_show = pygame.image.load('terence.png').convert_alpha()
terence_for_show = pygame.transform.scale_by(terence_for_show, 0.05)

terence = pygame.image.load('terence.png').convert_alpha()
terence = pygame.transform.scale_by(terence, 0.1)

blues = pygame.image.load('blues.png').convert_alpha()
blues = pygame.transform.scale_by(blues, 0.05)

matilda = pygame.image.load('matilda.png').convert_alpha()
matilda = pygame.transform.scale_by(matilda, 0.09)

king_pig = pygame.image.load('king_pig.png').convert_alpha()
king_pig = pygame.transform.scale_by(king_pig, 0.04)

pig = pygame.image.load('pig.png').convert_alpha()
pig = pygame.transform.scale_by(pig, 0.04)

hammer = pygame.image.load('hammer.png').convert_alpha()
hammer = pygame.transform.scale_by(hammer, 0.09)

bird = red

w, h = bird.get_size() #We get height and width of the current bird (red)

cata = pygame.image.load("catapult.png").convert_alpha()
cata = pygame.transform.scale_by(cata, 0.25)

background_image = pygame.image.load("background.jpg").convert()
background_image = pygame.transform.scale(background_image, (1600, 870)) 
#________________________________________________________________________


space = pymunk.Space() #Generate the pymunk space
space.gravity = (0, 0) #Sets its gravity to 0,0 so we calculate it manually
draw_options = pymunk.pygame_util.DrawOptions(screen) #Give the pygame screen to pymunk

#______________________________Setting up variables______________________________
save = rects_files(file_name, line_number)
rects = []

for i in range(int(len(save)/6)): #In the save, each rectangles has 6 parameters so we divid by 6 to get the nb of rect
    rects.append([(int(save[0+i*6]), int(save[1+i*6])), (int(save[2+i*6]), int(save[3+i*6])), int(save[4+i*6]), int(save[5+i*6])])
    #We add a rectangle,[(x, y), (w,h), color, mass]

#Place the props and note all of them in a list inside a dict
d_prop_info["shape"] = create_structure(space, rects)

for prop in d_prop_info["shape"]: #We itteratte for each prop: 
    #We note it's last velocity
    d_prop_info["last_vel"].append(prop.body.kinetic_energy)

#Create the limit of the map
map_limit(space)

#Create a pig and add it to a list inside a dictionary
d_pig["shape"].append(add_object(space, 1050, 350, 30, 10, 2))

"""handler = space.add_collision_handler(1,2)
handler.begin = ball.collision_handler"""
while running: #We loop while the game is running
    

    keys = pygame.key.get_pressed()#We get the current status of all keybord key

        

    for event in pygame.event.get():#We check the pygame event
        if event.type == pygame.QUIT: #If the user click the X
            running = False #We stop the loop
    
    #We apply the gravity to everything
    apply_gravity(d_prop_info, d_pig,ball, ball2, ball3, egg ,dt, small_g, gravity_multiplier ,prop_dragged)

    #We check if the pig as been "killed"
    l_to_remove = []
    for guy, last_vel in zip(d_pig["shape"], d_pig["last_vel"]): #For each pig
        
        #If the difference in velocity between 2 frames is to huge compare to it's mass (a heavier pig would need a more brutal shock)
        if abs(guy.body.kinetic_energy-last_vel) > 100000*guy.body.mass and not building: 
            
            #We remove the pig
            space.remove(guy, guy.body) #We remove it from the space
            l_to_remove.append(guy) #We will remove it from the list of current pig

            #We add the its position and other info to a list to show a cool effect to the score
            l_text.append([(guy.body.position[0], guy.body.position[1]), "10 000", (255,223,0), 2]) 
            score += 10000
        
        #We clear the list of shape and rebuild it without "dead" pig
        l_pig_memo = d_pig["shape"]
        d_pig["shape"] = []

        #For each pig in the game
        for piggy in l_pig_memo: 
            if piggy not in l_to_remove: #If we don't want to remove it
                d_pig["shape"].append(piggy) #We had him back to the list
    
    #pygame.draw.rect(screen, "black", pygame.Rect(bird_pos.x, bird_pos.y, round((1-explosion_timer)*3200), round((1-explosion_timer)*3200)))
    
    #We check if prop should be destroyed
    l_to_remove = []
    for prop, last_vel in zip(d_prop_info["shape"], d_prop_info["last_vel"]):#For each prop
        
        #If the difference in velocity between 2 frames is to huge compare to it's mass (a heavier prop would need a more brutal shock)
        if abs(prop.body.kinetic_energy-last_vel) > 50000*prop.body.mass and not building:
            
            #We remove the prop from the game
            space.remove(prop, prop.body)#We remove it from the pymunk space
            l_to_remove.append(prop) #We will remove it after the end of this loop
            l_timer_destruction.append([prop, 1]) #We add it to a list to make cool particles affect

            #We add the its position and other info to a list to show a cool effect to the score
            l_text.append([(prop.body.position[0], prop.body.position[1]), "1 000", (0,0,255), 0.8])
    
            score += 1000
        
        #We clear the list of shape and rebuild it without destroyed prop
        l_prop_memo = d_prop_info["shape"]
        d_prop_info["shape"] = []
        
        for prop in l_prop_memo: #For each prop
            if prop not in l_to_remove: #If the prop hasn't been destroyed
                d_prop_info["shape"].append(prop) # We add it back to the list
            
    event = mouse_event(mouse_B4) #get mouse event (check if mouse just got pressed/unpressed)

    l_text = show_score_on_screens(l_text, dt, font, screen) # We show the text needed on screen

    if event == 1: #If mouse just got pressed
        
        #If the mouse clicked on the bird while we aren't launching and the bird is on the screen (Not building)
        if abs(pygame.mouse.get_pos()[0]-bird_pos.x) < 30 and abs(pygame.mouse.get_pos()[1]-bird_pos.y) < 30 and not launching and bird:
           
            #It means we are dragging around the bird
            dragging = True
           
            #We note the coordinates to calculate how far the mouse moved
            origin_coo = pygame.mouse.get_pos()

        #If the mouse clicked in the top 50 pixels of the screen (Tool bar) and a bird is on the screen
        if pygame.mouse.get_pos()[1] < 50 and bird:
            """
            In this section we will to what's asked by the user
            Since to enter this if statement ths user has clicked in the top 50 pixels,
            We won't need to check the y coordinates of the mouse, only the x coordinates will need to be checked
            1st = Bring the bird to the catapult
            2nd = Rebuild the current structure
            3rd to 8th = List of bird
            9th = Building mode
            """

            #1 bring bird to cata
            if pygame.mouse.get_pos()[0] < 50:
                #We clear the game from any ball, and put it back on the cata (see remove_ball for more info)
                ball, bird_pos, launching, ball2, ball3, egg = remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching)
                #We give back the ability to use a special capacity
                capacity = False
                create_white_dot = True
            
            #2 Rebuild structure
            elif 50<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 100:
                #We destroy then rebuild evrything
                for props in d_prop_info["shape"]:#For each prop
                    space.remove(props, props.body)#We remove it from the space
                d_prop_info["shape"] = create_structure(space, rects) #We rebuild all props

            #________ List of all bird________
                """
            To change the bird, the code is the same way for each bird:
            bird  = new_bird
            birds_status = new_status (used for special capacity)
            weight = new_weight
            radius = new_bird_radius
            w,h = bird.get_size() #Set up the right size for the image used in some calculation
            """
            elif 100<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 200 and not launching:
                #1st bird : Red (The original)
                bird = red
                birds_status = 1
                weight = 10
                radius = 20
                w, h = bird.get_size()
            elif 200<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 300 and not launching:
                #2nd bird : Chuck (The yellow one with a dash)
                bird = chuck
                birds_status = 2
                weight = 17
                radius = 20
                w, h = bird.get_size()
            elif 300<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 400 and not launching:
                #4rd bird : Bomb (The black explosive one)   
                bird = bomb
                birds_status = 3
                weight = 25
                radius = 25
                w, h = bird.get_size()
            elif 400<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 500 and not launching:
                #5th bird : Terence (The big red one, no capacity except being overweight)
                bird = terence
                birds_status = 4
                weight = 100
                radius = 35
                w, h = bird.get_size()
            elif 500<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 600 and not launching:
                #6th bird : Blues (The blue one that divide into three 3 blue birds (They are brothers named Jay, Jake and Jim))
                bird = blues
                birds_status = 5
                weight = 6
                radius = 13
                w, h = bird.get_size()
            elif 600<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 700 and not launching:
                #7th bird : Matilda (The white one that shoots a egg to the ground)
                bird = matilda
                birds_status = 6
                weight = 20
                radius = 25
                w, h = bird.get_size()
            #________End list of bird________
            
            #9 Building mode
            elif 700<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 800 and not launching:
                bird = hammer #We swape the bird to the hammer
                birds_status = -1 #The status is changed to -1 to prevent capacity or other bug
                bird = None #We remove the bird
                building = True #We set ourselves in building mode
        
        #If the mouse clicked on the tool bar while we are in building mode
        elif pygame.mouse.get_pos()[1] < 50 and building:
            """
            This is a list of all possible action in the tool bar
            While being in the buiding mode

            """
            
            #Previous preset
            #This will clear the map and load the n-1 preset
            if pygame.mouse.get_pos()[0] < 50:
                rects = []
                line_number-=1 #Take the previous line numer
                save = rects_files(file_name, line_number) #Get the save from the save file

                for i in range(int(len(save)/6)): #For each prop in the save file
                    #We place it up in a list
                    rects.append([(int(save[0+i*6]), int(save[1+i*6])), (int(save[2+i*6]), int(save[3+i*6])), int(save[4+i*6]), int(save[5+i*6])])
                
                #We clear every current shape from the sapce
                for props in d_prop_info["shape"]:
                    space.remove(props, props.body)
                
                #We put all new shape in the list that keep tracks of props 
                #And we add them to the space at the same time
                d_prop_info["shape"] = create_structure(space, rects)
            
            #Next preset
            #This will clear the map and load the n+1 preset
            elif 50<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 100:
                rects = []
                line_number+=1 #Take the next line numer
                save = rects_files(file_name, line_number) #Get the save from the save file
                for i in range(int(len(save)/6)):  #For each prop in the save file
                    #We place it in a list
                    rects.append([(int(save[0+i*6]), int(save[1+i*6])), (int(save[2+i*6]), int(save[3+i*6])), int(save[4+i*6]), int(save[5+i*6])])
                
                #We clear every current shape from the sapce
                for props in d_prop_info["shape"]:
                    space.remove(props, props.body)
                
                #We put all new shape in the list that keep tracks of props 
                #And we add them to the space at the same time
                d_prop_info["shape"] = create_structure(space, rects)
            
            #Re launch the game
            #This will quit the building mode, restore all parameters to be ready to play
            elif 100<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 200:
                #We initialize all variables back to being able to play normally
                building = False
                placing = False
                first_po_prop = None
                prop_dragged = None
                paused = False
                l_white_dot = [] 
                small_g = 9.81
                bird = red
                birds_status = 1
                weight = 10
                radius = 20
                w, h = bird.get_size()
            
            #Instant clear
            #We instantly clears the map from any props
            elif 200<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 300:
                for props in d_prop_info["shape"]:
                    space.remove(props, props.body)
                d_prop_info["shape"] = []
            
            #Placing mode
            #This puts the user in placing mode
            #A black dot will be on the cursor of the user to indicate that he is in placing mode
            elif 300<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 400:
                #Depending on whether the user was already in placing mode or not
                #We change the mode to be placing / not longer placing
                if not placing: 
                    placing = True
                    first_po_prop = None
                else:
                    placing = False
                    first_po_prop = None
            
                """
                While in placing mode, the weight of the the structure matter so to change it
                There is 4 buttons to add restictively from left to right:
                50, 5, -5, -50
                Made for user to adjust the weight without having to spam a +1 a hundred times
                """
            elif 400<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 450:
                building_weight += 50
            elif 450<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 500:
                building_weight +=5
            elif 500<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 550:
                if building_weight > 5:
                    building_weight -=5
            elif 550<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 600:
                if building_weight > 50:
                    building_weight -=50
            
            #Save
            #We get the position of all props in the game and store them in a text file
            elif 600<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 700:
                rects = []
                line= ""
            
                #For each prop
                for prop in d_prop_info["shape"]:
                    polygon_verticles = prop.get_vertices() #We get all the polygons verticles
                    position = prop.body.position #We store it's position
                    mass = prop.body.mass
                    #We get the size of the said polygone
                    width = max(polygon_verticles, key=lambda x: x[0])[0] - min(polygon_verticles, key=lambda x: x[0])[0]
                    length = max(polygon_verticles, key=lambda x: x[1])[1] - min(polygon_verticles, key=lambda x: x[1])[1]
                    
                    rects.append([position, (width, length), 0, mass])
                for rec in rects:
                    #We add all of the props caracteristics to the line
                    #We do so for eac prop
                    line += str(round(rec[0][0]))+";"+str(round(rec[0][1]))+";"+str(round(rec[1][0]))+";"+str(round(rec[1][1]))+";"+str(round(rec[2]))+";"+str(round(rec[3]))+";"
                
                #Finally we write the line
                with open(file_name, "a") as f:
                    f.write(line+"\n")
                    f.close()
            
            #Pause
            #We stop the game from calculating gravity, mouvement, rotation etc..
            elif 700<pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < 800:
                if paused:
                    paused = False
                    small_g = 9.81
                else:
                    paused = True
        
        #If we are in placing mode
        elif placing:
            #If we've already placed a point
            if first_po_prop:
                #We get the size of the prop depending on how far is the click for the first placed point 
                #(We set the distance to 1 if it's 0 to prevent bug while placing the block)
                size = (pygame.mouse.get_pos()[0]-first_po_prop[0] if pygame.mouse.get_pos()[0]-first_po_prop[0]!=0 else 1,
                        pygame.mouse.get_pos()[1]-first_po_prop[1] if pygame.mouse.get_pos()[1]-first_po_prop[1]!=0 else 1)

                #We add the new structures to the list of structure while creating it on the space
                d_prop_info["shape"]+=create_structure(space, [[(first_po_prop[0]+size[0]/2, first_po_prop[1]+size[1]/2),size , 0, building_weight]])
                first_po_prop = None
                l_white_dot = []
            else:
                #If it's the first click we get the clicked_position
                first_po_prop = pygame.mouse.get_pos()
                #We add a point on the screen where the mouse was clicked
                l_white_dot.append((screen, "black", first_po_prop, 10))
        
        #If we are in the building mode without being in placing mode
        elif building and not placing: #The "and not placing" is useless but it's to be clear
            """
            This function will help the user to select a given prop
            He will then be able to perform action on it such as rotating it
            Moving it to follow the mouse
            Copy it or delete it
            """
            #If we clicked while dragging a prop, we are no longer dragging it
            if prop_dragged:
                prop_dragged = None

            #If we aren't already dragging a prop
            else:
                #We check the collision for each prop, if we are touching one
                #We set it as the prop we are dragging
                for prop in d_prop_info["shape"]:
                    polygon_verticles = prop.get_vertices() #We get all the polygons verticles
                    position = prop.body.position #We store it's position
                    
                    #We get the size of the said polygone
                    length = max(polygon_verticles, key=lambda x: x[1])[1] - min(polygon_verticles, key=lambda x: x[1])[1]
                    width = max(polygon_verticles, key=lambda x: x[0])[0] - min(polygon_verticles, key=lambda x: x[0])[0]

                    prop_image = pygame.Surface((width, length)) #We create a surface
                    new_image = pygame.transform.rotate(prop_image, prop.body.angle*-180/math.pi) #We rotate with the right angle
                    rec = new_image.get_rect() #We get the rectangle of the image
                    rec.center = position #We set the center of the new rectangle to the old position so it stays centered
                    if rectRect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0, rec[0], rec[1], rec[2], rec[3]):
                        prop_dragged = prop

        #If the bird is being launched and we hav'nt used it's special ability
        elif launching and not capacity:
            """
            For each status of bird, we apply different ability
            """
            #Chuck
            #The Yellow One
            if birds_status == 2:
                capacity = True
                #We give a boost in speed forward
                ball.body.apply_impulse_at_local_point((25000,0),(0,0))
            
            #Bomb
            #The Black One
            elif birds_status == 3:
                capacity = True
                #We give him a giantic boost so he glitch out of the screen but we don't remove him to prevent having bugs
                ball.body.apply_impulse_at_local_point((velocity[0], -50000000),(0,0))

                #We set up variable for the explosion to work properly
                explosion_timer = 1
                explosion_center = (bird_pos.x, bird_pos.y)

                #We call the explosion function
                d_prop_info, score,l_text = explode_prop(space, d_prop_info, explosion_center, explosion_timer, score, l_text)
            
            #The blues
            #The little blue one
            elif birds_status == 5:
                capacity = True
                #We create 2 more birds with a boost slightly downward and upward
                velocity2 = [velocity[0], velocity[1]*4/3+15]
                ball2 = launch(velocity2, weight, radius, space, ball.body.position, 0)
                velocity3 = [velocity[0], velocity[1]*1/4-15]
                ball3 = launch(velocity3, weight, radius, space, ball.body.position, 0)
            
            #Matilda
            #The White One
            elif birds_status == 6:
                capacity = True

                #We summon an egg that comes slamming down into the ground
                velocity_egg = [velocity[0], velocity[1]]
                egg = launch(velocity_egg, weight, radius, space, ball.body.position, 0)
                egg.body.apply_impulse_at_local_point((velocity[0], 88000),(0,0))#Add an impulse relative 
                ball.body.apply_impulse_at_local_point((velocity[0], -50000000),(0,0))
    
    elif event == -1: #If mouse just got unpressed
        if dragging: #If the user was dragging the bird from the cata
            #We launch it
            dragging = False
            launching = True
            l_white_dot = []
            #The velocity applied is the distance dragged from origin point were the mouse was clicked
            velocity = [(pygame.mouse.get_pos()[0]-origin_coo[0]), (pygame.mouse.get_pos()[1]-origin_coo[1])]

            #If there is already a ball(reminder, ball = body) we remove it
            ball, bird_pos, launching, ball2, ball3, egg = remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching)
                
            #Finally we launch the bird
            #Given the velocity calculated up above
            ball = launch(velocity, weight, radius, space, bird_pos, 1)


    if prop_dragged: #If the user has selected a prop
        #We move to props to stay under the cursor
        prop_dragged.body.position = pygame.mouse.get_pos()

        #We draw a white cirlce on the selected to prop to show the user clearly which prop has been selected
        #And to clarify IF a prop has been selected
        pygame.draw.circle(screen, "white", prop_dragged.body.position, 10)

        if keys[pygame.K_c]:
            if c_pressed == 0:
                c_pressed = 1
            else:
                c_pressed = -1
        else:
            c_pressed = 0

        #If we pres a or e we rotate the prop
        if keys[pygame.K_e]:
            prop_dragged.body.angle +=2*dt
        elif keys[pygame.K_a]:
            prop_dragged.body.angle -=2*dt
        
        #If we press d we delete the prop from the game
        elif keys[pygame.K_d]:
            #We remove it from the space
            space.remove(prop_dragged, prop_dragged.body)
            d_memo = d_prop_info["shape"]
            d_prop_info["shape"] = []
            #We remove it from the list of props
            for prop in d_memo:
                if prop != prop_dragged:
                    d_prop_info["shape"].append(prop)
            #We are no longer dragging anything
            prop_dragged = None
        
        #If we pressed c we duplicate the current prop
        elif c_pressed == 1:
            polygon_verticles = prop_dragged.get_vertices() #We get all the polygons verticles
            position = prop_dragged.body.position #We store it's position        
            #We get the size of the said polygone
            width = max(polygon_verticles, key=lambda x: x[0])[0] - min(polygon_verticles, key=lambda x: x[0])[0]
            length = max(polygon_verticles, key=lambda x: x[1])[1] - min(polygon_verticles, key=lambda x: x[1])[1]
            
            #We create another prop with the same parameter as the selected one
            d_prop_info["shape"]+=create_structure(space, [[prop_dragged.body.position,(width, length) , 0, prop.body.mass]])

    if explosion_timer > 0: #If there is an explosion on going
        #We explode the prop according to the explosion's center, it's evolution
        #And update the prop list according to it
        d_prop_info, score, l_text = explode_prop(space, d_prop_info, explosion_center, explosion_timer, score, l_text)

        #We draw 350 points
        for i in range(350):
            #We get a random position for the center point
            explo_co = [random.randint(-500, 500), random.randint(-500, 500)]

            #We get the invers of the norm to stay propotionnal
            if explo_co != [0, 0]:
                k = 1/norm(explo_co)
            else:
                k= 1

            #The minimum distance between the point and the explosion wave
            distance_min = round((1-explosion_timer)*160)-30

            #If it's negative we set it to 0
            if distance_min<0:
                distance_min=0
            
            #The distance is therfore choosen randomly between the minimum distance and
            #A value time 160 that increase as the timer decrease reaching eventually close to 160
            distance = random.randint(distance_min, round((1-explosion_timer)*160))
            #distance = random.randint(0, round((1-explosion_timer)*160))
            #This is an alternative without the wave effect   /\
            #                                                 ||

            #We multiply the random value by the inverse of the norm to keep it proportinnal 
            #Which give us a random direction
            #We then multiply by the previously caluclated distance
            explo_co[0] *= k*distance
            explo_co[1] *= k*distance

            #We place the point relatively to the center of the explosion
            explo_co[0] += explosion_center[0]
            explo_co[1] += explosion_center[1]

            #We draw it in a random color at the given place
            pygame.draw.circle(screen, random.choice(["grey", "red", "red", "red", "orange", "orange"]), (explo_co[0], explo_co[1]), 5)
        #We decrease the timer by dt (times 4 to speed things up but it's open to being changed)
        explosion_timer -= dt*4
    
    for i in range(len(l_timer_destruction)): #If a prop as been destroyed, for each destryoed prop
        #while the timer is postive
        if l_timer_destruction[i][1] > 0:
            #We draw 45 points colored randomly to show a destruction effect
            for j in range(45):
                pygame.draw.circle(screen, random.choice(["white", "white", "white", "gray", "gray", "black"]), (l_timer_destruction[i][0].body.position[0]+random.randint(-100, 100), l_timer_destruction[i][0].body.position[1]+random.randint(-100, 100)), 5)
        l_timer_destruction[i][1] -= dt*5
    
    if keys[pygame.K_r] and bird:#If we press R key we reset bird's position
        #We remove all body on the screen
        #And reset variables to be able to launch again
        ball, bird_pos, launching, ball2, ball3, egg = remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching)
        capacity = False
        create_white_dot = True
        l_white_dot = []

    if dragging: #While we're dragging the bird:

        #We adjust the bird's postion for it stay under the mouse but not to teleport if the bird's wasn't clicked in it's center
        bird_pos.x = origin_bird_pos[0] + pygame.mouse.get_pos()[0] - origin_coo[0] 
        bird_pos.y = origin_bird_pos[1] + pygame.mouse.get_pos()[1] - origin_coo[1]

        #We draw the rubber band of the stone launcher
        pygame.draw.line(screen, "black", (bird_pos.x-w/2, bird_pos.y+5), (165, 565), 4)
        pygame.draw.line(screen, "black", (bird_pos.x+w/2, bird_pos.y+15), (190, 565), 4)
        #pygame.draw.line(screen, "black", (bird_pos.x+5, bird_pos.y+5), (bird_pos.x-25, bird_pos.y-5), 3)
    
    elif launching and ball: #If the bird is being launched and there is a ball:

        #We set the image's position to be glued to the ball's position
        bird_pos.x = ball.body.position[0]
        bird_pos.y = ball.body.position[1]
        if frame_counter%3==0 and create_white_dot:
            l_white_dot.append((screen, "black", (bird_pos.x, bird_pos.y), 5))
    
    if paused:
        small_g = 0
        for prop in d_prop_info["shape"]:
            prop.body.velocity = (0,0)
            prop.body.angular_velocity = 0
        for guy in d_pig["shape"]:
            guy.body.velocity = (0,0)
            guy.body.angular_velocity = 0

    for dot in l_white_dot: #For each dot we want to draw
        #We draw it to the asked position with the asked color and radius
        pygame.draw.circle(dot[0], dot[1], dot[2], dot[3])
    
    d_pig["last_vel"] = []
    for guy in d_pig["shape"]: #For each pig we note it's last velocity 
        #It's used to calculate the difference of velocity and in the end, calculate if the pig should "die"
        d_pig["last_vel"].append(guy.body.kinetic_energy)
    
    
    d_prop_info["last_vel"] = []
    for prop in d_prop_info["shape"]: #For each prop
        if ball: #If a body exist
            polygon_verticles = prop.get_vertices() #We get all the polygons verticles
            position = prop.body.position #We store it's position
                        
            #We get the size of the said polygone
            length = max(polygon_verticles, key=lambda x: x[1])[1] - min(polygon_verticles, key=lambda x: x[1])[1]
            width = max(polygon_verticles, key=lambda x: x[0])[0] - min(polygon_verticles, key=lambda x: x[0])[0]

            prop_image = pygame.Surface((width, length)) #We create a surface
            new_image = pygame.transform.rotate(prop_image, prop.body.angle*-180/math.pi) #We rotate with the right angle
            rec = new_image.get_rect() #We get the rectangle of the image
            rec.center = position #We set the center of the new rectangle to the old position so it stays centered

            #If the bird is hitting a prop
            if rectRect(ball.body.position[0]-radius, ball.body.position[1]-radius, radius*2+10, radius*2+10,rec[0], rec[1], rec[2], rec[3]):
                #We stop placing dots
                create_white_dot = False
                #Execpt if it's Bomb we stop it from using his capacity
                #Why is bomb exempted ? Bcs it's funny and i like it so be it
                if birds_status !=3:
                    capacity = True
        #We note the lastest velocity of the prop to calc if it will be destroyed
        d_prop_info["last_vel"].append(prop.body.kinetic_energy)
    

    #We remember the status of the mouse for the next when we will use mouse_event()
    mouse_B4 = clicking()

    #Display the game on the screen
    pygame.display.flip()

    #limits FPS to 60
    #dt is delta time in seconds since last frame used in multiple operation
    #It's the time between each frame
    dt = clock.tick(60) / 1000
    #We cap dt so it's doesn't give a huge value if it freezes
    #Or when you drag the pygame window the game stop calculating but dt ain't stopping
    if dt > 1/30:
        dt = 1/30

    space.step(dt) #We advance the simulation by dt so it stays logical even in case of higher/lower fps
    clock.tick(60)
    frame_counter +=1
    
    #We draw evrything 
    draw(screen, space, draw_options, 
         bird, bird_pos, w,h, 
         ball, ball2 , ball3, 
         font, score, 
         background_image, cata, d_pig, pig, red, chuck, bomb, terence_for_show, terence, blues, matilda, king_pig, hammer, 
         building, placing, building_weight)

pygame.quit()
