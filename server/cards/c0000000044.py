from const import *
from event import *
from card import *

def init(self, mode = True):
    self.name = "生态恢复"
    self.description = "使你的全部法力水晶变为白色。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 0, 0, 6, 0, 0] #White Fire Water Tree Light Death

    def unusable(self):
        mana = self.player.getallmana()
        manasum = 0
        for i in range(5):
            manasum = manasum + mana[i + 1]
        if manasum == 0:
            return True
        return False
    self.unusable = unusable
    
    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        buff = Buff(self.system, "b0000000044_000", self, self)
        self.add_buff(buff)



    
