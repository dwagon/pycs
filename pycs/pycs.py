"""Main module."""
from collections import defaultdict
from prettytable import PrettyTable

from monster.skeleton import Skeleton
from monster.goblin import Goblin
from monster.ghoul import Ghoul
from monster.ghast import Ghast
from monster.giant_frog import GiantFrog

from character.barbarian import Barbarian
from character.cleric import Cleric
from character.fighter import Fighter
from character.paladin import Paladin
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
def statistics_report(arena):
    """Dump the hit statistics at the end"""
    tbl = PrettyTable()
    tbl.field_names = [
        "Name",
        "Attack",
        "Hits",
        "Misses",
        "Hit %",
        "Damage",
        "Crit %",
        "HP",
        "State",
    ]
    for creat in arena.combatants:
        tmp = creat.dump_statistics()
        for key, val in tmp.items():
            try:
                crit_p = int(100.0 * val["crits"] / val["hits"])
            except ZeroDivisionError:
                crit_p = 0
            tbl.add_row(
                [
                    creat.name,
                    key,
                    val["hits"],
                    val["misses"],
                    int(100.0 * val["hits"] / (val["hits"] + val["misses"])),
                    val["dmg"],
                    crit_p,
                    f"{creat.hp}/{creat.max_hp}",
                    creat.state.title(),
                ]
            )
    tbl.sortby = "Name"
    tbl.align["Name"] = "l"
    tbl.align["Attack"] = "l"
    print(tbl)


##############################################################################
def combat_test():
    """Run through a combat"""
    turn = 0
    print("#" * 80)
    arena = Arena(max_x=40, max_y=20)

    arena.add_combatant(Ghast(arena=arena, name="Ghast", side="Monsters"))
    arena.add_combatant(Ghoul(arena=arena, name="Ghoul", side="Monsters"))
    arena.add_combatant(GiantFrog(arena=arena, name="Giant Frog", side="Monsters"))
    arena.add_combatant(Skeleton(arena=arena, name="Skeleton", side="Monsters"))
    arena.add_combatant(Goblin(arena=arena, name="Goblin", side="Monsters"))

    arena.add_combatant(Barbarian(arena=arena, name="Barbara", level=1, side="Humans"))
    arena.add_combatant(Barbarian(arena=arena, name="Betty", level=2, side="Humans"))
    arena.add_combatant(Cleric(arena=arena, name="Charlise", level=3, side="Humans"))
    arena.add_combatant(Fighter(arena=arena, name="Frank", level=2, side="Humans"))
    arena.add_combatant(Paladin(arena=arena, name="Patty", level=5, side="Humans"))
    arena.add_combatant(Warlock(arena=arena, name="Wendy", level=1, side="Humans"))
    arena.do_initiative()
    print(f"{arena}")
    while arena.still_going():
        print(f"##### Turn {turn}: {dict(arena.remaining_participants())}")
        arena.turn()
        turn += 1
        assert turn < 100
    statistics_report(arena)

    return arena.winning_side()


# EOF
