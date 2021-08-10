""" Class defining the play area """
import math
from collections import defaultdict
from astar import AStar
from constants import Stat


##############################################################################
##############################################################################
class Arena(AStar):
    """Arena Class"""

    ##############################################################################
    def __init__(self, **kwargs):
        self.max_x = kwargs.get("max_x", 20)
        self.max_y = kwargs.get("max_y", 20)
        self.grid = {}
        self.combatants = []
        for j in range(self.max_y):
            for i in range(self.max_x):
                self.grid[(i, j)] = None

    ##############################################################################
    def distance_between(self, n1, n2):
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
        for nbx in (node_x - 1, node_x + 2):
            for nby in (node_y - 1, node_y + 2):
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
            (_.roll_initiative(), _.stats[Stat.DEX], id(_), _) for _ in self.combatants
        ]
        tmp.sort(reverse=True)
        self.combatants = [_[-1] for _ in tmp]
        print(f"Initiative: {self.combatants}")

    ##############################################################################
    def turn(self):
        """Give all the combatants a turn in initiative order"""
        for comb in self.combatants:
            comb.turn()

    ##############################################################################
    def add_combatant(self, comb, coords):
        """Add a combatant"""
        self.combatants.append(comb)
        self[coords] = comb
        comb.coords = coords

    ##############################################################################
    def distance(self, one, two):  # pylint: disable=no-self-use
        """Return the distance in moves between two protagonists"""
        if one.coords is None or two.coords is None:
            print(
                f"Error: arena.distance(one={one}@{one.coords}, two={two}@{two.coords})"
            )
            return 999
        dist = math.sqrt(
            pow(one.coords[0] - two.coords[0], 2)
            + pow(one.coords[1] - two.coords[1], 2)
        )
        return dist

    ##############################################################################
    def move_towards(self, creat, target):
        """Move the creature creat towards target"""
        print(f"{creat} @ {creat.coords} moving to {target} @ {target.coords}")
        # We can't move to the target square because it is occupied so no route
        # so try all the adjacent squares for the shortest route
        routes = {}
        for delta_x in (-1, 0, 1):
            for delta_y in (-1, 0, 1):
                dest = (target.coords[0] + delta_x, target.coords[1] + delta_y)
                if dest not in self.grid:    # Not on map, don't bother trying
                    continue
                route_iter = self.astar(creat.coords, dest)
                print(f"{dest=} {route_iter=}")
                if route_iter:
                    routes[dest] = list(route_iter)
        print(f"{routes=}")

        if not routes:
            print("{creat} couldn't find path to {target}")
            return creat.coords

        # Now pick the shortest workable route
        shortest = 999
        target_adj = None
        for dest, rout in routes.items():
            if rout and len(rout) < shortest:
                shortest = len(rout)
                target_adj = dest
        route = routes[target_adj]

        print(f"{route=}")

        # Are we adjacent - then don't bother moving
        if len(route) < 2:
            print(f"{creat} already adjacent to {target}")
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
    def pick_closest_enemy(self, creat):
        """Pick the closest enemy to creat"""
        myside = creat.side
        otherside = [_ for _ in self.combatants if _.side != myside]
        closest = None
        close_dist = 9999
        for enemy in otherside:
            if not enemy.is_alive():
                continue
            dist = self.distance(creat, enemy)
            print(f"Looking to attack {enemy}@{enemy.coords} from {creat.coords}: {dist} distance")
            if dist < close_dist:
                dist = close_dist
                closest = enemy
        return closest

    ##############################################################################
    def still_going(self):
        """Do we still have alive combatants on both sides"""
        sides = self.remaining_participants_count()
        if len([_ for _ in sides if _]) > 1:
            return True
        return False

    ##############################################################################
    def remaining_participants(self):
        """Who is still standing"""
        sides = defaultdict(list)
        for participant in self.combatants:
            if participant.is_alive():
                sides[participant.side].append(participant)
        return sides

    ##############################################################################
    def remaining_participants_count(self):
        """How many are still standing"""
        sides = defaultdict(int)
        for participant in self.combatants:
            if participant.is_alive():
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
