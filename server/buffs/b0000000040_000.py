from const import *
from event import *
from card import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "孢子侵渗"
    self.description = "使用: 获得两个新的绿色法力水晶。"
    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False

        self.system.yell(self.card, 0, True)
        sublists = ["tinyleaf_1", "tinyleaf_2", "tinyleaf_3"]
        self.system.playeffect("greenlight", sublists, None, None)
        self.system.yell(self.card, 1)
        
        param = [self.card.player, 2, -1, 3, 2, 1]
        event = Event(self.system, EVENT_CHANGEMANA, self, param)
        event.do()
        
        return False
    self.after_usecard = after_usecard
