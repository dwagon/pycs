"""Top-level package for pycs."""

__author__ = """Dougal Scott"""
__email__ = "dougal.scott@gmail.com"
__version__ = "0.1.0"

from collections import defaultdict
from prettytable import PrettyTable

from pycs.monster.ghast import Ghast
from pycs.monster.ghoul import Ghoul
from pycs.monster.giant_frog import GiantFrog
from pycs.monster.goblin import Goblin
from pycs.monster.skeleton import Skeleton
from pycs.monster.troll import Troll
from pycs.monster.violet_fungus import VioletFungus
from pycs.monster.wraith import Wraith

from pycs.character.barbarian import Barbarian
from pycs.character.cleric import Cleric
from pycs.character.fighter import Fighter
from pycs.character.paladin import Paladin
from pycs.character.warlock import Warlock

from pycs.arena import Arena


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
    arena.add_combatant(VioletFungus(arena=arena, name="Violet", side="Monsters"))
    arena.add_combatant(Wraith(arena=arena, name="Wraith", side="Monsters"))
    arena.add_combatant(Troll(arena=arena, name="Troll", side="Monsters"))

    arena.add_combatant(Barbarian(arena=arena, name="Barbara", level=4, side="Humans"))
    arena.add_combatant(Cleric(arena=arena, name="Charlise", level=5, side="Humans"))
    arena.add_combatant(Fighter(arena=arena, name="Frank", level=4, side="Humans"))
    arena.add_combatant(Paladin(arena=arena, name="Patty", level=4, side="Humans"))
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
