import functools
from typing import Dict, Set, List

# EN Locale Creature Name to rough depth in meters found at
all_creatures: Dict[str, int] = {
    "Gasopod": 0,
    "Bladderfish": 0,
    "Ancient Floater": 0,
    "Skyray": 0,
    "Garryfish": 0,
    "Peeper": 0,
    "Shuttlebug": 0,
    "Rabbit Ray": 0,
    "Stalker": 0,
    "Floater": 0,
    "Holefish": 0,
    "Cave Crawler": 0,
    "Hoopfish": 0,
    "Crashfish": 0,
    "Hoverfish": 0,
    "Spadefish": 0,
    "Reefback Leviathan": 0,
    "Reaper Leviathan": 0,
    "Warper": 0,
    "Boomerang": 0,
    "Biter": 200,
    "Sand Shark": 200,
    "Bleeder": 200,
    "Crabsnake": 300,
    "Jellyray": 300,
    "Oculus": 300,
    "Mesmer": 300,
    "Eyeye": 300,
    "Reginald": 400,
    "Sea Treader Leviathan": 400,
    "Crabsquid": 400,
    "Ampeel": 400,
    "Boneshark": 400,
    "Rockgrub": 400,
    "Ghost Leviathan": 500,
    "Ghost Leviathan Juvenile": 500,
    "Spinefish": 600,
    "Blighter": 600,
    "Blood Crawler": 600,
    "Ghostray": 1000,
    "Amoeboid": 1000,
    "River Prowler": 1000,
    "Red Eyeye": 1300,
    "Magmarang": 1300,
    "Crimson Ray": 1300,
    "Lava Larva": 1300,
    "Lava Lizard": 1300,
    "Sea Dragon Leviathan": 1300,
    "Cuddlefish": 300,
    "Sea Emperor Juvenile": 1700,
}

aggressive: Set[str] = {
    "Cave Crawler",  # is very easy without Stasis Rifle, but included for consistency
    "Crashfish",
    "Biter",
    "Bleeder",
    "Blighter",
    "Blood Crawler",
    "Mesmer",
    "Reaper Leviathan",
    "Crabsquid",
    "Warper",
    "Crabsnake",
    "Ampeel",
    "Stalker",
    "Sand Shark",
    "Boneshark",
    "Lava Lizard",
    "Sea Dragon Leviathan",
    "River Prowler",
    "Ghost Leviathan Juvenile",
    "Ghost Leviathan"
}

containment: Set[str] = {  # creatures that have to be raised from eggs
    "Cuddlefish",
}

hatchable: Set[str] = {  # aggressive creatures that can be grown from eggs as alternative to stasis
    "Ampeel",  # warning: electric shocks
    "Crabsquid",  # warning: electric shocks
    "Crabsnake",
    "Boneshark",
    "Crashfish",
    "Gasopod",
    "Lava Lizard",
    "Mesmer",
    "Sand Shark",
    "Stalker",
}

suffix: str = " Scan"

creature_locations: Dict[str, int] = {
    creature + suffix: creature_id for creature_id, creature in enumerate(all_creatures, start=34000)
}


class Definitions:
    """Only compute lists if needed and then cache them."""

    @functools.cached_property
    def all_creatures_presorted(self) -> List[str]:
        return sorted(all_creatures)

    @functools.cached_property
    def all_creatures_presorted_without_containment(self) -> List[str]:
        return [name for name in self.all_creatures_presorted if name not in containment]

    @functools.cached_property
    def all_creatures_presorted_without_stasis(self) -> List[str]:
        return [name for name in self.all_creatures_presorted if name not in aggressive or name in hatchable]

    @functools.cached_property
    def all_creatures_presorted_without_aggressive_and_containment(self) -> List[str]:
        return [name for name in self.all_creatures_presorted if name not in aggressive and name not in containment]

# only singleton needed
Definitions: Definitions = Definitions()
