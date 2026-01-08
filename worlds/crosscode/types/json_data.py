"""
Types related to JSON data
"""

import typing
from typing import TypedDict, NotRequired

class ExportChestInfo(TypedDict):
    name: str
    mwids: list[int]

class ExportCutsceneInfo(TypedDict):
    path: str
    mwids: list[int]

class ExportElementInfo(TypedDict):
    mwids: list[int]

class ExportQuestInfo(TypedDict):
    mwids: list[int]

class ExportRoomInfo(TypedDict):
    chests: NotRequired[dict[str, ExportChestInfo]]
    cutscenes: NotRequired[dict[str, list[ExportCutsceneInfo]]]
    elements: NotRequired[dict[str, ExportElementInfo]]
    quests: NotRequired[dict[str, ExportQuestInfo]]

class ExportShopLocationsInfo(TypedDict):
    perItemType: dict[int, int]
    perShop: dict[str, dict[int, int]]

class ExportShopUnlocksInfo(TypedDict):
    byId: dict[int, int]
    byShop: dict[str, int]
    byShopAndId: dict[str, dict[int, int]]

class ExportShopInfo(TypedDict):
    locations: ExportShopLocationsInfo
    unlocks: ExportShopUnlocksInfo

class ExportInfo(TypedDict):
    items: dict[str, ExportRoomInfo]
    quests: dict[str, typing.Any]
    shops: ExportShopInfo
    descriptions: dict[int, dict[str, str]]
    markers: dict[int, list[dict[str, typing.Any]]]
