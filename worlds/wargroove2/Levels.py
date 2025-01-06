from typing import List, TYPE_CHECKING

from BaseClasses import Region, Entrance, MultiWorld
from .Locations import location_table, Wargroove2Location
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import Wargroove2World

region_names: List[str] = ["North 1", "East 1", "South 1", "West 1",
                           "North 2A", "North 2B", "North 2C",
                           "East 2A", "East 2B", "East 2C",
                           "South 2A", "South 2B", "South 2C",
                           "West 2A", "West 2B", "West 2C",
                           "North 3A", "North 3B", "North 3C",
                           "East 3A", "East 3B", "East 3C",
                           "South 3A", "South 3B", "South 3C",
                           "West 3A", "West 3B", "West 3C"]
FINAL_LEVEL_1 = "Northern Finale"
FINAL_LEVEL_2 = "Eastern Finale"
FINAL_LEVEL_3 = "Southern Finale"
FINAL_LEVEL_4 = "Western Finale"

LEVEL_COUNT = 28
FINAL_LEVEL_COUNT = 4


def set_region_exit_rules(region: Region, world: "Wargroove2World", locations: List[str], operator: str = "or") -> None:
    if operator == "or":
        exit_rule = lambda state: any(
            world.get_location(location).access_rule(state) for location in locations)
    else:
        exit_rule = lambda state: all(
            world.get_location(location).access_rule(state) for location in locations)
    for region_exit in region.exits:
        region_exit.access_rule = exit_rule


class Wargroove2Level:
    name: str
    file_name: str
    location_rules: dict
    region_name: str
    victory_locations: List[str]
    has_ocean: bool = True

    def __init__(self, name: str, file_name: str, location_rules: dict, victory_locations: List[str] = [],
                 has_ocean: bool = True):
        self.name = name
        self.file_name = file_name
        self.location_rules = location_rules
        self.has_ocean = has_ocean
        if victory_locations:
            self.victory_locations = victory_locations
        else:
            self.victory_locations = [name + ': Victory']

    def define_access_rules(self, world: "Wargroove2World", player: int, additional_rule=lambda state: True) -> None:
        for location_name, rule_factory in self.location_rules.items():
            def combined_rule(state, current_rule=rule_factory(player)):
                return current_rule(state) and additional_rule(state)

            set_rule(world.get_location(location_name), combined_rule)
            loc_id = location_table.get(location_name, 0)
            extras = 1
            if loc_id is not None and location_name.endswith("Victory"):
                extras = world.options.victory_locations.value
            elif loc_id is not None:
                extras = world.options.objective_locations.value
            for i in range(1, extras):
                set_rule(world.get_location(location_name + f" Extra {i}"), combined_rule)
        region = world.get_region(self.region_name)
        set_region_exit_rules(region, world, self.victory_locations, operator='and')

    def define_region(self, name: str, multiworld: MultiWorld, player: int, exits=None) -> Region:
        self.region_name = name
        region = Region(name, player, multiworld)
        if self.location_rules.keys():
            for location in self.location_rules.keys():
                loc_id = location_table.get(location, 0)
                wg2_location = Wargroove2Location(player, location, loc_id, region)
                region.locations.append(wg2_location)
                extras = 1
                if loc_id is not None and location.endswith("Victory"):
                    extras = multiworld.worlds[player].options.victory_locations.value
                elif loc_id is not None:
                    extras = multiworld.worlds[player].options.objective_locations.value
                for i in range(1, extras):
                    extra_location = location + f" Extra {i}"
                    loc_id = location_table.get(extra_location, 0)
                    wg2_location = Wargroove2Location(player, extra_location, loc_id, region)
                    region.locations.append(wg2_location)

        if exits:
            for exit in exits:
                region.exits.append(Entrance(player, f"{name} exits to {exit}", region))

        return region


high_victory_checks_levels = [
    Wargroove2Level(
        name="Cherrystone Landing",
        file_name="Cherrystone_Landing.json",
        location_rules={
            "Cherrystone Landing: Victory": lambda player: lambda
                state: state.has_all(["Warship", "Barge", "Landing Event"], player),
            "Cherrystone Landing: Smacked a Trebuchet": lambda player: lambda
                state: state.has_all(["Warship", "Barge", "Landing Event", "Golem"], player),
            "Cherrystone Landing: Smacked a Fortified Village": lambda player: lambda
                state: state.has_all(["Barge", "Landing Event", "Golem"], player)
        }
    ),
    Wargroove2Level(
        name="Spire Fire",
        file_name="Spire_Fire.json",
        location_rules={
            "Spire Fire: Victory": lambda player: lambda state: state.has_any(["Mage", "Witch"], player),
            "Spire Fire: Kill Enemy Sky Rider": lambda player: lambda state: state.has("Witch", player),
            "Spire Fire: Win without losing your Dragon": lambda player: lambda state: state.has_any(["Mage", "Witch"], player)
        },
        has_ocean=False
    ),
    Wargroove2Level(
        name="Nuru's Vengeance",
        file_name="Nuru_Vengeance.json",
        location_rules={
            "Nuru's Vengeance: Victory": lambda player: lambda state: state.has("Knight", player),
            "Nuru's Vengeance: Defeat all Dogs": lambda player: lambda state: state.has("Knight", player),
            "Nuru's Vengeance: Spearman Destroys the Gate": lambda player: lambda
                state: state.has_all(["Knight", "Spearman"], player)
        },
        has_ocean=False
    ),
    Wargroove2Level(
        name="Slippery Bridge",
        file_name="Slippery_Bridge.json",
        location_rules={
            "Slippery Bridge: Victory": lambda player: lambda state: state.has("Frog", player),
            "Slippery Bridge: Control all Sea Villages": lambda player: lambda state:
            state.has("Merfolk", player),
        }
    ),
    Wargroove2Level(
        name="Den-Two-Away",
        file_name="Den-Two-Away.json",
        location_rules={
            "Den-Two-Away: Victory": lambda player: lambda state: state.has("Harpy", player),
            "Den-Two-Away: Commander Captures the Lumbermill": lambda player: lambda
                state: state.has_all(["Harpy", "Balloon"], player),
        }
    ),
    Wargroove2Level(
        name="Skydiving",
        file_name="Skydiving.json",
        location_rules={
            "Skydiving: Victory": lambda player: lambda state: state.has_all(["Balloon", "Airstrike Event"], player),
            "Skydiving: Dragon Defeats Stronghold": lambda player: lambda
                state: state.has_all(["Balloon", "Airstrike Event", "Dragon"], player),
        },
        has_ocean=False
    ),
    Wargroove2Level(
        name="Sunken Forest",
        file_name="Sunken_Forest.json",
        location_rules={
            "Sunken Forest: Victory": lambda player: lambda state: state.has_any(["Mage", "Harpoon Ship"], player),
            "Sunken Forest: High Ground": lambda player: lambda state: state.has("Archer", player),
            "Sunken Forest: Coastal Siege": lambda player: lambda state:
                state.has("Warship", player) and state.has_any(["Mage", "Harpoon Ship"], player),
        }
    ),
    Wargroove2Level(
        name="Tenri's Mistake",
        file_name="Tenris_Mistake.json",
        location_rules={
            "Tenri's Mistake: Victory": lambda player: lambda state: state.has_any(
                ["Balloon", "Air Trooper"], player),
            "Tenri's Mistake: Mighty Barracks": lambda player: lambda
                state: state.has_any(["Balloon", "Air Trooper"], player),
            "Tenri's Mistake: Commander Arrives": lambda player: lambda state: state.has("Balloon", player),
        }
    ),
    Wargroove2Level(
        name="Enmity Cliffs",
        file_name="Enmity_Cliffs.json",
        location_rules={
            "Enmity Cliffs: Victory": lambda player: lambda state: state.has_all(["Spearman", "Bridges Event"], player),
            "Enmity Cliffs: Spear Flood": lambda player: lambda state: state.has("Spearman", player),
            "Enmity Cliffs: Across the Gap": lambda player: lambda state: state.has_any(["Archer", "Rifleman"], player),
        },
        has_ocean=False
    ),
    Wargroove2Level(
        name="Terrible Tributaries",
        file_name="Terrible_Tributaries.json",
        location_rules={
            "Terrible Tributaries: Victory": lambda player: lambda state: state.has(
                "River Boat", player),
            "Terrible Tributaries: Swimming Knights": lambda player: lambda
                state: state.has_all(["Merfolk", "River Boat"], player),
            "Terrible Tributaries: Steal Code Names": lambda player: lambda
                state: state.has_all(["Thief", "River Boat"], player),
        }
    ),
    Wargroove2Level(
        name="Beached",
        file_name="Beached.json",
        location_rules={
            "Beached: Victory": lambda player: lambda state: state.has("Knight", player),
            "Beached: Turtle Power": lambda player: lambda state: state.has_all(["Turtle", "Knight"], player),
            "Beached: Happy Turtle": lambda player: lambda state: state.has_all(["Turtle", "Knight"], player),
        }
    ),
    Wargroove2Level(
        name="Portal Peril",
        file_name="Portal_Peril.json",
        location_rules={
            "Portal Peril: Victory": lambda player: lambda state: state.has("Wagon", player),
            "Portal Peril: Unleash the Hounds": lambda player: lambda state: state.has("Wagon", player),
            "Portal Peril: Overcharged": lambda player: lambda state: state.has("Wagon", player),
        },
        has_ocean=False
    ),
    Wargroove2Level(
        name="Riflemen Blockade",
        file_name="Riflemen_Blockade.json",
        location_rules={
            "Riflemen Blockade: Victory": lambda player: lambda state: state.has("Rifleman", player),
            "Riflemen Blockade: From the Mountains": lambda player: lambda
                state: state.has_all(["Rifleman", "Harpy"], player),
            "Riflemen Blockade: To the Road": lambda player: lambda
                state: state.has_all(["Rifleman", "Dragon"], player),
        },
        has_ocean=False
    ),
    Wargroove2Level(
        name="Towers of the Abyss",
        file_name="Towers_of_the_Abyss.json",
        location_rules={
            "Towers of the Abyss: Victory": lambda player: lambda state: state.has("Ballista", player),
            "Towers of the Abyss: Siege Master": lambda player: lambda state:
            state.has_all(["Ballista", "Trebuchet"], player),
            "Towers of the Abyss: Perfect Defense": lambda player: lambda state:
            state.has_all(["Ballista", "Walls Event"], player),
        },
        has_ocean=False
    ),
    Wargroove2Level(
        name="Kraken Strait",
        file_name="Kraken_Strait.json",
        location_rules={
            "Kraken Strait: Victory": lambda player: lambda state: state.has_all(["Frog", "Kraken"], player),
            "Kraken Strait: Well Defended": lambda player: lambda state: state.has_all(["Frog", "Kraken"], player),
            "Kraken Strait: Clipped Wings": lambda player: lambda state: state.has("Harpoon Ship", player),
        }
    ),
    Wargroove2Level(
        name="Gnarled Mountaintop",
        file_name="Gnarled_Mountaintop.json",
        location_rules={
            "Gnarled Mountaintop: Victory": lambda player: lambda state: state.has("Harpy", player),
            "Gnarled Mountaintop: Watch the Watchtower": lambda player: lambda state: state.has("Harpy", player),
            "Gnarled Mountaintop: Vine Skip": lambda player: lambda state: state.has("Air Trooper", player),
        },
        has_ocean=False
    ),
    Wargroove2Level(
        name="Gold Rush",
        file_name="Gold_Rush.json",
        location_rules={
            "Gold Rush: Victory": lambda player: lambda state: state.has("Thief", player) and
                                                                            state.has_any(
                                                                                ["Rifleman", "Merfolk", "Warship"],
                                                                                player),
            "Gold Rush: Lumber Island": lambda player: lambda state: state.has_any(
                ["Merfolk", "River Boat", "Barge"], player),
            "Gold Rush: Starglass Rush": lambda player: lambda state: state.has_any(
                ["River Boat", "Barge"], player),
        }
    ),
    Wargroove2Level(
        name="Finishing Blow",
        file_name="Finishing_Blow.json",
        location_rules={
            "Finishing Blow: Victory": lambda player: lambda state: state.has("Witch", player),
            "Finishing Blow: Mass Destruction": lambda player: lambda state: state.has("Witch", player),
            "Finishing Blow: Defortification": lambda player: lambda state: state.has("Thief", player),
        }
    ),
    Wargroove2Level(
        name="Frantic Inlet",
        file_name="Frantic_Inlet.json",
        location_rules={
            "Frantic Inlet: Victory": lambda player: lambda state: state.has(
                "Turtle", player) and state.has_any(["Barge", "Knight"], player),
            "Frantic Inlet: Plug the Gap": lambda player: lambda state: state.has("Spearman", player),
            "Frantic Inlet: Portal Detour": lambda player: lambda
                state: state.has_all(["Turtle", "Barge"], player),
        }
    ),
    Wargroove2Level(
        name="Operation Seagull",
        file_name="Operation_Seagull.json",
        location_rules={
            "Operation Seagull: Victory": lambda player: lambda state: state.has(
                "Merfolk", player) and state.has_any(["Harpoon Ship", "Witch"], player) and state.has_any(
                ["Turtle", "Harpy"], player),
            "Operation Seagull: Crack the Crystal": lambda player: lambda
                state: state.has_any(["Warship", "Kraken"], player),
            "Operation Seagull: Counter Break": lambda player: lambda
                state: state.has("Dragon", player) and
                             state.has_all(["Harpoon Ship", "Witch"], player),
        }
    ),
    Wargroove2Level(
        name="Air Support",
        file_name="Air_Support.json",
        location_rules={
            "Air Support: Victory": lambda player: lambda state: state.has_all(["Dragon", "Bridges Event"], player),
            "Air Support: Roadkill": lambda player: lambda state: state.has_all(["Dragon", "Bridges Event"], player),
            "Air Support: Flight Economy": lambda player: lambda
                state: state.has_all(["Air Trooper", "Bridges Event"], player),
        }
    ),
    Wargroove2Level(
        name="Fortification",
        file_name="Fortification.json",
        location_rules={
            "Fortification: Victory": lambda player: lambda state: state.has_all(
                ["Golem", "Walls Event"], player) and state.has_any(["Archer", "Trebuchet"], player),
            "Fortification: Hyper Repair": lambda player: lambda state: state.has_all(["Golem", "Walls Event"], player),
            "Fortification: Defensive Artillery": lambda player: lambda state: state.has("Trebuchet", player),
        },
        has_ocean=False
    ),
    Wargroove2Level(
        name="A Ribbitting Time",
        file_name="A_Ribbitting_Time.json",
        location_rules={
            "A Ribbitting Time: Victory": lambda player: lambda state: state.has("Frog", player),
            "A Ribbitting Time: Leap Frog": lambda player: lambda state: state.has("Frog", player),
            "A Ribbitting Time: Frogway Robbery": lambda player: lambda state: state.has_all(["Frog", "Thief"], player),
        }
    ),
    Wargroove2Level(
        name="Precarious Cliffs",
        file_name="Precarious_Cliffs.json",
        location_rules={
            "Precarious Cliffs: Victory": lambda player: lambda state: state.has_all(
                ["Airstrike Event", "Archer"], player),
            "Precarious Cliffs: No Crit for You": lambda player: lambda state: state.has("Airstrike Event", player),
            "Precarious Cliffs: Out Ranged": lambda player: lambda
                state: state.has_all(["Airstrike Event", "Archer"], player),
        },
        has_ocean=False
    ),
    Wargroove2Level(
        name="Split Valley",
        file_name="Split_Valley.json",
        location_rules={
            "Split Valley: Victory": lambda player: lambda state: state.has(
                "Trebuchet", player) and state.has_any(["Bridges Event", "Air Trooper"], player),
            "Split Valley: Longshot": lambda player: lambda state: state.has("Trebuchet", player),
            "Split Valley: Ranged Trinity": lambda player: lambda
                state: state.has_all(["Trebuchet", "Archer", "Ballista"], player),
        }
    ),
    Wargroove2Level(
        name="Bridge Brigade",
        file_name="Bridge_Brigade.json",
        location_rules={
            "Bridge Brigade: Victory": lambda player: lambda state: state.has_all(["Warship", "Spearman"], player),
            "Bridge Brigade: From the Depths": lambda player: lambda state: state.has("Kraken", player),
            "Bridge Brigade: Back to the Depths": lambda player: lambda state:
            state.has_all(["Warship", "Spearman", "Kraken"], player),
        },
        has_ocean=False
    ),
    Wargroove2Level(
        name="Grand Theft Village",
        file_name="Grand_Theft_Village.json",
        location_rules={
            "Grand Theft Village: Victory": lambda player: lambda state: state.has(
                "Thief", player) and state.has_any(["Mage", "Ballista"], player),
            "Grand Theft Village: Stand Tall": lambda player: lambda state: state.has("Golem", player),
            "Grand Theft Village: Pillager": lambda player: lambda state: True,
        },
        has_ocean=False
    ),
    Wargroove2Level(
        name="Wagon Freeway",
        file_name="Wagon_Freeway.json",
        location_rules={
            "Wagon Freeway: Victory": lambda player: lambda state: state.has_all(["Wagon", "Spearman"], player),
            "Wagon Freeway: All Mine Now": lambda player: lambda state: True,
            "Wagon Freeway: Pigeon Carrier": lambda player: lambda state: state.has("Air Trooper", player),
        },
        has_ocean=False
    ),
]

final_levels = [
    Wargroove2Level(
        name="Disastrous Crossing",
        file_name="Disastrous_Crossing.json",
        location_rules={"Disastrous Crossing: Victory":
                            lambda player: lambda state: state.has_any(
                                ["Merfolk", "River Boat"], player) and
                                                                      state.has_any(
                                                                          ["Knight", "Kraken"],
                                                                          player)}
    ),
    Wargroove2Level(
        name="Dark Mirror",
        file_name="Dark_Mirror.json",
        location_rules={
            "Dark Mirror: Victory": lambda player: lambda state: state.has(
                "Archer", player) and state.has_any(["Mage", "Ballista"], player) and state.has_any(
                ["Harpy", "Dragon"], player)},
        has_ocean=False
    ),
    Wargroove2Level(
        name="Doomed Metropolis",
        file_name="Doomed_Metropolis.json",
        location_rules={
            "Doomed Metropolis: Victory": lambda player: lambda state: state.has_all(["Mage", "Knight"], player)},
        has_ocean=False
    ),
    Wargroove2Level(
        name="Dementia Castle",
        file_name="Dementia_Castle.json",
        location_rules={"Dementia Castle: Victory":
                            lambda player: lambda state: state.has_all(["Merfolk", "Mage", "Golem", "Harpy"], player)}
    ),
]

low_victory_checks_levels = [

    Wargroove2Level(
        name="Swimming at the Docks",
        file_name="Swimming_at_the_Docks.json",
        location_rules={
            "Swimming at the Docks: Victory": lambda player: lambda state: True,
            "Swimming at the Docks: Dogs Counter Knights": lambda player: lambda state: True,
            "Swimming at the Docks: Kayaking": lambda player: lambda state: state.has("River Boat", player),
        }
    ),
    Wargroove2Level(
        name="Ancient Discoveries",
        file_name="Ancient_Discoveries.json",
        location_rules={
            "Ancient Discoveries: Victory": lambda player: lambda state: True,
            "Ancient Discoveries: So many Choices": lambda player: lambda state: True,
            "Ancient Discoveries: Height Advantage": lambda player: lambda state: state.has("Golem", player),
        }
    ),
    Wargroove2Level(
        name="Observation Isle",
        file_name="Observation_Isle.json",
        location_rules={
            "Observation Isle: Victory": lambda player: lambda state: True,
            "Observation Isle: Become the Watcher": lambda player: lambda state: True,
            "Observation Isle: Execute the Watcher": lambda player: lambda state: state.has("Walls Event", player),
        }
    ),
    Wargroove2Level(
        name="Majestic Mountain",
        file_name="Majestic_Mountain.json",
        location_rules={
            "Majestic Mountain: Victory": lambda player: lambda state: True,
            "Majestic Mountain: Mountain Climbing": lambda player: lambda state: True,
            "Majestic Mountain: Legend of the Mountains": lambda player: lambda state: state.has("Air Trooper", player),
        }
    ),
]

first_level = Wargroove2Level(
    name="Humble Beginnings Rebirth",
    file_name="",
    location_rules={
        "Humble Beginnings Rebirth: Victory": lambda player: lambda state: True,
        "Humble Beginnings Rebirth: Talk to Nadia": lambda player: lambda state: True,
        "Humble Beginnings Rebirth: Good Dog": lambda player: lambda state: True
    }
)
