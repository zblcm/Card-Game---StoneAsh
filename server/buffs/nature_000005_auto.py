from const import *
from event import *



def init(self):
    self.typ = BUFF_DYNAMIC
    self.original = True
    self.visable = False
    self.name = "自动潜行"
    self.description = "在召唤出来的回合获得永久潜行。"

    def after_move(self, old_event):
        if (self.card in old_event.param[0]) and (old_event.param[1] == PLACE_FIELD):
            hidenum = 0
            hidebuff = None
            for buff in self.card.buffs:
                if (buff.filename == "nature_000005"):
                    hidenum = buff.turnleft
                    hidebuff = buff
            if hidenum > 0:
                hidebuff.turnleft == -1
            if hidenum == 0:
                buff = Buff(self.system, "nature_000005", self.card, self.card)
                buff.turnleft == -1
                self.card.add_buff(buff)
        return True
    self.after_move = after_move
