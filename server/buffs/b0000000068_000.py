from const import *
from event import *
from card import *


def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "见习幻象师"
    self.description = "你每施放一个法术, 召唤一个1/1的幻象。"
    
    def after_usecard(self, old_event):
        card = old_event.param[0]
        if (self.card.place != PLACE_FIELD) or (card.typ != CARD_SPELL) or (card.player != self.card.player):
            return False

        self.system.yell(self.card, 0, True)
        sublists = ["tinystar"]
        self.system.playeffect("bluelight", sublists, self.card, self.card)
        self.system.yell(self.card, 1)

        group = []

        card = Card(self.system, 66, True, self.card.player)

        card.orimaxhealth = 1
        card.oriattack = 1
        card.maxhealth = card.orimaxhealth
        card.health = card.maxhealth
        card.attack = card.oriattack
            
        card.source = None
        group.append(card)
        self.system.cards.append(card)
        
        param = [group, PLACE_FIELD, True, False, False, False, False]
        event = Event(self.system, EVENT_MOVE, self, param)
        event.do()
        
        return False
    self.after_usecard = after_usecard
