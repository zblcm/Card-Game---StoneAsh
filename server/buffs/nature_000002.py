from const import *
from event import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = False
    self.visable = True
    self.name = "幻象生物"
    self.description = "受到魔法伤害或被作为法术牌的目标时, 杀死自身。"

    def operation(self):
        target = self.card
        param = [[target], self.card, True]
        event = Event(self.system, EVENT_KILL, self, param)
        event.do()

    def onplayerselect(self, old_event):
        target = old_event.param[1]
        if (self.card in target) and (self.card.place == PLACE_FIELD) and (old_event.buff and old_event.buff.card and old_event.buff.card.typ == CARD_SPELL):
            operation(self)
    self.onplayerselect = onplayerselect

    def after_damage(self, old_event):
        target = old_event.param[0]
        reason = old_event.param[3]
        if (self.card in target) and (self.card.place == PLACE_FIELD) and (reason == DAMAGE_MAGICAL):
            operation(self)
    self.after_damage = after_damage

    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (old_event.param[1] != PLACE_FIELD):
            self.card.remove_buff(self)
            return False
    self.after_move = after_move
