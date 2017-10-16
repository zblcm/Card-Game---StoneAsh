from const import *
from event import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "烈焰小鬼"
    self.description = "战吼: 对最多一个角色造成1点魔法伤害。"

    # 战吼 造成1点魔法伤害
    def warcry(self, old_event):
        
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
        text = "请选择至多一个角色来造成1点魔法伤害。"
        target = self.card.player.select(group, 1, text, 1, True, self)
        
        if len(target) <= 0:
            return False
        
        sublists = ["fireball_sub_1", "fireball_sub_2", "fireball_sub_3"]
        self.system.playeffect("fireball", sublists, self.card, target[0])
        self.system.yell(self.card)
        
        damage = []
        for character in target:
            damage.append(1)
        param = [target, self.card, damage, DAMAGE_MAGICAL]
        event = Event(self.system, EVENT_DAMAGE, self, param)
        event.do()

        return True
    self.warcry = warcry
