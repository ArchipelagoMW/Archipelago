from dataclasses import fields
from logging import warning
from typing import Any, TypedDict, ClassVar, TextIO

from BaseClasses import Location, Item, Tutorial, ItemClassification, MultiWorld, CollectionState
from Options import PlandoConnection, OptionError, PerGameCommonOptions, Range, Removed
from settings import Group, Bool, FilePath
from worlds.AutoWorld import WebWorld, World

from .bells import bell_location_groups, bell_location_name_to_id
from .breakables import breakable_location_name_to_id, breakable_location_groups, breakable_location_table
from .combat_logic import area_data, CombatState
from .er_data import portal_mapping, RegionInfo, tunic_er_regions
from .er_rules import set_er_location_rules
from .er_scripts import create_er_regions, verify_plando_directions
from .fuses import fuse_location_name_to_id, fuse_location_groups
from .grass import grass_location_table, grass_location_name_to_id, grass_location_name_groups, excluded_grass_locations
from .items import (item_name_to_id, item_table, item_name_groups, fool_tiers, filler_items, slot_data_item_names,
                    combat_items)
from .locations import location_table, location_name_groups, standard_location_name_to_id, hexagon_locations
from .logic_helpers import randomize_ability_unlocks, gold_hexagon
from .options import (TunicOptions, EntranceRando, tunic_option_groups, tunic_option_presets, TunicPlandoConnections,
                      LaurelsLocation, LaurelsZips, IceGrappling, LadderStorage, EntranceLayout,
                      check_options, LocalFill, get_hexagons_in_pool, HexagonQuestAbilityUnlockType)
from . import ut_stuff


class TunicSettings(Group):
    class DisableLocalSpoiler(Bool):
        """Disallows the TUNIC client from creating a local spoiler log."""

    class LimitGrassRando(Bool):
        """Limits the impact of Grass Randomizer on the multiworld by disallowing local_fill percentages below 95."""

    class UTPoptrackerPath(FilePath):
        """Path to the user's TUNIC Poptracker Pack."""
        description = "TUNIC Poptracker Pack zip file"
        required = False

    disable_local_spoiler: DisableLocalSpoiler | bool = False
    limit_grass_rando: LimitGrassRando | bool = True
    ut_poptracker_path: UTPoptrackerPath | str = UTPoptrackerPath()


class TunicWeb(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="A guide to setting up the TUNIC Randomizer for Archipelago multiworld games.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["SilentDestroyer"]
        )
    ]
    theme = "grassFlowers"
    game = "TUNIC"
    option_groups = tunic_option_groups
    options_presets = tunic_option_presets


class TunicItem(Item):
    game: str = "TUNIC"


class TunicLocation(Location):
    game: str = "TUNIC"


class SeedGroup(TypedDict):
    laurels_zips: bool  # laurels_zips value
    ice_grappling: int  # ice_grappling value
    ladder_storage: int  # ls value
    laurels_at_10_fairies: bool  # whether laurels location is set to 10 fairies
    entrance_layout: int  # entrance layout value
    has_decoupled_enabled: bool  # for checking that players don't have conflicting options
    plando: list[PlandoConnection]  # consolidated plando connections for the seed group
    bell_shuffle: bool  # off controls
    fuse_shuffle: bool  # off controls


class TunicWorld(World):
    """
    Explore a land filled with lost legends, ancient powers, and ferocious monsters in TUNIC, an isometric action game
    about a small fox on a big adventure. Stranded on a mysterious beach, armed with only your own curiosity, you will
    confront colossal beasts, collect strange and powerful items, and unravel long-lost secrets. Be brave, tiny fox!
    """
    game = "TUNIC"
    web = TunicWeb()
    author: str = "SilentSR & ScipioWright"

    options: TunicOptions
    options_dataclass = TunicOptions
    settings: ClassVar[TunicSettings]
    item_name_groups = item_name_groups
    # grass, breakables, fuses, and bells are separated out into their own files
    # this makes for easier organization, at the cost of stuff like what's directly below here
    location_name_groups = location_name_groups
    for group_name, members in grass_location_name_groups.items():
        location_name_groups.setdefault(group_name, set()).update(members)
    for group_name, members in breakable_location_groups.items():
        location_name_groups.setdefault(group_name, set()).update(members)
    for group_name, members in fuse_location_groups.items():
        location_name_groups.setdefault(group_name, set()).update(members)
    for group_name, members in bell_location_groups.items():
        location_name_groups.setdefault(group_name, set()).update(members)

    item_name_to_id = item_name_to_id
    location_name_to_id = standard_location_name_to_id.copy()
    location_name_to_id.update(grass_location_name_to_id)
    location_name_to_id.update(breakable_location_name_to_id)
    location_name_to_id.update(fuse_location_name_to_id)
    location_name_to_id.update(bell_location_name_to_id)

    player_location_table: dict[str, int]
    ability_unlocks: dict[str, int]
    slot_data_items: list[TunicItem]
    tunic_portal_pairs: dict[str, str]
    er_portal_hints: dict[int, str]
    seed_groups: dict[str, SeedGroup] = {}
    used_shop_numbers: set[int]
    er_regions: dict[str, RegionInfo]  # absolutely needed so outlet regions work

    # for the local_fill option
    fill_items: list[TunicItem]
    fill_locations: list[Location]
    backup_locations: list[Location]
    amount_to_local_fill: int

    # so we only loop the multiworld locations once
    # if these are locations instead of their info, it gives a memory leak error
    item_link_locations: dict[int, dict[str, list[tuple[int, str]]]] = {}
    player_item_link_locations: dict[str, list[Location]]

    using_ut: bool  # so we can check if we're using UT only once
    passthrough: dict[str, Any]
    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml
    tracker_world: ClassVar = ut_stuff.tracker_world

    def generate_early(self) -> None:
        # if you have multiple APWorlds, we want it to fail here instead of at the end of gen
        try:
            int(self.settings.disable_local_spoiler)
        except AttributeError:
            raise Exception("You have a TUNIC APWorld in your lib/worlds folder and custom_worlds folder.\n"
                            "This would cause an error at the end of generation.\n"
                            "Please remove one of them, most likely the one in lib/worlds.")

        # hidden option for me to do multi-slot test gens with random options more easily
        if self.options.all_random:
            for option_name in (attr.name for attr in fields(TunicOptions)
                                if attr not in fields(PerGameCommonOptions)):
                option = getattr(self.options, option_name)
                if option_name == "all_random":
                    continue
                if isinstance(option, Removed):
                    continue
                if option.supports_weighting:
                    if isinstance(option, Range):
                        option.value = self.random.randint(option.range_start, option.range_end)
                    else:
                        option.value = self.random.choice(list(option.name_lookup))

        check_options(self)
        self.er_regions = tunic_er_regions.copy()
        # empty plando connections if ER is off
        if self.options.plando_connections and not self.options.entrance_rando:
            self.options.plando_connections.value = ()
        # modify direction and order of plando connections for more consistency later on
        if self.options.plando_connections:
            def replace_connection(old_cxn: PlandoConnection, new_cxn: PlandoConnection, index: int) -> None:
                self.options.plando_connections.value.remove(old_cxn)
                self.options.plando_connections.value.insert(index, new_cxn)

            for index, cxn in enumerate(self.options.plando_connections):
                replacement = None
                if self.options.decoupled:
                    # flip any that are pointing to exit to point to entrance so that I don't have to deal with it
                    if cxn.direction == "exit":
                        replacement = PlandoConnection(cxn.exit, cxn.entrance, "entrance", cxn.percentage)
                    # if decoupled is on and you plando'd an entrance to itself but left the direction as both
                    if cxn.direction == "both" and cxn.entrance == cxn.exit:
                        replacement = PlandoConnection(cxn.entrance, cxn.exit, "entrance")
                # if decoupled is off, just convert these to both
                elif cxn.direction != "both":
                    replacement = PlandoConnection(cxn.entrance, cxn.exit, "both", cxn.percentage)

                if replacement:
                    replace_connection(cxn, replacement, index)

                if (self.options.entrance_layout == EntranceLayout.option_direction_pairs
                        and not verify_plando_directions(cxn)):
                    raise OptionError(f"TUNIC: Player {self.player_name} has invalid plando connections. "
                                      f"They have Direction Pairs enabled and the connection "
                                      f"{cxn.entrance} --> {cxn.exit} does not abide by this option.")

        ut_stuff.setup_options_from_slot_data(self)

        self.player_location_table = standard_location_name_to_id.copy()

        # setup our defaults for the local_fill option
        if self.options.local_fill == -1:
            if self.options.grass_randomizer:
                if self.options.breakable_shuffle:
                    self.options.local_fill.value = 96
                else:
                    self.options.local_fill.value = 95
            elif self.options.breakable_shuffle:
                self.options.local_fill.value = 40
            else:
                self.options.local_fill.value = 0

        if self.options.local_fill > 0 and self.settings.limit_grass_rando:
            # discard grass from non_local if it's meant to be limited
            self.options.non_local_items.value.discard("Grass")

        if self.options.grass_randomizer:
            if self.settings.limit_grass_rando and self.options.local_fill < 95 and self.multiworld.players > 1:
                raise OptionError(f"TUNIC: Player {self.player_name} has their Local Fill option set too low. "
                                  f"They must either bring it above 95% or the host needs to disable limit_grass_rando "
                                  f"in their host.yaml settings")

            self.player_location_table.update(grass_location_name_to_id)

        if self.options.breakable_shuffle:
            if self.options.entrance_rando:
                self.player_location_table.update(breakable_location_name_to_id)
            else:
                self.player_location_table.update({name: num for name, num in breakable_location_name_to_id.items()
                                                   if not name.startswith("Purgatory")})

        if self.options.shuffle_fuses:
            self.player_location_table.update(fuse_location_name_to_id)

        if self.options.shuffle_bells:
            self.player_location_table.update(bell_location_name_to_id)

    @classmethod
    def stage_generate_early(cls, multiworld: MultiWorld) -> None:
        tunic_worlds: tuple[TunicWorld] = multiworld.get_game_worlds("TUNIC")
        for tunic in tunic_worlds:
            # setting up state combat logic stuff, see has_combat_reqs for its use
            # and this is magic so pycharm doesn't like it, unfortunately
            if tunic.options.combat_logic:
                multiworld.state.tunic_need_to_reset_combat_from_collect[tunic.player] = False
                multiworld.state.tunic_need_to_reset_combat_from_remove[tunic.player] = False
                multiworld.state.tunic_area_combat_state[tunic.player] = {}
                for area_name in area_data.keys():
                    multiworld.state.tunic_area_combat_state[tunic.player][area_name] = CombatState.unchecked

            # if it's one of the options, then it isn't a custom seed group
            if tunic.options.entrance_rando.value in EntranceRando.options.values():
                continue
            group = tunic.options.entrance_rando.value
            # if this is the first world in the group, set the rules equal to its rules
            if group not in cls.seed_groups:
                cls.seed_groups[group] = \
                    SeedGroup(laurels_zips=bool(tunic.options.laurels_zips),
                              ice_grappling=tunic.options.ice_grappling.value,
                              ladder_storage=tunic.options.ladder_storage.value,
                              laurels_at_10_fairies=tunic.options.laurels_location == LaurelsLocation.option_10_fairies,
                              entrance_layout=tunic.options.entrance_layout.value,
                              has_decoupled_enabled=bool(tunic.options.decoupled),
                              plando=tunic.options.plando_connections.value.copy(),
                              bell_shuffle=bool(tunic.options.shuffle_bells),
                              fuse_shuffle=bool(tunic.options.shuffle_fuses))
                continue
            # I feel that syncing this one is worse than erroring out
            if bool(tunic.options.decoupled) != cls.seed_groups[group]["has_decoupled_enabled"]:
                raise OptionError(f"TUNIC: All players in the seed group {group} must "
                                  f"have Decoupled either enabled or disabled.")
            # off is more restrictive
            if not tunic.options.laurels_zips:
                cls.seed_groups[group]["laurels_zips"] = False
            # lower value is more restrictive
            if tunic.options.ice_grappling < cls.seed_groups[group]["ice_grappling"]:
                cls.seed_groups[group]["ice_grappling"] = tunic.options.ice_grappling.value
            # lower value is more restrictive
            if tunic.options.ladder_storage.value < cls.seed_groups[group]["ladder_storage"]:
                cls.seed_groups[group]["ladder_storage"] = tunic.options.ladder_storage.value
            # laurels at 10 fairies changes logic for secret gathering place placement
            if tunic.options.laurels_location == 3:
                cls.seed_groups[group]["laurels_at_10_fairies"] = True
            # off is more restrictive
            if not tunic.options.shuffle_bells:
                cls.seed_groups[group]["bell_shuffle"] = False
            # off is more restrictive
            if not tunic.options.shuffle_fuses:
                cls.seed_groups[group]["fuse_shuffle"] = False
            # fixed shop and direction pairs override standard, but conflict with each other
            if tunic.options.entrance_layout:
                if cls.seed_groups[group]["entrance_layout"] == EntranceLayout.option_standard:
                    cls.seed_groups[group]["entrance_layout"] = tunic.options.entrance_layout.value
                elif cls.seed_groups[group]["entrance_layout"] != tunic.options.entrance_layout.value:
                    raise OptionError(f"TUNIC: Conflict between seed group {group}'s Entrance Layout options. "
                                      f"Seed group cannot have both Fixed Shop and Direction Pairs enabled.")
            if tunic.options.plando_connections:
                # loop through the connections in the player's yaml
                for index, player_cxn in enumerate(tunic.options.plando_connections):
                    new_cxn = True
                    for group_cxn in cls.seed_groups[group]["plando"]:
                        # verify that it abides by direction pairs if enabled
                        if (cls.seed_groups[group]["entrance_layout"] == EntranceLayout.option_direction_pairs
                                and not verify_plando_directions(player_cxn)):
                            player_dir = "<->" if player_cxn.direction == "both" else "-->"
                            raise Exception(f"TUNIC: Conflict between Entrance Layout option and Plando Connection: "
                                            f"{player_cxn.entrance} {player_dir} {player_cxn.exit}")
                        # check if this pair is the same as a pair in the group already
                        if ((player_cxn.entrance == group_cxn.entrance and player_cxn.exit == group_cxn.exit)
                            or (player_cxn.entrance == group_cxn.exit and player_cxn.exit == group_cxn.entrance
                                and "both" in [player_cxn.direction, group_cxn.direction])):
                            new_cxn = False
                            # if the group's was one-way and the player's was two-way, we replace the group's now
                            if player_cxn.direction == "both" and group_cxn.direction == "entrance":
                                cls.seed_groups[group]["plando"].remove(group_cxn)
                                cls.seed_groups[group]["plando"].insert(index, player_cxn)
                            break
                        is_mismatched = (
                            player_cxn.entrance == group_cxn.entrance and player_cxn.exit != group_cxn.exit
                            or player_cxn.exit == group_cxn.exit and player_cxn.entrance != group_cxn.entrance
                        )
                        if not tunic.options.decoupled:
                            is_mismatched = is_mismatched or (
                                player_cxn.entrance == group_cxn.exit and player_cxn.exit != group_cxn.entrance
                                or player_cxn.exit == group_cxn.entrance and player_cxn.entrance != group_cxn.exit
                            )
                        if is_mismatched:
                            group_dir = "<->" if group_cxn.direction == "both" else "-->"
                            player_dir = "<->" if player_cxn.direction == "both" else "-->"
                            raise OptionError(f"TUNIC: Conflict between seed group {group}'s plando "
                                              f"connection {group_cxn.entrance} {group_dir} {group_cxn.exit} and "
                                              f"{tunic.player_name}'s plando connection "
                                              f"{player_cxn.entrance} {player_dir} {player_cxn.exit}")
                    if new_cxn:
                        cls.seed_groups[group]["plando"].append(player_cxn)

    def create_item(self, name: str, classification: ItemClassification = None) -> TunicItem:
        item_data = item_table[name]
        # evaluate alternate classifications based on options
        # it'll choose whichever classification isn't None first in this if else tree
        itemclass: ItemClassification = (classification
                                         or (item_data.combat_ic if self.options.combat_logic else None)
                                         or (ItemClassification.progression | ItemClassification.useful
                                             if name == "Glass Cannon"
                                             and (self.options.grass_randomizer or self.options.breakable_shuffle)
                                             and not self.options.start_with_sword else None)
                                         or (ItemClassification.progression | ItemClassification.useful
                                             if name == "Shield" and self.options.ladder_storage
                                             and not self.options.ladder_storage_without_items else None)
                                         or item_data.classification)
        return TunicItem(name, itemclass, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        tunic_items: list[TunicItem] = []
        self.slot_data_items = []

        items_to_create: dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_table.items()}

        # Calculate number of hexagons in item pool
        if self.options.hexagon_quest:
            items_to_create[gold_hexagon] = get_hexagons_in_pool(self)

        for money_fool in fool_tiers[self.options.fool_traps]:
            items_to_create["Fool Trap"] += items_to_create[money_fool]
            items_to_create[money_fool] = 0

        # creating these after the fool traps are made mostly so we don't have to mess with it
        if self.options.breakable_shuffle:
            for loc_data in breakable_location_table.values():
                if not self.options.entrance_rando and loc_data.er_region == "Purgatory":
                    continue
                items_to_create[f"Money x{self.random.randint(1, 5)}"] += 1

        if self.options.start_with_sword:
            self.multiworld.push_precollected(self.create_item("Sword"))

        if self.options.sword_progression:
            items_to_create["Stick"] = 0
            items_to_create["Sword"] = 0
        else:
            items_to_create["Sword Upgrade"] = 0

        if self.options.laurels_location:
            laurels = self.create_item("Hero's Laurels")
            if self.options.laurels_location == "6_coins":
                self.get_location("Coins in the Well - 6 Coins").place_locked_item(laurels)
            elif self.options.laurels_location == "10_coins":
                self.get_location("Coins in the Well - 10 Coins").place_locked_item(laurels)
            elif self.options.laurels_location == "10_fairies":
                self.get_location("Secret Gathering Place - 10 Fairy Reward").place_locked_item(laurels)
            items_to_create["Hero's Laurels"] = 0

        if self.options.grass_randomizer:
            items_to_create["Grass"] = len(grass_location_table)
            for grass_location in excluded_grass_locations:
                self.get_location(grass_location).place_locked_item(self.create_item("Grass"))
            items_to_create["Grass"] -= len(excluded_grass_locations)

        if self.options.keys_behind_bosses:
            rgb_hexagons = list(hexagon_locations.keys())
            # shuffle these in case not all are placed in hex quest
            self.random.shuffle(rgb_hexagons)
            for rgb_hexagon in rgb_hexagons:
                location = hexagon_locations[rgb_hexagon]
                if self.options.hexagon_quest:
                    if items_to_create[gold_hexagon] > 0:
                        hex_item = self.create_item(gold_hexagon)
                        items_to_create[gold_hexagon] -= 1
                        items_to_create[rgb_hexagon] = 0
                        self.get_location(location).place_locked_item(hex_item)
                else:
                    hex_item = self.create_item(rgb_hexagon)
                    self.get_location(location).place_locked_item(hex_item)
                    items_to_create[rgb_hexagon] = 0

        # Filler items in the item pool
        available_filler: list[str] = [filler for filler in items_to_create if items_to_create[filler] > 0 and
                                       item_table[filler].classification == ItemClassification.filler]

        # Remove filler to make room for other items
        def remove_filler(amount: int) -> None:
            for _ in range(amount):
                if not available_filler:
                    fill = "Fool Trap"
                else:
                    fill = self.random.choice(available_filler)
                if items_to_create[fill] == 0:
                    raise Exception("No filler items left to accommodate options selected. Turn down fool trap amount.")
                items_to_create[fill] -= 1
                if items_to_create[fill] == 0:
                    available_filler.remove(fill)

        if self.options.shuffle_ladders:
            ladder_count = 0
            for item_name, item_data in item_table.items():
                if item_data.item_group == "Ladders":
                    items_to_create[item_name] = 1
                    ladder_count += 1
            remove_filler(ladder_count)

        if self.options.shuffle_fuses:
            for item_name, item_data in item_table.items():
                if item_data.item_group == "Fuses":
                    if item_name == "Cathedral Elevator Fuse" and self.options.entrance_rando:
                        tunic_items.append(self.create_item(item_name, ItemClassification.useful))
                        continue
                    items_to_create[item_name] = 1

        if self.options.shuffle_bells:
            for item_name, item_data in item_table.items():
                if item_data.item_group == "Bells":
                    items_to_create[item_name] = 1

        if self.options.hexagon_quest:
            # Replace pages and normal hexagons with filler
            for replaced_item in list(filter(lambda item: "Pages" in item or item in hexagon_locations, items_to_create)):
                if replaced_item in item_name_groups["Abilities"] and self.options.ability_shuffling \
                        and self.options.hexagon_quest_ability_type == "pages":
                    continue
                filler_name = self.get_filler_item_name()
                items_to_create[filler_name] += items_to_create[replaced_item]
                if items_to_create[filler_name] >= 1 and filler_name not in available_filler:
                    available_filler.append(filler_name)
                items_to_create[replaced_item] = 0

            remove_filler(items_to_create[gold_hexagon])

            if not self.options.combat_logic:
                # Sort for deterministic order
                for hero_relic in sorted(item_name_groups["Hero Relics"]):
                    tunic_items.append(self.create_item(hero_relic, ItemClassification.useful))
                    items_to_create[hero_relic] = 0

        if not self.options.ability_shuffling:
            # Sort for deterministic order
            for page in sorted(item_name_groups["Abilities"]):
                if items_to_create[page] > 0:
                    tunic_items.append(self.create_item(page, ItemClassification.useful))
                    items_to_create[page] = 0
        # if ice grapple logic is on, probably really want icebolt
        elif self.options.ice_grappling:
            page = "Pages 52-53 (Icebolt)"
            if items_to_create[page] > 0:
                tunic_items.append(self.create_item(page, ItemClassification.progression | ItemClassification.useful))
                items_to_create[page] = 0

        if self.options.maskless:
            tunic_items.append(self.create_item("Scavenger Mask", ItemClassification.useful))
            items_to_create["Scavenger Mask"] = 0

        if self.options.lanternless:
            tunic_items.append(self.create_item("Lantern", ItemClassification.useful))
            items_to_create["Lantern"] = 0

        for item, quantity in items_to_create.items():
            for _ in range(quantity):
                tunic_items.append(self.create_item(item))

        for tunic_item in tunic_items:
            if tunic_item.name in slot_data_item_names:
                self.slot_data_items.append(tunic_item)

        # pull out the filler so that we can place it manually during pre_fill
        self.fill_items = []
        if self.options.local_fill > 0 and self.multiworld.players > 1:
            all_filler: list[TunicItem] = []
            non_filler: list[TunicItem] = []
            for tunic_item in tunic_items:
                if (tunic_item.excludable
                        and tunic_item.name not in self.options.local_items
                        and tunic_item.name not in self.options.non_local_items):
                    all_filler.append(tunic_item)
                else:
                    non_filler.append(tunic_item)
            self.amount_to_local_fill = int(self.options.local_fill.value * len(all_filler) / 100)
            self.fill_items += all_filler[:self.amount_to_local_fill]
            del all_filler[:self.amount_to_local_fill]
            tunic_items = all_filler + non_filler

        self.multiworld.itempool += tunic_items

    def pre_fill(self) -> None:
        if self.options.local_fill > 0 and self.multiworld.players > 1:
            # we need to reserve a couple locations so that we don't fill up every sphere 1 location
            sphere_one_locs = self.multiworld.get_reachable_locations(CollectionState(self.multiworld), self.player)
            reserved_locations: set[Location] = set(self.random.sample(sphere_one_locs, 2))
            viable_locations = [loc for loc in self.multiworld.get_unfilled_locations(self.player)
                                if loc not in reserved_locations
                                and loc.name not in self.options.priority_locations.value]

            if len(viable_locations) < self.amount_to_local_fill:
                raise OptionError(f"TUNIC: Not enough locations for local_fill option for {self.player_name}. "
                                  f"This is likely due to excess plando or priority locations.")
            self.random.shuffle(viable_locations)
            self.fill_locations = viable_locations[:self.amount_to_local_fill]
            self.backup_locations = viable_locations[self.amount_to_local_fill:]

    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld) -> None:
        tunic_fill_worlds: list[TunicWorld] = [world for world in multiworld.get_game_worlds("TUNIC")
                                               if world.options.local_fill.value > 0]
        if tunic_fill_worlds and multiworld.players > 1:
            grass_fill: list[TunicItem] = []
            non_grass_fill: list[TunicItem] = []
            grass_fill_locations: list[Location] = []
            non_grass_fill_locations: list[Location] = []
            backup_grass_locations: list[Location] = []
            backup_non_grass_locations: list[Location] = []
            for world in tunic_fill_worlds:
                if world.options.grass_randomizer:
                    grass_fill.extend(world.fill_items)
                    grass_fill_locations.extend(world.fill_locations)
                    backup_grass_locations.extend(world.backup_locations)
                else:
                    non_grass_fill.extend(world.fill_items)
                    non_grass_fill_locations.extend(world.fill_locations)
                    backup_non_grass_locations.extend(world.backup_locations)

            multiworld.random.shuffle(grass_fill)
            multiworld.random.shuffle(non_grass_fill)
            multiworld.random.shuffle(grass_fill_locations)
            multiworld.random.shuffle(non_grass_fill_locations)
            multiworld.random.shuffle(backup_grass_locations)
            multiworld.random.shuffle(backup_non_grass_locations)

            # these are slots that filled in TUNIC locations during pre_fill
            out_of_spec_worlds = set()

            for filler_item in grass_fill:
                loc_to_fill = grass_fill_locations.pop()
                try:
                    loc_to_fill.place_locked_item(filler_item)
                except Exception:
                    out_of_spec_worlds.add(multiworld.worlds[loc_to_fill.item.player].game)
                    for loc in backup_grass_locations:
                        if not loc.item:
                            loc.place_locked_item(filler_item)
                            break
                        else:
                            out_of_spec_worlds.add(multiworld.worlds[loc_to_fill.item.player].game)
                    else:
                        raise Exception("TUNIC: Could not fulfill local_filler option. This issue is caused by another "
                                        "world filling TUNIC locations during pre_fill.\n"
                                        "Archipelago does not allow us to place items into the item pool after "
                                        "create_items, so we cannot recover from this issue.\n"
                                        f"This is likely caused by the following world(s): {out_of_spec_worlds}.\n"
                                        f"Please let the world dev(s) for the listed world(s) know that there is an "
                                        f"issue there.\n"
                                        "As a workaround, you can try setting the local_filler option lower for "
                                        "TUNIC slots with Breakable Shuffle or Grass Rando enabled. You may be able to "
                                        "try generating again, as it may not happen every generation.")

            for filler_item in non_grass_fill:
                loc_to_fill = non_grass_fill_locations.pop()
                try:
                    loc_to_fill.place_locked_item(filler_item)
                except Exception:
                    out_of_spec_worlds.add(multiworld.worlds[loc_to_fill.item.player].game)
                    for loc in backup_non_grass_locations:
                        if not loc.item:
                            loc.place_locked_item(filler_item)
                            break
                        else:
                            out_of_spec_worlds.add(multiworld.worlds[loc_to_fill.item.player].game)
                    else:
                        raise Exception("TUNIC: Could not fulfill local_filler option. This issue is caused by another "
                                        "world filling TUNIC locations during pre_fill.\n"
                                        "Archipelago does not allow us to place items into the item pool after "
                                        "create_items, so we cannot recover from this issue.\n"
                                        f"This is likely caused by the following world(s): {out_of_spec_worlds}.\n"
                                        f"Please let the world dev(s) for the listed world(s) know that there is an "
                                        f"issue there.\n"
                                        "As a workaround, you can try setting the local_filler option lower for "
                                        "TUNIC slots with Breakable Shuffle or Grass Rando enabled. You may be able to "
                                        "try generating again, as it may not happen every generation.")
            if out_of_spec_worlds:
                warning("TUNIC: At least one other world has filled TUNIC locations during pre_fill. This may "
                        "cause issues for games that rely on placing items in their own world during pre_fill.\n"
                        f"This is likely being caused by the following world(s): {out_of_spec_worlds}.\n"
                        "Please let the world dev(s) for the listed world(s) know that there is an issue there.")

    def create_regions(self) -> None:
        self.tunic_portal_pairs = {}
        self.er_portal_hints = {}
        self.ability_unlocks = randomize_ability_unlocks(self)

        # stuff for universal tracker support, can be ignored for standard gen
        if self.using_ut and self.options.hexagon_quest_ability_type == "hexagons":
            self.ability_unlocks["Pages 24-25 (Prayer)"] = self.passthrough["Hexagon Quest Prayer"]
            self.ability_unlocks["Pages 42-43 (Holy Cross)"] = self.passthrough["Hexagon Quest Holy Cross"]
            self.ability_unlocks["Pages 52-53 (Icebolt)"] = self.passthrough["Hexagon Quest Icebolt"]

        portal_pairs = create_er_regions(self)
        if self.options.entrance_rando:
            # these get interpreted by the game to tell it which entrances to connect
            for portal1, portal2 in portal_pairs.items():
                self.tunic_portal_pairs[portal1.scene_destination()] = portal2.scene_destination()

    def set_rules(self) -> None:
        set_er_location_rules(self)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)

    # cache whether you can get through combat logic areas
    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        if change and self.options.combat_logic and item.name in combat_items:
            state.tunic_need_to_reset_combat_from_collect[self.player] = True
        return change

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if change and self.options.combat_logic and item.name in combat_items:
            state.tunic_need_to_reset_combat_from_remove[self.player] = True
        return change

    def write_spoiler_header(self, spoiler_handle: TextIO):
        if (self.options.hexagon_quest and self.options.ability_shuffling
                and self.options.hexagon_quest_ability_type == HexagonQuestAbilityUnlockType.option_hexagons):
            spoiler_handle.write("\nAbility Unlocks (Hexagon Quest):\n")
            for ability in self.ability_unlocks:
                # Remove parentheses for better readability
                spoiler_handle.write(f'{ability[ability.find("(")+1:ability.find(")")]}: {self.ability_unlocks[ability]} Gold Questagons\n')

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        if self.options.entrance_rando:
            hint_data.update({self.player: {}})
            # all state seems to have efficient paths
            all_state = self.multiworld.get_all_state(True)
            all_state.update_reachable_regions(self.player)
            paths = all_state.path
            portal_names = {portal.name for portal in portal_mapping}.union({f"Shop Portal {i + 1}" for i in range(500)})
            for location in self.multiworld.get_locations(self.player):
                # skipping event locations
                if not location.address:
                    continue
                path_to_loc = []
                previous_name = "placeholder"
                try:
                    name, connection = paths[location.parent_region]
                except KeyError:
                    # logic bug, proceed with warning since it takes a long time to update AP
                    warning(f"{location.name} is not logically accessible for {self.player_name}. "
                            "Creating entrance hint Inaccessible. Please report this to the TUNIC rando devs. "
                            "If you are using Plando Items (excluding early locations), then this is likely the cause.")
                    hint_text = "Inaccessible"
                else:
                    while connection != ("Menu", None):
                        name, connection = connection
                        # for LS entrances, we just want to give the portal name
                        if "(LS)" in name:
                            name = name.split(" (LS) ", 1)[0]
                        # was getting some cases like Library Grave -> Library Grave -> other place
                        if name in portal_names and name != previous_name:
                            previous_name = name
                            path_to_loc.append(name)
                    hint_text = " -> ".join(reversed(path_to_loc))

                if hint_text:
                    hint_data[self.player][location.address] = hint_text

    def get_real_location(self, location: Location) -> tuple[str, int]:
        # if it's not in a group, it's not in an item link
        if location.player not in self.multiworld.groups or not location.item:
            return location.name, location.player
        try:
            loc = self.player_item_link_locations[location.item.name].pop()
            return loc.name, loc.player
        except IndexError:
            warning(f"TUNIC: Failed to parse item location for in-game hints for {self.player_name}. "
                    f"Using a potentially incorrect location name instead.")
            return location.name, location.player

    def fill_slot_data(self) -> dict[str, Any]:
        slot_data: dict[str, Any] = {
            "seed": self.random.randint(0, 2147483647),
            "start_with_sword": self.options.start_with_sword.value,
            "keys_behind_bosses": self.options.keys_behind_bosses.value,
            "sword_progression": self.options.sword_progression.value,
            "ability_shuffling": self.options.ability_shuffling.value,
            "hexagon_quest": self.options.hexagon_quest.value,
            "hexagon_quest_ability_type": self.options.hexagon_quest_ability_type.value,
            "fool_traps": self.options.fool_traps.value,
            "laurels_zips": self.options.laurels_zips.value,
            "ice_grappling": self.options.ice_grappling.value,
            "ladder_storage": self.options.ladder_storage.value,
            "ladder_storage_without_items": self.options.ladder_storage_without_items.value,
            "lanternless": self.options.lanternless.value,
            "maskless": self.options.maskless.value,
            "entrance_rando": int(bool(self.options.entrance_rando.value)),
            "decoupled": self.options.decoupled.value if self.options.entrance_rando else 0,
            "shuffle_ladders": self.options.shuffle_ladders.value,
            "shuffle_fuses": self.options.shuffle_fuses.value,
            "shuffle_bells": self.options.shuffle_bells.value,
            "grass_randomizer": self.options.grass_randomizer.value,
            "combat_logic": self.options.combat_logic.value,
            "Hexagon Quest Prayer": self.ability_unlocks["Pages 24-25 (Prayer)"],
            "Hexagon Quest Holy Cross": self.ability_unlocks["Pages 42-43 (Holy Cross)"],
            "Hexagon Quest Icebolt": self.ability_unlocks["Pages 52-53 (Icebolt)"],
            "Hexagon Quest Goal": self.options.hexagon_goal.value,
            "Entrance Rando": self.tunic_portal_pairs,
            "disable_local_spoiler": int(self.settings.disable_local_spoiler or self.multiworld.is_race),
            "breakable_shuffle": self.options.breakable_shuffle.value,
        }

        # this would be in a stage if there was an appropriate stage for it
        self.player_item_link_locations = {}
        groups = self.multiworld.get_player_groups(self.player)
        # checking if groups so that this doesn't run if the player isn't in a group
        if groups:
            if not self.item_link_locations:
                tunic_worlds: tuple[TunicWorld] = self.multiworld.get_game_worlds("TUNIC")
                # figure out our groups and the items in them
                for tunic in tunic_worlds:
                    for group in self.multiworld.get_player_groups(tunic.player):
                        self.item_link_locations.setdefault(group, {})
                for location in self.multiworld.get_locations():
                    if location.item and location.item.player in self.item_link_locations.keys():
                        (self.item_link_locations[location.item.player].setdefault(location.item.name, [])
                         .append((location.player, location.name)))

            # if item links are on, set up the player's personal item link locations, so we can pop them as needed
            for group, item_links in self.item_link_locations.items():
                if group in groups:
                    for item_name, locs in item_links.items():
                        self.player_item_link_locations[item_name] = \
                            [self.multiworld.get_location(location_name, player) for player, location_name in locs]

        for tunic_item in filter(lambda item: item.location is not None and item.code is not None, self.slot_data_items):
            if tunic_item.name not in slot_data:
                slot_data[tunic_item.name] = []
            if tunic_item.name == gold_hexagon and len(slot_data[gold_hexagon]) >= 6:
                continue
            slot_data[tunic_item.name].extend(self.get_real_location(tunic_item.location))

        for start_item in self.options.start_inventory_from_pool:
            if start_item in slot_data_item_names:
                if start_item not in slot_data:
                    slot_data[start_item] = []
                for _ in range(self.options.start_inventory_from_pool[start_item]):
                    slot_data[start_item].extend(["Your Pocket", self.player])

        return slot_data

    # for the universal tracker, doesn't get called in standard gen
    # docs: https://github.com/FarisTheAncient/Archipelago/blob/tracker/worlds/tracker/docs/re-gen-passthrough.md
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        # we are using re_gen_passthrough over modifying the world here due to complexities with ER
        return slot_data
