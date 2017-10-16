from const import *
from event import *



def init(self):
    self.typ = BUFF_STATIC
    self.visable = True
    self.original = False
    self.name = "改色"
    self.description = "法力消耗变为蓝色。"
    def oncreate(self, event = None):
        self.changecost = [0, 0, 0, 0, 0, 0]
        for colorindex in range(6):
            if (self.card.cost[colorindex] > 0) and (colorindex != 2):
                self.changecost[colorindex] = self.card.cost[colorindex]
                self.changecost[2] = self.changecost[2] - self.card.cost[colorindex]
        if self.changecost[2] == 0:
            self.card.remove_buff(self)
            return False
        print(self.changecost)
        for colorindex in range(6):
            self.card.cost[colorindex] = self.card.cost[colorindex] - self.changecost[colorindex]
        print(self.card.cost)
    self.oncreate = oncreate
    

    def onremove(self, event = None):
        for colorindex in range(6):
            self.card.cost[colorindex] = self.card.cost[colorindex] + self.changecost[colorindex]
    self.onremove = onremove

    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (old_event.param[1] != PLACE_HAND):
            print("Remove")
            self.card.remove_buff(self)
            return False
    self.after_move = after_move
        
