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
from pycs.monsters import Gnoll
from pycs.monsters import GnollPackLord
from pycs.monsters import GnollFangOfYeenoghu
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
from pycs.gear import PotionHealing
from pycs.gear import PotionGreaterHealing
from pycs.gear import PotionSuperiorHealing
from pycs.gear import PotionSupremeHealing
from pycs.gear import Quarterstaff
from pycs.gear import Shield
from pycs.gear import Shortsword
from pycs.gear import Studded


DRAGON_ARMY = False
UNDEAD_ARMY = False
MONSTER_ARMY = False
GNOLL_ARMY = True
HUMAN_ARMY = True


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
    target.hit(dmg, DamageType.FIRE, source, False, "Flaming Weapon")


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
def dragon_army(arena):
    """Dragon and friends"""
    arena.add_combatant(AdultGoldDragon(name="Adult Gold Dragon", side="Dragon"))
    for i in range(9):
        arena.add_combatant(Kobold(name=f"Kobold{i}", side="Dragon"))


##############################################################################
def undead_army(arena):
    """Not a pulse amongst them"""
    for i in range(9):
        arena.add_combatant(Ghast(name=f"Ghast{i}", side="Undead"))
    arena.add_combatant(Ghoul(name="Ghoul", side="Undead"))
    for i in range(9):
        arena.add_combatant(Skeleton(name=f"Skeleton{i}", side="Undead"))
    arena.add_combatant(Wraith(name="Wraith", side="Undead"))
    for i in range(9):
        arena.add_combatant(Zombie(name=f"Zombie{i}", side="Undead"))


##############################################################################
def monster_army(arena):
    """Just a bunch of guys"""
    arena.add_combatant(BarbedDevil(name="Barbed Devil", side="Monsters"))
    arena.add_combatant(GiantFrog(name="Giant Frog", side="Monsters"))
    arena.add_combatant(VioletFungus(name="Violet Fungus", side="Monsters"))
    arena.add_combatant(Troll(name="Troll", side="Monsters"))
    for i in range(4):
        arena.add_combatant(Orc(name=f"Orc{i}", side="Monsters"))
    for i in range(4):
        arena.add_combatant(Goblin(name=f"Goblin{i}", side="Monsters"))
    for i in range(4):
        arena.add_combatant(Hobgoblin(name=f"Hobgoblin{i}", side="Monsters"))


##############################################################################
def gnoll_army(arena):
    """The hunger"""
    for i in range(20):
        arena.add_combatant(Gnoll(name=f"Gnoll{i}", side="Gnoll"))
    for i in range(4):
        arena.add_combatant(GnollPackLord(name=f"GnollPackLord{i}", side="Gnoll"))
    for i in range(1):
        arena.add_combatant(GnollFangOfYeenoghu(name=f"GnollFang{i}", side="Gnoll"))


##############################################################################
def human_army(arena):
    """Murder Hobos"""
    arena.add_combatant(
        Barbarian(
            name="Barbara",
            level=5,
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
            level=5,
            side="Humans",
            gear=[
                Shield(magic_bonus=1),
                Chainmail(magic_bonus=1),
                PotionHealing(ammo=1),
                Mace(magic_bonus=1, side_effect=flaming_weapon),
                Light_Crossbow(),
            ],
        )
    )
    arena.add_combatant(
        Fighter(
            name="Frank",
            level=5,
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
            level=5,
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
            level=5,
            side="Humans",
            race=Halfling,
            gear=[
                Shortsword(),
                PotionHealing(ammo=1),
                Longbow(magic_bonus=3),
                Leather(),
            ],
        )
    )
    arena.add_combatant(
        Rogue(
            name="Rowena",
            level=5,
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
            level=5,
            side="Humans",
            race=HalfElf,
            gear=[
                Studded(magic_bonus=1),
                Light_Crossbow(),
                Quarterstaff(),
                PotionHealing(ammo=2),
            ],
        )
    )


##############################################################################
def combat_test():
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
        participant_report(arena)
        arena.turn()
        turn += 1
        assert turn < 100
    print(f"{turn=}")
    statistics_report(arena)

    return arena.winning_side()


# EOF
