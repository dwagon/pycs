""" Class defining the play area """
import math
import random
from typing import Any, Optional
from collections import defaultdict
from collections import namedtuple
from astar import AStar
from pycs.constant import Stat, MonsterType
from pycs.creature import Creature


##############################################################################
##############################################################################
##############################################################################
class Arena(AStar):
    """Arena Class"""

    ##############################################################################
    def __init__(self, **kwargs: Any):
        self.max_x: int = kwargs.get("max_x", 20)
        self.max_y: int = kwargs.get("max_y", 20)
        self.grid: dict = {}
        self._combatants: list = []
        for j in range(self.max_y):
            for i in range(self.max_x):
                self.grid[(i, j)] = None

    ##############################################################################
    def distance_between(
        self, n1: tuple[int, int], n2: tuple[int, int]
    ) -> int:  # pylint: disable=unused-argument, invalid-name
        """This method always returns 1, as two 'neighbors' are always adjacent"""
        return 1

    ##########################################################################
    def heuristic_cost_estimate(self, current: tuple[int, int], goal: tuple[int, int]) -> float:
        """computes the 'direct' distance between two (x,y) tuples"""
        (point_x1, point_y1) = current
        (point_x2, point_y2) = goal
        hce = math.hypot(point_x2 - point_x1, point_y2 - point_y1)
        return hce

    ##########################################################################
    def neighbors(self, node: tuple[int, int]) -> list[tuple[int, int]]:
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
    def do_initiative(self) -> None:
        """Roll everyone's initiative and sort"""
        # ID is here as an ultimate tie breaker
        tmp = [(_.roll_initiative(), _.stats[Stat.DEX], id(_), _) for _ in self._combatants]
        tmp.sort(reverse=True)
        self._combatants = [_[-1] for _ in tmp]
        print(f"Initiative: {self._combatants}")

    ##############################################################################
    def turn(self) -> None:
        """Give all the combatants a turn in initiative order"""
        for comb in self.pick_everyone():
            comb.turn()

    ##############################################################################
    def remove_combatant(self, comb: Creature) -> None:
        """Remove combatant from arena - generally means dead"""
        self[comb.coords] = None

    ##############################################################################
    def add_combatant(self, comb: Creature, coords: Optional[tuple[int, int]] = None) -> None:
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
    def distance(self, one: Creature, two: Creature) -> int:
        """Return the distance in moves between two protagonists"""
        assert one.coords is not None
        assert two.coords is not None
        return self.distance_coords(one.coords, two.coords)

    ##############################################################################
    def distance_coords(self, one: tuple[int, int], two: tuple[int, int]) -> int:
        """Distance between two points"""
        assert isinstance(one, tuple)
        assert isinstance(two, tuple)
        dist = math.hypot(one[0] - two[0], one[1] - two[1])
        # Use floor() so that a diagonal still counts as range 1
        return math.floor(dist)

    ##############################################################################
    def move_away(self, creat: Creature, cause: Creature) -> tuple[int, int]:
        """Move away from {cause}"""
        dists = []
        result = namedtuple("result", "distance id coord")
        for nbour in self.neighbors(creat.coords):
            dists.append(result(self.distance_coords(nbour, cause.coords), id(nbour), nbour))
        dists.sort(reverse=True)
        dest = dists[0].coord
        self[creat.coords] = None
        self[dest] = creat
        return dest

    ##############################################################################
    def move_towards(self, creat: Creature, target: tuple[int, int]) -> tuple[int, int]:
        """Move the creature creat towards target coords one step"""
        # We can't move to the target square because it is occupied so no route
        # so try all the adjacent squares for the shortest route
        assert isinstance(target, tuple)
        routes = {}
        for dest in self.neighbors(target):
            route_iter = self.astar(creat.coords, dest)
            if route_iter:
                routes[dest] = list(route_iter)

        if not routes:
            print(f"{creat} couldn't find path to {target}")
            return creat.coords

        # Now pick the shortest workable route
        shortest = 999
        target_adj: tuple[int, int]
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
            print(f"{creat} @ {creat.coords} trying to jump in with {self[dest]} @ {dest}")
        self[creat.coords] = None
        self[dest] = creat
        return dest

    ##############################################################################
    def remaining_type(self, creat: Creature, typ_: MonsterType) -> list[Creature]:
        """Return the remaining combatants of the specified type"""
        remain = [_ for _ in self.pick_alive() if _.side != creat.side and _.is_type(typ_)]
        return remain

    ##############################################################################
    def pick_everyone(self) -> list[Creature]:
        """Return all combatants"""
        return self._combatants

    ##############################################################################
    def pick_alive(self) -> list[Creature]:
        """Return the list of living combatants"""
        combs = [_ for _ in self._combatants if _.is_alive()]
        return combs

    ##############################################################################
    def pick_closest_friends(self, creat: Creature) -> list[Creature]:
        """Pick the closest friends to creat sorted by distance"""
        result = namedtuple("result", "distance id creature")
        combs = [
            result(self.distance(creat, _), id(_), _)
            for _ in self.pick_alive()
            if _.side == creat.side and _ != creat
        ]
        combs.sort()
        res = [_.creature for _ in combs]
        return res

    ##############################################################################
    def pick_closest_enemy(self, creat: Creature) -> list[Creature]:
        """Pick the closest enemy creatures to {creat} sorted by distance"""
        result = namedtuple("result", "distance id creature")
        combs = [
            result(self.distance(creat, _), id(_), _)
            for _ in self.pick_alive()
            if _.side != creat.side
        ]
        combs.sort()
        res = [_.creature for _ in combs]
        return res

    ##############################################################################
    def still_going(self) -> bool:
        """Do we still have alive combatants on both sides"""
        sides = self.remaining_participants_count()
        if len([_ for _ in sides if _]) > 1:
            return True
        return False

    ##############################################################################
    def my_side(self, side: str) -> list[Creature]:
        """Who is still standing on my side"""
        return [_ for _ in self.pick_alive() if _.side == side]

    ##############################################################################
    def remaining_participants_count(self) -> defaultdict[str, int]:
        """How many are still standing"""
        sides: defaultdict[str, int] = defaultdict(int)
        for participant in self.pick_alive():
            sides[participant.side] += 1
        return sides

    ##############################################################################
    def winning_side(self) -> str:
        """Which side won?"""
        sides = self.remaining_participants_count()
        return list(sides.keys())[0]

    ##############################################################################
    def __setitem__(self, key: tuple[int, int], val: Any) -> None:
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
    def __getitem__(self, key: tuple[int, int]) -> Any:
        """Access the grid"""
        return self.grid[key]

    ##############################################################################
    def __repr__(self) -> str:
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
