from const import *
from event import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = False
    self.visable = True
    self.name = "潜行"
    self.description = "无法被选作攻击, 技能和法术的目标。攻击时会消失。"
    
    self.image = "nature_hide"
    self.imageinside = False
    
    self.flag_cannotbetarget = True
    self.flag_cannotbeattack = True

    self.turnleft = 1
    
    def onturnstart(self, old_event):
        if self.card.player == old_event.param[0]:
            if self.turnleft > 0:
                self.turnleft = self.turnleft - 1
            if self.turnleft == 0:
                self.card.remove_buff(self)
    self.onturnstart = onturnstart

    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (old_event.param[1] != PLACE_FIELD):
            self.card.remove_buff(self)
            return False
    self.after_move = after_move
    
    def before_attack(self, old_event):
        attacker = old_event.param[0]
        if self.card != attacker:
            return True
        self.card.remove_buff(self)
        return True    
    self.before_attack = before_attack
