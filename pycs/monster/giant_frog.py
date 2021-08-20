""" Giant Frog Monster Class """
import colors
import dice
from attacks import MeleeAttack
from constants import Condition
from constants import DamageType
from constants import MonsterType
from constants import Stat
from effect import Effect
from .monster import Monster


##############################################################################
class GiantFrog(Monster):
    """Giant Frog - https://www.dndbeyond.com/monsters/giant-frog"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "4d8"
        kwargs.update(
            {
                "ac": 11,
                "speed": 30,
                "type": MonsterType.BEAST,
                "str": 12,
                "dex": 13,
                "con": 11,
                "int": 2,
                "wis": 10,
                "cha": 3,
            }
        )
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Bite",
                reach=5,
                dmg=("1d6", 0),
                dmg_type=DamageType.PIERCING,
                heuristic=self.frog_bite,
                side_effect=self.swallow,
            )
        )
        self._swallowed = None

    ##########################################################################
    def swallow(self, source, target):  # pylint: disable=unused-argument
        """bite and swallow the target"""
        # Bite. The target is grappled (escape DC 11). Until this grapple ends, the
        # target is restrained, and the frog can't bite another target.

        target = self.target
        if self.has_grappled == target and self._swallowed is None:
            print(f"{self} swallowed {target}")
            target.add_effect(GiantFrogSwallowEffect())
            self.has_grappled = None
            self._swallowed = target
            target.remove_condition(Condition.GRAPPLED)
            return

        svth = target.saving_throw(Stat.STR, 11)
        if not svth:
            print(f"{target} to grappled by {self}")
            target.add_condition(Condition.GRAPPLED)
            self.has_grappled = target

    ##########################################################################
    def frog_bite(self, actor):  # pylint: disable=unused-argument
        """When is it good to bite"""
        if self.has_grappled:
            return 0
        return 1

    ##########################################################################
    def fallen_unconscious(self, dmg, dmg_type, critical):
        """Frog has died"""
        if self._swallowed:
            self._swallowed.remove_condition(Condition.RESTRAINED)
            self._swallowed.remove_condition(Condition.BLINDED)
            self._swallowed.remove_effect("Giant Frog Swallow")
            print(f"{self._swallowed} escapes from being swallowed by {self.name}")
        super().fallen_unconscious(dmg, dmg_type, critical)

    ##########################################################################
    def shortrepr(self):
        """What it looks like on the arena"""
        if self.is_alive():
            return colors.green("F")
        return colors.green("F", bg="red")


##############################################################################
##############################################################################
##############################################################################
class GiantFrogSwallowEffect(Effect):
    """Swallow. The frog makes one bite attack against a Small or smaller
    target it is grappling. If the attack hits, the target is swallowed,
    and the grapple ends. The swallowed target is blinded and restrained,
    it has total cover against attacks and other effects outside the
    frog, and it takes 5 (2d4) acid damage at the start of each of the
    frog's turns. The frog can have only one target swallowed at a time.
    If the frog dies, a swallowed creature is no longer restrained by
    it and can escape from the corpse using 5 feet of movement, exiting
    prone."""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Giant Frog Swallow", **kwargs)
        self.target = None

    ##########################################################################
    def initial(self, target):
        """Initial effect"""
        self.target = target
        target.add_condition(Condition.RESTRAINED)
        target.add_condition(Condition.BLINDED)

    ##########################################################################
    def hook_start_turn(self):
        dmg = int(dice.roll("2d4"))
        self.target.hit(dmg, DamageType.ACID, self, False)
        print(f"{self.target} hurt by {dmg} acid from being swallowed by Giant Frog")


# EOF
