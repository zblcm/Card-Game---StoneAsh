from const import *
from event import *


        

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.name = "遗迹守护兽"
    self.description = "无法攻击。每次被攻击前恢复所有生命值。"

    self.flag_cannotattack = True
    
    def before_attack(self, old_event):
        attacker = old_event.param[0]
        target = old_event.param[1]
        if self.card != target:
            return True

        group = [self.card]
        amount = [self.card.maxhealth - self.card.health]

        self.system.yell(self.card, 0, True)
        sublists = ["tinyleaf_1", "tinyleaf_2", "tinyleaf_3"]
        self.system.playeffect("greenlight", sublists, self.card, self.card)
        self.system.yell(self.card, 1)
        
        param = [group, self.card, amount]
        event = Event(self.system, EVENT_HEAL, self, param)
        event.do()

        return True
        
    self.before_attack = before_attack
