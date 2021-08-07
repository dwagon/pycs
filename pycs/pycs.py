"""Main module."""
from collections import defaultdict
from prettytable import PrettyTable
from monster.goblin import Goblin
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
    goblin_a = Goblin(arena=arena, name="Goblin A", side="Goblins")
    goblin_b = Goblin(arena=arena, name="Goblin B", side="Goblins")
    fighter = Fighter(arena=arena, name="Frank", side="Fighters")
    warlock = Warlock(arena=arena, name="Walter", side="Fighters")
    arena.add_combatant(goblin_a, (0, 0))
    arena.add_combatant(goblin_b, (arena.x - 1, 0))
    arena.add_combatant(fighter, (arena.x - 1, arena.y - 1))
    arena.add_combatant(warlock, (0, arena.y - 1))
    arena.do_initiative()
    print(f"{arena}")
    while arena.still_going():
        arena.turn()
        print(f"{arena}")
    return arena.winning_side()


# EOF
