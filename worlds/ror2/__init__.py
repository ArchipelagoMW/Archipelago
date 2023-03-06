import string

from .Items import RiskOfRainItem, item_table, item_pool_weights, environment_offest
from .Locations import RiskOfRainLocation, get_classic_item_pickups, item_pickups, orderedstage_location
from .Rules import set_rules
from .RoR2Environments import *

from BaseClasses import Region, Entrance, Item, ItemClassification, MultiWorld, Tutorial
from .Options import ItemWeights, ROR2Options
from worlds.AutoWorld import World, WebWorld
from .Regions import create_regions


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
    game = "Risk of Rain 2"
    options_dataclass = ROR2Options
    o: ROR2Options
    topology_present = False

    item_name_to_id = item_table
    location_name_to_id = item_pickups

    data_version = 6
    required_client_version = (0, 3, 7)
    web = RiskOfWeb()
    total_revivals: int

    def generate_early(self) -> None:
        # figure out how many revivals should exist in the pool
        if self.o.goal == "classic":
            total_locations = self.o.total_locations.value
        else:
            total_locations = len(
                orderedstage_location.get_locations(
                    chests=self.o.chests_per_stage.value,
                    shrines=self.o.shrines_per_stage.value,
                    scavengers=self.o.scavengers_per_stage.value,
                    scanners=self.o.scanner_per_stage.value,
                    altars=self.o.altars_per_stage.value,
                    dlc_sotv=self.o.dlc_sotv.value
                )
            )
        self.total_revivals = int(self.o.total_revivals.value / 100 *
                                  total_locations)
        if self.o.start_with_revive:
            self.total_revivals -= 1

    def create_items(self) -> None:
        # shortcut for starting_inventory... The start_with_revive option lets you start with a Dio's Best Friend
        if self.o.start_with_revive:
            self.multiworld.push_precollected(self.multiworld.create_item("Dio's Best Friend", self.player))

        environments_pool = {}
        # only mess with the environments if they are set as items
        if self.o.goal == "explore":

            # figure out all available ordered stages for each tier
            environment_available_orderedstages_table = environment_vanilla_orderedstages_table
            if self.o.dlc_sotv:
                environment_available_orderedstages_table = collapse_dict_list_vertical(environment_available_orderedstages_table, environment_sotv_orderedstages_table)

            environments_pool = shift_by_offset(environment_vanilla_table, environment_offest)

            if self.o.dlc_sotv:
                environment_offset_table = shift_by_offset(environment_sotv_table, environment_offest)
                environments_pool = {**environments_pool, **environment_offset_table}
            environments_to_precollect = 5 if self.o.begin_with_loop else 1
            # percollect environments for each stage (or just stage 1)
            for i in range(environments_to_precollect):
                unlock = self.multiworld.random.choices(list(environment_available_orderedstages_table[i].keys()), k=1)
                self.multiworld.push_precollected(self.create_item(unlock[0]))
                environments_pool.pop(unlock[0])

        # if presets are enabled generate junk_pool from the selected preset
        pool_option = self.o.item_weights.value
        junk_pool: Dict[str, int] = {}
        if self.o.item_pool_presets:
            # generate chaos weights if the preset is chosen
            if pool_option == ItemWeights.option_chaos:
                for name, max_value in item_pool_weights[pool_option].items():
                    junk_pool[name] = self.multiworld.random.randint(0, max_value)
            else:
                junk_pool = item_pool_weights[pool_option].copy()
        else:  # generate junk pool from user created presets
            junk_pool = {
                "Item Scrap, Green": self.o.green_scrap.value,
                "Item Scrap, Red": self.o.red_scrap.value,
                "Item Scrap, Yellow": self.o.yellow_scrap.value,
                "Item Scrap, White": self.o.white_scrap.value,
                "Common Item": self.o.common_item.value,
                "Uncommon Item": self.o.uncommon_item.value,
                "Legendary Item": self.o.legendary_item.value,
                "Boss Item": self.o.boss_item.value,
                "Lunar Item": self.o.lunar_item.value,
                "Void Item": self.o.void_item.value,
                "Equipment": self.o.equipment.value
            }

        # remove lunar items from the pool if they're disabled in the yaml unless lunartic is rolled
        if not self.o.enable_lunar or pool_option == ItemWeights.option_lunartic:
            junk_pool.pop("Lunar Item")
        # remove void items from the pool
        if not self.o.dlc_sotv or pool_option == ItemWeights.option_void:
            junk_pool.pop("Void Item")

        # Generate item pool
        itempool: List = []
        # Add revive items for the player
        itempool += ["Dio's Best Friend"] * self.total_revivals

        for env_name, _ in environments_pool.items():
            itempool += [env_name]

        # precollected environments are popped from the pool so counting like this is valid
        nonjunk_item_count = self.total_revivals + len(environments_pool)
        if self.o.goal == "classic":
            # classic mode
            total_locations = self.o.total_locations.value
        else:
            # explore mode
            total_locations = len(
                orderedstage_location.get_locations(
                    chests=self.o.chests_per_stage.value,
                    shrines=self.o.shrines_per_stage.value,
                    scavengers=self.o.scavengers_per_stage.value,
                    scanners=self.o.scanner_per_stage.value,
                    altars=self.o.altars_per_stage.value,
                    dlc_sotv=self.o.dlc_sotv.value
                )
            )
        junk_item_count = total_locations - nonjunk_item_count
        # Fill remaining items with randomly generated junk
        itempool += self.multiworld.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()),
                                                   k=junk_item_count)

        # Convert itempool into real items
        itempool = list(map(lambda name: self.create_item(name), itempool))
        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player)

    def create_regions(self) -> None:

        if self.o.goal == "classic":
            # classic mode
            menu = create_region(self.multiworld, self.player, "Menu")
            self.multiworld.regions.append(menu)
            # By using a victory region, we can define it as being connected to by several regions
            #   which can then determine the availability of the victory.
            victory_region = create_region(self.multiworld, self.player, "Victory")
            self.multiworld.regions.append(victory_region)
            petrichor = create_region(self.multiworld, self.player, "Petrichor V",
                                      get_classic_item_pickups(self.o.total_locations.value))
            self.multiworld.regions.append(petrichor)

            # classic mode can get to victory from the beginning of the game
            to_victory = Entrance(self.player, "beating game", petrichor)
            petrichor.exits.append(to_victory)
            to_victory.connect(victory_region)

            connection = Entrance(self.player, "Lobby", menu)
            menu.exits.append(connection)
            connection.connect(petrichor)
        else:
            # explore mode
            create_regions(self.multiworld, self.player)

        create_events(self.multiworld, self.player)

    def fill_slot_data(self):
        options_dict = self.o.as_dict("item_pickup_step", "shrine_use_step", "goal", "total_locations",
                                      "chests_per_stage", "shrines_per_stage", "scavengers_per_stage",
                                      "scanner_per_stage", "altars_per_stage", "total_revivals", "start_with_revive",
                                      "final_stage_death", "death_link")
        cased_dict = {}
        for key, value in options_dict.items():
            split_name = [name.title() for name in key.split("_")]
            split_name[0] = split_name[0].lower()
            new_name = "".join(split_name)
            cased_dict[new_name] = value

        return {
            **cased_dict,
            "seed": "".join(self.multiworld.per_slot_randoms[self.player].choice(string.digits) for _ in range(16)),
        }

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        classification = ItemClassification.filler
        if name == "Dio's Best Friend":
            classification = ItemClassification.progression
        elif name in {"Legendary Item", "Boss Item"}:
            classification = ItemClassification.useful
        elif name == "Lunar Item":
            classification = ItemClassification.trap

        # Only check for an item to be a environment unlock if those are known to be in the pool.
        # This should shave down comparions.

        elif name in environment_ALL_table.keys():
            if name in {"Hidden Realm: Bulwark's Ambry", "Hidden Realm: Gilded Coast,"}:
                classification = ItemClassification.useful
            else:
                classification = ItemClassification.progression

        item = RiskOfRainItem(name, classification, item_id, self.player)
        return item


def create_events(world: MultiWorld, player: int) -> None:
    total_locations = world.total_locations[player].value
    num_of_events = total_locations // 25
    if total_locations / 25 == num_of_events:
        num_of_events -= 1
    world_region = world.get_region("Petrichor V", player)
    if world.goal[player] == "classic":
        # only setup Pickups when using classic_mode
        for i in range(num_of_events):
            event_loc = RiskOfRainLocation(player, f"Pickup{(i + 1) * 25}", None, world_region)
            event_loc.place_locked_item(RiskOfRainItem(f"Pickup{(i + 1) * 25}", ItemClassification.progression, None, player))
            event_loc.access_rule = \
                lambda state, i=i: state.can_reach(f"ItemPickup{((i + 1) * 25) - 1}", "Location", player)
            world_region.locations.append(event_loc)
    elif world.goal[player] == "explore":
        for n in range(1, 6):

            event_region = world.get_region(f"OrderedStage_{n}", player)
            event_loc = RiskOfRainLocation(player, f"Stage_{n}", None, event_region)
            event_loc.place_locked_item(RiskOfRainItem(f"Stage_{n}", ItemClassification.progression, None, player))
            event_loc.show_in_spoiler = False
            event_region.locations.append(event_loc)

    victory_region = world.get_region("Victory", player)
    victory_event = RiskOfRainLocation(player, "Victory", None, victory_region)
    victory_event.place_locked_item(RiskOfRainItem("Victory", ItemClassification.progression, None, player))
    world_region.locations.append(victory_event)


def create_region(world: MultiWorld, player: int, name: str, locations: Dict[str, int] = {}) -> Region:
    ret = Region(name, player, world)
    for location_name, location_id in locations.items():
        ret.locations.append(RiskOfRainLocation(player, location_name, location_id, ret))
    return ret
