import string
from typing import Dict, List
from .Items import RiskOfRainItem, item_table, item_pool_weights
from .Locations import RiskOfRainLocation, item_pickups
from .Rules import set_rules

from BaseClasses import Region, RegionType, Entrance, Item, ItemClassification, MultiWorld, Tutorial
from .Options import ror2_options, ItemWeights
from worlds.AutoWorld import World, WebWorld

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
    forced_auto_forfeit = True
    web = RiskOfWeb()
    total_revivals: int

    def generate_early(self) -> None:
        # figure out how many revivals should exist in the pool
        self.total_revivals = int(self.options["total_revivals"].value // 100 * self.options["total_locations"].value)

    def generate_basic(self) -> None:
        # shortcut for starting_inventory... The start_with_revive option lets you start with a Dio's Best Friend
        if self.options["start_with_revive"].value:
            self.world.push_precollected(self.world.create_item("Dio's Best Friend", self.player))

        # if presets are enabled generate junk_pool from the selected preset
        pool_option = self.options["item_weights"].value
        junk_pool: Dict[str, int] = {}
        if self.options["item_pool_presets"]:
            # generate chaos weights if the preset is chosen
            if pool_option == ItemWeights.option_chaos:
                for name, max_value in item_pool_weights[pool_option].items():
                    junk_pool[name] = self.world.random.randint(0, max_value)
            else:
                junk_pool = item_pool_weights[pool_option].copy()
        else:  # generate junk pool from user created presets
            junk_pool = {
                "Item Scrap, Green": self.options["green_scrap"].value,
                "Item Scrap, Red": self.options["red_scrap"].value,
                "Item Scrap, Yellow": self.options["yellow_scrap"].value,
                "Item Scrap, White": self.options["white_scrap"].value,
                "Common Item": self.options["common_item"].value,
                "Uncommon Item": self.options["uncommon_item"].value,
                "Legendary Item": self.options["legendary_item"].value,
                "Boss Item": self.options["boss_item"].value,
                "Lunar Item": self.options["lunar_item"].value,
                "Equipment": self.options["equipment"].value
            }

        # remove lunar items from the pool if they're disabled in the yaml unless lunartic is rolled
        if not (self.options["enable_lunar"] or pool_option == ItemWeights.option_lunartic):
            junk_pool.pop("Lunar Item")

        # Generate item pool
        itempool: List = []
        # Add revive items for the player
        itempool += ["Dio's Best Friend"] * self.total_revivals

        # Fill remaining items with randomly generated junk
        itempool += self.world.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()),
                                              k=self.options["total_locations"].value - self.total_revivals)

        # Convert itempool into real items
        itempool = list(map(lambda name: self.create_item(name), itempool))

        self.world.itempool += itempool

    def set_rules(self) -> None:
        set_rules(self.world, self.player)

    def create_regions(self) -> None:
        menu = create_region(self.world, self.player, "Menu")
        petrichor = create_region(self.world, self.player, "Petrichor V",
                                  [f"ItemPickup{i + 1}" for i in range(self.options["total_locations"].value)])

        connection = Entrance(self.player, "Lobby", menu)
        menu.exits.append(connection)
        connection.connect(petrichor)

        self.world.regions += [menu, petrichor]

        self.create_events()

    def fill_slot_data(self):
        return {
            "itemPickupStep": self.options["item_pickup_step"].value,
            "seed": "".join(self.world.slot_seeds[self.player].choice(string.digits) for _ in range(16)),
            "totalLocations": self.options["total_locations"].value,
            "totalRevivals": self.options["total_revivals"].value,
            "startWithDio": self.options["start_with_revive"].value,
            "FinalStageDeath": self.options["final_stage_death"].value
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

    def create_events(self) -> None:
        total_locations = self.options["total_locations"].value
        num_of_events = total_locations // 25
        if total_locations / 25 == num_of_events:
            num_of_events -= 1
        world_region = self.world.get_region("Petrichor V", self.player)

        for i in range(num_of_events):
            event_loc = RiskOfRainLocation(self.player, f"Pickup{(i + 1) * 25}", None, world_region)
            event_loc.place_locked_item(RiskOfRainItem(f"Pickup{(i + 1) * 25}",
                                                       ItemClassification.progression, None, self.player))
            event_loc.access_rule(lambda state, i=i: state.can_reach(f"ItemPickup{((i + 1) * 25) - 1}", self.player))
            world_region.locations.append(event_loc)

        victory_event = RiskOfRainLocation(self.player, "Victory", None, world_region)
        victory_event.place_locked_item(RiskOfRainItem("Victory", ItemClassification.progression, None, self.player))
        world_region.locations.append(victory_event)


def create_region(world: MultiWorld, player: int, name: str, locations: List[str] = None) -> Region:
    ret = Region(name, RegionType.Generic, name, player, world)
    if locations:
        for location in locations:
            loc_id = item_pickups[location]
            location = RiskOfRainLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    return ret
