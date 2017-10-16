from const import *
from event import *
from card import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "兽性幻影"
    self.description = "使用: 召唤2只2/2的幻影野猪。"

    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False
        group = []

        self.system.yell(self.card, 0, True)
        sublists = ["tinystar"]
        self.system.playeffect("bluelight", sublists, None, None)
        self.system.yell(self.card, 1)
        
        new_card = Card(self.system, 1, True, self.card.player)
        new_card.source = None
        group.append(new_card)
        self.system.cards.append(new_card)
        
        new_card = Card(self.system, 1, True, self.card.player)
        new_card.source = None
        group.append(new_card)
        self.system.cards.append(new_card)
        
        param = [group, PLACE_FIELD, True, False, False, False, False]
        event = Event(self.system, EVENT_MOVE, self, param)
        event.do()
    self.after_usecard = after_usecard
