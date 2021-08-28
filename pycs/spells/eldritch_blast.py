"""https://www.dndbeyond.com/spells/eldritch-blast"""

from pycs.spell import AttackSpell
from pycs.constant import SpellType
from pycs.constant import DamageType


##############################################################################
class Eldritch_Blast(AttackSpell):
    """Spell"""

    def __init__(self, **kwargs):
        name = "Eldritch Blast"
        kwargs.update(
            {
                "reach": 120,
                "level": 0,
                "style": SpellType.TOHIT,
                "type": SpellType.RANGED,
                "dmg": ("1d10", 0),
                "dmg_type": DamageType.FORCE,
            }
        )
        super().__init__(name, **kwargs)


# EOF
