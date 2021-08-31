""" https://www.dndbeyond.com/classes/rogue """
import colors
from pycs.action import Action
from pycs.attack import MeleeAttack
from pycs.attack import RangedAttack
from pycs.character import Character
from pycs.constant import ActionCategory
from pycs.constant import DamageType
from pycs.constant import Race
from pycs.constant import Stat
from pycs.effect import Effect


##############################################################################
##############################################################################
##############################################################################
class Rogue(Character):
    """Rogue class"""

    def __init__(self, level=1, **kwargs):
        self.level = level
        kwargs.update(
            {
                "race": Race.ELF,
                "str": 12,
                "dex": 17,
                "con": 13,
                "int": 9,
                "wis": 14,
                "cha": 10,
                "ac": 14,
                "speed": 35,
            }
        )
        if level >= 1:
            kwargs["hp"] = 9
        if level >= 2:
            kwargs["hp"] = 15
        if level >= 3:
            kwargs["hp"] = 21
        if level >= 4:
            kwargs["hp"] = 31
            kwargs["dex"] = 18
            kwargs["con"] = 14
        if level >= 5:
            kwargs["hp"] = 38

        super().__init__(**kwargs)

        self.sneak_attack_dmg = "1d6"
        if level >= 2:
            self.add_effect(SneakAttack())
        if level >= 3:
            self.sneak_attack_dmg = "2d6"
            self.add_action(CunningAction())
        if level >= 4:
            pass
        if level >= 5:
            self.sneak_attack_dmg = "3d6"
            self.add_action(UncannyDodge())

        self.add_action(
            MeleeAttack(
                "Shortsword",
                reach=5,
                dmg=("1d6", 0),
                use_stat=Stat.DEX,
                dmg_type=DamageType.PIERCING,
            )
        )
        self.add_action(
            RangedAttack(
                "Longbow",
                s_range=150,
                l_range=600,
                dmg=("1d8", 0),
                dmg_type=DamageType.PIERCING,
            )
        )

    ##########################################################################
    def shortrepr(self):
        """What a rogue looks like in the arena"""
        if self.is_alive():
            return colors.black("R", bg="green")
        return colors.blue("R", bg="red")


##############################################################################
##############################################################################
##############################################################################
class UncannyDodge(Action):
    """When an attacker that you can see hits you with an attack,
    you can use your reaction to halve the attack’s damage against
    you."""

    ##########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Uncanny Dodge", **kwargs)
        self.category = ActionCategory.REACTION

    ##########################################################################
    def hook_predmg(self, **kwargs):
        """Half damage"""
        print("Using uncanny dodge to reduce damage")
        return int(kwargs.get("dmg") / 2)


##############################################################################
##############################################################################
##############################################################################
class CunningAction(Action):
    """You can take a bonus action on each of your turns to take the
    Dash, Disengage, or Hide action."""

    ##########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Cunning Action", **kwargs)
        self.category = ActionCategory.BONUS

    ##########################################################################
    def heuristic(self, doer):
        """Should we do this"""
        return 0
        # Don't know how to implement this yet


##############################################################################
##############################################################################
##############################################################################
class SneakAttack(Effect):
    """Beginning at 1st level, you know how to strike subtly and exploit
    a foe’s distraction. Once per turn, you can deal an extra 1d6 damage
    to one creature you hit with an attack if you have advantage on the
    attack roll. The attack must use a finesse or a ranged weapon.

    You don’t need advantage on the attack roll if another enemy of the
    target is within 5 feet of it, that enemy isn’t incapacitated, and
    you don’t have disadvantage on the attack roll.

    The amount of the extra damage increases as you gain levels in this
    class, as shown in the Sneak Attack column of the Rogue table."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Sneak Attack", **kwargs)
        self._used_this_turn = False

    ########################################################################
    def hook_start_turn(self):
        """Start the turn"""
        self._used_this_turn = False

    ########################################################################
    def hook_source_additional_damage(self, attack, source, target):
        """Do the sneak attack"""
        if self._used_this_turn:
            return ("", 0, None)

        if target.state != "OK":
            return ("", 0, None)

        allies_adjacent = False
        allies = [_ for _ in target.pick_closest_enemy() if _ != source]
        if allies:
            if allies[0].distance(target) <= 1:
                allies_adjacent = True
                print(f"Ally {allies[0]} adjacent to {target}")

        rnge = source.distance(target)
        if allies_adjacent and attack.has_disadvantage(source, target, rnge):
            print("but it doesn't matter as we have disadvantage")
            allies_adjacent = False

        if not allies_adjacent:
            if not attack.has_advantage(source, target, rnge):
                return ("", 0, None)
            else:
                print("We have advantage on attack")
        self._used_this_turn = True
        return (self.source.sneak_attack_dmg, 0, None)


# EOF
