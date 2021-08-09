""" Parent class for all creatures """
# pylint: disable=too-many-public-methods
import dice
from attacks import Attack
from constants import Condition
from constants import Stat


##############################################################################
##############################################################################
class Creature:
    """Parent class for all creatures"""

    ##########################################################################
    def __init__(self, arena, **kwargs):
        self.arena = arena
        self.name = kwargs.get("name", self.__class__.__name__)
        self.ac = kwargs.get("ac", 10)
        self.speed = int(kwargs.get("speed", 30) / 5)
        self.size = kwargs.get("size", "M")
        self.side = kwargs["side"]  # Mandatory
        self.stats = {}
        self.stats[Stat.STR] = kwargs.get("str", 11)
        self.stats[Stat.INT] = kwargs.get("int", 11)
        self.stats[Stat.DEX] = kwargs.get("dex", 11)
        self.stats[Stat.WIS] = kwargs.get("wis", 11)
        self.stats[Stat.CON] = kwargs.get("con", 11)
        self.stats[Stat.CHA] = kwargs.get("cha", 11)
        self.vulnerable = kwargs.get("vulnerable", [])
        self.immunity = kwargs.get("immunity", [])
        self.state = "OK"
        if "hp" in kwargs:
            self.hp = kwargs["hp"]
        else:
            self.hp = self.roll_hp()
        self.max_hp = self.hp
        self.actions = []
        self.reactions = []
        self.conditions = set()
        self.target = None
        self.coords = None

    ##########################################################################
    def __repr__(self):
        return f"{self.name}"

    ##########################################################################
    def stat_bonus(self, stat):
        """What's the stat bonus for the stat"""
        return int((self.stats[stat] - 10) / 2)

    ##########################################################################
    def saving_throw(self, stat, dc):
        """Make a saving throw against a stat"""
        # Need to add stat proficiency
        save = int(dice.roll("d20")) + self.stat_bonus(stat)
        if save >= dc:
            print(f"{self} made {stat} saving throw: {save} vs DC {dc}")
            return True
        print(f"{self} failed {stat} saving throw: {save} vs DC {dc}")
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
        print(f"{self} moving to {self.target}")
        for _ in range(self.speed):
            rnge, _ = self.get_attack_range()
            if self.arena.distance(self, self.target) < rnge:
                # Within range - don't move
                return
            dirn = self.arena.dir_to_move(self, self.target)
            self.coords = self.arena.move(self, dirn)

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
            if atk.has_disadvantage(rnge):
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
            if atk.has_disadvantage(rnge):
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
    def hit(self, dmg, source):
        """We've been hit by source- take damage"""
        print(f"{self} has taken {dmg} damage")
        self.hp -= dmg
        print(f"{self} now has {self.hp} HP")
        if self.hp <= 0:
            self.hp = 0
            self.state = "UNCONSCIOUS"
            print(f"{self} has fallen unconscious")
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
    def add_condition(self, cond):
        """Add a condition"""
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
        self.pick_target()
        self.move_to_target()
        action = self.choose_action()
        if action is None:
            print(f"{self} dashing")
            self.move_to_target()  # dash
            return
        if issubclass(action.__class__, Attack):
            self.attack()
        else:
            action.perform_action(self, self.target, 0)


# EOF
