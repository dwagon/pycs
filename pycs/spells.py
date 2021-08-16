""" Handle non-attack Actions """
from collections import namedtuple
import dice
from actions import Action


##############################################################################
##############################################################################
##############################################################################
class SpellAction(Action):
    """Spell action"""

    ########################################################################
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.type = kwargs.get("type")
        self.cure_hp = kwargs.get("cure_hp")
        self.level = kwargs.get("level")
        self.concentration = kwargs.get("concentration")

    ########################################################################
    def is_type(self, *types):
        """Is this spell of the specified types"""
        return self.type in types

    ########################################################################
    def perform_action(self, source):
        """Cast the spell"""
        print(f"{source} is casting {self.name}")
        source.cast(self)
        self.cast(source)

    ########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if not doer.spell_available(self):
            return 0
        return 1

    ########################################################################
    def cast(self, caster):  # pylint: disable=unused-argument
        """Needs to be replaced"""
        print(f"SpellAction.{__class__.__name__} needs a cast()")


##############################################################################
def health_level_of_peers(doer):
    """Return the health levels of peers as percentage"""
    result = namedtuple("Result", "health id target")
    peers = [
        result(100 * _.hp / _.max_hp, id(_), _) for _ in doer.arena.my_side(doer.side)
    ]
    peers.sort()
    return peers[0]


##############################################################################
def healing_heuristic(doer, spell):
    """Should we cast this"""
    if not doer.spell_available(spell):
        return 0
    peers = health_level_of_peers(doer)
    # print(f"health of peers = {peers}")
    if peers.health < 20:  # No one is less than 20% wounded
        return 5
    elif peers.health < 40:
        return 4
    elif peers.health < 60:
        return 2
    elif peers.health < 80:
        return 1
    else:
        return 0


##############################################################################
def pick_heal_target(doer):
    """Who to heal"""
    return health_level_of_peers(doer).target


##############################################################################
##############################################################################
##############################################################################
class AttackSpell(SpellAction):
    """A spell attack"""

    ########################################################################
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.reach = int(kwargs.get("reach", 5) / 5)
        self.level = kwargs.get("level", 99)
        # Style is tohit or save;
        #   "tohit" you need to roll to hit,
        #   "save" you hit automatically but save on damage
        self.style = kwargs.get("style", "tohit")
        self.type = kwargs.get("type")
        self.save = kwargs.get("save", ("none", 999))

    ########################################################################
    def roll_dmg(self, victim, critical=False):
        """Special spell damage"""
        if self.style == "tohit":
            return super().roll_dmg(victim, critical)
        saved = victim.saving_throw(stat=self.save[0], dc=self.save[1])
        dmg = int(dice.roll(self.dmg[0])) + self.dmg[1]
        if saved:
            dmg = int(dmg / 2)
        return dmg

    ########################################################################
    def pick_target(self, doer):
        """Who should we target"""
        return doer.pick_closest_enemy()

    ########################################################################
    def heuristic(self, doer):
        """Should we cast this"""
        if not doer.spell_available(self):
            return 0
        pot_target = doer.pick_closest_enemy()
        if not pot_target:
            return 0
        if doer.distance(pot_target) > self.range()[1]:
            return 0
        return 2

    ########################################################################
    def roll_to_hit(self, source, target, rnge):
        """Special spell attack"""
        assert self.style in ("tohit", "save")
        if self.style == "tohit":
            return super().roll_to_hit(source, target, rnge)
        return 999, False, False

    ########################################################################
    def range(self):
        """Return the range of the attack"""
        return self.reach, self.reach

    ########################################################################
    def post_attack_hook(self, source):
        """Tell the caster they have cast the spell"""
        pass

    ########################################################################
    def is_available(self, owner):
        """Is this action available?"""
        return owner.spell_available(self)


# EOF
