from const import *
from event import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "寒冰箭"
    self.description = "使用: 冻结目标生物并造成3点魔法伤害。如果目标已被冻结则将其消灭。"

    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False
        group = []

        # 判断是否有生物可以作为目标
        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (not card.unselectable(card, self.card.player)):
                group.append(card)
        if len(group) <= 0:
            return False

        self.system.yell(self.card, 0)
        text = "请选择至多一个角色来冻结或造成伤害。"
        targets = self.card.player.select(group, 1, text, 1, True, self)
        sublists = ["tinystar"]
        self.system.playeffect("iceball", sublists, None, targets[0])
        self.system.yell(self.card)
        
        target = targets[0]
        freezed = False
        for buff in target.buffs:
            if buff.filename == "nature_000003":
                freezed = True

        if freezed:
            param = [targets, self.card, True]
            event = Event(self.system, EVENT_KILL, self, param)
            event.do()
        else:
            # 冰冻
            buff = Buff(self.system, "nature_000003", self.card, target)
            target.add_buff(buff)

            # 伤害
            param = [targets, self.card, [3], DAMAGE_MAGICAL]
            event = Event(self.system, EVENT_DAMAGE, self, param)
            event.do()

        return True
        
    self.after_usecard = after_usecard
