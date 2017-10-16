from const import *
from event import *
from card import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "雪山灵狐"
    self.description = "战吼: 冻结一个未被冻结的生物。"
    def warcry(self, old_event):
        
        # 判断是否有生物可以冻结
        group = []
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (not card.unselectable(card, self.card.player)):
                freezed = False
                for buff in card.buffs:
                    if buff.filename == "nature_000003":
                        freezed = True
                if not freezed:
                    group.append(card)
        if len(group) <= 0:
            return False
        

        self.system.yell(self.card, 0)
        text = "请选择至多一个生物来冻结。"
        target = self.card.player.select(group, 1, text, 1, True, self)
        
        if len(target) <= 0:
            return False
        
        sublists = ["tinystar"]
        self.system.playeffect("iceball", sublists, self.card, target[0])
        self.system.yell(self.card)
        
        card = target[0]
        buff = Buff(self.system, "nature_000003", self.card, card)
        card.add_buff(buff)
        return False
    self.warcry = warcry
