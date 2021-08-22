""" Parent class for all creatures """
# pylint: disable=too-many-public-methods
import random
from typing import Optional
from collections import namedtuple
import dice
from actions import Action
from attacks import Attack
from spells import SpellAction
from constants import ActionType
from constants import ActionCategory
from constants import Condition
from constants import MonsterType
from constants import DamageType
from constants import Stat
from constants import Statistics


##############################################################################
##############################################################################
class Creature:  # pylint: disable=too-many-instance-attributes
    """Parent class for all creatures - monsters and characters"""

    ##########################################################################
    def __init__(self, arena, **kwargs):
        self.arena = arena
        self.vulnerable = kwargs.get("level", 0)
        self.name = kwargs.get("name", self.__class__.__name__)
        self.ac = kwargs.get("ac", 10)  # pylint: disable=invalid-name
        self.speed = int(kwargs.get("speed", 30) / 5)
        self.moves = self.speed
        self.type = kwargs.get("type", MonsterType.HUMANOID)
        self.size = kwargs.get("size", "M")
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
        if "spellcast_bonus" in kwargs:
            self.spellcast_modifier = self.stat_bonus(kwargs.get("spellcast_bonus"))
            self.spellcast_modifier += self.prof_bonus
        else:
            self.spellcast_modifier = 0
        self.action_preference = kwargs.get(
            "action_preference", {ActionType.MELEE: 1, ActionType.RANGED: 4}
        )
        self.attacks_per_action = kwargs.get("attacks_per_action", 1)
        self.vulnerable = kwargs.get("vulnerable", [])
        self.resistant = kwargs.get("resistant", [])
        self.immunity = kwargs.get("immunity", [])
        self.cond_immunity = kwargs.get("cond_immunity", [])
        self.state = "OK"
        if "hp" in kwargs:
            self.hp = kwargs["hp"]  # pylint: disable=invalid-name
        else:
            self.hp = self.roll_hp()
        self.max_hp = self.hp
        self.has_grappled = None
        self.actions = []
        self.bonus_actions = []
        self.reactions = []
        self.conditions = set()
        self.effects = {}
        self.target = None
        self.coords = None
        self.statistics = []
        self.options_this_turn = []

    ##########################################################################
    def __repr__(self):
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
        return chp

    ##########################################################################
    def pick_closest_enemy(self) -> list:
        """Which enemy is the closest"""
        return self.arena.pick_closest_enemy(self)

    ##########################################################################
    def pick_closest_friends(self) -> list:
        """Which friend is the closest"""
        return self.arena.pick_closest_friends(self)

    ##########################################################################
    def saving_throw(self, stat: Stat, dc: int) -> bool:  # pylint: disable=invalid-name
        """Make a saving throw against a stat"""
        # Need to add stat proficiency
        if self.has_condition(Condition.UNCONSCIOUS) and stat in (Stat.STR, Stat.DEX):
            print(
                f"{self} automatically failed {stat.value} saving throw as unconscious"
            )
            return False
        effct = {"bonus": 0}
        for _, eff in self.effects.items():
            effct.update(eff.hook_saving_throw(stat))

        if "advantage" in effct and effct["advantage"]:
            save = max(int(dice.roll("d20")), int(dice.roll("d20")))
            msg = " with advantage"
        elif "disadvantage" in effct and effct["disadvantage"]:
            save = min(int(dice.roll("d20")), int(dice.roll("d20")))
            msg = " with disadvantage"
        else:
            save = int(dice.roll("d20"))
            msg = ""

        save += effct["bonus"] + self.stat_bonus(stat)
        if save >= dc:
            print(f"{self} made {stat.value} saving throw: {save} vs DC {dc} {msg}")
            return True
        print(f"{self} failed {stat.value} saving throw: {save} vs DC {dc} {msg}")
        return False

    ##########################################################################
    def roll_initiative(self) -> int:
        """Roll initiative"""
        init = dice.roll(f"d20+{self.stat_bonus(Stat.DEX)}")
        print(f"{self} rolled {init} for initiative")
        return init

    ##########################################################################
    def move_to_target(self, target, rnge) -> None:
        """Move closer to the target - until we are in range of our action"""
        if self.has_condition(Condition.GRAPPLED):
            print(f"{self} is grappled - not moving")
            return
        if self.moves:
            print(f"{self} move to {target}")
        for _ in range(self.moves):
            # Within range - don't move
            dist = self.distance(target)
            if rnge and dist <= rnge:
                print(f"{target} is within range")
                return

            old_coords = self.coords
            self.coords = self.arena.move_towards(self, self.target)
            if old_coords == self.coords:
                print("Hand brake is on")
                break
            self.moves -= 1
            print(f"{self} moved to {self.coords}: {self.moves} left")

    ##########################################################################
    def pick_attack_by_name(self, name: str) -> Optional[Attack]:
        """Pick the attack by name"""
        for atk in self.actions:
            if atk.name == name:
                return atk
        return None

    ##########################################################################
    def hit(  # pylint: disable=too-many-arguments
        self, dmg: int, dmg_type: DamageType, source, critical: bool, atkname: str
    ) -> None:
        """We've been hit by source- take damage"""
        if dmg_type in self.vulnerable:
            print(f"{self} is vulnerable to {dmg_type.value}")
            dmg *= 2
        if dmg_type in self.immunity:
            print(f"{self} is immune to {dmg_type.value}")
            dmg = 0
        for eff in self.effects.values():
            dmg = eff.hook_being_hit(dmg, dmg_type)
        print(f"{self} has taken {dmg} damage ({dmg_type.value}) from {atkname}")
        self.hp -= dmg
        print(f"{self} now has {self.hp} HP")

        source.statistics.append(Statistics(atkname, dmg, dmg_type, critical))

        if self.hp <= 0:
            self.fallen_unconscious(dmg, dmg_type, critical)
        else:
            self.react(source)

    ##########################################################################
    def react(self, source) -> None:
        """React to an incoming attack with a reaction"""
        if ActionCategory.REACTION not in self.options_this_turn:
            return
        react = self.pick_action(typ=ActionCategory.REACTION, target=source)
        if react is not None:
            print(f"{self} reacts against {source}")
            react.perform_action(self)
            self.options_this_turn.remove(ActionCategory.REACTION)

    ##########################################################################
    def has_condition(self, cond) -> bool:
        """Do we have a condition"""
        return cond in self.conditions

    ##########################################################################
    def remove_condition(self, cond) -> None:
        """Remove a condition"""
        if self.has_condition(cond):
            self.conditions.remove(cond)

    ##########################################################################
    def add_condition(self, cond: Condition, source=None) -> None:
        """Add a condition - inflicted by source"""
        if cond not in self.cond_immunity:
            if source:
                print(f"{self} got {cond.value} from {source}")
            else:
                print(f"{self} is now {cond.value}")
            self.conditions.add(cond)

    ##########################################################################
    def add_action(self, action: Action) -> None:
        """Add an action to the creature"""
        self.actions.append(action)

    ##########################################################################
    def add_bonus_action(self, action: Action) -> None:
        """Add a bonus action to the creature"""
        self.bonus_actions.append(action)

    ##########################################################################
    def add_reaction(self, action: Action) -> None:
        """Add an reaction to the creature"""
        self.reactions.append(action)

    ##########################################################################
    def roll_hp(self) -> int:
        """Roll the initial hitpoints"""
        if not hasattr(self, "hitdice"):
            self.hitdice = ""
        return int(dice.roll(self.hitdice))

    ##########################################################################
    def is_alive(self) -> bool:
        """return if the creature is alive"""
        return self.hp > 0

    ##########################################################################
    def shortrepr(self):
        """What it looks like on the arena"""
        raise NotImplementedError(
            f"{self.__class__.__name__} needs to implement shortrepr()"
        )

    ##########################################################################
    def fallen_unconscious(
        self,
        dmg: int,  # pylint: disable=unused-argument
        dmg_type: DamageType,  # pylint: disable=unused-argument
        critical: bool,  # pylint: disable=unused-argument
    ) -> None:
        """Creature has fallen unconscious"""
        self.hp = 0
        self.state = "UNCONSCIOUS"
        self.add_condition(Condition.UNCONSCIOUS)
        if self.has_grappled:
            self.has_grappled.remove_condition(Condition.GRAPPLED)

    ##########################################################################
    def is_type(self, typ) -> bool:
        """Are we an instance of typ"""
        return self.type == typ

    ##########################################################################
    def end_turn(self):
        """Are the any effects for the end of the turn"""
        for name, effect in self.effects.copy().items():
            remove = effect.removal_end_of_its_turn(self)
            if remove:
                self.remove_effect(name)
        print(self.arena)

    ##########################################################################
    def remove_effect(self, name):
        """Remove an effect"""
        del self.effects[name]

    ##########################################################################
    def has_effect(self, name) -> bool:
        """Do we have an effect"""
        return name in self.effects

    ##########################################################################
    def add_effect(self, effect):
        """Add an effect"""
        self.effects[effect.name] = effect
        effect.initial(self)

    ##########################################################################
    def dump_statistics(self) -> dict:
        """Dump out the attack statistics - make prettier"""
        tmp = {}
        for name, dmg, _, crit in self.statistics:
            if name not in tmp:
                tmp[name] = {"hits": 0, "misses": 0, "dmg": 0, "crits": 0}
            if dmg == 0:
                tmp[name]["misses"] += 1
            else:
                tmp[name]["hits"] += 1
                tmp[name]["dmg"] += dmg
                if crit:
                    tmp[name]["crits"] += 1
        return tmp

    ##########################################################################
    def report(self):
        """Short report on the character"""
        print(f"| {self.name} @ {self.coords}")
        print(f"|  HP: {self.hp} / {self.max_hp} - {self.state}")
        print(f"|  AC: {self.ac}")
        if self.conditions:
            print(f"|  Conditions: {', '.join([_.value for _ in self.conditions])}")
        if self.effects:
            print(f"|  Temp Effects: {', '.join(self.effects)}")

    ##########################################################################
    def distance(self, target) -> int:
        """Distance from us to target"""
        return self.arena.distance(self, target)

    ##########################################################################
    def possible_actions(self, typ=ActionCategory.ACTION) -> list:
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
            if act.is_available(self):
                quality = act.heuristic(self)
                possible_acts.append((quality, act))
        return possible_acts

    ##########################################################################
    def spell_available(
        self, spell  # pylint: disable=unused-argument
    ) -> bool:  # pylint: disable=no-self-use
        """Spell casters should redefine this"""
        return False

    ##########################################################################
    def pick_action(self, typ=ActionCategory.ACTION, target=None) -> Action:
        """What are we going to do this turn based on individual action_preference"""
        # The random is added a) as a tie breaker for sort b) for a bit of fun
        actions = []
        acttuple = namedtuple("acttuple", "qual rnd heur pref act")
        for heur, act in self.possible_actions(typ):
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
        actions.sort(reverse=True)

        for act in actions:
            print(f"\t{act}")
        if not actions:
            return None

        action = actions[0].act
        if target is None:
            self.target = action.pick_target(self)
        else:
            self.target = target
        return action

    ##########################################################################
    def start_turn(self):
        """Start the turn"""
        # These are all the things we can do this turn
        self.options_this_turn = [
            ActionCategory.ACTION,
            ActionCategory.BONUS,
            ActionCategory.REACTION,
        ]
        if self.has_condition(Condition.PARALYZED):
            self.options_this_turn = []
        if self.state != "OK":
            self.options_this_turn = []
        self.moves = self.speed
        for eff in self.effects.copy().values():
            eff.hook_start_turn()

        for creat in self.arena.combatants:
            if creat == self:
                continue
            creat.start_others_turn(self)

    ##########################################################################
    def start_others_turn(self, creat):
        """Hook for anothing creature starting a turn near me"""

    ##########################################################################
    def move(self, act: Action):
        """Do a move"""
        if self.target and self.moves:
            if act:
                rnge, _ = act.range()
            else:
                rnge = None
            self.move_to_target(self.target, rnge)

    ##########################################################################
    def do_action(self, act: Action) -> bool:
        """Have an action"""
        if act and self.target:
            did_act = act.perform_action(self)
            if did_act is None or did_act:
                return True
        return False

    ##########################################################################
    def dash(self) -> None:
        """Do a dash action"""
        # Dash if we aren't in range yet
        if not self.target:
            enemies = self.pick_closest_enemy()
            if enemies:
                self.target = enemies[0]
        if self.target:
            print(f"{self} dashing")
            self.moves = self.speed
            self.options_this_turn.remove(ActionCategory.ACTION)
            self.move_to_target(self.target, None)

    ##########################################################################
    def do_stuff(self, categ: ActionCategory, moveto=False) -> None:
        """All the doing bits"""
        if categ not in self.options_this_turn:
            return

        # What are we going to do this turn
        act = self.pick_action(categ)

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
                print(f"{msg} self as a {categ.value} action")
            else:
                print(f"{msg} {self.target} as a {categ.value} action")
            did_act = self.do_action(act)
            if did_act and act.action_cost:
                self.options_this_turn.remove(categ)

    ##########################################################################
    def turn(self):
        """Have a go"""
        print()
        self.report()
        self.start_turn()
        self.do_stuff(ActionCategory.BONUS)
        self.do_stuff(ActionCategory.ACTION, moveto=True)
        self.do_stuff(ActionCategory.BONUS)
        self.do_stuff(ActionCategory.ACTION, moveto=True)
        if ActionCategory.ACTION in self.options_this_turn:
            self.dash()
        self.end_turn()


# EOF
