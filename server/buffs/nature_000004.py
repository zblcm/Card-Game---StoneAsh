from const import *
from event import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = False
    self.visable = True
    self.name = "风怒"
    self.description = "可以多进行一次攻击。"
    
    def oncreate(self, event = None):
        self.card.maxattacktime = self.card.maxattacktime + 1
    self.oncreate = oncreate

    def onremove(self, event = None):
        self.card.maxattacktime = self.card.maxattacktime - 1
    self.onremove = onremove

    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (old_event.param[1] != PLACE_FIELD):
            self.card.remove_buff(self)
            return False
    self.after_move = after_move
