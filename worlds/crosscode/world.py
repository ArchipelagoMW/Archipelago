"""
This module contains the world class for CrossCode.
"""

from collections import defaultdict, Counter
import typing
import logging
import itertools

from BaseClasses import ItemClassification, Location, LocationProgressType, Region, Item, MultiWorld
from Fill import fill_restrictive

from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule

from .common import NAME
from .logic import condition_satisfied
from .world_data import static_world_data

from .types.items import ItemData, CrossCodeItem
from .types.locations import CrossCodeLocation, LocationData
from .types.condition import LogicDict, Condition, LocationCondition
from .types.world import WorldData
from .types.regions import RegionsData
from .types.metadata import IncludeOptions
from .types.pools import Pools
from .types.slot import SlotData
from .options import CrossCodeOptions, ShopReceiveMode, ShopSendMode, StartWithDiscs, ProgressiveAreaUnlocks, option_groups

cclogger = logging.getLogger(__name__)

class CrossCodeWebWorld(WebWorld):
    """CrossCode is a retro-inspired 2D Action RPG set in the distant future,
    combining 16-bit SNES-style graphics with butter-smooth physics, a
    fast-paced combat system, and engaging puzzle mechanics, served with a
    gripping sci-fi story.
    """

    theme="ocean"

    tutorials = []

    bug_report_page = "https://github.com/CodeTriangle/CCMultiworldRandomizer/blob/master/README.md#how-to-get-support"

    option_groups=option_groups

class CrossCodeWorld(World):
    """CrossCode is a retro-inspired 2D Action RPG set in the distant future,
    combining 16-bit SNES-style graphics with butter-smooth physics, a
    fast-paced combat system, and engaging puzzle mechanics, served with a
    gripping sci-fi story.
    """

    game = NAME
    web = CrossCodeWebWorld()

    world_data: typing.ClassVar[WorldData] = static_world_data

    options_dataclass = CrossCodeOptions
    options: CrossCodeOptions #type: ignore
    topology_present = True

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a propery.
    base_id = world_data.base_id
    # Instead of dynamic numbering, IDs could be part of data.

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {
        key: value.combo_id for key, value in world_data.items_by_full_name.items()
    }

    location_name_to_id = {
        location.name: location.code for location in world_data.locations_dict.values() if location.code is not None
    }

    item_name_groups = {
        name: { entry.item.name for entry in entries }
        for name, entries in world_data.item_pools_template.items()
    }

    location_name_groups = {
        name: { entry.name for entry in entries }
        for name, entries in world_data.location_groups.items()
    }

    include_options: IncludeOptions
    required_items: Counter[ItemData]

    region_dict: dict[str, Region]
    logic_mode: str
    region_pack: RegionsData

    pre_fill_specific_dungeons_names: dict[str, set[str]]
    pre_fill_any_dungeon_names: set[str]

    pre_fill_specific_dungeons: dict[str, list[CrossCodeItem]]
    pre_fill_any_dungeon: list[CrossCodeItem]

    dungeon_location_list: dict[str, set[CrossCodeLocation]]
    dungeon_areas: typing.ClassVar[set[str]] = {"cold-dng", "heat-dng", "shock-dng", "wave-dng", "tree-dng"}

    logic_dict: LogicDict

    location_events: dict[str, Location]

    variables: dict[str, list[str]]

    pools_cache: typing.ClassVar[dict[tuple[tuple[str, object], ...], Pools]] = {}

    pools: Pools

    _filler_pool_names: list[str] = [
        "fillerCommonCons",
        "fillerCommonDrop",
        "fillerRareCons",
        "fillerRareDrop",
        "fillerEpicCons",
        "fillerEpicDrop",
        "fillerLegendary",
    ]

    _filler_pool_weights: list[int]

    _chest_level_names: list[str] = [ "Default", "Bronze", "Silver", "Gold" ]

    _chest_lock_weights: list[int]

    enabled_chain_names: set[str]

    _equip_chain_names = {
        'headsAllPurpose',
        'headsDefensive',
        'headsOffensive',
        'heads',
        'armsAllPurpose',
        'armsDefensive',
        'armsMelee',
        'armsRanged',
        'armsSpecial',
        'armsClassBased',
        'arms',
        'torsosAllPurpose',
        'torsosDefensive',
        'torsosMixed',
        'torsosOffensive',
        'torsos',
        'torsosClassBased',
        'legsAllPurpose',
        'legsDefensive',
        'legsOffensive',
        'legs'
    }

    def get_include_options(self) -> IncludeOptions:
        """
        The metadata dict is a dict that will be matched against the `metadata` fields in the ItemPoolEntry and Location
        classes to check for inclusion.
        """
        return {
            "trade": False,
            "shop": bool(self.options.shop_rando.value),
            "arena": False,
            "chest": True,
            "quest": bool(self.options.quest_rando.value),
        }

    def create_location(self, location: str, event_from_location: bool = False) -> CrossCodeLocation:
        """
        Create a location given a name and whether to create an event for progression purposes.
        """
        data = self.world_data.locations_dict[location]
        return CrossCodeLocation(
            self.player,
            data,
            self.logic_mode,
            self.region_dict,
            event_from_location=event_from_location
        )

    def create_item(self, name: str) -> CrossCodeItem:
        """
        Create an item given its name.
        """
        return CrossCodeItem(self.player, self.world_data.items_by_full_name[name])

    def get_filler_pool_names(self, k: int = 1) -> list[str]:
        """
        Get a list of filler pools from which you can pull.
        """
        return self.random.choices(self._filler_pool_names, cum_weights=self._filler_pool_weights, k=k)

    def get_filler_item_name(self) -> str:
        """
        Generate a random filler item name based on the weighted filler pools.
        """
        return self.pools.pull_items_from_pool(self.get_filler_pool_names()[0], self.random)[0].name

    def get_filler_item_data(self, k: int = 1) -> list[ItemData]:
        """
        Get a list of item data instances chosen randomly from the weighted filler pools.
        """
        pool_count = Counter(self.get_filler_pool_names(k))
        result: list[ItemData] = []
        for name, cnt in pool_count.items():
            result.extend(self.pools.pull_items_from_pool(name, self.random, cnt))
        return result

    def get_filler_items(self, k: int = 1) -> list[CrossCodeItem]:
        """
        Get a list of CrossCodeItem instances chosen randomly from the weighted filler pools.
        """
        return [CrossCodeItem(self.player, item) for item in self.get_filler_item_data(k)]

    def create_event_conditions(self, condition: typing.Optional[list[Condition]]):
        """
        Create events for a list containing any number of location conditions and add them to the world.
        """
        if condition is None:
            return

        for c in condition:
            if isinstance(c, LocationCondition):
                name = c.location_name
                if name in self.location_events:
                    continue
                location = self.create_location(name, event_from_location=True)
                self.location_events[name] = location
                self.region_dict[location.region].locations.append(location)
                location.place_locked_item(Item(location.name, ItemClassification.progression, None, self.player))

    def fill_pools(self):
        # do nothing if the pools are already set
        if hasattr(self, "pools"):
            return

        self.include_options = self.get_include_options()

        include_options_tuple = tuple(self.include_options.items())

        if include_options_tuple in self.pools_cache:
            self.pools = self.pools_cache[include_options_tuple]
        else:
            self.pools_cache[include_options_tuple] = self.pools = Pools(self.world_data, self.include_options)

        common = self.options.common_pool_weight.value
        rare = self.options.rare_pool_weight.value
        epic = self.options.epic_pool_weight.value
        legendary = self.options.legendary_pool_weight.value
        cons = self.options.consumable_weight.value
        drop = self.options.drop_weight.value

        # cumulative weights save work.
        self._filler_pool_weights = list(itertools.accumulate([
            common * cons,
            common * drop,
            rare * cons,
            rare * drop,
            epic * cons,
            epic * drop,
            legendary * (cons + drop),
        ]))

    def generate_early(self):
        self.fill_pools()

        self.variables = defaultdict(list)

        start_inventory = self.options.start_inventory.value
        # self.logic_mode = self.options.logic_mode.current_key
        self.logic_mode = "open"
        self.region_pack = self.world_data.region_packs[self.logic_mode]

        self.enabled_chain_names = set()

        green_leaf_shade_name = "Green Leaf Shade"

        area_unlocks = self.options.progressive_area_unlocks.value
        if area_unlocks & ProgressiveAreaUnlocks.COMBINE_POOLS:
            self.enabled_chain_names.add("areaItemsAll")
            green_leaf_shade_name = "Progressive Area Unlock"
        else:
            if area_unlocks & ProgressiveAreaUnlocks.DUNGEONS:
                self.enabled_chain_names.add("areaItemsDungeons")
            if area_unlocks & ProgressiveAreaUnlocks.OVERWORLD:
                self.enabled_chain_names.add("areaItemsOverworld")
                green_leaf_shade_name = "Progressive Overworld Area Unlock"

        if self.options.progressive_equipment.value:
            self.enabled_chain_names |= self._equip_chain_names

        self.required_items = Counter()
        self.required_items.update(self.pools.item_pools["required"])

        for name in self._equip_chain_names:
            self.required_items.update(self.pools.item_pools[f"pool:{name}"])

        if self.options.shop_rando.value:
            if self.options.shop_receive_mode == ShopReceiveMode.option_per_item_type:
                self.required_items.update(self.world_data.shop_unlock_by_id.values())
            if self.options.shop_receive_mode == ShopReceiveMode.option_per_shop:
                self.required_items.update(self.world_data.shop_unlock_by_shop.values())
            if self.options.shop_receive_mode == ShopReceiveMode.option_per_slot:
                self.required_items.update(self.world_data.shop_unlock_by_shop_and_id.values())

        if self.options.vt_shade_lock.value in [1, 2]:
            self.variables["vtShadeLock"].append("shades")
        if self.options.vt_shade_lock.value in (1, 3):
            self.variables["vtShadeLock"].append("bosses")
        if self.options.vw_meteor_passage.value:
            self.variables["vwPassage"].append("meteor")

        self.variables["canGrind"].append("noShadeWarp")

        if self.options.start_with_green_leaf_shade.value:
            self.multiworld.push_precollected(self.create_item(green_leaf_shade_name))

        if self.options.start_with_chest_detector.value:
            start_inventory["Chest Detector"] = 1

        if self.options.start_with_discs.value & StartWithDiscs.option_insight:
            start_inventory["Disc of Insight"] = 1
        if self.options.start_with_discs.value & StartWithDiscs.option_flora:
            start_inventory["Disc of Flora"] = 1

        if self.options.start_with_pet.value:
            chosen_pet = self.pools.pull_items_from_pool("pets", self.random)[0]
            start_inventory[chosen_pet.name] = 1

        if self.options.chest_lock_randomization.value:
            self._chest_lock_weights = list(itertools.accumulate([
                self.options.no_chest_lock_weight.value,
                self.options.bronze_chest_lock_weight.value,
                self.options.silver_chest_lock_weight.value,
                self.options.gold_chest_lock_weight.value,
            ]))

        if self.options.exclude_always_quests.value and not self.options.quest_rando.value:
            self.options.exclude_locations.value.update(self.location_name_groups["Always Quests"])

        self.pre_fill_any_dungeon_names = set()
        self.pre_fill_specific_dungeons_names = defaultdict(set)

        self.pre_fill_any_dungeon = []
        self.pre_fill_specific_dungeons = defaultdict(list)

        self.dungeon_location_list = defaultdict(set)

        local_items = self.options.local_items.value
        non_local_items = self.options.non_local_items.value

        for key in ("shade_shuffle", "element_shuffle", "small_key_shuffle", "master_key_shuffle", "chest_key_shuffle"):
            getattr(self.options, key).register_locality(local_items, non_local_items)

        for key in ("element_shuffle", "small_key_shuffle", "master_key_shuffle", "chest_key_shuffle"):
            getattr(self.options, key).register_pre_fill_lists(
                self.pre_fill_specific_dungeons_names,
                self.pre_fill_any_dungeon_names
            )

        self.logic_dict: LogicDict = {
            "mode": self.logic_mode,
            "variables": self.variables,
            "variable_definitions": self.world_data.variable_definitions,
            "keyrings": self.world_data.keyring_items if self.options.keyrings.value else set(),
            "item_progressive_replacements": self.pools.item_progressive_replacements,
            "chest_clearance_levels": {},
            "shop_receive_mode": self.options.shop_receive_mode.value if self.options.shop_rando.value else None,
            "shop_unlock_by_id": self.world_data.shop_unlock_by_id,
            "shop_unlock_by_shop": self.world_data.shop_unlock_by_shop,
            "shop_unlock_by_shop_and_id": self.world_data.shop_unlock_by_shop_and_id,
        }

        # Universal Tracker support
        # Anything that is generated in a non-standard fashion on my end has to be brought back into scope here from slot data.
        if hasattr(self.multiworld, "re_gen_passthrough"):
            slot_data: SlotData = self.multiworld.re_gen_passthrough["CrossCode"]
            # Reinterpret the JSON chest clearance levels dict (a string -> string mapping) as an int -> int mapping instead.
            self.logic_dict["chest_clearance_levels"] = {int(combo_id): clearance for combo_id, clearance in slot_data["options"]["chestClearanceLevels"].items()}

    @classmethod
    def create_group(cls, multiworld: "MultiWorld", new_player_id: int, players: set[int]) -> World:
        for player in players:
            multiworld.worlds[player].fill_pools()

        group = super().create_group(multiworld, new_player_id, players)
        arbitrary_player = list(players)[0]
        arbitrary_world = multiworld.worlds[arbitrary_player]
        group.pools = arbitrary_world.pools
        weights: list[int] = []
        for i in range(len(arbitrary_world._filler_pool_weights)):
            sum = 0
            for player in players:
                sum += multiworld.worlds[player]._filler_pool_weights[i]
            weights.append(sum)

        group._filler_pool_weights = weights
        return group

    def add_location(self, data: LocationData, region: Region):
        location = CrossCodeLocation(self.player, data, self.logic_mode, self.region_dict)
        if location.data.area in self.dungeon_areas:
            self.dungeon_location_list[location.data.area].add(location)
        region.locations.append(location)
        self.create_event_conditions(data.access.cond)

        if hasattr(self.multiworld, "generation_is_fake") or hasattr(self.multiworld, "re_gen_passthrough"):
            return

        if self.options.chest_lock_randomization.value and data.code in self.world_data.locked_locations:
            clearance = self.random.choices(
                self._chest_level_names,
                cum_weights=self._chest_lock_weights
            )[0]

            self.logic_dict["chest_clearance_levels"][data.code] = clearance

    def create_shops(self):
        for shop_name, shop in self.world_data.shops_dict.items():
            region = Region(shop_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)
            for mode, from_region in shop.access.region.items():
                if self.logic_mode == mode:
                    self.region_dict[from_region].connect(
                        region,
                        f"{from_region} => {shop_name}",
                        condition_satisfied(self.player, shop.access.cond, None, self.logic_dict) if shop.access.cond else None
                    )

                    if self.options.shop_send_mode == ShopSendMode.option_per_slot:
                        for data in self.world_data.per_shop_locations[shop_name].values():
                            self.add_location(data, region)

        if self.options.shop_send_mode.value == ShopSendMode.option_per_item_type:
            for data in self.world_data.global_shop_locations.values():
                self.add_location(data, self.region_dict["Menu"])

    def create_regions(self):
        self.multiworld.regions.extend(
            Region(name, self.player, self.multiworld)
            for name in self.region_pack.region_list
            if name not in self.region_pack.excluded_regions
        )
        self.region_dict = self.multiworld.regions.region_cache[self.player]
        self.location_events = {}

        for conn in self.region_pack.region_connections:
            self.region_dict[conn.region_from].connect(
                self.region_dict[conn.region_to],
                f"{conn.region_from} => {conn.region_to}",
                condition_satisfied(self.player, conn.cond, None, self.logic_dict) if conn.cond is not None else None
            )

            self.create_event_conditions(conn.cond)

        menu_region = Region("Menu", self.player, self.multiworld)
        menu_region.add_exits({self.region_pack.starting_region: "login"})
        self.multiworld.regions.append(menu_region)

        for name, region in self.region_dict.items():
            for data in self.pools.location_pool:
                if self.logic_mode in data.access.region and data.access.region[self.logic_mode] == name:
                    self.add_location(data, region)

            for data in self.pools.event_pool:
                if self.logic_mode in data.access.region and data.access.region[self.logic_mode] == name:
                    location = CrossCodeLocation(self.player, data, self.logic_mode, self.region_dict)
                    region.locations.append(location)
                    location.place_locked_item(Item(
                        location.data.name,
                        ItemClassification.progression,
                        None,
                        self.player
                    ))

            if name in self.region_pack.excluded_regions:
                for location in region.locations:
                    location.progress_type = LocationProgressType.EXCLUDED

        # also add any event conditions referenced in any possible value of a variable
        for conds in self.world_data.variable_definitions.values():
            for cond in conds.values():
                self.create_event_conditions(cond)

        if self.options.shop_rando:
            self.create_shops()

        goal_region = self.region_dict[self.region_pack.goal_region]
        goal = Location(self.player, "The Creator", parent=goal_region)
        goal.place_locked_item(Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        goal_region.locations.append(goal)

    def create_items(self):
        exclude = self.multiworld.precollected_items[self.player][:]

        # initially, we need as many items as there are locations
        num_needed_items = len(self.pools.location_pool)

        if self.options.shop_rando.value:
            if self.options.shop_send_mode.value == ShopSendMode.option_per_item_type:
                num_needed_items += len(self.world_data.global_shop_locations)
            elif self.options.shop_send_mode == ShopSendMode.option_per_slot:
                num_needed_items += sum(len(shop) for shop in self.world_data.per_shop_locations.values())

        # items that have been replaced by progressive items
        replaced: dict[str, list[CrossCodeItem]] = defaultdict(list)

        # deal with progressive chains
        for chain_name in self.enabled_chain_names:
            chain = self.pools.progressive_chains[chain_name]
            # item_to_add is the "Progressive [X]" item
            item_to_add = self.world_data.progressive_items[chain_name]

            # item_to_skip is the item that will be replaced by a progressive.
            for item_to_skip in chain:
                item = CrossCodeItem(self.player, item_to_add)
                # We note that we have replaced an item. When we create
                # items in the pool, this indicates that one of them should
                # use this item as a replacement.
                replaced[item_to_skip.name].append(item)

        for data, quantity in self.required_items.items():
            # if the item needs to be a keyring, limit its quantity to one.
            if self.options.keyrings.value and data.item.name in self.world_data.keyring_items:
                quantity = 1

            for _ in range(quantity):
                # create the item
                item = CrossCodeItem(self.player, data)

                # if there is an item to replace this with, do so.
                if item.name in replaced and len(replaced[item.name]) > 0:
                    item = replaced[item.name].pop()

                try:
                    # Check if the item is precollected.
                    # If it is, we'll need a replacement for it.
                    idx = exclude.index(item)
                    exclude.pop(idx)
                    continue
                except ValueError:
                    # If we can't find the item in the precollected list, it
                    # goes in the item pool and we need to add one less item.
                    num_needed_items -= 1

                # HOWEVER! We might not actually add the item to the pool.
                # If the item is set to be in the player's own dungeons or
                # its original dungeon, then we don't want to add it to the
                # pool after all.
                add_to_pool = True

                if item.name in self.pre_fill_any_dungeon_names:
                    self.pre_fill_any_dungeon.append(item)
                    add_to_pool = False

                for dng, names in self.pre_fill_specific_dungeons_names.items():
                    if item.name in names:
                        self.pre_fill_specific_dungeons[dng].append(item)
                        add_to_pool = False

                if add_to_pool:
                    self.multiworld.itempool.append(item)

        # Add filler items to fill up the pool.
        self.multiworld.itempool.extend(self.get_filler_items(num_needed_items))

    def set_rules(self):
        for _, region in self.region_dict.items():
            for loc in region.locations:
                if not isinstance(loc, CrossCodeLocation):
                    continue
                if loc.data.access.cond is not None:
                    add_rule(loc, condition_satisfied(self.player, loc.data.access.cond, loc.data.code, self.logic_dict))

    def pre_fill(self):
        allowed_locations_by_item: dict[Item, set[CrossCodeLocation]] = {}
        all_items_list = list(self.pre_fill_any_dungeon)
        all_locations: set[CrossCodeLocation] = set()

        for dungeon in self.dungeon_areas:
            for item in self.pre_fill_specific_dungeons[dungeon]:
                allowed_locations_by_item[item] = self.dungeon_location_list[dungeon]

            all_items_list.extend(self.pre_fill_specific_dungeons[dungeon])
            all_locations |= self.dungeon_location_list[dungeon]

        def make_item_rule(
            orig_rule: typing.Callable[[Item], bool],
            location: CrossCodeLocation
        ) -> typing.Callable[[Item], bool]:
            def result(item: Item) -> bool:
                return (
                    (
                        item not in allowed_locations_by_item or
                        location in allowed_locations_by_item[item]
                    ) and
                    orig_rule(item)
                )

            return result

        for _, locations in self.dungeon_location_list.items():
            for location in locations:
                location.item_rule = make_item_rule(location.item_rule, location)

        for item in self.pre_fill_any_dungeon:
            allowed_locations_by_item[item] = all_locations

        all_locations_list = list(all_locations)
        self.random.shuffle(all_locations_list)

        # Get the list of items and sort by priority
        def priority(item: CrossCodeItem) -> int:
            # 0 - Master dungeon-specific
            # 1 - Element dungeon-specific
            # 2 - Key dungeon-specific
            # 3 - Other dungeon-specific
            # 4 - Master any local dungeon
            # 5 - Element any local dungeon
            # 6 - Key any local dungeon
            # 7 - Other any local dungeon
            i = 3
            if item.name in ("Heat", "Cold", "Shock", "Wave"):
                i = 0
            if "Master" in item.name:
                i = 1
            elif "Key" in item.name:
                i = 2
            if allowed_locations_by_item[item] is all_locations:
                i += 4
            return i
        all_items_list.sort(key=priority)

        # Set up state
        all_state = self.multiworld.get_all_state(use_cache=False)
        # Remove dungeon items we are about to put in from the state so that we don't double count
        for item in all_items_list:
            all_state.remove(item)

        cclogger.debug("master_key_shuffle: %s", self.options.master_key_shuffle)
        cclogger.debug("small_key_shuffle: %s", self.options.small_key_shuffle)
        cclogger.debug("element_shuffle: %s", self.options.element_shuffle)
        cclogger.debug("chest_key_shuffle: %s", self.options.chest_key_shuffle)

        # Finally, fill!
        fill_restrictive(
            self.multiworld,
            all_state,
            all_locations_list,
            all_items_list,
            lock=True,
            single_player_placement=True,
            allow_partial=False,
        )

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        ours = hint_data.setdefault(self.player, {})

        for loc, clearance in self.logic_dict["chest_clearance_levels"].items():
            ours[loc] = clearance

    def fill_slot_data(self) -> SlotData:
        prog_chains = {}
        for name in self.enabled_chain_names:
            key = self.world_data.progressive_items[name].combo_id
            prog_chains[key] = [data.combo_id for data in self.pools.progressive_chains[name]]

        if self.options.shop_send_mode.value == ShopSendMode.option_per_item_type:
            shop_send_mode_string = "itemType"
        else:
            shop_send_mode_string = "slot"

        if self.options.shop_receive_mode.value == ShopReceiveMode.option_per_item_type:
            shop_receive_mode_string = "itemType"
        elif self.options.shop_receive_mode.value == ShopReceiveMode.option_per_shop:
            shop_receive_mode_string = "shop"
        elif self.options.shop_receive_mode.value == ShopReceiveMode.option_per_slot:
            shop_receive_mode_string = "slot"
        else:
            shop_receive_mode_string = "none"

        return {
            "mode": self.logic_mode,
            "dataVersion": self.world_data.data_version,
            "options": {
                "vtShadeLock": self.options.vt_shade_lock.value,
                "meteorPassage": bool(self.options.vw_meteor_passage.value),
                "vtSkip": bool(self.options.vt_skip.value),
                "keyrings": [self.world_data.single_items_dict[name].item_id for name in self.logic_dict["keyrings"]],
                "questRando": bool(self.options.quest_rando.value),
                "hiddenQuestRewardMode": self.options.hidden_quest_reward_mode.current_key,
                "hiddenQuestObfuscationLevel": self.options.hidden_quest_obfuscation_level.current_key,
                "questDialogHints": bool(self.options.quest_dialog_hints.value),
                "progressiveChains": prog_chains,
                "shopSendMode": shop_send_mode_string,
                "shopReceiveMode": shop_receive_mode_string,
                "shopDialogHints": bool(self.options.shop_dialog_hints.value),
                "chestClearanceLevels": self.logic_dict["chest_clearance_levels"],
            }
        }

    @staticmethod
    def interpret_slot_data(slot_data: SlotData) -> SlotData:
        return slot_data
