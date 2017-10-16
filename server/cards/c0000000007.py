from const import *
from buff import *

def init(self, mode = True):
    self.name = "熔岩暴怒者"
    self.description = ""
    self.typ = CARD_CREATURE
    self.subtype = [SUBTYPE_DEVIL]
    self.originalcost = [0, 3, 0, 0, 0, 0] #White Fire Water Tree Light Death
    self.orimaxhealth = 1
    self.oriattack = 5
    self.maxattacktime = 1

    if mode:
        self.cost = self.originalcost.copy()
        self.maxhealth = self.orimaxhealth
        self.health = self.maxhealth
        self.attack = self.oriattack
        self.attacktime = 0
        self.needtarget = False
        buff = Buff(self.system, "nature_000000_auto", self, self)
        self.add_buff(buff)

    
