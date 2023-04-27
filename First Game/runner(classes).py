import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3') # a bit loud tho
        self.jump_sound.set_volume(0.1) # 0->1
        
    def player_input(self):
        keys = pygame.key.get_pressed() # class now so no event loop input
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300: # pressing space
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1 # imitating gravity
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: 
            self.rect.bottom = 300 # fake floor

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self): # update all methods
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/fly2.png').convert_alpha()
            self.frames = [fly_2,fly_1]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_2,snail_1]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
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
#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)
# BackGround
sky_surface = pygame.image.load('graphics/Sky.png').convert() #imageregularsurface
ground_surface = pygame.image.load('graphics/ground.png').convert()
title_surface = test_font.render('Look at em go!!!',False,(64,64,64)) #textregularsurface (prompt,AA,color) 
title_rectangle = title_surface.get_rect(center = (400,100)) #topleft , midbottom , center
# Intro // Gameover
player_stand_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface,0,2) # scaling to make it better
player_stand_rectangle = player_stand_surface.get_rect(center = (400,200)) # middle
name_surface = test_font.render('Running Game',False,(111,196,169))
name_rectangle = name_surface.get_rect(center = (400,80))
instruction_surface = test_font.render('Press Space to Start',False,(64,64,64))
instruction_rectangle = instruction_surface.get_rect(center = (400,350))
# Music
background_music = pygame.mixer.Sound('audio/music.wav')
background_music.set_volume(0.3)
background_music.play(loops = -1) # loop forever
# Game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer: # timer
                obstacle_group.add(Obstacle(choice(['fly','fly','snail','snail']))) # 50% to get snail. 50% to get fly.
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # spacebar
                start_time = pygame.time.get_ticks()//1000 # time starts from 0 again.
                game_active = True # game starts again

    if game_active: # GameRunning State
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        player.draw(screen) # calling the whole class code
        player.update() # runs all class functions
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()
    else: # GameOver State
        screen.fill((94,129,162)) # blue background
        screen.blit(player_stand_surface,player_stand_rectangle) # could rotate using angle. lol
        screen.blit(name_surface,name_rectangle)
        if score != 0:
            score_surface = test_font.render(f'Score : {score}',False,(64,64,64))
            score_rectangle = score_surface.get_rect(center = (400,310))
            screen.blit(score_surface,score_rectangle)
        screen.blit(instruction_surface,instruction_rectangle)
    pygame.display.update() #updates screen every frame
    clock.tick(60) #60fps