from const import *
from event import *
from card import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "燎原火"
    self.description = "使用: 对对方所有生物造成1点伤害。"

    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False
        group = []
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (card.player != self.card.player):
                group.append(card)
        if len(group) <= 0:
            return False

        self.system.yell(self.card, 0, True)
        sublists = ["fireball_sub_1", "fireball_sub_2", "fireball_sub_3"]
        for card in group:
            self.system.playeffect("fireball", sublists, None, card)
        self.system.yell(self.card)
        
        damage = []
        for character in group:
            damage.append(1)
        param = [group, self.card, damage, DAMAGE_MAGICAL]
        event = Event(self.system, EVENT_DAMAGE, self, param)
        event.do()
        

    self.after_usecard = after_usecard
