from BaseClasses import ItemClassification, Item, MultiWorld

from enum import IntEnum
import json
from typing import NamedTuple


class LocationTiers(IntEnum):
    """
    Tier enum for locations to determine treasure quality.
    """
    LOW = 0,
    LOW_MID = 1,
    MID = 2,
    MID_HIGH = 3,
    HIGH_AWESOME = 4,
    SEALED = 5,
    NONE = 6


class ItemTiers(IntEnum):
    """
    Tier enum for treasure quality.
    """
    LOW_GEAR = 0
    LOW_CONSUMABLE = 1
    PASSABLE_GEAR = 2
    PASSABLE_CONSUMABLE = 3
    MID_GEAR = 4
    MID_CONSUMABLE = 5
    GOOD_GEAR = 6
    GOOD_CONSUMABLE = 7
    HIGH_GEAR = 8
    HIGH_CONSUMABLE = 9
    AWESOME_GEAR = 10
    AWESOME_CONSUMABLE = 11
    SEALED_TREASURE = 12


class ItemData(NamedTuple):
    """
    Store the data associated with a Chrono Trigger item.
    """
    name: str
    code: int
    item_type: str
    classification: ItemClassification


class CTJoTItemManager:
    """
    Manage item data.
    """
    _item_data_map_by_name: dict[str, ItemData] = {}
    _item_data_map_by_id: dict[int, ItemData] = {}
    _ITEM_ID_START = 5100000

    # Key items that lead to go mode or other progression
    _progression_items = ["Toma's Pop", "Bent Hilt", "Bent Sword",
                          "Dreamstone", "Ruby Knife", "Gate Key",
                          "Pendant", "Moon Stone", "PrismShard",
                          "C. Trigger", "Hero Medal", "Tools",
                          "JetsOfTime", "Grand Leon", "Clone",
                          "Jerky", "Robo's Rbn"]

    # Key items that are useful, but not progression
    _useful_items = ["Fragment"]

    # Some items to be used for junk fill in case more items are needed
    # TODO: May need to pick more filler items at some point.
    #       We make as many items as we have locations, so these "shouldn't" be
    #       necessary, but use Mop as a filler just in case.
    _junk_fill_items = ["Mop"]

    _characters = ["Crono", "Marle", "Lucca", "Robo", "Frog", "Ayla", "Magus"]

    _valid_item_difficulties = ["Easy", "Normal", "Hard"]

    # TODO: I'm not a huge fan of giant lists of item/location IDs, but I also don't want
    #       to have to fully reimplement the randomizer's treasure types/logic here.
    # Gear/consumable  IDs per item tier.
    _filler_item_tiers = [
        # low gear
        [149, 152, 153, 151, 150, 164, 2, 3, 18, 19, 32, 33, 47, 48, 60, 126, 127, 128, 92, 93, 94, 95, 96, 97],
        # low consumables
        [189, 190, 198, 199, 200, 201],
        # passable gear
        [171, 166, 156, 180, 172, 4, 5, 15, 185, 20, 34, 35, 49, 129, 130, 98, 99, 100, 101],
        # passable consumables
        [190, 192],
        # mid gear
        [168, 169, 160, 167, 157, 158, 159, 6, 7, 8, 21, 22, 36, 37, 50, 51, 52, 62, 63, 76, 131, 132, 139,
         102, 103, 117, 118, 119, 120, 121],
        # mid consumables
        [191, 193, 202, 203, 204],
        # good gear
        [173, 181, 182, 183, 161, 162, 170, 9, 10, 16, 23, 24, 38, 41, 53, 54, 64, 67, 77, 133, 136, 146, 147,
         104, 105, 113, 114, 115, 116],
        # good consumables
        [191, 194, 196],
        # high gear
        [154, 155, 163, 186, 11, 12, 13, 25, 26, 39, 55, 56, 65, 78, 137, 138, 140, 141, 142, 106, 110, 112],
        # high consumables
        [195, 196, 205, 206, 207],
        # awesome gear
        [187, 14, 83, 84, 85, 40, 57, 145, 134, 143, 108, 122, 109, 107],
        # awesome consumables
        [195, 197],
        # sealed treasure
        # Sealed chests have a massive list of possible gear/consumables
        # ranging from mid to awesome quality
        [168, 169, 160, 167, 157, 158, 159, 6, 7, 8, 21, 22, 36, 37, 50, 51, 52, 62, 63, 76, 131,
         132, 139, 102, 103, 117, 118, 119, 120, 121, 154, 173, 181, 182, 183, 161, 162, 170, 9,
         10, 16, 23, 24, 38, 41, 53, 54, 64, 67, 77, 133, 136, 146, 147, 104, 105, 113, 114, 115,
         116, 155, 163, 186, 11, 12, 13, 25, 26, 39, 55, 56, 65, 78, 137, 138, 140, 141, 142,
         106, 110, 112, 187, 14, 83, 84, 85, 40, 57, 145, 134, 143, 108, 122, 109, 107, 191, 193,
         202, 203, 204, 194, 196, 195, 197, 205, 206, 207]
    ]

    # Mapping of location tiers to location IDs within those tiers
    _location_tier_mapping: dict[LocationTiers, list[int]] = {
        LocationTiers.LOW: [86, 87, 105, 106, 88, 89, 90, 91, 107, 108, 109, 94, 95, 96, 92, 93, 110, 111, 112,
                            113, 114],
        LocationTiers.LOW_MID: [100, 101, 102, 103, 218, 115, 116, 117, 118, 119, 121, 130, 131, 132, 133, 134,
                                135, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 129, 122, 123, 124,
                                125, 126, 127, 128],
        LocationTiers.MID: [209, 210, 211, 212, 213, 214, 215, 216, 217, 54, 55, 120, 136, 137, 220, 221, 222, 223,
                            224, 225, 226, 227, 228, 229, 230, 80, 81, 82, 83, 84, 85, 56, 57, 58, 59, 60, 174, 175,
                            176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 187, 188, 189, 257, 258, 260, 17, 28],
        LocationTiers.MID_HIGH: [73, 74, 75, 219, 231, 232, 233, 234, 235, 236, 237, 238, 239, 150, 151, 152, 153,
                                 154, 23, 24, 25, 26, 16, 27, 42, 43, 44, 47, 48, 49, 50, 51, 52, 53, 242, 20, 21,
                                 22, 243, 244, 245, 246, 29, 30, 31, 32, 33, 34, 35, 36, 45, 46, 247, 248, 249, 250,
                                 37, 38, 39, 40, 259, 261, 262, 263, 264, 285, 286, 287, 288, 289, 290, 291, 76, 77,
                                 78, 294, 295, 296, 297, 298, 299, 14, 15, 18, 19, 41, 62, 79, 97, 98, 99, 104, 149,
                                 186, 190, 191, 312, 313],
        LocationTiers.HIGH_AWESOME: [155, 156, 157, 158, 240, 251, 252, 253, 254, 255, 256, 265, 266, 267, 268, 269,
                                     270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 284, 2, 3, 4,
                                     5, 6, 7, 8, 9, 10, 11, 1, 12, 13, 292, 293],
        LocationTiers.SEALED: [63, 64, 65, 66, 67, 69, 68, 70, 71, 72, 159, 164, 160, 161, 165, 166, 162, 168, 163,
                               167, 169, 170, 171, 172, 173]
    }

    # treasure distributions by item difficulty
    _easy_treasures = {
        LocationTiers.LOW: [
            (5,
             _filler_item_tiers[ItemTiers.PASSABLE_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.MID_CONSUMABLE]),
            (6,
             _filler_item_tiers[ItemTiers.PASSABLE_GEAR] +
             _filler_item_tiers[ItemTiers.MID_GEAR])
        ],
        LocationTiers.LOW_MID: [
            (50,
             _filler_item_tiers[ItemTiers.MID_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.GOOD_CONSUMABLE]
             ),
            (15, _filler_item_tiers[ItemTiers.GOOD_GEAR]),
            (45, _filler_item_tiers[ItemTiers.MID_GEAR])
        ],
        LocationTiers.MID: [
            (50,
             _filler_item_tiers[ItemTiers.GOOD_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.HIGH_CONSUMABLE]),
            (3, _filler_item_tiers[ItemTiers.AWESOME_GEAR]),
            (12, _filler_item_tiers[ItemTiers.HIGH_GEAR]),
            (45, _filler_item_tiers[ItemTiers.GOOD_GEAR])
        ],
        LocationTiers.MID_HIGH: [
            (50,
             _filler_item_tiers[ItemTiers.GOOD_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.HIGH_CONSUMABLE]),
            (3, _filler_item_tiers[ItemTiers.AWESOME_GEAR]),
            (12, _filler_item_tiers[ItemTiers.HIGH_GEAR]),
            (45, _filler_item_tiers[ItemTiers.GOOD_GEAR])
        ],
        LocationTiers.HIGH_AWESOME: [
            (50,
             _filler_item_tiers[ItemTiers.GOOD_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.HIGH_CONSUMABLE]),
            (3, _filler_item_tiers[ItemTiers.AWESOME_GEAR]),
            (12, _filler_item_tiers[ItemTiers.HIGH_GEAR]),
            (45, _filler_item_tiers[ItemTiers.GOOD_GEAR])
        ]
    }

    _normal_treasures = {
        LocationTiers.LOW: [
            (50, _filler_item_tiers[ItemTiers.LOW_CONSUMABLE]),
            (60, _filler_item_tiers[ItemTiers.LOW_GEAR])
        ],
        LocationTiers.LOW_MID: [
            (50,
             _filler_item_tiers[ItemTiers.LOW_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.PASSABLE_CONSUMABLE]
             ),
            (15, _filler_item_tiers[ItemTiers.MID_GEAR]),
            (45, _filler_item_tiers[ItemTiers.PASSABLE_GEAR])
        ],
        LocationTiers.MID: [
            (50,
             _filler_item_tiers[ItemTiers.PASSABLE_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.MID_CONSUMABLE]),
            (3, _filler_item_tiers[ItemTiers.HIGH_GEAR]),
            (12, _filler_item_tiers[ItemTiers.GOOD_GEAR]),
            (45, _filler_item_tiers[ItemTiers.MID_GEAR])
        ],
        LocationTiers.MID_HIGH: [
            (50,
             _filler_item_tiers[ItemTiers.MID_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.GOOD_CONSUMABLE]),
            (3, _filler_item_tiers[ItemTiers.AWESOME_GEAR]),
            (12, _filler_item_tiers[ItemTiers.HIGH_GEAR]),
            (45, _filler_item_tiers[ItemTiers.GOOD_GEAR])
        ],
        LocationTiers.HIGH_AWESOME: [
            (400,
             _filler_item_tiers[ItemTiers.GOOD_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.HIGH_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.AWESOME_CONSUMABLE]),
            (175, _filler_item_tiers[ItemTiers.AWESOME_GEAR]),
            (525,
             _filler_item_tiers[ItemTiers.GOOD_GEAR] +
             _filler_item_tiers[ItemTiers.HIGH_GEAR])
        ]
    }

    _hard_treasures = {
        LocationTiers.LOW: [
            (5, _filler_item_tiers[ItemTiers.LOW_CONSUMABLE]),
            (6, _filler_item_tiers[ItemTiers.LOW_GEAR])
        ],
        LocationTiers.LOW_MID: [
            (5,
             _filler_item_tiers[ItemTiers.LOW_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.PASSABLE_CONSUMABLE]
             ),
            (6, _filler_item_tiers[ItemTiers.PASSABLE_GEAR])
        ],
        LocationTiers.MID: [
            (5,
             _filler_item_tiers[ItemTiers.PASSABLE_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.MID_CONSUMABLE]),
            (6, _filler_item_tiers[ItemTiers.MID_GEAR])
        ],
        LocationTiers.MID_HIGH: [
            (5,
             _filler_item_tiers[ItemTiers.MID_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.GOOD_CONSUMABLE]),
            (6,
             _filler_item_tiers[ItemTiers.MID_GEAR] +
             _filler_item_tiers[ItemTiers.GOOD_GEAR]),
        ],
        LocationTiers.HIGH_AWESOME: [
            (400,
             _filler_item_tiers[ItemTiers.MID_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.GOOD_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.HIGH_CONSUMABLE] +
             _filler_item_tiers[ItemTiers.AWESOME_CONSUMABLE]),
            (175, _filler_item_tiers[ItemTiers.AWESOME_GEAR]),
            (525,
             _filler_item_tiers[ItemTiers.MID_GEAR] +
             _filler_item_tiers[ItemTiers.GOOD_GEAR] +
             _filler_item_tiers[ItemTiers.HIGH_GEAR])
        ]
    }

    _sealed_treasures = [(1, _filler_item_tiers[ItemTiers.SEALED_TREASURE])]

    _tab_treasures = [
        (10, [0xCD]),  # Power Tab
        (10, [0xCE]),  # Magic Tab
        (1, [0xCF])    # Speed Tab
    ]

    _treasure_distributions = {
        "Easy": _easy_treasures,
        "Normal": _normal_treasures,
        "Hard": _hard_treasures
    }

    def __init__(self):
        self._read_item_data()

    def _read_item_data(self):
        """
        Read the item_data file and populate the item DB
        """
        import pkgutil
        items = json.loads(pkgutil.get_data(__name__, "data/item_data.json").decode())
        for item_name, item_id in items.items():
            classification = ItemClassification.progression if item_name in self._progression_items \
                else ItemClassification.progression if item_name in self._characters \
                else ItemClassification.useful if item_name in self._useful_items \
                else ItemClassification.filler
            item_data = ItemData(item_name, self._ITEM_ID_START + item_id, "CTJoTItem", classification)
            self._item_data_map_by_name[item_name] = item_data
            self._item_data_map_by_id[item_id] = item_data

    def get_item_data_by_name(self, item_name: str) -> ItemData:
        """
        Get item data for the item with the given name.

        :param item_name: The name of the item whose data is being fetched
        :return: ItemData object associated with the given item name
        """
        return self._item_data_map_by_name[item_name]

    def create_item_by_name(self, item_name: str, player: int) -> Item:
        """
        Create an AP Item for the given item id and player.

        :param item_name: Name of the item to create
        :param player: ID of the player this item is for
        :return: AP Item object for the requested item
        """
        item = self.get_item_data_by_name(item_name)
        return Item(item.name, item.classification, item.code, player)

    @staticmethod
    def create_item(player: int, item: ItemData) -> Item:
        return Item(item.name, item.classification, item.code, player)

    @staticmethod
    def create_custom_item(item_name: str, item_code: int, classification: ItemClassification, player: int):
        return Item(item_name, classification, item_code, player)

    def create_item_by_id(self, item_id: int, player: int) -> Item:
        """
        Create an AP Item for the given item id and player.

        :param item_id: ID of the item to be created
        :param player: ID of the player this item is for
        :return: AP Item object for the requested item
        """
        item = self._item_data_map_by_id[item_id]
        return Item(item.name, item.classification, item.code, player)

    def get_junk_fill_items(self) -> list[str]:
        """
        Get the list of items that can be used a junk fill.

        :return: List of item names to use for junk fill
        """
        return self._junk_fill_items

    def get_item_name_to_id_mapping(self) -> dict[str, int]:
        """
        Get a dictionary of item names to IDs for all possible items.

        :return: Dictionary mapping item names to item IDs
        """
        return {name: item.code for name, item in self._item_data_map_by_name.items()}

    @staticmethod
    def create_event_item(item_name: str, player: int) -> Item:
        """
        Create an item object for an event rather than a normal item.

        Used for creating character recruitments and victory event items.

        :param item_name: Name of the item to create
        :param player: ID of the player this item is for
        :return: AP Item object with the given name for the given player
        """
        return Item(item_name, ItemClassification.progression, None, player)

    def get_random_item_for_location(self, location_id: int, difficulty: str, tab_treasures: int,
                                     multiworld: MultiWorld, player: int) -> Item:
        """
        Get a random item suitable for the tier of the given location ID.

        :param location_id: Location ID to generate a random item for
        :param difficulty: Item difficulty chosen by the player
        :param tab_treasures: Whether to use the tab treasures item distribution
        :param player: ID of the player to create items for
        :param multiworld: Multiworld instance for this game
        :return: Random Item object for the given loation
        """

        if difficulty not in self._valid_item_difficulties:
            difficulty = "Normal"

        # Figure out which treasure tier this location belongs to
        loc_tier = LocationTiers.NONE
        for tier_locations in self._location_tier_mapping.items():
            if location_id in tier_locations[1]:
                loc_tier = tier_locations[0]
                break
        if loc_tier == LocationTiers.NONE:
            # This shouldn't be possible, but if it ever happens then raise an exception
            raise ValueError("ERROR: CTJOT Invalid location id during item creation: " + str(location_id))

        # Select the treasure distribution to use based on game mode and flags
        if tab_treasures:
            # All treasures are tabs if tabsanity is turned on
            distribution = self._tab_treasures
        elif loc_tier == LocationTiers.SEALED:
            distribution = self._sealed_treasures
        else:
            distribution = self._treasure_distributions[difficulty][loc_tier]

        # Select a treasure and create an Archipelago item from the ID
        item_id = self._weighted_random(distribution, multiworld)
        item_data = self._item_data_map_by_id[item_id]
        item = self.create_item_by_name(item_data.name, player)

        return item

    @staticmethod
    def _weighted_random(distribution: list[tuple[int, list[int]]], multiworld: MultiWorld) -> int:
        """
        Return a random item from a list of item distributions.

        :param distribution: List of tuples containing a weight and a list of item IDs
        :param multiworld: Multiworld instance for this game
        :return: A randomly chosen item ID from the given item distributions
        """
        total_weight = sum(dist[0] for dist in distribution)
        choice = multiworld.random.randrange(0, total_weight)

        temp = 0
        for dist in distribution:
            temp = temp + dist[0]

            if temp > choice:
                # This is the chosen distribution, get a random item
                return multiworld.random.choice(dist[1])

        # Something went horribly wrong!
        raise ValueError(f"CTJoT Invalid value for treasure distribution: " + str(choice))
