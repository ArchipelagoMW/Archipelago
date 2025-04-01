from typing import Dict, List, Any, Tuple, TypedDict, ClassVar, Union, Set, TextIO
from logging import warning
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification, MultiWorld, CollectionState
from .items import (item_name_to_id, item_table, item_name_groups, fool_tiers, filler_items, slot_data_item_names,
                    combat_items)
from .locations import location_table, location_name_groups, standard_location_name_to_id, hexagon_locations, sphere_one
from .rules import set_location_rules, set_region_rules, randomize_ability_unlocks, gold_hexagon
from .er_rules import set_er_location_rules
from .regions import tunic_regions
from .er_scripts import create_er_regions
from .grass import grass_location_table, grass_location_name_to_id, grass_location_name_groups, excluded_grass_locations
from .er_data import portal_mapping, RegionInfo, tunic_er_regions
from .options import (TunicOptions, EntranceRando, tunic_option_groups, tunic_option_presets, TunicPlandoConnections,
                      LaurelsLocation, LogicRules, LaurelsZips, IceGrappling, LadderStorage, check_options,
                      get_hexagons_in_pool, HexagonQuestAbilityUnlockType)
from .breakables import breakable_location_name_to_id, breakable_location_groups, breakable_location_table
from .combat_logic import area_data, CombatState
from worlds.AutoWorld import WebWorld, World
from Options import PlandoConnection, OptionError
from settings import Group, Bool


class TunicSettings(Group):
    class DisableLocalSpoiler(Bool):
        """Disallows the TUNIC client from creating a local spoiler log."""

    class LimitGrassRando(Bool):
        """Limits the impact of Grass Randomizer on the multiworld by disallowing local_fill percentages below 95."""

    disable_local_spoiler: Union[DisableLocalSpoiler, bool] = False
    limit_grass_rando: Union[LimitGrassRando, bool] = True


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
    laurels_at_10_fairies: bool  # laurels location value
    fixed_shop: bool  # fixed shop value
    plando: TunicPlandoConnections  # consolidated plando connections for the seed group


class TunicWorld(World):
    """
    Explore a land filled with lost legends, ancient powers, and ferocious monsters in TUNIC, an isometric action game
    about a small fox on a big adventure. Stranded on a mysterious beach, armed with only your own curiosity, you will
    confront colossal beasts, collect strange and powerful items, and unravel long-lost secrets. Be brave, tiny fox!
    """
    game = "TUNIC"
    web = TunicWeb()

    options: TunicOptions
    options_dataclass = TunicOptions
    settings: ClassVar[TunicSettings]
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups
    for group_name, members in grass_location_name_groups.items():
        location_name_groups.setdefault(group_name, set()).update(members)
    for group_name, members in breakable_location_groups.items():
        location_name_groups.setdefault(group_name, set()).update(members)

    item_name_to_id = item_name_to_id
    location_name_to_id = standard_location_name_to_id.copy()
    location_name_to_id.update(grass_location_name_to_id)
    location_name_to_id.update(breakable_location_name_to_id)

    player_location_table: Dict[str, int]
    ability_unlocks: Dict[str, int]
    slot_data_items: List[TunicItem]
    tunic_portal_pairs: Dict[str, str]
    er_portal_hints: Dict[int, str]
    seed_groups: Dict[str, SeedGroup] = {}
    shop_num: int = 1  # need to make it so that you can walk out of shops, but also that they aren't all connected
    er_regions: Dict[str, RegionInfo]  # absolutely needed so outlet regions work

    # for the local_fill option
    fill_items: List[TunicItem]
    fill_locations: List[Location]
    amount_to_local_fill: int

    # so we only loop the multiworld locations once
    # if these are locations instead of their info, it gives a memory leak error
    item_link_locations: Dict[int, Dict[str, List[Tuple[int, str]]]] = {}
    player_item_link_locations: Dict[str, List[Location]]

    using_ut: bool  # so we can check if we're using UT only once
    passthrough: Dict[str, Any]
    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml

    def generate_early(self) -> None:
        try:
            int(self.settings.disable_local_spoiler)
        except AttributeError:
            raise Exception("You have a TUNIC APWorld in your lib/worlds folder and custom_worlds folder.\n"
                            "This would cause an error at the end of generation.\n"
                            "Please remove one of them, most likely the one in lib/worlds.")

        check_options(self)

        if self.options.logic_rules >= LogicRules.option_no_major_glitches:
            self.options.laurels_zips.value = LaurelsZips.option_true
            self.options.ice_grappling.value = IceGrappling.option_medium
            if self.options.logic_rules.value == LogicRules.option_unrestricted:
                self.options.ladder_storage.value = LadderStorage.option_medium

        self.er_regions = tunic_er_regions.copy()
        if self.options.plando_connections:
            for index, cxn in enumerate(self.options.plando_connections):
                # making shops second to simplify other things later
                if cxn.entrance.startswith("Shop"):
                    replacement = PlandoConnection(cxn.exit, "Shop Portal", "both")
                    self.options.plando_connections.value.remove(cxn)
                    self.options.plando_connections.value.insert(index, replacement)
                elif cxn.exit.startswith("Shop"):
                    replacement = PlandoConnection(cxn.entrance, "Shop Portal", "both")
                    self.options.plando_connections.value.remove(cxn)
                    self.options.plando_connections.value.insert(index, replacement)

        # Universal tracker stuff, shouldn't do anything in standard gen
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "TUNIC" in self.multiworld.re_gen_passthrough:
                self.using_ut = True
                self.passthrough = self.multiworld.re_gen_passthrough["TUNIC"]
                self.options.start_with_sword.value = self.passthrough["start_with_sword"]
                self.options.keys_behind_bosses.value = self.passthrough["keys_behind_bosses"]
                self.options.sword_progression.value = self.passthrough["sword_progression"]
                self.options.ability_shuffling.value = self.passthrough["ability_shuffling"]
                self.options.laurels_zips.value = self.passthrough["laurels_zips"]
                self.options.ice_grappling.value = self.passthrough["ice_grappling"]
                self.options.ladder_storage.value = self.passthrough["ladder_storage"]
                self.options.ladder_storage_without_items = self.passthrough["ladder_storage_without_items"]
                self.options.lanternless.value = self.passthrough["lanternless"]
                self.options.maskless.value = self.passthrough["maskless"]
                self.options.hexagon_quest.value = self.passthrough["hexagon_quest"]
                self.options.hexagon_quest_ability_type.value = self.passthrough.get("hexagon_quest_ability_type", 0)
                self.options.entrance_rando.value = self.passthrough["entrance_rando"]
                self.options.shuffle_ladders.value = self.passthrough["shuffle_ladders"]
                self.options.grass_randomizer.value = self.passthrough.get("grass_randomizer", 0)
                self.options.breakable_shuffle.value = self.passthrough.get("breakable_shuffle", 0)
                self.options.fixed_shop.value = self.options.fixed_shop.option_false
                self.options.laurels_location.value = self.options.laurels_location.option_anywhere
                self.options.combat_logic.value = self.passthrough["combat_logic"]
            else:
                self.using_ut = False
        else:
            self.using_ut = False

        self.player_location_table = standard_location_name_to_id.copy()

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

    @classmethod
    def stage_generate_early(cls, multiworld: MultiWorld) -> None:
        tunic_worlds: Tuple[TunicWorld] = multiworld.get_game_worlds("TUNIC")
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
                              fixed_shop=bool(tunic.options.fixed_shop),
                              plando=tunic.options.plando_connections)
                continue

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
            # more restrictive, overrides the option for others in the same group, which is better than failing imo
            if tunic.options.fixed_shop:
                cls.seed_groups[group]["fixed_shop"] = True

            if tunic.options.plando_connections:
                # loop through the connections in the player's yaml
                for cxn in tunic.options.plando_connections:
                    new_cxn = True
                    for group_cxn in cls.seed_groups[group]["plando"]:
                        # if neither entrance nor exit match anything in the group, add to group
                        if ((cxn.entrance == group_cxn.entrance and cxn.exit == group_cxn.exit)
                                or (cxn.exit == group_cxn.entrance and cxn.entrance == group_cxn.exit)):
                            new_cxn = False
                            break
                                   
                        # check if this pair is the same as a pair in the group already
                        is_mismatched = (
                            cxn.entrance == group_cxn.entrance and cxn.exit != group_cxn.exit
                            or cxn.entrance == group_cxn.exit and cxn.exit != group_cxn.entrance
                            or cxn.exit == group_cxn.entrance and cxn.entrance != group_cxn.exit
                            or cxn.exit == group_cxn.exit and cxn.entrance != group_cxn.entrance
                        )
                        if is_mismatched:
                            raise Exception(f"TUNIC: Conflict between seed group {group}'s plando "
                                            f"connection {group_cxn.entrance} <-> {group_cxn.exit} and "
                                            f"{tunic.player_name}'s plando connection {cxn.entrance} <-> {cxn.exit}")
                    if new_cxn:
                        cls.seed_groups[group]["plando"].value.append(cxn)

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
        tunic_items: List[TunicItem] = []
        self.slot_data_items = []

        items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_table.items()}

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
        available_filler: List[str] = [filler for filler in items_to_create if items_to_create[filler] > 0 and
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
            # skip items marked local or non-local, let fill deal with them in its own way
            # discard grass from non_local if it's meant to be limited
            if self.settings.limit_grass_rando:
                self.options.non_local_items.value.discard("Grass")
            all_filler: List[TunicItem] = []
            non_filler: List[TunicItem] = []
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
            reserved_locations: Set[str] = set(self.random.sample(sphere_one, 2))
            viable_locations = [loc for loc in self.multiworld.get_unfilled_locations(self.player)
                                if loc.name not in reserved_locations
                                and loc.name not in self.options.priority_locations.value]

            if len(viable_locations) < self.amount_to_local_fill:
                raise OptionError(f"TUNIC: Not enough locations for local_fill option for {self.player_name}. "
                                  f"This is likely due to excess plando or priority locations.")
            self.random.shuffle(viable_locations)
            self.fill_locations = viable_locations[:self.amount_to_local_fill]

    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld) -> None:
        tunic_fill_worlds: List[TunicWorld] = [world for world in multiworld.get_game_worlds("TUNIC")
                                               if world.options.local_fill.value > 0]
        if tunic_fill_worlds and multiworld.players > 1:
            grass_fill: List[TunicItem] = []
            non_grass_fill: List[TunicItem] = []
            grass_fill_locations: List[Location] = []
            non_grass_fill_locations: List[Location] = []
            for world in tunic_fill_worlds:
                if world.options.grass_randomizer:
                    grass_fill.extend(world.fill_items)
                    grass_fill_locations.extend(world.fill_locations)
                else:
                    non_grass_fill.extend(world.fill_items)
                    non_grass_fill_locations.extend(world.fill_locations)

            multiworld.random.shuffle(grass_fill)
            multiworld.random.shuffle(non_grass_fill)
            multiworld.random.shuffle(grass_fill_locations)
            multiworld.random.shuffle(non_grass_fill_locations)

            for filler_item in grass_fill:
                multiworld.push_item(grass_fill_locations.pop(), filler_item, collect=False)

            for filler_item in non_grass_fill:
                multiworld.push_item(non_grass_fill_locations.pop(), filler_item, collect=False)

    def create_regions(self) -> None:
        self.tunic_portal_pairs = {}
        self.er_portal_hints = {}
        self.ability_unlocks = randomize_ability_unlocks(self)

        # stuff for universal tracker support, can be ignored for standard gen
        if self.using_ut:
            self.ability_unlocks["Pages 24-25 (Prayer)"] = self.passthrough["Hexagon Quest Prayer"]
            self.ability_unlocks["Pages 42-43 (Holy Cross)"] = self.passthrough["Hexagon Quest Holy Cross"]
            self.ability_unlocks["Pages 52-53 (Icebolt)"] = self.passthrough["Hexagon Quest Icebolt"]

        # Most non-standard options use ER regions
        if (self.options.entrance_rando or self.options.shuffle_ladders or self.options.combat_logic
                or self.options.grass_randomizer or self.options.breakable_shuffle):
            portal_pairs = create_er_regions(self)
            if self.options.entrance_rando:
                # these get interpreted by the game to tell it which entrances to connect
                for portal1, portal2 in portal_pairs.items():
                    self.tunic_portal_pairs[portal1.scene_destination()] = portal2.scene_destination()
        else:
            # uses the original rules, easier to navigate and reference
            for region_name in tunic_regions:
                region = Region(region_name, self.player, self.multiworld)
                self.multiworld.regions.append(region)

            for region_name, exits in tunic_regions.items():
                region = self.get_region(region_name)
                region.add_exits(exits)

            for location_name, location_id in self.player_location_table.items():
                region = self.get_region(location_table[location_name].region)
                location = TunicLocation(self.player, location_name, location_id, region)
                region.locations.append(location)

            victory_region = self.get_region("Spirit Arena")
            victory_location = TunicLocation(self.player, "The Heir", None, victory_region)
            victory_location.place_locked_item(TunicItem("Victory", ItemClassification.progression, None, self.player))
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
            victory_region.locations.append(victory_location)

    def set_rules(self) -> None:
        # same reason as in create_regions
        if (self.options.entrance_rando or self.options.shuffle_ladders or self.options.combat_logic
                or self.options.grass_randomizer or self.options.breakable_shuffle):
            set_er_location_rules(self)
        else:
            set_region_rules(self)
            set_location_rules(self)

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
        if self.options.hexagon_quest and self.options.ability_shuffling\
                and self.options.hexagon_quest_ability_type == HexagonQuestAbilityUnlockType.option_hexagons:
            spoiler_handle.write("\nAbility Unlocks (Hexagon Quest):\n")
            for ability in self.ability_unlocks:
                # Remove parentheses for better readability
                spoiler_handle.write(f'{ability[ability.find("(")+1:ability.find(")")]}: {self.ability_unlocks[ability]} Gold Questagons\n')

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]) -> None:
        if self.options.entrance_rando:
            hint_data.update({self.player: {}})
            # all state seems to have efficient paths
            all_state = self.multiworld.get_all_state(True)
            all_state.update_reachable_regions(self.player)
            paths = all_state.path
            portal_names = [portal.name for portal in portal_mapping]
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

    def get_real_location(self, location: Location) -> Tuple[str, int]:
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

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
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
            "shuffle_ladders": self.options.shuffle_ladders.value,
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
                tunic_worlds: Tuple[TunicWorld] = self.multiworld.get_game_worlds("TUNIC")
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

        for plando_item in self.multiworld.plando_items[self.player]:
            if plando_item["from_pool"]:
                items_to_find = set()
                for item_type in [key for key in ["item", "items"] if key in plando_item]:
                    for item in plando_item[item_type]:
                        items_to_find.add(item)
                for item in items_to_find:
                    if item in slot_data_item_names:
                        slot_data[item] = []
                        for item_location in self.multiworld.find_item_locations(item, self.player):
                            slot_data[item].extend(self.get_real_location(item_location))

        return slot_data

    # for the universal tracker, doesn't get called in standard gen
    # docs: https://github.com/FarisTheAncient/Archipelago/blob/tracker/worlds/tracker/docs/re-gen-passthrough.md
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        # we are using re_gen_passthrough over modifying the world here due to complexities with ER
        return slot_data
