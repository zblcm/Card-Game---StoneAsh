from const import *
from event import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "迷魂箭"
    self.description = "对目标生物造成3点魔法伤害, 并使其攻击力减少7点。"

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
        text = "请选择至多一个角色来造成伤害并减少攻击力。"
        targets = self.card.player.select(group, 1, text, 1, True, self)
        sublists = ["purpleblot_sub"]
        self.system.playeffect("purpleblot", sublists, None, targets[0])
        self.system.yell(self.card)
        
        target = targets[0]
        freezed = False

        # 减攻击
        buff = Buff(self.system, "b0000000073_001", self.card, target)
        target.add_buff(buff)

        # 伤害
        param = [targets, self.card, [3], DAMAGE_MAGICAL]
        event = Event(self.system, EVENT_DAMAGE, self, param)
        event.do()

        return True
        
    self.after_usecard = after_usecard
