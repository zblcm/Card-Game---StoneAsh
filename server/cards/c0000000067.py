from const import *
from buff import *

def init(self, mode = True):
    self.name = "幻象师"
    self.description = "敌方每召唤一个生物, 召唤一个具有相同攻击力和生命值的幻象。"
    self.typ = CARD_CREATURE
    self.subtype = [SUBTYPE_HUMAN, SUBTYPE_MIGICIAN]
    self.originalcost = [0, 0, 5, 0, 0, 0] #White Fire Water Tree Light Death
    self.orimaxhealth = 6
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
        buff = Buff(self.system, "b0000000067_000", self, self)
        self.add_buff(buff)


    
