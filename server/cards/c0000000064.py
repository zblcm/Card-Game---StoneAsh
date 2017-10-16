from const import *
from event import *
from card import *

def init(self, mode = True):
    self.name = "奥术典籍"
    self.description = "抽三张牌。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 0, 5, 0, 0, 0] #White Fire Water Tree Light Death
    
    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        buff = Buff(self.system, "b0000000064_000", self, self)
        self.add_buff(buff)



    
