from const import *

class Player:
    def __init__(self, system, index, baseinfo):
        self.system = system
        self.index = index
        self.name = baseinfo.name
        self.image = baseinfo.image
        self.alive = True
        self.health = 30
        self.maxhealth = 30

        self.manaballs = []
        
        self.build_deck(baseinfo.deck)

    def get_order(self):
        for i in range(len(self.system.players)):
            if self == self.system.players[i]:
                return i
        return -1

    def build_deck(self, li):
        for number in li:
            card = Card(self.system, number, True, self)
            card.place = PLACE_DECK
            self.system.cards.append(card)
    
    def select(self, group, number, text, must, inplace, buff):
        
        # 发送场上目前的状态
        self.system.sendstate()
        
        # 发送选择请求
        selection_ask = self.system.communicator.packselection_ask(group, number, text, must, inplace)
        message = Message(MESSAGE_SELECT_ASK, selection_ask)
        self.system.server.sendfunc(message, self.index)
 
        # 使服务器等待
        self.system.server.askfunc(self.index, MESSAGE_SELECT)

        # 获取选择信息
        message = self.system.server.lastmessage

        # 解包信息
        selection = message.content
        group = self.system.communicator.unpackselection(selection)
        

        # 创建伪事件
        param = [self, group]
        event = Event(self.system, EVENT_PLAYERSELECT, buff, param)
        self.system.add_event_now(event)
        
        # 返回
        return group

    def operate(self, canattack, usecards, attackers, targets):
        
        # 发送场上目前的状态
        self.system.sendstate()
        
        # 发送选择请求
        operation_ask = self.system.communicator.packoperation_ask(canattack, usecards, attackers, targets)
        message = Message(MESSAGE_OPERATE_ASK, operation_ask)
        self.system.server.sendfunc(message, self.index)

        # 使服务器等待
        self.system.server.askfunc(self.index, MESSAGE_OPERATE)

        # 获取选择信息
        message = self.system.server.lastmessage

        # 解包信息并返回
        operation = message.content
        typ, param = self.system.communicator.unpackoperation(operation)
        return typ, param

    def getallmana(self):
        ans = [0, 0, 0, 0, 0, 0]
        for manaball in self.manaballs:
            ans[manaball.color] = ans[manaball.color] + 1
        return ans
    
    def getmana(self):
        ans = [0, 0, 0, 0, 0, 0]
        for manaball in self.manaballs:
            if (manaball.used == False):
                ans[manaball.color] = ans[manaball.color] + 1
        return ans

    def hasmana(self, cost):
        delta = [0, 0, 0, 0, 0, 0]
        mana  = self.getmana()
        for i in range(6):
            delta[i] = mana[i] - cost[i]
            if (i > 0) and (delta[i] < 0):
                delta[0] = delta[0] + delta[i]
                delta[i] = 0
        return delta[0] >= 0

    def sortmanaballs(self):
        newmanaballs = []
        for colorindex in range(6):
            for manaball in self.manaballs:
                if manaball.color == colorindex:
                    newmanaballs.append(manaball)
        self.manaballs = newmanaballs

    def lose(self):
        self.alive = False
        return True
    

from card import *
from event import *
from communicator import *
