from const import *
from event import *


        

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.name = "森林"
    self.description = "你每消耗1点法力, 回复1点生命值。你的回合开始时治疗所有友方生物。"


    def oncostmana(self, old_event):
        if (self.card.player != old_event.param[0]) or (self.card.place != PLACE_FIELD):
            return False

        costsum = 0
        cost = old_event.param[1]
        for colorindex in range(6):
            costsum = costsum + cost[colorindex]
            
        if costsum == 0:
            return False

        self.system.yell(self.card, 0, True)
        sublists = ["tinyleaf_1", "tinyleaf_2", "tinyleaf_3"]
        self.system.playeffect("greenlight", sublists, self.card, self.card.player)
        self.system.yell(self.card, 1)

        param = [[self.card.player], self.card, [costsum]]
        event = Event(self.system, EVENT_HEAL, self, param)
        event.do()
        
        return True
        
    self.oncostmana = oncostmana

    
    def onturnstart(self, old_event):
        if (self.card.player != old_event.param[0]) or (self.card.place != PLACE_FIELD):
            return False

        group = []
        amount = []
        for card in self.system.cards:
            if (card.player == self.card.player) and (card.place == PLACE_FIELD) and (card.health < card.maxhealth):
                group.append(card)
                amount.append(card.maxhealth - card.health)

        if len(group) <= 0:
            return False

        self.system.yell(self.card, 0, True)
        sublists = ["tinyleaf_1", "tinyleaf_2", "tinyleaf_3"]
        for card in group:
            self.system.playeffect("greenlight", sublists, self.card, card)
        self.system.yell(self.card, 1)
        
        param = [group, self.card, amount]
        event = Event(self.system, EVENT_HEAL, self, param)
        event.do()
        
    self.onturnstart = onturnstart
