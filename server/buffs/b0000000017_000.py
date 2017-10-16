from const import *
from event import *
from card import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "水元素"
    self.description = "冻结受到该生物伤害的生物。"
    
    def after_damage(self, old_event):
        targets = old_event.param[0]
        source = old_event.param[1]
        if (self.card == source):
            group = []
            for card in targets:
                if (isinstance(card, Card)) and (card.place == PLACE_FIELD) and (card.player != self.card.player):
                    freezed = False
                    for buff in card.buffs:
                        if buff.filename == "nature_000003":
                            freezed = True
                    if not freezed:
                        group.append(card)
            if len(group) <= 0:
                return False

            self.system.yell(self.card, 0, True)
            sublists = ["tinystar"]
            for card in group:
                self.system.playeffect("iceball", sublists, self.card, card)
            self.system.yell(self.card)

            for card in group:
                buff = Buff(self.system, "nature_000003", self.card, card)
                card.add_buff(buff)
                
                
    self.after_damage = after_damage
