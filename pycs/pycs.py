"""Main module."""
from collections import defaultdict
from prettytable import PrettyTable
from monster.skeleton import Skeleton
from character.fighter import Fighter
from character.warlock import Warlock
from arena import Arena


##############################################################################
def start(rounds):
    """Main"""
    stats = defaultdict(int)
    for _ in range(rounds):
        winner = combat_test()
        stats[winner] += 1
    win_report(stats, rounds)


##############################################################################
def win_report(stats, rounds):
    """Who is winning"""
    print("\nWinning stats")
    tbl = PrettyTable()
    tbl.field_names = ["Side", "Win Count", "Percentage"]
    for side, wins in stats.items():
        tbl.add_row([side, wins, 100.0 * wins / rounds])

    print(tbl)


##############################################################################
def combat_test():
    """Run through a combat"""
    print("#" * 80)
    arena = Arena(x=40, y=20)
    skeleton_a = Skeleton(arena=arena, name="Skeleton A", side="Monsters")
    skeleton_b = Skeleton(arena=arena, name="Skeleton B", side="Monsters")
    skeleton_c = Skeleton(arena=arena, name="Skeleton C", side="Monsters")
    fighter = Fighter(arena=arena, name="Frank", side="Humans")
    warlock = Warlock(arena=arena, name="Walter", side="Humans")
    arena.add_combatant(skeleton_a, (0, 0))
    arena.add_combatant(skeleton_b, (arena.x - 1, 0))
    arena.add_combatant(skeleton_c, (arena.x / 2, 0))
    arena.add_combatant(fighter, (arena.x - 1, arena.y - 1))
    arena.add_combatant(warlock, (0, arena.y - 1))
    arena.do_initiative()
    print(f"{arena}")
    while arena.still_going():
        arena.turn()
        print(f"{arena}")
    return arena.winning_side()


# EOF
