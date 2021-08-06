""" Class defining the play area """
import math
from collections import defaultdict


##############################################################################
##############################################################################
class Arena:
    """Arena Class"""

    ##############################################################################
    def __init__(self, **kwargs):
        self.x = kwargs.get("x", 20)
        self.y = kwargs.get("y", 20)
        self.grid = {}
        self.combatants = defaultdict(list)
        for j in range(self.y):
            for i in range(self.x):
                self.grid[(i, j)] = None

    ##############################################################################
    def add_combatant(self, comb, coords):
        """Add a combatant"""
        side = comb.side
        self.combatants[side].append(comb)
        self[coords] = comb
        comb.coord = coords

    ##############################################################################
    def distance(self, one, two):
        """Return the distance in moves between two protagonists"""
        dist = math.sqrt(
            pow(one.coords[0] - two.coords[0], 2)
            + pow(one.coords[1] - two.coords[1], 2)
        )
        return dist

    ##############################################################################
    def pick_closest_enemy(self, me):
        """Pick the closest enemy to me"""
        myside = me.side
        otherside = set(self.combatants.keys()) - set(myside)
        closest = None
        close_dist = 9999
        for enemy in self.combatants[otherside]:
            dist = self.distance(me, enemy)
            if dist < close_dist:
                dist = close_dist
                closest = enemy
        return closest

    ##############################################################################
    def still_going(self):
        """Do we still have alive combatants on both sides"""
        sides = set()
        for side, participants in self.combatants.items():
            for part in participants:
                if part.is_alive():
                    sides.add(side)
        if len(sides) > 1:
            return True
        return False

    ##############################################################################
    def __setitem__(self, key, val):
        """Change the grid"""
        self.grid[key] = val

    ##############################################################################
    def __getitem__(self, key):
        """Access the grid"""
        return self.grid[key]

    ##############################################################################
    def __repr__(self):
        """Display the grid"""
        output = []
        for j in range(self.y):
            outstr = ""
            for i in range(self.x):
                if self.grid[(i, j)] is None:
                    outstr += "."
                else:
                    outstr += self.grid[(i, j)].shortrepr()
            output.append(outstr)
        return "\n".join(output)


# EOF
