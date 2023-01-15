"""Top-level package for pycs."""

__author__ = """Dougal Scott"""
__email__ = "dougal.scott@gmail.com"

from collections import defaultdict
from prettytable import PrettyTable
import colors

from pycs.creature import Creature
from pycs.statistics import Statistics
from pycs.damage import Damage
from pycs.damageroll import DamageRoll
from pycs.monsters import AdultGoldDragon, YoungWhiteDragon
from pycs.monsters import Allosaurus, Ankylosaurus, Triceratops
from pycs.monsters import BarbedDevil
from pycs.monsters import (
    Ghast,
    Ghoul,
    MinotaurSkeleton,
    OgreZombie,
    Skeleton,
    VampireSpawn,
    Wraith,
    Zombie,
)

# from pycs.monsters import GiantFrog
from pycs.monsters import (
    Gnoll,
    GnollPackLord,
    GnollFangOfYeenoghu,
    GnollWitherling,
    GnollHunter,
)
from pycs.monsters import Goblin
from pycs.monsters import Hobgoblin
from pycs.monsters import Kobold
from pycs.monsters import Orc
from pycs.monsters import Troll
from pycs.monsters import VioletFungus
from pycs.monsters import Yeti
from pycs.races import Human, Elf, HalfElf, Halfling, HalfOrc

from pycs.characters import Barbarian, Cleric, Fighter, Paladin, Ranger, Rogue, Warlock

from pycs.constant import DamageType

from pycs.arena import Arena

from pycs.gear import Chainmail, Hide, Leather, Plate, Shield, Studded
from pycs.gear import Greataxe, Longsword, Mace, Quarterstaff, Shortsword
from pycs.gear import Javelin, LightCrossbow, Longbow
from pycs.gear import (
    PotionHealing,
    PotionGreaterHealing,
    PotionSuperiorHealing,
    PotionSupremeHealing,
)


DRAGON_ARMY = False
UNDEAD_ARMY = False
MONSTER_ARMY = False
GNOLL_ARMY = True
HUMAN_ARMY = True


##############################################################################
def start(rounds: int) -> None:
    """Main"""
    winning_stats: defaultdict[str, int] = defaultdict(int)
    all_stats = Statistics()
    for _ in range(rounds):
        winner, stats = combat_test()
        winning_stats[winner] += 1
        all_stats += stats
    print_overall_stats(all_stats)
    win_report(winning_stats, rounds)


##############################################################################
def print_overall_stats(stats: Statistics) -> None:
    """Do a dump of the global stats"""
    print("Overall Stats")
    tbl = PrettyTable()
    tbl.field_names = [
        "Name",
        "Attack",
        "Hits",
        "Misses",
        "Damage",
        "Damage/Attack"
    ]
    for typ_ in stats.all_types():
        for atk, details in stats.type_summary(typ_).items():
            dpa = details["damage"] / (details["hits"] + details["misses"])
            tbl.add_row([typ_, atk, details["hits"], details["misses"], details["damage"], dpa])
    tbl.sortby = "Damage/Attack"
    tbl.align["Name"] = "l"
    tbl.align["Attack"] = "l"
    tbl.float_format=".2"
    print(tbl)


##############################################################################
def win_report(stats: dict[str, int], rounds: int) -> None:
    """Who is winning"""
    print("\nWinning stats")
    tbl = PrettyTable()
    tbl.field_names = ["Side", "Win Count", "Percentage"]
    for side, wins in stats.items():
        tbl.add_row([side, wins, 100.0 * wins / rounds])

    print(tbl)


##############################################################################
def flaming_weapon(source: Creature, target: Creature, dmg: Damage) -> None:
    """Add some extra spice"""
    dmg = DamageRoll("1d6", 0, DamageType.FIRE).roll()
    target.hit(dmg, source, False, "Flaming Weapon")


##############################################################################
def damage_report(arena: Arena) -> None:
    """ Report on the damage inflicted by participants """
    tbl = PrettyTable()
    tbl.field_names = [
        "Name",
        "Attack",
        "Hits",
        "Misses",
        "Hit %",
        "Damage",
        "Criticals",
        "Crit %",
    ]
    for creat in arena.pick_everyone():
        stats = arena.statistics.creature_summary(creat)
        for atk, stat in stats.items():
            try:
                crit_p = int(100.0 * stat["crits"]  / stat["hits"])
            except ZeroDivisionError:
                crit_p = 0
            try:
                hit_p = int(100.0 * stat["hits"] / (stat["hits"]+ stat["misses"]))
            except ZeroDivisionError:
                hit_p = 0
            tbl.add_row([creat.name, atk, stat["hits"], stat["misses"], hit_p, stat["damage"], stat["crits"], crit_p])
    
    tbl.sortby = "Damage"
    tbl.align["Name"] = "l"
    tbl.align["Attack"] = "l"
    print(tbl)


##############################################################################
def statistics_report(arena: Arena) -> None:
    """Dump the hit statistics at the end"""
    damage_report(arena)
    participant_report(arena)

##############################################################################
def participant_report(arena: Arena) -> None:
    """ Participant details """
    tbl = PrettyTable()
    tbl.field_names = ["Name", "HP", "State"]
    for creat in arena.pick_everyone():
        tbl.add_row(
            [
                creat.name,
                f"{creat.hp}/{creat.max_hp}",
                ", ".join([_.name.title() for _ in creat.conditions]),
            ]
        )
    tbl.sortby = "Name"
    tbl.align["Name"] = "l"
    print(tbl)


##############################################################################
def participant_state(arena: Arena) -> None:
    """Report on participants"""
    sides = defaultdict(list)
    for part in arena.pick_everyone():
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
def dragon_army(arena: Arena) -> None:
    """Dragon and friends"""
    arena.add_combatant(AdultGoldDragon(name="Adult Gold Dragon", side="Dragon"))
    for i in range(9):
        arena.add_combatant(Kobold(name=f"Kobold{i}", side="Dragon"))
    arena.add_combatant(YoungWhiteDragon(name="Young White Dragon", side="Monsters"))


##############################################################################
def undead_army(arena: Arena) -> None:
    """Not a pulse amongst them"""
    for i in range(3):
        arena.add_combatant(Ghast(name=f"Ghast{i}", side="Undead"))
    arena.add_combatant(Ghoul(name="Ghoul", side="Undead"))
    for i in range(14):
        arena.add_combatant(Skeleton(name=f"Skeleton{i}", side="Undead"))
    arena.add_combatant(Wraith(name="Wraith", side="Undead"))
    for i in range(14):
        arena.add_combatant(Zombie(name=f"Zombie{i}", side="Undead"))
    for i in range(5):
        arena.add_combatant(OgreZombie(name=f"OgreZombie{i}", side="Undead"))
    arena.add_combatant(VampireSpawn(name="VampireSpawn", side="Undead"))
    for i in range(5):
        arena.add_combatant(MinotaurSkeleton(name=f"MinotaurSkeleton{i}", side="Undead"))


##############################################################################
def monster_army(arena: Arena) -> None:
    """Just a bunch of guys"""
    arena.add_combatant(BarbedDevil(name="Barbed Devil", side="Monsters"))
    # for i in range(4):
    #    arena.add_combatant(GiantFrog(name=f"Giant Frog{i}", side="Monsters"))
    arena.add_combatant(VioletFungus(name="Violet Fungus", side="Monsters"))
    arena.add_combatant(Troll(name="Troll", side="Monsters"))
    for i in range(4):
        arena.add_combatant(Orc(name=f"Orc{i}", side="Monsters"))
    for i in range(4):
        arena.add_combatant(Goblin(name=f"Goblin{i}", side="Monsters"))
    for i in range(4):
        arena.add_combatant(Hobgoblin(name=f"Hobgoblin{i}", side="Monsters"))
    arena.add_combatant(Allosaurus(name="Allosaurus", side="Monsters"))
    arena.add_combatant(Ankylosaurus(name="Ankylosaurus", side="Monsters"))
    arena.add_combatant(Triceratops(name="Triceratops", side="Monsters"))
    arena.add_combatant(Yeti(name="Yeti", side="Monsters"))


##############################################################################
def gnoll_army(arena: Arena) -> None:
    """The hunger"""
    for i in range(8):
        arena.add_combatant(Gnoll(name=f"Gnoll{i}", side="Gnoll"))
    for i in range(1):
        arena.add_combatant(GnollHunter(name=f"GnollHunter{i}", side="Gnoll"))
    for i in range(1):
        arena.add_combatant(GnollPackLord(name=f"GnollPackLord{i}", side="Gnoll"))
    for i in range(1):
        arena.add_combatant(GnollFangOfYeenoghu(name=f"GnollFang{i}", side="Gnoll"))
    for i in range(5):
        arena.add_combatant(GnollWitherling(name=f"GnollWitherling{i}", side="Gnoll"))


##############################################################################
def human_army(arena: Arena) -> None:
    """Murder Hobos"""
    arena.add_combatant(
        Barbarian(
            name="Barbara",
            level=3,
            side="Humans",
            race=Elf,
            gear=[
                Greataxe(magic_bonus=1),
                Javelin(ammo=2),
                Hide(magic_bonus=2),
                PotionGreaterHealing(ammo=1),
            ],
        )
    )
    arena.add_combatant(
        Cleric(
            name="Charlise",
            level=3,
            side="Humans",
            gear=[
                Shield(magic_bonus=1),
                Chainmail(magic_bonus=1),
                PotionHealing(ammo=1),
                Mace(magic_bonus=1, side_effect=flaming_weapon),
                LightCrossbow(),
            ],
        )
    )
    arena.add_combatant(
        Fighter(
            name="Frank",
            level=3,
            side="Humans",
            race=Human,
            gear=[
                Longsword(magic_bonus=2),
                PotionSuperiorHealing(ammo=1),
                Plate(magic_bonus=1),
                Shield(magic_bonus=1),
            ],
        )
    )
    arena.add_combatant(
        Paladin(
            name="Patty",
            level=3,
            side="Humans",
            race=HalfOrc,
            gear=[
                Chainmail(magic_bonus=1),
                Shield(magic_bonus=1),
                PotionHealing(ammo=1),
                Longsword(magic_bonus=2, side_effect=flaming_weapon),
                Javelin(ammo=3),
            ],
        )
    )
    arena.add_combatant(
        Ranger(
            name="Renee",
            level=3,
            side="Humans",
            race=Halfling,
            gear=[
                Shortsword(),
                PotionHealing(ammo=1),
                Longbow(magic_bonus=2),
                Leather(magic_bonus=1),
            ],
        )
    )
    arena.add_combatant(
        Rogue(
            name="Rowena",
            level=3,
            side="Humans",
            race=Elf,
            gear=[
                Shortsword(magic_bonus=1),
                PotionSupremeHealing(ammo=2),
                Longbow(),
                Leather(magic_bonus=1),
            ],
        )
    )
    arena.add_combatant(
        Warlock(
            name="Wendy",
            level=3,
            side="Humans",
            race=HalfElf,
            gear=[
                Studded(magic_bonus=1),
                LightCrossbow(),
                Quarterstaff(),
                PotionHealing(ammo=2),
            ],
        )
    )


##############################################################################
def combat_test() -> tuple[str, Statistics]:
    """Run through a combat"""
    turn = 0
    print("#" * 80)
    arena = Arena(max_x=45, max_y=25)

    if DRAGON_ARMY:
        dragon_army(arena)

    if UNDEAD_ARMY:
        undead_army(arena)

    if MONSTER_ARMY:
        monster_army(arena)

    if GNOLL_ARMY:
        gnoll_army(arena)

    if HUMAN_ARMY:
        human_army(arena)

    arena.do_initiative()
    print(f"{arena}")
    while arena.still_going():
        print(f"##### Turn {turn}")
        participant_state(arena)
        arena.turn()
        turn += 1
        assert turn < 100
    print(f"{turn=}")
    statistics_report(arena)
    return arena.winning_side(), arena.statistics


# EOF
