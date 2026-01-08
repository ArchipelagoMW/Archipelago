import logging
from typing import Any, Mapping, Optional

from BaseClasses import CollectionState, Item, ItemClassification, Tutorial
from Fill import fill_restrictive, FillError, sweep_from_pool
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, SuffixIdentifier, Type
from . import ItemPool
from .data import Items, Locations, Planets
from .data.Items import ALL_WEAPONS, check_progressive_item, CollectableData, get_bolt_pack, progression_rules
from .data.Locations import (ALL_POOLS, DEFAULT_LIST, LocationData, POOL_BOOT, POOL_EXTRA_ITEM, POOL_GADGET,
                             POOL_GOLD_BOLT, POOL_GOLDEN_WEAPON, POOL_HELMET, POOL_INFOBOT, POOL_PACK, POOL_SKILLPOINT,
                             POOL_WEAPON)
from .data.Planets import ALL_LOCATIONS, location_groups, PlanetData
from .Options import RacOptions, ShuffleGadgets, ShuffleInfobots, ShuffleWeapons, StartingItem, StartingLocation
from .Regions import create_regions

rac_logger = logging.getLogger("Ratchet & Clank")
rac_logger.setLevel(logging.DEBUG)


def run_client(_url: Optional[str] = None):
    # from .RacClient import launch
    # launch_subprocess(launch, name="RacClient")
    components.append(Component("Ratchet & Clank Client", func=run_client, component_type=Type.CLIENT,
                                file_identifier=SuffixIdentifier(".aprac")))


class RacWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Ratchet & Clank for Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["Panad"],
    )]


class RacItem(Item):
    game: str = "Ratchet & Clank"


class RacWorld(World):
    """
    Ratchet & Clank is a third-person shooter platform video game developed by Insomniac Games
    and published by Sony Computer Entertainment for the PlayStation 2 in 2002. It is the first
    game in the Ratchet & Clank series and the first game developed by Insomniac to not be owned by Universal
    Interactive.
    """
    game = "Ratchet & Clank"
    web = RacWeb()
    options_dataclass = RacOptions
    options: RacOptions
    topology_present = False
    item_name_to_id = {item.name: item.item_id for item in Items.ALL}
    location_name_to_id = {location.name: location.location_id for location in Planets.ALL_LOCATIONS if
                           location.location_id}
    item_name_groups = Items.get_item_groups()
    location_name_groups = location_groups
    item_pool: dict[str, list[Item]] = {}
    starting_planet = Items.NOVALIS_INFOBOT.name
    preplaced_items: list[Item] = []
    orders: dict[str, list[int]] = {}

    def get_filler_item_name(self) -> str:
        return get_bolt_pack(self.options)

    def generate_early(self) -> None:
        #rac_logger.debug(f"_________START EARLY GENERATION____________")
        rac_logger.warning(
            "INCOMPLETE WORLD! Slot '%s' is using an unfinished alpha world that is not stable yet!",
            self.player_name)
        rac_logger.warning("INCOMPLETE WORLD! Slot '%s' may require send_location/send_item for completion!",
                           self.player_name)
        self.item_pool: dict[str, list[Item]] = {}
        self.starting_planet = Items.NOVALIS_INFOBOT.name
        self.preplaced_items = []
        #rac_logger.debug(f"Pre-placed Item List: {self.preplaced_items}")
        #rac_logger.debug(f"item_pool size: {len(self.item_pool.values())}")

        shuffle_pools: list = [
            self.options.shuffle_infobots,
            self.options.shuffle_packs,
            self.options.shuffle_gadgets,
            self.options.shuffle_helmets,
            self.options.shuffle_boots,
            self.options.shuffle_weapons,
            self.options.shuffle_extra_items,
            self.options.shuffle_gold_weapons,
        ]
        disabled_pools = []
        restricted_pools = []
        useful_pools = []
        enabled_pools = []

        if self.options.shuffle_gold_bolts.value:
            enabled_pools += [POOL_GOLD_BOLT]
        else:
            disabled_pools += [POOL_GOLD_BOLT]
        # if self.options.shuffle_skill_points.value:
        #     enabled_pools += [POOL_SKILLPOINT]
        # else:
        #     disabled_pools += [POOL_SKILLPOINT]
        #rac_logger.debug(f"Iterating through Options:")
        for pool_option in shuffle_pools:
            #rac_logger.debug(f"Option: {pool_option}")
            match pool_option.value:
                case Options.ItemOptions.option_vanilla:
                    disabled_pools += [pool_option.pool]
                case Options.ItemOptions.option_random_same:
                    restricted_pools += [pool_option.pool]
                case Options.ItemOptions.option_random_item:
                    useful_pools += [pool_option.pool]
                case Options.ItemOptions.option_unrestricted:
                    enabled_pools += [pool_option.pool]

        if not enabled_pools:
            #rac_logger.debug(f"No pools enabled, setting to defaults")
            disabled_pools = [pool for pool in ALL_POOLS if pool not in DEFAULT_LIST]
            restricted_pools = []
            useful_pools = []
            enabled_pools = DEFAULT_LIST

        #rac_logger.debug(f"Disabled Pools: {disabled_pools}")
        #rac_logger.debug(f"Restricted Pools: {restricted_pools}")
        #rac_logger.debug(f"Useful Pools: {useful_pools}")
        #rac_logger.debug(f"Enabled Pools: {enabled_pools}")

        if not self.options.shuffle_gold_bolts.value:
            self.options.pack_size_gold_bolts.value = 1

        #rac_logger.debug(
            #f"Gold Bolt Pack Size: {self.options.pack_size_gold_bolts.value}, Bolt pack size: "
            #f"{self.options.pack_size_bolts.value}")

        #rac_logger.debug(f"Choose Progression Order")
        self.orders = {
            "progressive_suck_cannon_order": [Items.SUCK_CANNON.item_id, Items.GOLDEN_SUCK_CANNON.item_id],
            "progressive_bomb_glove_order": [Items.BOMB_GLOVE.item_id, Items.GOLDEN_BOMB_GLOVE.item_id],
            "progressive_devastator_order": [Items.DEVASTATOR.item_id, Items.GOLDEN_DEVASTATOR.item_id],
            "progressive_blaster_order": [Items.BLASTER.item_id, Items.GOLDEN_BLASTER.item_id],
            "progressive_pyrocitor_order": [Items.PYROCITOR.item_id, Items.GOLDEN_PYROCITOR.item_id],
            "progressive_mine_glove_order": [Items.MINE_GLOVE.item_id, Items.GOLDEN_MINE_GLOVE.item_id],
            "progressive_tesla_claw_order": [Items.TESLA_CLAW.item_id, Items.GOLDEN_TESLA_CLAW.item_id],
            "progressive_glove_of_doom_order": [Items.GLOVE_OF_DOOM.item_id, Items.GOLDEN_GLOVE_OF_DOOM.item_id],
            "progressive_morph_o_ray_order": [Items.MORPH_O_RAY.item_id, Items.GOLDEN_MORPH_O_RAY.item_id],
            "progressive_decoy_glove_order": [Items.DECOY_GLOVE.item_id, Items.GOLDEN_DECOY_GLOVE.item_id],
            "progressive_packs_order": [Items.HELI_PACK.item_id, Items.THRUSTER_PACK.item_id, Items.HYDRO_PACK.item_id],
            "progressive_helmets_order": [Items.O2_MASK.item_id, Items.SONIC_SUMMONER.item_id,
                                          Items.PILOTS_HELMET.item_id],
            "progressive_boots_order": [Items.GRINDBOOTS.item_id, Items.MAGNEBOOTS.item_id],
            "progressive_hoverboard_order": [Items.HOVERBOARD.item_id, Items.ZOOMERATOR.item_id],
            "progressive_raritanium_order": [Items.RARITANIUM.item_id, Items.PERSUADER.item_id],
            "progressive_nanotech_order": [Items.PREMIUM_NANOTECH.item_id, Items.ULTRA_NANOTECH.item_id],
        }
        progression_rules(self)
        #rac_logger.debug(f"Progression Order: {self.orders}")
        #rac_logger.debug(f"Creating Regions")
        create_regions(self)

        #rac_logger.debug(f"___Generate Item Pool___")
        option_list = Items.get_pool(self.options)
        #rac_logger.debug(f"length of option_list: {len(option_list)}")
        for item in option_list:
            #rac_logger.debug(f"item_pool size: {len(self.item_pool.values())}")
            item_list = self.item_pool.get(item.name) or []
            item_list.append(self.create_item(item.name))
            self.item_pool[item.name] = item_list

        #rac_logger.debug(f"item_pool size: {len(self.item_pool.values())}")
        if (self.options.shuffle_infobots == ShuffleInfobots.option_vanilla or
                self.options.starting_location == StartingLocation.option_false):
            starting_planet = self.item_pool[Items.NOVALIS_INFOBOT.name].pop(0)
        else:
            starting_planet = [planet for planet in Items.get_starting_planets(self.options)]
            self.random.shuffle(starting_planet)
            self.starting_planet = starting_planet[0].name
            starting_planet = self.item_pool[starting_planet[0].name].pop(0)
        #rac_logger.debug(f"item_pool size: {len(self.item_pool.values())}")

        if (self.options.shuffle_weapons == ShuffleWeapons.option_vanilla or
                self.options.starting_item == StartingItem.option_vanilla):
            starting_item = self.item_pool[check_progressive_item(self.options, Items.BOMB_GLOVE.name)].pop(0)
        else:
            starting_item = []
            item_list = [item.name for item in Items.STARTING_WEAPONS]
            if (self.options.starting_item == StartingItem.option_random_item and
                    self.options.shuffle_gadgets > ShuffleGadgets.option_random_same):
                item_list += [item.name for item in Items.GADGETS]
            if self.options.progressive_weapons.value is Options.GoldenWeaponProgression.option_normal:
                item_list += [item.name for item in Items.GOLDEN_WEAPONS]
            for name, item in self.item_pool.items():
                if name in item_list:
                    starting_item.extend(item)
            self.random.shuffle(starting_item)
            starting_item = self.item_pool[starting_item[0].name].pop(0)

        self.preplaced_items = [starting_item, starting_planet]
        self.multiworld.push_precollected(starting_item)
        self.multiworld.push_precollected(starting_planet)
        for name, count in self.options.start_inventory:
            #if count > len(self.item_pool[name]):
                #rac_logger.warning(f"Too many copies of {name} in yaml start inventory! Giving only "
                                   #f"{len(self.item_pool[name])} of {count} copies")
            for _ in range(count):
                if self.item_pool[name]:
                    self.preplaced_items += [self.item_pool[name].pop(0)]
                else:
                    break

        #rac_logger.debug(f"Starting items: {self.preplaced_items}")

        #rac_logger.debug(f"___Vanilla Locations___")
        self.preplaced_items += self.fill_pool(disabled_pools, 0)
        #rac_logger.debug(f"___Internal Shuffled Pools___")
        self.preplaced_items += self.fill_pool(restricted_pools, 1)
        #rac_logger.debug(f"___Group Shuffled Pools___")
        self.preplaced_items += self.fill_pool(useful_pools, 2)
        #rac_logger.debug(f"Pre-placed Items placed: {self.preplaced_items}")
        #rac_logger.debug(f"Pre-filled Locations removed: {[loc.name for loc in self.get_locations() if loc.item]}")
        #rac_logger.debug(f"_________END EARLY GENERATION____________")

    def fill_pool(self, pools, scope) -> (list, list):
        multiworld = self.multiworld
        placed_items = self.preplaced_items
        # for name in self.item_pool:
        #     if Items.from_name(name).pool == POOL_SKILLPOINT:
        #         placed_items += self.item_pool[name]
        #rac_logger.debug(f"placed_items: {placed_items}")
        unplaced_items: list[Item] = []
        for name, items in self.item_pool.items():
            #rac_logger.debug(f"Checking if {name} is unplaced")
            if items:
                if items[0].name.endswith("Gold Bolts"):
                    placed_items += self.item_pool[name]
                    continue
                elif items[0].name.endswith("Skill Point"):
                    continue
                elif items[0].name.endswith("Gold Bolt"):
                    placed_items += self.item_pool[name]
                    continue
                else:
                    #rac_logger.debug(f"Add to unplaced: {name}")
                    unplaced_items += items
        add_items: list[Item] = []
        match scope:
            case 0:
                for pool in pools:
                    #rac_logger.debug(f"Disable Pool: {pool}")
                    for loc in ALL_LOCATIONS:
                        if pool in loc.pools and loc.vanilla_item is not None:
                            if self.get_location(loc.name).item is not None:
                                raise FillError(f"Slot {self.player_name} selected vanilla {pool}, but Location:"
                                                f" {loc.name} was already filled")
                            elif pool == Items.GOLD_BOLT.pool:
                                item = self.item_pool[Items.GOLD_BOLT_1.name].pop(0)
                            elif self.item_pool[loc.vanilla_item]:
                                item = self.item_pool[loc.vanilla_item].pop(0)
                            else:
                                #rac_logger.warning(f"vanilla item {loc.vanilla_item} can't be placed at {loc.name}, "
                                                   #f"filler bolt pack placed instead")
                                item = self.create_item(get_bolt_pack(self.options))
                            self.get_location(loc.name).place_locked_item(item)
                            add_items += [item]
                            #rac_logger.debug(f"vanilla: {loc.name}, item: {item}")
            case 1:
                for pool in pools:
                    if pool == POOL_GOLDEN_WEAPON and POOL_WEAPON in pools:
                        continue
                    base_state = CollectionState(multiworld)
                    item_sweep = placed_items
                    #rac_logger.debug(f"unplaced items: {unplaced_items}")
                    for item in unplaced_items:
                        #rac_logger.debug(f"check {pool} pool: {item}")
                        item_pool = Items.from_name(item.name).pool
                        if item_pool != pool:
                            #if pool == POOL_WEAPON and POOL_GOLDEN_WEAPON in pools and item_pool == POOL_GOLDEN_WEAPON:
                                #rac_logger.debug(f"Gold Weapon skipped: {item}")
                            #else:
                                #rac_logger.debug(f"add to assumed: {item}")
                                item_sweep += [item]
                        #else:
                            #rac_logger.debug(f"{item} is in pool {pool}")
                    #rac_logger.debug(f"Assumed collected: {item_sweep}")
                    base_state = sweep_from_pool(base_state, item_sweep)
                    #rac_logger.debug(f"Restricted Pool: {pool}")
                    loc_temp = []
                    item_temp = []
                    for loc in ALL_LOCATIONS:
                        if pool in loc.pools and loc.vanilla_item is not None:
                            loc_temp += [self.get_location(loc.name)]
                            if self.item_pool[loc.vanilla_item]:
                                item_temp += [self.item_pool[loc.vanilla_item].pop(0)]
                            elif (self.starting_planet != Items.NOVALIS_INFOBOT.name and pool in
                                  Items.NOVALIS_INFOBOT.pool):
                                item_temp += [self.item_pool[Items.NOVALIS_INFOBOT.name].pop(0)]
                            else:
                                #rac_logger.warning(f"vanilla item {loc.vanilla_item} can't be shuffled into pool {pool}"
                                                   #f", filler bolt pack added instead")
                                item_temp += [self.create_item(get_bolt_pack(self.options))]
                        if pool == POOL_WEAPON and POOL_GOLDEN_WEAPON in pools:
                            if POOL_GOLDEN_WEAPON in loc.pools and loc.vanilla_item is not None:
                                loc_temp += [self.get_location(loc.name)]
                                if self.item_pool[loc.vanilla_item]:
                                    item_temp += [self.item_pool[loc.vanilla_item].pop(0)]
                                else:
                                    #rac_logger.warning(f"vanilla item {loc.vanilla_item} can't be shuffled into pool"
                                                       #f" {pool}, filler bolt pack added instead")
                                    item_temp += [self.create_item(get_bolt_pack(self.options))]
                    #rac_logger.debug(f"Randomize Locations: {loc_temp}")
                    add_items += item_temp
                    self.random.shuffle(item_temp)
                    #rac_logger.debug(f"Shuffled items: {item_temp}")
                    #rac_logger.debug(f"Reachability before Shuffle: {base_state.reachable_regions}")
                    #rac_logger.debug(f"Locations already checked: {base_state.locations_checked}")
                    reachable = [loc for loc in multiworld.get_reachable_locations(base_state, self.player)
                                 if loc in loc_temp]
                    #rac_logger.debug(f"Reachable Locations: {reachable}")
                    fill_restrictive(multiworld, base_state, loc_temp, item_temp, single_player_placement=True,
                                     lock=False, swap=True, allow_partial=False,
                                     name=f"RAC1 Restricted Item Fill: {pool}")
                    # for item in item_temp:
                    #     add_items.remove(item)
                    # if item_temp:
                    #     for loc in placed_locations:
                    #         rac_logger.debug(f"same group: {loc.name}, item: {loc.item}")
                    #     raise FillError(f"Slot {self.player_name} selected shuffle {pool} only among themselves, "
                    #                     f"but Items: {item_temp} could not get placed at Locations: {loc_temp}")
            case 2:
                loc_temp = []
                item_temp = []
                item_sweep = placed_items
                base_state = CollectionState(multiworld)
                for pool in pools:
                    #rac_logger.debug(f"add Pool: {pool}")
                    for loc in ALL_LOCATIONS:
                        if pool in loc.pools and loc.vanilla_item is not None:
                            loc_temp += [self.get_location(loc.name)]
                if loc_temp:
                    base_state = sweep_from_pool(base_state, item_sweep)
                    #rac_logger.debug(f"Randomizing Useful Locations: {loc_temp}")
                    self.random.shuffle(unplaced_items)
                    for i in range(len(loc_temp)):
                        item_temp += [self.item_pool[unplaced_items[i].name].pop(0)]
                    #rac_logger.debug(f"Shuffled items: {item_temp}")
                    add_items += item_temp
                    #rac_logger.debug(f"Reachability before Shuffle: {base_state.reachable_regions}")
                    reachable = [loc for loc in multiworld.get_reachable_locations(base_state, self.player)
                                 if loc in loc_temp]
                    #rac_logger.debug(f"Reachable Locations: {reachable}")

                    fill_restrictive(multiworld, base_state, loc_temp, item_temp, single_player_placement=True,
                                     lock=False, swap=True, allow_partial=True, name="RAC1 Useful Item Fill")
                    for item in item_temp:
                        add_items.remove(item)
                        item_list = self.item_pool.get(item.name) or []
                        item_list.append(self.create_item(item.name))
                        self.item_pool[item.name] = item_list
                    # if loc_temp:
                    #     for loc in placed_locations:
                    #         rac_logger.debug(f"any item: {loc.name}, item: {loc.item}")
                    #     if item_temp:
                    #         raise FillError(f"Slot {self.player_name} has locations requiring useful items that are "
                    #                     f"unfilled, Items: {item_temp} could not get placed at Locations: {loc_temp}")
                    #     else:
                    #         raise FillError(f"Slot {self.player_name} has locations requiring useful items that are "
                    #                     f"unfilled, No items left to get placed at Locations: {loc_temp}")
        return add_items

    def create_item(self, name: str, override: Optional[ItemClassification] = None) -> "Item":
        new_name = Items.check_progressive_item(self.options, name)
        #if new_name is not name:
            #rac_logger.warning(f"Item {name} was not initially set to its progressive item: {new_name}")
        #if name == Items.GOLD_BOLT or name == Items.BOLT_PACK:
            #rac_logger.warning(f"{name} should not be in the item pool!!! Please report")
        if override:
            return RacItem(new_name, override, self.item_name_to_id[new_name], self.player)
        item_data = Items.from_name(new_name)
        return RacItem(new_name, ItemPool.get_classification(item_data), self.item_name_to_id[new_name], self.player)

    def create_event(self, name: str) -> "Item":
        return RacItem(name, ItemClassification.progression, None, self.player)

    def get_pre_fill_items(self) -> list["Item"]:
        #rac_logger.debug(f"fetching preplaced_items")
        items = self.preplaced_items
        return items

    def create_items(self) -> None:
        #rac_logger.debug(f"_________START ITEM CREATION__________")
        #rac_logger.debug(f"item_pool size: {len(self.item_pool.values())}")
        items_to_add: list[Item] = []
        for items in self.item_pool.values():
            items_to_add.extend(items)

        # add bolt packs in whatever slots we have left
        unfilled = [i for i in self.multiworld.get_unfilled_locations(self.player) if not i.is_event]
        #rac_logger.debug(f"Items:{len(items_to_add)}, Locations:{len(unfilled)}")
        remain = len(unfilled) - len(items_to_add)
        if remain < 0:
            #rac_logger.debug(f"Items unplaced: {items_to_add}")
            #rac_logger.debug(f"Locations unfilled: {self.multiworld.get_unfilled_locations(self.player)}")
            raise FillError(f"Item Count: {len(items_to_add)} exceeds Location count: "
                            f"{len(self.multiworld.get_unfilled_locations(self.player))}")
        elif remain == 0:
            pass
        else:
            #rac_logger.debug(f"Not enough items to fill all locations. Adding {remain} filler items to the item pool")
            for _ in range(remain):
                items_to_add.append(self.create_item(get_bolt_pack(self.options)))
        #rac_logger.debug(f"Add item pool to multiworld: {items_to_add}")
        self.multiworld.itempool.extend(items_to_add)
        #rac_logger.debug(f"_________END ITEM CREATION__________")

    def set_rules(self) -> None:
        boss_location = self.multiworld.get_location(Locations.VELDIN_DREK.name, self.player)
        boss_location.place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        # def generate_output(self, output_directory: str) -> None:
        #     aprac2 = Rac2ProcedurePatch(player=self.player, player_name=self.multiworld.get_player_name(self.player))
        #     generate_patch(self, aprac2)
        #     rom_path = os.path.join(output_directory,
        #                             f"{self.multiworld.get_out_file_name_base(self.player)}{
        #                             aprac2.patch_file_ending}")
        # aprac2.write(rom_path)

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data: dict[str, Any] = {}
        slot_data |= Options.get_options_as_dict(self.options)
        slot_data["starting_planet"] = self.item_name_to_id[self.starting_planet]
        for item, value in self.orders.items():
            slot_data[item] = value
        return slot_data

    # def post_fill(self) -> None:
    #    from Utils import visualize_regions
    #    visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.player_name}_world.puml",
    #                      regions_to_highlight=self.multiworld.get_all_state(False).reachable_regions[
    #                          self.player])
