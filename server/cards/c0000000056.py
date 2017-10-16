from const import *
from buff import *




def init(self, mode = True):
    self.name = "意识拷贝"
    self.description = "查看并选择对方一张手牌。将一张该牌的复制加入你的手牌, 并将其法力消耗变为蓝色。"
    self.typ = CARD_SPELL
    self.subtype = [SUBTYPE_BASIC]
    self.originalcost = [0, 0, 2, 0, 0, 0] #White Fire Water Tree Light Death
    
    def unusable(self):
        for card in self.system.cards:
            if (card.place == PLACE_HAND) and (card.player != self.player) and (not card.unselectable(card, self.player)):
                return False
        return True
    self.unusable = unusable
    
    if mode:
        self.cost = self.originalcost.copy()
        self.needtarget = False
        buff = Buff(self.system, "b0000000056_000", self, self)
        self.add_buff(buff)

