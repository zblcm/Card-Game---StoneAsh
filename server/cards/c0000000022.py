from const import *
from buff import *

def init(self, mode = True):
    self.name = "寒冰箭"
    self.description = "冻结目标生物并造成3点魔法伤害。如果目标生物已被冻结则将其消灭。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 0, 2, 0, 0, 0] #White Fire Water Tree Light Death
    
    def unusable(self):
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (not card.unselectable(card, self.player)):
                return False
        return True
    self.unusable = unusable
        
    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        
        buff = Buff(self.system, "b0000000022_000", self, self)
        self.add_buff(buff)
        


    
