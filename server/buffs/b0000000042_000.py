from const import *
from event import *
from card import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "精神爆发"
    self.description = "使用: 召唤2个1/1的小精灵, 并使你的全部小精灵具有冲锋。"

    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False
        
        self.system.yell(self.card, 0, True)
        sublists = ["tinyleaf_1", "tinyleaf_2", "tinyleaf_3"]
        self.system.playeffect("greenlight", sublists, None, None)
        self.system.yell(self.card, 1)
        
        group = []
        
        new_card = Card(self.system, 41, True, self.card.player)
        new_card.source = None
        group.append(new_card)
        self.system.cards.append(new_card)
        
        new_card = Card(self.system, 41, True, self.card.player)
        new_card.source = None
        group.append(new_card)
        self.system.cards.append(new_card)
        
        param = [group, PLACE_FIELD, True, False, False, False, False]
        event = Event(self.system, EVENT_MOVE, self, param)
        event.do()

        for card in self.system.cards:
            if (card.player == self.card.player) and (card.number == 41):
                for buff in card.buffs:
                    if buff.filename == "nature_000000":
                        card.remove_buff(buff)
    self.after_usecard = after_usecard
