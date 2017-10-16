from const import *
from event import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = False
    self.visable = True
    self.name = "嘲讽"
    self.description = "有带有嘲讽的生物时必须先攻击带有嘲讽的生物。"
    
    self.image = "nature_taught"
    self.imageinside = False
    
    self.flag_taught = True


    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (old_event.param[1] != PLACE_FIELD):
            self.card.remove_buff(self)
            return False
    self.after_move = after_move
