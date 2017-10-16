from card import *
from player import *
from communicator import *

class Selector:
    def __init__(self, system):
        self.system = system
        self.selecting = False

    def new(self, selection_ask):
        self.selecting = True
        
        self.playerindexs = selection_ask.playerindexs
        self.cardindexs = selection_ask.cardindexs
        self.number = selection_ask.number
        self.text = selection_ask.text
        self.must = selection_ask.must
        self.inplace = selection_ask.inplace
        
        self.confirmplayerindexs = []
        self.confirmcardindexs = []
        self.confirmnumber = 0

        for playerindex in self.playerindexs:
            self.system.players[playerindex].selected = 1
        for cardindex in self.cardindexs:
            card = self.system.cards[cardindex]
            card.selected = 1
            card.seen = True
            
        self.system.label.set_text(self.text)

    def clicktarget(self, target):
        if self.system.label.text != self.text:
            self.system.label.set_text(self.text)
        if isinstance(target, Player):
            if not (target.playerinfo.index in self.playerindexs):
                return False
            if (target.playerinfo.index in self.confirmplayerindexs):
                print("取消了一个角色")
                self.confirmplayerindexs.remove(target.playerinfo.index)
                self.confirmnumber = self.confirmnumber - 1
                target.selected = 1
            else:
                print("选择了一个角色")
                self.confirmplayerindexs.append(target.playerinfo.index)
                self.confirmnumber = self.confirmnumber + 1
                target.selected = 2
        if isinstance(target, Card):
            if not (target.cardinfo.index in self.cardindexs):
                return False
            if (target.cardinfo.index in self.confirmcardindexs):
                print("取消了一个角色")
                self.confirmcardindexs.remove(target.cardinfo.index)
                self.confirmnumber = self.confirmnumber - 1
                target.selected = 1
            else:
                print("选择了一个角色")
                self.confirmcardindexs.append(target.cardinfo.index)
                self.confirmnumber = self.confirmnumber + 1
                target.selected = 2

    def finish(self):
        
        if (self.must == -1) and (self.confirmnumber < self.number):
            self.system.label.set_text("你必须选择至少%d个角色 !!!" % self.number)
            return False
        if (self.must == 0) and (self.confirmnumber != self.number):
            self.system.label.set_text("你必须选择%d个角色 !!!" % self.number)
            return False
        if (self.must == 1) and (self.confirmnumber > self.number):
            self.system.label.set_text("你最多选择%d个角色 !!!" % self.number)
            return False
        
        self.selecting = False

        for playerindex in self.playerindexs:
            self.system.players[playerindex].selected = 0
        for cardindex in self.cardindexs:
            card = self.system.cards[cardindex]
            card.selected = 0
            card.seen = False
        
        selection = Selection(self.confirmplayerindexs, self.confirmcardindexs)
        return selection

        
