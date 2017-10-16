from const import *
from event import *
from card import *


def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "水系法师"
    self.description = "你每释放一个法术, 召唤一个2/2的水元素。"
    
    def after_usecard(self, old_event):
        card = old_event.param[0]
        if (self.card.place != PLACE_FIELD) or (card.typ != CARD_SPELL) or (card.player != self.card.player):
            return False

        self.system.yell(self.card, 0, True)
        sublists = ["tinystar"]
        self.system.playeffect("bluelight", sublists, self.card, self.card)
        self.system.yell(self.card, 1)

        group = []

        card = Card(self.system, 17, True, self.card.player)
        card.source = None

        card.orimaxhealth = 2
        card.oriattack = 2
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
