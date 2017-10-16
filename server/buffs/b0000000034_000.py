from const import *
from event import *
from card import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "炎枪术"
    self.description = "使用: 造成8点魔法伤害。"
    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False
        
        # 判断是否有角色可以造成伤害
        group = []
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (not card.unselectable(card, self.card.player)):
                group.append(card)
        for player in self.system.players:
            if player.alive:
                group.append(player)
        if len(group) <= 0:
            return False
        
        self.system.yell(self.card, 0)
        text = "请选择一个角色来造成8点魔法伤害。"
        targets = self.card.player.select(group, 1, text, 0, True, self)        
        
        sublists = ["fireball_sub_1", "fireball_sub_2", "fireball_sub_3"]
        self.system.playeffect("firespear", sublists, None, targets[0])
        self.system.yell(self.card)
        
        damage = []
        for character in targets:
            damage.append(8)
        param = [targets, self.card, damage, DAMAGE_MAGICAL]
        event = Event(self.system, EVENT_DAMAGE, self, param)
        event.do()
        
        return False
    self.after_usecard = after_usecard
