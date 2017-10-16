from const import *
from event import *



def init(self):
    self.typ = BUFF_STATIC
    self.visable = True
    self.original = False
    self.name = "降费"
    self.description = "降低一点红色费用。"
    def oncreate(self, event = None):
        if self.card.cost[1] == 0:
            self.reduced = 0
            self.card.remove_buff(self)
        self.reduced = 1
        self.card.cost[1] = self.card.cost[1] - self.reduced
            
    self.oncreate = oncreate
    

    def onremove(self, event = None):
        self.card.cost[1] = self.card.cost[1] + self.reduced
    self.onremove = onremove

    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (old_event.param[1] != PLACE_HAND):
            self.card.remove_buff(self)
            return False
    self.after_move = after_move
        
