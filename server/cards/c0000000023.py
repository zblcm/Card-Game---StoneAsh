from const import *
from buff import *

def init(self, mode = True):
    self.name = "莱克斯之书"
    self.description = "你手牌中的法术牌减少1点法力消耗。"
    self.original = False
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BOOK]
    self.originalcost = [0, 0, 2, 0, 0, 0] #White Fire Water Tree Light Death
    
    def unusable(self):
        number = 0
        for card in self.system.cards:
            if (card.place == PLACE_HAND) and (card.player == self.player) and (card.typ == CARD_SPELL) and (card != self):
                return False
        return True
    self.unusable = unusable
        
    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        
        buff = Buff(self.system, "b0000000023_000", self, self)
        self.add_buff(buff)
        


    
