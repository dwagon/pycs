""" Parent class for all creatures """
import dice


##############################################################################
##############################################################################
class Creature:
    """Parent class for all creatures"""

    ##########################################################################
    def __init__(self, arena, **kwargs):
        self.arena = arena
        self.name = kwargs.get("name", "No Name")
        self.ac = kwargs.get("ac", 10)
        self.speed = kwargs.get("speed", 30)
        self.size = kwargs.get("size", "M")
        self.side = kwargs["side"]  # Mandatory
        self.stats = {}
        self.stats["str"] = kwargs.get("str", 11)
        self.stats["int"] = kwargs.get("int", 11)
        self.stats["dex"] = kwargs.get("dex", 11)
        self.stats["wis"] = kwargs.get("wis", 11)
        self.stats["con"] = kwargs.get("con", 11)
        self.stats["cha"] = kwargs.get("cha", 11)
        if "hp" in kwargs:
            self.hp = kwargs["hp"]
        else:
            self.hp = self.roll_hp()
        self.actions = []
        self.target = None

    ##########################################################################
    def pick_target(self):
        """Pick the target for the creature"""
        self.arena.pick_closest_enemy(self)

    ##########################################################################
    def move_to_target(self):
        """Move to the target"""

    ##########################################################################
    def attack(self):
        """Attack the target"""

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
        self.pick_target()
        self.move_to_target()
        self.attack()


# EOF
