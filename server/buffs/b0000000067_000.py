from const import *
from event import *
from card import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "幻象师"
    self.description = "敌方每召唤一个生物, 召唤一个具有相同攻击力和生命值的幻象。"

    def summonone(self):

        return True
        
    def after_move(self, old_event):
        if (old_event.param[1] != PLACE_FIELD) or (self.card.place != PLACE_FIELD):
            return False
        movers = old_event.param[0]

        templates = []
        for card in movers:
            if card.player != self.card.player:
                templates.append(card)

        if len(templates) <= 0:
            return False

        self.system.yell(self.card, 0, True)
        sublists = ["tinystar"]
        self.system.playeffect("bluelight", sublists, self.card, self.card)
        self.system.yell(self.card, 1)
        
        group = []
        for i in range(len(templates)):
            card = Card(self.system, 66, True, self.card.player)

            card.orimaxhealth = templates[i].orimaxhealth
            card.oriattack = templates[i].oriattack
            card.maxhealth = templates[i].maxhealth
            card.health = templates[i].health
            card.attack = templates[i].attack
            
            card.source = None
            group.append(card)
            self.system.cards.append(card)
        
        param = [group, PLACE_FIELD, True, False, False, False, False]
        event = Event(self.system, EVENT_MOVE, self, param)
        event.do()
        
        return True
    self.after_move = after_move
