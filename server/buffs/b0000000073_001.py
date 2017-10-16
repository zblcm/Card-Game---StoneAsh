from const import *
from event import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.visable = True
    self.original = False
    self.name = "迷魂箭"
    self.description = "-7攻击力。"
    
    def oncreate(self, old_event = None):
        self.reduce = 7
        if self.card.attack < self.reduce:
            self.reduce = self.card.attack
        
        self.card.attack = self.card.attack - self.reduce
    self.oncreate = oncreate

    def onremove(self, old_event = None):
        self.card.attack = self.card.attack + self.reduce
        if self.card.attack < 0:
            self.card.attack = 0
    self.onremove = onremove

    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (old_event.param[1] != PLACE_FIELD):
            self.card.remove_buff(self)
            return False
    self.after_move = after_move
