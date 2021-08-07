"""Main module."""
from monster.goblin import Goblin
from character.fighter import Fighter
from arena import Arena


##############################################################################
def start():
    """Main point"""
    arena = Arena(x=10, y=10)
    goblin = Goblin(arena=arena, side='A')
    fighter = Fighter(arena=arena, hp=2, side='B')
    arena.add_combatant(goblin, (0, 0))
    arena.add_combatant(fighter, (9, 9))
    print(f"{arena}")
    while arena.still_going():
        goblin.turn()
        fighter.turn()
        print(f"{arena}")

# EOF
