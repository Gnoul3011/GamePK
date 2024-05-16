import random
import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
class Player():
    def __init__(self, x, y, width, height, color, player, flip, data, sprite_sheet, animation_steps, sound):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3
        self.player= player
        self.data= data
        self.sprite_sheet= sprite_sheet
        self.animation_steps= animation_steps
        self.sound= sound
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.mana = 0
        self.max_mana = 100
        self.alive = True
        
    def load_images(self, sprite_sheet, animation_steps):
        #extract images from spritessheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
    
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False) #player1 quay mat qua trai
        # pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.x - (self.offset[0] * self.image_scale), self.y - (self.offset[1] * self.image_scale)))
    
    def move(self, screen_width, screen_height, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed()
        if self.attacking == False and self.alive == True and round_over == False:
            if key[pygame.K_LEFT]:
                dx = -SPEED
                self.running = True
            if key[pygame.K_RIGHT]:
                dx = SPEED
                self.running = True    
            if key[pygame.K_KP1] or key[pygame.K_KP2]:
                self.attack(target)
                if key[pygame.K_KP1]:
                    self.attack_type = 1
                if key[pygame.K_KP2]:
                    self.attack_type = 2
                    
        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom
        if self.rect.top + dy < 0:
            dy = 0

        self.x += dx
        self.y += dy

    def attack(self, target):
        random_health = random.randint(10, 30)
        self.attacking = True
        self.attack_sound.play()
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
            self.mana += 20
            if self.mana == 100:
                self.health += random_health
                self.mana = 0
            target.hit = True

       
                
    def update(self):
        #check what action the player is performing
        if self.mana >=100:
            self.mana = 100
        if self.health >= 100:
            self.health = 100
        if self.health <=0:
            self.health = 0
            self.alive = False
            self.update_action(6) #6: chet
        elif self.hit == True:
            self.update_action(5) #5: bi danh
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3) #3: tan cong 1
            elif self.attack_type ==2:
                self.update_action(4) #4: tan cong 2
        elif self.running == True:
            self.update_action(1) #1: chay
        else:
            self.update_action(0) #0: dung im
            
        animation_cooldown = 50
        #update image
        self.image = self.animation_list[self.action][self.frame_index] 
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #if the player is dead then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #check if an attack was executed
                if self.action == 3 or self.action ==4:
                    self.attacking = False
                    self.attack_cooldown = 20 #thoi gian ra chieu
                #check if damage was taken
                if self.action == 5:
                    self.hit = False
                    #if the player was in the middle of an attack, then the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 20
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, False, False) #player1 quay mặt qua trái
        surface.blit(img, (self.x - (self.offset[0] * self.image_scale), self.y - (self.offset[1] * self.image_scale)))
      

    
    def draw_health_bar(self, surface,x,y):
        health_bar_length = 100
        health_bar_height = 10
        fill = (self.health / 100) * health_bar_length
        ratio = self.health / 100
        pygame.draw.rect(surface, WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(surface, RED, (x, y, 400, 30))
        pygame.draw.rect(surface, GREEN, (x, y, 400 * ratio, 30))
    
    def draw_mana_bar(self,surface, x, y):
        ratio = self.mana / 100
        pygame.draw.rect(surface, WHITE, (x - 2, y - 2, 204, 8))
        pygame.draw.rect(surface, BLUE, (x, y, 200 * ratio, 5))