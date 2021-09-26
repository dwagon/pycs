""" Class defining the play area """
import math
import random
from collections import defaultdict
from collections import namedtuple
from astar import AStar
from pycs.constant import Stat


##############################################################################
##############################################################################
class Arena(AStar):
    """Arena Class"""

    ##############################################################################
    def __init__(self, **kwargs):
        self.max_x = kwargs.get("max_x", 20)
        self.max_y = kwargs.get("max_y", 20)
        self.grid = {}
        self._combatants = []
        for j in range(self.max_y):
            for i in range(self.max_x):
                self.grid[(i, j)] = None

    ##############################################################################
    def distance_between(self, n1, n2):  # pylint: disable=unused-argument, invalid-name
        """This method always returns 1, as two 'neighbors' are always adjacent"""
        return 1

    ##########################################################################
    def heuristic_cost_estimate(self, current, goal):
        """computes the 'direct' distance between two (x,y) tuples"""
        (point_x1, point_y1) = current
        (point_x2, point_y2) = goal
        hce = math.hypot(point_x2 - point_x1, point_y2 - point_y1)
        return hce

    ##########################################################################
    def neighbors(self, node):
        """Returns all the places we can reach from node"""
        node_x, node_y = node
        ans = []
        for nbx in range(node_x - 1, node_x + 2):
            for nby in range(node_y - 1, node_y + 2):
                if nbx == node_x and nby == node_y:
                    continue
                pos = (nbx, nby)
                try:
                    if self[pos] is None:
                        ans.append(pos)
                except KeyError:  # Skip off the edge
                    continue
        return ans

    ##############################################################################
    def do_initiative(self):
        """Roll everyone's initiative and sort"""
        # ID is here as an ultimate tie breaker
        tmp = [
            (_.roll_initiative(), _.stats[Stat.DEX], id(_), _) for _ in self._combatants
        ]
        tmp.sort(reverse=True)
        self._combatants = [_[-1] for _ in tmp]
        print(f"Initiative: {self._combatants}")

    ##############################################################################
    def turn(self):
        """Give all the combatants a turn in initiative order"""
        for comb in self.pick_everyone():
            comb.turn()

    ##############################################################################
    def remove_combatant(self, comb) -> None:
        """Remove combatant from arena - generally means dead"""
        self[comb.coords] = None
        comb.coords = None

    ##############################################################################
    def add_combatant(self, comb, coords=None) -> None:
        """Add a combatant"""
        comb.arena = self
        self._combatants.append(comb)
        if coords is None:
            while True:
                rndx = random.randint(0, self.max_x - 1)
                rndy = random.randint(0, self.max_y - 1)
                if self[(rndx, rndy)] is None:
                    coords = (rndx, rndy)
                    break
        self[coords] = comb
        comb.coords = coords

    ##############################################################################
    def distance(self, one, two):
        """Return the distance in moves between two protagonists"""
        assert one.coords is not None
        assert two.coords is not None
        dist = math.hypot(one.coords[0] - two.coords[0], one.coords[1] - two.coords[1])
        # Use floor() so that a diagonal still counts as range 1
        return math.floor(dist)

    ##############################################################################
    def move_towards(self, creat, target):
        """Move the creature creat towards target one step"""
        # print(f"{creat} @ {creat.coords} moving to {target} @ {target.coords}")
        # We can't move to the target square because it is occupied so no route
        # so try all the adjacent squares for the shortest route
        routes = {}
        for delta_x in (-1, 0, 1):
            for delta_y in (-1, 0, 1):
                dest = (target.coords[0] + delta_x, target.coords[1] + delta_y)
                if dest not in self.grid:  # Not on map, don't bother trying
                    continue
                route_iter = self.astar(creat.coords, dest)
                if route_iter:
                    routes[dest] = list(route_iter)

        if not routes:
            print(f"{creat} couldn't find path to {target}")
            return creat.coords

        # Now pick the shortest workable route
        shortest = 999
        target_adj = None
        for dest, rout in routes.items():
            if rout and len(rout) < shortest:
                shortest = len(rout)
                target_adj = dest
        route = routes[target_adj]

        # Are we adjacent - then don't bother moving
        if len(route) < 2:
            return creat.coords

        dest = route[1]
        if self[dest] is not None:
            print(
                f"{creat} @ {creat.coords} trying to jump in with {self[dest]} @ {dest}"
            )
        self[creat.coords] = None
        self[dest] = creat
        return dest

    ##############################################################################
    def remaining_type(self, creat, typ_):
        """Return the remaining combatants of the specified type"""
        remain = [
            _ for _ in self.pick_alive() if _.side != creat.side and _.is_type(typ_)
        ]
        return remain

    ##############################################################################
    def pick_everyone(self):
        """Return all combatants"""
        return self._combatants

    ##############################################################################
    def pick_alive(self):
        """Return the list of living combatants"""
        combs = [_ for _ in self._combatants if _.is_alive()]
        return combs

    ##############################################################################
    def pick_closest_friends(self, creat):
        """Pick the closest friends to creat sorted by distance"""
        result = namedtuple("result", "distance id creature")
        combs = [
            result(self.distance(creat, _), id(_), _)
            for _ in self.pick_alive()
            if _.side == creat.side and _ != creat
        ]
        combs.sort()
        result = [_.creature for _ in combs]
        return result

    ##############################################################################
    def pick_closest_enemy(self, creat):
        """Pick the closest enemy creatures to {creat} sorted by distance"""
        result = namedtuple("result", "distance id creature")
        combs = [
            result(self.distance(creat, _), id(_), _)
            for _ in self.pick_alive()
            if _.side != creat.side and _.is_alive()
        ]
        combs.sort()
        result = [_.creature for _ in combs]
        return result

    ##############################################################################
    def still_going(self):
        """Do we still have alive combatants on both sides"""
        sides = self.remaining_participants_count()
        if len([_ for _ in sides if _]) > 1:
            return True
        return False

    ##############################################################################
    def my_side(self, side):
        """Who is still standing on my side"""
        return [_ for _ in self.pick_alive() if _.side == side]

    ##############################################################################
    def remaining_participants_count(self):
        """How many are still standing"""
        sides = defaultdict(int)
        for participant in self.pick_alive():
            sides[participant.side] += 1
        return sides

    ##############################################################################
    def winning_side(self):
        """Which side won?"""
        sides = self.remaining_participants_count()
        return list(sides.keys())[0]

    ##############################################################################
    def __setitem__(self, key, val):
        """Change the grid"""
        assert isinstance(key, tuple)
        assert isinstance(key[0], int)
        assert isinstance(key[1], int)
        assert key[0] >= 0
        assert key[0] < self.max_x
        assert key[1] >= 0
        assert key[1] < self.max_y
        self.grid[key] = val

    ##############################################################################
    def __getitem__(self, key):
        """Access the grid"""
        return self.grid[key]

    ##############################################################################
    def __repr__(self):
        """Display the grid"""
        output = []
        for j in range(self.max_y):
            lineout = []
            for i in range(self.max_x):
                cell = ""
                # cell = f"{i},{j}="
                if self.grid[(i, j)] is None:
                    cell += "."
                else:
                    cell += self.grid[(i, j)].shortrepr()
                lineout.append(cell)
            output.append(" ".join(lineout))
        return "\n".join(output)


# EOF
