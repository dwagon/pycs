""" Creature Statistics"""
from typing import Any, Iterator, List, Self

from pycs.creature import Creature

##############################################################################
##############################################################################
##############################################################################
class Statistics:
    """Creature Statistics"""

    def __init__(self) -> None:
        self._data: List = []

    def add(self, **kwargs: Any) -> None:
        """Add damage to the creature stats"""
        vals = {
            "hit": kwargs.get("hit", False),
            "atkname": kwargs.get("atkname", ""),
            "critical": kwargs.get("critical", False),
            "damage": kwargs.get("dmg", 0),
        }
        target = kwargs.get("target")
        if target:
            vals["targettype"] = target.__class__.__name__
            vals["target"] = target.name
        source = kwargs.get("source")
        if source:
            vals["sourcetype"] = source.__class__.__name__
            vals["source"] = source.name

        self._data.append(vals)

    ##########################################################################
    def _creature_source(self, creature: Creature) -> Iterator[dict]:
        """Dump the stats for a specific creature"""
        for stat in self._data:
            if stat["source"] == creature.name and stat["sourcetype"] == creature.__class__.__name__:
                yield (stat)

    ##########################################################################
    def _type_source(self, creaturetype: str) -> Iterator[dict]:
        """Dump the stats for a specific creature type"""
        for stat in self._data:
            if stat["sourcetype"] == stat["sourcetype"] == creaturetype:
                yield (stat)

    ##########################################################################
    def _summary(self, iterator: Iterator) -> dict[str, dict]:
        """Generic stats summary"""
        stats: dict[str, dict] = {}
        for stat in iterator:
            atkname = stat["atkname"]
            if atkname not in stats:
                stats[atkname] = {"hits": 0, "misses": 0, "damage": 0, "crits": 0}
            if stat["hit"]:
                stats[atkname]["hits"] += 1
            else:
                stats[atkname]["misses"] += 1
            if stat["critical"]:
                stats[atkname]["crits"] += 1
            if stat["damage"]:
                stats[atkname]["damage"] += int(stat["damage"])
        return stats

    ##########################################################################
    def creature_summary(self, creature: Creature) -> dict:
        """Return a summary for attacks from {creature}"""
        return self._summary(self._creature_source(creature))

    ##########################################################################
    def type_summary(self, type: str) -> dict:
        """Return the stats for all the creatures of {type}"""
        return self._summary(self._type_source(type))

    ##########################################################################
    def all_types(self) -> Iterator[str]:
        """Yield every type of creature in the stats"""
        yielded = set()
        for stat in self._data:
            if stat["sourcetype"] not in yielded:
                yielded.add(stat["sourcetype"])
                yield stat["sourcetype"]

    ##########################################################################
    def __add__(self, other: Self) -> Self:
        self._data.extend(other._data)
        return self


# EOF
