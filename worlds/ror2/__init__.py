import string
from typing import Dict, List, Tuple

from worlds.ror2.RoR2Environments import shift_by_offset
from .Items import RiskOfRainItem, item_table, item_pool_weights, environment_offest
from .Locations import RiskOfRainLocation, get_classic_item_pickups, item_pickups, orderedstage_location
from .Rules import set_rules
from .RoR2Environments import *

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

            # figure out all available ordered stages for each tier
            environment_available_orderedstages_table = environment_vanilla_orderedstages_table
            if (self.world.dlc_sotv[self.player].value):
                environment_available_orderedstages_table = collapse_dict_list_vertical(environment_available_orderedstages_table, environment_sotv_orderedstages_table)

            environments_pool = shift_by_offset(environment_vanilla_table, environment_offest)

            if self.world.dlc_sotv[self.player].value:
                environments_pool|= shift_by_offset(environment_sotv_table, environment_offest)
                self.world.push_precollected(self.create_item("The Simulacrum (Titanic Plains)"))
                environments_pool.pop("The Simulacrum (Titanic Plains)")

            # TODO create an option for whether to start with a full loop granted or just an initial stage
            # randomly choose one evironment each to construct the loop
            for i in range(5):
                unlock = self.world.random.choices(list(environment_available_orderedstages_table[i].keys()))
                self.world.push_precollected(self.create_item(unlock[0]))
                environments_pool.pop(unlock[0])


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

        if (self.world.classic_mode[self.player].value):
            # classic mode
            total_locations = self.world.total_locations[self.player].value
        else:
            # explore mode
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

    def set_rules(self) -> None:
        set_rules(self.world, self.player)

    def create_regions(self) -> None:
        menu = create_region(self.world, self.player, "Menu")
        self.world.regions.append(menu)
        # By using a victory region, we can define it as being connected to by several regions
        #   which can then determine the availability of the victory.
        victory_region = create_region(self.world, self.player, "Victory")
        self.world.regions.append(victory_region)

        if (self.world.classic_mode[self.player].value):
            # classic mode
            petrichor = create_region(self.world, self.player, "Petrichor V",
                                        get_classic_item_pickups(self.world.total_locations[self.player].value))
            self.world.regions.append(petrichor)

            # classic mode can get to victory from the beginning of the game
            to_victory = Entrance(self.player, "beating game", petrichor)
            petrichor.exits.append(to_victory)
            to_victory.connect(victory_region)
        else:
            # explore mode
            petrichor = create_region(self.world, self.player, "Petrichor V")
            self.world.regions.append(petrichor)
            environment_regions = create_regions_all_orderedstage(self.world, self.player)
            self.world.regions += environment_regions # we need to add the regions to the world
            # adding the regions means we can get them from the world when connecting entrances

            if not self.world.environments_as_items[self.player].value:
                # connect all regions to menu
                for region in environment_regions:
                    envconnection = Entrance(self.player, f"Menu to {region.name}", menu)
                    menu.exits.append(envconnection)
                    envconnection.connect(region)

                # when there are no environments locked,
                #   victory can be achived from the beginning of the game
                to_victory = Entrance(self.player, "beating game", petrichor)
                petrichor.exits.append(to_victory)
                to_victory.connect(victory_region)

            else:
                # when explore_mode and environments_as_items are used,
                #   entrances need to be generated for every "environment-to-stage" and "stage-to-environment" connection
                # this is done dynamically for orderedstages and manually for all others with relevant condtions
                stage_regions: List[Region] = []

                # figure out all available ordered stages for each tier
                environment_available_orderedstages_table = environment_vanilla_orderedstages_table
                if (self.world.dlc_sotv[self.player].value):
                    environment_available_orderedstages_table = collapse_dict_list_vertical(environment_available_orderedstages_table, environment_sotv_orderedstages_table)

                # create 5 regions to represent each of the stages in the loop
                for n in range(1,6):
                    stage_regions.append(create_region(self.world, self.player, f"OrderedStage_{n}"))
                self.world.regions += stage_regions # this could happen later, just mocking the above addition of regions

                # Acess to a stage is determined by access to any of the environments in that stage.
                # Threfore any environment can only be accessed if the previous stage can be accessed.
                # For every environment in every stage, create two entrances:
                # - the first entrance goes from the previous stage to the environment
                # - the second entrance goes from the environment to the current stage
                for i in range(5):
                    current_stage = stage_regions[i]
                    if (0 <= i-1): prev_stage = stage_regions[i-1]
                    else: prev_stage = menu # stage 1 environments are accessed from the menu

                    for environment_name,_ in environment_available_orderedstages_table[i].items():
                        current_environment = self.world.get_region(environment_name, self.player)
                        stage_to_env = Entrance(self.player, f"{prev_stage.name} to {environment_name}", prev_stage)
                        stage_to_env.access_rule = lambda state, name=environment_name: state.has(name, self.player)
                        prev_stage.exits.append(stage_to_env)
                        stage_to_env.connect(current_environment)

                        env_to_stage = Entrance(self.player, f"{environment_name} to {current_stage.name}", current_environment)
                        current_environment.exits.append(env_to_stage)
                        env_to_stage.connect(current_stage)

                # create all other regions (even if we don't plan to use them)
                for environment_name,_ in environment_non_orderedstages_table.items():
                    # TODO maybe there is a better way to add regions as to not make duplicates on accident
                    self.world.regions.append(create_region(self.world, self.player, environment_name))
                    # TODO perhaps there is a clean way and efficient way to not create dlc regions when they are unneeded

                # all other connections that are needed
                other_connections: List[Tuple[str,str]] = [
                    ("Sky Meadow", "Hidden Realm: Bulwark's Ambry"), # via artifiact portal in skymeadow
                    ("OrderedStage_1", "Hidden Realm: Bazaar Between Time"), # via altars from any ordered stage
                    ("OrderedStage_1", "Hidden Realm: Gilded Coast"), # via gold altars from any ordered stage
                    ("OrderedStage_5", "Hidden Realm: A Moment, Fractured"), # via celestial portal from stage3 in later loops
                    ("Hidden Realm: A Moment, Fractured", "Hidden Realm: A Moment, Whole"), # via obelisk only in mysteryspace
                    ("Hidden Realm: Bulwark's Ambry", "Void Fields"), # via void portal in baazar
                    ("Sky Meadow", "Commencement"), # via primorial teleporter in skymeadow
                    ("OrderedStage_5", "Void Locus"), # via void portal found on or after stage 7
                    ("Void Fields", "Void Locus"), # via void portal found in voidarena
                    ("Void Locus", "The Planetarium"), # via deep void portal in voidstage
                    ("Commencement", "The Planetarium"), # via glass frog in moon2

                    # TODO make the connections change depending on win conditions
                    ("Commencement", "Victory"),
                    ("Hidden Realm: A Moment, Fractured", "Victory"),
                    ("Hidden Realm: A Moment, Whole", "Victory"),
                    ("The Planetarium", "Victory"),
                ]
                # Note that while it is possible to go to the limbo or voidstage without a full loop,
                #   it may play generate better acknowleding those occur after a full loop.

                for connection in other_connections:
                    source = self.world.get_region(connection[0], self.player)
                    exit = self.world.get_region(connection[1], self.player)

                    to_exit = Entrance(self.player, f"{source.name} to {exit.name}", source)
                    if (exit.name != "Victory"):
                        # if the exit is an environment, it requires the environment to go there
                        to_exit.access_rule = lambda state, name=exit.name: state.has(name, self.player)
                    source.exits.append(to_exit)
                    to_exit.connect(exit)


        connection = Entrance(self.player, "Lobby", menu)
        menu.exits.append(connection)
        connection.connect(petrichor)

        create_events(self.world, self.player)

    def fill_slot_data(self):
        return {
            "itemPickupStep": self.world.item_pickup_step[self.player].value,
            "seed": "".join(self.world.slot_seeds[self.player].choice(string.digits) for _ in range(16)),
            "classic_mode": self.world.classic_mode[self.player].value,
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
        classification = ItemClassification.filler
        if name == "Dio's Best Friend":
            classification = ItemClassification.progression
        elif name in {"Equipment", "Legendary Item"}:
            classification = ItemClassification.useful

        # Only check for an item to be a environment unlock if those are known to be in the pool.
        # This should shave down comparions.
        elif self.world.environments_as_items[self.player].value \
             and name in environment_ALL_table.keys():

            classification = ItemClassification.progression

        # TODO should lunar items be marked as traps?
        item = RiskOfRainItem(name, classification, item_id, self.player)
        return item


def create_events(world: MultiWorld, player: int) -> None:
    total_locations = world.total_locations[player].value
    num_of_events = total_locations // 25
    if total_locations / 25 == num_of_events:
        num_of_events -= 1
    world_region = world.get_region("Petrichor V", player)

    if (world.classic_mode[player].value):
        # only setup Pickups when using classic_mode
        for i in range(num_of_events):
            event_loc = RiskOfRainLocation(player, f"Pickup{(i + 1) * 25}", None, world_region)
            event_loc.place_locked_item(RiskOfRainItem(f"Pickup{(i + 1) * 25}", ItemClassification.progression, None, player))
            event_loc.access_rule(lambda state, i=i: state.can_reach(f"ItemPickup{((i + 1) * 25) - 1}", player))
            world_region.locations.append(event_loc)
    elif (world.environments_as_items[player].value):
        # only enforce extra events for explore_mode and environments_as_items
        for n in range(1,6):
            event_region = world.get_region(f"OrderedStage_{n}", player)
            event_loc = RiskOfRainLocation(player, f"OrderedStage_{n} Access", None, event_region)
            event_loc.place_locked_item(RiskOfRainItem(f"OrderedStage_{n} Access", ItemClassification.progression, None, player))
            world_region.locations.append(event_loc)

    victory_region = world.get_region("Victory", player)
    victory_event = RiskOfRainLocation(player, "Victory", None, victory_region)
    victory_event.place_locked_item(RiskOfRainItem("Victory", ItemClassification.progression, None, player))
    world_region.locations.append(victory_event)


def create_region(world: MultiWorld, player: int, name: str, locations: Dict[str,int] = {}) -> Region:
    ret = Region(name, RegionType.Generic, name, player, world)
    for location_name,location_id in locations.items():
        ret.locations.append( RiskOfRainLocation(player, location_name, location_id, ret) )
    return ret

def create_regions_all_orderedstage(world: MultiWorld, player: int) -> list[Region]:
    """
    Creates all regions for all ordered stages (accounting for world.dlc_sotv)
    """
    rets: List[Region] = []
    orderedstages = compress_dict_list_horizontal(environment_vanilla_orderedstages_table)
    if(world.dlc_sotv[player].value): orderedstages|= compress_dict_list_horizontal(environment_sotv_orderedstages_table)

    rets = create_region_orderedstage(world, player, orderedstages)

    return rets

def create_region_orderedstage(world: MultiWorld, player: int, environments: Dict[str,int]) -> Region:
    rets: List[Region] = []
    for environment_name, environment_index in environments.items():
        environment_locations = orderedstage_location.get_environment_locations(
            chests=world.chests_per_stage[player].value,
            shrines=world.shrines_per_stage[player].value,
            scavengers=world.scavengers_per_stage[player].value,
            scanners=world.scanner_per_stage[player].value,
            altars=world.altars_per_stage[player].value,
            environment=(environment_name, environment_index)
        )
        rets.append(create_region(world, player, environment_name, environment_locations))
    return rets
