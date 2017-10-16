from const import *
from buff import *

def init(self, mode = True):
    self.name = "迪普沃尔"
    self.description = "你每施放一个法术, 将一张法力消耗减少1点的火球术加入手牌。"
    self.typ = CARD_CREATURE
    self.subtype = [SUBTYPE_HUMAN, SUBTYPE_MIGICIAN]
    self.originalcost = [0, 7, 0, 0, 0, 0] #White Fire Water Tree Light Death    self.orimaxhealth = 1
    self.orimaxhealth = 8
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
        buff = Buff(self.system, "b0000000031_000", self, self)
        self.add_buff(buff)

    
