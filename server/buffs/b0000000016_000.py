from const import *
from event import *
from card import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "怒火爆发"
    self.description = "使用: 目标生物失去召唤失调及冻结, 在回合结束前攻击力+2。"
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
        text = "选择一只生物失去召唤失调及冻结, 在回合结束前攻击力+2。"
        target = self.card.player.select(group, 1, text, 0, True, self)
        sublists = ["tinystar"]
        self.system.playeffect("whiteball", sublists, None, target[0])
        self.system.yell(self.card)
        
        card = target[0]

        for buff in card.buffs:
            if (buff.filename == "nature_000000") or (buff.filename == "nature_000003"):
                card.remove_buff(buff)
        
        buff = Buff(self.system, "b0000000016_001", self.card, card)
        card.add_buff(buff)
        return False
    self.after_usecard = after_usecard
