from const import *
from event import *
from card import *


def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "结霜者"
    self.description = "你每召唤一个生物, 随机冻结对方的一个未冻结的生物。"

    def freezeone(self):
        
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
        
        self.system.yell(self.card, 0.25)
        sublists = ["tinystar"]
        self.system.playeffect("iceball", sublists, self.card, card)
        
        buff = Buff(self.system, "nature_000003", self.card, card)
        card.add_buff(buff)

        return True
        
    def after_move(self, old_event):
        if (old_event.param[1] != PLACE_FIELD) or (self.card.place != PLACE_FIELD):
            return False
        movers = old_event.param[0]

        number = 0
        for card in movers:
            if card.player == self.card.player:
                number = number + 1

        if number == 0:
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

        self.system.yell(self.card, 0, True)

        for i in range(number):
            if not freezeone(self):
                self.system.yell(self.card, 0.75)
                return True

        self.system.yell(self.card, 0.75)
        
        return True
    self.after_move = after_move
