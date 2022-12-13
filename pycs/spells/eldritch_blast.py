"""https://www.dndbeyond.com/spells/eldritch-blast"""

from typing import Any
from pycs.damageroll import DamageRoll
from pycs.spell import AttackSpell
from pycs.constant import SpellType
from pycs.constant import DamageType


##############################################################################
class EldritchBlast(AttackSpell):
    """Spell"""

    def __init__(self, **kwargs: Any):
        name = "Eldritch Blast"
        kwargs.update(
            {
                "reach": 120,
                "level": 0,
                "style": SpellType.TOHIT,
                "type": SpellType.RANGED,
                "dmgroll": DamageRoll("1d10", 0, DamageType.FORCE),
            }
        )
        super().__init__(name, **kwargs)


# EOF
