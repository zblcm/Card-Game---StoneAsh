from const import *
from event import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "山峰"
    self.description = "每次最多受到1点伤害。攻击生物时对其他敌方生物造成相同的物理伤害。"

    def before_damage(self, old_event):
        if not (self.card in old_event.param[0]):
            return True
        
        index = old_event.param[0].index(self.card)
        
        if (old_event.param[2][index] > 1):
            old_event.param[2][index] = 1
        return True
    self.before_damage = before_damage
    
    def after_attack(self, old_event):
        attacker = old_event.param[0]
        target = old_event.param[1]
        if (self.card != attacker) or (not (target in self.system.cards)):
            return False

        group = []
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (card.player != self.card.player) and (card != target):
                group.append(card)

        damage = []
        for card in group:
            damage.append(self.card.attack)
        
        param = [group, self.card, damage, DAMAGE_PHYSICAL]
        event = Event(self.system, EVENT_DAMAGE, self, param)
        event.do()
        
        return False      
    self.after_attack = after_attack
