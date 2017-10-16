from const import *
from buff import *

def init(self, mode = True):
    self.name = "水系法师"
    self.description = "你每释放一个法术, 召唤一个2/2的水元素。"
    self.typ = CARD_CREATURE
    self.subtype = [SUBTYPE_HUMAN, SUBTYPE_MIGICIAN]
    self.originalcost = [0, 0, 5, 0, 0, 0] #White Fire Water Tree Light Death
    self.orimaxhealth = 4
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
        buff = Buff(self.system, "b0000000070_000", self, self)
        self.add_buff(buff)


    
