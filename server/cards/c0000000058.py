from const import *
from event import *

def init(self, mode = True):
    self.name = "幻影龙"
    self.description = "成为法术牌的目标或受到魔法伤害时杀死自身。"
    self.typ = CARD_CREATURE
    self.subtype = [SUBTYPE_ILLUSION, SUBTYPE_DRAGON]
    self.originalcost = [0, 0, 6, 0, 0, 0] #White Fire Water Tree Light Death
    self.orimaxhealth = 7
    self.oriattack = 11
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
        buff = Buff(self.system, "nature_000002_auto", self, self)
        self.add_buff(buff)

    
