from const import *
from event import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "地狱驯犬人"
    self.description = "战吼: 召唤两个2/1带有冲锋的地狱犬。"

    # 战吼 造成1点魔法伤害
    def warcry(self, old_event):
        
        group = []

        self.system.yell(self.card, 1, True)
        
        new_card = Card(self.system, 27, True, self.card.player)
        new_card.source = None
        group.append(new_card)
        self.system.cards.append(new_card)
        
        new_card = Card(self.system, 27, True, self.card.player)
        new_card.source = None
        group.append(new_card)
        self.system.cards.append(new_card)
        
        param = [group, PLACE_FIELD, True, False, False, False, False]
        event = Event(self.system, EVENT_MOVE, self, param)
        event.do()

        return True
    self.warcry = warcry
