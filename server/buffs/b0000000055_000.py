from const import *
from event import *
from card import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "脑死"
    self.description = "使用: 查看并选择对方一张手牌。弃掉该牌。"

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
        text = "请选择一张卡片来弃掉。"
        targets = self.card.player.select(group, 1, text, 0, True, self)
        
        target = targets[0]
        sublists = ["tinystar"]
        self.system.playeffect("whiteball", sublists, None, target)
        self.system.yell(card)
        
        param = [[target], PLACE_GRAVE, False, False, False, False, True]
        event = Event(self.system, EVENT_MOVE, self, param)
        event.do()

    self.after_usecard = after_usecard
