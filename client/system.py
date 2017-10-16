import math

def foundtextcapacity(text_size, area_x, area_y):
    x_num = area_x / text_size
    y_num = area_y / text_size
    text_capacity = math.floor(x_num) * math.floor(y_num)
    return text_capacity

def foundtextsize(text_length, area_x, area_y, dotimes):
    headval = 1
    tailval = min(area_x, area_y)
    
    while True:
        midval = (headval * tailval) ** 0.5
        text_capacity = foundtextcapacity(midval, area_x, area_y)
        if text_capacity > text_length:
            headval = midval
        else:
            tailval = midval
            if dotimes < 0:
                return math.floor(midval)
        dotimes = dotimes - 1

import time
import pygame
from pygame.locals import *

from communicator import *
from client import *
from card import *
from player import *
from label import *
from effect import *

from selector import *
from operatorr import *
from imageloader import *



class System:
    def __init__(self):
        pygame.init()
        
        # 界面设定
        self.screen_length = int(640 * 1.5)
        self.screen_height = int(360 * 1.5)
        self.FPS = 60
        self.screen = pygame.display.set_mode((self.screen_length, self.screen_height), DOUBLEBUF, 32)
        self.clock = pygame.time.Clock()
        self.imageloader = Imageloader(self)
        self.loadimages()
        self.communicator = Communicator(self)
        
        # 初始化需要画的物体
        self.cards = []
        self.cardinfos = []
        self.players = []
        self.playerinfos = []
        self.drawcardinfos = [[[], [], [], [], []], [[], [], [], [], []]]
        self.drawcards = []
        self.floatwords = []
        self.effects = []
        self.label = Label(self)
        self.yellingcard = None
        self.focusingcard = None
        self.hoveringcard = None
        self.descriptingcard = None

        self.drawlock = False
        
        # 操作属性
        self.selector = Selector(self)
        self.operator = Operator(self)

        # 平台设定
        #self.client = Client(self, "192.168.1.128", 51234)
        #self.client = Client(self, "25.61.151.51", 51234)
        self.client = Client(self, "localhost", 51234)
        
    def loadimages(self):
        # 载入字体
        self.font = (pygame.font.Font("fonts/consolab.ttf", 20), pygame.font.Font("fonts/youyuan.ttf", 20))
        self.font_uni = (False, True)

        # 载入图片
        self.cardback = self.imageloader.load("images/pictures/cardback.png", False)
        self.cardtop = self.imageloader.load("images/pictures/cardtop.png", False)
        self.cardcreature = self.imageloader.load("images/pictures/creature.png", False)
        self.cardselect = []
        self.creatureselect = []
        for i in range(3):
            picture = self.imageloader.load("images/pictures/card_select_%d.png" % (i + 1))
            self.cardselect.append(picture)
            picture = self.imageloader.load("images/pictures/creature_select_%d.png" % (i + 1))
            self.creatureselect.append(picture)

        self.ball_attack = self.imageloader.load("images/pictures/ball_attack.png")
        self.ball_health = self.imageloader.load("images/pictures/ball_health.png")
        self.manaballs = []
        self.manaballs_c = []
        self.manaballs_e = []
        self.manacost = []
        for i in range(6):
            picture = self.imageloader.load("images/manaballs/manaball_%d.png" % i)
            self.manaballs.append(picture)
            picture = self.imageloader.load("images/manaballs/manaball_%d_c.png" % i)
            self.manaballs_c.append(picture)
            picture = self.imageloader.load("images/manaballs/manaball_%d_e.png" % i)
            self.manaballs_e.append(picture)
            picture = self.imageloader.load("images/pictures/cost_%d.png" % i)
            self.manacost.append(picture)

    
    # 运行
    def start(self):
        # 启动客户端口
        self.resized()
        self.client.start()
        time_passed = 0
        
        while True:
            
            # 绘画屏幕
            self.draw(time_passed)
            
            # 处理鼠标事件
            for event in pygame.event.get():
                self.deal(event)

            pygame.display.flip()
            
            # 计时
            time_passed = self.clock.tick(self.FPS)

    # 看看有没有新出现的卡
    def update(self):
        length = len(self.cards)
        newcards = []
        while (length < len(self.cardinfos)):
            card = Card(self, self.cardinfos[length])
            self.cards.append(card)
            newcards.append(card)
            length = length + 1

        for card in newcards:
            card.changeplace(card.cardinfo.playerinfo.index, card.cardinfo.place)
        
        length = len(self.players)
        while (length < len(self.playerinfos)):
            self.players.append(Player(self, self.playerinfos[length]))
            length = length + 1

    def resized(self):
        # resize selector
        self.cardselect_resized = []
        self.creatureselect_resized = []
        unit = self.screen_height * 0.2 / 220
        length = int(unit * 260)
        height = int(unit * 400)
        for i in range(3):
            picture = pygame.transform.smoothscale(self.cardselect[i], (length, height))
            self.cardselect_resized.append(picture)
            picture = pygame.transform.smoothscale(self.creatureselect[i], (length, length))
            self.creatureselect_resized.append(picture)
        
        # resize manaballs
        self.resizedmanaballs = []
        self.resizedmanaballs_c = []
        self.resizedmanaballs_e = []
        unit = self.screen_height
        length = int(unit * 0.05)
        
        for colorindex in range(6):
            self.resizedmanaballs.append(pygame.transform.smoothscale(self.manaballs[colorindex], (length, length)))
            self.resizedmanaballs_c.append(pygame.transform.smoothscale(self.manaballs_c[colorindex], (length, length)))
            self.resizedmanaballs_e.append(pygame.transform.smoothscale(self.manaballs_e[colorindex], (length, length)))

        # resize cards
        for card in self.cards:
            if (card.drawindex < 2):
                card.drawindex = 2

        # resize players
        for player in self.players:
            if (player.drawindex < 2):
                player.drawindex = 2

    # 绘画屏幕
    def drawcost(self):

        unit = self.screen_height
        length = int(unit * 0.05)
        y = int(0.95 * unit)
        
        manalength = 0
        for colorindex in range(6):
            manalength = manalength + self.playerinfos[self.index].unusedmana[colorindex]
            manalength = manalength + self.playerinfos[self.index].usedmana[colorindex]
        for colorindex_f in range(5):
            colorindex = 5 - colorindex_f
            for ballindex in range(self.playerinfos[self.index].usedmana[colorindex]):
                manalength = manalength - 1
            manacost = self.operator.costingmana[colorindex - 1]
            for ballindex in range(self.playerinfos[self.index].unusedmana[colorindex]):
                manalength = manalength - 1
                if (manacost > 0):
                    graph = self.resizedmanaballs_c[colorindex]
                    x = int(manalength * length)
                    self.screen.blit(graph, (x, y))
                    manacost = manacost - 1
        for ballindex in range(self.playerinfos[self.index].usedmana[0]):
            manalength = manalength - 1
        for colorindex_f in range(5):
            colorindex = 5 - colorindex_f
            manacost = self.operator.coloringmana[colorindex - 1]
            while manacost > 0:
                manalength = manalength - 1
                graph = self.resizedmanaballs_c[colorindex]
                x = int(manalength * length)
                self.screen.blit(graph, (x, y))
                manacost = manacost - 1

    def change_description(self):
        if (self.descriptingcard):
            self.descriptingcard.final_infoalpha = 0
        if (self.hoveringcard) and (self.hoveringcard.hovertime >= 500) and (self.hoveringcard.showtop()):
            self.descriptingcard = self.hoveringcard
            self.descriptingcard.final_infoalpha = 127
            if (self.operator.operating) and (self.operator.cardusing) and (self.operator.cardusing == self.descriptingcard):
                self.descriptingcard.final_infoalpha = 255
            if (self.operator.operating) and (self.operator.attacking) and (self.operator.attacking == self.descriptingcard):
                self.descriptingcard.final_infoalpha = 255
            if (self.yellingcard) and (self.yellingcard == self.descriptingcard):
                self.descriptingcard.final_infoalpha = 255
            return self.descriptingcard
        if (self.operator.operating) and (self.operator.cardusing):
            self.descriptingcard = self.operator.cardusing
            self.descriptingcard.final_infoalpha = 127
            return self.descriptingcard
        if (self.operator.operating) and (self.operator.attacking):
            self.descriptingcard = self.operator.attacking
            self.descriptingcard.final_infoalpha = 127
            return self.descriptingcard
        if (self.yellingcard):
            self.descriptingcard = self.yellingcard
            self.descriptingcard.final_infoalpha = 127
            return self.descriptingcard
        
    def draw(self, time_passed):
        self.screen.fill((239, 228, 176))
        self.screen.fill((235, 200, 255), pygame.Rect(int(self.screen_length - (self.screen_height * 0.25)), int(self.screen_height * 0.05), int(self.screen_height * 0.25), int(self.screen_height * 0.9)))
        self.change_description()
        for card in self.cards:
            card.drawinfo()

        self.drawcards = []
        for placeindex in (PLACE_FIELD, PLACE_HAND, PLACE_GRAVE, PLACE_DECK, PLACE_VOID):
            for playerindex in range(len(self.drawcardinfos)):
                for cardindex in range(len(self.drawcardinfos[playerindex][placeindex])):
                    cardinfo = self.drawcardinfos[playerindex][placeindex][cardindex]
                    card = cardinfo.card
                    card.update(time_passed)
                    card.draw()
                    self.drawcards.append(card)
                    card.drawlevel = 0

        for player in self.players:
            player.draw()
            player.update(time_passed)
            player.drawlevel = 0

        for effect in self.effects:
            effect.draw()
            effect.update(time_passed)

        for floatword in self.floatwords:
            floatword.draw()
            floatword.update(time_passed)

        if self.operator.operating:
            self.drawcost()
            
        self.label.update(time_passed)
        self.label.draw()

    # 处理鼠标事件
    def deal(self, event):
        for player in self.players:
            player.deal(event)
        cardindex = len(self.drawcards)
        stilldeal = True
        while (cardindex > 0):
            cardindex = cardindex - 1
            if stilldeal:
                stilldeal = self.drawcards[cardindex].deal(event)
            self.drawcards[cardindex].alwaysdeal(event)
        self.label.deal(event)
        if (self.selector.selecting) and (event.type == MOUSEBUTTONDOWN) and (event.button == 3):
            self.select_end()
        if (self.operator.operating) and (not self.operator.attacking) and (not self.operator.cardusing) and (event.type == MOUSEBUTTONDOWN) and (event.button == 3):
            self.operator.nothing()
        if (self.operator.operating) and (self.operator.attacking) and (event.type == MOUSEBUTTONDOWN) and (event.button == 3):
            self.operator.attacktarget(False)
        if (self.operator.operating) and (self.operator.attacking) and (event.type == MOUSEBUTTONUP) and (event.button == 1):
            self.operator.attacktarget(False)
        if (self.operator.operating) and (self.operator.cardusing) and (event.type == MOUSEBUTTONDOWN) and (event.button == 3):
            self.operator.usecard(False)
        if (self.operator.operating) and (self.operator.cardusing) and (event.type == MOUSEBUTTONUP) and (event.button == 1):
            x, y = event.pos
            self.operator.usecard(y < self.screen_height * 0.7)

    # 服务器交流
    def setbaseinfo(self, name, image, deck):
        self.baseinfo = Baseinfo(name, image, deck)

    def makebaseinfomessage(self):
        message = Message(MESSAGE_BASE, self.baseinfo)
        return message

    def dealmessage(self, message):
        if message.typ == MESSAGE_STATE:
            self.acceptstate(message.content)
        if message.typ == MESSAGE_SERVER:
            self.acceptserverinfo(message.content)
        if message.typ == MESSAGE_OPERATE_ASK:
            self.operate_start(message.content)
        if message.typ == MESSAGE_SELECT_ASK:
            # print("SELECT !!!!!")
            self.select_start(message.content)
        if message.typ == MESSAGE_YELL:
            self.acceptyell(message.content)
        if message.typ == MESSAGE_PLAY_EFFECT:
            self.playeffect(message.content)

    def acceptstate(self, state):
        self.playerinfos, self.cardinfos, drawcardinfos = self.communicator.unpackstate(state)

        
        # 为cardinfo分配index
        for cardinfoindex in range(len(self.cardinfos)):
            cardinfo = self.cardinfos[cardinfoindex]
            cardinfo.index = cardinfoindex

        # 为cardinfo分配drawindex
        for playerplacecardinfos in drawcardinfos:
            for placecardinfos in playerplacecardinfos:
                for cardinfoindex in range(len(placecardinfos)):
                    cardinfo = placecardinfos[cardinfoindex]
                    cardinfo.drawindex = cardinfoindex

        self.drawlock == True
        
        # 更变玩家的信息
        for index in range(len(self.players)):
            player = self.players[index]
            playerinfo = self.playerinfos[index]
            player.changeinfo(playerinfo)

        # 更变卡片的信息
        for index in range(len(self.cards)):
            card = self.cards[index]
            cardinfo = self.cardinfos[index]
            card.changeinfo(cardinfo)

        self.drawcardinfos = drawcardinfos
        self.update()

        self.drawlock == False

    def acceptserverinfo(self, serverinfo):
        self.index = serverinfo.index

    def select_start(self, selection_ask):
        self.label.final_alpha = 191
        self.selector.new(selection_ask)
        
    def select_end(self):
        selection = self.selector.finish()
        if selection:
            message = Message(MESSAGE_SELECT, selection)
            self.client.send(message)
            self.label.final_alpha = 0

    def operate_start(self, operation_ask):
        self.label.final_alpha = 191
        self.operator.new(operation_ask)

    def operate_end(self, operation):
        if operation:
            message = Message(MESSAGE_OPERATE, operation)
            self.client.send(message)
            self.label.final_alpha = 0

    def acceptyell(self, yellobj):
        cardindex = yellobj.cardindex
        self.yellingcard = self.cards[cardindex]

    def playeffect(self, effectobj):
        filename = effectobj.filename
        subfilenames = effectobj.subfilenames
        startindex = effectobj.startindex
        starttyp = effectobj.starttyp
        finalindex = effectobj.finalindex
        finaltyp = effectobj.finaltyp
        time = effectobj.time
        mask = effectobj.mask

        if starttyp == 0:
            startobj = None
            unit = self.screen_height
            sx = int(self.screen_length - (unit * (0.025 + 0.2 - 0.1)))
            sy = int(unit * (0.05 + 0.025 + (0.2 / 220 * 140)))
        if starttyp == 1:
            startobj = self.cards[startindex]
            cw, ch = startobj.getabssize()
            sx = startobj.x + (cw / 2)
            sy = startobj.y + (ch / 2)
        if starttyp == 2:
            startobj = self.players[startindex]
            cw = self.screen_height * 0.2
            ch = cw
            sx = startobj.x + (cw / 2)
            sy = startobj.y + (ch / 2)
            
        if finaltyp == 0:
            finalobj = None
            unit = self.screen_height
            ex = int(self.screen_length - (unit * (0.025 + 0.2 - 0.1)))
            ey = int(unit * (0.05 + 0.025 + (0.2 / 220 * 140)))
        if finaltyp == 1:
            finalobj = self.cards[finalindex]
            cw, ch = finalobj.getabssize()
            ex = finalobj.final_x + (cw / 2)
            ey = finalobj.final_y + (ch / 2)
        if finaltyp == 2:
            finalobj = self.players[finalindex]
            cw = self.screen_height * 0.2
            ch = cw
            ex = finalobj.x + (cw / 2)
            ey = finalobj.y + (ch / 2)

        Effect(self, filename, subfilenames, time, (sx, sy), (ex, ey), finalobj, mask)
                    

if __name__ == "__main__":
    
    system = System()
    system.setbaseinfo("刘乘铭", 0, [0, 2, 0, 2, 0, 2, 0, 2, 0, 2])
    system.start()

        
