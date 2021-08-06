"""Main module."""
from monster.goblin import Goblin
from character.fighter import Fighter
from arena import Arena


##############################################################################
def start():
    """Main point"""
    arena = Arena(x=20, y=20)
    goblin = Goblin(hp=5)
    fighter = Fighter(hp=2)
    arena.add_combatant(goblin, (0, 0), side='A')
    arena.add_combatant(fighter, (19, 19), side='B')
    while arena.still_going():
        goblin.turn()
        fighter.turn()
        print(f"{arena}")
        print(f"{goblin=}")
        print(f"{fighter=}")

# EOF
