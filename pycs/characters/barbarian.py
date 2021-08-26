""" Barbarian """
import colors
from pycs.action import Action
from pycs.attack import MeleeAttack
from pycs.attack import RangedAttack
from pycs.constant import ActionType
from pycs.constant import DamageType
from pycs.constant import Stat
from pycs.effect import Effect
from pycs.character import Character


##############################################################################
##############################################################################
##############################################################################
class Barbarian(Character):
    """Barbarian class"""

    ##########################################################################
    def __init__(self, level, **kwargs):
        self.level = level
        kwargs.update(
            {
                "str": 16,
                "dex": 14,
                "con": 15,
                "int": 11,
                "wis": 13,
                "cha": 9,
                "ac": 16,
                "action_preference": {
                    BarbarianRage: 9,
                    ActionType.MELEE: 8,
                    ActionType.RANGED: 4,
                },
            }
        )
        if level >= 1:
            kwargs["hp"] = 14
        if level >= 2:
            # Reckless attack
            # Danger Sense
            kwargs["hp"] = 23
        if level >= 3:
            kwargs["hp"] = 32
            # Primal path - Path of the beserker
            # Frenzy
        if level >= 4:
            kwargs["hp"] = 41
            kwargs["str"] = 18
        if level >= 5:
            kwargs["hp"] = 50
            kwargs["speed"] = 40
            kwargs["attacks_per_action"] = 2
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Greataxe",
                reach=5,
                dmg=("1d12", 0),
                dmg_type=DamageType.SLASHING,
            )
        )
        self.add_action(
            RangedAttack(
                "Javelin",
                reach=5,
                ammo=3,
                dmg=("1d6", 0),
                dmg_type=DamageType.PIERCING,
            )
        )
        self.add_bonus_action(BarbarianRage())
        if level >= 2:
            self.add_effect(BarbarianDangerSenseEffect())

    ##########################################################################
    def report(self):
        """Character Report"""
        super().report()
        javs = self.pick_attack_by_name("Javelin")
        print(f"|  Javelins: {javs.ammo}")

    ##########################################################################
    def shortrepr(self):
        """What a fighter looks like in the arena"""
        if self.is_alive():
            return colors.blue("B", bg="green")
        return colors.blue("B", bg="red")


##############################################################################
##############################################################################
##############################################################################
class BarbarianRage(Action):
    """Shield biting stuff"""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Barbarian Rage", **kwargs)
        self.type = ActionType.BUFF

    ########################################################################
    def pick_target(self, doer):
        """Who do we do it to"""
        return doer

    ########################################################################
    def heuristic(self, doer):
        if doer.has_effect("Rage"):
            return 0
        return 2

    ########################################################################
    def perform_action(self, source):
        """Do the action"""
        source.add_effect(BarbarianRageEffect())


##############################################################################
##############################################################################
##############################################################################
class BarbarianFrenziedRageEffect(Effect):
    """While raging, you can choose to frenzy. You can make a single
    melee weapon attack as a bonus action on each of your turns after
    this one. When your rage ends, you suffer one level of exhaustion."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Frenzied Rage", **kwargs)


##############################################################################
##############################################################################
##############################################################################
class BarbarianRageEffect(Effect):
    """You gain advantage on STR checks and saving throws (not attacks),
    +2 melee damage with STR weapons, resistance to bludgeoning, piercing,
    slashing damage. You can't cast or concentrate on spells while
    raging."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Rage", **kwargs)

    ########################################################################
    def hook_being_hit(self, dmg, dmgtype):
        """Mod damage"""
        if dmgtype in (
            DamageType.BLUDGEONING,
            DamageType.PIERCING,
            DamageType.SLASHING,
        ):
            return int(dmg / 2)
        return dmg

    ########################################################################
    def hook_source_additional_melee_damage(self):
        return "", 2, None

    ########################################################################
    def hook_saving_throw(self, stat):
        """Advantage on strength"""
        eff = super().hook_saving_throw(stat)
        if stat == Stat.STR:
            eff.update({"advantage": True})
        return eff


##############################################################################
##############################################################################
##############################################################################
class BarbarianDangerSenseEffect(Effect):
    """You have advantage on DEX saving throws against effects that you
    can see while not blinded, deafened, or incapacitated."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Danger Sense", **kwargs)


##############################################################################
##############################################################################
##############################################################################
class BarbarianRecklessAttack(Effect):
    """When you make your first attack on your turn, you can decide to
    attack recklessly, giving you advantage on melee weapon attack rolls
    using STR during this turn, but attack rolls against you have
    advantage until your next turn."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Reckless Attack", **kwargs)


# EOF
