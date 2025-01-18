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
    "Overworld by Quarry Gate - Sign": TunicLocationData("Overworld", BreakableType.sign),
    "Overworld South of Checkpoint - Sign": TunicLocationData("Overworld", BreakableType.sign),
    "Overworld by Ruined Passage - Sign": TunicLocationData("Overworld", BreakableType.sign),
    "East Overworld - Pot 1": TunicLocationData("East Overworld", BreakableType.pot),
    "East Overworld - Pot 2": TunicLocationData("East Overworld", BreakableType.pot),
    "East Overworld - Pot 3": TunicLocationData("East Overworld", BreakableType.pot),
    "East Overworld - Pot 4": TunicLocationData("East Overworld", BreakableType.pot),
    "East Overworld - Pot 5": TunicLocationData("East Overworld", BreakableType.pot),
    "East Overworld - Sign 1": TunicLocationData("East Overworld", BreakableType.sign),
    "East Overworld - Sign 2": TunicLocationData("East Overworld", BreakableType.sign),
    "Upper Overworld - Pot 1": TunicLocationData("Upper Overworld", BreakableType.pot),
    "Upper Overworld - Pot 2": TunicLocationData("Upper Overworld", BreakableType.pot),
    "Upper Overworld - Pot 3": TunicLocationData("Upper Overworld", BreakableType.pot),
    "Upper Overworld - Pot 4": TunicLocationData("Upper Overworld", BreakableType.pot),
    "Overworld to West Garden from Furnace - Sign": TunicLocationData("Overworld to West Garden from Furnace", BreakableType.sign),
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
    "Forest Belltower Main - Pot 1": TunicLocationData("Forest Belltower Main", BreakableType.pot),
    "Forest Belltower Main - Pot 2": TunicLocationData("Forest Belltower Main", BreakableType.pot),
    "Forest Belltower Main - Pot 3": TunicLocationData("Forest Belltower Main", BreakableType.pot),
    "Forest Belltower Main - Pot 4": TunicLocationData("Forest Belltower Main", BreakableType.pot),
    "Forest Belltower Main - Pot 5": TunicLocationData("Forest Belltower Main", BreakableType.pot),
    "Forest Belltower Main - Pot 6": TunicLocationData("Forest Belltower Main", BreakableType.pot),
    "Forest Belltower Upper - Barrel 1": TunicLocationData("Forest Belltower Upper", BreakableType.barrel),
    "Forest Belltower Upper - Barrel 2": TunicLocationData("Forest Belltower Upper", BreakableType.barrel),
    "Forest Belltower Upper - Barrel 3": TunicLocationData("Forest Belltower Upper", BreakableType.barrel),
    "Forest Belltower after Boss - Pot 1": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower after Boss - Pot 2": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower after Boss - Pot 3": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower after Boss - Pot 4": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower after Boss - Pot 5": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower after Boss - Pot 6": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower after Boss - Pot 7": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower after Boss - Pot 8": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Forest Belltower after Boss - Pot 9": TunicLocationData("Forest Belltower Upper", BreakableType.pot),
    "Guardhouse 1 - Pot 1": TunicLocationData("Guard House 1 East", BreakableType.pot),
    "Guardhouse 1 - Pot 2": TunicLocationData("Guard House 1 East", BreakableType.pot),
    "Guardhouse 1 - Pot 3": TunicLocationData("Guard House 1 East", BreakableType.pot),
    "Guardhouse 1 - Pot 4": TunicLocationData("Guard House 1 East", BreakableType.pot),
    "Guardhouse 1 - Pot 5": TunicLocationData("Guard House 1 East", BreakableType.pot),
    "East Forest by Envoy - Sign 1": TunicLocationData("East Forest", BreakableType.sign),
    "East Forest - Sign 1": TunicLocationData("East Forest", BreakableType.sign),
    "East Forest - Pot 1": TunicLocationData("East Forest", BreakableType.pot),
    "East Forest - Pot 2": TunicLocationData("East Forest", BreakableType.pot),
    "East Forest - Pot 3": TunicLocationData("East Forest", BreakableType.pot),
    "East Forest by Envoy - Pot 1": TunicLocationData("East Forest", BreakableType.pot),
    "East Forest by Envoy - Pot 2": TunicLocationData("East Forest", BreakableType.pot),
    "East Forest by Envoy - Pot 3": TunicLocationData("East Forest", BreakableType.pot),
    "Guardhouse 2 - Pot 1": TunicLocationData("Guard House 2 Lower", BreakableType.pot),
    "Guardhouse 2 - Pot 2": TunicLocationData("Guard House 2 Lower", BreakableType.pot),
    "Guardhouse 2 - Pot 3": TunicLocationData("Guard House 2 Lower", BreakableType.pot),
    "Guardhouse 2 - Pot 4": TunicLocationData("Guard House 2 Lower", BreakableType.pot),
    "Guardhouse 2 - Pot 5": TunicLocationData("Guard House 2 Lower", BreakableType.pot),
    "Beneath the Well Back - Pot 1": TunicLocationData("Beneath the Well Back", BreakableType.pot),
    "Beneath the Well Back - Pot 2": TunicLocationData("Beneath the Well Back", BreakableType.pot),
    "Beneath the Well Back - Pot 3": TunicLocationData("Beneath the Well Back", BreakableType.pot),
    "Beneath the Well East - Barrel 1": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well East - Barrel 2": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well East - Barrel 3": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well West - Barrel 1": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well West - Barrel 2": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well West - Barrel 3": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well West - Barrel 4": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well West - Barrel 5": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well West - Barrel 6": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well West - Barrel 7": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well West - Barrel 8": TunicLocationData("Beneath the Well Main", BreakableType.barrel),
    "Beneath the Well East - Pot 1": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Beneath the Well East - Pot 2": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Beneath the Well East - Pot 3": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Beneath the Well East - Pot 4": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Beneath the Well East - Pot 5": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Beneath the Well East - Pot 6": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Beneath the Well East - Pot 7": TunicLocationData("Beneath the Well Main", BreakableType.pot),
    "Well Boss - Barrel 1": TunicLocationData("Well Boss", BreakableType.barrel),
    "Well Boss - Barrel 2": TunicLocationData("Well Boss", BreakableType.barrel),
    "Dark Tomb Pot Hallway - Pot 1": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Pot Hallway - Pot 2": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Pot Hallway - Pot 3": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Pot Hallway - Pot 4": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Pot Hallway - Pot 5": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Pot Hallway - Pot 6": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Pot Hallway - Pot 7": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Pot Hallway - Pot 8": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Pot Hallway - Pot 9": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Pot Hallway - Pot 10": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Pot Hallway - Pot 11": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Pot Hallway - Pot 12": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Pot Hallway - Pot 13": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Pot Hallway - Pot 14": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Final Chamber - Pot 1": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Final Chamber - Pot 2": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Final Chamber - Pot 3": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Final Chamber - Pot 4": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Dark Tomb Final Chamber - Pot 5": TunicLocationData("Dark Tomb Main", BreakableType.pot),
    "Magic Dagger House - Pot 1": TunicLocationData("Magic Dagger House", BreakableType.pot),
    "Magic Dagger House - Pot 2": TunicLocationData("Magic Dagger House", BreakableType.pot),
    "Magic Dagger House - Pot 3": TunicLocationData("Magic Dagger House", BreakableType.pot),
    "Fortress Courtyard - Fire Pot 1": TunicLocationData("Fortress Courtyard westmost pots", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 2": TunicLocationData("Fortress Courtyard westmost pots", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 3": TunicLocationData("Fortress Courtyard west pots", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 4": TunicLocationData("Fortress Courtyard west pots", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 5": TunicLocationData("Fortress Courtyard", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 6": TunicLocationData("Fortress Courtyard", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 7": TunicLocationData("Fortress Courtyard", BreakableType.fire_pot),
    "Fortress Courtyard - Fire Pot 8": TunicLocationData("Fortress Courtyard", BreakableType.fire_pot),
    "Fortress Courtyard Upper - Fire Pot": TunicLocationData("Fortress Courtyard Upper pot", BreakableType.fire_pot),
    "Fortress Grave Path - Pot 1": TunicLocationData("Fortress Grave Path Entry", BreakableType.pot),
    "Fortress Grave Path - Pot 2": TunicLocationData("Fortress Grave Path Entry", BreakableType.pot),
    "Fortress Grave Path by Grave - Pot 1": TunicLocationData("Fortress Grave Path pots", BreakableType.pot),
    "Fortress Grave Path by Grave - Pot 2": TunicLocationData("Fortress Grave Path pots", BreakableType.pot),
    "Fortress Grave Path by Grave - Pot 3": TunicLocationData("Fortress Grave Path pots", BreakableType.pot),
    "Fortress Grave Path by Grave - Pot 4": TunicLocationData("Fortress Grave Path pots", BreakableType.pot),
    "Fortress Grave Path by Grave - Pot 5": TunicLocationData("Fortress Grave Path pots", BreakableType.pot),
    "Fortress Grave Path by Grave - Pot 6": TunicLocationData("Fortress Grave Path pots", BreakableType.pot),
    "Fortress Grave Path - Fire Pot 1": TunicLocationData("Fortress Grave Path westmost pot", BreakableType.fire_pot),
    "Fortress Grave Path - Fire Pot 2": TunicLocationData("Fortress Grave Path Combat", BreakableType.fire_pot),
    "Eastern Vault Fortress by Door - Pot 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Door - Pot 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Door - Pot 3": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Door - Pot 4": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Door - Pot 5": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Door - Pot 6": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Door - Pot 7": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Door - Pot 8": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Door - Pot 9": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Door - Pot 10": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Door - Pot 11": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Broken Checkpoint - Pot 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Broken Checkpoint - Pot 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Broken Checkpoint - Pot 3": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Checkpoint - Pot 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Checkpoint - Pot 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Checkpoint - Pot 3": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Overlook - Pot 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Overlook - Pot 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress Slorm Room - Pot 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress Slorm Room - Pot 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress Slorm Room - Pot 3": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress Chest Room - Pot 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress Chest Room - Pot 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Stairs to Basement - Pot 1": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Stairs to Basement - Pot 2": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Eastern Vault Fortress by Stairs to Basement - Pot 3": TunicLocationData("Eastern Vault Fortress", BreakableType.pot),
    "Beneath the Fortress Entry Spot - Pot 1": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.pot),
    "Beneath the Fortress Entry Spot - Pot 2": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.pot),
    "Beneath the Fortress Entry Spot - Crate 1": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress Entry Spot - Crate 2": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress Entry Spot - Crate 3": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress Entry Spot - Crate 4": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress Entry Spot - Crate 5": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress Entry Spot - Crate 6": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress Entry Spot - Crate 7": TunicLocationData("Beneath the Vault Entry Spot", BreakableType.crate),
    "Beneath the Fortress Main - Crate 1": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress Main - Crate 2": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress Main - Crate 3": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress Main - Crate 4": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress Main - Crate 5": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress Main - Crate 6": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress Main - Crate 7": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress Main - Crate 8": TunicLocationData("Beneath the Vault Main", BreakableType.crate),
    "Beneath the Fortress Back - Fire Pot 1": TunicLocationData("Beneath the Vault Back", BreakableType.fire_pot),
    "Beneath the Fortress Back - Fire Pot 2": TunicLocationData("Beneath the Vault Back", BreakableType.fire_pot),
    "Beneath the Fortress Back - Fire Pot 3": TunicLocationData("Beneath the Vault Back", BreakableType.fire_pot),
    "Beneath the Fortress Back - Barrel 1": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress Back - Barrel 2": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress Back - Barrel 3": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress Back - Barrel 4": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress Back - Barrel 5": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress Back - Barrel 6": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress Back - Barrel 7": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress Back - Barrel 8": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress Back - Barrel 9": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress Back - Barrel 10": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress Back - Barrel 11": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress Back - Barrel 12": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Beneath the Fortress Back - Barrel 13": TunicLocationData("Beneath the Vault Back", BreakableType.barrel),
    "Fortress Leaf Piles - Leaf Pile 1": TunicLocationData("Fortress Leaf Piles", BreakableType.leaves),
    "Fortress Leaf Piles - Leaf Pile 2": TunicLocationData("Fortress Leaf Piles", BreakableType.leaves),
    "Fortress Leaf Piles - Leaf Pile 3": TunicLocationData("Fortress Leaf Piles", BreakableType.leaves),
    "Fortress Leaf Piles - Leaf Pile 4": TunicLocationData("Fortress Leaf Piles", BreakableType.leaves),
    "Fortress Arena - Pot 1": TunicLocationData("Fortress Arena", BreakableType.pot),
    "Fortress Arena - Pot 2": TunicLocationData("Fortress Arena", BreakableType.pot),
    "Ruined Atoll Southwest - Pot 1": TunicLocationData("Ruined Atoll", BreakableType.pot),
    "Ruined Atoll Southwest - Pot 2": TunicLocationData("Ruined Atoll", BreakableType.pot),
    "Ruined Atoll Southwest - Table": TunicLocationData("Ruined Atoll", BreakableType.table),
    "Ruined Atoll near Birds - Explosive Pot": TunicLocationData("Ruined Atoll", BreakableType.explosive_pot),
    "Frog Stairs Upper - Pot 1": TunicLocationData("Frog Stairs Upper", BreakableType.pot),
    "Frog Stairs Upper - Pot 2": TunicLocationData("Frog Stairs Upper", BreakableType.pot),
    "Frog Stairs Upper - Pot 3": TunicLocationData("Frog Stairs Upper", BreakableType.pot),
    "Frog Stairs Upper - Pot 4": TunicLocationData("Frog Stairs Upper", BreakableType.pot),
    "Frog Stairs Upper - Pot 5": TunicLocationData("Frog Stairs Upper", BreakableType.pot),
    "Frog Stairs Upper - Pot 6": TunicLocationData("Frog Stairs Upper", BreakableType.pot),
    "Frog's Domain above Orb Altar - Pot 1": TunicLocationData("Frog's Domain Front", BreakableType.pot),
    "Frog's Domain above Orb Altar - Pot 2": TunicLocationData("Frog's Domain Front", BreakableType.pot),
    "Frog's Domain Side Room - Pot 1": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain Side Room - Pot 2": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain Side Room - Pot 3": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain Main Room - Pot 1": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain Main Room - Pot 2": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain Side Room - Pot 4": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain after Gate - Pot 1": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain after Gate - Pot 2": TunicLocationData("Frog's Domain Main", BreakableType.pot),
    "Frog's Domain Orb Room - Explosive Pot 1": TunicLocationData("Frog's Domain Main", BreakableType.explosive_pot),
    "Frog's Domain Orb Room - Explosive Pot 2": TunicLocationData("Frog's Domain Main", BreakableType.explosive_pot),
    "Library Lab - Library Glass 1": TunicLocationData("Library Lab", BreakableType.glass),
    "Library Lab - Library Glass 2": TunicLocationData("Library Lab", BreakableType.glass),
    "Library Lab - Library Glass 3": TunicLocationData("Library Lab", BreakableType.glass),
    "Quarry East - Explosive Pot 1": TunicLocationData("Quarry", BreakableType.explosive_pot),
    "Quarry East - Explosive Pot 2": TunicLocationData("Quarry", BreakableType.explosive_pot),
    "Quarry East - Explosive Pot 3": TunicLocationData("Quarry", BreakableType.explosive_pot),
    "Quarry East beneath Scaffolding - Explosive Pot": TunicLocationData("Quarry", BreakableType.explosive_pot),
    "Quarry Monastery Entry - Explosive Pot 1": TunicLocationData("Quarry Monastery Entry", BreakableType.explosive_pot),
    "Quarry Monastery Entry - Explosive Pot 2": TunicLocationData("Quarry Monastery Entry", BreakableType.explosive_pot),
    "Quarry Back - Pot 1": TunicLocationData("Quarry Back", BreakableType.pot),
    "Quarry Back - Pot 2": TunicLocationData("Quarry Back", BreakableType.pot),
    "Quarry Back - Pot 3": TunicLocationData("Quarry Back", BreakableType.pot),
    "Quarry Back - Pot 4": TunicLocationData("Quarry Back", BreakableType.pot),
    "Quarry Back - Pot 5": TunicLocationData("Quarry Back", BreakableType.pot),
    "Quarry near Shortcut Ladder - Explosive Pot 1": TunicLocationData("Quarry Back", BreakableType.explosive_pot),
    "Quarry near Shortcut Ladder - Explosive Pot 2": TunicLocationData("Quarry Back", BreakableType.explosive_pot),
    "Quarry near Shortcut Ladder - Crate 1": TunicLocationData("Quarry Back", BreakableType.crate),
    "Quarry near Shortcut Ladder - Crate 2": TunicLocationData("Quarry Back", BreakableType.crate),
    "Quarry near Shortcut Ladder - Crate 3": TunicLocationData("Quarry Back", BreakableType.crate),
    "Quarry near Shortcut Ladder - Crate 4": TunicLocationData("Quarry Back", BreakableType.crate),
    "Quarry near Shortcut Ladder - Crate 5": TunicLocationData("Quarry Back", BreakableType.crate),
    "Lower Quarry - Explosive Pot 1": TunicLocationData("Lower Quarry upper pots", BreakableType.explosive_pot),
    "Lower Quarry - Explosive Pot 2": TunicLocationData("Lower Quarry upper pots", BreakableType.explosive_pot),
    "Lower Quarry - Explosive Pot 3": TunicLocationData("Lower Quarry", BreakableType.explosive_pot),
    "Lower Quarry on Scaffolding - Explosive Pot 1": TunicLocationData("Lower Quarry", BreakableType.explosive_pot),
    "Lower Quarry on Scaffolding - Explosive Pot 2": TunicLocationData("Lower Quarry", BreakableType.explosive_pot),
    "Lower Quarry Shooting Range - Crate 1": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Lower Quarry Shooting Range - Crate 2": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Lower Quarry Shooting Range - Crate 3": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Lower Quarry Shooting Range - Crate 4": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Lower Quarry Shooting Range - Crate 5": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Lower Quarry on Scaffolding - Crate 1": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Lower Quarry on Scaffolding - Crate 2": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Lower Quarry on Scaffolding - Crate 3": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Lower Quarry on Scaffolding - Crate 4": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Lower Quarry on Scaffolding - Crate 5": TunicLocationData("Lower Quarry", BreakableType.crate),
    "Even Lower Quarry - Crate 1": TunicLocationData("Even Lower Quarry", BreakableType.crate),
    "Even Lower Quarry - Crate 2": TunicLocationData("Even Lower Quarry", BreakableType.crate),
    "Monastery Back - Crate 1": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery Back - Crate 2": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery Back - Crate 3": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery Back - Crate 4": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery Back - Crate 5": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery Back - Crate 6": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery Back - Crate 7": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery Back - Crate 8": TunicLocationData("Monastery Back", BreakableType.crate),
    "Monastery Back - Crate 9": TunicLocationData("Monastery Back", BreakableType.crate),
    "Cathedral - Pot 1": TunicLocationData("Cathedral Main", BreakableType.pot),
    "Cathedral - Pot 2": TunicLocationData("Cathedral Main", BreakableType.pot),
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
    "Overworld South of Checkpoint - Break Bombable Wall": TunicLocationData("Overworld", BreakableType.wall),
    "Overworld Cube Cave Entrance - Break Bombable Wall": TunicLocationData("Overworld", BreakableType.wall),
    "Overworld near Fountain - Break Bombable Wall": TunicLocationData("Overworld", BreakableType.wall),
    "Ruined Atoll - Break Bombable Wall": TunicLocationData("Ruined Atoll", BreakableType.wall),
    "East Forest - Break Bombable Wall": TunicLocationData("East Forest", BreakableType.wall),
    "Eastern Vault Fortress - Break Bombable Wall": TunicLocationData("Eastern Vault Fortress", BreakableType.wall),
    "Quarry Back - Break Bombable Wall": TunicLocationData("Quarry Back", BreakableType.wall),
    "Quarry East - Break Bombable Wall": TunicLocationData("Quarry", BreakableType.wall),
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
    "Guard House 1 East": "Guard House 1",
    "Guard House 2 Lower": "Guard House 2",
    "Beneath the Well Back": "Beneath the Well",
    "Beneath the Well Main": "Beneath the Well",
    "Well Boss": "Dark Tomb Checkpoint",
    "Dark Tomb Main": "Dark Tomb",
    "Fortress Courtyard Upper": "Fortress Courtyard",
    "Beneath the Vault Entry Spot": "Beneath the Vault",
    "Beneath the Vault Main": "Beneath the Vault",
    "Beneath the Vault Back": "Beneath the Vault",
    "Dusty": "Fortress Leaf Piles",
    "Frog Stairs Upper": "Frog Stairs",
    "Quarry Monastery Entry": "Quarry",
    "Quarry Back": "Quarry",
    "Lower Quarry": "Quarry",
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
    return has_sword(state, world.player) or state.has_any(("Magic Wand", "Gun"), world.player)


def can_break_leaf_piles(state: CollectionState, world: "TunicWorld") -> bool:
    return has_melee(state, world.player) or state.has_any(("Magic Dagger", "Gun"), world.player)


def can_break_bomb_walls(state: CollectionState, world: "TunicWorld") -> bool:
    return state.has("Gun", world.player) or can_shop(state, world)


def create_breakable_exclusive_regions(world: "TunicWorld") -> list[Region]:
    player = world.player
    new_regions: list[Region] = []

    region = Region("Fortress Courtyard westmost pots", world.player, world.multiworld)
    new_regions.append(region)
    world.get_region("Fortress Courtyard").connect(region)
    world.get_region("Fortress Exterior near cave").connect(
        region, rule=lambda state: state.has_any(("Magic Wand", "Gun"), player))

    region = Region("Fortress Courtyard west pots", world.player, world.multiworld)
    new_regions.append(region)
    world.get_region("Fortress Courtyard").connect(region)
    world.get_region("Fortress Exterior near cave").connect(
        region, rule=lambda state: state.has("Magic Wand", player))

    region = Region("Fortress Courtyard Upper pot", world.player, world.multiworld)
    new_regions.append(region)
    world.get_region("Fortress Courtyard Upper").connect(region)
    world.get_region("Fortress Courtyard").connect(
        region, rule=lambda state: state.has("Magic Wand", player))

    region = Region("Fortress Grave Path westmost pot", world.player, world.multiworld)
    new_regions.append(region)
    world.get_region("Fortress Grave Path Entry").connect(region)
    world.get_region("Fortress Grave Path Upper").connect(
        region, rule=lambda state: state.has_any(("Magic Wand", "Gun"), player))

    region = Region("Fortress Grave Path pots", world.player, world.multiworld)
    new_regions.append(region)
    world.get_region("Fortress Grave Path by Grave").connect(region)
    world.get_region("Fortress Grave Path Dusty Entrance Region").connect(
        region, rule=lambda state: state.has("Magic Wand", player))

    region = Region("Lower Quarry upper pots", world.player, world.multiworld)
    new_regions.append(region)
    world.get_region("Lower Quarry").connect(region)
    world.get_region("Quarry Back").connect(
        region, rule=lambda state: state.has_any(("Magic Wand", "Gun"), player))

    for region in new_regions:
        world.multiworld.regions.append(region)

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
