from const import *
from event import *




def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "幻影狼"
    self.description = "上场时添加野兽之力效果。"
    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (self.card.place == PLACE_FIELD):
            buff = Buff(self.system, "b0000000004_001", self.card, self.card)
            self.card.add_buff(buff)
            return False
    self.after_move = after_move
