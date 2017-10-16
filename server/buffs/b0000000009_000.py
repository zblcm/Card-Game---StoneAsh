from const import *
from event import *
from card import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "读心术"
    self.description = "使用: 查看并选择对方一张手牌。你使用该牌, 并且无需支付其法力。不能使用时将会弃掉该牌。"

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
        text = "请选择一张卡片来使用。不能使用的场合将弃掉。"
        targets = self.card.player.select(group, 1, text, 0, True, self)
        
        target = targets[0]
        sublists = ["tinystar"]
        self.system.playeffect("whiteball", sublists, None, target)
        self.system.yell(card)
        
        old_player = target.player
        target.player = self.card.player
        if (target.unusable(target)):
            # 弃掉的场合
            target.player = old_player
            param = [[target], PLACE_GRAVE, False, False, False, False, True]
            event = Event(self.system, EVENT_MOVE, self, param)
            event.do()
        else:
            # 使用的场合
            parame = [target, None, True, False]
            event = Event(self.system, EVENT_USECARD, None, parame)
            event.do()
        

    self.after_usecard = after_usecard
