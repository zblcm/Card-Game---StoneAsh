from const import *
from event import *



def init(self):
    self.typ = BUFF_STATIC
    self.visable = True
    self.original = False
    self.name = "狼光环效果"
    self.description = "+1攻击力。"
    def oncreate(self, event = None):
        self.card.attack = self.card.attack + 1
    self.oncreate = oncreate
    

    def onremove(self, event = None):
        self.card.attack = self.card.attack - 1
        if self.card.attack < 0:
            self.card.attack = 0
    self.onremove = onremove
