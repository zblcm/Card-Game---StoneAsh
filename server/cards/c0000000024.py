from const import *
from buff import *

def init(self, mode = True):
    self.name = "伊瓦尔之书"
    self.description = "随机召唤一个法师。"
    self.original = False
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BOOK]
    self.originalcost = [0, 0, 2, 0, 0, 0] #White Fire Water Tree Light Death
    
    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        
        buff = Buff(self.system, "b0000000024_000", self, self)
        self.add_buff(buff)
        


    
