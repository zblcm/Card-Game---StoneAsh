from const import *
from event import *


        

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.name = "调和者布兰卡"
    self.description = "你花费红色费用时, 你的所有手牌减少1点蓝色费用。你花费蓝色费用时, 你的所有手牌减少一点红色费用。"


    def oncostmana(self, old_event):
        #print("file:幻影狼 ,card:%s ,buff:%s ,function:onmove" % (buff.card.name, buff.name))
        # 自己离场
        if (self.card.player != old_event.param[0]) or (self.card.place != PLACE_FIELD):
            return False

        oldcost = old_event.param[1]
        redcost = oldcost[1]
        bluecost = oldcost[2]

        if (redcost == 0) and (bluecost == 0):
            return False

        bluegroup = []
        if (redcost > 0):
            for card in self.system.cards:
                if (card.cost[2] > 0) and (card.player == self.card.player) and (card.place == PLACE_HAND):
                    bluegroup.append(card)
        
        redgroup = []
        if (bluecost > 0):
            for card in self.system.cards:
                if (card.cost[1] > 0) and (card.player == self.card.player) and (card.place == PLACE_HAND):
                    redgroup.append(card)

        if (len(redgroup) == 0) and (len(bluegroup) == 0):
            return False

        effectgroup = redgroup.copy()
        for card in bluegroup:
            if not (card in effectgroup):
                effectgroup.append(card)

        self.system.yell(self.card, 0, True)
        sublists = ["tinystar"]
        for card in effectgroup:
            self.system.playeffect("whiteball", sublists, None, card)
        self.system.yell(self.card)

        for card in redgroup:
            buff = Buff(self.system, "b0000000029_001", self.card, card)
            card.add_buff(buff)
        
        for card in bluegroup:
            buff = Buff(self.system, "b0000000029_002", self.card, card)
            card.add_buff(buff)
        
        return True
        
    self.oncostmana = oncostmana
