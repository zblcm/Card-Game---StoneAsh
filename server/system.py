class Turn:
    def __init__(self, system, player):
        self.system = system
        self.player = player
        self.events = []

        # 恢复魔法球
        param = [player, -1, -2, -2, 0, 1]
        event = Event(system, EVENT_CHANGEMANA, None, param)
        self.events.append(event)

        # 添加新的白色魔法球
        param = [player, 1, -1, 0, 100, 1]
        event = Event(system, EVENT_CHANGEMANA, None, param)
        self.events.append(event)

        # 抽卡
        param = [player]
        event = Event(system, EVENT_DRAW, None, param)
        self.events.append(event)
        
        # 回合开始
        param = [player]
        event = Event(system, EVENT_TURNSTART, None, param)
        self.events.append(event)
        
        # 玩家行动
        param = [player, True]
        event = Event(system, EVENT_PLAYEROPERATION, None, param)
        self.events.append(event)


class System:
    def __init__(self, server, baseinfos):
        self.server = server
        self.communicator = Communicator(self)
        self.cards = []

        # 初始化玩家信息
        self.players = []
        playerindex = 0
        for baseinfo in baseinfos:
            player = Player(self, playerindex, baseinfo)
            self.players.append(player)
            # 告诉玩家他的index
            serverinfo = Serverinfo(playerindex)
            message = Message(MESSAGE_SERVER, serverinfo)
            self.server.sendfunc(message, playerindex)
            playerindex = playerindex+ 1

        # 创建全卡表
        self.allcards = []
        for i in range(63):
            self.allcards.append(Card(self, i, False))

        # 创造第一个回合
        self.turns = [Turn(self, self.players[0])]

        param = [self.players[0]]
        self.add_event(Event(self, EVENT_DRAW, None, param), 0, 2)
        self.add_event(Event(self, EVENT_DRAW, None, param), 0, 2)
        self.add_event(Event(self, EVENT_DRAW, None, param), 0, 2)
        self.add_event(Event(self, EVENT_DRAW, None, param), 0, 2)
        
        param = [self.players[1]]
        self.add_event(Event(self, EVENT_DRAW, None, param), 0, 2)
        self.add_event(Event(self, EVENT_DRAW, None, param), 0, 2)
        self.add_event(Event(self, EVENT_DRAW, None, param), 0, 2)
        self.add_event(Event(self, EVENT_DRAW, None, param), 0, 2)
        self.add_event(Event(self, EVENT_DRAW, None, param), 0, 2)

    # Game precoss function

    def over(self):
        i = 0
        for player in self.players:
            if player.alive:
                i = i + 1
        if i < 2:
            return True
        return False

    def start(self):
        self.player = self.players[-1]
        self.turn_index = 0
        self.event_index = 0

        # 全局循环
        while (not self.over()):
            # 回合循环
            while (not self.over()) and (self.event_index < len(self.turns[self.turn_index].events)):
                # 执行事件
                self.do_event_now()
                self.event_index = self.event_index + 1
            self.turn_index = self.turn_index + 1
            self.event_index = 0
            while (self.turn_index >= len(self.turns)):
                self.append_turn()
        print("end.")
        self.sendstate()

    def yell(self, card, yelltime = 1, sendstate = False):
        if sendstate:
            self.sendstate()
        
        cardindex = self.cards.index(card)
        yellobj = Yell(cardindex)
        message = Message(MESSAGE_YELL, yellobj)
        for player in self.players:
            self.server.sendfunc(message, player.index)
        time.sleep(yelltime * 0.5)

    def playeffect(self, filename, subfilenames, launcher, reciever, time = 1, mask = None):

        startindex = 0
        starttyp = 0
        if launcher in self.cards:
            startindex = self.cards.index(launcher)
            starttyp = 1
        if launcher in self.players:
            startindex = self.players.index(launcher)
            starttyp = 2
        
        finalindex = 0
        finaltyp = 0
        if reciever in self.cards:
            finalindex = self.cards.index(reciever)
            finaltyp = 1
        if reciever in self.players:
            finalindex = self.players.index(reciever)
            finaltyp = 2
            
        effectobj = Playeffect(filename, subfilenames, startindex, starttyp, finalindex, finaltyp, time * 0.5, mask)
        message = Message(MESSAGE_PLAY_EFFECT, effectobj)
        for player in self.players:
            self.server.sendfunc(message, player.index)

    def sendstate(self):
        state = self.communicator.packstate()
        message = Message(MESSAGE_STATE, state)
        for playerindex in range(len(self.players)):
            self.server.sendfunc(message, playerindex)

    # Event function

    def get_now_index(self):
        return self.turn_index, self.event_index
    
    def add_event(self, event, turn_index, event_index):
        self.turns[turn_index].events.insert(event_index, event)
    
    def add_event_now(self, event, later = None):
        # print("debug: event adding, typ:%d, priority:%d" % (event.typ, event.priority))
        events = self.turns[self.turn_index].events
        if later:
            lateindex = later.get_index()
        event_index = self.event_index + 1
        while (event_index < len(events)):
            if (event.priority > events[event_index].priority) or (later and (laterindex <= event_index)):
                event_index = event_index + 1
            else:
                self.add_event(event, self.turn_index, event_index)
                return True
        self.add_event(event, self.turn_index, event_index)
        return False

    def do_event(self, turn_index, event_index):
        return self.turns[turn_index].events[event_index].do()

    def do_event_now(self):
        return self.do_event(self.turn_index, self.event_index)

    def append_turn(self):
        turn = Turn(self, self.players[(self.turns[-1].player.index + 1) % len(self.players)])
        self.turns.append(turn)

    def get_current_turn(self):
        return self.turns[self.turn_index]

from const import *
from event import *
from player import *
from communicator import *
import time

if __name__ == "__main__":

    from communicator import *
    base1 = Baseinfo("Apple", [0, 2, 0, 2, 0, 2, 0, 2, 0, 2])
    base2 = Baseinfo("Chloe", [0, 2, 0, 2, 0, 2, 0, 2, 0, 2])
    system = System(None, [base1, base2])
    system.start()
    
