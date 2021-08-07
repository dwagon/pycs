"""Main module."""
from collections import defaultdict
from prettytable import PrettyTable
from monster.goblin import Goblin
from character.fighter import Fighter
from arena import Arena

ROUNDS = 20


##############################################################################
def start():
    """Main"""
    stats = defaultdict(int)
    for _ in range(ROUNDS):
        winner = combat_test()
        stats[winner] += 1
    win_report(stats)


##############################################################################
def win_report(stats):
    """Who is winning"""
    print("\nWinning stats")
    tbl = PrettyTable()
    tbl.field_names = ["Side", "Win Count", "Percentage"]
    for side, wins in stats.items():
        tbl.add_row([side, wins, 100.0 * wins / ROUNDS])

    print(tbl)


##############################################################################
def combat_test():
    """Run through a combat"""
    print("#" * 80)
    arena = Arena(x=10, y=10)
    goblin = Goblin(arena=arena, side="Goblins")
    fighter = Fighter(arena=arena, hp=2, side="Fighters")
    arena.add_combatant(goblin, (0, 0))
    arena.add_combatant(fighter, (9, 9))
    arena.do_initiative()
    print(f"{arena}")
    while arena.still_going():
        arena.turn()
        print(f"{arena}")
    return arena.winning_side()


# EOF
