from const import *
from buff import *

def init(self, mode = True):
    self.name = "烈焰小鬼"
    self.description = "战吼: 造成1点魔法伤害。"
    self.typ = CARD_CREATURE
    self.subtype = [SUBTYPE_DEVIL]
    self.originalcost = [0, 1, 0, 0, 0, 0] #White Fire Water Tree Light Death    self.orimaxhealth = 1
    self.orimaxhealth = 1
    self.oriattack = 1
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
        buff = Buff(self.system, "b0000000000_000", self, self)
        self.add_buff(buff)

    
