from const import *
from event import *
from card import *


def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "占卜"
    self.description = "使用: 抽两张牌。"
    
    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False
        
        self.system.yell(self.card, 0, True)
        sublists = ["tinystar"]
        self.system.playeffect("bluelight", sublists, None, None)
        self.system.yell(self.card, 1)
        
        param = [self.card.player]
        event = Event(self.system, EVENT_DRAW, self, param)
        event.do()
        
        param = [self.card.player]
        event = Event(self.system, EVENT_DRAW, self, param)
        event.do()
    self.after_usecard = after_usecard
