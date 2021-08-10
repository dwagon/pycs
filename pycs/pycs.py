"""Main module."""
from collections import defaultdict
from prettytable import PrettyTable

# from monster.skeleton import Skeleton
# from monster.goblin import Goblin
# from monster.ghoul import Ghoul
from monster.zombie import Zombie
from character.fighter import Fighter
from character.warlock import Warlock
from character.cleric import Cleric
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
    # skeleton_a = Skeleton(arena=arena, name="Skeleton", side="Monsters")
    # goblin = Goblin(arena=arena, name="Goblin", side="Monsters")
    # ghoul = Ghoul(arena=arena, name="Ghoul", side="Monsters")
    fighter = Fighter(arena=arena, name="Frank", side="Humans")
    warlock = Warlock(arena=arena, name="Walter", side="Humans")
    cleric = Cleric(arena=arena, name="Charlise", side="Humans")
    # arena.add_combatant(skeleton_a, (0, 0))
    # arena.add_combatant(goblin, (arena.max_x - 1, 0))
    # arena.add_combatant(ghoul, (arena.max_x / 2, 0))
    arena.add_combatant(Zombie(arena=arena, name="Zombie 1", side="Monsters"), (0, 0))
    arena.add_combatant(Zombie(arena=arena, name="Zombie 2", side="Monsters"), (4, 0))
    arena.add_combatant(Zombie(arena=arena, name="Zombie 3", side="Monsters"), (8, 0))
    arena.add_combatant(Zombie(arena=arena, name="Zombie 4", side="Monsters"), (12, 0))
    arena.add_combatant(Zombie(arena=arena, name="Zombie 5", side="Monsters"), (14, 0))
    arena.add_combatant(fighter, (arena.max_x - 1, arena.max_y - 1))
    arena.add_combatant(warlock, (0, arena.max_y - 1))
    arena.add_combatant(cleric, (int(arena.max_x / 2), arena.max_y - 1))
    arena.do_initiative()
    print(f"{arena}")
    while arena.still_going():
        print(f"##### Turn {turn}: {arena.remaining_participants()}")
        arena.turn()
        print(f"{arena}")
        turn += 1
        assert turn < 100
    statistics_report(arena)

    return arena.winning_side()


# EOF
