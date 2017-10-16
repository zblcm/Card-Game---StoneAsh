from const import *
from event import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "炎铸剑师"
    self.description = "战吼: 使一个单位本回合攻击力+4, 不受物理伤害。"

    # 战吼
    def warcry(self, old_event):
        
        # 判断是否有角色可以造成伤害
        group = []
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (not card.unselectable(card, self.card.player)):
                group.append(card)
        if len(group) <= 0:
            return False
        
        self.system.yell(self.card, 0)
        text = "请选择至多一个角色攻击力+4并不受物理伤害。"
        targets = self.card.player.select(group, 1, text, 1, True, self)
        
        if len(targets) <= 0:
            return False
        
        sublists = ["tinystar"]
        self.system.playeffect("whiteball", sublists, None, targets[0])
        self.system.yell(self.card)
        
        card = targets[0]
        buff = Buff(self.system, "b0000000030_001", self.card, card)
        card.add_buff(buff)

        return True
    self.warcry = warcry
