""" Handle non-attack Actions """
from collections import namedtuple
from typing import Any, NamedTuple, Optional, TYPE_CHECKING, cast
import dice
from pycs.action import Action
from pycs.constant import SpellType, Stat
from pycs.util import check_args

if TYPE_CHECKING:
    from pycs.creature import Creature

##############################################################################
##############################################################################
##############################################################################
class SpellAction(Action):
    """Spell action"""

    ########################################################################
    def __init__(self, name: str, **kwargs: Any):
        check_args(self._valid_args(), name, kwargs)
        super().__init__(name, **kwargs)
        self.reach = kwargs.get("reach", 0) / 5
        self.type: SpellType = kwargs.get("type", SpellType.UNKNOWN)  # type: ignore
        self.cure_hp = kwargs.get("cure_hp")
        self.level: int = kwargs.get("level", 0)
        self.concentration = kwargs.get("concentration")
        self.caster: "Creature"

    ##########################################################################
    def _valid_args(self) -> set[str]:
        """What is valid in this class for kwargs"""
        return super()._valid_args() | {
            "reach",
            "type",
            "cure_hp",
            "level",
            "concentration",
        }

    ########################################################################
    def is_available(self) -> bool:
        """Is this action available?"""
        return self.owner.spell_available(self)

    ########################################################################
    def failed_save(self, source: "Creature", target: "Creature", dmg: int) -> None:
        """Called when the target failed save"""

    ########################################################################
    def made_save(self, source: "Creature", target: "Creature", dmg: int) -> None:
        """Called when the target made save"""

    ########################################################################
    def is_type(self, *types: SpellType) -> bool:
        """Is this spell of the specified types"""
        return self.type in types

    ########################################################################
    def range(self) -> tuple[int, int]:
        """Return the good / worse range for the spell"""
        return self.reach, self.reach

    ########################################################################
    def spell_modifier(self, attacker: "Creature") -> int:
        """Spell Casting modifier"""
        return attacker.stat_bonus(attacker.spellcast_bonus_stat)

    ########################################################################
    def atk_modifier(self, attacker: "Creature") -> int:
        """Attack modifier"""
        return self.spell_modifier(attacker)

    ########################################################################
    def dmg_modifier(self, attacker: "Creature") -> int:
        """Damage modifier"""
        return 0

    ########################################################################
    def perform_action(self) -> bool:
        """Cast the spell"""
        if not self.owner.spell_available(self):
            return False
        self.owner.cast(self)
        print(f"{self.owner} is casting {self.name}")
        self.caster = self.owner
        if self.concentration and self.caster.concentration:
            self.caster.remove_concentration()
        result = self.cast()
        if self.concentration:
            self.owner.add_concentration(self)
        return result

    ########################################################################
    def heuristic(self) -> int:
        """Should we do the spell"""
        if not self.owner.spell_available(self):
            return 0
        return 1

    ########################################################################
    def cast(self) -> bool:
        """Needs to be replaced"""
        raise NotImplementedError(f"SpellAction.{self.__class__.__name__} needs a cast()")

    ##########################################################################
    def end_concentration(self) -> None:
        """What happens when we stop concentrating"""


##############################################################################
class HealthResult(NamedTuple):
    health: int
    id: int
    target: "Creature"


##############################################################################
def health_level_of_peers(doer: "Creature") -> Optional[HealthResult]:
    """Return the health levels (missing hp) of peers"""
    hurt_peers = [
        HealthResult(_.max_hp - _.hp, id(_), _)
        for _ in doer.arena.my_side(doer.side)
        if _.max_hp != 0
    ]
    if not hurt_peers:
        return None
    hurt_peers.sort(reverse=True)
    return hurt_peers[0]


##############################################################################
def healing_heuristic(doer: "Creature", spell: SpellAction) -> int:
    """Should we cast this"""
    if not doer.spell_available(spell):
        return 0
    peers = health_level_of_peers(doer)
    if not peers:
        return 0
    return peers.health


##############################################################################
def pick_heal_target(doer: "Creature") -> Optional["Creature"]:
    """Who to heal"""
    recip = health_level_of_peers(doer)
    if recip is None:
        return None
    return recip.target


##############################################################################
##############################################################################
##############################################################################
class AttackSpell(SpellAction):
    """A spell attack"""

    ########################################################################
    def __init__(self, name: str, **kwargs: Any):
        check_args(self._valid_args(), name, kwargs)
        super().__init__(name, **kwargs)
        self.style: SpellType = kwargs.get("style", SpellType.TOHIT)
        self.type: SpellType = kwargs.get("type", SpellType.UNKNOWN)
        self.save_stat: Stat = cast(Stat, kwargs.get("save_stat"))
        self.save_dc = kwargs.get("save_dc")

    ##########################################################################
    def _valid_args(self) -> set[str]:
        """What is valid in this class for kwargs"""
        return super()._valid_args() | {"style", "type", "save_stat", "save_dc"}

    ########################################################################
    def stat_dmg_bonus(self, attacker: "Creature") -> int:
        """No spell bonus to damage"""
        return attacker.stat_bonus(attacker.spellcast_bonus_stat)

    ########################################################################
    def roll_dmg(self, victim: "Creature", critical: bool = False) -> int:
        """Special spell damage"""
        if self.style == SpellType.TOHIT:
            return super().roll_dmg(victim, critical)
        dmg = int(dice.roll(self.dmg[0]))
        print(f"{self.owner} rolled {dmg} on {self.dmg[0]} for damage")
        if self.dmg[1]:
            dmg += self.dmg[1]
            print(f"Adding bonus of {self.dmg[1]} -> {dmg}")
        spell_dc = self.save_dc
        if not spell_dc:
            spell_dc = self.owner.spellcast_save
        saved = victim.saving_throw(stat=self.save_stat, dc=spell_dc, effect="unknown")
        if saved:
            if self.style == SpellType.SAVE_HALF:
                dmg = int(dmg / 2)
            if self.style == SpellType.SAVE_NONE:
                dmg = 0
            self.made_save(source=self.owner, target=victim, dmg=dmg)
        else:
            self.failed_save(source=self.owner, target=victim, dmg=dmg)
        return max(dmg, 0)

    ########################################################################
    def heuristic(self) -> int:
        """Should we cast this"""
        if not self.owner.spell_available(self):
            return 0
        pot_target = self.owner.pick_closest_enemy()
        if not pot_target:
            return 0
        if self.owner.distance(pot_target[0]) > self.range()[1]:
            return 0
        return self.max_dmg()

    ########################################################################
    def roll_to_hit(self, target: "Creature") -> tuple[int, bool, bool]:
        """Special spell attack"""
        if self.style == SpellType.TOHIT:
            return super().roll_to_hit(target)
        return 999, False, False

    ########################################################################
    def range(self) -> tuple[int, int]:
        """Return the range of the attack"""
        return self.reach, self.reach

    ########################################################################
    def cast(self) -> bool:
        """Cast the attack spell - overwrite if required"""
        return self.do_attack()


# EOF
