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
        comb.coords = coords

    ##############################################################################
    def distance(self, one, two):
        """Return the distance in moves between two protagonists"""
        if one.coords is None or two.coords is None:
            print(f"Error: arena.distance(one={one}@{one.coords}, two={two}@{two.coords})")
            return 999
        dist = math.sqrt(
            pow(one.coords[0] - two.coords[0], 2)
            + pow(one.coords[1] - two.coords[1], 2)
        )
        return dist

    ##############################################################################
    def dir_to_move(self, one, two):
        """Direction to move for creature one to get closer to creature two"""
        # Replace with a* or equiv if we start getting complex arenas
        # Need to do basic collision detection at some point
        dirn = ""
        if pow(one.coords[0] - two.coords[0], 2) > pow(
            one.coords[1] - two.coords[1], 2
        ):
            if one.coords[0] > two.coords[0]:
                dirn = "W"
            if one.coords[0] < two.coords[0]:
                dirn = "E"
        else:
            if one.coords[1] > two.coords[1]:
                dirn = "N"
            if one.coords[1] < two.coords[1]:
                dirn = "S"
        print(f"dir_to_move({one}@{one.coords} -> {two}@{two.coords}) = {dirn}")
        return dirn

    ##############################################################################
    def move(self, creat, dirn):
        """Move the creature creat in direction dirn"""
        dirmap = {"W": (-1, 0), "E": (1, 0), "S": (0, 1), "N": (0, -1)}
        target = (creat.coords[0] + dirmap[dirn][0], creat.coords[1] + dirmap[dirn][1])
        if self[target] is None:
            self[creat.coords] = None
            self[target] = creat
        return target

    ##############################################################################
    def pick_closest_enemy(self, me):
        """Pick the closest enemy to me"""
        myside = me.side
        otherside = (set(self.combatants.keys()) - set(myside)).pop()
        closest = None
        close_dist = 9999
        for enemy in self.combatants[otherside]:
            print(f"Looking to move to {enemy}@{enemy.coords} from {me.coords}")
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
            lineout = []
            for i in range(self.x):
                cell = f"{i},{j}="
                if self.grid[(i, j)] is None:
                    cell += "."
                else:
                    cell += self.grid[(i, j)].shortrepr()
                lineout.append(cell)
            output.append(" ".join(lineout))
        return "\n".join(output)


# EOF
