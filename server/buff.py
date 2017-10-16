from const import *
from importlib.machinery import SourceFileLoader

class Buff:
    def __init__(self, system, filename, source, card):
        # 需要send的buffs
        self.system = system
        self.filename = filename
        self.image = None
        self.imageinside = False
        self.source = source
        self.card = card
        self.visable = False
        self.original = True    	# Buff能否被复制
        
        self.flag_slienced = False
        self.flag_cannotbetarget = False
        self.flag_cannotbeattack = False
        self.flag_cannotattack = False
        self.flag_taught = False

        self.onplayerselect = False
        self.onturnstart = False
        self.onturnstop = False
        self.oncostmana = False
        
        self.before_draw = False
        self.after_draw = False
        self.before_move = False
        self.after_move = False
        self.before_damage = False
        self.after_damage = False
        self.before_heal = False
        self.after_heal = False
        self.before_kill = False
        self.after_kill = False
        self.before_attack = False
        self.after_attack = False
        self.before_usecard = False
        self.after_usecard = False
        
        self.warcry = False
        self.deadword = False

        self.onremove = False
        self.oncreate = False

        
        #file = SourceFileLoader("module.name", "buffs/b%010d.py" % number).load_module()
        file = SourceFileLoader("module.name", "buffs/%s.py" % filename).load_module()
        file.init(self)

        
