from collections import Counter
from typing import ClassVar, Dict, Any, Type
from BaseClasses import Region, Location, Item, ItemClassification, Tutorial
from Options import PerGameCommonOptions
from worlds.AutoWorld import World, WebWorld
from .Items import item_table, group_table, base_id
from .Locations import location_table
from .Rules import create_rules, get_feather_state
from .Options import ShortHikeOptions

class ShortHikeWeb(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the A Short Hike randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Chandler"]
    )]

class ShortHikeWorld(World):
    """
    A Short Hike is a relaxing adventure set on the islands of Hawk Peak. Fly and climb using Claire's wings and Golden Feathers
    to make your way up to the summit. Along the way you'll meet other hikers, discover hidden treasures,
    and take in the beautiful world around you.
    """

    game: str = "A Short Hike"
    web = ShortHikeWeb()
    data_version = 2

    item_name_to_id = {item["name"]: item["id"] for item in item_table}
    location_name_to_id = {loc["name"]: loc["id"] for loc in location_table}
    location_name_to_game_id = {loc["name"]: loc["inGameId"] for loc in location_table}
    location_name_to_chest_angle = {loc["name"]: loc["chestAngle"] for loc in location_table}

    item_name_groups = group_table
    
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = ShortHikeOptions
    options: ShortHikeOptions

    required_client_version = (0, 4, 4)

    def __init__(self, multiworld, player):
        super(ShortHikeWorld, self).__init__(multiworld, player)

    def set_rules(self):
        create_rules()

    def create_item(self, name: str) -> "ShortHikeItem":
        item_id: int = self.item_name_to_id[name]
        id = item_id - base_id - 1

        return ShortHikeItem(name, item_table[id]["classification"], item_id, player=self.player)

    def create_event(self, event: str):
        return ShortHikeItem(event, ItemClassification.progression_skip_balancing, None, self.player)

    def create_items(self) -> None:
        skipped_items = []
        additional_junk = 0

        for item, count in self.multiworld.start_inventory[self.player].value.items():
            for _ in range(count):
                skipped_items.append(item)
                additional_junk += 1

        counter = Counter(skipped_items)

        for item in item_table:
            count = item["count"] - counter[item["name"]]
            
            if count <= 0:
                continue
            else:
                for i in range(count):
                    self.multiworld.itempool.append(self.create_item(item["name"]))
 
        feather_count = self.options.golden_feathers
        if self.options.goal == 1 or self.options.goal == 3:
            if feather_count < 12:
                feather_count = 12

        junk = 45 - self.options.silver_feathers - feather_count - self.options.buckets + additional_junk
        self.multiworld.itempool += [self.create_item("13 Coins") for _ in range(junk)]
        self.multiworld.itempool += [self.create_item("Golden Feather") for _ in range(feather_count - counter["Golden Feather"])]
        self.multiworld.itempool += [self.create_item("Silver Feather") for _ in range(self.options.silver_feathers - counter["Silver Feather"])]
        self.multiworld.itempool += [self.create_item("Bucket") for _ in range(self.options.buckets - counter["Bucket"])]

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        
        main_region = Region("Hawk Peak", self.player, self.multiworld)

        for loc in self.location_name_to_id.keys():
            main_region.locations.append(ShortHikeLocation(self.player, loc, self.location_name_to_id[loc], main_region))

        self.multiworld.regions.append(main_region)

        menu_region.connect(main_region)

        if self.options.goal == 0:
            # Nap
            self.multiworld.completion_condition[self.player] = lambda state: get_feather_state(self, 6, 8, 7, state)
        elif self.options.goal == 1:
            # Photo
            self.multiworld.completion_condition[self.player] = lambda state: get_feather_state(self, 12, 12, 12, state)
        elif self.options.goal == 2:
            # Races
            self.multiworld.completion_condition[self.player] = lambda state: get_feather_state(self, 6, 8, 7, state)
        elif self.options.goal == 3:
            # Help Everyone
            self.multiworld.completion_condition[self.player] = lambda state: (get_feather_state(self, 12, 12, 12, state)
                and state.has("Toy Shovel", self.player) and state.has("Camping Permit", self.player)
                and state.has("Motorboat Key", self.player) and state.has("Headband", self.player)
                and state.has("Wristwatch", self.player) and state.has("Seashell", self.player, 15)
                and state.has("Shell Necklace", self.player))
        elif self.options.goal == 4:
            # Fishmonger
            self.multiworld.completion_condition[self.player] = lambda state: (get_feather_state(self, 6, 8, 7, state)
                and state.has("Fishing Rod", self.player) and state.has("Fishing Journal", self.player))

    def set_rules(self):
        create_rules(self, location_table)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {}
        locations: Dict[int, Any] = {}

        world = self.multiworld
        player = self.player
        options = self.options

        for loc in world.get_filled_locations(player):
            if loc.item.code == None:
                continue
            else:
                data = {
                    "ap_id": loc.address,
                    "item_name": loc.item.name,
                    "player_name": world.player_name[loc.item.player],
                    "type": int(loc.item.classification),
                    "chest_angle": self.location_name_to_chest_angle[loc.name]
                }

                locations[self.location_name_to_game_id[loc.name]] = data

        settings = {
            "goal": int(options.goal),
            "logicLevel": int(options.golden_feather_progression),
        }
    
        slot_data = {
            "locations": locations,
            "settings": settings,
        }
    
        return slot_data

class ShortHikeItem(Item):
    game: str = "A Short Hike"

class ShortHikeLocation(Location):
    game: str = "A Short Hike"