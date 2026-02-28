"""Rules for Archipelago."""

from BaseClasses import MultiWorld
from worlds.generic.Rules import forbid_item
from randomizer.Enums.Items import Items
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Types import Types
from randomizer.Enums.Settings import ShuffleLoadingZones, LogicType


def set_rules(world: MultiWorld, player: int):
    """Set the rules for the given player's world."""
    world.completion_condition[player] = lambda state: state.has("Banana Hoard", player)

    # Check if minimal logic is enabled
    dk64_world = world.worlds[player]
    if dk64_world.options.logic_type.value == LogicType.minimal:
        apply_minimal_logic_rules(world, player, dk64_world)
        return

    # DK64_TODO: Get location access rules from DK64R for non-minimal logic modes


def apply_minimal_logic_rules(world: MultiWorld, player: int, dk64_world):
    """Apply minimal logic rules to prevent invalid item placements."""
    spoiler = dk64_world.spoiler

    # Determine level 7 for Key 5 restriction
    level_7 = None
    level_7_lobby_map = None

    if spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.all:
        if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
            # In level shuffle, check level 7
            level_7 = spoiler.settings.level_order[7]
        else:
            # Vanilla Order
            level_7 = Levels.CreepyCastle

        # Map the level to its lobby map
        lobby_map_dict = {
            Levels.JungleJapes: Maps.JungleJapesLobby,
            Levels.AngryAztec: Maps.AngryAztecLobby,
            Levels.FranticFactory: Maps.FranticFactoryLobby,
            Levels.GloomyGalleon: Maps.GloomyGalleonLobby,
            Levels.FungiForest: Maps.FungiForestLobby,
            Levels.CrystalCaves: Maps.CrystalCavesLobby,
            Levels.CreepyCastle: Maps.CreepyCastleLobby,
        }
        level_7_lobby_map = lobby_map_dict.get(level_7)

    # Kong items for self-lock prevention
    kong_items = {
        Items.Donkey: "Donkey",
        Items.Diddy: "Diddy",
        Items.Lanky: "Lanky",
        Items.Tiny: "Tiny",
        Items.Chunky: "Chunky",
    }

    # Iterate through all locations to apply rules
    for loc_id, location_data in spoiler.LocationList.items():
        location_name = location_data.name

        # Skip if location doesn't exist in Archipelago
        try:
            ap_location = world.get_location(location_name, player)
        except KeyError:
            continue

        # Rule 1: Key 5 (Fungi Forest Key) cannot be in Level 7 or its lobby
        if level_7 is not None:
            # Check if in the level itself
            if location_data.level == level_7:
                forbid_item(ap_location, "Key 5", player)

            # Check if in the level's lobby
            if level_7_lobby_map is not None and location_data.default_mapid_data is not None:
                for map_data in location_data.default_mapid_data:
                    if map_data.map == level_7_lobby_map:
                        forbid_item(ap_location, "Key 5", player)
                        break

        # Rule 2: Kongs cannot be locked behind shops that require that specific Kong to access
        if location_data.type == Types.Shop and location_data.kong < 5:
            kong_item = list(kong_items.keys())[location_data.kong]
            kong_name = kong_items[kong_item]
            forbid_item(ap_location, kong_name, player)

        # Rule 3: Kongs cannot be on their own banana medal or half-medal locations
        if location_data.type in (Types.Medal, Types.HalfMedal) and location_data.kong < 5:
            kong_item = list(kong_items.keys())[location_data.kong]
            kong_name = kong_items[kong_item]
            forbid_item(ap_location, kong_name, player)

    # Rule 4: DK cannot be in blast-locked locations
    non_dk_location_ids = [
        Locations.JapesDonkeyBaboonBlast,
        Locations.FactoryDonkeyDKArcade,
        Locations.NintendoCoin,
    ]

    for loc_id in non_dk_location_ids:
        location_data = spoiler.LocationList.get(loc_id)
        if location_data:
            try:
                ap_location = world.get_location(location_data.name, player)
                forbid_item(ap_location, "Donkey", player)
            except KeyError:
                pass
