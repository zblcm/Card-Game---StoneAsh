from card import *
from player import *
from communicator import *

class Operator:
    def __init__(self, system):
        self.system = system
        self.operating = False
        self.cardusing = False
        self.attacking = False

        self.costingmana = [0, 0, 0, 0, 0]
        self.coloringmana = [0, 0, 0, 0, 0]

    def new(self, operation_ask):
        self.operating = True
        self.canattack = operation_ask.canattack
        self.usecardindexs = operation_ask.usecardindexs
        self.attackerindexs = operation_ask.attackerindexs
        self.targetindexs = operation_ask.targetindexs
        self.targetplayerindexs = operation_ask.targetplayerindexs

        self.canattack = self.canattack and (len(self.attackerindexs) > 0) and (len(self.targetindexs) + len(self.targetplayerindexs) > 0)
        self.canusecard = (len(self.usecardindexs) > 0)

        self.attackerindex = None
        self.targetindex = None
        self.hastarget = 0

        self.reoperate()

    def reoperate(self):
        self.cardusing = False
        self.attacking = False
        for cardindex in self.usecardindexs:
            self.system.cards[cardindex].selected = 1
        for cardindex in self.attackerindexs:
            self.system.cards[cardindex].selected = 1
            
        for playerindex in self.targetplayerindexs:
            self.system.players[playerindex].selected = 0
        for cardindex in self.targetindexs:
            self.system.cards[cardindex].selected = 0

        if self.canattack or self.canusecard:
            self.system.label.set_text("请拖动卡片来使用手牌或进行攻击。右键单击来结束回合/取消操作。")
        else:
            self.system.label.set_text("你什么都没法做。右键单击来结束回合/取消操作。")

    def presstarget(self, attacker):
        if isinstance(attacker, Player):
            return False
        
        if (attacker.cardinfo.index in self.usecardindexs):
            self.cardusing = attacker
            for cardindex in self.usecardindexs:
                self.system.cards[cardindex].selected = 0
            for cardindex in self.attackerindexs:
                self.system.cards[cardindex].selected = 0
            attacker.final_mask = [127, 191, 255, 191]
            #attacker.final_y = attacker.final_y - (0.2 * self.system.screen_height)
            #attacker.focusing = False
            self.system.label.set_text("将鼠标拖出手牌区域来使用。")
            
            costingmana = [0, 0, 0, 0, 0]
            coloringmana = [0, 0, 0, 0, 0]
            manacost = attacker.cardinfo.cost
            for i in range(5):
                costingmana[i] = manacost[i + 1]
                manadelta = costingmana[i] - self.system.playerinfos[self.system.index].unusedmana[i + 1]
                if manadelta > 0:
                    coloringmana[i] = manadelta
            self.costingmana = costingmana
            self.coloringmana = coloringmana
                
            return True
        
        if (attacker.cardinfo.index in self.attackerindexs):
            self.attacking = attacker
            for cardindex in self.usecardindexs:
                self.system.cards[cardindex].selected = 0
            for cardindex in self.attackerindexs:
                self.system.cards[cardindex].selected = 0
            for playerindex in self.targetplayerindexs:
                self.system.players[playerindex].selected = 1
            for cardindex in self.targetindexs:
                self.system.cards[cardindex].selected = 1
            attacker.final_mask = [255, 0, 0, 127]
            self.system.label.set_text("将鼠标拖至目标单位上来攻击。")
            return True
        
        return False
    
    def attacktarget(self, target):
        if not target:
            self.attacking.final_mask = [0, 0, 0, 0]
            return self.reoperate()
        self.hastarget = 0
        
        if isinstance(target, Player):
            if not (target.playerinfo.index in self.targetplayerindexs):
                self.attacking.final_mask = [0, 0, 0, 0]
                return self.reoperate()
            self.hastarget = 1
            self.targetindex = target.playerinfo.index
            
        if isinstance(target, Card):
            if not (target.cardinfo.index in self.targetindexs):
                self.attacking.final_mask = [0, 0, 0, 0]
                return self.reoperate()
            self.hastarget = 2
            self.targetindex = target.cardinfo.index
            
        if self.hastarget > 0:
            self.attackerindex = self.attacking.cardinfo.index
            self.typ = 2
            self.finish()
            return True

        return self.reoperate()

    def usecard(self, succeed):
        if not succeed:
            self.cardusing.final_mask = [0, 0, 0, 0]
            self.cardusing.drawlevel = 1
            self.costingmana = [0, 0, 0, 0, 0]
            self.coloringmana = [0, 0, 0, 0, 0]
            return self.reoperate()
        self.hastarget = 0
        self.attackerindex = self.cardusing.cardinfo.index
        self.targetindex = 0
        self.typ = 1
        self.finish()

    def nothing(self):
        self.hastarget = 0
        self.attackerindex = 0
        self.targetindex = 0
        self.typ = 0
        self.finish()

    def finish(self):
        self.operating = False
        if self.cardusing:
            #self.cardusing.final_mask = [0, 0, 0, 0]
            #self.cardusing.drawlevel = 1
            self.costingmana = [0, 0, 0, 0, 0]
            self.coloringmana = [0, 0, 0, 0, 0]
            self.cardusing = False
        if self.attacking:
            self.costingmana = [0, 0, 0, 0, 0]
            self.coloringmana = [0, 0, 0, 0, 0]
            self.attacking.final_mask = [0, 0, 0, 0]
            self.attacking = False
        
        for cardindex in self.usecardindexs:
            self.system.cards[cardindex].selected = 0
        for cardindex in self.attackerindexs:
            self.system.cards[cardindex].selected = 0
        for playerindex in self.targetplayerindexs:
            self.system.players[playerindex].selected = 0
        for cardindex in self.targetindexs:
            self.system.cards[cardindex].selected = 0
        operation = Operation(self.typ, self.attackerindex, self.targetindex, self.hastarget)
        self.system.operate_end(operation)
        
