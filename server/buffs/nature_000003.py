from const import *
from event import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.visable = True
    self.original = False
    self.name = "冻结"
    self.description = "在下个自己的回合结束前不能攻击。"
    self.image = "nature_freeze"
    self.imageinside = True
    self.flag_cannotattack = True

    self.turnleft = 1
    
    def onturnstop(self, old_event):
        if self.card.player == old_event.param[0]:
            if self.turnleft > 0:
                self.turnleft = self.turnleft - 1
            if self.turnleft == 0:
                self.card.remove_buff(self)
    self.onturnstop = onturnstop

    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (old_event.param[1] != PLACE_FIELD):
            self.card.remove_buff(self)
            return False
    self.after_move = after_move
