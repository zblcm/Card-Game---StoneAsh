from const import *
from event import *
from card import *

def init(self, mode = True):
    self.name = "精神爆发"
    self.description = "召唤2个1/1的小精灵, 并使你的全部小精灵具有冲锋。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 0, 0, 4, 0, 0] #White Fire Water Tree Light Death

    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        buff = Buff(self.system, "b0000000042_000", self, self)
        self.add_buff(buff)



    
