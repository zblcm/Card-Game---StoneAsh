import pygame
from pygame.locals import *

class Imageloader:
    def __init__(self, system):
        self.system = system
        self.loadcache = {}
        self.resizedcache = {}

    def load(self, name, alpha = True):
        if name in self.loadcache:
            return self.loadcache[name].copy()
        else:
            if alpha:
                image = pygame.image.load(name).convert_alpha()
                """
                width, height = image.get_size()
                surface = pygame.Surface((width, height))
                surface.blit(image, (0, 0))
                image = surface
                """
            else:
                image = pygame.image.load(name).convert()
            self.loadcache[name] = image
            return image.copy()

    def resize(self, name, alpha = True):
        if name in self.resizedcache:
            return self.resizedcache[name].copy()
        else:
            image_o = self.load(name, alpha)
            width_o, height_o = image_o.get_size()
            unit = self.system.screen_height * 0.2 / 220
            width_f = width_o * unit
            height_f = height_o * unit
            image_f = pygame.transform.smoothscale(image_o, (int(width_f), int(height_f)))
            self.resizedcache[name] = image_f
            return image_f.copy()
            
    def onresize(self):
        self.resizedcache = {}
