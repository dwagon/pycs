""" Warlock """
from typing import Any
import colors

# from pycs.spells import Command
from pycs.character import Character
from pycs.constant import ActionType
from pycs.constant import SpellType
from pycs.constant import Stat
from pycs.spell import SpellAction
from pycs.spells import BurningHands
from pycs.spells import EldritchBlast
from pycs.spells import Fireball
from pycs.spells import Frostbite
from pycs.spells import HellishRebuke
from pycs.spells import PoisonSpray
from pycs.spells import ScorchingRay
from pycs.spells import Shatter
from pycs.spells import Thunderclap


##############################################################################
class Warlock(Character):
    """Warlock class"""

    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "str": 8,
                "dex": 14,
                "con": 14,
                "int": 12,
                "wis": 11,
                "cha": 17,
                "actions": [],
                "effects": [],
                "stat_prof": [Stat.WIS, Stat.CHA],
                "spellcast_bonus_stat": Stat.CHA,
                "action_preference": {
                    SpellType.RANGED: 5,
                    SpellType.MELEE: 3,
                    ActionType.RANGED: 2,
                    ActionType.MELEE: 1,
                },
            }
        )
        level = kwargs.get("level", 1)
        if level >= 1:
            kwargs["hp"] = 10
            kwargs["actions"].append(EldritchBlast())
            kwargs["actions"].append(Frostbite())
            kwargs["actions"].append(PoisonSpray())
            kwargs["actions"].append(BurningHands())
            kwargs["actions"].append(HellishRebuke())
            self.spell_slots = 1
        if level >= 2:
            self.spell_slots = 2
            kwargs["hp"] = 17
            kwargs["actions"].append(ScorchingRay())
        if level >= 3:
            kwargs["hp"] = 24
        if level >= 4:
            kwargs["hp"] = 31
            kwargs["actions"].append(Shatter())
            kwargs["actions"].append(Thunderclap())
            kwargs["cha"] = 19
        if level >= 5:
            kwargs["hp"] = 38
            kwargs["actions"].append(Fireball())

        super().__init__(**kwargs)
        # L2
        # self.add_action(Command())
        # Agonizing Blast
        # When you cast eldritch blast, add your Charisma modifier to the
        # damage it deals on a hit.
        # Armor of Shadows
        # You can cast mage armor on yourself at will, without expending
        # a spell slot or material components.

        # L3
        # Pact Boon: Pact of the Blades
        # Summon magical weapon

    ##########################################################################
    def report(self) -> None:
        super().report()
        print(f"|  Spells: {self.spell_slots}")

    ########################################################################
    def spell_available(self, spell: SpellAction) -> bool:
        """Do we have enough slots to cast a spell"""
        if spell.level == 0:
            return True
        if self.spell_slots > 0:
            return True
        return False

    ########################################################################
    def cast(self, spell: SpellAction) -> bool:
        """Cast a spell"""
        if spell.level == 0:  # Cantrip
            return False
        self.spell_slots -= 1
        return True

    ########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a warlock looks like in the arena"""
        if self.is_alive():
            return colors.blue("W", bg="green")
        return colors.blue("W", bg="red")


# EOF
