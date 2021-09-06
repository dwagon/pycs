""" Handle non-attack Actions """
from collections import namedtuple
import dice
from pycs.action import Action
from pycs.constant import SpellType


##############################################################################
##############################################################################
##############################################################################
class SpellAction(Action):
    """Spell action"""

    ########################################################################
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.reach = kwargs.get("reach", 0) / 5
        self.type = kwargs.get("type")
        self.cure_hp = kwargs.get("cure_hp")
        self.level = kwargs.get("level")
        self.concentration = kwargs.get("concentration")
        self.caster = None
        self.target = None

    ########################################################################
    def failed_save(self, source, target, dmg):
        """Called when the target failed save"""

    ########################################################################
    def made_save(self, source, target, dmg):
        """Called when the target made save"""

    ########################################################################
    def is_type(self, *types):
        """Is this spell of the specified types"""
        return self.type in types

    ########################################################################
    def range(self):
        """Return the good / worse range for the spell"""
        return self.reach, self.reach

    ########################################################################
    def modifier(self, attacker):
        """Attack modifier"""
        return attacker.stat_bonus(attacker.spellcast_bonus_stat) + attacker.prof_bonus

    ########################################################################
    def perform_action(self, source):
        """Cast the spell"""
        if not source.spell_available(self):
            return False
        source.cast(self)
        print(f"{source} is casting {self.name}")
        self.caster = source
        if self.concentration and self.caster.concentration:
            self.caster.remove_concentration()
        result = self.cast(source)
        if self.concentration:
            source.add_concentration(self)
        return result

    ########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if not doer.spell_available(self):
            return 0
        return 1

    ########################################################################
    def cast(self, caster):
        """Needs to be replaced"""
        raise NotImplementedError(f"SpellAction.{__class__.__name__} needs a cast()")


##############################################################################
def health_level_of_peers(doer):
    """Return the health levels (missing hp) of peers"""
    result = namedtuple("Result", "health id target")
    peers = [
        result(_.max_hp - _.hp, id(_), _)
        for _ in doer.arena.my_side(doer.side)
        if _.max_hp != 0
    ]
    if not peers:
        return None
    peers.sort(reverse=True)
    return peers[0]


##############################################################################
def healing_heuristic(doer, spell):
    """Should we cast this"""
    if not doer.spell_available(spell):
        return 0
    peers = health_level_of_peers(doer)
    if not peers:
        return 0
    return peers.health


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
        self.style = kwargs.get("style", SpellType.TOHIT)
        self.type = kwargs.get("type")
        self.save_stat = kwargs.get("save_stat")
        self.save_dc = kwargs.get("save_dc")

    ########################################################################
    def stat_dmg_bonus(self, attacker):
        """No spell bonus to damage"""
        return attacker.stat_bonus(attacker.spellcast_bonus_stat)

    ########################################################################
    def roll_dmg(self, source, victim, critical=False):
        """Special spell damage"""
        if self.style == SpellType.TOHIT:
            return super().roll_dmg(source, victim, critical)
        dmg = int(dice.roll(self.dmg[0]))
        print(f"{source} rolled {dmg} on {self.dmg[0]} for damage")
        if self.dmg[1]:
            dmg += self.dmg[1]
            print(f"Adding bonus of {self.dmg[1]} -> {dmg}")
        dmg_bon = self.stat_dmg_bonus(source)
        if dmg_bon:
            dmg += dmg_bon
            print(f"Adding stat bonus of {dmg_bon} -> {dmg}")
        spell_dc = self.save_dc
        if not spell_dc:
            spell_dc = source.spellcast_save
        saved = victim.saving_throw(stat=self.save_stat, dc=spell_dc, effect="unknown")
        if saved:
            if self.style == SpellType.SAVE_HALF:
                dmg = int(dmg / 2)
            if self.style == SpellType.SAVE_NONE:
                dmg = 0
            self.made_save(source=source, target=victim, dmg=dmg)
        else:
            self.failed_save(source=source, target=victim, dmg=dmg)
        return max(dmg, 0)

    ########################################################################
    def heuristic(self, doer):
        """Should we cast this"""
        if not doer.spell_available(self):
            return 0
        pot_target = doer.pick_closest_enemy()
        if not pot_target:
            return 0
        if doer.distance(pot_target[0]) > self.range()[1]:
            return 0
        return self.max_dmg(doer)

    ########################################################################
    def roll_to_hit(self, source, target):
        """Special spell attack"""
        if self.style == SpellType.TOHIT:
            return super().roll_to_hit(source, target)
        return 999, False, False

    ########################################################################
    def range(self):
        """Return the range of the attack"""
        return self.reach, self.reach

    ########################################################################
    def is_available(self, owner):
        """Is this action available?"""
        return owner.spell_available(self)

    ########################################################################
    def cast(self, caster):
        """Cast the attack spell - overwrite if required"""
        return self.do_attack(caster)

    ##########################################################################
    def end_concentration(self):
        """What happens when we stop concentrating"""


# EOF
