from const import *
from event import *
from card import *


def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "伊瓦尔魔导书"
    self.description = "使用: 随机召唤一个法师。"

    def after_usecard(self, old_event):
        import random
        if not old_event.param[0] == self.card:
            return False

        self.system.yell(self.card, 1, True)

        numbers = []
        for cardtemp in self.system.allcards:
            if SUBTYPE_MIGICIAN in cardtemp.subtype:
                numbers.append(cardtemp.number)
        number = numbers[random.randint(1, len(numbers)) - 1]
        
        group = []
        new_card = Card(self.system, number, True, self.card.player)
        new_card.source = None
        group.append(new_card)
        self.system.cards.append(new_card)
        
        param = [group, PLACE_FIELD, True, False, False, False, False]
        event = Event(self.system, EVENT_MOVE, self, param)
        event.do()
    self.after_usecard = after_usecard
