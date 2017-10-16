from const import *
from event import *
from card import *


def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "见习冰法师"
    self.description = "你每施放一个法术, 随机冻结一个未被冻结的敌方生物。"
    
    def after_usecard(self, old_event):
        card = old_event.param[0]
        if (self.card.place != PLACE_FIELD) or (card.typ != CARD_SPELL) or (card.player != self.card.player):
            return False
        
        # 判断是否有生物可以冻结
        group = []
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (card.player != self.card.player):
                freezed = False
                for buff in card.buffs:
                    if buff.filename == "nature_000003":
                        freezed = True
                if not freezed:
                    group.append(card)
        if len(group) <= 0:
            return False
        
        import random
        index = random.randint(0, len(group) - 1)
        
        card = group[index]
        
        self.system.yell(self.card, 0, True)
        sublists = ["tinystar"]
        self.system.playeffect("iceball", sublists, self.card, card)
        self.system.yell(self.card)
        
        buff = Buff(self.system, "nature_000003", self.card, card)
        card.add_buff(buff)
        
        return False
    self.after_usecard = after_usecard
