"""
Provides the ListInfo class, which stores most of the world data during the codegen step.
"""

from collections import defaultdict
from enum import StrEnum
import typing

from BaseClasses import ItemClassification

from .parse import JsonParser
from .context import Context
from .util import BASE_ID, DYNAMIC_ITEM_AREA_OFFSET, RESERVED_ITEM_IDS
from .markers import Marker, MarkerGenerator

from ..types.items import ItemData, ProgressiveItemChainSingle, SingleItemData, ItemPoolEntry, ProgressiveItemChain
from ..types.locations import AccessInfo, LocationData
from ..types.condition import Condition, NeverCondition, RegionCondition, OrCondition, AndCondition, ShopSlotCondition
from ..types.shops import ShopData

class LocationCategory(StrEnum):
    """
    Enum of check types, used for location categorization and markers.
    """
    CHEST = "Chest"
    CUTSCENE = "Cutscene"
    ELEMENT = "Element"
    QUEST = "Quest"


class ListInfo:
    """
    The ListInfo class contains a large amount of list-type data. It is stored in this class until it is eventually used
    to generate the python files.
    """
    ctx: Context
    json_parser: JsonParser
    marker_generator: MarkerGenerator

    current_location_code: int
    current_item_code: int

    locations_data: dict[str, LocationData]
    events_data: dict[str, LocationData]
    pool_locations: list[LocationData]
    location_groups: dict[str, list[LocationData]]

    locked_locations: list[int]

    single_items_dict: dict[str, SingleItemData]
    items_dict: dict[tuple[str, int], ItemData]
    dynamic_items: dict[str, ItemData]

    item_pools: dict[str, list[ItemPoolEntry]]

    reward_amounts: dict[str, int]

    variable_definitions: dict[str, dict[str, list[Condition]]]

    shop_data: dict[str, ShopData]
    per_shop_locations: dict[str, dict[int, LocationData]]
    global_shop_locations: dict[int, LocationData]
    shop_unlock_by_id: dict[int, ItemData]
    shop_unlock_by_shop: dict[str, ItemData]
    shop_unlock_by_shop_and_id: dict[tuple[str, int], ItemData]
    global_slot_region_conditions_list: dict[str, list[Condition]]

    progressive_chains: dict[str, ProgressiveItemChain]
    progressive_items: dict[str, ItemData]

    descriptions: dict[int, dict[str, str]]

    markers: dict[str, list[Marker]]

    def __init__(self, ctx: Context):
        self.ctx = ctx

        self.json_parser = JsonParser(self.ctx)
        self.current_location_code = max(self.ctx.cached_location_ids.values(), default=BASE_ID)
        if self.current_location_code != BASE_ID:
            self.current_location_code += 1

        self.current_item_code = max(self.ctx.cached_item_ids.values(), default=BASE_ID + DYNAMIC_ITEM_AREA_OFFSET)
        if self.current_item_code != BASE_ID + DYNAMIC_ITEM_AREA_OFFSET:
            self.current_item_code += 1

        self.locations_data = {}
        self.events_data = {}
        self.pool_locations = []
        self.location_groups = defaultdict(list)

        self.locked_locations = []

        self.single_items_dict = {}
        self.items_dict = {}
        self.dynamic_items = {}

        self.item_pools = {}

        self.reward_amounts = {}

        self.shop_data = {}
        self.per_shop_locations = defaultdict(dict)
        self.global_shop_locations = {}
        self.shop_unlock_by_id = {}
        self.shop_unlock_by_shop = {}
        self.shop_unlock_by_shop_and_id = {}
        self.global_slot_region_conditions_list = {}

        self.json_parser = JsonParser(self.ctx)
        self.json_parser.single_items_dict = self.single_items_dict
        self.json_parser.items_dict = self.items_dict

        self.progressive_chains = {}
        self.progressive_items = {}

        self.descriptions = {}

        self.marker_generator = MarkerGenerator(self.ctx)
        self.markers = defaultdict(list)

        self.variable_definitions = defaultdict(dict)

    def build(self):
        """
        Builds the list data using the context provided with the program's initialization.
        """
        self.__add_item_data_list(self.ctx.rando_data["items"])

        file = self.ctx.rando_data

        if "chests" in file:
            self.__add_location_list(file["chests"], LocationCategory.CHEST)
        if "cutscenes" in file:
            self.__add_location_list(file["cutscenes"], LocationCategory.CUTSCENE)
        if "elements" in file:
            self.__add_location_list(file["elements"], LocationCategory.ELEMENT)
        if "quests" in file:
            self.__add_location_list(file["quests"], LocationCategory.QUEST, True)

        self.__add_shop_list(self.ctx.rando_data["shops"])

        self.__add_item_pool_list(file["itemPools"])

        # Add any extra items (i.e. elements) that the JSON parser ran into
        self.single_items_dict.update(self.json_parser.single_items_dict)

        for name, data in self.single_items_dict.items():
            if (name, 1) in self.items_dict:
                continue

            self.items_dict[name, 1] = ItemData(data, 1, BASE_ID + RESERVED_ITEM_IDS + data.item_id)

        self.__add_progressive_chains(file["progressiveChains"])

        self.__add_vars(self.ctx.rando_data["vars"])

    def __get_cached_location_id(self, name: str) -> typing.Optional[int]:
        """
        Check to see if the context has a cached ID. If the location has no cached ID, returns None. 
        """
        return self.ctx.cached_location_ids.get(name, None)

    def __get_or_allocate_location_id(self, name: str) -> int:
        """
        Get the cached location ID, or allocate a new one if it is not cached.
        """
        locid = self.__get_cached_location_id(name)

        if locid is None:
            locid = self.current_location_code
            self.current_location_code += 1

        return locid

    def __get_cached_item_id(self, name: str) -> typing.Optional[int]:
        """
        Check to see if the context has a cached ID for an item in the dynamically allocated area. If the item has no
        cached ID, returns None. 
        """
        return self.ctx.cached_item_ids.get(name, None)

    def __get_or_allocate_item_id(self, name: str) -> int:
        """
        Get the cached item ID, or allocate a new one if it is not cached.
        """
        item_id = self.__get_cached_item_id(name)

        if item_id is None:
            item_id = self.current_item_code
            self.current_item_code += 1

        return item_id

    def __add_location(self, name: str, raw_loc: dict[str, typing.Any], category: LocationCategory, create_event: bool = False):
        """
        Add a location to the lists.
        """
        dbentry = self.ctx.database["quests"][raw_loc["questid"]] if "questid" in raw_loc else {}
        rewards = dbentry.get("rewards", {})
        item_rewards = rewards.get("items", [])
        num_rewards = max(1, len(item_rewards))

        properties = raw_loc.get("properties", {})

        found = False

        if name in self.reward_amounts:
            if num_rewards != self.reward_amounts[name]:
                found = True
                num_rewards = 0
                raise RuntimeError(
                    f"Location of name '{name}' already exists with {self.reward_amounts[name]} rewards. "
                    "Cannot add or overwrite with {num_rewards}."
                )

        if category == LocationCategory.QUEST:
            area = dbentry["area"]
        else:
            area = raw_loc.get("location", {}).get("area", None)
        area_name = self.ctx.area_names[area]

        location_names: list[str] = []

        metadata = raw_loc.get("metadata", None)

        access_info = self.json_parser.parse_location_access_info(raw_loc)

        locked = "clearance" in raw_loc

        for idx in range(num_rewards):
            full_name = name
            if num_rewards > 1:
                full_name = full_name + f" - Reward {idx + 1}"

            location_names.append(full_name)

            locid = self.__get_or_allocate_location_id(full_name)

            loc = LocationData(
                name=full_name,
                code=locid,
                area=area,
                metadata=metadata,
                access=access_info
            )

            self.locations_data[full_name] = loc
            self.pool_locations.append(loc)
            if area != None:
                try:
                    self.location_groups[area_name].append(loc)
                    self.location_groups[f"{area_name} {category}s"].append(loc)
                except KeyError:
                    print(f"Cannot add location '{name}' in area '{area}'")

            if properties.get("alwaysQuest", False):
                self.location_groups["Always Quests"].append(loc)

            if locked:
                self.locked_locations.append(locid)

            marker = self.marker_generator.generate_marker(raw_loc, locid)

            if marker is not None:
                self.markers[area].append(marker)

        if not found and (num_rewards > 1 or create_event):
            event_name = f"{name} (Event)"
            event = LocationData(
                name=f"{name} (Event)",
                code=None,
                area=None,
                metadata=metadata,
                access=access_info,
            )
            self.events_data[event_name] = event

    def __add_location_list(self, loc_list: dict[str, dict[str, typing.Any]], category: LocationCategory, create_events: bool = False):
        """
        Add a list of locations to the list.
        """
        for name, raw_loc in loc_list.items():
            self.__add_location(name, raw_loc, category, create_events)

    def __add_item_data(self, name: str, raw_item: dict[str, typing.Any]) -> tuple[SingleItemData, ItemData]:
        """
        Add an item to the list.
        """
        single_item, item  = self.json_parser.parse_item_data(name, raw_item)
        self.single_items_dict[name] = single_item
        self.items_dict[name, 1] = item

        if "description" in raw_item:
            self.descriptions[item.combo_id] = raw_item["description"]

        return single_item, item

    def __add_shop_unlock_item(self, name: str) -> ItemData:
        prev_item = self.dynamic_items.get(name)
        if prev_item is not None:
            return prev_item

        single_item = SingleItemData(
            name=name,
            item_id=0,
            classification=ItemClassification.progression,
            unique=True
        )

        self.single_items_dict[name] = single_item

        item = ItemData(
            item=single_item,
            amount=1,
            combo_id=self.__get_or_allocate_item_id(name)
        )

        self.items_dict[name, 1] = item
        self.dynamic_items[name] = item

        return item

    def __add_shop(self, shop_display_name: str, raw_shop: dict[str, typing.Any]):
        shop_name = raw_shop["location"]["shop"]
        area = raw_shop["location"]["area"]
        area_name = self.ctx.area_names[area]
        shop_base_name = shop_display_name.split(" +")[0] # this is a hack until there are heirarchical shops

        dbentry = self.ctx.database["shops"][shop_name]

        real_name = dbentry["name"]["en_US"]

        metadata = raw_shop.get("metadata", {})
        metadata["shops"] = True
        access_info = self.json_parser.parse_location_access_info(raw_shop)

        shop_locs = self.per_shop_locations[shop_display_name]

        by_shop_name =  f"Shop Unlock: {shop_base_name}"
        by_shop_item = self.__add_shop_unlock_item(by_shop_name)
        self.shop_unlock_by_shop[shop_name] = by_shop_item
        self.descriptions[by_shop_item.combo_id] = {
            "en_US": f"Unlocks \\c[3]all item slots\\c[0] in the shop \\c[3]{real_name}\\c[0]."
        }

        for item_name in raw_shop["slots"]:
            item_data = self.ctx.rando_data["items"][item_name]

            slot_location_name = f"Shop Slot: {item_name} ({shop_display_name})"

            locid = self.__get_or_allocate_location_id(slot_location_name)

            item_id = item_data["id"]

            slot_location = LocationData(
                name=slot_location_name,
                code=locid,
                area=area,
                metadata=metadata,
                access=AccessInfo(
                    region={ name: shop_display_name for name in access_info.region },
                    cond=[ShopSlotCondition(shop_name, item_id)],
                ),
            )

            self.location_groups[area_name].append(slot_location)
            self.location_groups[f"{area_name} Shops"].append(slot_location)

            shop_locs[item_id] = slot_location
            self.locations_data[slot_location.name] = slot_location

            global_location = self.global_shop_locations.get(item_id, None)

            by_shop_and_id_name = f"Slot Unlock: {item_name} ({shop_display_name})"
            by_shop_and_id_item = self.__add_shop_unlock_item(by_shop_and_id_name)
            self.shop_unlock_by_shop_and_id[shop_name, item_id] = by_shop_and_id_item

            self.descriptions[by_shop_and_id_item.combo_id] = {
                "en_US": f"Unlocks the slot selling \\c[3]{item_name}\\c[0] in \\c[3]{real_name}\\c[0]."
            }

            if global_location is None:
                item_type_location_name = f"Global Shop Slot: {item_name}"

                locid = self.__get_cached_location_id(item_type_location_name)

                if locid is None:
                    locid = self.current_location_code
                    self.current_location_code += 1

                slot_condition = self.global_slot_region_conditions_list[item_id] = []

                global_location = LocationData(
                    name=item_type_location_name,
                    code=locid,
                    area=None,
                    metadata=metadata,
                    access=AccessInfo(
                        region={ name: "Menu" for name in access_info.region },
                        cond=[
                            OrCondition(slot_condition)
                        ],
                    ),
                )

                by_id_name = f"Global Slot Unlock: {item_name}"
                by_id_item = self.__add_shop_unlock_item(by_id_name)
                self.shop_unlock_by_id[item_id] = by_id_item
                self.global_shop_locations[item_id] = global_location

                self.locations_data[global_location.name] = global_location

                self.descriptions[by_id_item.combo_id] = {
                    "en_US": f"Unlocks slots selling \\c[3]{item_name}\\c[0] in \\c[3]all shops\\c[0]."
                }

            # Require the player to be able to reach the shop region in all modes that the shop has a region in.
            self.global_slot_region_conditions_list[item_id].append(
                AndCondition([
                    RegionCondition(None, shop_display_name),
                    ShopSlotCondition(shop_name, item_id)
                ])
            )

        self.shop_data[shop_display_name] = ShopData(
            internal_name=shop_name,
            name=shop_display_name,
            access=access_info,
            metadata=metadata
        )

    def __add_shop_list(self, loc_list: dict[str, dict[str, typing.Any]]):
        for name, raw_shop in loc_list.items():
            self.__add_shop(name, raw_shop)

    def __add_item_data_list(self, item_list: dict[str, dict[str, typing.Any]]):
        """
        Add a list of items to the list.
        """
        for name, raw_item in item_list.items():
            self.__add_item_data(name, raw_item)

    def __add_item_pool(self, name: str, raw: list[dict[str, typing.Any]]):
        """
        Add an item pool to the list of item pools.
        """
        pool: list[ItemPoolEntry] = []
        for data in raw:
            item = self.__add_reward(data["item"])
            pool.append(ItemPoolEntry(
                item=item,
                quantity=data.get("quantity", 1),
                metadata=data.get("metadata", None)
            ))

        self.item_pools[name] = pool

    def __add_item_pool_list(self, raw: dict[str, list[dict[str, typing.Any]]]):
        """
        Add a list of item pools to the list of item pools.
        """
        for name, pool in raw.items():
            self.__add_item_pool(name, pool)

    def __add_reward(self, reward: list[dict[str, typing.Any]]) -> ItemData:
        """
        Ensure an item reward is in the list of items.
        """
        item = self.json_parser.parse_reward(reward)
        key = (item.item.name, item.amount)
        if key in self.items_dict:
            item = self.items_dict[key]
        else:
            self.items_dict[key] = item
        return item

    def __add_progressive_chain_items(self, chain: ProgressiveItemChain):
        if isinstance(chain, ProgressiveItemChainSingle):
            for entry in chain.items:
                key = (entry.item.item.name, entry.item.amount)
                if key not in self.items_dict:
                    self.items_dict[key] = entry.item
        else:
            for subchain in chain.subchains:
                for entry in subchain.chain:
                    key = (entry.item.item.name, entry.item.amount)
                    if key not in self.items_dict:
                        self.items_dict[key] = entry.item

    def __add_progressive_chain(self, name: str, raw: dict[str, typing.Any]):
        """
        Add a progressive chain to the list.
        """
        chain = self.progressive_chains[name] = self.json_parser.parse_progressive_chain(name, raw)
        self.__add_progressive_chain_items(chain)
        raw["reserved"] = True
        _, item = self.__add_item_data(f"Progressive {chain.display_name}", raw)
        self.progressive_items[name] = item

    def __add_progressive_chains(self, raw: dict[str, dict[str, typing.Any]]):
        """
        Add a list of progressive chain to the list.
        """
        for name, chain in raw.items():
            self.__add_progressive_chain(name, chain)

    def __add_vars(self, variables: dict[str, str | dict[str, list[typing.Any]]]):
        """
        Add a list of variable conditions to the list..
        """
        for name, values in variables.items():
            if isinstance(values, str):
                if values == "boolean":
                    self.variable_definitions[name] = {
                        "off": [NeverCondition()],
                        "on": []
                    }
                    continue
                else:
                    raise RuntimeError(f"{values} is not a valid variable type shorthand.")
            for value, conds in values.items():
                self.variable_definitions[name][value] = self.json_parser.parse_condition(conds)
