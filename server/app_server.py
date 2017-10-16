from logic import *
from game_obj import *
from server import *
import time
import pygame
from pygame.locals import *


class System:
    def __init__(self):
        self.screen_length = 640
        self.screen_height = 480
        self.surface = pygame.display.set_mode((self.screen_length, self.screen_height), DOUBLEBUF, 32)
        self.clock = pygame.time.Clock()
        self.sur_rec_s = []
        self.down_pos_s = [0, 0, 0, 0, 0, 0, 0]
        
    def run(self):
        self.server = Server("", 51234)
        self.server.set_recfunc(self.recfunc)
        self.server.start()
        while True:
            for event in pygame.event.get():
                self.deal(event)
            
            pygame.display.flip()
            time_passed = self.clock.tick(30)

            self.surface.fill((0, 0, 0))

            self.draw()

    def recfunc(self, server, command, source):
        if (command.title == "hit"):
            self.sur_rec_s.pop(command.data)
        self.send()
    
    def getlist(self):
        l = []
        for sur_rec in self.sur_rec_s:
            l.append(sur_rec.rec)
        return l
        
            
    def deal(self, event):
        if (event.type == MOUSEBUTTONDOWN):
            self.down_pos_s[event.button] = Point.convert(event.pos)
        if (event.type == MOUSEBUTTONUP):
            if event.button == 1:
                sur_rec = Sur_rec(Rectangle(self.down_pos_s[event.button], Point.convert(event.pos)), self, self)
                sur_rec.set_color((100, 255, 255))
                self.sur_rec_s.append(sur_rec)
                self.send()
                

    def draw(self):
        for sur_rec in self.sur_rec_s:
            sur_rec.draw()
                    
    def send(self):
        self.server.sendall(Command("list", self.getlist()))

def main():
    pygame.init()
    a = System()

    a.run()


main()
        
