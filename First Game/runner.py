import pygame #module
from sys import exit
from random import randint

def player_animation():
    # if on floor then walking animation else jump animation
    global player_surface, player_index

    if player_rectangle.bottom < 300:
        player_surface = player_jump # jump surface
    else:
        player_index += 0.1
        if player_index >= len(player_walk) :
            player_index = 0
        player_surface = player_walk[int(player_index)] # cycles through the two player surfaces

def obstacle_movement(obstacle_rectangle_list):
    if obstacle_rectangle_list: # if list [] then False
        for obstacle in obstacle_rectangle_list:
            obstacle.x -= 5
            if obstacle.bottom == 300:
                screen.blit(snail_surface,obstacle)
            else:
                screen.blit(fly_surface,obstacle)
        obstacle_rectangle_list = [obs for obs in obstacle_rectangle_list if obs.x > -50]
        # only getting the obs if its on the screen. Will delete the off screen obs by itself 
        # by not taking them back in the list.
        return obstacle_rectangle_list
    else:
        return []
    
def collisions(player, obstacles):
    if obstacles:
        for obs in obstacles:
            if player.colliderect(obs):
                return False
    return True

def display_score():
    current_time = pygame.time.get_ticks()//1000 - start_time # //1000 to get seconds.
    score_surface = test_font.render(f'{current_time}',False,(64,64,64)) #rgb
    score_rectangle = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rectangle)
    return current_time

pygame.init() #initialize
screen = pygame.display.set_mode((800,400)) #displaysurface (width,height)
pygame.display.set_caption('Running Game') #title of game
clock = pygame.time.Clock() #clock for constant frame rate
test_font = pygame.font.Font('font/Pixeltype.ttf',50) #fontregular (style,size)
game_active = False # intro and gameover are same!
start_time = 0
score = 0

#test_surface = pygame.Surface((800,400)) #regularsurface (w,h)
#test_surface.fill('coral') #Plain colour regularsurface

#red = pygame.Surface((100,200)) #(w,h)
#red.fill('Red') #typeofcolor

sky_surface = pygame.image.load('graphics/Sky.png').convert() #imageregularsurface
ground_surface = pygame.image.load('graphics/ground.png').convert()

title_surface = test_font.render('Look at em go!!!',False,(64,64,64)) #textregularsurface (prompt,AA,color) 
# color either rgb, hex or predet by pygame.
title_rectangle = title_surface.get_rect(center = (400,100)) #topleft , midbottom , center

# Obstacles
# snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha() #snailenemy
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_2,snail_frame_1]
snail_index = 0
snail_surface = snail_frames[snail_index]
#snail_x_pos = 800 #original position
#snail_y_pos = 265 #original position
#snail_rectangle = snail_surface.get_rect(midbottom = (800,300))
# fly_surface = pygame.image.load('graphics/Fly/fly1.png').convert_alpha() #flyenemy
fly_frame_1 = pygame.image.load('graphics/Fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_2,fly_frame_1]
fly_index = 0
fly_surface = fly_frames[fly_index] 

obstacle_rectangle_list = []

# Player
# player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha() #player
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha() #player
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha() #player
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha() #player

player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(midbottom = (80,300)) #player rectangle #midbottom , topleft , etc...

#intro // gameover
player_stand_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface,0,2) # scaling to make it better
player_stand_rectangle = player_stand_surface.get_rect(center = (400,200)) # middle
name_surface = test_font.render('Running Game',False,(111,196,169))
name_rectangle = name_surface.get_rect(center = (400,80))
instruction_surface = test_font.render('Press Space to Start',False,(64,64,64))
instruction_rectangle = instruction_surface.get_rect(center = (400,350))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200) # faster than the snail animation

player_gravity = 0

# Music
jump_sound = pygame.mixer.Sound('audio/jump.mp3') # a bit loud tho
jump_sound.set_volume(0.1) # 0->1
background_music = pygame.mixer.Sound('audio/music.wav')
background_music.set_volume(0.3)
background_music.play(loops = -1) # loop forever

while True: #all game inside loop
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit
            pygame.quit() #exit loop when window is closed # opposite of pygame.init()
            exit() #breaks while True loop
        if game_active:
            if event.type == pygame.KEYDOWN: # input space bar whenever on 'floor'
                if event.key == pygame.K_SPACE and player_rectangle.bottom == 300:
                    print('jump!')
                    player_gravity = -23 # moving player up
                    jump_sound.play()
            if event.type == pygame.KEYUP:
                print('released')

            if event.type == obstacle_timer: # timer
                if randint(0,2):
                    obstacle_rectangle_list.append(snail_surface.get_rect(bottomright=(randint(900,1100),300)))
                else:
                    obstacle_rectangle_list.append(fly_surface.get_rect(bottomright=(randint(900,1100),200)))
            
            # animations
            if event.type == snail_animation_timer:
                snail_index = 0 if snail_index == 1 else 1
            snail_surface = snail_frames[snail_index]

            if event.type == fly_animation_timer:
                fly_index = 0 if fly_index == 1 else 1
            fly_surface = fly_frames[fly_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # spacebar
                #snail_rectangle.right = 900 # snail goes 
                start_time = pygame.time.get_ticks()//1000 # time starts from 0 again.
                game_active = True # game starts again

        # if event.type == pygame.MOUSEMOTION: 
        #   mouse_position = event.pos #alternate way to get mouse position
        
        # if event.type == pygame.MOUSEBUTTONUP: #released
        #     print('released mouse button')
        # elif event.type == pygame.MOUSEBUTTONDOWN:#pushed
        #     print("pressed mouse button")
    
    if game_active:   
        #displaying images
        #screen.blit(test_surface,(0,0))
        #screen.blit(red,(200,100))
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        #screen.blit(score_surface,score_rectangle) # its background was covering it.
        
        # score
        score = display_score()

        # Obstacle movement
        obstacle_rectangle_list = obstacle_movement(obstacle_rectangle_list)

        #animations
        player_animation()
        # screen.blit(snail_surface,snail_rectangle)
        # snail_rectangle.right -= 5
        # if snail_rectangle.right < -50:
        #     snail_rectangle.right = 900
        #print(snail_rectangle.right)
        #snail_x_pos -= 10 #speed
        #snail_y_pos -= 10
        #if snail_x_pos < -50: #if outside of screen, return
        #    snail_x_pos = 800 #original position

        #rectangles
        screen.blit(player_surface,player_rectangle) # rectangle used for positioning instead of tuple which is always topleft
        # rectangle also used for moving player
        # player_rectangle.left += 10 # rectangle moving which also moves the player (surface)
        # print(player_rectangle.left)
        # if player_rectangle.x > 850:
        #     player_rectangle.x = -10
        # if player_rectangle.y > 400:
        #     player_rectangle.y = 0
        # print(player_rectangle.x,player_rectangle.y)
        
        #collision detection
        #rectanges help in collision detection
        # if player_rectangle.colliderect(snail_rectangle):
            # print('snail collision!')

        mouse_position = pygame.mouse.get_pos() #tuple returning x,y
        if player_rectangle.collidepoint(mouse_position): #mouse position from event loop
            print('player collision!')
        #another way of collision detection is rec1.collidepoint((x,y))
        # if player_rectangle.collidepoint(mouse_position): #if mouse touching player surface (rectangle)
            # print('collision!')
            # print(pygame.mouse.get_pressed()) #tuple of mouse button pressed or no?

        #drawing with rectangles (+colors)
        pygame.draw.rect(screen,'#c0e8ec',title_rectangle) # blue color
        screen.blit(title_surface,title_rectangle) # text in middle using rect

        # pygame.draw.line(screen,'Pink',(0,0),(800,400),10) # straight diag line slope = -1
        # pygame.draw.line(screen,'Pink',(0,400),(800,0),10) # straight diag line slope =  1

        # pygame.draw.line(screen,'Pink',(0,0),mouse_position,5) # moving lines acc to mouse
        # pygame.draw.line(screen,'Pink',(800,0),mouse_position,5) 
        # pygame.draw.line(screen,'Pink',(0,400),mouse_position,5) 
        # pygame.draw.line(screen,'Pink',(800,400),mouse_position,5) 

        # pygame.draw.ellipse(screen,'Pink',pygame.Rect(50,200,100,100)) # circle

        #player character

        # keyboard input
        # keys = pygame.key.get_pressed() # all inputs 1 or 0.
        # space_bar = keys[pygame.K_SPACE]
        # if space_bar:
        #     print('jump!')

        # gravity
        player_gravity += 1 # technically exp but not really
        player_rectangle.y += player_gravity # constanting moving player down!
        # floor
        if player_rectangle.bottom >= 300: # fake floor but works!
            player_rectangle.bottom = 300

        # different game states (1:48:33)
        # if snail_rectangle.colliderect(player_rectangle): # die
        #     game_active = False
        # Collisions final
        game_active = collisions(player_rectangle,obstacle_rectangle_list)
    else:
        # intro // game over state
        screen.fill((94,129,162)) # blue background
        screen.blit(player_stand_surface,player_stand_rectangle) # could rotate using angle. lol
        screen.blit(name_surface,name_rectangle)
        if score != 0:
            score_surface = test_font.render(f'Score : {score}',False,(64,64,64))
            score_rectangle = score_surface.get_rect(center = (400,310))
            screen.blit(score_surface,score_rectangle)
        screen.blit(instruction_surface,instruction_rectangle)

        obstacle_rectangle_list.clear() # all enemies deleted... cause game over

        player_rectangle.midbottom = (80,300)
        player_gravity = 0 

    pygame.display.update() #updates screen every frame
    clock.tick(60) #60fps