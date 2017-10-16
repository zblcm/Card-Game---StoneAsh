from const import *
from event import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "集水者"
    self.description = "战吼: 将两张水元素置入你的手牌, 它们的法力消耗降低1点。"

    def warcry(self, old_event):
        group = []

        self.system.yell(self.card, 1, True)
        
        new_card = Card(self.system, 17, True, self.card.player)
        new_card.source = None
        buff = Buff(self.system, "b0000000069_001", self.card, new_card)
        new_card.add_buff(buff)
        group.append(new_card)
        self.system.cards.append(new_card)
        
        new_card = Card(self.system, 17, True, self.card.player)
        new_card.source = None
        buff = Buff(self.system, "b0000000069_001", self.card, new_card)
        new_card.add_buff(buff)
        group.append(new_card)
        self.system.cards.append(new_card)
        
        param = [group, PLACE_HAND, True, False, False, False, False]
        event = Event(self.system, EVENT_MOVE, self, param)
        event.do()

        return True
    self.warcry = warcry
