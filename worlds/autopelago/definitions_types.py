from typing import Literal, NotRequired, TypeAlias, TypedDict, Union

Aura = Literal[
  "well_fed",
  "lucky",
  "energized",
  "stylish",
  "smart",
  "confident",
  "upset_tummy",
  "unlucky",
  "sluggish",
  "distracted",
  "startled",
  "conspiratorial",
]


class AutopelagoItemDefinitionCls(TypedDict):
    name: str | list[str]
    rat_count: NotRequired[int]
    flavor_text: NotRequired[str]
    auras_granted: NotRequired[list[str]]


# AutopelagoItemDefinition can be in any of these formats:
# 1: [name, [aura1, aura2]]
# 2: [[name_with_lactose, lactose_intolerant_name], [aura1, aura2]]
# 3:
# - name: Yet Another Rat
#   rat_count: 1
#   flavor_text: Some flavor text that shows up nowhere for now.
#   auras_granted: [aura1, aura2]
AutopelagoItemDefinition = tuple[str | list[str], list[str]] | AutopelagoItemDefinitionCls
AutopelagoNonProgressionItemType = Literal["useful_nonprogression", "trap", "filler"]
AutopelagoGameRequirement: TypeAlias = Union[
    "AutopelagoAllRequirement", "AutopelagoAnyRequirement", "AutopelagoItemRequirement",
    "AutopelagoRatCountRequirement", "AutopelagoAnyTwoRequirement"]


class AutopelagoAllRequirement(TypedDict):
    all: list[AutopelagoGameRequirement]


class AutopelagoAnyRequirement(TypedDict):
    any: list[AutopelagoGameRequirement]


class AutopelagoAnyTwoRequirement(TypedDict):
    any_two: list[AutopelagoGameRequirement]


class AutopelagoItemRequirement(TypedDict):
    item: str


class AutopelagoRatCountRequirement(TypedDict):
    rat_count: int


class AutopelagoLandmarkRegionDefinition(TypedDict):
    name: str
    unrandomized_item: str
    requires: AutopelagoGameRequirement
    exits: list[str] | None


class AutopelagoItemKeyReferenceCls(TypedDict):
    item: str
    count: int


AutopelagoItemKeyReference = str | AutopelagoItemKeyReferenceCls


# "filler region" means that it's a region to fill out the locations, not that it's a region intended to contain filler
# items. naming things is hard >.<
class AutopelagoFillerRegionItemsDefinition(TypedDict):
    # "key" as in "item key", as in "the key of the item in the 'items' section of this file", not as in "key item",
    # even though all are, in fact, progression items.
    key: list[AutopelagoItemKeyReference]
    useful_nonprogression: int
    filler: int


class AutopelagoFillerRegionDefinition(TypedDict):
    name_template: str
    unrandomized_items: AutopelagoFillerRegionItemsDefinition
    ability_check_dc: int
    exits: list[str]


class AutopelagoRegionDefinitions(TypedDict):
    landmarks: dict[str, AutopelagoLandmarkRegionDefinition]
    fillers: dict[str, AutopelagoFillerRegionDefinition]


class AutopelagoDefinitions(TypedDict):
    items: dict[str, AutopelagoItemDefinitionCls]
    regions: AutopelagoRegionDefinitions


class AutopelagoRegionDefinition:
    key: str
    exits: list[str]
    locations: list[str]
    requires: AutopelagoAllRequirement
    landmark: bool

    def __init__(self, key: str, exits: list[str], locations: list[str], requires: AutopelagoGameRequirement,
                 landmark: bool):
        self.key = key
        self.exits = exits
        self.locations = locations
        self.requires = requires
        self.landmark = landmark
