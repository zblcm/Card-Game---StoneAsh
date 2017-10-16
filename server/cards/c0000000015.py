from const import *
from buff import *

def init(self, mode = True):
    self.name = "见习冰法师"
    self.description = "你每施放一个法术, 随机冻结一个未被冻结的敌方生物。"
    self.typ = CARD_CREATURE
    self.subtype = [SUBTYPE_HUMAN, SUBTYPE_MIGICIAN]
    self.originalcost = [0, 0, 3, 0, 0, 0] #White Fire Water Tree Light Death
    self.orimaxhealth = 4
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
        buff = Buff(self.system, "b0000000015_000", self, self)
        self.add_buff(buff)


    
