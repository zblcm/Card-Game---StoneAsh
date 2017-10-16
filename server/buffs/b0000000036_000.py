from const import *
from event import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "风元素"
    self.description = "不受物理伤害, 受双倍魔法伤害。"

    def before_damage(self, old_event):
        if not (self.card in old_event.param[0]):
            return True
        
        index = old_event.param[0].index(self.card)
        
        if (old_event.param[3] == DAMAGE_PHYSICAL):
            old_event.param[4][index] = False
        
        if (old_event.param[3] == DAMAGE_MAGICAL):
            old_event.param[2][index] = old_event.param[2][index] * 2
        return True
    self.before_damage = before_damage
