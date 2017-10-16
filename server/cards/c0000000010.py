from const import *
from buff import *

def init(self, mode = True):
    self.name = "火焰飞斩"
    self.description = "对一个生物造成2点伤害, 并对其控制者造成2点伤害。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 1, 0, 0, 0, 0] #White Fire Water Tree Light Death
    
    def unusable(self):
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (not card.unselectable(card, self.player)):
                return False
        return True
    self.unusable = unusable
    
    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        
        buff = Buff(self.system, "b0000000010_000", self, self)
        self.add_buff(buff)

