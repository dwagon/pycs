"""https://www.dndbeyond.com/spells/bless"""

from typing import Any, Optional
from unittest.mock import patch
import dice
from pycs.creature import Creature
from pycs.constant import SpellType
from pycs.constant import ActionCategory
from pycs.constant import Stat
from pycs.effect import Effect
from pycs.spell import SpellAction
from pycs.spells.spelltest import SpellTest


##############################################################################
##############################################################################
##############################################################################
class Bless(SpellAction):
    """You bless up to three creatures of your choice within range.
    Whenever a target makes an attack roll or a saving throw before the
    spell ends, the target can roll a d4 and add the number rolled to
    the attack roll or saving throw.

    At Higher Levels. When you cast this spell using a spell slot of
    2nd level or higher, you can target one additional creature for
    each slot level above 1st."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        name = "Bless"
        kwargs.update(
            {
                "reach": 30,
                "level": 1,
                "type": SpellType.BUFF,
                "concentration": SpellType.CONCENTRATION,
            }
        )
        self._affected: list[Creature] = []
        super().__init__(name, **kwargs)

    ###########################################################################
    def heuristic(self) -> int:
        """Should we do the spell"""
        # The more applicable targets the more likely we should do it
        close = 0
        for targ in self.owner.arena.my_side(self.owner.side):
            if self.owner.distance(targ) <= self.range()[0]:
                if self.owner.has_effect("Bless"):
                    continue
                close += 2
        return close

    ###########################################################################
    def pick_target(self) -> Optional[Creature]:
        """Who should we do the spell to"""
        # Improve this
        return self.owner

    ###########################################################################
    def cast(self) -> bool:
        """Do the spell"""
        self._affected = []
        targets = 3
        for friend in self.owner.arena.my_side(self.owner.side):
            if friend.has_effect("Bless"):
                continue
            targets -= 1
            print(f"{friend} is now Blessed")
            friend.add_effect(BlessEffect(cause=self.owner))
            self._affected.append(friend)
            if targets <= 0:
                break
        return True

    ##########################################################################
    def end_concentration(self) -> None:
        """What happens when we stop concentrating"""
        for pers in self._affected:
            pers.remove_effect("Bless")


##############################################################################
##############################################################################
##############################################################################
class BlessEffect(Effect):
    """The Effect of the bless spell"""

    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Bless", **kwargs)

    def hook_attack_to_hit(self, **kwargs: Any) -> int:
        """Mod attack roll"""
        eff = super().hook_attack_to_hit(**kwargs)
        eff += int(dice.roll("d4"))
        return eff

    def hook_saving_throw(self, stat: Stat, **kwargs: Any) -> dict:
        """Mod saving throw"""
        eff = super().hook_saving_throw(stat, **kwargs)
        eff.update({"bonus": int(dice.roll("d4"))})
        print(f"Bless adds {eff['bonus']} to saving throw")
        return eff


##############################################################################
##############################################################################
##############################################################################
class TestBless(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self) -> None:
        """setup"""
        super().setUp()
        self.caster.add_action(Bless())

    ##########################################################################
    def test_cast(self) -> None:
        """test casting"""
        self.assertFalse(self.friend.has_effect("Bless"))
        self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=False)
        self.assertTrue(self.friend.has_effect("Bless"))

    ##########################################################################
    def test_saving_throw_effect(self) -> None:
        """test the bless effect on saving throws"""
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 9
            save = self.friend.saving_throw(Stat.CON, 10)
            self.assertFalse(save)
        self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=False)
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 9
            save = self.friend.saving_throw(Stat.CON, 10)
            self.assertTrue(save)

    ##########################################################################
    def test_to_hit_effect(self) -> None:
        """test the bless effect on attack rolls"""
        act = self.friend.actions[0]
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 9
            to_hit, _, _ = act.roll_to_hit(self.enemy)
        self.assertEqual(to_hit, 9)

        self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=False)
        act = self.friend.actions[0]
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 9
            to_hit, _, _ = act.roll_to_hit(self.enemy)
        self.assertGreaterEqual(to_hit, 10)

    ##########################################################################
    def test_concentration(self) -> None:
        """Does the effect remove when we end concentration"""
        self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=False)
        self.assertTrue(self.friend.has_effect("Bless"))
        self.caster.remove_concentration()
        self.assertFalse(self.friend.has_effect("Bless"))


# EOF
