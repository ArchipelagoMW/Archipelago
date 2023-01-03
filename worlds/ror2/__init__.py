import string
from typing import Dict, List

from BaseClasses import Entrance, Item, ItemClassification, MultiWorld, Region, RegionType, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import RiskOfRainItem, item_pool_weights, item_table
from .Locations import RiskOfRainLocation, item_pickups
from .Options import ItemWeights, ror2_options
from .Rules import set_rules

client_version = 1


class RiskOfWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Risk of Rain 2 integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Ijwu"]
    )]


class RiskOfRainWorld(World):
    """
     Escape a chaotic alien planet by fighting through hordes of frenzied monsters – with your friends, or on your own.
     Combine loot in surprising ways and master each character until you become the havoc you feared upon your
     first crash landing.
    """
    game: str = "Risk of Rain 2"
    option_definitions = ror2_options
    topology_present = False

    item_name_to_id = item_table
    location_name_to_id = item_pickups

    data_version = 4
    web = RiskOfWeb()
    total_revivals: int

    def generate_early(self) -> None:
        # figure out how many revivals should exist in the pool
        self.total_revivals = int(self.multiworld.total_revivals[self.player].value / 100 *
                                  self.multiworld.total_locations[self.player].value)

    def generate_basic(self) -> None:
        # shortcut for starting_inventory... The start_with_revive option lets you start with a Dio's Best Friend
        if self.multiworld.start_with_revive[self.player].value:
            self.multiworld.push_precollected(self.multiworld.create_item("Dio's Best Friend", self.player))

        # if presets are enabled generate junk_pool from the selected preset
        pool_option = self.multiworld.item_weights[self.player].value
        junk_pool: Dict[str, int] = {}
        if self.multiworld.item_pool_presets[self.player]:
            # generate chaos weights if the preset is chosen
            if pool_option == ItemWeights.option_chaos:
                for name, max_value in item_pool_weights[pool_option].items():
                    junk_pool[name] = self.multiworld.random.randint(0, max_value)
            else:
                junk_pool = item_pool_weights[pool_option].copy()
        else:  # generate junk pool from user created presets
            junk_pool = {
                "Item Scrap, Green": self.multiworld.green_scrap[self.player].value,
                "Item Scrap, Red": self.multiworld.red_scrap[self.player].value,
                "Item Scrap, Yellow": self.multiworld.yellow_scrap[self.player].value,
                "Item Scrap, White": self.multiworld.white_scrap[self.player].value,
                "Common Item": self.multiworld.common_item[self.player].value,
                "Uncommon Item": self.multiworld.uncommon_item[self.player].value,
                "Legendary Item": self.multiworld.legendary_item[self.player].value,
                "Boss Item": self.multiworld.boss_item[self.player].value,
                "Lunar Item": self.multiworld.lunar_item[self.player].value,
                "Equipment": self.multiworld.equipment[self.player].value
            }

        # remove lunar items from the pool if they're disabled in the yaml unless lunartic is rolled
        if not (self.multiworld.enable_lunar[self.player] or pool_option == ItemWeights.option_lunartic):
            junk_pool.pop("Lunar Item")

        # Generate item pool
        itempool: List = []
        # Add revive items for the player
        itempool += ["Dio's Best Friend"] * self.total_revivals

        # Fill remaining items with randomly generated junk
        itempool += self.multiworld.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()),
                                              k=self.multiworld.total_locations[self.player].value - self.total_revivals)

        # Convert itempool into real items
        itempool = list(map(lambda name: self.create_item(name), itempool))

        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player)

    def create_regions(self) -> None:
        menu = create_region(self.multiworld, self.player, "Menu")
        petrichor = create_region(self.multiworld, self.player, "Petrichor V",
                                  [f"ItemPickup{i + 1}" for i in range(self.multiworld.total_locations[self.player].value)])

        connection = Entrance(self.player, "Lobby", menu)
        menu.exits.append(connection)
        connection.connect(petrichor)

        self.multiworld.regions += [menu, petrichor]

        create_events(self.multiworld, self.player)

    def fill_slot_data(self):
        return {
            "itemPickupStep": self.multiworld.item_pickup_step[self.player].value,
            "seed": "".join(self.multiworld.slot_seeds[self.player].choice(string.digits) for _ in range(16)),
            "totalLocations": self.multiworld.total_locations[self.player].value,
            "totalRevivals": self.multiworld.total_revivals[self.player].value,
            "startWithDio": self.multiworld.start_with_revive[self.player].value,
            "FinalStageDeath": self.multiworld.final_stage_death[self.player].value
        }

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        if name == "Dio's Best Friend":
            classification = ItemClassification.progression
        elif name in {"Equipment", "Legendary Item"}:
            classification = ItemClassification.useful
        else:
            classification = ItemClassification.filler
        item = RiskOfRainItem(name, classification, item_id, self.player)
        return item


def create_events(world: MultiWorld, player: int) -> None:
    total_locations = world.total_locations[player].value
    num_of_events = total_locations // 25
    if total_locations / 25 == num_of_events:
        num_of_events -= 1
    world_region = world.get_region("Petrichor V", player)

    for i in range(num_of_events):
        event_loc = RiskOfRainLocation(player, f"Pickup{(i + 1) * 25}", None, world_region)
        event_loc.place_locked_item(RiskOfRainItem(f"Pickup{(i + 1) * 25}", ItemClassification.progression, None, player))
        event_loc.access_rule(lambda state, i=i: state.can_reach(f"ItemPickup{((i + 1) * 25) - 1}", player))
        world_region.locations.append(event_loc)

    victory_event = RiskOfRainLocation(player, "Victory", None, world_region)
    victory_event.place_locked_item(RiskOfRainItem("Victory", ItemClassification.progression, None, player))
    world_region.locations.append(victory_event)


def create_region(world: MultiWorld, player: int, name: str, locations: List[str] = None) -> Region:
    ret = Region(name, RegionType.Generic, name, player, world)
    if locations:
        for location in locations:
            loc_id = item_pickups[location]
            location = RiskOfRainLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    return ret
