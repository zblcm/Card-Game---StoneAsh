from const import *
from event import *
from card import *

def init(self, mode = True):
    self.name = "精神强化"
    self.description = "召唤2个1/1的小精灵, 并使你的全部小精灵获得+1/+1。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 0, 0, 5, 0, 0] #White Fire Water Tree Light Death

    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        buff = Buff(self.system, "b0000000049_000", self, self)
        self.add_buff(buff)



    
