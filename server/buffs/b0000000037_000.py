from const import *
from event import *
from card import *

def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "生根"
    self.description = "使用: 获得一个空的白色法力水晶。"
    def after_usecard(self, old_event):
        if not old_event.param[0] == self.card:
            return False

        self.system.yell(self.card, 0, True)
        sublists = ["tinyleaf_1", "tinyleaf_2", "tinyleaf_3"]
        self.system.playeffect("greenlight", sublists, None, None)
        self.system.yell(self.card, 1)
        
        param = [self.card.player, 1, -1, 0, 2, 0]
        event = Event(self.system, EVENT_CHANGEMANA, self, param)
        event.do()
        
        return False
    self.after_usecard = after_usecard
