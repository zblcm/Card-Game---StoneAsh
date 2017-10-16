from const import *
from event import *
from card import *

def init(self, mode = True):
    self.name = "精神涌动"
    self.description = "召唤4个1/1的小精灵, 并使你的全部小精灵获得风怒。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 0, 0, 7, 0, 0] #White Fire Water Tree Light Death

    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        buff = Buff(self.system, "b0000000050_000", self, self)
        self.add_buff(buff)



    
