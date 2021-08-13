""" Constants used everywhere """
from enum import Enum


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
class SpellType(Enum):
    """What sort of spell is it"""

    HEALING = "healing"
    ATTACK = "attack"
    BUFF = "buff"


# EOF
