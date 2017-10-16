from const import *
from event import *
from card import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "迷雾"
    self.description = "使用: 你的不具有潜行的生物在下个你的回合开始前获得潜行。"

    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False
        
        group = []
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (card.player == self.card.player):
                hided = False
                for buff in card.buffs:
                    if buff.filename == "nature_000005":
                        hided = True
                if not hided:
                    group.append(card)
        if len(group) <= 0:
            return False

        self.system.yell(self.card, 0, True)
        sublists = ["tinystar"]
        for card in group:
            self.system.playeffect("whiteball", sublists, None, card)
        self.system.yell(self.card)
        
        for card in group:
            buff = Buff(self.system, "nature_000005", self.card, card)
            card.add_buff(buff)
        

    self.after_usecard = after_usecard
