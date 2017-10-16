from const import *
from event import *


        

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = False
    self.visable = True
    self.name = "狼光环"
    self.description = "你的野兽+1攻击力。"

    def oncreate(self, old_event = None):
        self.effectbuff = []
        self.effectcard = []
        for card in self.system.cards:
            if (card.player == self.card.player) and (card.place == PLACE_FIELD) and (SUBTYPE_BEAST in card.subtype):
                new_buff = Buff(self.system, "b0000000047_002", self.card, card)
                card.add_buff(new_buff)
                self.effectbuff.append(new_buff)
                self.effectcard.append(card)
    self.oncreate = oncreate
    
    def onremove(self, old_event = None):
        for buff in self.effectbuff:
            buff.card.remove_buff(buff)
    self.onremove = onremove
    
    def after_move(self, old_event):
        # 自己离场
        if (self.card in old_event.param[0]) and (self.card.place != PLACE_FIELD):
            self.card.remove_buff(self)
            return False

        # 其他卡片进场
        for card in old_event.param[0]:
            if (card.place == PLACE_FIELD) and (not card in self.effectcard) and (card.player == self.card.player) and (SUBTYPE_BEAST in card.subtype):
                new_buff = Buff(self.system, "b0000000047_002", self.card, card)
                card.add_buff(new_buff)
                self.effectbuff.append(new_buff)
                self.effectcard.append(card)

        # 其他卡片离场
        for card in old_event.param[0]:
            if (card.place != PLACE_FIELD) and (card in self.effectcard):
                for buff in self.effectbuff:
                    if buff in card.buffs:
                        card.remove_buff(buff)
                        self.effectbuff.remove(buff)
                        self.effectcard.remove(card)
    self.after_move = after_move
