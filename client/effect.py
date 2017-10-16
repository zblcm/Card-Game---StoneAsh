import pygame
from pygame.locals import *
from system import *
from subeffect import *
import math
import random

class Effect:
    def __init__(self, system, filename, subfilenames, time, startcenter, finalcenter, hitobject = None, hitmask = None):
        self.system = system
        surface_o = self.system.imageloader.resize("images/effects/%s.png" % filename)

        self.hitobject = hitobject
        self.hitmask = hitmask
        self.subeffects = []
        self.subfilenames = subfilenames
        self.timepassed = 0
        self.hited = False

        # 计算角度
        sx, sy = startcenter[0], startcenter[1]
        ex, ey = finalcenter[0], finalcenter[1]

        sdis = (((sx - ex) ** 2) + ((sy - ey) ** 2)) ** 0.5
        if sdis == 0:
            ey = ey + 1
            sdis = (((sx - ex) ** 2) + ((sy - ey) ** 2)) ** 0.5

        asin = (ey - sy) / sdis * (-1)
        angle = math.asin(asin) / math.pi * 180
        # print(angle)
        if ex < sx:
            surface_p = pygame.transform.flip(surface_o, True, False)
            counter = -1
        else:
            surface_p = surface_o
            counter = 1
        self.surface = pygame.transform.rotate(surface_p, (angle * counter))
        self.system.effects.append(self)

        # 计算速度
        self.speed = 0
        self.acceleration = 2 * sdis / (time ** 2)

        # 计算始末位置
        length, height = self.surface.get_size()
        self.x = sx - (length / 2)
        self.y = sy - (height / 2)
        self.final_x = ex - (length / 2)
        self.final_y = ey - (height / 2)



    # Draw level 0 - Draw
    def update(self, time):
        if not self.hited:
            self.speed = self.speed + (self.acceleration * time / 1000)
            dis = (((self.x - self.final_x) ** 2) + ((self.y - self.final_y) ** 2)) ** (0.5)
            if (dis < self.speed * time / 1000):
                self.hit()
            else:
                scale = (dis - (self.speed * time / 1000)) / dis
                self.x = (self.x - self.final_x) * scale + self.final_x
                self.y = (self.y - self.final_y) * scale + self.final_y
                
            if (len(self.subfilenames) > 0):
                self.timepassed = self.timepassed + time
                while (self.timepassed > 5):
                    self.timepassed = self.timepassed - 5
                    subeffectindex = random.randint(1, len(self.subfilenames)) - 1
                    angle = random.randint(0, 360)
                    Subeffect(self.system, self, self.subfilenames[subeffectindex], angle)

        for subeffect in self.subeffects:
            subeffect.update(time)

    def draw(self):
        if not self.hited:
            self.system.screen.blit(self.surface, (int(self.x), int(self.y)))
        for subeffect in self.subeffects:
            subeffect.draw()
        if (self.hited) and (len(self.subeffects) == 0):
            self.system.effects.remove(self)

    def hit(self):
        if self.hitobject and self.hitmask:
            self.hitobject.mask = hitmask
        self.hited = True
        
                
