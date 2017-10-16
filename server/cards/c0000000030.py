from const import *
from buff import *

def init(self, mode = True):
    self.name = "炎铸剑师"
    self.description = "战吼: 使一个生物本回合攻击力+4并不受物理伤害。"
    self.typ = CARD_CREATURE
    self.subtype = [SUBTYPE_DEVIL]
    self.originalcost = [0, 4, 0, 0, 0, 0] #White Fire Water Tree Light Death    self.orimaxhealth = 1
    self.orimaxhealth = 3
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
        buff = Buff(self.system, "b0000000030_000", self, self)
        self.add_buff(buff)

    
