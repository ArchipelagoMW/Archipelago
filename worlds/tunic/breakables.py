from typing import TYPE_CHECKING, NamedTuple

from enum import IntEnum
from BaseClasses import CollectionState, Region
from worlds.generic.Rules import set_rule
from .rules import has_sword, has_melee
from .er_rules import can_shop
if TYPE_CHECKING:
    from . import TunicWorld


# just getting an id that is a decent chunk ahead of the grass ones
breakable_base_id = 509342400 + 8000


class BreakableType(IntEnum):
    pot = 1
    fire_pot = 2
    explosive_pot = 3
    sign = 4
    barrel = 5
    crate = 6
    table = 7
    glass = 8
    leaves = 9
    wall = 10


class TunicLocationData(NamedTuple):
    er_region: str
    breakable: BreakableType


breakable_location_table: dict[str, TunicLocationData] = {
    "Overworld - [Northwest] Sign by Quarry Gate": TunicLocationData("Overworld", BreakableType.sign),
    "Overworld - [Central] Sign South of Checkpoint": TunicLocationData("Overworld", BreakableType.sign),
    "Overworld - [Central] Sign by Ruined Passage": TunicLocationData("Overworld", BreakableType.sign),
    "Overworld - [East] Pot near Slimes 1": TunicLocationData("East Overworld", BreakableType.pot),
    "Overworld - [East] Pot near Slimes 2": TunicLocationData("East Overworld", BreakableType.pot),
    "Overworld - [East] Pot near Slimes 3": TunicLocationData("East Overworld", BreakableType.pot),
    "Overworld - [East] Pot near Slimes 4": TunicLocationData("East Overworld", BreakableType.pot),
    "Overworld - [East] Pot near Slimes 5": TunicLocationData("East Overworld", BreakableType.pot),
    "Overworld - [East] Forest Sign": TunicLocationData("East Overworld", BreakableType.sign),
    "Overworld - [East] Fortress Sign": TunicLocationData("East Overworld", BreakableType.sign),
    "Overworld - [North] Pot 1": TunicLocationData("Upper Overworld", BreakableType.pot),
    "Overworld - [North] Pot 2": TunicLocationData("Upper Overworld", BreakableType.pot),
    "Overworld - [North] Pot 3": TunicLocationData("Upper Overworld", BreakableType.pot),
    "Overworld - [North] Pot 4": TunicLocationData("Upper Overworld", BreakableType.pot),
    "Overworld - [West] Sign Near West Garden Entrance": TunicLocationData("Overworld to West Garden from Furnace", BreakableType.sign),
    "Stick House - Pot 1": TunicLocationData("Stick House", BreakableType.pot),
    "Stick House - Pot 2": TunicLocationData("Stick House", BreakableType.pot),
    "Stick House - Pot 3": TunicLocationData("Stick House", BreakableType.pot),
    "Stick House - Pot 4": TunicLocationData("Stick House", BreakableType.pot),
    "Stick House - Pot 5": TunicLocationData("Stick House", BreakableType.pot),
    "Stick House - Pot 6": TunicLocationData("Stick House", BreakableType.pot),
    "Stick House - Pot 7": TunicLocationData("Stick House", BreakableType.pot),
    "Ruined Shop - Pot 1": TunicLocationData("Ruined Shop", BreakableType.pot),
    "Ruined Shop - Pot 2": TunicLocationData("Ruined Shop", BreakableType.pot),
    "Ruined Shop - Pot 3": TunicLocationData("Ruined Shop", BreakableType.pot),
    "Ruined Shop - Pot 4": TunicLocationData("Ruined Shop", BreakableType.pot),
    "Ruined Shop - Pot 5": TunicLocationData("Ruined Shop", BreakableType.pot),
    "Hourglass Cave - Sign": TunicLocationData("Hourglass Cave", BreakableType.sign),
    "Forest Belltower - Pot by Slimes 1": TunicLocationData("Forest Belltower Main", BreakableType.pot),
    "Forest Belltower - Pot by Slimes 2": TunicLocationData("Forest Belltower Main", BreakableType.pot),
    "Forest Belltower - Pot by Slimes 3": TunicLocationData("Forest Belltower Main", BreakableType.pot),
    "Forest Belltower - Pot by Slimes 4": TunicLocationData("Forest Belltower Main", BreakableType.pot),
    "Forest Belltower - Pot by Slimes 5": TunicLocationData("Forest Belltower Main", BreakableType.pot),
    "Forest Belltower - Pot by Slimes 6": TunicLocationData("Forest Belltower Main", BreakableType.pot),
    "Forest Belltower - [Upper] Barrel 1": TunicLocationData("Forest Belltower Upper", BreakableType.barrel),
    "Forest Belltower - [Upper] Barrel 2": TunicLocationData("Forest Belltower Upper", BreakableType.barrel),
    "Forest Belltower - [Upper] Barrel 3": TunicLocationData("Forest Belltower Upper", BreakableType.barrel),
    "Forest Belltower - Pot after Guard Captain 1": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower - Pot after Guard Captain 2": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower - Pot after Guard Captain 3": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower - Pot after Guard Captain 4": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower - Pot after Guard Captain 5": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower - Pot after Guard Captain 6": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower - Pot after Guard Captain 7": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower - Pot after Guard Captain 8": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower - Pot after Guard Captain 9": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Guardhouse 1 - Pot 1": TunicLocationData("Guard House 1 East", BreakableType.pot),
    "Guardhouse 1 - Pot 2": TunicLocationData("Guard House 1 East", BreakableType.pot),
    "Guardhouse 1 - Pot 3": TunicLocationData("Guard House 1 East", BreakableType.pot),
    "Guardhouse 1 - Pot 4": TunicLocationData("Guard House 1 East", BreakableType.pot),
    "Guardhouse 1 - Pot 5": TunicLocationData("Guard House 1 East", BreakableType.pot),
    "East Forest - Sign by Grave Path": TunicLocationData("East Forest", BreakableType.sign),
    "East Forest - Sign by Guardhouse 1": TunicLocationData("East Forest", BreakableType.sign),
    "East Forest - Pot by Grave Path 1": TunicLocationData("East Forest", BreakableType.pot),
    "East Forest - Pot by Grave Path 2": TunicLocationData("East Forest", BreakableType.pot),
    "East Forest - Pot by Grave Path 3": TunicLocationData("East Forest", BreakableType.pot),
    "East Forest - Pot by Envoy 1": TunicLocationData("East Forest", BreakableType.pot),
    "East Forest - Pot by Envoy 2": TunicLocationData("East Forest", BreakableType.pot),
    "East Forest - Pot by Envoy 3": TunicLocationData("East Forest", BreakableType.pot),
    "Guardhouse 2 - Bottom Floor Pot 1": TunicLocationData("Guard House 2 Lower", BreakableType.pot),
    "Guardhouse 2 - Bottom Floor Pot 2": TunicLocationData("Guard House 2 Lower", BreakableType.pot),
    "Guardhouse 2 - Bottom Floor Pot 3": TunicLocationData("Guard House 2 Lower", BreakableType.pot),
    "Guardhouse 2 - Bottom Floor Pot 4": TunicLocationData("Guard House 2 Lower", BreakableType.pot),
    "Guardhouse 2 - Bottom Floor Pot 5": TunicLocationData("Guard House 2 Lower", BreakableType.pot),
    "Beneath the Well - [Side Room] Pot by Chest 1": TunicLocationData("Beneath the Well Back", BreakableType.pot),
    "Beneath the Well - [Side Room] Pot by Chest 2": TunicLocationData("Beneath the Well Back", BreakableType.pot),
    "Beneath the Well - [Side Room] Pot by Chest 3": TunicLocationData("Beneath the Well Back", BreakableType.pot),
    "Beneath the Well - [Third Room] Barrel by Bridge 1": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well - [Third Room] Barrel by Bridge 2": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well - [Third Room] Barrel by Bridge 3": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well - [Third Room] Barrel after Back Corridor 1": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well - [Third Room] Barrel after Back Corridor 2": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well - [Third Room] Barrel after Back Corridor 3": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well - [Third Room] Barrel after Back Corridor 4": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well - [Third Room] Barrel after Back Corridor 5": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well - [Third Room] Barrel by West Turret 1": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well - [Third Room] Barrel by West Turret 2": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well - [Third Room] Barrel by West Turret 3": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well - [Third Room] Pot by East Turret 1": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Beneath the Well - [Third Room] Pot by East Turret 2": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Beneath the Well - [Third Room] Pot by East Turret 3": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Beneath the Well - [Third Room] Pot by East Turret 4": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Beneath the Well - [Third Room] Pot by East Turret 5": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Beneath the Well - [Third Room] Pot by East Turret 6": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Beneath the Well - [Third Room] Pot by East Turret 7": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Well Boss - Barrel 1": TunicLocationData("Well Boss", BreakableType.barrel),
    "Well Boss - Barrel 2": TunicLocationData("Well Boss", BreakableType.barrel),
    "Dark Tomb - Pot Hallway Pot 1": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - Pot Hallway Pot 2": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - Pot Hallway Pot 3": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - Pot Hallway Pot 4": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - Pot Hallway Pot 5": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - Pot Hallway Pot 6": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - Pot Hallway Pot 7": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - Pot Hallway Pot 8": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - Pot Hallway Pot 9": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - Pot Hallway Pot 10": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - Pot Hallway Pot 11": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - Pot Hallway Pot 12": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - Pot Hallway Pot 13": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - Pot Hallway Pot 14": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - 2nd Laser Room Pot 1": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - 2nd Laser Room Pot 2": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - 2nd Laser Room Pot 3": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - 2nd Laser Room Pot 4": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb - 2nd Laser Room Pot 5": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "West Garden House - Pot 1": TunicLocationData("Magic Dagger House", BreakableType.pot),
    "West Garden House - Pot 2": TunicLocationData("Magic Dagger House", BreakableType.pot),
    "West Garden House - Pot 3": TunicLocationData("Magic Dagger House", BreakableType.pot),
    "Fortress Courtyard - Fire Pot 1": TunicLocationData("Fortress Courtyard westmost pots", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 2": TunicLocationData("Fortress Courtyard westmost pots", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 3": TunicLocationData("Fortress Courtyard west pots", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 4": TunicLocationData("Fortress Courtyard west pots", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 5": TunicLocationData("Fortress Courtyard", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 6": TunicLocationData("Fortress Courtyard", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 7": TunicLocationData("Fortress Courtyard", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 8": TunicLocationData("Fortress Courtyard", BreakableType.fire_pot),
    "Fortress Courtyard - Upper Fire Pot": TunicLocationData("Fortress Courtyard Upper pot", BreakableType.fire_pot),
    "Fortress Grave Path - [Entry] Pot 1": TunicLocationData("Fortress Grave Path Entry", BreakableType.pot),
    "Fortress Grave Path - [Entry] Pot 2": TunicLocationData("Fortress Grave Path Entry", BreakableType.pot),
    "Fortress Grave Path - [By Grave] Pot 1": TunicLocationData("Fortress Grave Path pots", BreakableType.pot),
    "Fortress Grave Path - [By Grave] Pot 2": TunicLocationData("Fortress Grave Path pots", BreakableType.pot),
    "Fortress Grave Path - [By Grave] Pot 3": TunicLocationData("Fortress Grave Path pots", BreakableType.pot),
    "Fortress Grave Path - [By Grave] Pot 4": TunicLocationData("Fortress Grave Path pots", BreakableType.pot),
    "Fortress Grave Path - [By Grave] Pot 5": TunicLocationData("Fortress Grave Path pots", BreakableType.pot),
    "Fortress Grave Path - [By Grave] Pot 6": TunicLocationData("Fortress Grave Path pots", BreakableType.pot),
    "Fortress Grave Path - [Central] Fire Pot 1": TunicLocationData("Fortress Grave Path westmost pot", BreakableType.fire_pot),
    "Fortress Grave Path - [Central] Fire Pot 2": TunicLocationData("Fortress Grave Path Combat", BreakableType.fire_pot),
    "Eastern Vault Fortress - [Central] Pot by Door 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [Central] Pot by Door 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [Central] Pot by Door 3": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [Central] Pot by Door 4": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [Central] Pot by Door 5": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [Central] Pot by Door 6": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [Central] Pot by Door 7": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [Central] Pot by Door 8": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [Central] Pot by Door 9": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [Central] Pot by Door 10": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [Central] Pot by Door 11": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [East Wing] Pot by Broken Checkpoint 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [East Wing] Pot by Broken Checkpoint 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [East Wing] Pot by Broken Checkpoint 3": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [West Wing] Pot by Checkpoint 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [West Wing] Pot by Checkpoint 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [West Wing] Pot by Checkpoint 3": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [West Wing] Pot by Overlook 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [West Wing] Pot by Overlook 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [West Wing] Slorm Room Pot 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [West Wing] Slorm Room Pot 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [West Wing] Slorm Room Pot 3": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [West Wing] Chest Room Pot 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [West Wing] Chest Room Pot 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [West Wing] Pot by Stairs to Basement 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [West Wing] Pot by Stairs to Basement 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress - [West Wing] Pot by Stairs to Basement 3": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Beneath the Fortress - Entry Spot Pot 1": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.pot),
    "Beneath the Fortress - Entry Spot Pot 2": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.pot),
    "Beneath the Fortress - Entry Spot Crate 1": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress - Entry Spot Crate 2": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress - Entry Spot Crate 3": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress - Entry Spot Crate 4": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress - Entry Spot Crate 5": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress - Entry Spot Crate 6": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress - Entry Spot Crate 7": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress - Slorm Room Crate 1": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress - Slorm Room Crate 2": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress - Crate under Rope 1": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress - Crate under Rope 2": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress - Crate under Rope 3": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress - Crate under Rope 4": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress - Crate under Rope 5": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress - Crate under Rope 6": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress - Fuse Room Fire Pot 1": TunicLocationData("Beneath the Vault Back", BreakableType.fire_pot),
    "Beneath the Fortress - Fuse Room Fire Pot 2": TunicLocationData("Beneath the Vault Back", BreakableType.fire_pot),
    "Beneath the Fortress - Fuse Room Fire Pot 3": TunicLocationData("Beneath the Vault Back", BreakableType.fire_pot),
    "Beneath the Fortress - Barrel by Back Room 1": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress - Barrel by Back Room 2": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress - Barrel by Back Room 3": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress - Barrel by Back Room 4": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress - Barrel by Back Room 5": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress - Barrel by Back Room 6": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress - Back Room Barrel 1": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress - Back Room Barrel 2": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress - Back Room Barrel 3": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress - Back Room Barrel 4": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress - Back Room Barrel 5": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress - Back Room Barrel 6": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress - Back Room Barrel 7": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Fortress Leaf Piles - Leaf Pile 1": TunicLocationData("Fortress Leaf Piles", BreakableType.leaves),
    "Fortress Leaf Piles - Leaf Pile 2": TunicLocationData("Fortress Leaf Piles", BreakableType.leaves),
    "Fortress Leaf Piles - Leaf Pile 3": TunicLocationData("Fortress Leaf Piles", BreakableType.leaves),
    "Fortress Leaf Piles - Leaf Pile 4": TunicLocationData("Fortress Leaf Piles", BreakableType.leaves),
    "Fortress Arena - Pot 1": TunicLocationData("Fortress Arena", BreakableType.pot),
    "Fortress Arena - Pot 2": TunicLocationData("Fortress Arena", BreakableType.pot),
    "Ruined Atoll - [West] Pot in Broken House 1": TunicLocationData("Ruined Atoll", BreakableType.pot),
    "Ruined Atoll - [West] Pot in Broken House 2": TunicLocationData("Ruined Atoll", BreakableType.pot),
    "Ruined Atoll - [West] Table in Broken House": TunicLocationData("Ruined Atoll", BreakableType.table),
    "Ruined Atoll - [South] Explosive Pot near Birds": TunicLocationData("Ruined Atoll", BreakableType.explosive_pot),
    "Frog Stairs - [Upper] Pot 1": TunicLocationData("Frog Stairs Upper", BreakableType.pot),
    "Frog Stairs - [Upper] Pot 2": TunicLocationData("Frog Stairs Upper", BreakableType.pot),
    "Frog Stairs - [Upper] Pot 3": TunicLocationData("Frog Stairs Upper", BreakableType.pot),
    "Frog Stairs - [Upper] Pot 4": TunicLocationData("Frog Stairs Upper", BreakableType.pot),
    "Frog Stairs - [Upper] Pot 5": TunicLocationData("Frog Stairs Upper", BreakableType.pot),
    "Frog Stairs - [Upper] Pot 6": TunicLocationData("Frog Stairs Upper", BreakableType.pot),
    "Frog's Domain - Pot above Orb Altar 1": TunicLocationData("Frog's Domain Front", BreakableType.pot),
    "Frog's Domain - Pot above Orb Altar 2": TunicLocationData("Frog's Domain Front", BreakableType.pot),
    "Frog's Domain - Side Room Pot 1": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain - Side Room Pot 2": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain - Side Room Pot 3": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain - Main Room Pot 1": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain - Main Room Pot 2": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain - Side Room Pot 4": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain - Pot after Gate 1": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain - Pot after Gate 2": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain - Orb Room Explosive Pot 1": TunicLocationData("Frog's Domain Main", BreakableType.explosive_pot),
    "Frog's Domain - Orb Room Explosive Pot 2": TunicLocationData("Frog's Domain Main", BreakableType.explosive_pot),
    "Library Lab - Display Case 1": TunicLocationData("Library Lab", BreakableType.glass),
    "Library Lab - Display Case 2": TunicLocationData("Library Lab", BreakableType.glass),
    "Library Lab - Display Case 3": TunicLocationData("Library Lab", BreakableType.glass),
    "Quarry - [East] Explosive Pot 1": TunicLocationData("Quarry", BreakableType.explosive_pot),
    "Quarry - [East] Explosive Pot 2": TunicLocationData("Quarry", BreakableType.explosive_pot),
    "Quarry - [East] Explosive Pot 3": TunicLocationData("Quarry", BreakableType.explosive_pot),
    "Quarry - [East] Explosive Pot beneath Scaffolding": TunicLocationData("Quarry", BreakableType.explosive_pot),
    "Quarry - [Central] Explosive Pot near Monastery 1": TunicLocationData("Quarry Monastery Entry", BreakableType.explosive_pot),
    "Quarry - [Central] Explosive Pot near Monastery 2": TunicLocationData("Quarry Monastery Entry", BreakableType.explosive_pot),
    "Quarry - [Back Entrance] Pot 1": TunicLocationData("Quarry Back", BreakableType.pot),
    "Quarry - [Back Entrance] Pot 2": TunicLocationData("Quarry Back", BreakableType.pot),
    "Quarry - [Back Entrance] Pot 3": TunicLocationData("Quarry Back", BreakableType.pot),
    "Quarry - [Back Entrance] Pot 4": TunicLocationData("Quarry Back", BreakableType.pot),
    "Quarry - [Back Entrance] Pot 5": TunicLocationData("Quarry Back", BreakableType.pot),
    "Quarry - [Central] Explosive Pot near Shortcut Ladder 1": TunicLocationData("Quarry Back", BreakableType.explosive_pot),
    "Quarry - [Central] Explosive Pot near Shortcut Ladder 2": TunicLocationData("Quarry Back", BreakableType.explosive_pot),
    "Quarry - [Central] Crate near Shortcut Ladder 1": TunicLocationData("Quarry Back", BreakableType.crate),
    "Quarry - [Central] Crate near Shortcut Ladder 2": TunicLocationData("Quarry Back", BreakableType.crate),
    "Quarry - [Central] Crate near Shortcut Ladder 3": TunicLocationData("Quarry Back", BreakableType.crate),
    "Quarry - [Central] Crate near Shortcut Ladder 4": TunicLocationData("Quarry Back", BreakableType.crate),
    "Quarry - [Central] Crate near Shortcut Ladder 5": TunicLocationData("Quarry Back", BreakableType.crate),
    "Quarry - [West] Explosive Pot near Bombable Wall 1": TunicLocationData("Lower Quarry upper pots", BreakableType.explosive_pot),
    "Quarry - [West] Explosive Pot near Bombable Wall 2": TunicLocationData("Lower Quarry upper pots", BreakableType.explosive_pot),
    "Quarry - [West] Explosive Pot above Shooting Range": TunicLocationData("Lower Quarry", BreakableType.explosive_pot),
    "Quarry - [West] Explosive Pot near Isolated Chest 1": TunicLocationData("Lower Quarry", BreakableType.explosive_pot),
    "Quarry - [West] Explosive Pot near Isolated Chest 2": TunicLocationData("Lower Quarry", BreakableType.explosive_pot),
    "Quarry - [West] Crate by Shooting Range 1": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Quarry - [West] Crate by Shooting Range 2": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Quarry - [West] Crate by Shooting Range 3": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Quarry - [West] Crate by Shooting Range 4": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Quarry - [West] Crate by Shooting Range 5": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Quarry - [West] Crate near Isolated Chest 1": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Quarry - [West] Crate near Isolated Chest 2": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Quarry - [West] Crate near Isolated Chest 3": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Quarry - [West] Crate near Isolated Chest 4": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Quarry - [West] Crate near Isolated Chest 5": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Quarry - [Lowlands] Crate 1": TunicLocationData("Even Lower Quarry", BreakableType.crate),
    "Quarry - [Lowlands] Crate 2": TunicLocationData("Even Lower Quarry", BreakableType.crate),
    "Monastery - Crate 1": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery - Crate 2": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery - Crate 3": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery - Crate 4": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery - Crate 5": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery - Crate 6": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery - Crate 7": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery - Crate 8": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery - Crate 9": TunicLocationData("Monastery Back", BreakableType.crate),
    "Cathedral - [1F] Pot by Stairs 1": TunicLocationData("Cathedral Main", BreakableType.pot),
    "Cathedral - [1F] Pot by Stairs 2": TunicLocationData("Cathedral Main", BreakableType.pot),
    "Purgatory - Pot 1": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 2": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 3": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 4": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 5": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 6": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 7": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 8": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 9": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 10": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 11": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 12": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 13": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 14": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 15": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 16": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 17": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 18": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 19": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 20": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 21": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 22": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 23": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 24": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 25": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 26": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 27": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 28": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 29": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 30": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 31": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 32": TunicLocationData("Purgatory", BreakableType.pot),
    "Purgatory - Pot 33": TunicLocationData("Purgatory", BreakableType.pot),
    "Overworld - [Central] Break Bombable Wall": TunicLocationData("Overworld", BreakableType.wall),
    "Overworld - [Southwest] Break Cube Cave Bombable Wall": TunicLocationData("Overworld", BreakableType.wall),
    "Overworld - [Southwest] Break Bombable Wall near Fountain": TunicLocationData("Overworld", BreakableType.wall),
    "Ruined Atoll - [Northwest] Break Bombable Wall": TunicLocationData("Ruined Atoll", BreakableType.wall),
    "East Forest - Break Bombable Wall": TunicLocationData("East Forest", BreakableType.wall),
    "Eastern Vault Fortress - [East Wing] Break Bombable Wall": TunicLocationData("Eastern Vault Fortress", BreakableType.wall),
    "Quarry - [West] Break Upper Area Bombable Wall": TunicLocationData("Quarry Back", BreakableType.wall),
    "Quarry - [East] Break Bombable Wall": TunicLocationData("Quarry", BreakableType.wall),
}


breakable_location_name_to_id: dict[str, int] = {name: breakable_base_id + index
                                                 for index, name in enumerate(breakable_location_table)}


# key is the name in the table above, value is the loc group name for the area
loc_group_convert: dict[str, str] = {
    "East Overworld": "Overworld",
    "Upper Overworld": "Overworld",
    "Overworld to West Garden from Furnace": "Overworld",
    "Forest Belltower Upper": "Forest Belltower",
    "Forest Belltower Main": "Forest Belltower",
    "Guard House 1 East": "Guardhouse 1",
    "Guard House 2 Lower": "Guardhouse 2",
    "Beneath the Well Back": "Beneath the Well",
    "Beneath the Well Main": "Beneath the Well",
    "Well Boss": "Dark Tomb Checkpoint",
    "Dark Tomb Main": "Dark Tomb",
    "Fortress Courtyard Upper": "Fortress Courtyard",
    "Fortress Courtyard Upper pot": "Fortress Courtyard",
    "Fortress Courtyard west pots": "Fortress Courtyard",
    "Fortress Courtyard westmost pots": "Fortress Courtyard",
    "Beneath the Vault Entry Spot": "Beneath the Fortress",
    "Beneath the Vault Main": "Beneath the Fortress",
    "Beneath the Vault Back": "Beneath the Fortress",
    "Fortress Grave Path Entry": "Fortress Grave Path",
    "Fortress Grave Path Combat": "Fortress Grave Path",
    "Fortress Grave Path westmost pot": "Fortress Grave Path",
    "Fortress Grave Path pots": "Fortress Grave Path",
    "Dusty": "Fortress Leaf Piles",
    "Frog Stairs Upper": "Frog Stairs",
    "Quarry Monastery Entry": "Quarry",
    "Quarry Back": "Quarry",
    "Lower Quarry": "Quarry",
    "Lower Quarry upper pots": "Quarry",
    "Even Lower Quarry": "Quarry",
    "Monastery Back": "Monastery",
}


breakable_location_groups: dict[str, set[str]] = {}
for location_name, location_data in breakable_location_table.items():
    group_name = loc_group_convert.get(location_data.er_region, location_data.er_region)
    breakable_location_groups.setdefault(group_name, set()).add(location_name)


def can_break_breakables(state: CollectionState, world: "TunicWorld") -> bool:
    return has_melee(state, world.player) or state.has_any(("Magic Wand", "Gun"), world.player)


# and also the table
def can_break_signs(state: CollectionState, world: "TunicWorld") -> bool:
    return (has_sword(state, world.player) or state.has_any(("Magic Wand", "Gun"), world.player)
            or (has_melee(state, world.player) and state.has("Glass Cannon", world.player)))


def can_break_leaf_piles(state: CollectionState, world: "TunicWorld") -> bool:
    return has_melee(state, world.player) or state.has_any(("Magic Dagger", "Gun"), world.player)


def can_break_bomb_walls(state: CollectionState, world: "TunicWorld") -> bool:
    return state.has("Gun", world.player) or can_shop(state, world)


def create_breakable_exclusive_regions(world: "TunicWorld") -> list[Region]:
    player = world.player
    multiworld = world.multiworld
    new_regions: list[Region] = []

    region = Region("Fortress Courtyard westmost pots", player, multiworld)
    new_regions.append(region)
    world.get_region("Fortress Courtyard").connect(region)
    world.get_region("Fortress Exterior near cave").connect(
        region, rule=lambda state: state.has_any(("Magic Wand", "Gun"), player))

    region = Region("Fortress Courtyard west pots", player, multiworld)
    new_regions.append(region)
    world.get_region("Fortress Courtyard").connect(region)
    world.get_region("Fortress Exterior near cave").connect(
        region, rule=lambda state: state.has("Magic Wand", player))

    region = Region("Fortress Courtyard Upper pot", player, multiworld)
    new_regions.append(region)
    world.get_region("Fortress Courtyard Upper").connect(region)
    world.get_region("Fortress Courtyard").connect(
        region, rule=lambda state: state.has("Magic Wand", player))

    region = Region("Fortress Grave Path westmost pot", player, multiworld)
    new_regions.append(region)
    world.get_region("Fortress Grave Path Entry").connect(region)
    world.get_region("Fortress Grave Path Upper").connect(
        region, rule=lambda state: state.has_any(("Magic Wand", "Gun"), player))

    region = Region("Fortress Grave Path pots", player, multiworld)
    new_regions.append(region)
    world.get_region("Fortress Grave Path by Grave").connect(region)
    world.get_region("Fortress Grave Path Dusty Entrance Region").connect(
        region, rule=lambda state: state.has("Magic Wand", player))

    region = Region("Lower Quarry upper pots", player, multiworld)
    new_regions.append(region)
    world.get_region("Lower Quarry").connect(region)
    world.get_region("Quarry Back").connect(
        region, rule=lambda state: state.has_any(("Magic Wand", "Gun"), player))

    for region in new_regions:
        multiworld.regions.append(region)

    return new_regions


def set_breakable_location_rules(world: "TunicWorld") -> None:
    for loc_name, loc_data in breakable_location_table.items():
        if not world.options.entrance_rando and loc_data.er_region == "Purgatory":
            continue
        location = world.get_location(loc_name)
        if loc_data.breakable == BreakableType.leaves:
            set_rule(location, lambda state: can_break_leaf_piles(state, world))
        elif loc_data.breakable in (BreakableType.sign, BreakableType.table):
            set_rule(location, lambda state: can_break_signs(state, world))
        elif loc_data.breakable == BreakableType.wall:
            set_rule(location, lambda state: can_break_bomb_walls(state, world))
        else:
            set_rule(location, lambda state: can_break_breakables(state, world))
