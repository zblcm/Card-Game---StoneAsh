from const import *
from event import *
from card import *


def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "迪普沃尔"
    self.description = "你每施放一个法术, 将一张法力消耗减少1点的火球术加入手牌。"
    
    def after_usecard(self, old_event):
        card = old_event.param[0]
        if (self.card.place != PLACE_FIELD) or (card.typ != CARD_SPELL) or (card.player != self.card.player):
            return False

        group = []

        self.system.yell(self.card, 1, True)
        
        new_card = Card(self.system, 28, True, self.card.player)
        new_card.source = None
        group.append(new_card)
        self.system.cards.append(new_card)
        
        param = [group, PLACE_HAND, True, False, False, False, False]
        event = Event(self.system, EVENT_MOVE, self, param)
        event.do()

        buff = Buff(self.system, "b0000000031_001", self.card, new_card)
        new_card.add_buff(buff)
        
        return False
    self.after_usecard = after_usecard
