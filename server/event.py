from const import *
from random import *
from manaball import *

class Event:
    def __init__(self, system, typ, buff, param):
        self.system = system
        self.typ = typ
        self.buff = buff
        self.param = param
        self.lastevent = None
        self.set_priority()

    def copy(self):
        return Event(self.system, self.typ, self.buff, self.param)

    def get_index(self):
        turn, index = self.get_order
        return index
    
    def get_order(self):
        for turn in range(len(self.system.events)):
            index = self.get_turn_order(turn)
            if index > -1:
                return turn, index
        return -1, -1

    def get_turn_order(self, turn):
        # can be better if it is another language
        for index in range(len(self.system.events[turn])):
            if self.system.events[turn][index] == self:
                return index
        return -1

    def set_priority(self):
        
        if self.typ == EVENT_LOSE:
            self.priority = 0
        if self.typ == EVENT_PLAYEROPERATION:
            self.priority = 12
        if self.typ == EVENT_CHANGEMANA:
            self.priority = 5
        if self.typ == EVENT_JUMPTURN:
            self.priority = 11
        if self.typ == EVENT_PLAYERSELECT:
            self.priority = 3
        
        if self.typ == EVENT_TURNSTART:
            self.priority = 1
        if self.typ == EVENT_TURNOVER:
            self.priority = 13
        if self.typ == EVENT_MOVE:
            self.priority = 4
        if self.typ == EVENT_DRAW:
            self.priority = 8
        if self.typ == EVENT_DAMAGE:
            self.priority = 6
        if self.typ == EVENT_KILL:
            self.priority = 7
        if self.typ == EVENT_USECARD:
            self.priority = 10
        if self.typ == EVENT_ATTACK:
            self.priority = 9
        if self.typ == EVENT_COSTMANA:
            self.priority = 2
        if self.typ == EVENT_HEAL:
            self.priority = 6
            

    def do(self):
        print("Event do: %d %d, type %d" % (self.system.turn_index, self.system.event_index, self.typ))

        if self.typ == EVENT_LOSE:
            return self.lose()
        if self.typ == EVENT_PLAYEROPERATION:
            return self.playeroperation()
        if self.typ == EVENT_CHANGEMANA:
            return self.changemana()
        #if self.typ == EVENT_JUMPTURN:
        #    return self.jumpturn()
        if self.typ == EVENT_PLAYERSELECT:
            return self.playerselect()
        
        if self.typ == EVENT_TURNSTART:
            return self.turnstart()
        if self.typ == EVENT_TURNOVER:
            return self.turnstop()
        if self.typ == EVENT_MOVE:
            return self.move()
        if self.typ == EVENT_DRAW:
            return self.draw()
        if self.typ == EVENT_DAMAGE:
            return self.damage()
        if self.typ == EVENT_KILL:
            return self.kill()
        if self.typ == EVENT_USECARD:
            return self.usecard()
        if self.typ == EVENT_ATTACK:
            return self.attack()
        if self.typ == EVENT_COSTMANA:
            return self.costmana()
        if self.typ == EVENT_HEAL:
            return self.heal()

    # Actual event function. The return value means if the event is succeed.
    def lose(self):
        # param: players.
        players = self.param[0]
        for player in players:
            print("有玩家死亡了。")
            player.lose()
        return True
    
    def playeroperation(self):
        # param: player.
        player = self.param[0]
        canattack = self.param[1]

        # 获取可能的攻击者和攻击单位的信息
        attackers = []
        targets = []
        taughter = []
        if canattack:
            for card in self.system.cards:
                if (card.place == PLACE_FIELD) and (card.player == player) and (card.attacktime < card.maxattacktime) and (card.cannotattack(card) == False):
                    attackers.append(card)
                if (card.place == PLACE_FIELD) and (card.player != player) and (card.unattackable(card) == False):
                    targets.append(card)
                    taught = False
                    for buff in card.buffs:
                        if buff.flag_taught:
                            taught = True
                    if taught:
                        taughter.append(card)
            for tplayer in self.system.players:
                if (tplayer.alive) and (tplayer != player):
                    targets.append(tplayer)
            if len(taughter) > 0:
                targets = taughter

        # 获取可以使用的卡牌
        usecards = []
        for card in self.system.cards:
            if (card.place == PLACE_HAND) and (card.player == player) and (player.hasmana(card.cost)) and (card.unusable(card) == False):
                usecards.append(card)
        
        # 询问玩家需要做什么
        typ, param = player.operate(canattack, usecards, attackers, targets)

        # 添加攻击事件
        if (typ == 2):
            attacker = param[0]
            target = param[1]
            # 添加攻击事件
            parame = [attacker, target]
            event = Event(self.system, EVENT_ATTACK, None, parame)
            self.system.add_event_now(event)

        # 添加使用卡片的事件
        if (typ == 1):
            card = param[0]
            target = param[1]
            parame = [card, target, True, True]
            event = Event(self.system, EVENT_USECARD, None, parame)
            self.system.add_event_now(event)

        # 添加下个询问玩家的事件
        if (typ != 0) or (player != self.system.get_current_turn().player):
            parame = [self.system.get_current_turn().player, True]
            event = Event(self.system, EVENT_PLAYEROPERATION, None, parame)
            self.system.add_event_now(event)
        # 添加回合结束的事件
        else:
            parame = [self.system.get_current_turn().player]
            event = Event(self.system, EVENT_TURNOVER, None, parame)
            self.system.add_event_now(event)

        return False
    
    def changemana(self):
        # param: player, number, old_color, new_color, old_status, new_status.
        # number: -1:infiniey
        # old_color: 0:white -1:void -2:any
        # new_color: 0:white -1:void -2:unchanged
        # old_status: 0:used 1:unused 2:any
        # new_status: 0:used 1:unused 2:unchanged
        
        player = self.param[0]
        number = self.param[1]
        old_color = self.param[2]
        new_color = self.param[3]
        old_status = self.param[4]
        new_status = self.param[5]

        # 检查条件
        if number == 0:
            return False
        if (old_color == -1) and (new_color == -1):
            return False
        if (old_color == -1) and (number < 0):
            return False

        # 选取符合条件的魔法球
        group = []
        for manaball in player.manaballs:
            if ((old_color == -2) or (old_color == manaball.color)):
                if (old_status == 2) or ((old_status == 0) and (manaball.used)) or ((old_status == 1) and not (manaball.used)):
                    group.append(manaball)

        # 检查条件 - 魔法球数目
        if (old_color != -1) and (len(group) <= 0):
            return False
        if (old_color != -1) and ((number > len(group)) or (number < 0)):
            number = len(group)
        if number == 0:
            return False
        
        # 实际操作
        while number > 0:
            number = number - 1

            # 添加魔法球
            if old_color == -1:
                manaball = Manaball(self.system, player)
                player.manaballs.append(manaball)
                if new_color >= 0:
                    manaball.color = new_color
                if new_status == 0:
                    manaball.used = True
                if new_status == 1:
                    manaball.used = False
            else:

                # 随机选取魔法球
                manaball = group[randint(0, len(group) - 1)]
                group.remove(manaball)

                # 删除魔法球
                if new_color == -1:
                    player.manaballs.remove(manaball)
                # 改变魔法球
                else:
                    if new_color != -2:
                        manaball.color = new_color
                    if new_status == 0:
                        manaball.used = True
                    if new_status == 1:
                        manaball.used = False

        # 魔法球重新排序
        player.sortmanaballs()
        
        return True

    def jumpturn(self):
        #param: player
        
        return False

    def playerselect(self):
        
    	# 伪事件 用来触发buff
        # param: player, group
        player = self.param[0]
        group = self.param[1]
        
        # 检查条件
        if len(group) <= 0:
            return False

        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if buff.onplayerselect:
                    buff.onplayerselect(buff, self)
        return True

    def turnstart(self):
        # param: player
        player = self.param[0]
        

        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if buff.onturnstart:
                    buff.onturnstart(buff, self)

        # 重置攻击次数
        for card in self.system.cards:
            if (card.place == PLACE_FIELD):
                card.attacktime = 0
                

        return True

    def turnstop(self):
        # param: player
        player = self.param[0]
        
        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if buff.onturnstop:
                    buff.onturnstop(buff, self)
        return False

    def move(self):
        # param: group, location, warcry.
        group = self.param[0]
        location = self.param[1]
        warcry = self.param[2]
        deadword = self.param[3]
        usecard = self.param[4]
        draw = self.param[5]
        discard = self.param[6]

        if self.lastevent:
            passevent = self.lastevent
        else:
            passevent = self

        # 检查条件
        if len(group) <= 0:
            return False

        # 触发亡语特效
        if (deadword) and (location == PLACE_GRAVE):
            for card in self.system.cards:
                for buff in card.buffs:
                    if buff.deadword:
                        buff.deadword(buff, passevent)

        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if buff.before_move:
                    if not buff.before_move(buff, self):
                        return False

        # 移动卡片
        for card in group:
            card.old_place = card.place
            card.place = location

        # 触发使用卡片特效
        if (usecard):
            for card in self.system.cards:
                for buff in card.buffs:
                    if buff.after_usecard:
                        buff.after_usecard(buff, passevent)
            
        # 卡片控制权交还
        if (location == PLACE_GRAVE):
            for card in self.param[0]:
                if (card.source):
                    card.player = card.source
                

        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if buff.after_move:
                    buff.after_move(buff, self)

        # 卡片信息复原
        for card in group:
            #if (card.old_place == PLACE_HAND) and (location != PLACE_HAND):
            #    card.cost = card.originalcost.copy()
            if (card.old_place == PLACE_FIELD) and (location != PLACE_FIELD):
            #    card.maxhealth = card.orimaxhealth
                card.health = card.maxhealth
            #    card.attack = card.oriattack
                    

        # 触发战吼特效
        if (warcry) and (location == PLACE_FIELD):
            for card in group:
                for buff in card.buffs:
                    if buff.warcry:
                        buff.warcry(buff, self)
        # 触发抽牌特效
        if (draw) and (location == PLACE_HAND):
            for card in self.system.cards:
                for buff in card.buffs:
                    if buff.after_draw:
                        buff.after_draw(buff, passevent)
        return False

    def draw(self):
        # param: player
        player = self.param[0]
        
        # 创建卡池
        deck = []
        for card in self.system.cards:
            if card.player == player and card.place == PLACE_DECK:
                deck.append(card)

        # 有卡抽的场合
        if len(deck) > 0:
            
            # 触发特效
            for card in self.system.cards:
                for buff in card.buffs:
                    if buff.before_draw:
                        if not buff.before_draw(buff, self):
                            return False

            # 创建移动效果
            card = deck[randint(0, len(deck) - 1)]
            param = [[card], PLACE_HAND, False, False, False, True, False]
            event = Event(self.system, EVENT_MOVE, self.buff, param)
            self.system.add_event_now(event)
            event.lastevent = self

            return True
        else:
            return False

    def damage(self):
        # param: target, source, number, damagetype

        target = self.param[0]
        source = self.param[1]
        damage = self.param[2]
        damagetype = self.param[3]
        

        # 检查条件
        if len(target) <= 0:
            return False

        # 为特效创建enable数组
        enables = []
        for index in range(len(target)):
            enables.append(damage[index] > 0)
        self.param.append(enables)

        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if (buff.before_damage):
                    if not buff.before_damage(buff, self):
                        return False

        # 判定有没有可以造成伤害的单位
        still = False
        for cond in enables:
            if cond:
                still = True
        if not still:
            return False

        # 造成伤害
        for index in range(len(target)):
            cond = enables[index]
            if cond:
                character = target[index]
                character.health = character.health - damage[index]

        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if buff.after_damage:
                    buff.after_damage(buff, self)

        # 判定死亡群组
        deadcards = []
        deadplayers = []
        for character in target:
            if character.health <= 0:
                if isinstance(character, Card):
                    deadcards.append(character)
                if isinstance(character, Player):
                    deadplayers.append(character)
                
        # 创建死亡效果
        if (len(deadplayers) > 0):
            param = [deadplayers]
            event = Event(self.system, EVENT_LOSE, self.buff, param)
            self.system.add_event_now(event)
            
        if (len(deadcards) > 0):
            param = [deadcards, source, True]
            event = Event(self.system, EVENT_KILL, self.buff, param)
            self.system.add_event_now(event)
        
        return True

    def heal(self):
        # param: target, source, number
        target = self.param[0]
        source = self.param[1]
        amount = self.param[2]

        # 检查条件
        if len(target) <= 0:
            return False

        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if buff.before_heal:
                    if not buff.before_heal(buff, self):
                        return False

        # 造成治疗
        for index in range(len(target)):
            character = target[index]
            character.health = character.health + amount[index]
            if character.health > character.maxhealth:
                character.health = character.maxhealth

        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if buff.after_heal:
                    buff.after_heal(buff, self)        
        return True

    def kill(self):
        # param: targets, attacker, deadword
        targets = self.param[0]
        killer = self.param[1]
        deadword = self.param[2]

        # 检查条件
        if len(targets) <= 0:
            return False
        
        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if buff.before_kill:
                    if not buff.before_kill(buff, self):
                        return False

        # 创建移动效果
        param = [targets, PLACE_GRAVE, False, True, False, False, False]
        event = Event(self.system, EVENT_MOVE, self.buff, param)
        self.system.add_event_now(event)
        event.lastevent = self
        
        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if buff.after_kill:
                    buff.after_kill(buff, self)
                    
        return True

    def usecard(self):
        # param: card, target, fromhand, pay
        card = self.param[0]
        target = self.param[1]
        fromhand = self.param[2]
        pay = self.param[3]
        
        player = card.player

        # 检查条件 - 自定义条件
        if card.disabled(card):
            return False
        
        # 检查费用并支付
        if pay:
            if player.hasmana(card.cost):
                param = [player, card.cost]
                event = Event(self.system, EVENT_COSTMANA, self.buff, param)
                self.system.add_event_now(event)
                self.lastevent = event
            else:
                return False
            

        # 触发特效
        for buff in card.buffs:
            if buff.before_usecard:
                if not buff.before_usecard(buff, self):
                    return False

        # 生物牌的场合
        if card.typ == CARD_CREATURE:
            # 移去场上
            param = [[card], PLACE_FIELD, True, False, True, False, False]
            event = Event(self.system, EVENT_MOVE, self.buff, param)
            self.system.add_event_now(event)
            event.lastevent = self
        
        # 法术牌的场合
        if card.typ == CARD_SPELL:
            # 移去墓地
            param = [[card], PLACE_GRAVE, False, False, True, False, False]
            event = Event(self.system, EVENT_MOVE, self.buff, param)
            self.system.add_event_now(event)
            event.lastevent = self
        
        
        return True

    def attack(self):
        # param: attacker, target
        attacker = self.param[0]
        target = self.param[1]
        
        # 检查条件 - 自定义条件
        if attacker.cannotattack(attacker):
            return False

        attacker.attacktime = attacker.attacktime + 1
        
        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if buff.before_attack:
                    if not buff.before_attack(buff, self):
                        return False

        # 计算受到伤害
        if isinstance(target, Card):
            dtaken = target.attack
        if isinstance(target, Player):
            dtaken = 0

        # 造成伤害
        if attacker.attack > 0:
            group = [target]
            damage = [attacker.attack]
            param = [group, attacker, damage, DAMAGE_PHYSICAL]
            event = Event(self.system, EVENT_DAMAGE, self.buff, param)
            self.system.add_event_now(event)
            self.lastevent = event

        if dtaken > 0:
            group = [attacker]
            damage = [dtaken]
            param = [group, target, damage, DAMAGE_PHYSICAL]
            event = Event(self.system, EVENT_DAMAGE, self.buff, param)
            self.system.add_event_now(event)
            self.lastevent = event

        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if buff.after_attack:
                    buff.after_attack(buff, self)
        
        return True

    def costmana(self):
        # param: player, costlist.
        player = self.param[0]
        cost = self.param[1].copy()
        
        # 检查条件 - 费用
        if not player.hasmana(cost):
            return False

        # 消费对应颜色的魔法球
        for manaball in player.manaballs:
            if (manaball.used == False) and (cost[manaball.color] > 0):
                manaball.used = True
                cost[manaball.color] = cost[manaball.color] - 1

        # 消费白色的魔法球
        manaballindex = 0
        for colorindex in range(6):
            while cost[colorindex] > 0:
                while (player.manaballs[manaballindex].used == True) or (player.manaballs[manaballindex].color > 0):
                    manaballindex = manaballindex + 1
                player.manaballs[manaballindex].used = True
                player.manaballs[manaballindex].color = colorindex
                cost[colorindex] = cost[colorindex] - 1

        # 魔法球重新排序
        player.sortmanaballs()
        
        
        # 触发特效
        for card in self.system.cards:
            for buff in card.buffs:
                if buff.oncostmana:
                    buff.oncostmana(buff, self)

        return True
                

from card import *

from buff import *
from player import *
