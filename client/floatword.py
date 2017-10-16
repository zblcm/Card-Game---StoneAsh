import pygame
from pygame.locals import *
from system import *

class Floatword:
    def __init__(self, system, text, height, center_pos, final_rel_pos, rel_speed = 5, time = 750, color = (255, 255, 255)):
        self.system = system
        self.speed_rel = rel_speed
        self.time = time
        
        surface = self.system.font[0].render(text, True, color)
        length_o, height_o  = surface.get_size()
        self.height = height
        self.length = self.height / height_o * length_o
        self.surface = pygame.transform.smoothscale(surface, (int(self.length), int(self.height)))
        self.x = center_pos[0] - (self.length / 2)
        self.y = center_pos[1] - (self.height / 2)
        self.final_x = self.x + final_rel_pos[0]
        self.final_y = self.y + final_rel_pos[1]

        self.system.floatwords.append(self)

    # Draw level 0 - Draw
    def update(self, time):
        self.time = self.time - time
        
        # Change position
        dis = (((self.x - self.final_x) ** 2) + ((self.y - self.final_y) ** 2)) ** (0.5)
        if (dis > 0):
            speed_v = (dis * time / 1000 * self.speed_rel)
            scale = (dis - speed_v) / dis
            self.x = (self.x - self.final_x) * scale + self.final_x
            self.y = (self.y - self.final_y) * scale + self.final_y
        return True
    
    def draw(self):
        
        if self.time < 0:
            self.remove()
            return False

        self.system.screen.blit(self.surface, (int(self.x), int(self.y)))

    def remove(self):
        self.system.floatwords.remove(self)
                
