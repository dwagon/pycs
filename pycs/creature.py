""" Parent class for all creatures """


class Creature:
    """Parent class for all creatures"""

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "No Name")
        self.armour = kwargs.get("armour", 10)
        self.speed = kwargs.get("speed", 30)
        self.size = kwargs.get("size", "M")
        self.stats = {}
        self.stats["str"] = kwargs.get("str", 11)
        self.stats["int"] = kwargs.get("str", 11)
        self.stats["dex"] = kwargs.get("str", 11)
        self.stats["wis"] = kwargs.get("str", 11)
        self.stats["con"] = kwargs.get("str", 11)
        self.stats["cha"] = kwargs.get("str", 11)


# EOF
