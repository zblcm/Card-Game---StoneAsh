from const import *
from event import *
from card import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "火元素"
    self.description = "攻击时不造成攻击, 对对方造成自己攻击力的魔法伤害。"
    
    def before_attack(self, old_event):
        attacker = old_event.param[0]
        target = old_event.param[1]
        if self.card != attacker:
            return True

        self.system.yell(self.card, 0, True)
        sublists = ["fireball_sub_1", "fireball_sub_2", "fireball_sub_3"]
        self.system.playeffect("fireball", sublists, self.card, target)
        self.system.yell(self.card)
        
        damage = [self.card.attack]
        param = [[target], self.card, damage, DAMAGE_MAGICAL]
        event = Event(self.system, EVENT_DAMAGE, self, param)
        event.do()
        
        return False      
    self.before_attack = before_attack
