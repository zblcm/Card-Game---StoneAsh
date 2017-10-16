from const import *
from event import *
from card import *

def init(self, mode = True):
    self.name = "迷雾"
    self.description = "你的全部生物在下个你的回合开始前获得潜行。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 0, 0, 1, 0, 0] #White Fire Water Tree Light Death

    def unusable(self):
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (card.player == self.player):
                hided = False
                for buff in card.buffs:
                    if buff.filename == "nature_000005":
                        hided = True
                if not hided:
                    return False
        return True
    self.unusable = unusable
    
    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        buff = Buff(self.system, "b0000000043_000", self, self)
        self.add_buff(buff)



    
