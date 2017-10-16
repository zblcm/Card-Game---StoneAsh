import pygame
from pygame.locals import *

from const import *
from floatword import *
from system import *

class Card:
    def __init__(self, system, cardinfo):
        self.system = system
        self.cardinfo = cardinfo
        cardinfo.card = self
        self.drawlevel = 5
        self.drawed = False
        self.selected = 0
        
        self.x = int((self.system.screen_length - (self.system.screen_height * 0.2 * 360 / 220)) * 0.5)
        self.y = int(self.system.screen_height * 0.4)
        self.final_x = self.x
        self.final_y = self.y

        self.mask = [0, 0, 0, 0]
        self.final_mask = [0, 0, 0, 0]
        
        self.alpha = 0
        self.final_alpha = 255
        self.infoalpha = 0
        self.final_infoalpha = 0
        
        self.lockcreature = False
        self.focusing = False
        self.hovering = False
        self.seen = False
        self.needremakebuffdescription = True
        self.needresizebuffdescription = False
        self.hovertime = 0

    # 卡片信息变更
    def makebuffinfo(self, name, description):
        surface = pygame.Surface((220, 150))
        surface.fill((255, 255, 255))

        # 誊写卡名
        name_text_o = self.system.font[1].render(name, True, (0, 0, 0))
        name_text_length_o, name_text_height_o = name_text_o.get_size()
        name_text_height_f = 40
        name_text_length_f = int(name_text_height_f / name_text_height_o * name_text_length_o)
        if name_text_length_f > 210:
            name_text_length_f = 210
        name_text_f = pygame.transform.smoothscale(name_text_o, (name_text_length_f, name_text_height_f))
        startx = 5 + ((210 - name_text_length_f) / 2)
        surface.blit(name_text_f, (startx, 0))
        
        # 誊写描述
        text = description
        text_length = len(text)
        if text_length > 0:
            text_size = int(foundtextsize(text_length, 210, 95, 20))
            if text_size > 35:
                text_size = 35
            sx = 5
            sy = 50
            text_index = 0
            while text_index < text_length:
                char = text[text_index]
                if (len(char) == len(char.encode())):
                    char_size = int(text_size * 0.5)
                else:
                    char_size = text_size
                if (sx + char_size > 215):
                    sx = 5
                    sy = sy + text_size
                char_sur = self.system.font[1].render(char, True, (0, 0, 0))
                char_sur_resized = pygame.transform.smoothscale(char_sur, (char_size, text_size))
                surface.blit(char_sur_resized, (sx, sy))
                text_index = text_index + 1
                sx = sx + char_size
        return surface

    def remakebuffinfos(self):
        self.needresizebuffdescription = True
        self.needremakebuffdescription = False
        self.description_buffinfos = []
        for buffinfo in self.cardinfo.buffinfos:
            if buffinfo.visable:
                self.description_buffinfos.append(self.makebuffinfo(buffinfo.name, buffinfo.description))
                
    def changeinfo(self, cardinfo):
        oldinfo = self.cardinfo
        newinfo = cardinfo
        
        if (self.drawlevel < 1) and ((oldinfo.place != newinfo.place) or (oldinfo.playerinfo.index != newinfo.playerinfo.index)):
            # print("debug: %d %d" % (len(self.system.drawcardinfos[oldinfo.playerinfo.index][oldinfo.place]), len(self.system.drawcardinfos[newinfo.playerinfo.index][newinfo.place])))
            self.changeplace(oldinfo.playerinfo.index, oldinfo.place)
            self.changeplace(newinfo.playerinfo.index, newinfo.place)

        if (self.drawlevel < 5) and (oldinfo.number != newinfo.number):
            self.drawlevel = 5
        if (self.drawlevel < 4) and (oldinfo.typ != newinfo.typ):
            self.drawlevel = 4
        if (self.drawlevel < 3) and ((oldinfo.cost != newinfo.cost) or ((oldinfo.typ == CARD_CREATURE) and (newinfo.typ == CARD_CREATURE) and ((oldinfo.attack != newinfo.attack) or (oldinfo.health != newinfo.health)))):
            self.drawlevel = 3
            if (oldinfo.place == PLACE_FIELD) and (oldinfo.health > newinfo.health) and (self.showtop()):
                self.mask = [255, 0, 0, 191]
                
                unit = self.system.screen_height * 0.2 / 220
                text = "-%d" % int(oldinfo.health - newinfo.health)
                height = unit * 100
                center_pos = (self.x + unit * 110, self.y + unit * 110)
                final_rel_pos = (0, unit * (-110))
                rel_speed = 5
                time = 750
                Floatword(self.system, text, height, center_pos, final_rel_pos, rel_speed, time, (255, 127, 127))
                
            if (oldinfo.place == PLACE_FIELD) and (newinfo.place == PLACE_FIELD) and (oldinfo.health < newinfo.health) and (self.showtop()):
                self.mask = [0, 255, 0, 191]
                
                unit = self.system.screen_height * 0.2 / 220
                text = "+%d" % int(newinfo.health - oldinfo.health)
                height = unit * 100
                center_pos = (self.x + unit * 110, self.y + unit * 110)
                final_rel_pos = (0, unit * (-110))
                rel_speed = 5
                time = 750
                Floatword(self.system, text, height, center_pos, final_rel_pos, rel_speed, time, (127, 255, 127))
                
            if (oldinfo.place == PLACE_FIELD) and (newinfo.place == PLACE_GRAVE) and (oldinfo.health > 0) and (self.showtop()):
                self.mask = [255, 0, 0, 191]
                
                unit = self.system.screen_height * 0.2 / 220
                text = "-%d" % int(oldinfo.health)
                height = unit * 100
                center_pos = (self.x + unit * 110, self.y + unit * 110)
                final_rel_pos = (0, unit * (-110))
                rel_speed = 5
                time = 750
                Floatword(self.system, text, height, center_pos, final_rel_pos, rel_speed, time, (255, 127, 127))
            
        self.cardinfo = newinfo
        newinfo.card = self

        self.needremakebuffdescription = True
        self.remakebuffimages()

    def changeplace(self, playerindex, placeindex):
        for cardinfo in self.system.drawcardinfos[playerindex][placeindex]:
            if cardinfo.card.drawlevel < 1:
                cardinfo.card.drawlevel = 1

    # 卡片绘制分级函数
    def reload(self):
        self.image = self.system.imageloader.load("images/cards/c%010d.png" % self.cardinfo.number, False)

    # Draw level 4 - Remake
    def make_card(self):
        # 制作卡背
        self.cardback = self.system.cardback.copy()

        # 制作卡面
        cardtop = self.system.cardtop.copy()
        cardtop.blit(self.image, (10, 50))
        
        # 誊写卡名
        name_text_o = self.system.font[1].render(self.cardinfo.name, True, (0, 0, 0))
        name_text_length_o, name_text_height_o = name_text_o.get_size()
        name_text_height_f = 40
        name_text_length_f = int(name_text_height_f / name_text_height_o * name_text_length_o)
        if name_text_length_f > 200:
            name_text_length_f = 200
        name_text_f = pygame.transform.smoothscale(name_text_o, (name_text_length_f, name_text_height_f))
        startx = 200 - name_text_length_f + 10
        cardtop.blit(name_text_f, (startx, 0))

        # 誊写描述
        extra = 0
        if self.cardinfo.typ == CARD_CREATURE:
            extra = 25
        text = self.cardinfo.description
        text_length = len(text)
        if text_length > 0:
            text_size = int(foundtextsize(text_length, 210 - extra, 90, 20))
            sx = 5 + extra
            sy = 265
            text_index = 0
            while text_index < text_length:
                char = text[text_index]
                if (len(char) == len(char.encode())):
                    char_size = int(text_size * 0.5)
                else:
                    char_size = text_size
                if (sx + char_size > 215):
                    sx = 5 + extra
                    sy = sy + text_size
                char_sur = self.system.font[1].render(char, True, (0, 0, 0))
                char_sur_resized = pygame.transform.smoothscale(char_sur, (char_size, text_size))
                cardtop.blit(char_sur_resized, (sx, sy))
                text_index = text_index + 1
                sx = sx + char_size

    	# 制作生物卡面信息
        if self.cardinfo.typ == CARD_CREATURE:
            
            # 制作生物形态
            cardcreature = self.system.cardcreature.copy()
            cardcreature.blit(self.image, (10, 10))
            self.cardcreature = cardcreature
        self.cardtop = cardtop

    # Draw level 3 - Rewrite
    
    def resize_text(self, text):
        numlength_o, numheight_o = text.get_size()
        numheight = 40
        numlength = numlength_o / numheight_o * numheight
        if numlength > numheight:
            numlength = numheight
        text_sur = pygame.transform.smoothscale(text, (int(numlength), int(numheight)))
        return text_sur, numlength, numheight

    def write_words(self):
        lgiht_red_color = (255, 127, 127)
        white_color = (255, 255, 255)
        black_color = (0, 0, 0)
        dark_red_color = (127, 0, 0)
        dark_green_color = (0, 127, 0)

        # 设置cost文字
        self.cost_bottoms = []
        for colorindex_f in range(5):
            colorindex = colorindex_f + 1
            if (self.cardinfo.cost[colorindex] > 0) or (self.cardinfo.originalcost[colorindex] > 0):
                cost_bottom = self.system.manacost[colorindex].copy()
                cost_string = ("%d" % self.cardinfo.cost[colorindex])

                if (self.cardinfo.cost[colorindex] > self.cardinfo.originalcost[colorindex]):
                    cost_color = dark_red_color
                if (self.cardinfo.cost[colorindex] == self.cardinfo.originalcost[colorindex]):
                    cost_color = black_color
                if (self.cardinfo.cost[colorindex] < self.cardinfo.originalcost[colorindex]):
                    cost_color = dark_green_color
                    
                cost_text_o = self.system.font[0].render(cost_string, True, cost_color)
                cost_text_o_length, cost_text_o_height = cost_text_o.get_size()
                cost_text_f_height = 30
                cost_text_f_length = cost_text_o_length * cost_text_f_height / cost_text_o_height
                if cost_text_f_height > 30:
                    cost_text_f_height = 30
                cost_text_f = pygame.transform.smoothscale(cost_text_o, (int(cost_text_f_length), int(cost_text_f_height)))
                extrax = int((30 - cost_text_f_length) / 2)
                cost_bottom.blit(cost_text_f, (5 + extrax, 5))
                self.cost_bottoms.append(cost_bottom)
                
        # 设置攻击和防御
        if self.cardinfo.typ == CARD_CREATURE:
            attack_string = ("%d" % self.cardinfo.attack)
            health_string = ("%d" % self.cardinfo.health)
            attack_text = self.system.font[0].render(attack_string, True, white_color)
            if self.cardinfo.health < self.cardinfo.maxhealth:
                health_text = self.system.font[0].render(health_string, True, lgiht_red_color)
            else:
                health_text = self.system.font[0].render(health_string, True, white_color)
            self.ball_attack = self.system.ball_attack.copy()
            sur, l, h = self.resize_text(attack_text)
            extrax = int((40 - l) / 2)
            self.ball_attack.blit(sur, (extrax + 5, 5))
            self.ball_health = self.system.ball_health.copy()
            sur, l, h = self.resize_text(health_text)
            extrax = int((40 - l) / 2)
            self.ball_health.blit(sur, (extrax + 5, 5))
            
        return False

    # Draw level 2 - Resize
    def resizebuffinfos(self):
        self.needresizebuffdescription = False
        new_length = self.system.screen_height * 0.2
        new_height = new_length / 220 * 150
        cur_height = new_length / 220 * (360 + 20)
        self.description_buffinfos_surfaces = []
        for surface in self.description_buffinfos:
            new_surface = pygame.transform.smoothscale(surface, (int(new_length), int(new_height)))
            self.description_buffinfos_surfaces.append([new_surface, 0, int(cur_height)])
            cur_height = cur_height + new_height
        
    def remakebuffimages(self):
        self.buffimages = []
        for buffinfo in self.cardinfo.buffinfos:
            if buffinfo.image:
                image = self.system.imageloader.resize("images/buffs/%s.png" % buffinfo.image)
                length_s, height_s = self.getabssize()
                length_i, height_i = image.get_size()
                ix = int((length_s / 2) - (length_i / 2))
                iy = int((height_s / 2) - (height_i / 2))
                self.buffimages.append((image, ix, iy, buffinfo.imageinside))
    
    def resize(self):
        unit = self.system.screen_height
        length = int(self.system.screen_height * 0.2)
        height = int(length / 220 * 360)

    	# 重设卡片和选择框
        self.cardback = pygame.transform.smoothscale(self.cardback, (length, height))
        self.cardtop = pygame.transform.smoothscale(self.cardtop, (length, height))
        self.mask_sur = pygame.Surface((length, height))
        self.infotop = self.cardtop.copy()

        if self.cardinfo.typ == CARD_CREATURE:
            self.mask_sur_creature = pygame.Surface((length, length))
            self.cardcreature = pygame.transform.smoothscale(self.cardcreature, (length, length))

        # 重设属性球
        if self.cardinfo.typ == CARD_CREATURE:
            ball_length = int((unit * 0.2) * (50 / 220))
            self.ball_attack_sur = pygame.transform.smoothscale(self.ball_attack, (ball_length, ball_length))
            self.ball_health_sur = pygame.transform.smoothscale(self.ball_health, (ball_length, ball_length))
            self.infoball_attack_sur = self.ball_attack_sur.copy()
            self.infoball_health_sur = self.ball_health_sur.copy()

        # 重设cost
        cost_length = int(length / 220 * 40)
        self.resized_costs = []
        for cost_bottom in self.cost_bottoms:
            resized_cost = pygame.transform.smoothscale(cost_bottom, (cost_length, cost_length))
            self.resized_costs.append(resized_cost)

        self.needresizebuffdescription = True
        self.remakebuffimages()

    # Draw level 1 - Repos
    def resetfinalpos(self):
        unit = self.system.screen_height
        wscale = self.system.screen_length / self.system.screen_height
        peernum = len(self.system.drawcardinfos[self.cardinfo.playerinfo.index][self.cardinfo.place])
        
        self.ballsurs = []
        self.costsurs = []
        length_s, height_s = self.getabssize()
        
        # 手牌的场合
        if self.cardinfo.place == PLACE_HAND:
            # 计算间隔
            if peernum <= 1:
                interval = 0
            else:
                interval = ((wscale - 0.25 - 0.25) - (0.2 * peernum)) / (peernum - 1)
                if interval > 0.05:
                    interval = 0.05
            totalw = (0.2 * peernum) + (interval * (peernum - 1))
            startw = 0.225 + ((wscale - 0.225 - totalw - 0.25) / 2)
            

            perx = startw + ((interval + 0.2) * self.cardinfo.drawindex)
            self.final_x = int(perx * unit)

            # 自己的牌
            if (self.cardinfo.playerinfo.index == self.system.index):
                pery = 0.75 + 0.025
                self.final_y = int(pery * unit)
            # 对面的牌
            else:
                pery = 0.25 - 0.025
                self.final_y = int((pery * unit) - (length_s / 220 * 360))
                
            # 计算属性球位置
            scale = length_s / 220
            if self.cardinfo.typ == CARD_CREATURE:
                self.ballsurs.append([self.ball_attack_sur, int(scale * (-25)),  int(scale * 285)])
                self.ballsurs.append([self.ball_health_sur, int(scale * (-25)),  int(scale * 335)])

            # 计算cost位置
            
            # 重设cost
            startx = scale * (-40)
            starty = 0
            for resized_cost in self.resized_costs:
                costsur = [resized_cost, int(startx), int(starty)]
                self.costsurs.append(costsur)
                starty = starty + (scale * (40))

        # 场上的场合
        if self.cardinfo.place == PLACE_FIELD:
            # 计算间隔
            if peernum <= 1:
                interval = 0
            else:
                interval = ((wscale - 0.05 - 0.25) - (0.2 * peernum)) / (peernum - 1)

            if interval > 0.1:
                interval = 0.1
                
            totalw = (0.2 * peernum) + (interval * (peernum - 1))
            startw = (wscale - totalw - 0.25) / 2
                
            perx = startw + ((interval + 0.2) * self.cardinfo.drawindex)
            self.final_x = int(perx * unit)

            # 自己的牌
            if (self.cardinfo.playerinfo.index == self.system.index):
                pery = 0.5 + 0.025
                self.final_y = int(pery * unit)
            # 对面的牌
            else:
                pery = 0.25 + 0.025
                self.final_y = int(pery * unit)

            # 计算属性球位置
            scale = length_s / 220
            self.ballsurs.append([self.ball_attack_sur, int(scale * (-25)),  int(scale * (-25))])
            self.ballsurs.append([self.ball_health_sur, int(scale * (-25)),  int(scale * 195)])

        if (self.cardinfo.place == PLACE_DECK) or (self.cardinfo.place == PLACE_GRAVE) or (self.cardinfo.place == PLACE_VOID):
            self.final_alpha = 0
        else:
            self.final_alpha = 255
        self.final_mask = [0, 0, 0, 0]

    # Draw level 1 - Draw
    def update(self, time):
        # Change position
        speed_c = 50 * time / 1000
        dis = (((self.x - self.final_x) ** 2) + ((self.y - self.final_y) ** 2)) ** (0.5)
        if (dis < speed_c):
            self.x = self.final_x
            self.y = self.final_y
        else:
            speed_v = (dis * time / 1000 * 5)
            scale = (dis - (speed_c + speed_v)) / dis
            self.x = int((self.x - self.final_x) * scale + self.final_x)
            self.y = int((self.y - self.final_y) * scale + self.final_y)

        # Change color
        speed_color = 512 * time / 1000

        if self.final_mask[3] > 0:
            for i in range(3):
                self.mask[i] = self.final_mask[i]
        if abs(self.mask[3] - self.final_mask[3]) < speed_color:
            self.mask[3] = int(self.final_mask[3])
        else:
            if self.mask[3] > self.final_mask[3]:
                self.mask[3] = int(self.mask[3] - speed_color)
            else:
                self.mask[3] = int(self.mask[3] + speed_color)

        """
        # Change mask
        for i in range(4):
            if abs(self.mask[i] - self.final_mask[i]) < speed_color:
                self.mask[i] = int(self.final_mask[i])
            else:
                if self.mask[i] > self.final_mask[i]:
                    self.mask[i] = int(self.mask[i] - speed_color)
                else:
                    self.mask[i] = int(self.mask[i] + speed_color)
        """

        # Chenge card alpha
        if abs(self.alpha - self.final_alpha) < speed_color:
            self.alpha = int(self.final_alpha)
        else:
            if self.alpha > self.final_alpha:
                self.alpha = int(self.alpha - speed_color)
            else:
                self.alpha = int(self.alpha + speed_color)
                

        # Change info alpha
        if abs(self.infoalpha - self.final_infoalpha) < speed_color:
            self.infoalpha = int(self.final_infoalpha)
        else:
            if self.infoalpha > self.final_infoalpha:
                self.infoalpha = int(self.infoalpha - speed_color)
            else:
                self.infoalpha = int(self.infoalpha + speed_color)
                

        # Set hovertime
        if self.hovering:
            self.hovertime = self.hovertime + time
        
        return True

    def showtop(self):
        if (self.cardinfo.place == PLACE_FIELD) or (self.cardinfo.place == PLACE_GRAVE) or (self.cardinfo.place == PLACE_VOID):
            return True
        return (self.cardinfo.playerinfo.index == self.system.index) or (self.seen)

    def showcreature(self):
        if (self.cardinfo.typ != CARD_CREATURE):
            return False
        if (self.cardinfo.place == PLACE_FIELD) or (self.lockcreature):
            return True
        return False

    def getabssize(self):
        length = int(self.system.screen_height * 0.2)
        height = int(length / 220 * 360)
        if self.showcreature():
            return length, length
        else:
            return length, height
    
    def draw(self):
        # 0:nothong 1:repos 2:resize 3:rewords 4:remake 5:reload
        if (self.drawlevel >= 5):
            self.reload()
        if (self.drawlevel >= 4):
            self.make_card()
        if (self.drawlevel >= 3):
            self.write_words()
        if (self.drawlevel >= 2):
            self.resize()
        if (self.drawlevel >= 1):
            self.resetfinalpos()

        if self.alpha == 0:
            self.lockcreature = False
            return False
        if self.lockcreature and (self.cardinfo.place == PLACE_HAND or self.cardinfo.place == PLACE_DECK):
            self.lockcreature = False
        length_s, height_s = self.getabssize()
        scale = length_s / 220
        mask = None
        drawball = False

        # 场上的场合
        if self.cardinfo.place == PLACE_FIELD:
            self.lockcreature = True

        if self.showcreature():
            drawball = True
            content = self.cardcreature
            if self.selected > 0:
                select = self.system.creatureselect_resized[self.selected - 1]
            if self.mask[3] > 0:
                # 本来应该判定如果mask没变就不用fill 可是太麻烦了
                self.mask_sur_creature.fill(self.mask)
                mask = self.mask_sur_creature
        else:
            if self.showtop():
                content = self.cardtop
                drawball = True
            else:
                content = self.cardback
            if self.selected > 0:
                select = self.system.cardselect_resized[self.selected - 1]
            if self.mask[3] > 0:
                # 本来应该判定如果mask没变就不用fill 可是太麻烦了
                self.mask_sur.fill(self.mask)
                mask = self.mask_sur
            

        if (self.alpha > 0):
            content = content.copy()
            for buffsur in self.buffimages:
                if buffsur[3]:
                    content.blit(buffsur[0], (buffsur[1], buffsur[2]))
            content.set_alpha(self.alpha)
            self.system.screen.blit(content, (self.x, self.y))
            if mask:
                mask.fill(self.mask)
                mask.set_alpha(self.mask[3])
                self.system.screen.blit(mask, (self.x, self.y))
            if self.selected > 0:
                selectx = length_s / 220 * (-20)
                selecty = length_s / 220 * (-20)
                self.system.screen.blit(select, (self.x + selectx, self.y + selecty))
            for costsur in self.costsurs:
                costsur[0].set_alpha(self.alpha)
                self.system.screen.blit(costsur[0], (self.x + costsur[1], self.y + costsur[2]))
            
            if drawball:
                for ball in self.ballsurs:
                    ball[0].set_alpha(self.alpha)
                    self.system.screen.blit(ball[0], (self.x + ball[1], self.y + ball[2]))
            for buffsur in self.buffimages:
                if not buffsur[3]:
                    self.system.screen.blit(buffsur[0], (self.x + buffsur[1], self.y + buffsur[2]))
    # 画出详细信息
    def drawinfo(self):
        if self.infoalpha == 0:
            return False

        # Draw card
        unit = self.system.screen_height
        startx = int(self.system.screen_length - (unit * (0.025 + 0.2)))
        starty = int(unit * (0.025 + 0.05))
        self.infotop.set_alpha(self.infoalpha)
        self.system.screen.blit(self.infotop, (startx, starty))
        
        # Draw buffs
        if self.needremakebuffdescription:
            self.remakebuffinfos()
        if self.needresizebuffdescription:
            self.resizebuffinfos()
        for l in self.description_buffinfos_surfaces:
            l[0].set_alpha(self.infoalpha)
            self.system.screen.blit(l[0], (startx + l[1], starty + l[2]))
        
        # Draw balls
        length_s, height_s = self.getabssize()
        if self.cardinfo.typ == CARD_CREATURE:
            scale = length_s / 220
            
            ballx = int(scale * (-25))
            bally = int(scale * 285)
            self.infoball_attack_sur.set_alpha(self.infoalpha)
            self.system.screen.blit(self.infoball_attack_sur, (startx + ballx, starty + bally))

            bally = int(scale * 335)
            self.infoball_health_sur.set_alpha(self.infoalpha)
            self.system.screen.blit(self.infoball_health_sur, (startx + ballx, starty + bally))

    # 判定鼠标是否在卡图内
    def inside(self, x, y):
        if self.alpha == 0:
            return False
        
        length_s, height_s = self.getabssize()
        sx = self.x
        sy = self.y
        ex = self.x + length_s
        ey = self.y + height_s
        return ((x >= sx) and (x <= ex) and (y >= sy) and (y <= ey))

    # 处理事件
    def deal(self, event):
        
        # 被选择
        if self.system.selector.selecting:
            if (event.type == MOUSEBUTTONDOWN) and (event.button == 1):
                x, y = event.pos
                if self.inside(x, y):
                    self.select()

        # 被操作
        if self.system.operator.operating:
            if (event.type == MOUSEBUTTONDOWN) and (event.button == 1):
                x, y = event.pos
                if self.inside(x, y):
                    self.operate_press()

        # 被攻击
        if (self.system.operator.operating) and (self.system.operator.attacking):
            if (event.type == MOUSEBUTTONUP) and (event.button == 1):
                x, y = event.pos
                if self.inside(x, y):
                    self.operate_target()

        # 鼠标悬停 - 抽出手牌
        if (not self.focusing) and (self.cardinfo.place == PLACE_HAND) and (not ((self.system.operator.operating) and (self.system.operator.cardusing))):
            if (event.type == MOUSEMOTION):
                x, y = event.pos
                if (self.inside(x, y)):
                    if (self.cardinfo.playerinfo.index == self.system.index):
                        self.final_y = int(self.final_y - (self.system.screen_height * 0.175))
                        self.focusing = True
                        self.system.focusingcard = self
                    else:
                        if self.showtop(): 
                            self.final_y = int(self.final_y + (self.system.screen_height * 0.175))
                            self.focusing = True
                            self.system.focusingcard = self

        # 鼠标悬停 - 观看手牌
        if (not self.hovering):
            if (event.type == MOUSEMOTION):
                x, y = event.pos
                if (self.inside(x, y)):
                    self.hovering = True
                    self.system.hoveringcard = self

        # 是否继续处理
        if (event.type == MOUSEBUTTONDOWN) or (event.type == MOUSEBUTTONUP) or (event.type == MOUSEMOTION):
            x, y = event.pos
            if self.inside(x, y):
                return False

        # 什么都不做
        return True

    # 总是处理的事件
    def alwaysdeal(self, event):
        # 取消悬停 - 抽出手牌
        if (self.focusing) and (self.system.focusingcard != self):
            self.focusing = False
            self.drawlevel = 1

        if (self.focusing) and (self.cardinfo.place == PLACE_HAND) and (not ((self.system.operator.operating) and (self.system.operator.cardusing == self))):
            if (event.type == MOUSEMOTION):
                x, y = event.pos
                length_s, height_s = self.getabssize()
                sx = self.x
                sy = self.y
                ex = self.x + length_s
            
                if not ((x >= sx) and (x <= ex) and (y >= sy)):
                    if self.drawlevel < 1:
                        self.drawlevel = 1
                    self.system.focusingcard == None
                    self.focusing = False

        # 取消悬停 - 观看手牌
        if (self.hovering) and (self.system.hoveringcard != self):
            self.hovering = False

        if (self.hovering):
            if (event.type == MOUSEMOTION):
                x, y = event.pos
                if (not self.inside(x, y)):
                    self.hovering = False
                    self.system.hoveringcard = None
                    self.hovertime = 0

    # 被选择
    def select(self):
        self.system.selector.clicktarget(self)

    # 被操作
    def operate_press(self):
        self.system.operator.presstarget(self)

    # 被操作目标
    def operate_target(self):
        self.system.operator.attacktarget(self)









                
