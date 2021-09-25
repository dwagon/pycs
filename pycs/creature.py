""" Parent class for all creatures """
# pylint: disable=too-many-public-methods
import random
from collections import defaultdict
from collections import namedtuple
from typing import Optional
import dice
from pycs.action import Action
from pycs.attack import Attack
from pycs.constant import ActionCategory
from pycs.constant import ActionType
from pycs.constant import Condition
from pycs.constant import Damage
from pycs.constant import DamageType
from pycs.constant import MonsterSize
from pycs.constant import MonsterType
from pycs.constant import Stat
from pycs.constant import Statistics
from pycs.equipment import Armour
from pycs.spell import SpellAction
from pycs.util import check_args


##############################################################################
##############################################################################
class Creature:  # pylint: disable=too-many-instance-attributes
    """Parent class for all creatures - monsters and characters"""

    ##########################################################################
    def __init__(self, **kwargs):
        check_args(self._valid_args(), self.__class__.__name__, kwargs)
        self.arena = None  # Set by adding to arena
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
        self.spellcast_bonus_stat = kwargs.get("spellcast_bonus_stat")
        self.action_preference = kwargs.get(
            "action_preference", {ActionType.MELEE: 1, ActionType.RANGED: 4}
        )
        self.attacks_per_action = kwargs.get("attacks_per_action", 1)
        self.vulnerable = kwargs.get("vulnerable", [])
        self.resistant = kwargs.get("resistant", [])
        self.immunity = kwargs.get("immunity", [])
        self.cond_immunity = kwargs.get("cond_immunity", [])
        self.hp = kwargs["hp"]  # pylint: disable=invalid-name
        self.max_hp = self.hp
        self.has_grappled = None

        self.bonus_actions = []
        self.reactions = []
        self.actions = []
        for act in kwargs.get("actions", []):
            self.add_action(act)

        self.conditions = set([Condition.OK])

        self.effects = {}
        for effect in kwargs.get("effects", []):
            effect.owner = self
            self.effects[effect.name] = effect

        self.target = None
        self.coords = None
        self.statistics = []
        self.options_this_turn = []
        self.concentration = None
        self.damage_this_turn = []
        self.damage_last_turn = []

        self.gear = []
        for gear in kwargs.get("gear", []):
            self.add_gear(gear)

    ##########################################################################
    def _valid_args(self):  # pylint: disable=no-self-use
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
    def spellcast_save(self):
        """Saving throw DC vs spells from this creature"""
        if self.spellcast_bonus_stat is None:
            return 0
        return 8 + self.stat_bonus(self.spellcast_bonus_stat) + self.prof_bonus

    ##########################################################################
    @property
    def ac(self):  # pylint: disable=invalid-name
        """The armour class"""
        if self._ac is None:
            tmp = 0
            dbon = True  # Can we apply dex bonus
            max_db = 999  # Max Dex bonus
            for geah in self.gear:
                if issubclass(geah.__class__, Armour):
                    tmp += geah.ac + geah.ac_bonus + geah.magic_bonus
                    if not geah.dex_bonus:
                        dbon = False
                    max_db = min(max_db, geah.max_dex_bonus)
            if tmp == 0:  # No armour so default to 10
                tmp = 10
            if dbon:
                dexbonus = min(self.stat_bonus(Stat.DEX), max_db)
                tmp += dexbonus
        else:
            tmp = self._ac
        for _, eff in self.effects.items():
            mod = eff.hook_ac_modifier(self)
            tmp += mod
        return tmp

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
        if self.has_condition(Condition.UNCONSCIOUS):
            self.add_condition(Condition.OK)
            self.remove_condition(Condition.UNCONSCIOUS)
            print(f"{self} regained consciousness")
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
    def saving_throw(  # pylint: disable=invalid-name
        self, stat: Stat, dc: int, **kwargs
    ) -> bool:
        """Make a saving throw against a stat"""
        if self.has_condition(Condition.UNCONSCIOUS) and stat in (Stat.STR, Stat.DEX):
            print(
                f"{self} automatically failed {stat.value} saving throw as unconscious"
            )
            return False
        effct = {"bonus": 0}
        for _, eff in self.effects.items():
            effct.update(eff.hook_saving_throw(stat, **kwargs))

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
                return

            # Have to check every move if we are in any effect area
            for part in self.arena.combatants:
                for eff in part.effects.values():
                    for comb in self.arena.combatants:
                        eff.hook_start_in_range(comb)

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
        print(f"{self}: pick_attack_by_name({name=}) - none found")
        return None

    ##########################################################################
    def hit(  # pylint: disable=too-many-arguments
        self, dmg: int, dmg_type: DamageType, source, critical: bool, atkname: str
    ) -> None:
        """We've been hit by source- take damage"""
        dmg = self.react_predmg(dmg, dmg_type, source, critical)
        if dmg_type in self.vulnerable:
            print(f"{self} is vulnerable to {dmg_type.value}")
            dmg *= 2
        if dmg_type in self.immunity:
            print(f"{self} is immune to {dmg_type.value}")
            dmg = 0
        if dmg_type in self.resistant:
            print(f"{self} is resistant to {dmg_type.value}")
            dmg /= 2
        for eff in self.effects.values():
            dmg = eff.hook_being_hit(dmg, dmg_type)
        dmg = int(dmg)
        print(f"{self} has taken {dmg} damage ({dmg_type.value}) from {atkname}")
        self.hp -= dmg
        print(f"{self} now has {self.hp} HP")
        if dmg and self.concentration:
            svth = self.saving_throw(Stat.CON, max(10, int(dmg / 2)))
            if not svth:
                print(f"{self} failed concentration save on {self.concentration}")
                self.remove_concentration()

        source.statistics.append(Statistics(atkname, dmg, dmg_type, critical))
        self.damage_this_turn.append(Damage(dmg, dmg_type))

        if self.hp <= 0:
            self.fallen_unconscious(dmg, dmg_type, critical)
        else:
            self.react_postdmg(source)

    ##########################################################################
    def react_predmg(self, dmg: int, dmg_type: DamageType, source, critical: bool):
        """About to take damage - do we have a reaction that can alter the damage"""
        if ActionCategory.REACTION not in self.options_this_turn:
            return dmg
        react = self.pick_action(
            typ=ActionCategory.REACTION, target=source, need_hook="hook_predmg"
        )
        if react is not None:
            print(f"{self} reacts against {source}")
            dmg = react.hook_predmg(
                dmg=dmg, dmg_type=dmg_type, source=source, critical=critical
            )
            self.options_this_turn.remove(ActionCategory.REACTION)
        return dmg

    ##########################################################################
    def react_postdmg(self, source) -> None:
        """React to an incoming attack with a reaction"""
        if ActionCategory.REACTION not in self.options_this_turn:
            return
        react = self.pick_action(
            typ=ActionCategory.REACTION, target=source, need_hook="hook_postdmg"
        )
        if react is not None:
            print(f"{self} reacts against {source}")
            react.hook_postdmg()
            self.options_this_turn.remove(ActionCategory.REACTION)

    ##########################################################################
    def has_condition(self, *conditions: list) -> bool:
        """Do we have a condition"""
        for cond in conditions:
            if cond in self.conditions:
                return True
        return False

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
    def add_gear(self, gear):
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
        """return if the creature is alive"""
        return self.hp > 0

    ##########################################################################
    def shortrepr(self):  # pylint: disable=no-self-use
        """What it looks like on the arena"""
        return "?"

    ##########################################################################
    def fallen_unconscious(
        self,
        dmg: int,  # pylint: disable=unused-argument
        dmg_type: DamageType,  # pylint: disable=unused-argument
        critical: bool,  # pylint: disable=unused-argument
    ) -> None:
        """Creature has fallen unconscious"""
        keep_going = True
        for _, eff in self.effects.items():
            if not eff.hook_fallen_unconscious(dmg, dmg_type, critical):
                keep_going = False
        if not keep_going:
            return
        self.hp = 0
        if self.has_condition(Condition.UNCONSCIOUS):
            return
        self.remove_concentration()
        self.add_condition(Condition.UNCONSCIOUS)
        self.remove_condition(Condition.OK)
        if self.has_grappled:
            self.has_grappled.remove_condition(Condition.GRAPPLED)

    ##########################################################################
    def is_type(self, typ) -> bool:
        """Are we an instance of typ"""
        return self.type == typ

    ##########################################################################
    def end_turn(self, draw=True):
        """Are the any effects for the end of the turn"""
        for name, effect in self.effects.copy().items():
            remove = effect.removal_end_of_its_turn(self)
            if remove:
                self.remove_effect(name)
        if draw and self.has_condition(Condition.OK):
            print(self.arena)

    ##########################################################################
    def remove_effect(self, name):
        """Remove an effect"""
        self.effects[name].finish(self)
        del self.effects[name]

    ##########################################################################
    def has_effect(self, name) -> bool:
        """Do we have an effect"""
        return name in self.effects

    ##########################################################################
    def add_effect(self, effect):
        """Add an effect"""
        self.effects[effect.name] = effect
        effect.owner = self
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
        print(f"|  HP: {self.hp} / {self.max_hp}")
        print(f"|  AC: {self.ac}")
        if self.concentration:
            print(f"|  Concentration: {self.concentration}")
        if self.conditions:
            print(f"|  Conditions: {', '.join([_.value for _ in self.conditions])}")
        if self.effects:
            print(f"|  Effects: {', '.join(self.effects)}")
        if self.damage_this_turn:
            print(f"|  Damage This Turn: {self.damage_summary(self.damage_this_turn)}")
        if self.damage_last_turn:
            print(f"|  Damage Last Turn: {self.damage_summary(self.damage_last_turn)}")
        for act in self.actions + self.bonus_actions + self.reactions:
            if act.ammo is not None:
                print(f"|  {act} Ammo: {act.ammo}")

    ##########################################################################
    def damage_summary(self, dmglist):  # pylint: disable=no-self-use
        """Summarise damage"""
        if not dmglist:
            return "None"
        taken = defaultdict(int)
        for tkn in dmglist:
            if tkn.hp:
                taken[tkn.type] += tkn.hp
        output = []
        for typ, val in taken.items():
            output.append(f"{val} x {typ.value}")

        return ", ".join(output)

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
            if act.is_available():
                quality = act.get_heuristic()
                possible_acts.append((quality, act))
        return possible_acts

    ##########################################################################
    def spell_available(  # pylint: disable=no-self-use
        self, spell  # pylint: disable=unused-argument
    ) -> bool:
        """Spell casters should redefine this"""
        return False

    ##########################################################################
    def pick_action(
        self, typ=ActionCategory.ACTION, target=None, need_hook=None
    ) -> Action:
        """What are we going to do this turn based on individual action_preference
        If {need_hook} is set then the action must define that hook to be in contention
        """
        # The random is added a) as a tie breaker for sort b) for a bit of fun
        actions = []
        acttuple = namedtuple("acttuple", "qual rnd heur pref act")
        for heur, act in self.possible_actions(typ):
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

        action = actions[0].act
        if target is None:
            self.target = action.pick_target()
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
        self.damage_last_turn = self.damage_this_turn
        self.damage_this_turn = []
        if self.has_condition(Condition.PARALYZED):
            self.options_this_turn = []
        if not self.has_condition(Condition.OK):
            self.options_this_turn = []
        self.moves = self.speed
        for eff in self.effects.copy().values():
            eff.hook_start_turn()

        for part in self.arena.combatants:
            for eff in part.effects.values():
                for comb in self.arena.combatants:
                    eff.hook_start_in_range(comb)

        for creat in self.arena.combatants:
            if creat == self:
                creat.hook_start_turn()
                continue
            creat.start_others_turn(self)

    ##########################################################################
    def start_others_turn(self, creat):
        """Hook for another creature starting a turn near me"""

    ##########################################################################
    def hook_start_turn(self):
        """Hook for us starting a turn"""

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
                print(f"{msg} self as a {categ.value}")
            else:
                print(f"{msg} {self.target} as a {categ.value}")
            did_act = self.do_action(act)
            if did_act and act.action_cost:
                self.options_this_turn.remove(categ)

    ##########################################################################
    def add_concentration(self, spell):
        """Start a new concentration spell"""
        if self.concentration:
            print(f"{self} removing {self.concentration} as casting {spell}")
            self.remove_concentration()
        self.concentration = spell

    ##########################################################################
    def remove_concentration(self):
        """Stop concentrating on a  spell"""
        if not self.concentration:
            return
        self.concentration.end_concentration()
        self.concentration = None

    ##########################################################################
    def rolld20(self, reason):
        """Roll a d20"""
        d20 = int(dice.roll("d20"))
        for _, eff in self.effects.items():
            d20 = eff.hook_d20(d20, reason)
        return d20

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
