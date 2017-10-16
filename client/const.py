# Originally, bit operation can be used on this
# Place
PLACE_DECK = 0
PLACE_HAND = 1
PLACE_FIELD = 2
PLACE_GRAVE = 3
PLACE_VOID = 4

# Card Type
CARD_CREATURE = 0
CARD_SPELL = 1

# Card Subtype
SUBTYPE_BASIC = 0
SUBTYPE_DEVIL = 1
SUBTYPE_ILLUSION = 2
SUBTYPE_ELEMENT = 3
SUBTYPE_BEAST = 4
SUBTYPE_HUMAN = 5
SUBTYPE_MIGICIAN = 6
SUBTYPE_DEMIGOD = 7
SUBTYPE_GOD = 8
SUBTYPE_DRAGON = 9

SUBTYPE_BOOK = 100

# Buff Type
BUFF_STATIC = 0
BUFF_DYNAMIC = 1

# Event Type
EVENT_LOSE = 0
EVENT_PLAYEROPERATION = 1
EVENT_CHANGEMANA = 2
EVENT_JUMPTURN = 3

EVENT_PLAYERSELECT = 4
EVENT_TURNSTART = 5
EVENT_TURNOVER = 6
EVENT_MOVE = 7
EVENT_DRAW = 8
EVENT_DAMAGE = 9
EVENT_KILL = 10

EVENT_USECARD = 11
EVENT_ATTACK = 12
EVENT_COSTMANA = 13
EVENT_HEAL = 14

# Damage Type
DAMAGE_PHYSICAL = 0
DAMAGE_MAGICAL = 1

# Reason
REASON_NATURAL = 0
REASON_SPELL = 1
REASON_ABILITY = 2

# Message Type
MESSAGE_BASE = 0
MESSAGE_SERVER = 1
MESSAGE_STATE = 2
MESSAGE_OPERATE = 3
MESSAGE_SELECT = 4
MESSAGE_OPERATE_ASK = 5
MESSAGE_SELECT_ASK = 6
MESSAGE_YELL = 7
MESSAGE_PLAY_EFFECT = 8


def hasconst(power, num):
    return (power >> num) & 1

def haspower(power1, power2):
    return (power1 | power2) == power1

def enpower(nums):
    ans = 0
    for num in nums:
        ans = ans + (1 << nums)
    return ans

def depower(power):
    ans = []
    i = 0
    while power > 0:
        if (power & 1) == 1:
            ans.append(i)
        i = i + 1
        power = power >> 1
    return ans
    
if __name__ == "__main__":
    print(depower(32))

