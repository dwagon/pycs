""" Parent class for all creatures """
import dice


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
        self.stats["str"] = kwargs.get("str", 11)
        self.stats["int"] = kwargs.get("int", 11)
        self.stats["dex"] = kwargs.get("dex", 11)
        self.stats["wis"] = kwargs.get("wis", 11)
        self.stats["con"] = kwargs.get("con", 11)
        self.stats["cha"] = kwargs.get("cha", 11)
        self.state = "OK"
        if "hp" in kwargs:
            self.hp = kwargs["hp"]
        else:
            self.hp = self.roll_hp()
        self.actions = []
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
    def roll_initiative(self):
        """Roll initiative"""
        init = dice.roll(f"d20+{self.stat_bonus('dex')}")
        print(f"{self} rolled {init} for initiative")
        return init

    ##########################################################################
    def pick_target(self):
        """Pick the target for the creature
        This should be overwritten for cleverness
        """
        # Keep it simple and just go for the closest
        self.target = self.arena.pick_closest_enemy(self)
        print(f"{self} picked {self.target} as target")

    ##########################################################################
    def move_to_target(self):
        """Move to the target"""
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
            print(f"{self} thinking about using {atk}")
            _, long = atk.range()
            if long > rnge:
                rnge = long
                attack = atk
        print(f"{self} picking {attack} with range {rnge}")
        return rnge, attack

    ##########################################################################
    def pick_best_attack(self):
        """Return the best (most damage) attack for this range"""
        # Treat disdvantage as having half damage - need to make this cleverer
        rnge = self.arena.distance(self, self.target)
        maxdmg = 0
        attck = None
        for atk in self.actions:
            if atk.range()[1] < rnge:
                continue
            mxd = atk.max_dmg()
            if atk.has_disadvantage(rnge):
                mxd /= 2
            if mxd > maxdmg:
                maxdmg = mxd
                attck = atk
        print(f"{self} picking {attck}")
        return attck

    ##########################################################################
    def roll_to_hit(self, attck):
        """Roll to hit with the attack"""
        rnge = self.arena.distance(self, self.target)
        if attck.has_disadvantage(rnge):
            to_hit = min(dice.roll(f"d20{attck.bonus}"), dice.roll(f"d20{attck.bonus}"))
        else:
            to_hit = dice.roll(f"d20{attck.bonus}")
        return to_hit

    ##########################################################################
    def attack(self):
        """Attack the target"""
        print(f"{self} attacking {self.target}")
        attck = self.pick_best_attack()
        if attck is None:
            print(f"{self} has no attack")
            return
        to_hit = self.roll_to_hit(attck)
        print(f"{self} rolled {to_hit}")
        if to_hit > self.target.ac:
            dmg = dice.roll(attck.dmg)
            print(f"{self} hit {self.target} with {attck} for {dmg}")
            self.target.hit(dmg)
        else:
            print(f"{self} missed {self.target} with {attck}")

    ##########################################################################
    def hit(self, dmg):
        """We've been hit - take damage"""
        print(f"{self} has taken {dmg} damage")
        self.hp -= dmg
        print(f"{self} now has {self.hp} HP")
        if self.hp <= 0:
            self.hp = 0
            self.state = "UNCONSCIOUS"
            print(f"{self} has fallen unconscious")

    ##########################################################################
    def add_action(self, action):
        """Add an action to the creature"""
        self.actions.append(action)

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
    def turn(self):
        """Have a go"""
        print()
        if self.state != "OK":
            print(f"{self.name} {self.state}")
            return
        print(f"{self.name} having a turn")
        self.pick_target()
        self.move_to_target()
        self.attack()


# EOF
