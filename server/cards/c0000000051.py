from const import *
from buff import *

def init(self, mode = True):
    self.name = "山峰"
    self.description = "每次最多受到1点伤害。攻击生物时对其他敌方生物造成等量物理伤害。"
    self.typ = CARD_CREATURE
    self.subtype = [SUBTYPE_DEMIGOD]
    self.originalcost = [0, 0, 0, 9, 0, 0] #White Fire Water Tree Light Death
    self.orimaxhealth = 12
    self.oriattack = 2
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
        buff = Buff(self.system, "b0000000051_000", self, self)
        self.add_buff(buff)


    
