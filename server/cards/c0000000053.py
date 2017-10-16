from const import *
from buff import *

def init(self, mode = True):
    self.name = "潜行蜥蜴"
    self.description = "潜行。你的回合结束时, 使一个随机友方生物获得潜行。"
    self.typ = CARD_CREATURE
    self.subtype = []
    self.originalcost = [0, 0, 0, 5, 0, 0] #White Fire Water Tree Light Death
    self.orimaxhealth = 8
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
        buff = Buff(self.system, "nature_000005_auto", self, self)
        self.add_buff(buff)
        buff = Buff(self.system, "b0000000053_000", self, self)
        self.add_buff(buff)


    
