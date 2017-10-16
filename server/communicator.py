from const import *

class Communicator:
    def __init__(self, system):
        self.system = system

    # 服务端函数
    def packstate(self):
        # pack player
        playerinfos = []
        for index in range(len(self.system.players)):
            player = self.system.players[index]
            playerinfos.append(Playerinfo(player))

        # pack card
        cardinfos = []
        for index in range(len(self.system.cards)):
            card = self.system.cards[index]
            playerinfo = card.player.info
            if card.source:
                sourceinfo = card.source.info
            else:
                sourceinfo = None
            cardinfos.append(Cardinfo(card, playerinfo, sourceinfo))

        # pack buff
        for index_c in range(len(self.system.cards)):
            card = self.system.cards[index_c]
            for index_b in range(len(card.buffs)):
                buff = card.buffs[index_b]
                cardinfo = buff.card.info
                if buff.source:
                    sourceinfo = buff.source.info
                else:
                    sourceinfo = None
                cardinfo.buffinfos.append(Buffinfo(buff, cardinfo, sourceinfo))

        state = State(playerinfos, cardinfos)
        self.laststate = state

        return state

    def packoperation_ask(self, canattack, usecards, attackers, targets):
        usecardindexs = []
        attackerindexs = []
        targetindexs = []
        targetplayerindexs = []
        
        for cardindex in range(len(self.system.cards)):
            card = self.system.cards[cardindex]
            
            if card in usecards:
                usecardindexs.append(cardindex)
            if card in attackers:
                attackerindexs.append(cardindex)
            if card in targets:
                targetindexs.append(cardindex)

        for playerindex in range(len(self.system.players)):
            player = self.system.players[playerindex]
            if player in targets:
                targetplayerindexs.append(playerindex)
                
        operation_ask = Operation_ask(canattack, usecardindexs, attackerindexs, targetindexs, targetplayerindexs)
        return operation_ask

    def packselection_ask(self, group, number, text, must, inplace):
        # pack group
        playerindexs = []
        for playerindex in range(len(self.system.players)):
            player = self.system.players[playerindex]
            if (player in group):
                playerindexs.append(playerindex)
                
        cardindexs = []
        for cardindex in range(len(self.system.cards)):
            card = self.system.cards[cardindex]
            if (card in group):
                cardindexs.append(cardindex)

        selection_ask = Selection_ask(playerindexs, cardindexs, number, text, must, inplace)
        return selection_ask

    def unpackoperation(self, operation):
        param = []
        if (operation.typ != 0):
            attacker = self.system.cards[operation.attackerindex]
            param.append(attacker)

        if (operation.hastarget == 0):
            param.append(False)
        if (operation.hastarget == 1):
            target = self.system.players[operation.targetindex]
            param.append(target)
        if (operation.hastarget == 2):
            target = self.system.cards[operation.targetindex]
            param.append(target)
        
        return operation.typ, param

    def unpackselection(self, selection):
        group = []
        for playerindex in selection.playerindexs:
            group.append(self.system.players[playerindex])
        for cardindex in selection.cardindexs:
            group.append(self.system.cards[cardindex])
        return group

    # 客户端函数
    def unpackstate(self, state):
        playerinfos = state.playerinfos
        drawcardinfos = []
        for playerinfo in playerinfos:
            drawcardinfos.append([[], [], [], [], []])
        for cardinfo in state.cardinfos:
            drawcardinfos[cardinfo.playerinfo.index][cardinfo.place].append(cardinfo)
        return state.playerinfos, state.cardinfos, drawcardinfos

# 传输的命令
class Message:
    def __init__(self, typ, content):
        self.typ = typ
        self.content = content        

# 传输的命令种类
class Baseinfo:
    def __init__(self, name, image, deck):
        self.name = name
        self.image = image
        self.deck = deck
        
class Serverinfo:
    def __init__(self, index):
        self.index = index

class State:
    def __init__(self, playerinfos, cardinfos):
        self.playerinfos = playerinfos
        self.cardinfos = cardinfos

class Operation:
    def __init__(self, typ, attackerindex, targetindex, hastarget):
        self.typ = typ # 0:nothing 1:usecard 2:attack
        self.attackerindex = attackerindex
        self.targetindex = targetindex
        self.hastarget = hastarget # 0:none 1:player 2:creature

class Selection:
    def __init__(self, playerindexs, cardindexs):
        self.playerindexs = playerindexs
        self.cardindexs = cardindexs

class Operation_ask:
    def __init__(self, canattack, usecardindexs, attackerindexs, targetindexs, targetplayerindexs):
        self.canattack = canattack
        self.usecardindexs = usecardindexs
        self.attackerindexs = attackerindexs
        self.targetindexs = targetindexs
        self.targetplayerindexs = targetplayerindexs

class Selection_ask:
    def __init__(self, playerindexs, cardindexs, number, text, must, inplace):
        self.playerindexs = playerindexs
        self.cardindexs = cardindexs
        self.number = number
        self.text = text
        self.must = must
        self.inplace = inplace

class Yell:
    def __init__(self, cardindex):
        self.cardindex = cardindex

class Playeffect:
    def __init__(self, filename, subfilenames, startindex, starttyp, finalindex, finaltyp, time = 1, mask = None):
        self.filename =  filename
        self.subfilenames = subfilenames
        self.startindex = startindex
        self.starttyp = starttyp
        self.finalindex = finalindex
        self.finaltyp = finaltyp
        self.time = time
        self.mask = mask

# 传输的物体
class Playerinfo:
    def __init__(self, player):
        player.info = self

        self.index = player.index
        self.image = player.image
        self.name = player.name
        self.health = player.health
        self.alive = player.alive
        
        self.unusedmana = [0, 0, 0, 0, 0, 0]
        self.usedmana = [0, 0, 0, 0, 0, 0]
        for manaball in player.manaballs:
            if manaball.used:
                self.usedmana[manaball.color] = self.usedmana[manaball.color] + 1
            else:
                self.unusedmana[manaball.color] = self.unusedmana[manaball.color] + 1
        

class Cardinfo:
    def __init__(self, card, playerinfo, sourceinfo):
        card.info = self
        self.playerinfo = playerinfo
        self.sourceinfo = sourceinfo
        self.buffinfos = []
        self.name = card.name
        self.description = card.description
        self.number = card.number
        self.place = card.place
        self.typ = card.typ
        self.subtype = card.subtype
        self.originalcost = card.originalcost
        self.cost = card.cost
        if card.typ == CARD_CREATURE:
            self.maxhealth = card.maxhealth
            self.health = card.health
            self.attack = card.attack
            self.canattack = (card.maxattacktime > card.attacktime)

class Buffinfo:
    def __init__(self, buff, cardinfo, sourceinfo):
        self.filename = buff.filename
        self.name = buff.name
        self.description = buff.description
        self.image = buff.image
        self.imageinside = buff.imageinside
        self.cardinfo = cardinfo
        self.sourceinfo = sourceinfo

        self.typ = buff.typ
        self.visable = buff.visable
