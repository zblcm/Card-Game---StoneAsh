from const import *
from event import *
from card import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "莱克斯魔导书"
    self.description = "使用: 你手牌中的法术牌随机减少1点法力消耗。"

    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False
        group = []
        for card in self.system.cards:
            if (card.place == PLACE_HAND) and (card.player == self.card.player) and (card.typ == CARD_SPELL) and (card != self.card):
                group.append(card)
        if len(group) <= 0:
            return False

        self.system.yell(self.card, 0, True)
        sublists = ["tinystar"]
        for card in group:
            self.system.playeffect("whiteball", sublists, None, card)
        self.system.yell(self.card)
        
        for card in group:
            buff = Buff(self.system, "b0000000023_001", self.card, card)
            card.add_buff(buff)        

    self.after_usecard = after_usecard
