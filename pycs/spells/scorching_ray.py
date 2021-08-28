"""https://www.dndbeyond.com/spells/scorching-ray"""

import random
from pycs.constant import ActionCategory
from pycs.constant import DamageType
from pycs.constant import SpellType
from pycs.spell import AttackSpell


##############################################################################
class Scorching_Ray(AttackSpell):
    """You create three rays of fire and hurl them at targets within
    range. You can hurl them at one target or several.

    Make a ranged spell attack for each ray. On a hit, the target takes
    2d6 fire damage.

    At Higher Levels. When you cast this spell using a spell slot of
    3rd level or higher, you create one additional ray for each slot
    level above 2nd."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Scorching Ray"
        kwargs.update(
            {
                "category": ActionCategory.ACTION,
                "reach": 120,
                "level": 2,
                "dmg": ("2d6", 0),
                "dmg_type": DamageType.FIRE,
                "style": SpellType.TOHIT,
                "type": SpellType.RANGED,
            }
        )
        super().__init__(name, **kwargs)

    ##########################################################################
    def cast(self, caster):
        """Do the spell"""
        targets = []
        for enemy in caster.pick_closest_enemy():
            if caster.distance(enemy) < self.range()[0]:
                targets.append(enemy)
        for _ in range(3):
            target = random.choice(targets)
            print(f"Targeting {target} with Scorching Ray")
            to_hit, crit_hit, crit_miss = self.roll_to_hit(caster, target, 999)
            if to_hit >= target.ac and not crit_miss:
                dmg = self.roll_dmg(caster, target)
                target.hit(dmg, self.dmg_type, caster, crit_hit, self.name)
            else:
                print(
                    f"Scorching Ray missed {target} (Rolled {to_hit} < AC: {target.ac})"
                )

    ##########################################################################
    def pick_target(self, doer):
        """Who should we do the spell to"""
        for enemy in doer.pick_closest_enemy():
            if doer.distance(enemy) < self.range()[0]:
                return enemy
        return None

    ##########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        targets = 0
        for enemy in doer.pick_closest_enemy():
            if doer.distance(enemy) < self.range()[0]:
                targets += 1
        return min(3, targets)


# EOF
