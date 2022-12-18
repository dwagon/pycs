""" All the effects on a creature"""
from typing import Any, TYPE_CHECKING
from pycs.effect import Effect
from pycs.constant import Stat
from pycs.damage import Damage
from pycs.action import Action


if TYPE_CHECKING:
    from pycs.creature import Creature
    from pycs.damageroll import DamageRoll


##############################################################################
##############################################################################
##############################################################################
class Effects:
    def __init__(self, owner: "Creature"):
        self._owner = owner
        self._effects: dict[str, Effect] = {}

    ##########################################################################
    def __str__(self) -> str:
        output = []
        for _, eff in self._effects.items():
            output.append(eff.name)
        return ", ".join(output)

    ##########################################################################
    def add_effect(self, source: "Creature", effect: Effect) -> None:
        """ Add an effect """
        self._effects[effect.name] = effect
        print(f"{effect.name} added to {self._owner}")
        effect.initial(self._owner)

    ##########################################################################
    def remove_effect(self, effect: Effect|str) -> None:
        """ Add an effect """
        if isinstance(effect, str):
            effect = self._effects[effect]
        self._effects[effect.name].finish(self._owner)
        print(f"{effect.name} removed from {self._owner}")
        del self._effects[effect.name]

    ##########################################################################
    def remove_all_effects(self) -> None:
        for _, eff in self._effects.copy().items():
            self.remove_effect(eff)

    ##########################################################################
    def __getitem__(self, __name: str) -> Effect:
        return self._effects[__name]

    ##########################################################################
    def has_effect(self, name: str) -> bool:
        return name in self._effects

    ##########################################################################
    def hook_ac_modifier(self) -> int:
        """ Modification of AC"""
        tmp = 0
        for _, eff in self._effects.items():
            mod = eff.hook_ac_modifier()
            tmp += mod
        return tmp

    ##########################################################################
    def hook_saving_throw(self, stat: Stat, **kwargs: Any) -> dict[str, int]:
        result = {}
        for _, eff in self._effects.items():
            result.update(eff.hook_saving_throw(stat, **kwargs))
        return result

    ##########################################################################
    def hook_fallen_unconscious(self, dmg: Damage, critical: bool) -> bool:
        for _, eff in self._effects.items():
            if eff.hook_fallen_unconscious(dmg, critical):
                return False
        return True

    ##########################################################################
    def hook_being_hit(self, dmg: Damage) -> Damage:
        for _, eff in self._effects.items():
            dmg = eff.hook_being_hit(dmg)
        return dmg

    ##########################################################################
    def hook_gives_advantage_against(self) -> bool:
        """Gives advantage against creature who has effect"""
        for _, eff in self._effects.items():
            if eff.hook_gives_advantage_against():
                return True
        return False

    ##########################################################################
    def hook_gives_disadvantage_against(self) -> bool:
        """Gives disadvantage against creature who has effect"""
        for _, eff in self._effects.items():
            if eff.hook_gives_disadvantage_against():
                return True
        return False

    ##########################################################################
    def hook_gives_advantage(self, target: "Creature") -> bool:
        """Gives advantage for creature doing the attack"""
        for _, eff in self._effects.items():
            if eff.hook_gives_advantage(target):
                return True
        return False
    
    ##########################################################################
    def hook_gives_disadvantage(self, target: "Creature") -> bool:
        """Gives disadvantage for creature doing the attack"""
        for _, eff in self._effects.items():
            if eff.hook_gives_disadvantage(target):
                return True
        return False

    ##########################################################################
    def hook_heuristic_mod(self, action: Action, actor: "Creature") -> int:
        """Modification to the actions {action} heuristic"""
        tmp = 0
        for _, eff in self._effects.items():
            mod = eff.hook_heuristic_mod(action, actor)
            tmp += mod
        return tmp

   ##########################################################################
    def removal_after_being_attacked(self) -> None:
        """Do we remove the effect after being turned"""
        for _, eff in self._effects.copy().items():
            if eff.removal_after_being_attacked():
                self.remove_effect(eff)

    ##########################################################################
    def hook_source_additional_damage(self, attack: Action, source: "Creature", target: "Creature") -> None:
        """Addition damage from melee weapons based on the owner of the effect"""
        for atkname, eff in self._effects.items():
            o_dmgroll: DamageRoll = eff.hook_source_additional_damage(attack, self._owner, target)
            dmg = o_dmgroll.roll()
            if dmg:
                target.hit(dmg, self._owner, critical=False, atkname=atkname)

    ##########################################################################
    def hook_target_additional_damage(self, attack: Action, source: "Creature", target: "Creature") -> None:
        """Addition damage from melee weapons based on the owner of the effect"""
        for atkname, eff in self._effects.items():
            t_dmgroll: DamageRoll = eff.hook_target_additional_damage(attack, self._owner, target)
            dmg = t_dmgroll.roll()
            if dmg:
                target.hit(dmg, self._owner, critical=False, atkname=atkname)

    ##########################################################################
    def hook_attack_to_hit(self, target: "Creature", range: int, action: Action) -> tuple[int, list[str]]:
        """Modify the roll to hit on attacks"""
        msg : list[str]= []
        to_hit: int = 0
        for name, eff in self._effects.items():
            mod = eff.hook_attack_to_hit(target=target, range=range, action=action)
            if mod:
                to_hit += mod
                msg.append(f"+{mod} from {name}")
        return to_hit, msg

    ##########################################################################
    def hook_start_turn(self) -> None:
        """We start the turn with an effect"""
        for _, eff in self._effects.items():
            eff.hook_start_turn()

    ##########################################################################
    def removal_end_of_its_turn(self, victim: "Creature") -> None:
        """Do we remove this effect and the end of the victims turn"""
        for _, eff in self._effects.copy().items():
            if eff.removal_end_of_its_turn(victim):
                self.remove_effect(eff)

    ##########################################################################
    def hook_start_in_range(self, creat: "Creature") -> None:
        """Did we start our turn in range of any effect"""
        for _, eff in self._effects.items():
            eff.hook_start_in_range(creat)

    ##########################################################################
    def hook_d20(self, val: int, reason: str) -> int:
        """We have rolled {val} on a d20 for {reason}"""
        newval = val
        for _, eff in self._effects.items():
            newval = eff.hook_d20(newval, reason)
        return newval

# EOF