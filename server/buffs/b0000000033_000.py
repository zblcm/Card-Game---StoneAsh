from const import *
from event import *
from card import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "定向射击"
    self.description = "使用: 对对方玩家造成5点魔法伤害。"
    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False

        targets = []
        for player in self.system.players:
            if player != self.card.player:
                targets.append(player)      

        damage = []
        sublists = ["fireball_sub_1", "fireball_sub_2", "fireball_sub_3"]
        for target in targets:
            self.system.playeffect("fireball", sublists, None, target)
            damage.append(5)
        self.system.yell(self.card)

        param = [targets, self.card, damage, DAMAGE_MAGICAL]
        event = Event(self.system, EVENT_DAMAGE, self, param)
        event.do()
        
        return False
    self.after_usecard = after_usecard
