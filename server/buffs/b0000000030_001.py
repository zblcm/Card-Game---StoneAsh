from const import *
from event import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.visable = True
    self.original = False
    self.name = "炎之剑盾"
    self.description = "+4攻击力, 不受物理伤害。"
    
    def oncreate(self, old_event = None):
        self.card.attack = self.card.attack + 4
    self.oncreate = oncreate

    def onremove(self, old_event = None):
        self.card.attack = self.card.attack - 4
        if self.card.attack < 0:
            self.card.attack = 0
    self.onremove = onremove
    
    def onturnstop(self, old_event):
        self.card.remove_buff(self)
    self.onturnstop = onturnstop
    
    def before_damage(self, old_event):
        if not (self.card in old_event.param[0]):
            return True
        if not (old_event.param[3] == DAMAGE_PHYSICAL):
            return True
        index = old_event.param[0].index(self.card)
        old_event.param[4][index] = False
        return True
    self.before_damage = before_damage

    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (old_event.param[1] != PLACE_FIELD):
            self.card.remove_buff(self)
            return False
    self.after_move = after_move
