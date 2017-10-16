from const import *
from buff import *

def init(self, mode = True):
    self.name = "调和者布兰卡"
    self.description = "你花费红色费用时, 你的所有手牌减少1点蓝色费用。你花费蓝色费用时, 你的所有手牌减少一点红色费用。"
    self.typ = CARD_CREATURE
    self.subtype = [SUBTYPE_BASIC, SUBTYPE_MIGICIAN]
    self.originalcost = [0, 3, 3, 0, 0, 0] #White Fire Water Tree Light Death
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
        buff = Buff(self.system, "b0000000029_000", self, self)
        self.add_buff(buff)

