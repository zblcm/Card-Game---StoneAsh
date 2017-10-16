import pygame
from pygame.locals import *

from const import *
from system import *

class Label:
    def __init__(self, system):
        self.system = system
        self.drawlevel = 5
        self.length_o = 600
        self.height_o = 220
        self.text = ""
        self.surface_o = pygame.Surface((self.length_o, self.height_o))

        self.x = int((self.system.screen_length - (self.system.screen_height * 0.2 * self.length_o / self.height_o)) * 0.5)
        self.y = int((self.system.screen_height - (self.system.screen_height * 0.2)) * 0.5)
        self.final_x = self.x
        self.final_y = self.y
        self.alpha = 0
        self.final_alpha = 0

    def set_text(self, text):
        self.text = text
        self.drawlevel = 4
        
    # Draw level 4 - Remake
    def remake(self):
        unit = self.system.screen_height
        self.surface_o.fill((255, 255, 255))
        self.surface_o.set_alpha(191)
        text = self.text

        # 誊写描述
        text_length = len(text)
        if text_length > 0:
            text_size = int(foundtextsize(text_length, self.length_o - 50, self.height_o - 20, 20))
            sx = 25
            sy = 10
            text_index = 0
            while text_index < text_length:
                char = text[text_index]
                if (len(char) == len(char.encode())):
                    char_size = int(text_size * 0.5)
                else:
                    char_size = text_size
                if (sx + char_size > self.length_o - 25):
                    sx = 25
                    sy = sy + text_size
                char_sur = self.system.font[1].render(char, True, (0, 0, 0))
                char_sur_resized = pygame.transform.smoothscale(char_sur, (char_size, text_size))
                self.surface_o.blit(char_sur_resized, (sx, sy))
                text_index = text_index + 1
                sx = sx + char_size

    # Draw level 2 - Resize
    def resize(self):
        unit = self.system.screen_height
        self.height_f = unit * 0.2
        self.length_f = self.height_f * self.length_o / self.height_o

        self.surface_f = pygame.transform.smoothscale(self.surface_o, (int(self.length_f), int(self.height_f)))

    # Draw level 0 - Draw
    def update(self, time):
        # Change position
        speed_c = 50 * time / 1000
        dis = (((self.x - self.final_x) ** 2) + ((self.y - self.final_y) ** 2)) ** (0.5)
        if (dis <= speed_c):
            self.x = self.final_x
            self.y = self.final_y
        else:
            speed_v = (dis * time / 1000 * 5)
            scale = (dis - (speed_c + speed_v)) / dis
            self.x = int((self.x - self.final_x) * scale + self.final_x)
            self.y = int((self.y - self.final_y) * scale + self.final_y)

        # Change color
        speed_color = 255 * time / 1000
        if abs(self.alpha - self.final_alpha) < speed_color:
            self.alpha = int(self.final_alpha)
        else:
            if self.alpha > self.final_alpha:
                self.alpha = int(self.alpha - speed_color)
            else:
                self.alpha = int(self.alpha + speed_color)
        
        return True
    
    def draw(self):
        # 0:nothong 1:repos 2:resize 3:rewords 4:remake 5:reload
        if (self.drawlevel >= 4):
            self.remake()
        if (self.drawlevel >= 2):
            self.resize()

        if self.alpha == 0:
            self.lockcreature = False
            return False

        self.surface_f.set_alpha(self.alpha)
        self.system.screen.blit(self.surface_f, (int(self.x), int(self.y)))

    # 判定鼠标是否在卡图内
    def inside(self, x, y):
        if self.alpha == 0:
            return False
        
        sx = self.x
        sy = self.y
        ex = self.x + self.length
        ey = self.y + self.height
        return ((x >= sx) and (x <= ex) and (y >= sy) and (y <= ey))

    # 处理事件
    def deal(self, event):
        if self.alpha == 0:
            return False
        
        # 鼠标悬停
        if (event.type == MOUSEMOTION):
            x, y = event.pos
            self.repos(x, y)
            

    def repos(self, mouse_x, mouse_y):
        cx, cy = self.get_center(mouse_x, mouse_y)
        self.final_x = int(cx - (self.length_f / 2))
        self.final_y = int(cy - (self.height_f / 2))


    # 被选择
    def get_center(self, mouse_x, mouse_y):
        screen_center_x = self.system.screen_length / 2
        screen_center_y = self.system.screen_height / 2
        min_center_x = self.length_f / 2
        min_center_y = self.height_f / 2
        max_center_x = self.system.screen_length - min_center_x
        max_center_y = self.system.screen_height - min_center_y
        

        # 屏幕中心
        if (mouse_x == screen_center_x) and (mouse_y == screen_center_y):
            center_x = screen_center_x
            center_y = min_center_y
            return center_x, center_y

        # 轴心线
        if (mouse_x == screen_center_x) and (mouse_y > screen_center_y):
            center_x = screen_center_x
            center_y = min_center_y
            return center_x, center_y
        
        if (mouse_x == screen_center_x) and (mouse_y < screen_center_y):
            center_x = screen_center_x
            center_y = max_center_y
            return center_x, center_y
        
        if (mouse_x > screen_center_x) and (mouse_y == screen_center_y):
            center_x = min_center_x
            center_y = screen_center_y
            return center_x, center_y
        
        if (mouse_x < screen_center_x) and (mouse_y == screen_center_y):
            center_x = max_center_x
            center_y = screen_center_y
            return center_x, center_y

        # 其他
        mouse_rel_x = mouse_x - screen_center_x
        mouse_rel_y = mouse_y - screen_center_y

        if (mouse_rel_x > 0) and (mouse_rel_y > 0):
            cal_rel_x = min_center_x - screen_center_x
            cal_rel_y = min_center_y - screen_center_y
            pot_rel_x = (mouse_rel_x / mouse_rel_y) * cal_rel_y
            pot_rel_y = (mouse_rel_y / mouse_rel_x) * cal_rel_x
            ans_rel_x = max(cal_rel_x, pot_rel_x)
            ans_rel_y = max(cal_rel_y, pot_rel_y)
            center_x = ans_rel_x + screen_center_x
            center_y = ans_rel_y + screen_center_y
            return center_x, center_y

        if (mouse_rel_x > 0) and (mouse_rel_y < 0):
            cal_rel_x = min_center_x - screen_center_x
            cal_rel_y = max_center_y - screen_center_y
            pot_rel_x = (mouse_rel_x / mouse_rel_y) * cal_rel_y
            pot_rel_y = (mouse_rel_y / mouse_rel_x) * cal_rel_x
            ans_rel_x = max(cal_rel_x, pot_rel_x)
            ans_rel_y = min(cal_rel_y, pot_rel_y)
            center_x = ans_rel_x + screen_center_x
            center_y = ans_rel_y + screen_center_y
            return center_x, center_y

        if (mouse_rel_x < 0) and (mouse_rel_y > 0):
            cal_rel_x = max_center_x - screen_center_x
            cal_rel_y = min_center_y - screen_center_y
            pot_rel_x = (mouse_rel_x / mouse_rel_y) * cal_rel_y
            pot_rel_y = (mouse_rel_y / mouse_rel_x) * cal_rel_x
            ans_rel_x = min(cal_rel_x, pot_rel_x)
            ans_rel_y = max(cal_rel_y, pot_rel_y)
            center_x = ans_rel_x + screen_center_x
            center_y = ans_rel_y + screen_center_y
            return center_x, center_y

        if (mouse_rel_x < 0) and (mouse_rel_y < 0):
            cal_rel_x = max_center_x - screen_center_x
            cal_rel_y = max_center_y - screen_center_y
            pot_rel_x = (mouse_rel_x / mouse_rel_y) * cal_rel_y
            pot_rel_y = (mouse_rel_y / mouse_rel_x) * cal_rel_x
            ans_rel_x = min(cal_rel_x, pot_rel_x)
            ans_rel_y = min(cal_rel_y, pot_rel_y)
            center_x = ans_rel_x + screen_center_x
            center_y = ans_rel_y + screen_center_y
            return center_x, center_y
            
            








                
