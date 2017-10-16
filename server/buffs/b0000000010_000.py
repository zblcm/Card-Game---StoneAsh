from const import *
from event import *
from card import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "火焰飞斩"
    self.description = "使用: 对一个生物造成2点魔法伤害, 并对他的控制者造成2点魔法伤害。"
    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False
        
        # 判断是否有角色可以造成伤害
        group = []
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (not card.unselectable(card, self.card.player)):
                group.append(card)
        if len(group) <= 0:
            return False
        
        self.system.yell(self.card, 0)
        text = "请选择一个生物来造成2点魔法伤害。"
        targets = self.card.player.select(group, 1, text, 0, True, self)        
        targets.append(targets[0].player)
        damage = [2, 2]
        
        sublists = ["fireball_sub_1", "fireball_sub_2", "fireball_sub_3"]
        self.system.playeffect("fireball", sublists, None, targets[0])
        self.system.playeffect("fireball", sublists, None, targets[1])
        self.system.yell(self.card)

        param = [targets, self.card, damage, DAMAGE_MAGICAL]
        event = Event(self.system, EVENT_DAMAGE, self, param)
        event.do()
        
        return False
    self.after_usecard = after_usecard
