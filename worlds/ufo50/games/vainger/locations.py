from typing import TYPE_CHECKING, Dict, NamedTuple, Set, Optional
from BaseClasses import Region, ItemClassification, Item, Location
from worlds.generic.Rules import add_rule

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World

# adapted from Barbuta, thanks Scipio! <3


class LocationInfo(NamedTuple):
    id_offset: Optional[int]
    region_name: str


# the letter is the column (left to right), the number is the row (top to bottom)
# based on a map at https://steamcommunity.com/sharedfiles/filedetails/?id=3341323146
# except numbering each sector from 1 to 10.
location_table: Dict[str, LocationInfo] = {
    "LatomR4C1 - Shield Upgrade": LocationInfo(0, "LatomR3C4 Genepod"),
    "LatomR7C1 - Shield Upgrade": LocationInfo(1, "LatomR3C4 Genepod"),
    "LatomR9C1 - Shield Upgrade": LocationInfo(2, "LatomR9C3 Genepod"),
    "LatomR9C2 - Shield Upgrade": LocationInfo(3, "LatomR9C3 Genepod"),
    "LatomR4C3 - Shield Upgrade": LocationInfo(4, "LatomR6C3 Genepod"),
    "LatomR6C3 - Clone Material": LocationInfo(5, "LatomR6C3 Genepod"),
    "LatomR5C4 - Key Code": LocationInfo(6, "LatomR5C4 Genepod"),
    "LatomR6C4 - Security Clearance": LocationInfo(7, "LatomR6C4 Area"),
    "LatomR4C5 - Shield Upgrade": LocationInfo(8, "LatomR5C6 Genepod"),
    "LatomR8C7 - Multi Mod": LocationInfo(9, "LatomR7C6 Genepod"),
    "LatomR4C9 - Pulse Mod": LocationInfo(10, "LatomR4C9 Genepod"),
    # TODO: does this need to be R4C9 instead due to the miniboss?
    "LatomR1C10 - Stabilizer": LocationInfo(11, "LatomR5C6 Genepod"),
    "LatomR3C10 - Shield Upgrade": LocationInfo(12, "LatomR5C6 Genepod"),  # do it from R5C6 to avoid the issues with R4C9
    "LatomR10C10 - Shield Upgrade": LocationInfo(13, "LatomR9C3 Genepod"),

    "LatomR5C4 - Boss Defeated": LocationInfo(None, "LatomR6C3 Genepod"),  # alien?

    "ThetaR2C1 - Clone Material": LocationInfo(100, "ThetaR4C1 Genepod"),
    "ThetaR3C1 - Shield Upgrade": LocationInfo(101, "ThetaR4C1 Genepod"),
    "ThetaR9C1 - Shield Upgrade": LocationInfo(102, "VerdeR1C1 Genepod"),
    "ThetaR5C3 - Clone Material": LocationInfo(103, "ThetaR4C1 Genepod"),
    # the logic is different approaching these two from the left or the right.
    # I don't think it matters because both sides require hot-shot and heat mod is the only barrier to circling around?
    # but I'm going to express the difference anyway.
    "ThetaR8C3 - Shield Upgrade": LocationInfo(104, "ThetaR8C3 Location"),
    "ThetaR10C3 - Shield Upgrade": LocationInfo(105, "ThetaR10C3 Location"),
    "ThetaR7C4 - Shield Upgrade": LocationInfo(106, "ThetaR4C1 Genepod"),
    "ThetaR9C5 - Key Code": LocationInfo(107, "ThetaR9C5 Genepod"),
    "ThetaR1C8 - Shield Upgrade": LocationInfo(108, "ThetaR7C9 Genepod"),
    "ThetaR4C8 - Heat Mod": LocationInfo(109, "ThetaR7C9 Genepod"),
    "ThetaR4C9 - Shield Upgrade": LocationInfo(110, "ThetaR7C9 Genepod"),
    "ThetaR7C10 - Shield Upgrade": LocationInfo(111, "ThetaR7C9 Genepod"),

    "ThetaR9C5 - Boss Defeated": LocationInfo(None, "ThetaR6C6 Genepod"),  # I have no memory of this one lol

    "VerdeR1C1 - Shield Upgrade": LocationInfo(200, "VerdeR1C1 Genepod"),
    "VerdeR5C2 - Force Mod": LocationInfo(201, "VerdeSW Area"),
    "VerdeR4C3 - Shield Upgrade": LocationInfo(202, "VerdeR1C1 Genepod"),
    "VerdeR5C3 - Shield Upgrade": LocationInfo(203, "VerdeSW Area"),
    "VerdeR1C5 - Key Code": LocationInfo(204, "VerdeR1C5 Genepod"),
    "VerdeR5C5 - Security Clearance": LocationInfo(205, "VerdeSW Area"),
    "VerdeR8C6 - Shield Upgrade": LocationInfo(206, "VerdeSW Area"),
    "VerdeR5C7 - Shield Upgrade": LocationInfo(207, "VerdeR7C9 Genepod"),
    "VerdeR10C7 - Security Clearance": LocationInfo(208, "VerdeR7C9 Genepod"),
    # need a separate region to account for the fact that the heat armor damage boost is only possible from the right
    "VerdeR7C8 - Shield Upgrade": LocationInfo(209, "VerdeR7C8 Location"),
    "VerdeR4C9 - Shield Upgrade": LocationInfo(210, "VerdeR7C9 Genepod"),
    "VerdeR9C9 - Key Code": LocationInfo(211, "VerdeR9C9 Genepod"),
    "VerdeR2C10 - Stabilizer": LocationInfo(212, "VerdeR7C9 Genepod"),
    "VerdeR9C10 - Shield Upgrade": LocationInfo(213, "VerdeR7C9 Genepod"),

    "VerdeR1C5 - Ramses Defeated": LocationInfo(None, "VerdeR1C1 Genepod"),
    "VerdeR9C9 - Sura Defeated": LocationInfo(None, "VerdeSW Area"),  # This might be Jorgensen, not Sura
    
    "Control - Shield Upgrade": LocationInfo(300, "Control Genepod"),

    "Control - Hooper Defeated": LocationInfo(None, "Control Genepod"),

    "Garden": LocationInfo(997, "ThetaR7C9 Genepod"),  # for now it's a clone of the heat mod location.
    "Gold": LocationInfo(998, "Control Genepod"),
    "Cherry": LocationInfo(999, "Control Genepod")
}


def get_locations() -> Dict[str, int]:
    return {f"Vainger - {name}": data.id_offset + get_game_base_id("Vainger") for name, data in location_table.items()
            if data.id_offset is not None}


def get_location_groups() -> Dict[str, Set[str]]:
    location_groups: Dict[str, Set[str]] = {"Vainger": {f"Vainger - {loc_name}" for loc_name, loc_data in location_table.items()
                                                        if loc_data.id_offset is not None}}
    return location_groups


def create_locations(world: "UFO50World", regions: Dict[str, Region]) -> None:
    for loc_name, loc_data in location_table.items():
        if loc_name == "Cherry" and "Vainger" not in world.options.cherry_allowed_games:
            break
        region = regions[f"Vainger - {loc_data.region_name}"]
        if loc_name in ["Gold", "Cherry"] and "Vainger" in world.goal_games:
            if (loc_name == "Gold" and "Vainger" not in world.options.cherry_allowed_games) or loc_name == "Cherry":
                loc = Location(world.player, f"Vainger - {loc_name}", None, region)
                loc.place_locked_item(Item("Completed Vainger", ItemClassification.progression, None, world.player))
                add_rule(world.get_location("Completed All Games"), lambda state: state.has("Completed Vainger", world.player))
                region.locations.append(loc)
                break

        loc = Location(world.player, f"Vainger - {loc_name}",
                       loc_data.id_offset + get_game_base_id("Vainger") if loc_data.id_offset is not None else None, region)
        if loc_data.id_offset is None:      # this is an event location
            loc.place_locked_item(Item(f"Vainger - {loc_name}", ItemClassification.progression, None,
                                       world.player))
        region.locations.append(loc)
