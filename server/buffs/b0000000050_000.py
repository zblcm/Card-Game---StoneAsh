from const import *
from event import *
from card import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "精神涌动"
    self.description = "使用: 召唤4个1/1的小精灵, 并使你的全部小精灵获得风怒。"

    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False
        
        self.system.yell(self.card, 0, True)
        sublists = ["tinyleaf_1", "tinyleaf_2", "tinyleaf_3"]
        self.system.playeffect("greenlight", sublists, None, None)
        self.system.yell(self.card, 1)
        
        group = []

        for i in range(4):
            new_card = Card(self.system, 41, True, self.card.player)
            new_card.source = None
            group.append(new_card)
            self.system.cards.append(new_card)
                
        
        param = [group, PLACE_FIELD, True, False, False, False, False]
        event = Event(self.system, EVENT_MOVE, self, param)
        event.do()

        for card in self.system.cards:
            if (card.player == self.card.player) and (card.number == 41):
                buff = Buff(self.system, "nature_000004", self.card, card)
                card.add_buff(buff)
                    
    self.after_usecard = after_usecard
