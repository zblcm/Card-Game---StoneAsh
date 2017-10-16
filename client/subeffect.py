import pygame
from pygame.locals import *
from system import *
import math

class Subeffect:
    def __init__(self, system, father, filename, angle, dis = None, time = None):
        self.system = system
        self.father = father
        surface_o = self.system.imageloader.resize("images/effects/%s.png" % filename)

        # 重设角度
        if (angle % 360 > 90) and (angle % 360 < 270):
            surface_p = pygame.transform.flip(surface_o, True, False)
            counter = -1
        else:
            surface_p = surface_o
            counter = 1
        self.surface = pygame.transform.rotate(surface_p, (angle * counter))
        self.angle = angle / 180 * math.pi

        # 计算速度
        if not dis:
            dis = self.system.screen_height * 0.2
        if not time:
            time = 0.5
        self.speed = dis / time * 2
        self.deceleration = self.speed / time

        # 计算始末位置
        length_s, height_s = self.surface.get_size()
        length_f, height_f = self.father.surface.get_size()
        fx, fy = self.father.x, self.father.y
        cx, cy = fx + (length_f / 2), fy + (height_f / 2)
        self.x, self.y = cx - (length_s / 2), cy - (height_s / 2)
        
        self.father.subeffects.append(self)

    # Draw level 0 - Draw
    def update(self, time):
        self.speed = self.speed - (self.deceleration * time / 1000)

        if (self.speed <= 0):
            self.end()
        else:
            self.x = self.x + (self.speed * time / 1000) * math.cos(self.angle)
            self.y = self.y + (self.speed * time / 1000) * math.sin(self.angle)

    def draw(self):
        self.system.screen.blit(self.surface, (int(self.x), int(self.y)))

    def end(self):
        self.father.subeffects.remove(self)
                
