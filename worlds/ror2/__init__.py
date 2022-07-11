import string
from .Items import RiskOfRainItem, item_table, item_pool_weights
from .Locations import location_table, RiskOfRainLocation, base_location_table
from .Rules import set_rules

from BaseClasses import Region, RegionType, Entrance, Item, ItemClassification, MultiWorld, Tutorial
from .Options import ror2_options
from ..AutoWorld import World, WebWorld

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
    options = ror2_options
    topology_present = False

    item_name_to_id = item_table
    location_name_to_id = location_table

    data_version = 3
    forced_auto_forfeit = True
    web = RiskOfWeb()

    def generate_basic(self):
        # shortcut for starting_inventory... The start_with_revive option lets you start with a Dio's Best Friend
        if self.world.start_with_revive[self.player].value:
            self.world.push_precollected(self.world.create_item("Dio's Best Friend", self.player))

        # if presets are enabled generate junk_pool from the selected preset
        pool_option = self.world.item_weights[self.player].value
        if self.world.item_pool_presets[self.player].value:
            # generate chaos weights if the preset is chosen
            if pool_option == 5:
                junk_pool = {
                    "Item Scrap, Green": self.world.random.randint(0, 80),
                    "Item Scrap, Red": self.world.random.randint(0, 45),
                    "Item Scrap, Yellow": self.world.random.randint(0, 30),
                    "Item Scrap, White": self.world.random.randint(0, 100),
                    "Common Item": self.world.random.randint(0, 100),
                    "Uncommon Item": self.world.random.randint(0, 70),
                    "Legendary Item": self.world.random.randint(0, 30),
                    "Boss Item": self.world.random.randint(0, 20),
                    "Lunar Item": self.world.random.randint(0, 60),
                    "Equipment": self.world.random.randint(0, 40)
                }
            else:
                junk_pool = item_pool_weights[pool_option].copy()
        else:  # generate junk pool from user created presets
            junk_pool = {
                "Item Scrap, Green": self.world.green_scrap[self.player].value,
                "Item Scrap, Red": self.world.red_scrap[self.player].value,
                "Item Scrap, Yellow": self.world.yellow_scrap[self.player].value,
                "Item Scrap, White": self.world.white_scrap[self.player].value,
                "Common Item": self.world.common_item[self.player].value,
                "Uncommon Item": self.world.uncommon_item[self.player].value,
                "Legendary Item": self.world.legendary_item[self.player].value,
                "Boss Item": self.world.boss_item[self.player].value,
                "Lunar Item": self.world.lunar_item[self.player].value,
                "Equipment": self.world.equipment[self.player].value
            }

        # remove lunar items from the pool if they're disabled in the yaml unless lunartic is rolled
        if not self.world.enable_lunar[self.player]:
            if not pool_option == 4:
                junk_pool.pop("Lunar Item")

        # Generate item pool
        itempool = []

        # Add revive items for the player
        itempool += ["Dio's Best Friend"] * int(self.world.total_revivals[self.player] / 100 * self.world.total_locations[self.player])

        # Fill remaining items with randomly generated junk
        itempool += self.world.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()),
                                              k=self.world.total_locations[self.player] -
                                                int(self.world.total_revivals[self.player] / 100 * self.world.total_locations[self.player]))

        # Convert itempool into real items
        itempool = list(map(lambda name: self.create_item(name), itempool))

        self.world.itempool += itempool

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_regions(self):
        create_regions(self.world, self.player)
        create_events(self.world, self.player, int(self.world.total_locations[self.player]))

    def fill_slot_data(self):
        return {
            "itemPickupStep": self.world.item_pickup_step[self.player].value,
            "seed": "".join(self.world.slot_seeds[self.player].choice(string.digits) for i in range(16)),
            "totalLocations": self.world.total_locations[self.player].value,
            "totalRevivals": self.world.total_revivals[self.player].value,
            "startWithDio": self.world.start_with_revive[self.player].value,
            "FinalStageDeath": self.world.final_stage_death[self.player].value
        }

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        item = RiskOfRainItem(name, ItemClassification.filler, item_id, self.player)
        if name == 'Dio\'s Best Friend':
            item.classification = ItemClassification.progression
        elif name == 'Equipment':
            item.classification = ItemClassification.useful
        return item


def create_events(world: MultiWorld, player: int, total_locations: int):
    num_of_events = total_locations // 25
    if total_locations / 25 == num_of_events:
        num_of_events -= 1
    for i in range(num_of_events):
        event_loc = RiskOfRainLocation(player, f"Pickup{(i + 1) * 25}", None, world.get_region('Petrichor V', player))
        event_loc.place_locked_item(RiskOfRainItem(f"Pickup{(i + 1) * 25}", ItemClassification.progression, None, player))
        event_loc.access_rule(lambda state, i=i: state.can_reach(f"ItemPickup{((i + 1) * 25) - 1}", player))
        world.get_region('Petrichor V', player).locations.append(event_loc)


# generate locations based on player setting
def create_regions(world, player: int):
    world.regions += [
        create_region(world, player, 'Menu', None, ['Lobby']),
        create_region(world, player, 'Petrichor V',
                      [location for location in base_location_table] +
                      [f"ItemPickup{i}" for i in range(1, 1 + world.total_locations[player])])
    ]

    world.get_entrance("Lobby", player).connect(world.get_region("Petrichor V", player))
    world.get_location("Victory", player).place_locked_item(RiskOfRainItem("Victory", ItemClassification.progression,
                                                                           None, player))


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, RegionType.Generic, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = location_table[location]
            location = RiskOfRainLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret
