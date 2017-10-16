from const import *
from event import *
from card import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "冰爆"
    self.description = "使用: 消灭敌方所有被冻结的生物。"

    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False
        group = []
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (card.player != self.card.player):
                freezed = False
                for buff in card.buffs:
                    if buff.filename == "nature_000003":
                        freezed = True
                if freezed:
                    group.append(card)
        if len(group) <= 0:
            return False

        self.system.yell(self.card, 0, True)
        sublists = ["tinystar"]
        for card in group:
            self.system.playeffect("iceball", sublists, None, card)
        self.system.yell(self.card)
        
        param = [group, self.card, True]
        event = Event(self.system, EVENT_KILL, self, param)
        event.do()
        

    self.after_usecard = after_usecard
