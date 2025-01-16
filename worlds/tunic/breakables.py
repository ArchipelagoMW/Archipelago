from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import CollectionState, Region
from worlds.generic.Rules import set_rule
from .rules import has_sword, has_melee
if TYPE_CHECKING:
    from . import TunicWorld


# just getting an id that is a decent chunk ahead of the grass ones
breakable_base_id = 509342400 + 8000


class TunicLocationData(NamedTuple):
    er_region: str
    breakable: str | None = None


breakable_location_table: dict[str, TunicLocationData] = {
    "Overworld - Sign 1": TunicLocationData("Overworld", breakable="Sign"),
    "Overworld - Sign 2": TunicLocationData("Overworld", breakable="Sign"),
    "Overworld - Sign 3": TunicLocationData("Overworld", breakable="Sign"),
    "East Overworld - Pot 1": TunicLocationData("East Overworld", breakable="Pot"),
    "East Overworld - Pot 2": TunicLocationData("East Overworld", breakable="Pot"),
    "East Overworld - Pot 3": TunicLocationData("East Overworld", breakable="Pot"),
    "East Overworld - Pot 4": TunicLocationData("East Overworld", breakable="Pot"),
    "East Overworld - Pot 5": TunicLocationData("East Overworld", breakable="Pot"),
    "East Overworld - Sign 1": TunicLocationData("East Overworld", breakable="Sign"),
    "East Overworld - Sign 2": TunicLocationData("East Overworld", breakable="Sign"),
    "Upper Overworld - Pot 1": TunicLocationData("Upper Overworld", breakable="Pot"),
    "Upper Overworld - Pot 2": TunicLocationData("Upper Overworld", breakable="Pot"),
    "Upper Overworld - Pot 3": TunicLocationData("Upper Overworld", breakable="Pot"),
    "Upper Overworld - Pot 4": TunicLocationData("Upper Overworld", breakable="Pot"),
    "Overworld to West Garden from Furnace - Sign": TunicLocationData("Overworld to West Garden from Furnace", breakable="Sign"),
    "Stick House - Pot 1": TunicLocationData("Stick House", breakable="Pot"),
    "Stick House - Pot 2": TunicLocationData("Stick House", breakable="Pot"),
    "Stick House - Pot 3": TunicLocationData("Stick House", breakable="Pot"),
    "Stick House - Pot 4": TunicLocationData("Stick House", breakable="Pot"),
    "Stick House - Pot 5": TunicLocationData("Stick House", breakable="Pot"),
    "Stick House - Pot 6": TunicLocationData("Stick House", breakable="Pot"),
    "Stick House - Pot 7": TunicLocationData("Stick House", breakable="Pot"),
    "Ruined Shop - Pot 1": TunicLocationData("Ruined Shop", breakable="Pot"),
    "Ruined Shop - Pot 2": TunicLocationData("Ruined Shop", breakable="Pot"),
    "Ruined Shop - Pot 3": TunicLocationData("Ruined Shop", breakable="Pot"),
    "Ruined Shop - Pot 4": TunicLocationData("Ruined Shop", breakable="Pot"),
    "Ruined Shop - Pot 5": TunicLocationData("Ruined Shop", breakable="Pot"),
    "Hourglass Cave - Sign": TunicLocationData("Hourglass Cave", breakable="Sign"),
    "Forest Belltower Main - Pot 1": TunicLocationData("Forest Belltower Main", breakable="Pot"),
    "Forest Belltower Main - Pot 2": TunicLocationData("Forest Belltower Main", breakable="Pot"),
    "Forest Belltower Main - Pot 3": TunicLocationData("Forest Belltower Main", breakable="Pot"),
    "Forest Belltower Main - Pot 4": TunicLocationData("Forest Belltower Main", breakable="Pot"),
    "Forest Belltower Main - Pot 5": TunicLocationData("Forest Belltower Main", breakable="Pot"),
    "Forest Belltower Main - Pot 6": TunicLocationData("Forest Belltower Main", breakable="Pot"),
    "Forest Belltower Upper - Barrel 1": TunicLocationData("Forest Belltower Upper", breakable="Barrel"),
    "Forest Belltower Upper - Barrel 2": TunicLocationData("Forest Belltower Upper", breakable="Barrel"),
    "Forest Belltower Upper - Barrel 3": TunicLocationData("Forest Belltower Upper", breakable="Barrel"),
    "Forest Belltower after Boss - Pot 1": TunicLocationData("Forest Belltower Upper", breakable="Pot"),
    "Forest Belltower after Boss - Pot 2": TunicLocationData("Forest Belltower Upper", breakable="Pot"),
    "Forest Belltower after Boss - Pot 3": TunicLocationData("Forest Belltower Upper", breakable="Pot"),
    "Forest Belltower after Boss - Pot 4": TunicLocationData("Forest Belltower Upper", breakable="Pot"),
    "Forest Belltower after Boss - Pot 5": TunicLocationData("Forest Belltower Upper", breakable="Pot"),
    "Forest Belltower after Boss - Pot 6": TunicLocationData("Forest Belltower Upper", breakable="Pot"),
    "Forest Belltower after Boss - Pot 7": TunicLocationData("Forest Belltower Upper", breakable="Pot"),
    "Forest Belltower after Boss - Pot 8": TunicLocationData("Forest Belltower Upper", breakable="Pot"),
    "Forest Belltower after Boss - Pot 9": TunicLocationData("Forest Belltower Upper", breakable="Pot"),
    "Guard House 1 - Pot 1": TunicLocationData("Guard House 1 East", breakable="Pot"),
    "Guard House 1 - Pot 2": TunicLocationData("Guard House 1 East", breakable="Pot"),
    "Guard House 1 - Pot 3": TunicLocationData("Guard House 1 East", breakable="Pot"),
    "Guard House 1 - Pot 4": TunicLocationData("Guard House 1 East", breakable="Pot"),
    "Guard House 1 - Pot 5": TunicLocationData("Guard House 1 East", breakable="Pot"),
    "East Forest by Envoy - Sign 1": TunicLocationData("East Forest", breakable="Sign"),
    "East Forest - Sign 1": TunicLocationData("East Forest", breakable="Sign"),
    "East Forest - Pot 1": TunicLocationData("East Forest", breakable="Pot"),
    "East Forest - Pot 2": TunicLocationData("East Forest", breakable="Pot"),
    "East Forest - Pot 3": TunicLocationData("East Forest", breakable="Pot"),
    "East Forest by Envoy - Pot 1": TunicLocationData("East Forest", breakable="Pot"),
    "East Forest by Envoy - Pot 2": TunicLocationData("East Forest", breakable="Pot"),
    "East Forest by Envoy - Pot 3": TunicLocationData("East Forest", breakable="Pot"),
    "Guard House 2 - Pot 1": TunicLocationData("Guard House 2 Lower", breakable="Pot"),
    "Guard House 2 - Pot 2": TunicLocationData("Guard House 2 Lower", breakable="Pot"),
    "Guard House 2 - Pot 3": TunicLocationData("Guard House 2 Lower", breakable="Pot"),
    "Guard House 2 - Pot 4": TunicLocationData("Guard House 2 Lower", breakable="Pot"),
    "Guard House 2 - Pot 5": TunicLocationData("Guard House 2 Lower", breakable="Pot"),
    "Beneath the Well Back - Pot 1": TunicLocationData("Beneath the Well Back", breakable="Pot"),
    "Beneath the Well Back - Pot 2": TunicLocationData("Beneath the Well Back", breakable="Pot"),
    "Beneath the Well Back - Pot 3": TunicLocationData("Beneath the Well Back", breakable="Pot"),
    "Beneath the Well East - Barrel 1": TunicLocationData("Beneath the Well Main", breakable="Barrel"),
    "Beneath the Well East - Barrel 2": TunicLocationData("Beneath the Well Main", breakable="Barrel"),
    "Beneath the Well East - Barrel 3": TunicLocationData("Beneath the Well Main", breakable="Barrel"),
    "Beneath the Well West - Barrel 1": TunicLocationData("Beneath the Well Main", breakable="Barrel"),
    "Beneath the Well West - Barrel 2": TunicLocationData("Beneath the Well Main", breakable="Barrel"),
    "Beneath the Well West - Barrel 3": TunicLocationData("Beneath the Well Main", breakable="Barrel"),
    "Beneath the Well West - Barrel 4": TunicLocationData("Beneath the Well Main", breakable="Barrel"),
    "Beneath the Well West - Barrel 5": TunicLocationData("Beneath the Well Main", breakable="Barrel"),
    "Beneath the Well West - Barrel 6": TunicLocationData("Beneath the Well Main", breakable="Barrel"),
    "Beneath the Well West - Barrel 7": TunicLocationData("Beneath the Well Main", breakable="Barrel"),
    "Beneath the Well West - Barrel 8": TunicLocationData("Beneath the Well Main", breakable="Barrel"),
    "Beneath the Well East - Pot 1": TunicLocationData("Beneath the Well Main", breakable="Pot"),
    "Beneath the Well East - Pot 2": TunicLocationData("Beneath the Well Main", breakable="Pot"),
    "Beneath the Well East - Pot 3": TunicLocationData("Beneath the Well Main", breakable="Pot"),
    "Beneath the Well East - Pot 4": TunicLocationData("Beneath the Well Main", breakable="Pot"),
    "Beneath the Well East - Pot 5": TunicLocationData("Beneath the Well Main", breakable="Pot"),
    "Beneath the Well East - Pot 6": TunicLocationData("Beneath the Well Main", breakable="Pot"),
    "Beneath the Well East - Pot 7": TunicLocationData("Beneath the Well Main", breakable="Pot"),
    "Well Boss - Barrel 1": TunicLocationData("Well Boss", breakable="Barrel"),
    "Well Boss - Barrel 2": TunicLocationData("Well Boss", breakable="Barrel"),
    "Dark Tomb Pot Hallway - Pot 1": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Pot Hallway - Pot 2": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Pot Hallway - Pot 3": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Pot Hallway - Pot 4": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Pot Hallway - Pot 5": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Pot Hallway - Pot 6": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Pot Hallway - Pot 7": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Pot Hallway - Pot 8": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Pot Hallway - Pot 9": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Pot Hallway - Pot 10": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Pot Hallway - Pot 11": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Pot Hallway - Pot 12": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Pot Hallway - Pot 13": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Pot Hallway - Pot 14": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Final Chamber - Pot 1": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Final Chamber - Pot 2": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Final Chamber - Pot 3": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Final Chamber - Pot 4": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Dark Tomb Final Chamber - Pot 5": TunicLocationData("Dark Tomb Main", breakable="Pot"),
    "Magic Dagger House - Pot 1": TunicLocationData("Magic Dagger House", breakable="Pot"),
    "Magic Dagger House - Pot 2": TunicLocationData("Magic Dagger House", breakable="Pot"),
    "Magic Dagger House - Pot 3": TunicLocationData("Magic Dagger House", breakable="Pot"),
    "Fortress Courtyard - Fire Pot 1": TunicLocationData("Fortress Courtyard westmost pots", breakable="Fire Pot"),
    "Fortress Courtyard - Fire Pot 2": TunicLocationData("Fortress Courtyard westmost pots", breakable="Fire Pot"),
    "Fortress Courtyard - Fire Pot 3": TunicLocationData("Fortress Courtyard west pots", breakable="Fire Pot"),
    "Fortress Courtyard - Fire Pot 4": TunicLocationData("Fortress Courtyard west pots", breakable="Fire Pot"),
    "Fortress Courtyard - Fire Pot 5": TunicLocationData("Fortress Courtyard", breakable="Fire Pot"),
    "Fortress Courtyard - Fire Pot 6": TunicLocationData("Fortress Courtyard", breakable="Fire Pot"),
    "Fortress Courtyard - Fire Pot 7": TunicLocationData("Fortress Courtyard", breakable="Fire Pot"),
    "Fortress Courtyard - Fire Pot 8": TunicLocationData("Fortress Courtyard", breakable="Fire Pot"),
    "Fortress Courtyard Upper - Fire Pot": TunicLocationData("Fortress Courtyard Upper pot", breakable="Fire Pot"),
    "Fortress Grave Path - Pot 1": TunicLocationData("Fortress Grave Path Entry", breakable="Pot"),
    "Fortress Grave Path - Pot 2": TunicLocationData("Fortress Grave Path Entry", breakable="Pot"),
    "Fortress Grave Path by Grave - Pot 1": TunicLocationData("Fortress Grave Path pots", breakable="Pot"),
    "Fortress Grave Path by Grave - Pot 2": TunicLocationData("Fortress Grave Path pots", breakable="Pot"),
    "Fortress Grave Path by Grave - Pot 3": TunicLocationData("Fortress Grave Path pots", breakable="Pot"),
    "Fortress Grave Path by Grave - Pot 4": TunicLocationData("Fortress Grave Path pots", breakable="Pot"),
    "Fortress Grave Path by Grave - Pot 5": TunicLocationData("Fortress Grave Path pots", breakable="Pot"),
    "Fortress Grave Path by Grave - Pot 6": TunicLocationData("Fortress Grave Path pots", breakable="Pot"),
    "Fortress Grave Path - Fire Pot 1": TunicLocationData("Fortress Grave Path westmost pot", breakable="Fire Pot"),
    "Fortress Grave Path - Fire Pot 2": TunicLocationData("Fortress Grave Path Combat", breakable="Fire Pot"),
    "Eastern Vault Fortress by Door - Pot 1": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Door - Pot 2": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Door - Pot 3": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Door - Pot 4": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Door - Pot 5": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Door - Pot 6": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Door - Pot 7": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Door - Pot 8": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Door - Pot 9": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Door - Pot 10": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Door - Pot 11": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Broken Checkpoint - Pot 1": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Broken Checkpoint - Pot 2": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Broken Checkpoint - Pot 3": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Checkpoint - Pot 1": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Checkpoint - Pot 2": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Checkpoint - Pot 3": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Overlook - Pot 1": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Overlook - Pot 2": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress Slorm Room - Pot 1": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress Slorm Room - Pot 2": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress Slorm Room - Pot 3": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress Chest Room - Pot 1": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress Chest Room - Pot 2": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Stairs to Basement - Pot 1": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Stairs to Basement - Pot 2": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Eastern Vault Fortress by Stairs to Basement - Pot 3": TunicLocationData("Eastern Vault Fortress", breakable="Pot"),
    "Beneath the Vault Entry Spot - Pot 1": TunicLocationData("Beneath the Vault Entry Spot", breakable="Pot"),
    "Beneath the Vault Entry Spot - Pot 2": TunicLocationData("Beneath the Vault Entry Spot", breakable="Pot"),
    "Beneath the Vault Entry Spot - Crate 1": TunicLocationData("Beneath the Vault Entry Spot", breakable="Crate"),
    "Beneath the Vault Entry Spot - Crate 2": TunicLocationData("Beneath the Vault Entry Spot", breakable="Crate"),
    "Beneath the Vault Entry Spot - Crate 3": TunicLocationData("Beneath the Vault Entry Spot", breakable="Crate"),
    "Beneath the Vault Entry Spot - Crate 4": TunicLocationData("Beneath the Vault Entry Spot", breakable="Crate"),
    "Beneath the Vault Entry Spot - Crate 5": TunicLocationData("Beneath the Vault Entry Spot", breakable="Crate"),
    "Beneath the Vault Entry Spot - Crate 6": TunicLocationData("Beneath the Vault Entry Spot", breakable="Crate"),
    "Beneath the Vault Entry Spot - Crate 7": TunicLocationData("Beneath the Vault Entry Spot", breakable="Crate"),
    "Beneath the Vault Main - Crate 1": TunicLocationData("Beneath the Vault Main", breakable="Crate"),
    "Beneath the Vault Main - Crate 2": TunicLocationData("Beneath the Vault Main", breakable="Crate"),
    "Beneath the Vault Main - Crate 3": TunicLocationData("Beneath the Vault Main", breakable="Crate"),
    "Beneath the Vault Main - Crate 4": TunicLocationData("Beneath the Vault Main", breakable="Crate"),
    "Beneath the Vault Main - Crate 5": TunicLocationData("Beneath the Vault Main", breakable="Crate"),
    "Beneath the Vault Main - Crate 6": TunicLocationData("Beneath the Vault Main", breakable="Crate"),
    "Beneath the Vault Main - Crate 7": TunicLocationData("Beneath the Vault Main", breakable="Crate"),
    "Beneath the Vault Main - Crate 8": TunicLocationData("Beneath the Vault Main", breakable="Crate"),
    "Beneath the Vault Back - Fire Pot 1": TunicLocationData("Beneath the Vault Back", breakable="Fire Pot"),
    "Beneath the Vault Back - Fire Pot 2": TunicLocationData("Beneath the Vault Back", breakable="Fire Pot"),
    "Beneath the Vault Back - Fire Pot 3": TunicLocationData("Beneath the Vault Back", breakable="Fire Pot"),
    "Beneath the Vault Back - Barrel 1": TunicLocationData("Beneath the Vault Back", breakable="Barrel"),
    "Beneath the Vault Back - Barrel 2": TunicLocationData("Beneath the Vault Back", breakable="Barrel"),
    "Beneath the Vault Back - Barrel 3": TunicLocationData("Beneath the Vault Back", breakable="Barrel"),
    "Beneath the Vault Back - Barrel 4": TunicLocationData("Beneath the Vault Back", breakable="Barrel"),
    "Beneath the Vault Back - Barrel 5": TunicLocationData("Beneath the Vault Back", breakable="Barrel"),
    "Beneath the Vault Back - Barrel 6": TunicLocationData("Beneath the Vault Back", breakable="Barrel"),
    "Beneath the Vault Back - Barrel 7": TunicLocationData("Beneath the Vault Back", breakable="Barrel"),
    "Beneath the Vault Back - Barrel 8": TunicLocationData("Beneath the Vault Back", breakable="Barrel"),
    "Beneath the Vault Back - Barrel 9": TunicLocationData("Beneath the Vault Back", breakable="Barrel"),
    "Beneath the Vault Back - Barrel 10": TunicLocationData("Beneath the Vault Back", breakable="Barrel"),
    "Beneath the Vault Back - Barrel 11": TunicLocationData("Beneath the Vault Back", breakable="Barrel"),
    "Beneath the Vault Back - Barrel 12": TunicLocationData("Beneath the Vault Back", breakable="Barrel"),
    "Beneath the Vault Back - Barrel 13": TunicLocationData("Beneath the Vault Back", breakable="Barrel"),
    "Fortress Leaf Piles - Leaf Pile 1": TunicLocationData("Fortress Leaf Piles", breakable="Leaf Pile"),
    "Fortress Leaf Piles - Leaf Pile 2": TunicLocationData("Fortress Leaf Piles", breakable="Leaf Pile"),
    "Fortress Leaf Piles - Leaf Pile 3": TunicLocationData("Fortress Leaf Piles", breakable="Leaf Pile"),
    "Fortress Leaf Piles - Leaf Pile 4": TunicLocationData("Fortress Leaf Piles", breakable="Leaf Pile"),
    "Fortress Arena - Pot 1": TunicLocationData("Fortress Arena", breakable="Pot"),
    "Fortress Arena - Pot 2": TunicLocationData("Fortress Arena", breakable="Pot"),
    "Atoll Southwest - Pot 1": TunicLocationData("Ruined Atoll", breakable="Pot"),
    "Atoll Southwest - Pot 2": TunicLocationData("Ruined Atoll", breakable="Pot"),
    "Atoll Southwest - Table": TunicLocationData("Ruined Atoll", breakable="Table"),
    "Atoll near Birds - Explosive Pot": TunicLocationData("Ruined Atoll", breakable="Explosive Pot"),
    "Frog Stairs Upper - Pot 1": TunicLocationData("Frog Stairs Upper", breakable="Pot"),
    "Frog Stairs Upper - Pot 2": TunicLocationData("Frog Stairs Upper", breakable="Pot"),
    "Frog Stairs Upper - Pot 3": TunicLocationData("Frog Stairs Upper", breakable="Pot"),
    "Frog Stairs Upper - Pot 4": TunicLocationData("Frog Stairs Upper", breakable="Pot"),
    "Frog Stairs Upper - Pot 5": TunicLocationData("Frog Stairs Upper", breakable="Pot"),
    "Frog Stairs Upper - Pot 6": TunicLocationData("Frog Stairs Upper", breakable="Pot"),
    "Frog's Domain above Orb Altar - Pot 1": TunicLocationData("Frog's Domain Front", breakable="Pot"),
    "Frog's Domain above Orb Altar - Pot 2": TunicLocationData("Frog's Domain Front", breakable="Pot"),
    "Frog's Domain Side Room - Pot 1": TunicLocationData("Frog's Domain Main", breakable="Pot"),
    "Frog's Domain Side Room - Pot 2": TunicLocationData("Frog's Domain Main", breakable="Pot"),
    "Frog's Domain Side Room - Pot 3": TunicLocationData("Frog's Domain Main", breakable="Pot"),
    "Frog's Domain Main Room - Pot 1": TunicLocationData("Frog's Domain Main", breakable="Pot"),
    "Frog's Domain Main Room - Pot 2": TunicLocationData("Frog's Domain Main", breakable="Pot"),
    "Frog's Domain Side Room - Pot 4": TunicLocationData("Frog's Domain Main", breakable="Pot"),
    "Frog's Domain after Gate - Pot 1": TunicLocationData("Frog's Domain Main", breakable="Pot"),
    "Frog's Domain after Gate - Pot 2": TunicLocationData("Frog's Domain Main", breakable="Pot"),
    "Frog's Domain Orb Room - Explosive Pot 1": TunicLocationData("Frog's Domain Main", breakable="Explosive Pot"),
    "Frog's Domain Orb Room - Explosive Pot 2": TunicLocationData("Frog's Domain Main", breakable="Explosive Pot"),
    "Library Lab - Library Glass 1": TunicLocationData("Library Lab", breakable="Library Glass"),
    "Library Lab - Library Glass 2": TunicLocationData("Library Lab", breakable="Library Glass"),
    "Library Lab - Library Glass 3": TunicLocationData("Library Lab", breakable="Library Glass"),
    "Quarry East - Explosive Pot 1": TunicLocationData("Quarry", breakable="Explosive Pot"),
    "Quarry East - Explosive Pot 2": TunicLocationData("Quarry", breakable="Explosive Pot"),
    "Quarry East - Explosive Pot 3": TunicLocationData("Quarry", breakable="Explosive Pot"),
    "Quarry East beneath Scaffolding - Explosive Pot": TunicLocationData("Quarry", breakable="Explosive Pot"),
    "Quarry Monastery Entry - Explosive Pot 1": TunicLocationData("Quarry Monastery Entry", breakable="Explosive Pot"),
    "Quarry Monastery Entry - Explosive Pot 2": TunicLocationData("Quarry Monastery Entry", breakable="Explosive Pot"),
    "Quarry Back - Pot 1": TunicLocationData("Quarry Back", breakable="Pot"),
    "Quarry Back - Pot 2": TunicLocationData("Quarry Back", breakable="Pot"),
    "Quarry Back - Pot 3": TunicLocationData("Quarry Back", breakable="Pot"),
    "Quarry Back - Pot 4": TunicLocationData("Quarry Back", breakable="Pot"),
    "Quarry Back - Pot 5": TunicLocationData("Quarry Back", breakable="Pot"),
    "Quarry near Shortcut Ladder - Explosive Pot 1": TunicLocationData("Quarry Back", breakable="Explosive Pot"),
    "Quarry near Shortcut Ladder - Explosive Pot 2": TunicLocationData("Quarry Back", breakable="Explosive Pot"),
    "Quarry near Shortcut Ladder - Crate 1": TunicLocationData("Quarry Back", breakable="Crate"),
    "Quarry near Shortcut Ladder - Crate 2": TunicLocationData("Quarry Back", breakable="Crate"),
    "Quarry near Shortcut Ladder - Crate 3": TunicLocationData("Quarry Back", breakable="Crate"),
    "Quarry near Shortcut Ladder - Crate 4": TunicLocationData("Quarry Back", breakable="Crate"),
    "Quarry near Shortcut Ladder - Crate 5": TunicLocationData("Quarry Back", breakable="Crate"),
    "Lower Quarry - Explosive Pot 1": TunicLocationData("Lower Quarry upper pots", breakable="Explosive Pot"),
    "Lower Quarry - Explosive Pot 2": TunicLocationData("Lower Quarry upper pots", breakable="Explosive Pot"),
    "Lower Quarry - Explosive Pot 3": TunicLocationData("Lower Quarry", breakable="Explosive Pot"),
    "Lower Quarry on Scaffolding - Explosive Pot 1": TunicLocationData("Lower Quarry", breakable="Explosive Pot"),
    "Lower Quarry on Scaffolding - Explosive Pot 2": TunicLocationData("Lower Quarry", breakable="Explosive Pot"),
    "Lower Quarry Shooting Range - Crate 1": TunicLocationData("Lower Quarry", breakable="Crate"),
    "Lower Quarry Shooting Range - Crate 2": TunicLocationData("Lower Quarry", breakable="Crate"),
    "Lower Quarry Shooting Range - Crate 3": TunicLocationData("Lower Quarry", breakable="Crate"),
    "Lower Quarry Shooting Range - Crate 4": TunicLocationData("Lower Quarry", breakable="Crate"),
    "Lower Quarry Shooting Range - Crate 5": TunicLocationData("Lower Quarry", breakable="Crate"),
    "Lower Quarry on Scaffolding - Crate 1": TunicLocationData("Lower Quarry", breakable="Crate"),
    "Lower Quarry on Scaffolding - Crate 2": TunicLocationData("Lower Quarry", breakable="Crate"),
    "Lower Quarry on Scaffolding - Crate 3": TunicLocationData("Lower Quarry", breakable="Crate"),
    "Lower Quarry on Scaffolding - Crate 4": TunicLocationData("Lower Quarry", breakable="Crate"),
    "Lower Quarry on Scaffolding - Crate 5": TunicLocationData("Lower Quarry", breakable="Crate"),
    "Even Lower Quarry - Crate 1": TunicLocationData("Even Lower Quarry", breakable="Crate"),
    "Even Lower Quarry - Crate 2": TunicLocationData("Even Lower Quarry", breakable="Crate"),
    "Monastery Back - Crate 1": TunicLocationData("Monastery Back", breakable="Crate"),
    "Monastery Back - Crate 2": TunicLocationData("Monastery Back", breakable="Crate"),
    "Monastery Back - Crate 3": TunicLocationData("Monastery Back", breakable="Crate"),
    "Monastery Back - Crate 4": TunicLocationData("Monastery Back", breakable="Crate"),
    "Monastery Back - Crate 5": TunicLocationData("Monastery Back", breakable="Crate"),
    "Monastery Back - Crate 6": TunicLocationData("Monastery Back", breakable="Crate"),
    "Monastery Back - Crate 7": TunicLocationData("Monastery Back", breakable="Crate"),
    "Monastery Back - Crate 8": TunicLocationData("Monastery Back", breakable="Crate"),
    "Monastery Back - Crate 9": TunicLocationData("Monastery Back", breakable="Crate"),
    "Cathedral - Pot 1": TunicLocationData("Cathedral Main", breakable="Pot"),
    "Cathedral - Pot 2": TunicLocationData("Cathedral Main", breakable="Pot"),
    "Purgatory - Pot 1": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 2": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 3": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 4": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 5": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 6": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 7": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 8": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 9": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 10": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 11": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 12": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 13": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 14": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 15": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 16": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 17": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 18": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 19": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 20": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 21": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 22": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 23": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 24": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 25": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 26": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 27": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 28": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 29": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 30": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 31": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 32": TunicLocationData("Purgatory", breakable="Pot"),
    "Purgatory - Pot 33": TunicLocationData("Purgatory", breakable="Pot"),
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
        if loc_data.breakable == "Leaf Pile":
            set_rule(location, lambda state: can_break_leaf_piles(state, world))
        elif loc_data.breakable in ("Sign", "Table"):
            set_rule(location, lambda state: can_break_signs(state, world))
        else:
            set_rule(location, lambda state: can_break_breakables(state, world))
