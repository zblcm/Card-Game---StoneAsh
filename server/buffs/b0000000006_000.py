from const import *
from event import *
from card import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "肌能燃烧"
    self.description = "使用: 目标生物攻击力+2。"
    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False
        
        # 判断是否有生物可以增加攻击力
        group = []
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (not card.unselectable(card, self.card.player)):
                group.append(card)
        if len(group) <= 0:
            return False
        

        self.system.yell(self.card, 0)
        text = "请选择一只生物来增加3点攻击力。"
        target = self.card.player.select(group, 1, text, 0, True, self)
        sublists = ["tinystar"]
        self.system.playeffect("whiteball", sublists, None, target[0])
        self.system.yell(self.card)
        
        card = target[0]
        buff = Buff(self.system, "b0000000006_001", self.card, card)
        card.add_buff(buff)
        return False
    self.after_usecard = after_usecard
