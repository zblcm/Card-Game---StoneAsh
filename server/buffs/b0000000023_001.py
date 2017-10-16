from const import *
from event import *



def init(self):
    self.typ = BUFF_STATIC
    self.visable = True
    self.original = False
    self.name = "降费"
    self.description = "随机降低一点一种颜色的费用。"
    def oncreate(self, event = None):

        reduce = 1
        
        costsum = 0
        for colorindex in range(6):
            costsum = costsum + self.card.cost[colorindex]
        if costsum < reduce:
            reduce = costsum
        if reduce == 0:
            self.reducelist = [0, 0, 0, 0, 0, 0]
            self.card.remove_buff(self)
            return False

        randlist = []
        for i in range(costsum):
            randlist.append(i)
        outlist = []
        
        import random
        while reduce > 0:
            index = random.randint(1, len(randlist)) - 1
            number = randlist[index]
            randlist.remove(number)
            outlist.append(number)
            reduce = reduce - 1
        
        reducelist = [0, 0, 0, 0, 0, 0]
        for colorindex in range(6):
            for costindex in range(self.card.cost[colorindex]):
                costsum = costsum - 1
                if costsum in outlist:
                    reducelist[colorindex] = reducelist[colorindex] + 1
        
        for colorindex in range(6):
            self.card.cost[colorindex] = self.card.cost[colorindex] - reducelist[colorindex]

        self.reducelist = reducelist
            
    self.oncreate = oncreate
    

    def onremove(self, event = None):
        for colorindex in range(6):
            self.card.cost[colorindex] = self.card.cost[colorindex] + self.reducelist[colorindex] 
    self.onremove = onremove

    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (old_event.param[1] != PLACE_HAND):
            self.card.remove_buff(self)
            return False
    self.after_move = after_move
        
