from const import *
from event import *
from card import *


def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "薇安蒂魔导书"
    self.description = "使用: 随机施放一个法术。"

    def after_usecard(self, old_event):
        import random
        if not old_event.param[0] == self.card:
            return False

        numbers = []
        for cardtemp in self.system.allcards:
            cardtemp.player = self.card.player
            if (cardtemp.typ == CARD_SPELL) and (cardtemp.original) and (not cardtemp.unusable(cardtemp)):
                numbers.append(cardtemp.number)
        number = numbers[random.randint(1, len(numbers)) - 1]
        
        
        group = []
        new_card = Card(self.system, number, True, self.card.player)
        print(new_card.name + " 被释放了")
        new_card.source = None
        group.append(new_card)
        self.system.cards.append(new_card)
        self.system.yell(self.card, 1, True)
        
        parame = [new_card, None, False, False]
        event = Event(self.system, EVENT_USECARD, None, parame)
        event.do()
    self.after_usecard = after_usecard
