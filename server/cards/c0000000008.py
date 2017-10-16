from const import *
from buff import *


def init(self, mode = True):
    self.name = "燎原火"
    self.description = "对对方所有生物造成1点伤害。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 2, 0, 0, 0, 0] #White Fire Water Tree Light Death


    def unusable(self):
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (card.player != self.player):
                return False
        return True
    self.unusable = unusable

    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        
        buff = Buff(self.system, "b0000000008_000", self, self)
        self.add_buff(buff)
        
