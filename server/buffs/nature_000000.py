from const import *
from event import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.visable = True
    self.original = False
    self.name = "召唤失调"
    self.description = "在本回合不能攻击。"
    self.image = "nature_sleep"
    self.imageinside = False
    self.flag_cannotattack = True
    
    def onturnstop(self, old_event):
        self.card.remove_buff(self)
    self.onturnstop = onturnstop

    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (old_event.param[1] != PLACE_FIELD):
            self.card.remove_buff(self)
            return False
    self.after_move = after_move
