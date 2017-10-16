from const import *
from buff import *

def init(self, mode = True):
    self.name = "定向爆破"
    self.description = "对对方玩家造成5点魔法伤害。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 2, 0, 0, 0, 0] #White Fire Water Tree Light Death
    
    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        
        buff = Buff(self.system, "b0000000033_000", self, self)
        self.add_buff(buff)

