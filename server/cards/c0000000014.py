from const import *
from buff import *

def init(self, mode = True):
    self.name = "纵火恶魔"
    self.description = "你每使用一张法术牌, 对对方一名随机角色造成2点魔法伤害。"
    self.typ = CARD_CREATURE
    self.subtype = [SUBTYPE_DEVIL, SUBTYPE_MIGICIAN]
    self.originalcost = [0, 2, 0, 0, 0, 0] #White Fire Water Tree Light Death
    self.orimaxhealth = 3
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
        buff = Buff(self.system, "b0000000014_000", self, self)
        self.add_buff(buff)


    
