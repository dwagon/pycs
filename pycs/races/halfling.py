"""https://www.dndbeyond.com/races/halfling"""
import io
import unittest
from unittest.mock import patch
import dice
from pycs.constant import Condition
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.race import Race


##############################################################################
##############################################################################
##############################################################################
class Halfling(Race):
    """Breakfast?"""

    def __init__(self, **kwargs):
        kwargs["effects"] = [Brave(), Lucky()]
        super().__init__("Halfling", **kwargs)


##############################################################################
##############################################################################
##############################################################################
class Lucky(Effect):
    """When you roll a 1 on the d20 for an attack roll, ability check,
    or saving throw, you can reroll the die and must use the new roll."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Lucky", **kwargs)

    ########################################################################
    def hook_d20(self, val, reason):
        """Reroll ones"""
        if reason in ("attack", "ability", "save"):
            if val == 1:
                val = int(dice.roll("d20"))
                print(f"Lucky - reroll 1 to {val}")
        return val


##############################################################################
##############################################################################
##############################################################################
class Brave(Effect):
    """You have advantage on saving throws against being frightened."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Brave", **kwargs)

    ########################################################################
    def hook_saving_throw(self, stat, **kwargs):
        """Advantage Frightened"""
        eff = super().hook_saving_throw(stat, **kwargs)
        if kwargs.get("effect") == Condition.FRIGHTENED:
            eff["advantage"] = True
        return eff


##############################################################################
##############################################################################
##############################################################################
class TestLucky(unittest.TestCase):
    """Test Lucky"""

    def setUp(self):
        kwargs = {
            "str": 6,
            "int": 7,
            "dex": 11,
            "wis": 18,
            "con": 11,
            "cha": 15,
            "hp": 30,
            "ac": 10,
            "race": Halfling,
            "name": "Hobbit",
            "side": "a",
        }
        self.hobbit = Creature(None, **kwargs)
        self.hobbit.add_effect(Lucky())

    ########################################################################
    def test_not_lucky(self):
        """Test what happens when we roll a 1 - but doesn't apply"""
        with patch.object(dice, "roll") as mock:
            mock.return_value = 1
            init = self.hobbit.roll_initiative()
            self.assertEqual(init, 1)

    ########################################################################
    def test_lucky(self):
        """Test what happens when we roll a 1 - but does apply"""
        with patch.object(dice, "roll") as mock:
            mock.side_effect = [1, 10]
            svth = self.hobbit.saving_throw(Stat.STR, dc=5)
            self.assertTrue(svth)


##############################################################################
##############################################################################
##############################################################################
class TestBrave(unittest.TestCase):
    """Test Brave"""

    def setUp(self):
        kwargs = {
            "str": 6,
            "int": 7,
            "dex": 11,
            "wis": 18,
            "con": 11,
            "cha": 15,
            "hp": 30,
            "ac": 10,
            "race": Halfling,
            "name": "Hobbit",
            "side": "a",
        }
        self.hobbit = Creature(None, **kwargs)
        self.hobbit.add_effect(Brave())

    ########################################################################
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_brave(self, mock_stdout):
        """Do some saving throws"""
        self.hobbit.saving_throw(Stat.STR, 10, effect=Condition.FRIGHTENED)
        self.assertTrue("with advantage" in mock_stdout.getvalue())


# EOF
