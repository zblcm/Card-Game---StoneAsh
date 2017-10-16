from const import *
from event import *
from card import *


def init(self, mode = True):
    self.name = "怒火爆发"
    self.description = "目标生物失去召唤失调及冻结, 在回合结束前攻击力+3。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 2, 0, 0, 0, 0] #White Fire Water Tree Light Death
    
    def unusable(self):
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (not card.unselectable(card, self.player)):
                return False
        return True
    self.unusable = unusable
    
    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        
        buff = Buff(self.system, "b0000000016_000", self, self)
        self.add_buff(buff)
        



    
