import string
from typing import Dict, List
from .Items import RiskOfRainItem, item_table, item_pool_weights, get_environment_table
from .Locations import RiskOfRainLocation, item_pickups, environment_vanilla_orderedstage_table, environment_sotv_orderedstage_table, orderedstage_location
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
        self.total_revivals = int(self.world.total_revivals[self.player].value / 100 *
                                  self.world.total_locations[self.player].value)

    def generate_basic(self) -> None:
        # shortcut for starting_inventory... The start_with_revive option lets you start with a Dio's Best Friend
        if self.world.start_with_revive[self.player].value:
            self.world.push_precollected(self.world.create_item("Dio's Best Friend", self.player))


        environments_pool = {}
        # only mess with the environments if they are set as items
        if (self.world.environments_as_items[self.player].value):
            environments_pool = get_environment_table(self.world.dlc_sotv[self.player].value)

            # TODO allow for different precollected environments
            self.world.push_precollected(self.world.create_item("Titanic Plains", self.player))
            environments_pool.pop("Titanic Plains")
            self.world.push_precollected(self.world.create_item("The Simulacrum (Titanic Plains)", self.player))
            environments_pool.pop("The Simulacrum (Titanic Plains)")

        # if presets are enabled generate junk_pool from the selected preset
        pool_option = self.world.item_weights[self.player].value
        junk_pool: Dict[str, int] = {}
        if self.world.item_pool_presets[self.player]:
            # generate chaos weights if the preset is chosen
            if pool_option == ItemWeights.option_chaos:
                for name, max_value in item_pool_weights[pool_option].items():
                    junk_pool[name] = self.world.random.randint(0, max_value)
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
        if not (self.world.enable_lunar[self.player] or pool_option == ItemWeights.option_lunartic):
            junk_pool.pop("Lunar Item")

        # Generate item pool
        itempool: List = []
        # Add revive items for the player
        itempool += ["Dio's Best Friend"] * self.total_revivals

        for env_name,_ in environments_pool.items():
            itempool += [env_name]

        # precollected environments are popped from the pool so counting like this is valid
        nonjunk_item_count = self.total_revivals + len(environments_pool)
        # TODO figure out how to properly handle this for new/classic/legacy
        #total_locations = self.world.total_locations[self.player].value
        total_locations = len(
            orderedstage_location.get_locations(
                chests=self.world.chests_per_stage[self.player].value,
                shrines=self.world.shrines_per_stage[self.player].value,
                scavengers=self.world.scavengers_per_stage[self.player].value,
                scanners=self.world.scanner_per_stage[self.player].value,
                altars=self.world.altars_per_stage[self.player].value,
                dlc_sotv=self.world.dlc_sotv[self.player].value
            )
        )
        junk_item_count = total_locations - nonjunk_item_count

        # Fill remaining items with randomly generated junk
        itempool += self.world.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()),
                                              k=junk_item_count)

        # Convert itempool into real items
        itempool = list(map(lambda name: self.create_item(name), itempool))

        self.world.itempool += itempool
        print("total_locations", total_locations) # XXX
        print("junk_item_count", junk_item_count) # XXX
        print("len(itempool)", len(itempool)) # XXX

    def set_rules(self) -> None:
        set_rules(self.world, self.player)

    def create_regions(self) -> None:
        menu = create_region(self.world, self.player, "Menu")
        # TODO make a classic/legacy YAML option
        petrichor = create_region(self.world, self.player, "Petrichor V")
        # petrichor = create_region(self.world, self.player, "Petrichor V",
        #                           [f"ItemPickup{i + 1}" for i in range(self.world.total_locations[self.player].value)])

        environment_regions = create_regions_all_orderedstage(self.world, self.player)

        connection = Entrance(self.player, "Lobby", menu)
        menu.exits.append(connection)
        connection.connect(petrichor)
        for region in environment_regions:
            envconnection = Entrance(self.player, f"Entrance for {region.name}", menu)
            menu.exits.append(envconnection)
            envconnection.connect(region)

        self.world.regions += [menu, petrichor]
        self.world.regions += environment_regions

        create_events(self.world, self.player)

    def fill_slot_data(self):
        return {
            "itemPickupStep": self.world.item_pickup_step[self.player].value,
            "seed": "".join(self.world.slot_seeds[self.player].choice(string.digits) for _ in range(16)),
            "totalLocations": self.world.total_locations[self.player].value,
            "chests_per_stage": self.world.chests_per_stage[self.player].value,
            "shrines_per_stage": self.world.shrines_per_stage[self.player].value,
            "scavengers_per_stage": self.world.scavengers_per_stage[self.player].value,
            "scanner_per_stage": self.world.scanner_per_stage[self.player].value,
            "altars_per_stage": self.world.altars_per_stage[self.player].value,
            "totalRevivals": self.world.total_revivals[self.player].value,
            "startWithDio": self.world.start_with_revive[self.player].value,
            "FinalStageDeath": self.world.final_stage_death[self.player].value,
            "EnvironmentsAsItems": self.world.environments_as_items[self.player].value,
            "DeathLink": self.world.death_link[self.player].value,
        }

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        if False: pass
        # TODO don't make every item be filler
        # if name == "Dio's Best Friend":
        #     classification = ItemClassification.progression
        # elif name in {"Equipment", "Legendary Item"}:
        #     classification = ItemClassification.useful
        else:
            classification = ItemClassification.filler
        item = RiskOfRainItem(name, classification, item_id, self.player)
        return item


def create_events(world: MultiWorld, player: int) -> None:
    world_region = world.get_region("Petrichor V", player)
    victory_event = RiskOfRainLocation(player, "Victory", None, world_region)
    victory_event.place_locked_item(RiskOfRainItem("Victory", ItemClassification.progression, None, player))
    world_region.locations.append(victory_event)
    return
    # TODO figure out how to properly handle this for new/classic/legacy

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
    # TODO this could use a dictionary instead of a list to be consistant with the below (and they could be generic together)
    ret = Region(name, RegionType.Generic, name, player, world)
    if locations:
        for location in locations:
            loc_id = item_pickups[location]
            location = RiskOfRainLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    return ret

global G_environment_locations # XXX
G_environment_locations = 0 # XXX

def create_regions_all_orderedstage(world: MultiWorld, player: int) -> list[Region]:
    rets = []
    orderedstages = environment_vanilla_orderedstage_table
    if(world.dlc_sotv[player].value): orderedstages|= environment_sotv_orderedstage_table

    print("creating regions") # XXX
    global G_environment_locations # XXX
    G_environment_locations = 0 # XXX

    for environment_name, environment_index in orderedstages.items():
        environment_locations = orderedstage_location.get_environment_locations(
            chests=world.chests_per_stage[player].value,
            shrines=world.shrines_per_stage[player].value,
            scavengers=world.scavengers_per_stage[player].value,
            scanners=world.scanner_per_stage[player].value,
            altars=world.altars_per_stage[player].value,
            environment=(environment_name, environment_index)
        )
        rets.append(create_region_orderedstage(world, player, environment_name, environment_locations))

    print("created locations:", G_environment_locations) # XXX

    return rets

def create_region_orderedstage(world: MultiWorld, player: int, name: str, locations: Dict[str,int]) -> Region:
    ret = Region(name, RegionType.Generic, name, player, world)
    global G_environment_locations # XXX
    for location_name,location_id in locations.items():
        G_environment_locations+= 1 # XXX
        ret.locations.append( RiskOfRainLocation(player, location_name, location_id, ret) )
    return ret
