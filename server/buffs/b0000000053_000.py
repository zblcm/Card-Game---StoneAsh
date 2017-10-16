from const import *
from event import *


        

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.name = "潜行蜥蜴"
    self.description = "潜行。你的回合结束时, 使一个随机友方生物获得潜行。"

    def getcardmaxturnnum(card):
        maxturnnum = 0
        for buff in card.buffs:
            if buff.filename == "nature_000005":
                if buff.turnleft < 0:
                    return buff.turnleft
                if buff.turnleft > maxturnnum:
                    maxturnnum = buff.turnleft
        return maxturnnum
    
    def onturnstop(self, old_event):
        if (self.card.player != old_event.param[0]) or (self.card.place != PLACE_FIELD):
            return False

        # 优先选择潜行时间最短的生物
        minturnnum = -1

        for card in self.system.cards:
            if (card.place == PLACE_FIELD) and (card.player == self.card.player):
                cardmaxturnnum = getcardmaxturnnum(card)
                if (cardmaxturnnum >= 0) and ((minturnnum < 0) or (cardmaxturnnum < minturnnum)):
                    group = []
                    minturnnum = cardmaxturnnum
                if (cardmaxturnnum == minturnnum) and (minturnnum >= 0):
                    group.append(card)
        
        if (minturnnum < 0) or (len(group) == 0):
            return False

        import random
        target = group[random.randint(1, len(group)) - 1]
        
        self.system.yell(self.card, 0, True)
        sublists = ["tinystar"]
        self.system.playeffect("whiteball", sublists, self.card, target)
        self.system.yell(self.card)

        if (minturnnum > 0):
            for buff in target.buffs:
                if buff.filename == "nature_000005":
                    buff.turnleft = -1
        else:
            buff = Buff(self.system, "nature_000005", self.card, target)
            target.add_buff(buff)
            buff.turnleft = -1

        return True
                
    self.onturnstop = onturnstop
