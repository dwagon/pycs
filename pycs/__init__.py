"""Top-level package for pycs."""

__author__ = """Dougal Scott"""
__email__ = "dougal.scott@gmail.com"

from collections import defaultdict
from prettytable import PrettyTable
import colors
import dice

from pycs.monsters import AdultGoldDragon
from pycs.monsters import BarbedDevil
from pycs.monsters import Ghast
from pycs.monsters import Ghoul
from pycs.monsters import GiantFrog
from pycs.monsters import Goblin
from pycs.monsters import Hobgoblin
from pycs.monsters import Kobold
from pycs.monsters import Orc
from pycs.monsters import Skeleton
from pycs.monsters import Troll
from pycs.monsters import VioletFungus
from pycs.monsters import Wraith
from pycs.monsters import Zombie
from pycs.races import Human, Elf, HalfElf, Halfling, HalfOrc

from pycs.characters import Barbarian
from pycs.characters import Cleric
from pycs.characters import Fighter
from pycs.characters import Paladin
from pycs.characters import Ranger
from pycs.characters import Rogue
from pycs.characters import Warlock

from pycs.constant import DamageType

from pycs.arena import Arena

from pycs.gear import Chainmail
from pycs.gear import Greataxe
from pycs.gear import Hide
from pycs.gear import Javelin
from pycs.gear import Leather
from pycs.gear import Light_Crossbow
from pycs.gear import Longbow
from pycs.gear import Longsword
from pycs.gear import Mace
from pycs.gear import Plate
from pycs.gear import Potion_Healing
from pycs.gear import Quarterstaff
from pycs.gear import Shield
from pycs.gear import Shortsword
from pycs.gear import Studded


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
def flaming_weapon(source, target, dmg):
    """Add some extra spice"""
    dmg = int(dice.roll("1d6"))
    target.hit(dmg, DamageType.FIRE, source, False, "Flaming Sword")


##############################################################################
def statistics_report(arena):
    """Dump the hit statistics at the end"""
    # Damage Details
    tbl = PrettyTable()
    tbl.field_names = [
        "Name",
        "Attack",
        "Hits",
        "Misses",
        "Hit %",
        "Damage",
        "Crit %",
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
                ]
            )
    tbl.sortby = "Name"
    tbl.align["Name"] = "l"
    tbl.align["Attack"] = "l"
    print(tbl)

    # Participant details
    tbl = PrettyTable()
    tbl.field_names = ["Name", "HP", "State"]
    for creat in arena.combatants:
        tbl.add_row(
            [
                creat.name,
                f"{creat.hp}/{creat.max_hp}",
                creat.state.title(),
            ]
        )
    tbl.sortby = "Name"
    tbl.align["Name"] = "l"
    print(tbl)


##############################################################################
def participant_report(arena):
    """Report on participants"""
    sides = defaultdict(list)
    for part in arena.combatants:
        sides[part.side].append(part)
    for side in sides:
        output = []
        for creat in sides[side]:
            if creat.is_alive():
                output.append(colors.green(creat))
            else:
                output.append(colors.red(creat))
        print(f"{side}: {', '.join(output)}")


##############################################################################
def combat_test():
    """Run through a combat"""
    turn = 0
    print("#" * 80)
    arena = Arena(max_x=45, max_y=25)

    # Dragon Army
    arena.add_combatant(
        AdultGoldDragon(arena=arena, name="Adult Gold Dragon", side="Dragon")
    )
    for i in range(3):
        arena.add_combatant(Kobold(arena=arena, name=f"Kobold{i}", side="Dragon"))

    # Undead Army
    arena.add_combatant(Ghast(arena=arena, name="Ghast", side="Undead"))
    arena.add_combatant(Ghoul(arena=arena, name="Ghoul", side="Undead"))
    for i in range(9):
        arena.add_combatant(Skeleton(arena=arena, name=f"Skeleton{i}", side="Undead"))
    arena.add_combatant(Wraith(arena=arena, name="Wraith", side="Undead"))
    arena.add_combatant(Zombie(arena=arena, name="Zombie", side="Undead"))

    # Monsters
    arena.add_combatant(BarbedDevil(arena=arena, name="Barbed Devil", side="Monsters"))
    arena.add_combatant(GiantFrog(arena=arena, name="Giant Frog", side="Monsters"))
    arena.add_combatant(VioletFungus(arena=arena, name="Violet", side="Monsters"))
    arena.add_combatant(Troll(arena=arena, name="Troll", side="Monsters"))
    for i in range(4):
        arena.add_combatant(Orc(arena=arena, name=f"Orc{i}", side="Monsters"))
    for i in range(4):
        arena.add_combatant(Goblin(arena=arena, name=f"Goblin{i}", side="Monsters"))
    for i in range(4):
        arena.add_combatant(
            Hobgoblin(arena=arena, name=f"Hobgoblin{i}", side="Monsters")
        )

    # Murder Hobos
    arena.add_combatant(
        Barbarian(
            arena=arena,
            name="Barbara",
            level=5,
            side="Humans",
            race=Elf,
            gear=[
                Greataxe(magic_bonus=1),
                Javelin(ammo=2),
                Hide(magic_bonus=2),
                Potion_Healing(ammo=1),
            ],
        )
    )
    arena.add_combatant(
        Cleric(
            arena=arena,
            name="Charlise",
            level=5,
            side="Humans",
            gear=[
                Shield(magic_bonus=1),
                Chainmail(magic_bonus=1),
                Potion_Healing(ammo=1),
                Mace(magic_bonus=1, side_effect=flaming_weapon),
                Light_Crossbow(),
            ],
        )
    )
    arena.add_combatant(
        Fighter(
            arena=arena,
            name="Frank",
            level=5,
            side="Humans",
            race=Human,
            gear=[
                Longsword(magic_bonus=2),
                Potion_Healing(ammo=1),
                Plate(magic_bonus=1),
                Shield(magic_bonus=1),
            ],
        )
    )
    arena.add_combatant(
        Paladin(
            arena=arena,
            name="Patty",
            level=5,
            side="Humans",
            race=HalfOrc,
            gear=[
                Chainmail(magic_bonus=1),
                Shield(magic_bonus=1),
                Potion_Healing(ammo=1),
                Longsword(magic_bonus=2, side_effect=flaming_weapon),
                Javelin(ammo=3),
            ],
        )
    )
    arena.add_combatant(
        Ranger(
            arena=arena,
            name="Renee",
            level=5,
            side="Humans",
            race=Halfling,
            gear=[
                Shortsword(),
                Potion_Healing(ammo=1),
                Longbow(magic_bonus=3),
                Leather(),
            ],
        )
    )
    arena.add_combatant(
        Rogue(
            arena=arena,
            name="Rowena",
            level=5,
            side="Humans",
            race=Elf,
            gear=[
                Shortsword(magic_bonus=1),
                Potion_Healing(ammo=2),
                Longbow(),
                Leather(magic_bonus=1),
            ],
        )
    )
    arena.add_combatant(
        Warlock(
            arena=arena,
            name="Wendy",
            level=5,
            side="Humans",
            race=HalfElf,
            gear=[
                Studded(magic_bonus=1),
                Light_Crossbow(),
                Quarterstaff(),
                Potion_Healing(ammo=2),
            ],
        )
    )

    arena.do_initiative()
    print(f"{arena}")
    while arena.still_going():
        print(f"##### Turn {turn}")
        participant_report(arena)
        arena.turn()
        turn += 1
        assert turn < 100
    statistics_report(arena)

    return arena.winning_side()


# EOF
