from const import *
from event import *

def init(self, mode = True):
    self.name = "小精灵"
    self.description = ""
    self.original = False
    self.typ = CARD_CREATURE
    self.subtype = []
    self.originalcost = [0, 0, 0, 1, 0, 0] #White Fire Water Tree Light Death
    self.orimaxhealth = 1
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

    
