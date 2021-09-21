"""https://www.dndbeyond.com/spells/spirit-guardians"""

import dice
from pycs.constant import DamageType
from pycs.constant import SpellType
from pycs.constant import Stat
from pycs.effect import Effect
from pycs.spell import SpellAction


##############################################################################
##############################################################################
##############################################################################
class Spirit_Guardians(SpellAction):
    """You call forth spirits to protect you. They flit around you to
    a distance of 15 feet for the duration. If you are good or neutral,
    their spectral form appears angelic or fey (your choice). If you
    are evil, they appear fiendish.

    When you cast this spell, you can designate any number of creatures
    you can see to be unaffected by it. An affected creature's speed
    is halved in the area, and when the creature enters the area for
    the first time on a turn or starts its turn there, it must make a
    Wisdom saving throw. On a failed save, the creature takes 3d8 radiant
    damage (if you are good or neutral) or 3d8 necrotic damage (if you
    are evil). On a successful save, the creature takes half as much
    damage."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Spirit Guardians"
        kwargs.update(
            {
                "reach": 15,
                "level": 3,
                "type": SpellType.RANGED,
                "concentration": SpellType.CONCENTRATION,
            }
        )
        super().__init__(name, **kwargs)

    ##########################################################################
    def heuristic(self):
        """Should we do the spell
        the more people it can effect the more we should do it"""
        if self.owner.has_effect("Spirit Guardian"):
            return 0
        heur = 0
        for enem in self.owner.pick_closest_enemy():
            if self.owner.distance(enem) < self.range()[0]:
                heur += 24  # 3d8
        return heur * 2

    ##########################################################################
    def pick_target(self):
        """Who should we do the spell to"""
        return self.owner

    ##########################################################################
    def cast(self):
        """Do the spell"""
        self.owner.add_effect(SpiritGuardianEffect(caster=self.owner))
        return True

    ##########################################################################
    def end_concentration(self):
        """What happens when we stop concentrating"""
        self.owner.remove_effect("Spirit Guardian")


##############################################################################
##############################################################################
##############################################################################
class SpiritGuardianEffect(Effect):
    """Spirit Guardian Effect"""

    ##########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Spirit Guardian", **kwargs)
        self._victims = set()

    ##########################################################################
    def hook_start_turn(self):
        """Reset who has been affected this turn"""
        self._victims = set()

    ##########################################################################
    def hook_start_in_range(self, creat):
        """Are we in range of the effect"""
        if creat.side == self.caster.side:
            return
        if self.caster.distance(creat) > 15 / 5:
            return
        if creat in self._victims:
            return
        self._victims.add(creat)
        dmg = int(dice.roll("3d8"))
        if creat.saving_throw(Stat.WIS, self.caster.spellcast_save):
            dmg /= 2
        creat.hit(dmg, DamageType.RADIANT, self.caster, False, "Spirit Guardian")


# EOF
