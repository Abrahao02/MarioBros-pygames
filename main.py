from typing import Any
import pygame
import random
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        player_move0 = pygame.image.load('graphics/mario/mario_move0.png').convert_alpha()
        player_move1 = pygame.image.load('graphics/mario/mario_move1.png').convert_alpha()
        self.player_move = [player_move0,player_move1]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/mario/mario_jump.png').convert_alpha()
        
        self.image = self.player_move[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100,300))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('sound/jump-sound-effect.mp3')
        self.jump_sound.set_volume(0.1)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -15
            self.jump_sound.play()
            
    def apply_gravity(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_move):self.player_index = 0
            self.image = self.player_move[int(self.player_index)]
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'koopa':
            koopa_0 = pygame.image.load('graphics/koopa_0.png').convert_alpha()
            koopa_1 = pygame.image.load('graphics/koopa_1.png').convert_alpha()
            self.frames = [koopa_0,koopa_1]
            y_pos = 301
        else:    
            goomba_0 = pygame.image.load('graphics/goombas_0.png').convert_alpha()
            goomba_1 = pygame.image.load('graphics/goombas_1.png').convert_alpha()
            self.frames = [goomba_0,goomba_1]
            y_pos = 300
            
        self.animation_index = 0    
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1100),y_pos))
        
    def animation_state(self):
        self.animation_index += 0.1    
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
               
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 3
            
            if obstacle_rect.bottom == 300: screen.blit(goomba_surf,obstacle_rect)
            else:
                screen.blit(koopa_surf,obstacle_rect)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
            
        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def collisions_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True
        

def player_animation():
    global player_surf, player_index
    
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_move):player_index = 0
        player_surf = player_move[int(player_index)]
        # andar
    # animcao do mario
    # animao de pular do mario
    
                 
# Inicialização do Pygame
pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('RunAndWin')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',30)
game_active = False
start_time = 0
score = 0
bg_Music = pygame.mixer.Sound('sound/Super Mario Bros. medley.mp3')
bg_Music.play(loops = -1)


# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()


# goomba
goomba_frame_0 = pygame.image.load('graphics/goombas_0.png').convert_alpha()
goomba_frame_1 = pygame.image.load('graphics/goombas_1.png').convert_alpha()
goomba_frames = [goomba_frame_0,goomba_frame_1]
goomba_frames_index = 0
goomba_surf = goomba_frames[goomba_frames_index]

# koopa
koopa_frame_0 = pygame.image.load('graphics/koopa_0.png').convert_alpha()
koopa_frame_1 = pygame.image.load('graphics/koopa_1.png').convert_alpha()
koopa_frame = [koopa_frame_0, koopa_frame_1]
koopa_frame_index = 0
koopa_surf = koopa_frame[koopa_frame_index]

obstacle_rect_list = []

player_move0 = pygame.image.load('graphics/mario/mario_move0.png').convert_alpha()
player_move1 = pygame.image.load('graphics/mario/mario_move1.png').convert_alpha()
player_move = [player_move0,player_move1]
player_index = 0
player_jump = pygame.image.load('graphics/mario/mario_jump.png').convert_alpha()

player_surf = player_move[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load('graphics/mario/mario1.png').convert_alpha()
player_stand= pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Mario Bros' ,False,'White')
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,'White')
game_message_rect = game_message.get_rect(center = (400,300))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

goomba_animation_time = pygame.USEREVENT + 2
pygame.time.set_timer(goomba_animation_time,500)

koopa_animation_time = pygame.USEREVENT + 3
pygame.time.set_timer(koopa_animation_time,499)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active:    
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: 
                    player_gravity = -15
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -15
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                
        if game_active:
            if event.type == obstacle_timer: 
                obstacle_group.add(Obstacle(choice(['koopa','goomba', 'goomba', 'goomba'])))
                      
            if event.type == goomba_animation_time:
                if goomba_frames_index == 0: goomba_frames_index = 1
                else: goomba_frames_index = 0
                goomba_surf = goomba_frames[goomba_frames_index]   
                
            if event.type == koopa_animation_time:
                if koopa_frame_index == 0: koopa_frame_index = 1
                else: koopa_frame_index = 0
                koopa_surf = koopa_frame[koopa_frame_index]      
                    
    if game_active:
        screen.blit(sky_surface,(0,0))    
        screen.blit(ground_surface,(0,300)) 
        #se quiser um quadrado no fundo das letras
        # pygame.draw.rect(screen, '#C0E8EC', score_rect,) 
        # pygame.draw.rect(screen, '#C0E8EC', score_rect,10)    
        # screen.blit(score_surf,score_rect) 
        score = display_score()

        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        game_active = collisions_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        
        score_message = test_font.render(f'Your score: {score}',False,'White')
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)
        
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
        

    pygame.display.update()
    clock.tick(60)