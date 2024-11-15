import pygame
from random import randint, choice

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner by ade")
clock = pygame.time.Clock()
font = pygame.font.Font("font/Pixeltype.ttf", 50)

bg_music =pygame.mixer.Sound("audio/music.wav")
bg_music.set_volume(0.1)
bg_music.play(loops=-1)

sky_surface= pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = font.render("Pixel Runner", False, (110, 200, 170))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = font.render("Press space to start!", False, (110, 200, 170))
game_message_rect = game_message.get_rect(center=(400, 330))






score=0

bg_x = 0
bg_x_slow = 0

#rgb
red = (255, 0, 0)

#classes are like blueprints
class Player(pygame.sprite.Sprite):
    def __init__(self): # method is a function insside of a class
        super().__init__()   
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]    
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png")
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound("audio/jump.wav")
        self.jump_sound.set_volume(0.2)
        
    def player_input(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300 
            
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly":
            fly_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
            
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
            #the image thats gonna show for the paricular image
        self.rect = self.image.get_rect(midbottom=(randint(900,1100),  y_pos))
        
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):  
            self.animation_index= 0
        self.image = self.frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        if self.rect.right < 0:
            self.kill()    
        #destroy is used to get rid of the character when its off the screen
 
def display_score():
    current_time = int(pygame.time.get_ticks()/ 1000) - start_time
    score_surf = font.render(f"Score:  {current_time}", False, (64, 64, 64))    
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


obstacle_timer = pygame.USEREVENT
pygame.time.set_timer(obstacle_timer, 1500) 



obstacle_group = pygame.sprite.Group()

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True                 

player = pygame.sprite.GroupSingle()
player.add(Player())   

game_active = False
   #checking if the game is active 
while True:
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == obstacle_timer and game_active:
            obstacle_group.add(Obstacle(choice(["fly", "snail", "snail"])))
          
        if game_active == False and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  
            game_active = True
            start_time= int(pygame.time.get_ticks()/ 1000)
    
    
    if game_active:
        #draw backgroundn
        screen.blit(sky_surface,(bg_x_slow,0))
        screen.blit(sky_surface,(bg_x_slow + sky_surface.get_width(),0))
        
        screen.blit(ground_surface,(bg_x,300))
        screen.blit(ground_surface,(bg_x + ground_surface.get_width(),300))
        
        bg_x -= 5
        bg_x_slow -= 1
        #reset background after scrolling
        if bg_x <= -ground_surface.get_width():
            bg_x = 0
        if bg_x_slow <= -ground_surface.get_width():
            bg_x_slow = 0
        
        score = display_score()
        
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)                    
        obstacle_group.update()
        
        game_active = collision_sprite()
    else:#draw title screen
        screen.fill((100, 137, 170))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        score_message = font.render(f"Your score: {score}", False, (110, 200, 170) )
        score_message_rect = score_message.get_rect(center=(400, 330))
        
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
            
        
        
    
    pygame.display.update()
    clock.tick(60)    