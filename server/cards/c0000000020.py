from const import *
from buff import *

def init(self, mode = True):
    self.name = "寒流"
    self.description = "冻结对方所有未被冻结的生物。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 0, 3, 0, 0, 0] #White Fire Water Tree Light Death
    
    def unusable(self):
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (card.player != self.player):
                freezed = False
                for buff in card.buffs:
                    if buff.filename == "nature_000003":
                        freezed = True
                if not freezed:
                    return False
        return True
    self.unusable = unusable
        
    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        
        buff = Buff(self.system, "b0000000020_000", self, self)
        self.add_buff(buff)
        


    
