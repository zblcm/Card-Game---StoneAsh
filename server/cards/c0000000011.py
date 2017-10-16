from const import *
from buff import *

def init(self, mode = True):
    self.name = "反召唤"
    self.description = "使一个生物返回手牌。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 0, 1, 0, 0, 0] #White Fire Water Tree Light Death

    def unusable(self):
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (not card.unselectable(card, self.player)):
                return False
        return True
    self.unusable = unusable
    
    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        
        buff = Buff(self.system, "b0000000011_000", self, self)
        self.add_buff(buff)

