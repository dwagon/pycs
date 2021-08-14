""" https://www.dndbeyond.com/spells/guiding-bolt """

from attacks import SpellAttack
from constants import DamageType
from constants import SpellType


##############################################################################
class Guiding_Bolt(SpellAttack):
    """Spell"""

    def __init__(self, **kwargs):
        name = "Guiding Bolt"
        kwargs.update(
            {
                "type": SpellType.RANGED,
                "reach": 120,
                "bonus": 5,
                "dmg": ("4d6", 5),
                "dmg_type": DamageType.RADIANT,
                "level": 1,
            }
        )
        super().__init__(name, **kwargs)


# EOF
