""" https://www.dndbeyond.com/classes/rogue """
import colors
from pycs.action import Action
from pycs.character import Character
from pycs.constant import ActionCategory
from pycs.constant import Race
from pycs.constant import Stat
from pycs.effect import Effect
from pycs.gear import Leather
from pycs.gear import Potion_Healing
from pycs.gear import Longbow
from pycs.gear import Shortsword


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
                "stat_prof": [Stat.DEX, Stat.INT],
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

        self.add_gear(Shortsword())
        self.add_gear(Potion_Healing(ammo=2))
        self.add_gear(Longbow())
        self.add_gear(Leather())

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
    def heuristic(self):
        """Should we do this - prob could be smarter, but at the moment
        just do it for the first attack"""
        return 1

    ##########################################################################
    def hook_predmg(self, **kwargs):
        """Half damage"""
        print("Using uncanny dodge to reduce damage")
        return int(kwargs.get("dmg") / 2)

    ##########################################################################
    def perform_action(self):
        """Need to define but nothing to do"""


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
    def heuristic(self):
        """Should we do this"""
        return 0
        # Don't know how to implement this yet

    ##########################################################################
    def perform_action(self):
        """Not implemented yet"""


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
        if allies_adjacent and attack.has_disadvantage(target, rnge):
            print("but it doesn't matter as we have disadvantage")
            allies_adjacent = False

        if not allies_adjacent:
            if not attack.has_advantage(target, rnge):
                return ("", 0, None)
            print("We have advantage on attack")
        self._used_this_turn = True
        return (self.source.sneak_attack_dmg, 0, None)


# EOF
