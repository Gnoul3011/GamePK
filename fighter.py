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