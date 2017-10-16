from const import *
from event import *
from card import *


def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "纵火恶魔"
    self.description = "你每使用一张法术牌, 对一个随机敌方角色造成2点魔法伤害。"
    def after_usecard(self, old_event):
        card = old_event.param[0]
        if (self.card.place != PLACE_FIELD) or (card.typ != CARD_SPELL) or (card.player != self.card.player) or (old_event.param[2] == False):
            return False
        
        # 判断是否有角色可以造成伤害
        group = []
        group_2 = []
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (card.player != self.card.player):
                # 优先对生命值大于0的生物造成伤害
                if card.health > 0:
                    group.append(card)
                else:
                    group_2.append(card)
        for player in self.system.players:
            if (player.alive) and (player != self.card.player):
                group.append(player)
        if len(group) <= 0:
            group = group_2
        if len(group) <= 0:
            return False
        
        import random
        index = random.randint(0, len(group) - 1)
        
        card = group[index]
        targets = [card]
        damage = [2]

        self.system.yell(self.card, 0, True)
        sublists = ["fireball_sub_1", "fireball_sub_2", "fireball_sub_3"]
        self.system.playeffect("fireball", sublists, self.card, card)
        self.system.yell(self.card)

        param = [targets, self.card, damage, DAMAGE_MAGICAL]
        event = Event(self.system, EVENT_DAMAGE, self, param)
        event.do()
        
        return False
    self.after_usecard = after_usecard
