from const import *
from importlib.machinery import SourceFileLoader



class Card:
    def __init__(self, system, number, mode = True, player = None):
        self.system = system
        self.number = number
        self.original = True

        # 设置什么情况下不能使用
        def default_unusable(card):
            return False
        self.unusable = default_unusable
        
        if mode:
            self.buffs = []
            self.player = player
            self.source = player
            self.place = PLACE_VOID

            # 设置什么情况下被沉默
            def default_disabled(card):
                for buff in card.buffs:
                    if buff.flag_slienced:
                        return True
                return False

            # 设置什么情况下不能被选择
            def default_unselectable(card, player):
                if card.player == player:
                    return False
                for buff in card.buffs:
                    if buff.flag_cannotbetarget:
                        return True
                return False

            # 设置什么情况下不能被攻击
            def default_unattackable(card):
                for buff in card.buffs:
                    if buff.flag_cannotbeattack:
                        return True
                return False

            # 设置什么情况下不能攻击
            def default_cannotattack(card):
                for buff in card.buffs:
                    if buff.flag_cannotattack:
                        return True
                return False
            
            self.disabled = default_disabled
            self.unselectable = default_unselectable
            self.unattackable = default_unattackable
            self.cannotattack = default_cannotattack
        
        file = SourceFileLoader("module.name", "cards/c%010d.py" % number).load_module()
        file.init(self, mode)

    def add_buff(self, buff):
        #print("%s 添加了 %s" % (self.name, buff.name))
        self.buffs.append(buff)
        if buff.oncreate:
            buff.oncreate(buff)
        #print("%s 拥有 %s" % (self.name, self.buffs_string()))

    def remove_buff(self, buff):
        #print("%s 移除了 %s" % (self.name, buff.name))
        if buff.onremove:
            buff.onremove(buff)
        self.buffs.remove(buff)
        #print("%s 还剩 %s" % (self.name, self.buffs_string()))
        
    def buffs_string(self):
        s = ""
        for buff in self.buffs:
            s = s + " " + buff.name
        return s
        
