from const import *
from buff import *

def init(self, mode = True):
    self.name = "遗迹守护兽"
    self.description = "嘲讽。无法攻击。每次被攻击前恢复所有生命值。"
    self.typ = CARD_CREATURE
    self.subtype = [SUBTYPE_DEMIGOD]
    self.originalcost = [0, 0, 0, 7, 0, 0] #White Fire Water Tree Light Death
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
        buff = Buff(self.system, "nature_000006_auto", self, self)
        self.add_buff(buff)
        buff = Buff(self.system, "b0000000059_000", self, self)
        self.add_buff(buff)


    
