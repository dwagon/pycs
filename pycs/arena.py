""" Class defining the play area """
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
    def add_combatant(self, comb, coords, side):
        """Add a combatant"""
        self.combatants[side].append(comb)
        self[coords] = comb

    ##############################################################################
    def still_going(self):
        """ Do we still have alive combatants on both sides """
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
