""" Parent class for all creatures """
# pylint: disable=too-many-public-methods
from __future__ import annotations

import random
from collections import defaultdict
from collections import namedtuple
from typing import Optional, Any, TYPE_CHECKING

import dice
from pycs.action import Action
from pycs.damage import Damage
from pycs.constant import ActionCategory
from pycs.constant import ActionType
from pycs.constant import Condition
from pycs.constant import DamageType
from pycs.constant import MonsterSize
from pycs.constant import MonsterType
from pycs.constant import Stat
from pycs.util import check_args
from pycs.equipment import Armour, Equipment
from pycs.attack import Attack
from pycs.effects import Effects
from pycs.spell import SpellAction


if TYPE_CHECKING:
    from pycs.effect import Effect
    from pycs.arena import Arena


##############################################################################
##############################################################################
##############################################################################
class Creature:  # pylint: disable=too-many-instance-attributes
    """Parent class for all creatures - monsters and characters"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        check_args(self._valid_args(), self.__class__.__name__, kwargs)
        self.arena: "Arena"  # Set by adding to arena
        self.name = kwargs.get("name", self.__class__.__name__)
        self._ac = kwargs.get("ac", None)
        self.speed = int(kwargs.get("speed", 30) / 5)
        self.moves = self.speed
        self.type = kwargs.get("type", MonsterType.HUMANOID)
        self.size = kwargs.get("size", MonsterSize.MEDIUM)
        self.critical = kwargs.get("critical", 20)
        self.prof_bonus = kwargs.get("prof_bonus", 2)
        self.side = kwargs["side"]  # Mandatory
        self.stats = {
            Stat.STR: kwargs["str"],
            Stat.INT: kwargs["int"],
            Stat.DEX: kwargs["dex"],
            Stat.WIS: kwargs["wis"],
            Stat.CON: kwargs["con"],
            Stat.CHA: kwargs["cha"],
        }
        self.stat_prof = kwargs.get("stat_prof", [])
        self.spellcast_bonus_stat: Stat = kwargs.get("spellcast_bonus_stat", Stat.INT)
        self.action_preference = kwargs.get("action_preference", {ActionType.MELEE: 1, ActionType.RANGED: 4})
        self.attacks_per_action = kwargs.get("attacks_per_action", 1)
        self.vulnerable = kwargs.get("vulnerable", [])
        self.resistant = kwargs.get("resistant", [])
        self.immunity = kwargs.get("immunity", [])
        self.cond_immunity = kwargs.get("cond_immunity", [])
        self.hp = kwargs["hp"]  # pylint: disable=invalid-name
        self.max_hp = self.hp
        self.has_grappled: Optional[Creature] = None
        self.grappled_by: Optional[Creature] = None
        self.escape_grapple_dc = 0
        self.death_saves = 0
        self.bonus_actions: list[Action] = []
        self.reactions: list[Action] = []
        self.actions: list[Action] = []
        for act in kwargs.get("actions", []):
            self.add_action(act)

        self.conditions = set([Condition.OK])

        self.effects = Effects(self)
        for effect in kwargs.get("effects", []):
            self.effects.add_effect(self, effect)

        self.target: Optional[Creature] = None
        self.coords: tuple[int, int]
        self.options_this_turn: list[ActionCategory] = []
        self.concentration: Optional["SpellAction"] = None
        self.damage_this_turn: list[Damage] = []
        self.damage_last_turn: list[Damage] = []

        self.gear: list[Equipment] = []
        for gear in kwargs.get("gear", []):
            self.add_gear(gear)

    ##########################################################################
    def __hash__(self) -> int:
        return hash(self.name + self.__class__.__name__)

    ##########################################################################
    def _valid_args(self) -> set[str]:
        """What is valid in this class for kwargs"""
        return {
            "name",
            "ac",
            "speed",
            "type",
            "size",
            "critical",
            "prof_bonus",
            "side",
            "str",
            "int",
            "dex",
            "wis",
            "con",
            "cha",
            "stat_prof",
            "spellcast_bonus_stat",
            "action_preference",
            "attacks_per_action",
            "vulnerable",
            "resistant",
            "immunity",
            "cond_immunity",
            "hp",
            "actions",
            "effects",
            "gear",
        }

    ##########################################################################
    @property
    def spellcast_save(self) -> int:
        """Saving throw DC vs spells from this creature"""
        if self.spellcast_bonus_stat is None:
            return 0
        return 8 + self.stat_bonus(self.spellcast_bonus_stat) + self.prof_bonus

    ##########################################################################
    @property
    def ac(self) -> int:  # pylint: disable=invalid-name
        """The armour class"""
        if self._ac is None:
            tmp = 0
            dbon = True  # Can we apply dex bonus
            max_db = 999  # Max Dex bonus
            for geah in self.gear:
                if issubclass(geah.__class__, Armour):
                    tmp += geah.ac + geah.ac_bonus + geah.magic_bonus  # type: ignore
                    if not geah.dex_bonus:  # type: ignore
                        dbon = False
                    max_db = min(max_db, geah.max_dex_bonus)  # type: ignore
            if tmp == 0:  # No armour so default to 10
                tmp = 10
            if dbon:
                dexbonus = min(self.stat_bonus(Stat.DEX), max_db)
                tmp += dexbonus
        else:
            tmp = self._ac
        tmp += self.effects.hook_ac_modifier()
        return tmp

    ##########################################################################
    def __repr__(self) -> str:
        return f"{self.name}"

    ##########################################################################
    def stat_bonus(self, stat: Stat) -> int:
        """What's the stat bonus for the stat"""
        return int((self.stats[stat] - 10) / 2)

    ##########################################################################
    def heal(self, cure_dice: str, cure_bonus: int) -> int:
        """Heal ourselves"""
        chp = 0
        if cure_dice:
            chp = int(dice.roll(cure_dice))
        chp += cure_bonus
        chp = min(chp, self.max_hp - self.hp)
        self.hp += chp
        print(f"{self} cured of {chp} hp")
        if self.has_condition(Condition.UNCONSCIOUS):
            self.death_saves = 0
            self.add_condition(Condition.OK)
            self.remove_condition(Condition.UNCONSCIOUS)
            print(f"{self} regained consciousness")
        return chp

    ##########################################################################
    def grapple(self, enemy: Creature, escape_dc: int = 0) -> bool:
        """Grapple an enemy"""
        grap = self.rolld20("grapple")
        grap += self.stat_bonus(Stat.STR)
        # Should do this skill based (Athletics vs Acrobatics)
        targ = enemy.rolld20("grapple")
        if enemy.stats[Stat.STR] > enemy.stats[Stat.DEX]:
            targ += enemy.stat_bonus(Stat.STR)
        else:
            targ += enemy.stat_bonus(Stat.DEX)
        if grap > targ:
            self.has_grappled = enemy
            enemy.grappled_by = self
            enemy.escape_grapple_dc = escape_dc
            print(f"{self} has grappled {enemy} ({grap} > {targ})")
            enemy.add_condition(Condition.GRAPPLED)
            return True
        print(f"{self} failed to grapple {enemy} ({grap} < {targ})")
        return False

    ##########################################################################
    def ungrapple(self) -> None:
        """Remove a grapple"""
        victim = self.has_grappled
        if victim is None:
            return
        victim.escape_grapple_dc = 0
        victim.grappled_by = None
        victim.remove_condition(Condition.GRAPPLED)
        self.has_grappled = None
        print(f"{self} is no longer grappling {victim}")

    ##########################################################################
    def pick_closest_enemy(self) -> list[Creature]:
        """Which enemy is the closest"""
        return self.arena.pick_closest_enemy(self)

    ##########################################################################
    def pick_closest_friends(self) -> list:
        """Which friend is the closest"""
        return self.arena.pick_closest_friends(self)

    ##########################################################################
    def saving_throw(self, stat: Stat, dc: int, **kwargs: Any) -> bool:  # pylint: disable=invalid-name
        """Make a saving throw against a stat"""
        if self.has_condition(Condition.UNCONSCIOUS) and stat in (Stat.STR, Stat.DEX):
            print(f"{self} automatically failed {stat.value} saving throw as unconscious")
            return False
        effct = {"bonus": 0}
        effct.update(self.effects.hook_saving_throw(stat, **kwargs))

        if "advantage" in effct and effct["advantage"]:
            save = max(self.rolld20("save"), self.rolld20("save"))
            msg = " with advantage"
        elif "disadvantage" in effct and effct["disadvantage"]:
            save = min(self.rolld20("save"), self.rolld20("save"))
            msg = " with disadvantage"
        else:
            save = self.rolld20("save")
            msg = ""
        if stat in self.stat_prof:
            save += self.prof_bonus

        save += effct["bonus"] + self.stat_bonus(stat)
        if save >= dc:
            print(f"{self} made {stat.value} saving throw: {save} vs DC {dc} {msg}")
            return True
        print(f"{self} failed {stat.value} saving throw: {save} vs DC {dc} {msg}")
        return False

    ##########################################################################
    def roll_initiative(self) -> int:
        """Roll initiative"""
        init = self.rolld20("initiative")
        init += self.stat_bonus(Stat.DEX)
        print(f"{self} rolled {init} for initiative")
        return init

    ##########################################################################
    def move_to_target(self, target: Creature, rnge: Optional[int]) -> None:
        """Move closer to the target - until we are in range of our action"""
        if self.has_condition(Condition.GRAPPLED):
            print(f"{self} is grappled - not moving")
            return
        if self.has_grappled:
            print(f"{self} has grappled {self.has_grappled}- not moving")
            return
        for _ in range(self.moves):
            # Within range - don't move
            dist = self.distance(target)
            if rnge and dist <= rnge:
                return

            # Have to check every move if we are in any effect area
            for partic in self.arena.pick_alive():
                for comb in self.arena.pick_alive():
                    partic.effects.hook_start_in_range(comb)

            old_coords = self.coords
            self.coords = self.arena.move_towards(self, target.coords)
            if old_coords == self.coords:
                break
            self.moves -= 1
            print(f"{self} moving towards {target} - moved to {self.coords}: {self.moves} left")

    ##########################################################################
    def pick_action_by_name(self, name: str) -> Optional[Action]:
        """Pick the attack by name"""
        for atk in self.actions:
            if atk.name == name:
                return atk
        for atk in self.bonus_actions:
            if atk.name == name:
                return atk
        for atk in self.reactions:
            if atk.name == name:
                return atk
        print(f"{self}: pick_action_by_name({name=}) - none found")
        return None

    ##########################################################################
    def hit(self, dmg: Damage, source: Creature, critical: bool, atkname: str) -> None:
        """We've been hit by source - take damage"""
        dmg = self._react_predmg(dmg, source, critical)
        if dmg.type in self.vulnerable:
            print(f"{self} is vulnerable to {dmg.type.value}")
            dmg.hp *= 2
        if dmg.type in self.immunity:
            print(f"{self} is immune to {dmg.type.value}")
            dmg.hp = 0
        if dmg.type in self.resistant:
            print(f"{self} is resistant to {dmg.type.value}")
            dmg.hp //= 2
        dmg = self.effects.hook_being_hit(dmg)

        print(f"{self} has taken {dmg} from {atkname}")
        self.hp -= dmg.hp
        print(f"{self} now has {self.hp} HP")
        if dmg and self.concentration:
            svth = self.saving_throw(Stat.CON, max(10, dmg.hp // 2))
            if not svth:
                print(f"{self} failed concentration save on {self.concentration}")
                self.remove_concentration()

        self.arena.statistics.add(target=self, source=source, hit=True, atkname=atkname, dmg=dmg, critical=critical)
        if dmg:
            self.damage_this_turn.append(dmg)

        if self.hp <= 0:
            self.fallen_unconscious(dmg, critical)
        else:
            self._react_postdmg(source)

    ##########################################################################
    def miss(self, source: Creature, atkname: str) -> None:
        """Was attacked by source, but missed *spppt!*"""
        self.arena.statistics.add(target=self, source=source, hit=False, atkname=atkname)

    ##########################################################################
    def _react_predmg(self, dmg: Damage, source: Creature, critical: bool) -> Damage:
        """About to take damage - do we have a reaction that can alter the damage"""
        if ActionCategory.REACTION not in self.options_this_turn:
            return dmg
        react = self._pick_action(typ=ActionCategory.REACTION, target=source, need_hook="hook_predmg")
        if react is not None:
            print(f"{self} reacts against {source}")
            dmg = react.hook_predmg(dmg=dmg, source=source, critical=critical)
            self.options_this_turn.remove(ActionCategory.REACTION)
        return dmg

    ##########################################################################
    def _react_postdmg(self, source: Creature) -> None:
        """React to an incoming attack with a reaction"""
        if ActionCategory.REACTION not in self.options_this_turn:
            return
        react = self._pick_action(typ=ActionCategory.REACTION, target=source, need_hook="hook_postdmg")
        if react is not None:
            print(f"{self} reacts against {source}")
            react.hook_postdmg()
            self.options_this_turn.remove(ActionCategory.REACTION)

    ##########################################################################
    def has_condition(self, *conditions: Condition) -> bool:
        """Do we have a condition"""
        for cond in conditions:
            if cond in self.conditions:
                return True
        return False

    ##########################################################################
    def remove_condition(self, cond: Condition) -> None:
        """Remove a condition"""
        if self.has_condition(cond):
            self.conditions.remove(cond)

    ##########################################################################
    def add_condition(self, cond: Condition, source: Optional[Creature] = None) -> None:
        """Add a condition - inflicted by source"""
        if cond not in self.cond_immunity:
            if source:
                print(f"{self} got {cond.value} from {source}")
            else:
                print(f"{self} is now {cond.value}")
            self.conditions.add(cond)

    ##########################################################################
    def add_gear(self, gear: Equipment) -> None:
        """Add something to the equipment list"""
        self.gear.append(gear)
        gear.owner = self
        for action in gear.actions:
            action.gear = gear
            self.add_action(action)

    ##########################################################################
    def add_action(self, action: Action) -> None:
        """Add an action to the creature"""
        action.owner = self
        if action.category == ActionCategory.BONUS:
            self.bonus_actions.append(action)
        elif action.category == ActionCategory.REACTION:
            self.reactions.append(action)
        else:
            self.actions.append(action)

    ##########################################################################
    def is_alive(self) -> bool:
        """return True if the creature is alive and conscious"""
        if self.has_condition(Condition.DEAD) or self.has_condition(Condition.UNCONSCIOUS):
            return False
        return True

    ##########################################################################
    def shortrepr(self) -> str:
        """What it looks like on the arena"""
        return "?"

    ##########################################################################
    def fallen_unconscious(self, dmg: Damage, critical: bool) -> None:
        """Creature has fallen unconscious"""
        if not self.effects.hook_fallen_unconscious(dmg, critical):
            return
        self.hp = 0
        if self.has_grappled:
            self.ungrapple()
        for comb in self.arena.pick_alive():
            if comb == self:
                continue
            comb.hook_see_someone_die(self)
        self.creature_fallen_unconscious(dmg, critical)

    ##########################################################################
    def creature_fallen_unconscious(self, dmg: Damage, critical: bool) -> None:
        """How you actually fall unconscious depends on what you are"""
        raise NotImplementedError(f"{self.__class__.__name__} needs a creature_fallen_unconscious()")

    ##########################################################################
    def hook_see_someone_die(self, creat: Creature) -> None:
        """Someone has died - react"""

    ##########################################################################
    def is_type(self, typ: MonsterType) -> bool:
        """Are we an instance of typ"""
        return self.type == typ

    ##########################################################################
    def end_turn(self, draw: bool = True) -> None:
        """Are the any effects for the end of the turn"""
        self.effects.removal_end_of_its_turn(self)
        if draw and self.has_condition(Condition.OK):
            print(self.arena)

    ##########################################################################
    def remove_effect(self, effect: Effect | str) -> None:
        """Remove an effect"""
        self.effects.remove_effect(effect)

    ##########################################################################
    def has_effect(self, name: str) -> bool:
        """Do we have an effect"""
        return self.effects.has_effect(name)

    ##########################################################################
    def add_effect(self, effect: "Effect") -> None:
        """Add an effect"""
        self.effects.add_effect(self, effect)

    ##########################################################################
    def report(self) -> None:
        """Short report on the character"""
        print(f"| {self.name} @ {self.coords}")
        print(f"|  HP: {self.hp} / {self.max_hp}")
        print(f"|  AC: {self.ac}")
        if self.concentration:
            print(f"|  Concentration: {self.concentration}")
        if self.conditions:
            print(f"|  Conditions: {', '.join([_.value for _ in self.conditions])}")
        if self.effects:
            print(f"|  Effects: {str(self.effects)}")
        if self.has_grappled:
            print(f"|  Grappling {self.has_grappled}")
        if self.grappled_by:
            print(f"|  Grappled by {self.grappled_by}")
        if self.damage_this_turn:
            print(f"|  Damage This Turn: {self.damage_summary(self.damage_this_turn)}")
        if self.damage_last_turn:
            print(f"|  Damage Last Turn: {self.damage_summary(self.damage_last_turn)}")
        for act in self.actions + self.bonus_actions + self.reactions:
            if act.ammo is not None:
                print(f"|  {act} Ammo: {act.ammo}")

    ##########################################################################
    def damage_summary(self, dmglist: list[Damage]) -> str:
        """Summarise damage"""
        if not dmglist:
            return "None"
        taken: defaultdict[DamageType, int] = defaultdict(int)
        for tkn in dmglist:
            if tkn.hp:
                taken[tkn.type] += tkn.hp
        output = []
        for typ, val in taken.items():
            output.append(f"{val} x {typ.value}")

        return ", ".join(output)

    ##########################################################################
    def distance(self, target: Creature) -> int:
        """Distance from us to target"""
        return self.arena.distance(self, target)

    ##########################################################################
    def _possible_actions(self, typ: ActionCategory = ActionCategory.ACTION) -> list:
        """What are all the things we can do this turn and how good do they
        feel about happening"""
        possible_acts = []
        if typ == ActionCategory.ACTION:
            from_actions = self.actions
        elif typ == ActionCategory.BONUS:
            from_actions = self.bonus_actions
        elif typ == ActionCategory.REACTION:
            from_actions = self.reactions
        for act in from_actions:
            if act.is_available():
                quality = act.get_heuristic()
                possible_acts.append((quality, act))
        if self.has_condition(Condition.GRAPPLED) and typ == ActionCategory.ACTION:
            possible_acts.append((10, BreakGrapple(owner=self)))
        return possible_acts

    ##########################################################################
    def spell_available(self, spell: "SpellAction") -> bool:  # pylint: disable=unused-argument
        """Spell casters should redefine this"""
        return False

    ##########################################################################
    def _pick_action(
        self,
        typ: ActionCategory = ActionCategory.ACTION,
        target: Optional[Creature] = None,
        need_hook: Optional[str] = None,
    ) -> Optional[Action]:
        """What are we going to do this turn based on individual action_preference
        If {need_hook} is set then the action must define that hook to be in contention
        """
        # The random is added a) as a tie breaker for sort b) for a bit of fun
        actions = []
        acttuple = namedtuple("acttuple", "qual rnd heur pref act")
        for heur, act in self._possible_actions(typ):
            if need_hook and not hasattr(act, need_hook):
                continue
            if act.__class__ in self.action_preference:
                pref = self.action_preference.get(act.__class__)
            elif issubclass(act.__class__, SpellAction):
                pref = self.action_preference.get(act.type, 1)
            elif issubclass(act.__class__, Attack):
                pref = self.action_preference.get(act.type, 1)
            else:
                pref = self.action_preference.get(act, 1)
            if heur * pref != 0:
                actions.append(acttuple(heur * pref, random.random(), heur, pref, act))
            else:
                print(f"\t{typ.value} Not {heur=},  {pref=},  {act=}")
        actions.sort(reverse=True)

        for act in actions:
            print(f"\t{act}")
        if not actions:
            return None

        action: Action = actions[0].act
        if target is None:
            self.target = action.pick_target()
        else:
            self.target = target
        return action

    ##########################################################################
    def _make_death_save(self) -> None:
        """Death Saves - going to ignore stabilising"""
        roll = int(dice.roll("d20"))
        print(f"{self} rolled {roll} on death saving throw")
        if roll == 1:
            self.death_saves += 2
            print(f"{self} badly failed a death saving throw - at {self.death_saves}")
        elif roll <= 10:
            self.death_saves += 1
            print(f"{self} failed a death saving throw - at {self.death_saves}")
        elif roll == 20:
            print(f"{self} gasps back to life")
            self.heal("", 1)
        else:
            print(f"{self} made a death saving throw - at {self.death_saves}")

        if self.death_saves >= 3:
            self.died()

    ##########################################################################
    def died(self) -> None:
        """Creature has died"""
        self.hp = 0
        if self.has_condition(Condition.GRAPPLED) and self.grappled_by is not None:
            self.grappled_by.ungrapple()
        self.effects.remove_all_effects()
        self.add_condition(Condition.DEAD)
        self.remove_condition(Condition.UNCONSCIOUS)
        self.remove_condition(Condition.OK)
        self.arena.remove_combatant(self)

    ##########################################################################
    def start_turn(self) -> None:
        """Start the turn"""
        # These are all the things we can do this turn
        self.damage_last_turn = self.damage_this_turn
        self.damage_this_turn = []
        if self.has_condition(Condition.UNCONSCIOUS):
            self._make_death_save()
            if self.has_condition(Condition.DEAD):
                return
        self.options_this_turn = [
            ActionCategory.ACTION,
            ActionCategory.BONUS,
            ActionCategory.REACTION,
        ]
        if self.has_condition(Condition.PARALYZED):
            self.options_this_turn = []
        if not self.has_condition(Condition.OK):
            self.options_this_turn = []
        if self.has_condition(Condition.PRONE):
            print(f"{self} gets up from being prone")
            self.moves = int(self.speed / 2)
            self.remove_condition(Condition.PRONE)
        else:
            self.moves = self.speed
        self.effects.hook_start_turn()

        for part in self.arena.pick_alive():
            for comb in self.arena.pick_alive():
                part.effects.hook_start_in_range(comb)

        for creat in self.arena.pick_alive():
            if creat == self:
                creat.hook_start_turn()
                continue
            creat.start_others_turn(self)

    ##########################################################################
    def start_others_turn(self, creat: Creature) -> None:
        """Hook for another creature starting a turn near me"""

    ##########################################################################
    def hook_start_turn(self) -> None:
        """Hook for us starting a turn"""

    ##########################################################################
    def move_away(self, cause: Creature) -> None:
        """Move away from the {cause}"""
        if cause.coords is None:  # Cause is dead?
            return
        for _ in range(self.moves):
            self.coords = self.arena.move_away(self, cause)
            self.moves -= 1
            print(f"{self} moved to {self.coords}: {self.moves} left")

    ##########################################################################
    def move(self, act: Optional[Action]) -> None:
        """Do a move"""
        if self.target is not None and self.moves:
            if act:
                rnge, _ = act.range()
            else:
                rnge = None
            self.move_to_target(self.target, rnge)

    ##########################################################################
    def do_action(self, act: Action) -> bool:
        """Have an action"""
        if act and self.target is not None:
            assert act.owner is not None
            act.ammo_usage()
            did_act = act.perform_action()
            if did_act is None or did_act:
                return True
        return False

    ##########################################################################
    def dash(self) -> None:
        """Do a dash action"""
        # Dash if we aren't in range yet
        if self.target is None:
            enemies = self.pick_closest_enemy()
            if enemies:
                self.target = enemies[0]
        if self.target is not None:
            print(f"{self} dashing")
            self.moves = self.speed
            self.options_this_turn.remove(ActionCategory.ACTION)
            self.move_to_target(self.target, None)

    ##########################################################################
    def do_stuff(self, categ: ActionCategory, moveto: bool = False) -> None:
        """All the doing bits"""
        if categ not in self.options_this_turn:
            return

        # What are we going to do this turn
        act = self._pick_action(categ)
        if act is None:
            victims = self.pick_closest_enemy()
            if victims:
                self.target = victims[0]

        # Move closer to target
        if moveto:
            self.move(act)

        # Do the action
        if act:
            msg = f"{self} is going to do {act} to"
            if self.target == self:
                print(f"{msg} self as {categ.value}")
            else:
                print(f"{msg} {self.target} as {categ.value}")
            did_act = self.do_action(act)
            if did_act and act.action_cost:
                self.options_this_turn.remove(categ)

    ##########################################################################
    def add_concentration(self, spell: "SpellAction") -> None:
        """Start a new concentration spell"""
        if self.concentration:
            print(f"{self} removing {self.concentration} as casting {spell}")
            self.remove_concentration()
        self.concentration = spell

    ##########################################################################
    def remove_concentration(self) -> None:
        """Stop concentrating on a  spell"""
        if not self.concentration:
            return
        self.concentration.end_concentration()
        self.concentration = None

    ##########################################################################
    def rolld20(self, reason: str) -> int:
        """Roll a d20"""
        d20 = int(dice.roll("d20"))
        d20 = self.effects.hook_d20(d20, reason)
        return d20

    ##########################################################################
    def flee(self) -> bool:
        """Forced to flee?"""
        # Not implemented yet
        return False

    ##########################################################################
    def turn(self) -> None:
        """Have a go"""
        if self.has_condition(Condition.DEAD):
            return
        print()
        self.report()
        self.start_turn()
        if not self.flee():
            self.do_stuff(ActionCategory.BONUS)
            self.do_stuff(ActionCategory.ACTION, moveto=True)
            self.do_stuff(ActionCategory.BONUS)
            self.do_stuff(ActionCategory.ACTION, moveto=True)
            if ActionCategory.ACTION in self.options_this_turn:
                self.dash()
        self.end_turn()


##############################################################################
##############################################################################
##############################################################################
class BreakGrapple(Action):
    """Try and break the grapple"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        super().__init__("Break Grapple", **kwargs)
        self.category = ActionCategory.ACTION

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do this"""
        return 0

    ##########################################################################
    def perform_action(self) -> bool:
        """Do this"""
        enemy = self.owner.grappled_by
        if self.owner.stats[Stat.STR] > self.owner.stats[Stat.DEX]:
            targ = self.owner.rolld20(Stat.STR)
            targ += self.owner.stat_bonus(Stat.STR)
        else:
            targ = self.owner.rolld20(Stat.DEX)
            targ += self.owner.stat_bonus(Stat.DEX)

        if self.owner.escape_grapple_dc:
            escape = self.owner.escape_grapple_dc
        else:
            escape = enemy.rolld20(Stat.STR)
            escape += enemy.stat_bonus(Stat.STR)

        if targ > escape:
            print(f"{self.owner} has broken grapple of {enemy} ({targ} > {escape})")
            self.owner.grappled_by.ungrapple()
        else:
            print(f"{self.owner} failed to break grapple of {enemy} ({targ} < {escape})")
        return True


# EOF
