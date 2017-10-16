import pygame
from pygame.locals import *

class Player:
    def __init__(self, system, playerinfo):
        self.system = system
        self.playerinfo = playerinfo
        
        self.drawlevel = 5
        self.manaballsur = pygame.Surface((self.system.screen_length, int(self.system.screen_height * 0.05)))

        self.selected = 0

        self.mask = [0, 0, 0, 0]
        self.final_mask = [0, 0, 0, 0]

    def changeinfo(self, playerinfo):
        oldinfo = self.playerinfo
        newinfo = playerinfo
        
        if (self.drawlevel < 5) and (oldinfo.image != newinfo.image):
            self.drawlevel = 5
        if (self.drawlevel < 3) and (oldinfo.health != newinfo.health):
            self.drawlevel = 3
            if (oldinfo.health > newinfo.health):
                self.mask = [255, 0, 0, 255]
            
        self.playerinfo = newinfo
        newinfo.player = self

    def reload(self):
        self.image = self.system.imageloader.load("images/players/%03d.png" % self.playerinfo.image, False)

    def make_card(self):
        # 制作生物
        cardcreature = self.system.cardcreature.copy()
        cardcreature.blit(self.image, (10, 10))
        ball_health = self.system.ball_health.copy()
        cardcreature.blit(ball_health, (170, 170))
        self.cardcreature = cardcreature
        

    def write_words(self):
        white_color = (255, 255, 255)
        health_string = ("%d" % self.playerinfo.health)
        self.health_text = self.system.font[0].render(health_string, True, white_color)

    def resize(self):
        unit = self.system.screen_height
        length = int(unit * 0.2)
        self.cardcreature = pygame.transform.scale(self.cardcreature, (length, length))
        self.creatureselect = []
        for i in range(3):
            picture = pygame.transform.scale(self.system.creatureselect[i], (length, length))
            self.creatureselect.append(picture)
        self.length = length
        self.height = length

        # resize text
        numlength_o, numheight_o = self.health_text.get_size()
        numheight = self.length / 220 * 40
        numlength = numlength_o / numheight_o * numheight
        if numlength > numheight:
            numlength = numheight
        self.health_sur = pygame.transform.scale(self.health_text, (int(numlength), int(numheight)))
        self.mask_sur_creature = pygame.Surface((length, length))

    def setpos(self):
        unit = self.system.screen_height
        self.x = 0

        # 自己的牌
        if (self.playerinfo.index == self.system.index):
            pery = 0.75
            self.y = int(pery * unit)
        # 对面的牌
        else:
            pery = 0.05
            self.y = int(pery * unit)

        # 计算文字位置
        scale = self.length / 220
        totalw, totalh = self.health_sur.get_size()
        extrax = int(((scale * 50) - totalw) / 2)
        self.health_sur_info = [self.health_sur, int(scale * 175) + extrax,  int(scale * 175)]

    # Draw level 1 - Draw
    def update(self, time):
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
            self.setpos()

        content = self.cardcreature
        self.system.screen.blit(content, (self.x, self.y))
        if self.selected > 0:
            select = self.creatureselect[self.selected - 1]
            self.system.screen.blit(select, (self.x, self.y))

        self.system.screen.blit(self.health_sur_info[0], (self.x + self.health_sur_info[1], self.y + self.health_sur_info[2]))

        if self.mask[3] > 0:
            self.mask_sur_creature.fill(self.mask)
            self.mask_sur_creature.set_alpha(self.mask[3])
            self.system.screen.blit(self.mask_sur_creature, (self.x, self.y))

        self.draw_manaballs()

    def draw_manaballs(self):
        unit = self.system.screen_height
        length = int(unit * 0.05)
        
        self.manaballsur.fill((0, 0, 0))
        index = 0
        for colorindex in range(6):
            for ballindex in range(self.playerinfo.unusedmana[colorindex]):
                self.manaballsur.blit(self.system.resizedmanaballs[colorindex], (index * length, 0))
                index = index + 1
            for ballindex in range(self.playerinfo.usedmana[colorindex]):
                self.manaballsur.blit(self.system.resizedmanaballs_e[colorindex], (index * length, 0))
                index = index + 1

        x = 0
        if (self.playerinfo.index == self.system.index):
            y = int(0.95 * unit)
        else:
            pery = 0.05
            y = 0

        self.system.screen.blit(self.manaballsur, (x, y))

    # 判定鼠标是否在卡图内
    def inside(self, x, y):
        sx = self.x
        sy = self.y
        ex = self.x + self.length
        ey = self.y + self.height
        return ((x >= sx) and (x <= ex) and (y >= sy) and (y <= ey))

    # 处理事件
    def deal(self, event):
        if self.system.selector.selecting:
            if (event.type == MOUSEBUTTONDOWN) and (event.button == 1):
                x, y = event.pos
                if self.inside(x, y):
                    self.select()
                    
        if (self.system.operator.operating) and (self.system.operator.attacking):
            if (event.type == MOUSEBUTTONUP) and (event.button == 1):
                x, y = event.pos
                if self.inside(x, y):
                    self.operate_target()

    # 被选择
    def select(self):
        self.system.selector.clicktarget(self)
    # 被操作目标
    def operate_target(self):
        self.system.operator.attacktarget(self)
