"""
Provides a memoizing parser for the JSON data.
"""

import string
import typing

from BaseClasses import ItemClassification

from .context import Context
from .util import BASE_ID, RESERVED_ITEM_IDS, get_item_classification

from ..types.items import ItemData, ProgressiveChainEntry, ProgressiveItemChain, ProgressiveItemChainSingle, ProgressiveItemChainMulti, ProgressiveItemSubchain, SingleItemData
from ..types.locations import AccessInfo, Condition
from ..types.regions import RegionConnection, RegionsData
from ..types.condition import AndCondition, ChestKeyCondition, ItemCondition, LocationCondition, NeverCondition, QuestCondition, RegionCondition, AnyElementCondition, \
    OrCondition, ShopSlotCondition, VariableCondition

class JsonParserError(Exception):
    """
    An exception to be thrown upon a failure to parse JSON data.
    """
    subject: typing.Any
    problem_item: typing.Any
    message: str

    def __init__(self, subject: typing.Any, problem_item: typing.Any, kind: str, message: str):
        self.subject = subject
        self.problem_item = problem_item
        self.message = f"Error parsing {kind}: {message}"
        super().__init__(subject, problem_item, message)

class JsonParser:
    """
    A memoizing parser for the JSON data, taking in dicts and lists and returning semantically meaningful class
    instances representing the items.
    """
    ctx: Context

    single_items_dict: dict[str, SingleItemData]
    items_dict: dict[tuple[str, int], ItemData]

    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.single_items_dict = {}
        self.items_dict = {}

    def parse_condition(self, raw: list[typing.Any]) -> list[Condition]:
        """
        Parse a list of conditions (in the form of lists) into a list of subclasses of Condition.
        """
        result: list[Condition] = []

        for cond in raw:
            if not isinstance(cond, list):
                raise JsonParserError(raw, cond, "condition", "condition not a list")

            num_args = len(cond) - 1
            if cond[0] == "item":
                if num_args == 1:
                    result.append(ItemCondition(cond[1]))
                elif num_args == 2:
                    result.append(ItemCondition(cond[1], cond[2]))
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "item condition",
                        f"expected 1 or 2 argument, not {num_args}"
                    )

            elif cond[0] == "quest":
                if num_args == 1:
                    result.append(QuestCondition(cond[1]))
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "quest condition",
                        f"expected 1 argument, not {num_args}"
                    )

            elif cond[0] in ["cutscene", "location"]:
                if num_args == 1:
                    result.append(LocationCondition(cond[1]))
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "location condition",
                        f"expected 1 argument, not {num_args}"
                    )

            elif cond[0] == "region":
                if num_args == 2:
                    mode, region = cond[1:]
                    result.append(RegionCondition(mode, region))
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "region condition",
                        f"expected 2 arguments, not {num_args}"
                    )

            elif cond[0] == "any_element":
                result.append(AnyElementCondition())

            elif cond[0] in ("any", "or"):
                result.append(OrCondition(self.parse_condition(cond[1:])))

            elif cond[0] in ("all", "and"):
                result.append(AndCondition(self.parse_condition(cond[1:])))

            elif cond[0] == "var":
                if num_args == 1:
                    result.append(VariableCondition(cond[1]))
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "location condition",
                        f"expected 1 argument, not {num_args}"
                    )

            elif cond[0] == "shop_slot":
                if num_args == 2:
                    result.append(ShopSlotCondition(cond[1], cond[2]))
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "shop slot condition",
                        f"expected 2 arguments, not {num_args}"
                    )

            elif cond[0] == "never":
                result.append(NeverCondition())

            else:
                raise JsonParserError(raw, cond, "condition", f"unknown type {cond[0]}")

        # Return None if there are no conditions
        return result

    def parse_location_access_info(self, raw: dict[str, typing.Any]) -> AccessInfo:
        """
        Take the "clearance", "region", and "condition" keys of a dict and parse them into an instance of AccessInfo.
        """
        region = {}
        if "region" in raw:
            region = raw["region"]

            if not isinstance(region, dict):
                raise JsonParserError(raw, raw["region"], "location", "region must be a dict")

            for region_name in region.values():
                if not isinstance(region_name, str):
                    raise JsonParserError(raw, region_name, "location", "region name must be a string")

        condition: list[Condition] = []
        if "condition" in raw:
            condition = self.parse_condition(raw["condition"])

        if "clearance" in raw:
            clearance = raw["clearance"]
            if not isinstance(clearance, str):
                raise JsonParserError(raw, clearance, "location", "clearance must be a string")
            condition.append(ChestKeyCondition(clearance))

        return AccessInfo(region, condition)

    def parse_item_data(self, name: str, raw: dict[str, typing.Any]) -> tuple[SingleItemData, ItemData]:
        """
        Parse an item data entry as given in ``rando_data["items"]``.

        This also uses the item database to access information about it.
        """
        item_id = raw["id"]

        db_entry = self.ctx.item_data[item_id]

        cls = get_item_classification(db_entry)

        item_type = db_entry["type"]

        if "classification" in raw:
            cls_str = raw["classification"]
            if not hasattr(ItemClassification, cls_str):
                raise JsonParserError(raw, cls_str, "item reward", "invalid classification")
            cls = getattr(ItemClassification, cls_str)

        if raw.get("reserved", False):
            single_item = SingleItemData(
                name=name,
                item_id=-RESERVED_ITEM_IDS + item_id,
                classification=cls,
                unique=True,
            )
            item = ItemData(
                item=single_item,
                amount=1,
                combo_id=BASE_ID + item_id,
            )
        else:
            single_item = SingleItemData(
                name=name,
                item_id=item_id,
                classification=cls,
                unique=raw.get("unique", not item_type == "CONS")
            )
            item = ItemData(
                item=single_item,
                amount=1
            )

        return single_item, item

    def parse_item_reward(self, raw: list[typing.Any]) -> ItemData:
        """
        Parse an item reward of the form ``["item", "Heat", 1]``.
        """
        if len(raw) == 1:
            name = raw[0]
            amount = 1
        elif len(raw) == 2:
            name = raw[0]
            amount = raw[1]
        else:
            raise JsonParserError(raw, raw, "item reward", "expected one or two elements")

        try:
            return self.items_dict[name, amount]
        except KeyError:
            pass

        try:
            single_item = self.single_items_dict[name]
        except KeyError as e:
            raise JsonParserError(raw, name, "item reward", "item does not exist in randomizer data") from e

        return ItemData(
            item=single_item,
            amount=amount,
        )

    def parse_reward(self, raw: list[typing.Any]) -> ItemData:
        """
        Parse any reward, including item rewards.
        """
        kind, *info = raw

        if kind == "item":
            return self.parse_item_reward(info)
        raise RuntimeError(f"Error parsing reward {raw}: unrecognized type")

    def __parse_progressive_itemlist(self, raw_items: list[dict[str, typing.Any]]) -> list[ProgressiveChainEntry]:
        items = []
        for entry in raw_items:
            if "item" not in entry:
                raise JsonParserError(entry, None, "progressive chain entry", "Need an 'item' property")

            metadata = entry.get("condition", None)

            items.append(ProgressiveChainEntry(
                item=self.parse_reward(entry["item"]),
                metadata=metadata,
            ))

        return items

    def __parse_progressive_subchain(self, raw: list[dict[str, typing.Any]]) -> list[ProgressiveItemSubchain]:
        subchains = []

        for entry in raw:
            metadata = entry.get("metadata", None)
            itemlist = entry.get("content", None)
            if type(itemlist) != list:
                raise JsonParserError(raw, itemlist, "progressive subchain", f"Need a list of item entries")

            subchains.append(ProgressiveItemSubchain(metadata, self.__parse_progressive_itemlist(itemlist)))

        return subchains

    def parse_progressive_chain(self, name: str, raw: dict[str, typing.Any]) -> ProgressiveItemChain:
        display_name = raw.get("displayName", None)
        if type(display_name) != str:
            raise JsonParserError(raw, display_name, "progressive chain", f"Need string display name for chain {name}")

        raw_items = raw.get("items", None)
        if type(raw_items) != list:
            raise JsonParserError(raw, raw_items, "progressive chain", f"Need list of items for chain {name}")

        if raw.get("multi", False):
            return ProgressiveItemChainMulti(
                display_name=display_name,
                subchains=self.__parse_progressive_subchain(raw_items)
            )
        else:
            return ProgressiveItemChainSingle(
                display_name=display_name,
                items=self.__parse_progressive_itemlist(raw_items),
            )



    def parse_region_connection(self, raw: dict[str, typing.Any]) -> RegionConnection:
        """
        Parse a region connection.
        """
        if "from" not in raw:
            raise JsonParserError(raw, None, "connection", "region from not found")
        region_from = raw["from"]

        if not isinstance(region_from, str):
            raise JsonParserError(raw, region_from, "connection", "region must be str")

        if "to" not in raw:
            raise JsonParserError(raw, None, "connection", "region to not found")
        region_to = raw["to"]

        if not isinstance(region_to, str):
            raise JsonParserError(raw, region_to, "connection", "region must be str")

        condition = None
        if "condition" in raw:
            condition = self.parse_condition(raw["condition"])

        return RegionConnection(region_from, region_to, condition)

    def parse_regions_data(self, raw: dict[str, typing.Any]) -> RegionsData:
        """
        Parse all the properties of a region, including the list of connections.
        """
        if "start" not in raw:
            raise JsonParserError(raw, None, "regions data", "must have starting region")
        start = raw["start"]

        if not isinstance(start, str):
            raise JsonParserError(raw, start, "regions data", "starting region must be a string")

        if "goal" not in raw:
            raise JsonParserError(raw, None, "regions data", "must have goal region")
        goal = raw["goal"]

        if not isinstance(goal, str):
            raise JsonParserError(raw, goal, "regions data", "goal region must be a string")

        exclude = []
        if "exclude" in raw:
            exclude = raw["exclude"]
            if not isinstance(exclude, list) or not all(isinstance(region, str) for region in exclude):
                raise JsonParserError(raw, exclude, "regions data", "excluded regions must be strings")

        if "connections" not in raw:
            raise JsonParserError(raw, None, "regions data", "no connections found")
        raw_connections = raw["connections"]

        if not isinstance(raw_connections, list):
            raise JsonParserError(raw, raw_connections, "regions data", "connection must be list")

        regions_seen: set[str] = set()

        connections = []

        for raw_conn in raw_connections:
            conn = self.parse_region_connection(raw_conn)
            regions_seen.add(conn.region_to)
            regions_seen.add(conn.region_from)

            connections.append(conn)

        region_list = list(regions_seen)

        region_list.sort(key=lambda x: float(x.strip(string.ascii_letters)))

        return RegionsData(start, goal, exclude, region_list, connections)

    def parse_regions_data_list(self, raw: dict[str, dict[str, typing.Any]]) -> dict[str, RegionsData]:
        """
        Parse all of the regions.
        """
        return {name: self.parse_regions_data(data) for name, data in raw.items()}
