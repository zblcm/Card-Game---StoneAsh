from const import *
from event import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.visable = True
    self.original = False
    self.name = "精神强化"
    self.description = "+1攻击力和生命值。"
    
    def oncreate(self, old_event = None):
        self.card.attack = self.card.attack + 1
        self.card.maxhealth = self.card.maxhealth + 1
        self.card.health = self.card.health + 1
    self.oncreate = oncreate

    def onremove(self, old_event = None):
        self.card.attack = self.card.attack - 1
        self.card.maxhealth = self.card.maxhealth - 1
        if self.card.attack < 0:
            self.card.attack = 0
        if self.card.maxhealth < 0:
            self.card.maxhealth = 0
        if self.card.health > self.card.maxhealth:
            self.card.health = self.card.maxhealth
    self.onremove = onremove

    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (old_event.param[1] != PLACE_FIELD):
            self.card.remove_buff(self)
            return False
    self.after_move = after_move
