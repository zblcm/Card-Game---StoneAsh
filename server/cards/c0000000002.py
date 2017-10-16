from const import *
from event import *
from card import *

def init(self, mode = True):
    self.name = "兽性幻影"
    self.description = "召唤两只2/2的幻影野猪。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 0, 3, 0, 0, 0] #White Fire Water Tree Light Death

    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        buff = Buff(self.system, "b0000000002_000", self, self)
        self.add_buff(buff)



    
