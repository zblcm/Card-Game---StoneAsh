from const import *
from buff import *

def init(self, mode = True):
    self.name = "森林"
    self.description = "你每消耗1点法力, 回复1点生命值。你的回合开始时治疗所有友方生物。"
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
        buff = Buff(self.system, "b0000000052_000", self, self)
        self.add_buff(buff)


    
