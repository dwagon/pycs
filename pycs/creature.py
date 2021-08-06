""" Parent class for all creatures """


##############################################################################
##############################################################################
class Creature:
    """Parent class for all creatures"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "No Name")
        self.armour = kwargs.get("armour", 10)
        self.speed = kwargs.get("speed", 30)
        self.size = kwargs.get("size", "M")
        self.stats = {}
        self.stats["str"] = kwargs.get("str", 11)
        self.stats["int"] = kwargs.get("int", 11)
        self.stats["dex"] = kwargs.get("dex", 11)
        self.stats["wis"] = kwargs.get("wis", 11)
        self.stats["con"] = kwargs.get("con", 11)
        self.stats["cha"] = kwargs.get("cha", 11)
        self.hp = kwargs.get("hp", 0)

    ##########################################################################
    def is_alive(self):
        """ return if the creature is alive """
        return self.hp > 0

    ##########################################################################
    def shortrepr(self):
        """ What it looks like on the arena """
        raise NotImplementedError(f"{self.__class__.__name__} needs to implement shortrepr()")

    ##########################################################################
    def turn(self):
        """ Have a go """
        raise NotImplementedError(f"{self.__class__.__name__} needs to implement turn()")
# EOF
