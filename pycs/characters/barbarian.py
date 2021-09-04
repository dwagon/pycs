""" Barbarian """
import colors
from pycs.gear import Greataxe
from pycs.gear import Potion_Healing
from pycs.gear import Javelin
from pycs.gear import Hide
from pycs.action import Action
from pycs.attack import MeleeAttack
from pycs.character import Character
from pycs.constant import ActionCategory
from pycs.constant import ActionType
from pycs.constant import DamageType
from pycs.constant import Stat
from pycs.effect import Effect


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
        self.add_gear(Greataxe(magic_bonus=3))
        self.add_gear(Javelin(ammo=3))
        self.add_gear(Hide())
        self.add_gear(Potion_Healing(ammo=1))
        self.add_action(BarbarianRage())
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
        self.category = ActionCategory.BONUS

    ########################################################################
    def pick_target(self, doer):
        """Who do we do it to"""
        return doer

    ########################################################################
    def heuristic(self, doer):
        """Should we do it"""
        if doer.has_effect("Rage"):
            return 0
        return 10

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
    def hook_source_additional_damage(self, attack, source, target):
        """Rage causes dangerous things"""
        if issubclass(attack.__class__, MeleeAttack):
            return ("", 2, None)
        return ("", 0, None)

    ########################################################################
    def hook_saving_throw(self, stat, **kwargs):
        """Advantage on strength"""
        eff = super().hook_saving_throw(stat, **kwargs)
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
