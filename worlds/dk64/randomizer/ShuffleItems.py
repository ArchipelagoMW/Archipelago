"""Shuffles items for Item Rando."""

import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.VendorType import VendorType
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Settings import RandomPrices, ShuffleLoadingZones
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import ShopLocationReference
from randomizer.Lists.LevelInfo import LevelInfoList
from randomizer.Patching.Library.ItemRando import LocationSelection


class MoveData:
    """Class which contains information pertaining to a move's attributes."""

    def __init__(self, subtype, kong, index, shared=False, count=1):
        """Initialize with given data."""
        self.subtype = subtype
        self.kong = kong
        self.index = index
        self.shared = shared
        self.count = count


def ShuffleItems(spoiler):
    """Shuffle items into assortment."""
    progressive_move_flag_dict = {
        Items.ProgressiveSlam: [0x3BC, 0x3BD, 0x3BE],
        Items.ProgressiveAmmoBelt: [0x292, 0x293],
        Items.ProgressiveInstrumentUpgrade: [0x294, 0x295, 0x296],
    }
    flag_dict = {}
    blueprint_flag_dict = {}
    locations_not_needing_flags = []
    locations_needing_flags = []

    for location_enum in spoiler.LocationList:
        item_location = spoiler.LocationList[location_enum]
        # If location is a shuffled one...
        if (
            (
                item_location.default_mapid_data is not None
                or item_location.type in (Types.Shop, Types.Shockwave)
                or (
                    item_location.type == Types.TrainingBarrel and not item_location.constant
                )  # Depending on starting moves, training barrels can be empty (only when constant). This quick check prevents weirdness later in this method.
            )
            and (not item_location.inaccessible or item_location.type in (Types.Cranky, Types.Funky, Types.Candy, Types.Snide))  # Shopkeepers' locations are either inaccessible or vanilla
            and item_location.type in spoiler.settings.shuffled_location_types
        ):
            # Create placement info for the patcher to use
            placement_info = {}
            # Items that need specific placement in the world, either as a reward or something spawned in
            if item_location.default_mapid_data:
                for location in item_location.default_mapid_data:
                    placement_info[location.map] = location.id
                old_flag = item_location.default_mapid_data[0].flag
                old_kong = item_location.default_mapid_data[0].kong
                placement_index = [-1]  # Irrelevant for non-shop locations
            # Shop locations: Cranky, Funky, Candy, Training Barrels, and BFI
            else:
                old_flag = -1  # Irrelevant for shop locations
                # Get flag
                if item_location.type == Types.Shop:
                    for level, data in ShopLocationReference.items():
                        for vendor, loc_list in data.items():
                            if location_enum in loc_list:
                                kong = loc_list.index(location_enum)
                                if kong == 5:
                                    kong = 0  # shared
                                handled_level = level
                                if level == Levels.DKIsles:
                                    handled_level = 7
                                if vendor == VendorType.Cranky:
                                    old_flag = 0x320 + (handled_level * 5) + kong
                                elif vendor == VendorType.Funky:
                                    old_flag = 0x320 + ((8 + handled_level) * 5) + kong
                                elif vendor == VendorType.Candy:
                                    candy_index = {
                                        Levels.AngryAztec: 0,
                                        Levels.FranticFactory: 1,
                                        Levels.GloomyGalleon: 2,
                                        Levels.CrystalCaves: 3,
                                        Levels.CreepyCastle: 4,
                                    }
                                    old_flag = 0x320 + ((15 + candy_index[level]) * 5) + kong
                elif item_location.type == Types.Shockwave:
                    old_flag = 0x179
                elif item_location.type == Types.TrainingBarrel:
                    tbarrel_flags = {
                        Locations.IslesSwimTrainingBarrel: 0x182,
                        Locations.IslesBarrelsTrainingBarrel: 0x185,
                        Locations.IslesOrangesTrainingBarrel: 0x184,
                        Locations.IslesVinesTrainingBarrel: 0x183,
                    }
                    old_flag = tbarrel_flags[location_enum]
                old_kong = item_location.kong
                placement_index = item_location.placement_index
            price = 0
            if item_location.type == Types.Shop:
                # Vanilla prices are based on item, not location
                if spoiler.settings.random_prices == RandomPrices.vanilla:
                    # If it's not in the prices dictionary, the item is free
                    if item_location.item in spoiler.settings.prices.keys():
                        price = spoiler.settings.prices[item_location.item]
                else:
                    price = spoiler.settings.prices[location_enum]
            location_selection = LocationSelection(
                vanilla_item=ItemList[item_location.default].type,
                flag=old_flag,
                placement_data=placement_info,
                is_reward_point=item_location.is_reward,
                is_shop=item_location.type in (Types.Shop, Types.TrainingBarrel, Types.Shockwave, Types.Climbing),
                price=price,
                placement_index=placement_index,
                kong=old_kong,
                location=location_enum,
                name=item_location.name,
            )
            # Get the item at this location
            if item_location.item is None or item_location.item == Items.NoItem:
                new_item = None
            else:
                new_item = ItemList[item_location.item]
            # If this location isn't empty, set the new item and required kong
            if new_item is not None:
                location_selection.new_type = new_item.type
                location_selection.new_kong = new_item.kong
                location_selection.new_item = item_location.item
                # If this item has a dedicated specific flag, then set it now (Moves, Kongs, andKeys right now)
                if new_item.rando_flag is not None:
                    if new_item.rando_flag == -1:  # This means it's a progressive move or fake item and they need special flags
                        ref_item = item_location.item
                        location_selection.new_flag = progressive_move_flag_dict[ref_item].pop()
                    else:
                        location_selection.new_flag = new_item.rando_flag
                    locations_not_needing_flags.append(location_selection)
                # Company Coins keep their original flag
                elif new_item.type in (Types.NintendoCoin, Types.RarewareCoin):
                    location_selection.new_flag = new_item.flag
                    locations_not_needing_flags.append(location_selection)
                elif new_item.type in (Types.FakeItem, Types.JunkItem, Types.ArchipelagoItem, Types.FillerBanana, Types.FillerCrown, Types.FillerFairy, Types.FillerMedal, Types.FillerPearl):
                    location_selection.new_flag = 0x7FFF
                    locations_not_needing_flags.append(location_selection)
                # Otherwise we need to put it in the list of locations needing flags
                else:
                    location_selection.new_flag = 0x7FFF
                    locations_not_needing_flags.append(location_selection)
                    # locations_needing_flags.append(location_selection)
            # If this location is empty, it doesn't need a flag and we need to None out these fields
            else:
                location_selection.new_type = None
                location_selection.new_kong = None
                location_selection.new_flag = None
                locations_not_needing_flags.append(location_selection)
            # Add this location's flag to the lists of available flags by location
            # Initialize relevant list if it doesn't exist
            if item_location.type not in flag_dict.keys() and item_location.type != Types.Blueprint:
                if item_location.type == Types.IslesMedal and Types.Medal not in flag_dict.keys():
                    flag_dict[Types.Medal] = []
                else:
                    flag_dict[item_location.type] = []
            # Add this location's vanilla flag as a valid flag for this type of item/kong pairing
            vanilla_item_type = ItemList[item_location.default].type
            if item_location.type == Types.Shop:  # Except for shop locations - many of these are non-vanilla locations and won't have a valid vanilla item
                flag_dict[item_location.type].append(old_flag)
            # Link blueprint Items to their default flags stored in their Location
            elif item_location.type == Types.Blueprint:
                blueprint_flag_dict[item_location.default] = item_location.default_mapid_data[0].flag
            else:
                flag_dict[vanilla_item_type].append(old_flag)
    # Shuffle the list of locations needing flags so the flags are assigned randomly across seeds
    spoiler.settings.random.shuffle(locations_needing_flags)
    for location in locations_needing_flags:
        if location.new_flag is None:
            if location.new_type == Types.Blueprint:
                location.new_flag = blueprint_flag_dict[spoiler.LocationList[location.location].item]
            elif location.new_type:
                location.new_flag = flag_dict[location.new_type].pop()

    # If we failed to give any location a flag, something is very wrong
    if any([data for data in locations_needing_flags if data.new_flag is None]):
        [data for data in locations_needing_flags if data.new_flag is None]
        raise Ex.FillException("ERROR: Failed to create a valid flag assignment for this fill!")

    # If Keys are not shuffled but are placed as constants (e.g., SLO with no key shuffle),
    # we still need to add them to item_assignment for patching purposes
    if Types.Key not in spoiler.settings.shuffled_location_types:
        if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
            import randomizer.ItemPool as ItemPool

            vanilla_keys_assignment = []
            for level in LevelInfoList.values():
                key_location = spoiler.LocationList[level.KeyLocation]

                if key_location.item is not None and key_location.item in ItemPool.Keys():
                    placement_info = {}
                    if key_location.default_mapid_data:
                        for location in key_location.default_mapid_data:
                            placement_info[location.map] = location.id
                        old_flag = key_location.default_mapid_data[0].flag
                        old_kong = key_location.default_mapid_data[0].kong
                    else:
                        old_flag = -1
                        old_kong = Kongs.any

                    location_selection = LocationSelection(
                        vanilla_item=ItemList[key_location.default].type,
                        flag=old_flag,
                        placement_data=placement_info,
                        is_reward_point=key_location.is_reward,
                        is_shop=False,
                        price=0,
                        placement_index=[-1],
                        kong=old_kong,
                        location=level.KeyLocation,
                        name=key_location.name,
                    )
                    # Set new item to the key that was placed
                    new_item = ItemList[key_location.item]
                    location_selection.new_type = new_item.type
                    location_selection.new_kong = new_item.kong
                    location_selection.new_item = key_location.item
                    location_selection.new_flag = new_item.rando_flag
                    vanilla_keys_assignment.append(location_selection)

            locations_not_needing_flags.extend(vanilla_keys_assignment)

    spoiler.item_assignment = locations_needing_flags + locations_not_needing_flags
    # Generate human-readable version for debugging purposes
    # human_item_data = {}
    # for loc in spoiler.item_assignment:
    #     name = "Nothing"
    #     if loc.new_type is not None:
    #         name = ItemList[spoiler.LocationList[loc.location].item].name
    #     location_name = loc.name
    #     if "Kasplat" in location_name:
    #         location_name = f"{location_name.split('Kasplat')[0]} {NameFromKong(loc.old_kong)} Kasplat"
    #     human_item_data[location_name] = name
    # spoiler.debug_human_item_assignment = human_item_data
