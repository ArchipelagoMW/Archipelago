from dataclasses import dataclass
from typing import Callable, Dict, Optional, Set, Union

from BaseClasses import Location, MultiWorld
from .Items import RLItem, item_table

__all__ = ["RLLocation", "RLLocationData", "location_groups", "location_table"]

LOCATION_ID_OFFSET = 91_000


def always_create(multiworld: MultiWorld, player: int) -> bool:
    return True


def get_chest_region(chests_per_zone: int, current_index: int) -> str:
    """Returns the correct region name for this chest, assuming universal chests are enabled."""
    if current_index < chests_per_zone:
        return "Castle Hamson"
    elif current_index < chests_per_zone * 2:
        return "Forest Abkhazia"
    elif current_index < chests_per_zone * 3:
        return "The Maya"
    else:
        return "The Land of Darkness"


def can_create_normal_chest(multiworld: MultiWorld, player: int, index: int):
    """Returns if it's possible to create this normal chest location during generation."""
    if getattr(multiworld, "universal_chests")[player]:
        return False

    return getattr(multiworld, "chests_per_zone")[player] > index


def can_create_universal_chest(multiworld: MultiWorld, player: int, index: int):
    """Returns if it's possible to create this universal chest location during generation."""
    if not getattr(multiworld, "universal_chests")[player]:
        return False

    return getattr(multiworld, "chests_per_zone")[player] * 4 > index


def can_create_normal_fairy_chest(multiworld: MultiWorld, player: int, index: int):
    """Returns if it's possible to create this normal fairy chest location during generation."""
    if getattr(multiworld, "universal_fairy_chests")[player]:
        return False

    return getattr(multiworld, "fairy_chests_per_zone")[player] > index


def can_create_universal_fairy_chest(multiworld: MultiWorld, player: int, index: int):
    """Returns if it's possible to create this universal fairy chest location during generation."""
    if not getattr(multiworld, "universal_fairy_chests")[player]:
        return False

    return getattr(multiworld, "fairy_chests_per_zone")[player] * 4 > index


def get_castle_boss(multiworld: MultiWorld, player: int) -> str:
    if getattr(multiworld, "khidr")[player] == "challenge":
        return "Defeat Neo Khidr"

    return "Defeat Khidr"


def get_forest_boss(multiworld: MultiWorld, player: int) -> str:
    if getattr(multiworld, "alexander")[player] == "challenge":
        return "Defeat Alexander IV"

    return "Defeat Alexander"


def get_tower_boss(multiworld: MultiWorld, player: int) -> str:
    if getattr(multiworld, "leon")[player] == "challenge":
        return "Defeat Ponce de Freon"

    return "Defeat Ponce de Leon"


def get_dungeon_boss(multiworld: MultiWorld, player: int) -> str:
    if getattr(multiworld, "herodotus")[player] == "challenge":
        return "Defeat Astrodotus"

    return "Defeat Herodotus"


def get_final_boss(multiworld: MultiWorld, player: int) -> str:
    return "Defeat The Fountain"


def get_open_door(multiworld: MultiWorld, player: int) -> str:
    return "Open Fountain Room Door"


class RLLocation(Location):
    game: str = "Rogue Legacy"


@dataclass
class RLLocationData:
    """A collection of metadata for each location prior to creation into an RLLocation."""
    name: str
    region: Union[str, Callable[[MultiWorld, int], str]]
    address: Optional[int]
    can_create: Callable[[MultiWorld, int], bool]
    locked_item: Optional[Callable[[MultiWorld, int], str]]

    def __init__(
            self,
            region: Union[str, Callable[[MultiWorld, int], str]],
            address: Optional[int] = None,
            can_create: Callable[[MultiWorld, int], bool] = always_create,
            locked_item: Optional[Callable[[MultiWorld, int], str]] = None):
        self.region = region
        self.address = address + LOCATION_ID_OFFSET if address is not None else None
        self.can_create = can_create
        self.locked_item = locked_item

    @property
    def event(self) -> bool:
        """Returns True if this is an event location."""
        return self.address is None

    def create_location(self, multiworld: MultiWorld, player: int):
        """Creates the location from its location metadata and place in its appropriate region."""
        # Get region name.
        if isinstance(self.region, str):
            region = multiworld.get_region(self.region, player)
        else:
            region = multiworld.get_region(self.region(multiworld, player), player)

        # Create location and place.
        location = RLLocation(player, self.name, self.address, region)
        region.locations.append(location)

        # If a location must contain a locked item, create and place that item.
        if self.locked_item:
            item_name = self.locked_item(multiworld, player)
            item_data = item_table[item_name]
            location.place_locked_item(RLItem(item_name, item_data.classification, item_data.code, player))


location_groups: Dict[str, Set[str]] = {
    "Boss Rewards": {
        "Castle Hamson - Boss Reward",
        "Forest Abkhazia - Boss Reward",
        "The Maya - Boss Reward",
        "Land of Darkness - Boss Reward",
    },
    "Mini Boss Rewards": {
        "Barbatos & Amon's Reward",   
        "Botis' Reward",              
        "Stolas & Focalor's Reward",  
        "Sallos' Reward",             
        "Berith & Halphas' Reward",   
    },
    "Manor Renovations": {
        "Manor - Ground Road",          
        "Manor - Main Base",            
        "Manor - Main Bottom Window",   
        "Manor - Main Top Window",      
        "Manor - Main Rooftop",         
        "Manor - Left Wing Base",       
        "Manor - Left Wing Window",     
        "Manor - Left Wing Rooftop",    
        "Manor - Left Big Base",        
        "Manor - Left Big Upper 1",     
        "Manor - Left Big Upper 2",     
        "Manor - Left Big Windows",     
        "Manor - Left Big Rooftop",     
        "Manor - Left Far Base",        
        "Manor - Left Far Roof",        
        "Manor - Left Extension",       
        "Manor - Left Tree 1",          
        "Manor - Left Tree 2",          
        "Manor - Right Wing Base",      
        "Manor - Right Wing Window",    
        "Manor - Right Wing Rooftop",   
        "Manor - Right Big Base",       
        "Manor - Right Big Upper",      
        "Manor - Right Big Rooftop",    
        "Manor - Right High Base",      
        "Manor - Right High Upper",     
        "Manor - Right High Tower",     
        "Manor - Right Extension",      
        "Manor - Right Tree",           
        "Manor - Observatory Base",     
        "Manor - Observatory Telescope",
    },
    "Secret Room": {
        "Secret Room Left Chest",
        "Secret Room Right Chest",
    },
}

location_table: Dict[str, RLLocationData] = {
    # Manor Renovation
    "Manor - Ground Road":                      RLLocationData("Manor - Tier 1",         0),
    "Manor - Main Base":                        RLLocationData("Manor - Tier 1",         1),
    "Manor - Main Bottom Window":               RLLocationData("Manor - Tier 1",         2),
    "Manor - Main Top Window":                  RLLocationData("Manor - Tier 1",         3),
    "Manor - Main Rooftop":                     RLLocationData("Manor - Tier 1",         4),
    "Manor - Left Wing Base":                   RLLocationData("Manor - Tier 1",         5),
    "Manor - Left Wing Window":                 RLLocationData("Manor - Tier 2",         6),
    "Manor - Left Wing Rooftop":                RLLocationData("Manor - Tier 2",         7),
    "Manor - Left Big Base":                    RLLocationData("Manor - Tier 2",         8),
    "Manor - Left Big Upper 1":                 RLLocationData("Manor - Tier 3",         9),
    "Manor - Left Big Upper 2":                 RLLocationData("Manor - Tier 3",        10),
    "Manor - Left Big Windows":                 RLLocationData("Manor - Tier 3",        11),
    "Manor - Left Big Rooftop":                 RLLocationData("Manor - Tier 3",        12),
    "Manor - Left Far Base":                    RLLocationData("Manor - Tier 3",        13),
    "Manor - Left Far Roof":                    RLLocationData("Manor - Tier 3",        14),
    "Manor - Left Extension":                   RLLocationData("Manor - Tier 3",        15),
    "Manor - Left Tree 1":                      RLLocationData("Manor - Tier 2",        16),
    "Manor - Left Tree 2":                      RLLocationData("Manor - Tier 2",        17),
    "Manor - Right Wing Base":                  RLLocationData("Manor - Tier 1",        18),
    "Manor - Right Wing Window":                RLLocationData("Manor - Tier 2",        19),
    "Manor - Right Wing Rooftop":               RLLocationData("Manor - Tier 2",        20),
    "Manor - Right Big Base":                   RLLocationData("Manor - Tier 2",        21),
    "Manor - Right Big Upper":                  RLLocationData("Manor - Tier 3",        22),
    "Manor - Right Big Rooftop":                RLLocationData("Manor - Tier 3",        23),
    "Manor - Right High Base":                  RLLocationData("Manor - Tier 4",        24),
    "Manor - Right High Upper":                 RLLocationData("Manor - Tier 4",        25),
    "Manor - Right High Tower":                 RLLocationData("Manor - Tier 4",        26),
    "Manor - Right Extension":                  RLLocationData("Manor - Tier 3",        27),
    "Manor - Right Tree":                       RLLocationData("Manor - Tier 2",        28),
    "Manor - Observatory Base":                 RLLocationData("Manor - Tier 4",        29),
    "Manor - Observatory Telescope":            RLLocationData("Manor - Tier 4",        30),

    # Boss Rewards
    "Castle Hamson - Boss Reward":              RLLocationData("Castle Hamson",        100),
    "Forest Abkhazia - Boss Reward":            RLLocationData("Forest Abkhazia",      102),
    "The Maya - Boss Reward":                   RLLocationData("The Maya",             104),
    "Land of Darkness - Boss Reward":           RLLocationData("The Land of Darkness", 106),

    # One-off Locations
    "The Jukebox":                              RLLocationData("Castle Hamson",        200),
    "CDG Portrait":                             RLLocationData("Castle Hamson",        201),
    "Cheapskate Elf's Reward":                  RLLocationData("Cheapskate Elf",       202),
    "Carnival Reward":                          RLLocationData("Castle Hamson",        203),
    "Secret Room Left Chest":                   RLLocationData("The Secret Room",      204),
    "Secret Room Right Chest":                  RLLocationData("The Secret Room",      205),
    "Barbatos & Amon's Reward":                 RLLocationData("Castle Hamson",        206),
    "Botis' Reward":                            RLLocationData("Castle Hamson",        207),
    "Stolas & Focalor's Reward":                RLLocationData("Castle Hamson",        208),
    "Sallos' Reward":                           RLLocationData("Castle Hamson",        209),
    "Berith & Halphas' Reward":                 RLLocationData("Castle Hamson",        210),

    # Diaries
    **{f"Diary Entry {i+1}":                    RLLocationData("Castle Hamson",        300+i) for i in range(0,   6)},
    **{f"Diary Entry {i+1}":                    RLLocationData("Forest Abkhazia",      300+i) for i in range(6,  12)},
    **{f"Diary Entry {i+1}":                    RLLocationData("The Maya",             300+i) for i in range(12, 18)},
    **{f"Diary Entry {i+1}":                    RLLocationData("The Land of Darkness", 300+i) for i in range(18, 24)},
    "The Final Diary Entry":                    RLLocationData("The Fountain Room",    324),

    # Chests
    **{f"Castle Hamson - Chest {i+1}":          RLLocationData(
        "Castle Hamson",
        600+i,
        lambda multiworld, player, i=i: can_create_normal_chest(multiworld, player, i),
    ) for i in range(50)},
    **{f"Forest Abkhazia - Chest {i+1}":        RLLocationData(
        "Forest Abkhazia",
        700+i,
        lambda multiworld, player, i=i: can_create_normal_chest(multiworld, player, i),
    ) for i in range(50)},
    **{f"The Maya - Chest {i+1}":               RLLocationData(
        "The Maya",
        800+i,
        lambda multiworld, player, i=i: can_create_normal_chest(multiworld, player, i),
    ) for i in range(50)},
    **{f"Land of Darkness - Chest {i+1}":       RLLocationData(
        "The Land of Darkness",
        900+i,
        lambda multiworld, player, i=i: can_create_normal_chest(multiworld, player, i),
    ) for i in range(50)},
    **{f"Universal Chest {i+1}":                RLLocationData(
        lambda multiworld, player, i=i: get_chest_region(getattr(multiworld, "chests_per_zone")[player], i),
        1000+i,
        lambda multiworld, player, i=i: can_create_universal_chest(multiworld, player, i),
    ) for i in range(200)},

    # Fairy Chests
    **{f"Castle Hamson - Fairy Chest {i+1}":    RLLocationData(
        "Castle Fairy Chests",
        400+i,
        lambda multiworld, player, i=i: can_create_normal_fairy_chest(multiworld, player, i),
    ) for i in range(15)},
    **{f"Forest Abkhazia - Fairy Chest {i+1}":  RLLocationData(
        "Forest Fairy Chests",
        450+i,
        lambda multiworld, player, i=i: can_create_normal_fairy_chest(multiworld, player, i),
    ) for i in range(15)},
    **{f"The Maya - Fairy Chest {i+1}":         RLLocationData(
        "Tower Fairy Chests",
        500+i,
        lambda multiworld, player, i=i: can_create_normal_fairy_chest(multiworld, player, i),
    ) for i in range(15)},
    **{f"Land of Darkness - Fairy Chest {i+1}": RLLocationData(
        "Dungeon Fairy Chests",
        550+i,
        lambda multiworld, player, i=i: can_create_normal_fairy_chest(multiworld, player, i),
    ) for i in range(15)},
    **{f"Universal Fairy Chest {i+1}":          RLLocationData(
        lambda multiworld, player, i=i: get_chest_region(getattr(multiworld, "fairy_chests_per_zone")[player], i),
        1200+i,
        lambda multiworld, player, i=i: can_create_universal_fairy_chest(multiworld, player, i),
    ) for i in range(60)},

    # Events
    "Castle Hamson Boss":                       RLLocationData("Castle Hamson",        locked_item=get_castle_boss),
    "Forest Abkhazia Boss":                     RLLocationData("Forest Abkhazia",      locked_item=get_forest_boss),
    "The Maya Boss":                            RLLocationData("The Maya",             locked_item=get_tower_boss),
    "Land of Darkness Boss":                    RLLocationData("The Land of Darkness", locked_item=get_dungeon_boss),
    "The Fountain Room Boss":                   RLLocationData("The Fountain Room",    locked_item=get_final_boss),
    "The Fountain Room Door":                   RLLocationData("Castle Hamson",        locked_item=get_open_door)
}

# Set the location name for each location based on key.
for location_name, location_data in location_table.items():
    location_data.name = location_name
