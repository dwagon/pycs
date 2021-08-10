""" Parent class for all creatures """
# pylint: disable=too-many-public-methods
import dice
from attacks import Attack
from constants import Condition
from constants import Stat


##############################################################################
##############################################################################
class Creature:  # pylint: disable=too-many-instance-attributes
    """Parent class for all creatures"""

    ##########################################################################
    def __init__(self, arena, **kwargs):
        self.arena = arena
        self.name = kwargs.get("name", self.__class__.__name__)
        self.ac = kwargs.get("ac", 10)  # pylint: disable=invalid-name
        self.speed = int(kwargs.get("speed", 30) / 5)
        self.size = kwargs.get("size", "M")
        self.side = kwargs["side"]  # Mandatory
        self.stats = {
            Stat.STR: kwargs["str"],
            Stat.INT: kwargs["int"],
            Stat.DEX: kwargs["dex"],
            Stat.WIS: kwargs["wis"],
            Stat.CON: kwargs["con"],
            Stat.CHA: kwargs["cha"],
        }
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
        self.reactions = []
        self.conditions = set()
        self.temp_effects = {}
        self.target = None
        self.coords = None
        self.statistics = []

    ##########################################################################
    def __repr__(self):
        return f"{self.name}"

    ##########################################################################
    def stat_bonus(self, stat):
        """What's the stat bonus for the stat"""
        return int((self.stats[stat] - 10) / 2)

    ##########################################################################
    def saving_throw(self, stat, dc):  # pylint: disable=invalid-name
        """Make a saving throw against a stat"""
        # Need to add stat proficiency
        if self.has_condition(Condition.UNCONSCIOUS) and stat in (Stat.STR, Stat.DEX):
            print(
                f"{self} automatically failed {stat.value} saving throw as unconscious"
            )
            return False
        save = int(dice.roll("d20")) + self.stat_bonus(stat)
        if save >= dc:
            print(f"{self} made {stat.value} saving throw: {save} vs DC {dc}")
            return True
        print(f"{self} failed {stat.value} saving throw: {save} vs DC {dc}")
        return False

    ##########################################################################
    def roll_initiative(self):
        """Roll initiative"""
        init = dice.roll(f"d20+{self.stat_bonus(Stat.DEX)}")
        print(f"{self} rolled {init} for initiative")
        return init

    ##########################################################################
    def pick_target(self):
        """Pick the target for the creature
        This should be overwritten for cleverness
        """
        # Keep it simple and just go for the closest
        self.target = self.arena.pick_closest_enemy(self)
        if self.target is None:
            print(f"{self} No more enemies to fight")
        else:
            print(f"{self} picked {self.target} as target")

    ##########################################################################
    def move_to_target(self):
        """Move to the target"""
        if not self.target:
            return
        if self.has_condition(Condition.GRAPPLED):
            print(f"{self} is grappled - not moving")
            return
        print(f"{self} moving to {self.target}")
        for _ in range(self.speed):
            rnge, _ = self.get_attack_range()
            # Within range - don't move
            dist = self.arena.distance(self, self.target)
            if dist <= rnge:
                print(f"{self} within {rnge} range of {self.target}: {dist}")
                return
            old_coords = self.coords
            self.coords = self.arena.move_towards(self, self.target)
            if old_coords == self.coords:
                # We aren't moving - don't keep trying
                break

    ##########################################################################
    def get_attack_range(self):
        """Return the range and the attack with the longest range"""
        attack = None
        rnge = 0
        for atk in self.actions:
            _, long = atk.range()
            if long > rnge:
                rnge = long
                attack = atk
        return rnge, attack

    ##########################################################################
    def pick_attack_by_name(self, name):
        """Pick the attack by name"""
        for atk in self.actions:
            if atk.name == name:
                return atk
        return None

    ##########################################################################
    def pick_best_attack(self):
        """Return the best (most damage) attack for this range"""
        # Treat disdvantage as having half damage - need to make this cleverer
        if self.target is None:
            return None
        rnge = self.arena.distance(self, self.target)
        maxdmg = 0
        attck = None
        for atk in self.actions:
            if not atk.is_available(self):
                continue
            if atk.range()[1] < rnge:
                continue
            mxd = atk.max_dmg(self.target)
            if atk.has_disadvantage(self, self.target, rnge):
                mxd /= 2
            if mxd > maxdmg:
                maxdmg = mxd
                attck = atk
        return attck

    ##########################################################################
    def pick_best_reaction(self, source):
        """Return the best (most damage) reaction for this range"""
        # Treat disdvantage as having half damage - need to make this cleverer
        rnge = self.arena.distance(self, source)
        maxdmg = 0
        attck = None
        for atk in self.reactions:
            if not atk.is_available(self):
                continue
            if atk.range()[1] < rnge:
                continue
            mxd = atk.max_dmg(source)
            if atk.has_disadvantage(self, self.target, rnge):
                mxd /= 2
            if mxd > maxdmg:
                maxdmg = mxd
                attck = atk
        return attck

    ##########################################################################
    def attack(self):
        """Attack the target"""
        if self.target is None:
            return
        print(f"{self} attacking {self.target}")
        attck = self.pick_best_attack()
        if attck is None:
            print(f"{self} has no attack")
            return
        rnge = self.arena.distance(self, self.target)
        attck.perform_action(self, self.target, rnge)

    ##########################################################################
    def hit(self, dmg, dmg_type, source, critical):
        """We've been hit by source- take damage"""
        print(f"{self} has taken {dmg} damage")
        self.hp -= dmg
        print(f"{self} now has {self.hp} HP")
        if self.hp <= 0:
            self.fallen_unconscious(dmg, dmg_type, critical)
        else:
            if self.reactions:
                rnge = self.arena.distance(self, source)
                self.react(source, rnge)

    ##########################################################################
    def react(self, source, rnge):
        """React to an incoming attack with a reaction"""
        react = self.pick_best_reaction(source)
        if react is not None:
            print(f"{self} reacts against {source}")
            react.perform_action(self, source, rnge)

    ##########################################################################
    def has_condition(self, cond):
        """Do we have a condition"""
        return cond in self.conditions

    ##########################################################################
    def remove_condition(self, cond):
        """Remove a condition"""
        self.conditions.remove(cond)

    ##########################################################################
    def add_condition(self, cond, source=None):
        """Add a condition - inflicted by source"""
        if cond not in self.cond_immunity:
            if source:
                print(f"{self} got {cond.value} from {source}")
            else:
                print(f"{self} got {cond.value}")
            self.conditions.add(cond)

    ##########################################################################
    def add_action(self, action):
        """Add an action to the creature"""
        self.actions.append(action)

    ##########################################################################
    def add_reaction(self, action):
        """Add an reaction to the creature"""
        self.reactions.append(action)

    ##########################################################################
    def roll_hp(self):
        """Roll the initial hitpoints"""
        if not hasattr(self, "hitdice"):
            self.hitdice = ""
        return int(dice.roll(self.hitdice))

    ##########################################################################
    def is_alive(self):
        """return if the creature is alive"""
        return self.hp > 0

    ##########################################################################
    def shortrepr(self):
        """What it looks like on the arena"""
        raise NotImplementedError(
            f"{self.__class__.__name__} needs to implement shortrepr()"
        )

    ##########################################################################
    def choose_action(self):
        """What action are we going to take"""
        if self.target is None:
            return None
        attck = self.pick_best_attack()
        return attck

    ##########################################################################
    def fallen_unconscious(
        self, dmg, dmg_type, critical
    ):  # pylint: disable=unused-argument
        """Creature has fallen unconscious"""
        self.hp = 0
        self.state = "UNCONSCIOUS"
        self.add_condition(Condition.UNCONSCIOUS)
        if self.has_grappled:
            self.has_grappled.remove_condition(Condition.GRAPPLED)
        print(f"{self} has fallen unconscious")

    ##########################################################################
    def check_end_effects(self):
        """Are the any effects for the end of the turn"""
        for effect, hook in self.temp_effects.copy().items():
            remove = hook(self)
            if remove:
                self.remove_temp_effect(effect)

    ##########################################################################
    def remove_temp_effect(self, name):
        """Remove a temporary effect"""
        del self.temp_effects[name]

    ##########################################################################
    def add_temp_effect(self, name, hook):
        """Add a temporary effect"""
        self.temp_effects[name] = hook

    ##########################################################################
    def check_start_effects(self):
        """Are there any effects for the start of the turn"""
        for creat in self.arena.combatants:
            if creat == self:
                creat.start_turn()
                continue
            creat.start_others_turn(self)

    ##########################################################################
    def dump_statistics(self):
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
    def start_turn(self):
        """Start the turn"""

    ##########################################################################
    def start_others_turn(self, creat):
        """Hook for anothing creature starting a turn near me"""

    ##########################################################################
    def turn(self):
        """Have a go"""
        print()
        print(f"{self.name} having a turn")
        if self.has_condition(Condition.PARALYZED):
            print(f"{self} is paralyzed")
            return
        if self.state != "OK":
            print(f"{self.name} {self.state}")
            return
        self.check_start_effects()
        self.pick_target()
        self.move_to_target()
        action = self.choose_action()
        if action is None and self.target:
            print(f"{self} dashing")
            self.move_to_target()  # dash
            return
        if issubclass(action.__class__, Attack):
            self.attack()
        else:
            action.perform_action(self, self.target, 0)

        self.check_end_effects()


# EOF
