""" Constants used everywhere """
from enum import Enum
from collections import namedtuple


##############################################################################
##############################################################################
##############################################################################
class DamageType(Enum):
    """Damage types"""

    ACID = "acid"
    BLUDGEONING = "bludgeoning"
    COLD = "cold"
    FIRE = "fire"
    FORCE = "force"
    LIGHTNING = "lightning"
    NECROTIC = "necrotic"
    PIERCING = "piercing"
    POISON = "poison"
    PSYCHIC = "psychic"
    RADIANT = "radiant"
    SLASHING = "slashing"
    THUNDER = "thunder"


##############################################################################
##############################################################################
##############################################################################
class Condition(Enum):
    """Conditions"""

    BLINDED = "blinded"
    CHARMED = "charmed"
    DEAFENED = "deafened"
    EXHAUSTION = "exhaustion"
    FRIGHTENED = "frightened"
    GRAPPLED = "grappled"
    INCAPACITATED = "incapacitated"
    INVISIBLE = "invisible"
    PARALYZED = "paralyzed"
    PETRIFIED = "petrified"
    POISONED = "poisoned"
    PRONE = "prone"
    RESTRAINED = "restrained"
    STUNNED = "stunned"
    UNCONSCIOUS = "unconscious"


##############################################################################
##############################################################################
##############################################################################
class Stat(Enum):
    """Ability Scores"""

    STR = "strength"
    DEX = "dexterity"
    CON = "constitution"
    INT = "intelligence"
    WIS = "wisdom"
    CHA = "charisma"


##############################################################################
##############################################################################
##############################################################################
class ActionType(Enum):
    """What sort of action is it"""

    BUFF = "buff"
    HEALING = "healing"
    MELEE = "melee"
    RANGED = "ranged"
    UNKNOWN = "unknown"


##############################################################################
##############################################################################
##############################################################################
class SpellType(Enum):
    """What sort of spell is it"""

    BUFF = "buff"
    HEALING = "healing"
    MELEE = "melee"
    RANGED = "ranged"


##############################################################################
##############################################################################
##############################################################################
class ActionCategory(Enum):
    """What sort of action is it"""

    ACTION = "action"
    BONUS = "bonus"
    MOVE = "move"
    REACTION = "reaction"


##############################################################################
##############################################################################
##############################################################################
class MonsterType(Enum):
    """What sort of Monster is it"""

    BEAST = "beast"
    CELESTIAL = "celestial"
    CONSTRUCT = "construct"
    DRAGON = "dragon"
    ELEMENTAL = "elemental"
    FEY = "fey"
    FIEND = "fiend"
    GIANT = "giant"
    HUMANOID = "humanoid"
    PLANT = "plant"
    UNDEAD = "undead"


##############################################################################
##############################################################################
##############################################################################
class Race(Enum):
    """What race a character is"""

    HUMAN = "Human"
    HALFORC = "Half-Orc"


##############################################################################
##############################################################################
##############################################################################
Damage = namedtuple("Damage", "hp type")
Statistics = namedtuple("Statistics", "name damage damagetype critical")

# EOF
