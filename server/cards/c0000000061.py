from const import *
from buff import *

def init(self, mode = True):
    self.name = "魔法拳"
    self.description = "造成4点物理伤害。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 0, 4, 0, 0, 0] #White Fire Water Tree Light Death
    
    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        
        buff = Buff(self.system, "b0000000061_000", self, self)
        self.add_buff(buff)

