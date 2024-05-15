import pygame
import random

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.reset(player, x, y, flip, data, sprite_sheet, animation_steps, sound)
        
    def load_images(self, sprite_sheet, animation_steps):
        #extract images from spritessheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale))
)
            animation_list.append(temp_img_list)
        return animation_list
    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        
        #get keypresses
        key = pygame.key.get_pressed()
        
        #can only perform other actions if not currently attacking
        if self.attacking == False and self.alive == True and round_over == False:
            #check player 1 controls
            if self.player == 1:
                #movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                #jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                    
                #attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    #determine which attack type was used
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2
                        
            #check player 2 controls
            if self.player == 2:
                #movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                #jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                    
                #attack
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    #determine which attack type was used
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2
          
        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y
            
        #ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom
            
        #ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
            
        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        #update player position
        self.rect.x += dx
        self.rect.y += dy
        
    #handle animation updates