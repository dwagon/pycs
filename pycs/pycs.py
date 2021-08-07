"""Main module."""
from collections import defaultdict
from prettytable import PrettyTable
from monster.goblin import Goblin
from character.fighter import Fighter
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
    arena = Arena(x=10, y=10)
    goblin_a = Goblin(arena=arena, name="Goblin A", side="Goblins")
    goblin_b = Goblin(arena=arena, name="Goblin B", side="Goblins")
    fighter = Fighter(arena=arena, name="Frank", side="Fighters")
    arena.add_combatant(goblin_a, (0, 0))
    arena.add_combatant(goblin_b, (9, 0))
    arena.add_combatant(fighter, (9, 9))
    arena.do_initiative()
    print(f"{arena}")
    while arena.still_going():
        arena.turn()
        print(f"{arena}")
    return arena.winning_side()


# EOF
