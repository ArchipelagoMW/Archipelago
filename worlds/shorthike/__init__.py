from typing import ClassVar, Dict, Any, Type
from BaseClasses import ItemClassification, Region, Location, Item, Tutorial
from Options import PerGameCommonOptions
from worlds.AutoWorld import World, WebWorld
from .Items import item_table, group_table, base_id
from .Locations import location_table
from .Rules import create_rules, get_min_feathers
from .Options import ShortHikeOptions, shorthike_option_groups

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
    option_groups = shorthike_option_groups

class ShortHikeWorld(World):
    """
    A Short Hike is a relaxing adventure set on the islands of Hawk Peak. Fly and climb using Claire's wings and Golden Feathers
    to make your way up to the summit. Along the way you'll meet other hikers, discover hidden treasures,
    and take in the beautiful world around you.
    """

    game = "A Short Hike"
    web = ShortHikeWeb()

    item_name_to_id = {item["name"]: item["id"] for item in item_table}
    location_name_to_id = {loc["name"]: loc["id"] for loc in location_table}
    location_name_to_game_id = {loc["name"]: loc["inGameId"] for loc in location_table}

    item_name_groups = group_table
    
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = ShortHikeOptions
    options: ShortHikeOptions

    required_client_version = (0, 4, 4)

    def get_filler_item_name(self) -> str:
        return self.options.filler_coin_amount.current_option_name

    def create_item(self, name: str) -> "ShortHikeItem":
        item_id: int = self.item_name_to_id[name]
        id = item_id - base_id - 1

        classification = item_table[id]["classification"]
        if self.options.easier_races and name == "Running Shoes":
            classification = ItemClassification.progression

        return ShortHikeItem(name, classification, item_id, player=self.player)

    def create_items(self) -> None:
        itempool = []
        for item in item_table:
            count = item["count"]
            
            if count <= 0:
                continue
            else:
                for i in range(count):
                    itempool.append(self.create_item(item["name"]))
 
        feather_count = self.options.golden_feathers
        if self.options.goal == 1 or self.options.goal == 3:
            if feather_count < 12:
                feather_count = 12

        itempool += [self.create_item("Golden Feather") for _ in range(feather_count)]
        itempool += [self.create_item("Silver Feather") for _ in range(self.options.silver_feathers)]
        itempool += [self.create_item("Bucket") for _ in range(self.options.buckets)]
        itempool += [self.create_item("Stick") for _ in range(self.options.sticks)]
        itempool += [self.create_item("Toy Shovel") for _ in range(self.options.toy_shovels)]

        if self.options.random_walkie_talkie:
            itempool.append(self.create_item("Walkie Talkie"))
        else:
            self.multiworld.get_location("Lose Race Gift", self.player).place_locked_item(self.create_item("Walkie Talkie"))

        junk = len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool)
        itempool += [self.create_item(self.get_filler_item_name()) for _ in range(junk)]

        self.multiworld.itempool += itempool

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        
        main_region = Region("Hawk Peak", self.player, self.multiworld)

        for loc in self.location_name_to_id.keys():
            main_region.locations.append(ShortHikeLocation(self.player, loc, self.location_name_to_id[loc], main_region))

        self.multiworld.regions.append(main_region)

        menu_region.connect(main_region)

        if self.options.goal == "nap":
            # Nap
            self.multiworld.completion_condition[self.player] = lambda state: (state.has("Golden Feather", self.player, get_min_feathers(self, 7, 9))
                or (state.has("Bucket", self.player) and state.has("Golden Feather", self.player, 7)))
        elif self.options.goal == "photo":
            # Photo
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Golden Feather", self.player, 12)
        elif self.options.goal == "races":
            # Races
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("Hawk Peak Race Reward", self.player)
        elif self.options.goal == "help_everyone":
            # Help Everyone
            self.multiworld.completion_condition[self.player] = lambda state: (state.can_reach_location("Collect 15 Seashells", self.player)
                and state.has("Golden Feather", self.player, 12)
                and state.can_reach_location("Tough Bird Salesman (400 Coins)", self.player)
                and state.can_reach_location("Ranger May Shell Necklace Golden Feather", self.player)
                and state.can_reach_location("Sue the Rabbit Shoes Reward", self.player)
                and state.can_reach_location("Wristwatch Trade", self.player)
                and state.can_reach_location("Return Camping Permit", self.player)
                and state.can_reach_location("Boat Challenge Reward", self.player)
                and state.can_reach_location("Shovel Kid Trade", self.player)
                and state.can_reach_location("Purchase Sunhat", self.player)
                and state.can_reach_location("Artist Golden Feather", self.player))
        elif self.options.goal == "fishmonger":
            # Fishmonger
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("Catch All Fish Reward", self.player)

    def set_rules(self):
        create_rules(self, location_table)

    def fill_slot_data(self) -> Dict[str, Any]:
        options = self.options

        settings = {
            "goal": int(options.goal),
            "logicLevel": int(options.golden_feather_progression),
            "costMultiplier": int(options.cost_multiplier),
            "shopCheckLogic": int(options.shop_check_logic),
            "minShopCheckLogic": int(options.min_shop_check_logic),
            "easierRaces": bool(options.easier_races),
        }
    
        slot_data = {
            "settings": settings,
        }
    
        return slot_data

class ShortHikeItem(Item):
    game: str = "A Short Hike"

class ShortHikeLocation(Location):
    game: str = "A Short Hike"
