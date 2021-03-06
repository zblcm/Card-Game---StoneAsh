from const import *
from buff import *

def init(self, mode = True):
    self.name = "集水者"
    self.description = "战吼: 将两张水元素置入你的手牌, 它们的法力消耗降低1点。"
    self.typ = CARD_CREATURE
    self.subtype = [SUBTYPE_HUMAN, SUBTYPE_MIGICIAN]
    self.originalcost = [0, 0, 2, 0, 0, 0] #White Fire Water Tree Light Death
    self.orimaxhealth = 1
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
        buff = Buff(self.system, "b0000000069_000", self, self)
        self.add_buff(buff)


    
