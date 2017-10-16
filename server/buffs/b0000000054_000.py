from const import *
from event import *
from card import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "心像探知"
    self.description = "使用: 查看并选择对方一张手牌。将其置入你的手牌, 并将其法力消耗变为蓝色。"

    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False
        
        group = []
        for card in self.system.cards:
            if (card.place == PLACE_HAND) and (card.player != self.card.player) and (not card.unselectable(card, self.card.player)):
                group.append(card)
        if len(group) <= 0:
            return False

        self.system.yell(card, 0)
        text = "请选择一张卡片来置入你的手牌, 并将其法力消耗变为蓝色。"
        targets = self.card.player.select(group, 1, text, 0, True, self)
        
        target = targets[0]
        sublists = ["tinystar"]
        self.system.playeffect("whiteball", sublists, None, target)
        self.system.yell(card)
        
        target.player = self.card.player
        
        buff = Buff(self.system, "b0000000054_001", self.card, target)
        target.add_buff(buff)
        

    self.after_usecard = after_usecard
