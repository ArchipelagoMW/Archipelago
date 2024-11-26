"""
Classes and functions related to creating a ROM patch
"""
import copy
import os
import struct
from typing import TYPE_CHECKING, Dict, List, Tuple

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings

from .data import TrainerPokemonDataTypeEnum, BASE_OFFSET, data
from .items import reverse_offset_item_value
from .options import (RandomizeWildPokemon, RandomizeTrainerParties, EliteFourRequirement, NormanRequirement,
                      MatchTrainerLevels)
from .pokemon import HM_MOVES, get_random_move
from .util import bool_array_to_int, encode_string, get_easter_egg

if TYPE_CHECKING:
    from . import PokemonEmeraldWorld


_LOOPING_MUSIC = [
    "MUS_GSC_ROUTE38", "MUS_GSC_PEWTER", "MUS_ROUTE101", "MUS_ROUTE110", "MUS_ROUTE120", "MUS_ROUTE122",
    "MUS_PETALBURG", "MUS_OLDALE", "MUS_GYM", "MUS_SURF", "MUS_PETALBURG_WOODS", "MUS_LILYCOVE_MUSEUM",
    "MUS_OCEANIC_MUSEUM", "MUS_ENCOUNTER_GIRL", "MUS_ENCOUNTER_MALE", "MUS_ABANDONED_SHIP", "MUS_FORTREE",
    "MUS_BIRCH_LAB", "MUS_B_TOWER_RS", "MUS_ENCOUNTER_SWIMMER", "MUS_CAVE_OF_ORIGIN", "MUS_ENCOUNTER_RICH",
    "MUS_VERDANTURF", "MUS_RUSTBORO", "MUS_POKE_CENTER", "MUS_CAUGHT", "MUS_VICTORY_GYM_LEADER", "MUS_VICTORY_LEAGUE",
    "MUS_VICTORY_WILD", "MUS_C_VS_LEGEND_BEAST", "MUS_ROUTE104", "MUS_ROUTE119", "MUS_CYCLING", "MUS_POKE_MART",
    "MUS_LITTLEROOT", "MUS_MT_CHIMNEY", "MUS_ENCOUNTER_FEMALE", "MUS_LILYCOVE", "MUS_DESERT", "MUS_HELP",
    "MUS_UNDERWATER", "MUS_VICTORY_TRAINER", "MUS_ENCOUNTER_MAY", "MUS_ENCOUNTER_INTENSE", "MUS_ENCOUNTER_COOL",
    "MUS_ROUTE113", "MUS_ENCOUNTER_AQUA", "MUS_FOLLOW_ME", "MUS_ENCOUNTER_BRENDAN", "MUS_EVER_GRANDE",
    "MUS_ENCOUNTER_SUSPICIOUS", "MUS_VICTORY_AQUA_MAGMA", "MUS_GAME_CORNER", "MUS_DEWFORD", "MUS_SAFARI_ZONE",
    "MUS_VICTORY_ROAD", "MUS_AQUA_MAGMA_HIDEOUT", "MUS_SAILING", "MUS_MT_PYRE", "MUS_SLATEPORT", "MUS_MT_PYRE_EXTERIOR",
    "MUS_SCHOOL", "MUS_HALL_OF_FAME", "MUS_FALLARBOR", "MUS_SEALED_CHAMBER", "MUS_CONTEST_WINNER", "MUS_CONTEST",
    "MUS_ENCOUNTER_MAGMA", "MUS_ABNORMAL_WEATHER", "MUS_WEATHER_GROUDON", "MUS_SOOTOPOLIS", "MUS_HALL_OF_FAME_ROOM",
    "MUS_TRICK_HOUSE", "MUS_ENCOUNTER_TWINS", "MUS_ENCOUNTER_ELITE_FOUR", "MUS_ENCOUNTER_HIKER", "MUS_CONTEST_LOBBY",
    "MUS_ENCOUNTER_INTERVIEWER", "MUS_ENCOUNTER_CHAMPION", "MUS_B_FRONTIER", "MUS_B_ARENA", "MUS_B_PYRAMID",
    "MUS_B_PYRAMID_TOP", "MUS_B_PALACE", "MUS_B_TOWER", "MUS_B_DOME", "MUS_B_PIKE", "MUS_B_FACTORY", "MUS_VS_RAYQUAZA",
    "MUS_VS_FRONTIER_BRAIN", "MUS_VS_MEW", "MUS_B_DOME_LOBBY", "MUS_VS_WILD", "MUS_VS_AQUA_MAGMA", "MUS_VS_TRAINER",
    "MUS_VS_GYM_LEADER", "MUS_VS_CHAMPION", "MUS_VS_REGI", "MUS_VS_KYOGRE_GROUDON", "MUS_VS_RIVAL", "MUS_VS_ELITE_FOUR",
    "MUS_VS_AQUA_MAGMA_LEADER", "MUS_RG_FOLLOW_ME", "MUS_RG_GAME_CORNER", "MUS_RG_ROCKET_HIDEOUT", "MUS_RG_GYM",
    "MUS_RG_CINNABAR", "MUS_RG_LAVENDER", "MUS_RG_CYCLING", "MUS_RG_ENCOUNTER_ROCKET", "MUS_RG_ENCOUNTER_GIRL",
    "MUS_RG_ENCOUNTER_BOY", "MUS_RG_HALL_OF_FAME", "MUS_RG_VIRIDIAN_FOREST", "MUS_RG_MT_MOON", "MUS_RG_POKE_MANSION",
    "MUS_RG_ROUTE1", "MUS_RG_ROUTE24", "MUS_RG_ROUTE3", "MUS_RG_ROUTE11", "MUS_RG_VICTORY_ROAD", "MUS_RG_VS_GYM_LEADER",
    "MUS_RG_VS_TRAINER", "MUS_RG_VS_WILD", "MUS_RG_VS_CHAMPION", "MUS_RG_PALLET", "MUS_RG_OAK_LAB", "MUS_RG_OAK",
    "MUS_RG_POKE_CENTER", "MUS_RG_SS_ANNE", "MUS_RG_SURF", "MUS_RG_POKE_TOWER", "MUS_RG_SILPH", "MUS_RG_FUCHSIA",
    "MUS_RG_CELADON", "MUS_RG_VICTORY_TRAINER", "MUS_RG_VICTORY_WILD", "MUS_RG_VICTORY_GYM_LEADER", "MUS_RG_VERMILLION",
    "MUS_RG_PEWTER", "MUS_RG_ENCOUNTER_RIVAL", "MUS_RG_RIVAL_EXIT", "MUS_RG_CAUGHT", "MUS_RG_POKE_JUMP",
    "MUS_RG_UNION_ROOM", "MUS_RG_NET_CENTER", "MUS_RG_MYSTERY_GIFT", "MUS_RG_BERRY_PICK", "MUS_RG_SEVII_CAVE",
    "MUS_RG_TEACHY_TV_SHOW", "MUS_RG_SEVII_ROUTE", "MUS_RG_SEVII_DUNGEON", "MUS_RG_SEVII_123", "MUS_RG_SEVII_45",
    "MUS_RG_SEVII_67", "MUS_RG_VS_DEOXYS", "MUS_RG_VS_MEWTWO", "MUS_RG_VS_LEGEND", "MUS_RG_ENCOUNTER_GYM_LEADER",
    "MUS_RG_ENCOUNTER_DEOXYS", "MUS_RG_TRAINER_TOWER", "MUS_RG_SLOW_PALLET", "MUS_RG_TEACHY_TV_MENU",
]

_FANFARES: Dict[str, int] = {
    "MUS_LEVEL_UP":             80,
    "MUS_OBTAIN_ITEM":         160,
    "MUS_EVOLVED":             220,
    "MUS_OBTAIN_TMHM":         220,
    "MUS_HEAL":                160,
    "MUS_OBTAIN_BADGE":        340,
    "MUS_MOVE_DELETED":        180,
    "MUS_OBTAIN_BERRY":        120,
    "MUS_AWAKEN_LEGEND":       710,
    "MUS_SLOTS_JACKPOT":       250,
    "MUS_SLOTS_WIN":           150,
    "MUS_TOO_BAD":             160,
    "MUS_RG_POKE_FLUTE":       450,
    "MUS_RG_OBTAIN_KEY_ITEM":  170,
    "MUS_RG_DEX_RATING":       196,
    "MUS_OBTAIN_B_POINTS":     313,
    "MUS_OBTAIN_SYMBOL":       318,
    "MUS_REGISTER_MATCH_CALL": 135,
}
_EVOLUTION_FANFARE_INDEX = list(_FANFARES.keys()).index("MUS_EVOLVED")

CAVE_EVENT_NAME_TO_ID = {
    "TERRA_CAVE_ROUTE_114_1": 1,
    "TERRA_CAVE_ROUTE_114_2": 2,
    "TERRA_CAVE_ROUTE_115_1": 3,
    "TERRA_CAVE_ROUTE_115_2": 4,
    "TERRA_CAVE_ROUTE_116_1": 5,
    "TERRA_CAVE_ROUTE_116_2": 6,
    "TERRA_CAVE_ROUTE_118_1": 7,
    "TERRA_CAVE_ROUTE_118_2": 8,
    "MARINE_CAVE_ROUTE_105_1": 9,
    "MARINE_CAVE_ROUTE_105_2": 10,
    "MARINE_CAVE_ROUTE_125_1": 11,
    "MARINE_CAVE_ROUTE_125_2": 12,
    "MARINE_CAVE_ROUTE_127_1": 13,
    "MARINE_CAVE_ROUTE_127_2": 14,
    "MARINE_CAVE_ROUTE_129_1": 15,
    "MARINE_CAVE_ROUTE_129_2": 16,
}


class PokemonEmeraldProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Pokemon Emerald"
    hash = "605b89b67018abcea91e693a4dd25be3"
    patch_file_ending = ".apemerald"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().pokemon_emerald_settings.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes


def write_tokens(world: "PokemonEmeraldWorld", patch: PokemonEmeraldProcedurePatch) -> None:
    # TODO: Remove when the base patch is updated to include this change
    # Moves an NPC to avoid overlapping people during trainersanity
    patch.write_token(
        APTokenTypes.WRITE,
        0x53A298 + (0x18 * 7) + 4,  # Space Center 1F event address + 8th event + 4-byte offset for x coord
        struct.pack("<H", 11)
    )

    # Set free fly location
    if world.options.free_fly_location:
        patch.write_token(
            APTokenTypes.WRITE,
            data.rom_addresses["gArchipelagoOptions"] + 0x20,
            struct.pack("<B", world.free_fly_location_id)
        )

    location_info: List[Tuple[int, int, str]] = []
    for location in world.multiworld.get_locations(world.player):
        if location.address is None:
            continue

        if location.item is None:
            continue

        # Set local item values
        if not world.options.remote_items and location.item.player == world.player:
            if type(location.item_address) is int:
                patch.write_token(
                    APTokenTypes.WRITE,
                    location.item_address,
                    struct.pack("<H", location.item.code - BASE_OFFSET)
                )
            elif type(location.item_address) is list:
                for address in location.item_address:
                    patch.write_token(
                        APTokenTypes.WRITE,
                        address,
                        struct.pack("<H", location.item.code - BASE_OFFSET)
                    )
        else:
            if type(location.item_address) is int:
                patch.write_token(
                    APTokenTypes.WRITE,
                    location.item_address,
                    struct.pack("<H", data.constants["ITEM_ARCHIPELAGO_PROGRESSION"])
                )
            elif type(location.item_address) is list:
                for address in location.item_address:
                    patch.write_token(
                        APTokenTypes.WRITE,
                        address,
                        struct.pack("<H", data.constants["ITEM_ARCHIPELAGO_PROGRESSION"])
                    )

            # Creates a list of item information to store in tables later. Those tables are used to display the item and
            # player name in a text box. In the case of not enough space, the game will default to "found an ARCHIPELAGO
            # ITEM"
            location_info.append((location.address - BASE_OFFSET, location.item.player, location.item.name))

    if world.options.trainersanity:
        # Duplicate entries for rival fights
        # For each of the 5 fights, there are 6 variations that have to be accounted for (for starters * genders)
        # The Brendan Mudkip is used as a proxy in the rest of the AP code
        for locale in ["ROUTE_103", "ROUTE_110", "ROUTE_119", "RUSTBORO", "LILYCOVE"]:
            location = world.multiworld.get_location(data.locations[f"TRAINER_BRENDAN_{locale}_MUDKIP_REWARD"].label, world.player)
            alternates = [
                f"TRAINER_BRENDAN_{locale}_TREECKO",
                f"TRAINER_BRENDAN_{locale}_TORCHIC",
                f"TRAINER_MAY_{locale}_MUDKIP",
                f"TRAINER_MAY_{locale}_TREECKO",
                f"TRAINER_MAY_{locale}_TORCHIC",
            ]
            location_info.extend((
                data.constants["TRAINER_FLAGS_START"] + data.constants[trainer],
                location.item.player,
                location.item.name
            ) for trainer in alternates)

    player_name_ids: Dict[str, int] = {world.player_name: 0}
    item_name_offsets: Dict[str, int] = {}
    next_item_name_offset = 0
    for i, (flag, item_player, item_name) in enumerate(sorted(location_info, key=lambda t: t[0])):
        # The player's own items are still set in the table with the value 0 to indicate the game should not show any
        # message (the message for receiving an item will pop up when the client eventually gives it to them).
        # In race mode, no item location data is included, and only recieved (or own) items will show any text box.
        if item_player == world.player or world.multiworld.is_race:
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 0,
                struct.pack("<H", flag)
            )
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 2,
                struct.pack("<H", 0)
            )
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 4,
                struct.pack("<B", 0)
            )
        else:
            player_name = world.multiworld.get_player_name(item_player)

            if player_name not in player_name_ids:
                # Only space for 50 player names
                if len(player_name_ids) >= 50:
                    continue

                player_name_ids[player_name] = len(player_name_ids)
                for j, b in enumerate(encode_string(player_name, 17)):
                    patch.write_token(
                        APTokenTypes.WRITE,
                        data.rom_addresses["gArchipelagoPlayerNames"] + (player_name_ids[player_name] * 17) + j,
                        struct.pack("<B", b)
                    )

            if item_name not in item_name_offsets:
                if len(item_name) > 35:
                    item_name = item_name[:34] + "…"

                # Only 36 * 250 bytes for item names
                if next_item_name_offset + len(item_name) + 1 > 36 * 250:
                    continue

                item_name_offsets[item_name] = next_item_name_offset
                next_item_name_offset += len(item_name) + 1
                patch.write_token(
                    APTokenTypes.WRITE,
                    data.rom_addresses["gArchipelagoItemNames"] + (item_name_offsets[item_name]),
                    encode_string(item_name) + b"\xFF"
                )

            # There should always be enough space for one entry per location
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 0,
                struct.pack("<H", flag)
            )
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 2,
                struct.pack("<H", item_name_offsets[item_name])
            )
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 4,
                struct.pack("<B", player_name_ids[player_name])
            )

    easter_egg = get_easter_egg(world.options.easter_egg.value)

    # Set start inventory
    start_inventory = world.options.start_inventory.value.copy()

    starting_badges = 0
    if start_inventory.pop("Stone Badge", 0) > 0:
        starting_badges |= (1 << 0)
    if start_inventory.pop("Knuckle Badge", 0) > 0:
        starting_badges |= (1 << 1)
    if start_inventory.pop("Dynamo Badge", 0) > 0:
        starting_badges |= (1 << 2)
    if start_inventory.pop("Heat Badge", 0) > 0:
        starting_badges |= (1 << 3)
    if start_inventory.pop("Balance Badge", 0) > 0:
        starting_badges |= (1 << 4)
    if start_inventory.pop("Feather Badge", 0) > 0:
        starting_badges |= (1 << 5)
    if start_inventory.pop("Mind Badge", 0) > 0:
        starting_badges |= (1 << 6)
    if start_inventory.pop("Rain Badge", 0) > 0:
        starting_badges |= (1 << 7)

    pc_slots: List[Tuple[str, int]] = []
    while any(qty > 0 for qty in start_inventory.values()):
        if len(pc_slots) >= 19:
            break

        for i, item_name in enumerate(start_inventory.keys()):
            if len(pc_slots) >= 19:
                break

            quantity = min(start_inventory[item_name], 999)
            if quantity == 0:
                continue

            start_inventory[item_name] -= quantity

            pc_slots.append((item_name, quantity))

    pc_slots.sort(reverse=True)

    for i, slot in enumerate(pc_slots):
        address = data.rom_addresses["sNewGamePCItems"] + (i * 4)
        item = reverse_offset_item_value(world.item_name_to_id[slot[0]])
        patch.write_token(APTokenTypes.WRITE, address + 0, struct.pack("<H", item))
        patch.write_token(APTokenTypes.WRITE, address + 2, struct.pack("<H", slot[1]))

    # Set species data
    _set_species_info(world, patch, easter_egg)

    # Set encounter tables
    if world.options.wild_pokemon != RandomizeWildPokemon.option_vanilla:
        _set_encounter_tables(world, patch)

    # Set opponent data
    if world.options.trainer_parties != RandomizeTrainerParties.option_vanilla or easter_egg[0] == 2:
        _set_opponents(world, patch, easter_egg)

    # Set legendary pokemon
    _set_legendary_encounters(world, patch)

    # Set misc pokemon
    _set_misc_pokemon(world, patch)

    # Set starters
    _set_starters(world, patch)

    # Set TM moves
    _set_tm_moves(world, patch, easter_egg)

    # Randomize move tutor moves
    _randomize_move_tutor_moves(world, patch, easter_egg)

    # Set TM/HM compatibility
    _set_tmhm_compatibility(world, patch)

    # Randomize opponent double or single
    _randomize_opponent_battle_type(world, patch)

    # Options
    # struct ArchipelagoOptions
    # {
    #     /* 0x00 */ u16 birchPokemon;
    #     /* 0x02 */ bool8 advanceTextWithHoldA;
    #     /* 0x03 */ u8 receivedItemMessageFilter; // 0 = Show All; 1 = Show Progression Only; 2 = Show None
    #     /* 0x04 */ bool8 betterShopsEnabled;
    #     /* 0x05 */ bool8 reusableTms;
    #     /* 0x06 */ bool8 guaranteedCatch;
    #     /* 0x07 */ bool8 purgeSpinners;
    #     /* 0x08 */ bool8 areTrainersBlind;
    #     /* 0x09 */ u16 expMultiplierNumerator;
    #     /* 0x0B */ u16 expMultiplierDenominator;
    #     /* 0x0D */ bool8 matchTrainerLevels;
    #     /* 0x0E */ s8 matchTrainerLevelBonus;
    #     /* 0x0F */ bool8 eliteFourRequiresGyms;
    #     /* 0x10 */ u8 eliteFourRequiredCount;
    #     /* 0x11 */ bool8 normanRequiresGyms;
    #     /* 0x12 */ u8 normanRequiredCount;
    #     /* 0x13 */ u8 startingBadges;
    #     /* 0x14 */ u32 hmTotalBadgeRequirements;
    #     /* 0x18 */ u8 hmSpecificBadgeRequirements[8];
    #     /* 0x20 */ u8 freeFlyLocation;
    #     /* 0x21 */ u8 terraCaveLocationId:4;
    #                u8 marineCaveLocationId:4;
    #     /* 0x22 */ bool8 addRoute115Boulders;
    #     /* 0x23 */ bool8 addBumpySlopes;
    #     /* 0x24 */ bool8 modifyRoute118;
    #     /* 0x25 */ u16 removedBlockers;
    #     /* 0x27 */ bool8 berryTreesRandomized;
    #     /* 0x28 */ bool8 isDexsanity;
    #     /* 0x29 */ bool8 isTrainersanity;
    #     /* 0x2A */ bool8 isWarpRando;
    #     /* 0x2B */ u8 activeEasterEgg;
    #     /* 0x2C */ bool8 normalizeEncounterRates;
    #     /* 0x2D */ bool8 allowWonderTrading;
    #     /* 0x2E */ u16 matchTrainerLevelMultiplierNumerator;
    #     /* 0x30 */ u16 matchTrainerLevelMultiplierDenominator;
    #     /* 0x32 */ bool8 allowSkippingFanfares;
    # };
    options_address = data.rom_addresses["gArchipelagoOptions"]

    # Set Birch pokemon
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x00,
        struct.pack("<H", world.random.choice(list(data.species.keys())))
    )

    # Set hold A to advance text
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x02,
        struct.pack("<B", 1 if world.options.turbo_a else 0)
    )

    # Set receive item messages type
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x03,
        struct.pack("<B", world.options.receive_item_messages.value)
    )

    # Set better shops
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x04,
        struct.pack("<B", 1 if world.options.better_shops else 0)
    )

    # Set reusable TMs
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x05,
        struct.pack("<B", 1 if world.options.reusable_tms_tutors else 0)
    )

    # Set guaranteed catch
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x06,
        struct.pack("<B", 1 if world.options.guaranteed_catch else 0)
    )

    # Set purge spinners
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x07,
        struct.pack("<B", 1 if world.options.purge_spinners else 0)
    )

    # Set blind trainers
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x08,
        struct.pack("<B", 1 if world.options.blind_trainers else 0)
    )

    # Set exp modifier
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x09,
        struct.pack("<H", min(max(world.options.exp_modifier.value, 0), 2**16 - 1))
    )
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x0B,
        struct.pack("<H", 100)
    )

    # Set match trainer levels
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x0D,
        struct.pack("<B", 1 if world.options.match_trainer_levels else 0)
    )

    # Set match trainer levels bonus
    if world.options.match_trainer_levels == MatchTrainerLevels.option_additive:
        match_trainer_levels_bonus = max(min(world.options.match_trainer_levels_bonus.value, 100), -100)
        patch.write_token(APTokenTypes.WRITE, options_address + 0x0E, struct.pack("<b", match_trainer_levels_bonus))
    elif world.options.match_trainer_levels == MatchTrainerLevels.option_multiplicative:
        patch.write_token(APTokenTypes.WRITE, options_address + 0x2E, struct.pack("<H", world.options.match_trainer_levels_bonus.value + 100))
        patch.write_token(APTokenTypes.WRITE, options_address + 0x30, struct.pack("<H", 100))

    # Set elite four requirement
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x0F,
        struct.pack("<B", 1 if world.options.elite_four_requirement == EliteFourRequirement.option_gyms else 0)
    )

    # Set elite four count
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x10,
        struct.pack("<B", min(max(world.options.elite_four_count.value, 0), 8))
    )

    # Set norman requirement
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x11,
        struct.pack("<B", 1 if world.options.norman_requirement == NormanRequirement.option_gyms else 0)
    )

    # Set norman count
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x12,
        struct.pack("<B", min(max(world.options.norman_count.value, 0), 8))
    )

    # Set starting badges
    patch.write_token(APTokenTypes.WRITE, options_address + 0x13, struct.pack("<B", starting_badges))

    # Set HM badge requirements
    field_move_order = [
        "HM01 Cut",
        "HM05 Flash",
        "HM06 Rock Smash",
        "HM04 Strength",
        "HM03 Surf",
        "HM02 Fly",
        "HM08 Dive",
        "HM07 Waterfall",
    ]
    badge_to_bit = {
        "Stone Badge": 1 << 0,
        "Knuckle Badge": 1 << 1,
        "Dynamo Badge": 1 << 2,
        "Heat Badge": 1 << 3,
        "Balance Badge": 1 << 4,
        "Feather Badge": 1 << 5,
        "Mind Badge": 1 << 6,
        "Rain Badge": 1 << 7,
    }

    # Number of badges
    # Uses 4 bits per HM. 0-8 means it's a valid requirement, otherwise use specific badges.
    hm_badge_counts = 0
    for i, hm in enumerate(field_move_order):
        hm_badge_counts |= (world.hm_requirements[hm] if isinstance(world.hm_requirements[hm], int) else 0xF) << (i * 4)
    patch.write_token(APTokenTypes.WRITE, options_address + 0x14, struct.pack("<I", hm_badge_counts))

    # Specific badges
    for i, hm in enumerate(field_move_order):
        if isinstance(world.hm_requirements, list):
            bitfield = 0
            for badge in world.hm_requirements:
                bitfield |= badge_to_bit[badge]
            patch.write_token(APTokenTypes.WRITE, options_address + 0x18, struct.pack("<B", bitfield))

    # Set terra/marine cave locations
    terra_cave_id = CAVE_EVENT_NAME_TO_ID[world.multiworld.get_location("TERRA_CAVE_LOCATION", world.player).item.name]
    marine_cave_id = CAVE_EVENT_NAME_TO_ID[world.multiworld.get_location("MARINE_CAVE_LOCATION", world.player).item.name]
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x21,
        struct.pack("<B", terra_cave_id | (marine_cave_id << 4))
    )

    # Set route 115 boulders
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x22,
        struct.pack("<B", 1 if world.options.extra_boulders else 0)
    )

    # Swap route 115 layout if bumpy slope enabled
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x23,
        struct.pack("<B", 1 if world.options.extra_bumpy_slope else 0)
    )

    # Swap route 115 layout if bumpy slope enabled
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x24,
        struct.pack("<B", 1 if world.options.modify_118 else 0)
    )

    # Set removed blockers
    removed_roadblocks = world.options.remove_roadblocks.value
    removed_roadblocks_bitfield = 0
    removed_roadblocks_bitfield |= (1 << 0) if "Safari Zone Construction Workers" in removed_roadblocks else 0
    removed_roadblocks_bitfield |= (1 << 1) if "Lilycove City Wailmer" in removed_roadblocks else 0
    removed_roadblocks_bitfield |= (1 << 2) if "Route 110 Aqua Grunts" in removed_roadblocks else 0
    removed_roadblocks_bitfield |= (1 << 3) if "Aqua Hideout Grunts" in removed_roadblocks else 0
    removed_roadblocks_bitfield |= (1 << 4) if "Route 119 Aqua Grunts" in removed_roadblocks else 0
    removed_roadblocks_bitfield |= (1 << 5) if "Route 112 Magma Grunts" in removed_roadblocks else 0
    removed_roadblocks_bitfield |= (1 << 6) if "Seafloor Cavern Aqua Grunt" in removed_roadblocks else 0
    patch.write_token(APTokenTypes.WRITE, options_address + 0x25, struct.pack("<H", removed_roadblocks_bitfield))

    # Mark berry trees as randomized
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x27,
        struct.pack("<B", 1 if world.options.berry_trees else 0)
    )

    # Mark dexsanity as enabled
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x28,
        struct.pack("<B", 1 if world.options.dexsanity else 0)
    )

    # Mark trainersanity as enabled
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x29,
        struct.pack("<B", 1 if world.options.trainersanity else 0)
    )

    # Set easter egg data
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x2B,
        struct.pack("<B", easter_egg[0])
    )

    # Set normalize encounter rates
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x2C,
        struct.pack("<B", 1 if world.options.normalize_encounter_rates else 0)
    )

    # Set allow wonder trading
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x2D,
        struct.pack("<B", 1 if world.options.enable_wonder_trading else 0)
    )

    # Set allowed to skip fanfares
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x32,
        struct.pack("<B", 1 if world.options.fanfares else 0)
    )

    if easter_egg[0] == 2:
        offset = data.rom_addresses["gBattleMoves"] + 4
        patch.write_token(APTokenTypes.WRITE, offset + (easter_egg[1] * 12), struct.pack("<B", 50))
        patch.write_token(APTokenTypes.WRITE, offset + (data.constants["MOVE_CUT"] * 12), struct.pack("<B", 1))
        patch.write_token(APTokenTypes.WRITE, offset + (data.constants["MOVE_FLY"] * 12), struct.pack("<B", 1))
        patch.write_token(APTokenTypes.WRITE, offset + (data.constants["MOVE_SURF"] * 12), struct.pack("<B", 1))
        patch.write_token(APTokenTypes.WRITE, offset + (data.constants["MOVE_STRENGTH"] * 12), struct.pack("<B", 1))
        patch.write_token(APTokenTypes.WRITE, offset + (data.constants["MOVE_FLASH"] * 12), struct.pack("<B", 1))
        patch.write_token(APTokenTypes.WRITE, offset + (data.constants["MOVE_ROCK_SMASH"] * 12), struct.pack("<B", 1))
        patch.write_token(APTokenTypes.WRITE, offset + (data.constants["MOVE_WATERFALL"] * 12), struct.pack("<B", 1))
        patch.write_token(APTokenTypes.WRITE, offset + (data.constants["MOVE_DIVE"] * 12), struct.pack("<B", 1))
        patch.write_token(APTokenTypes.WRITE, offset + (data.constants["MOVE_DIG"] * 12), struct.pack("<B", 1))

    # Set slot auth
    patch.write_token(APTokenTypes.WRITE, data.rom_addresses["gArchipelagoInfo"], world.auth)

    # Randomize music
    if world.options.music:
        # The "randomized sound table" is a patchboard that redirects sounds just before they get played
        randomized_looping_music = copy.copy(_LOOPING_MUSIC)
        world.random.shuffle(randomized_looping_music)
        for original_music, randomized_music in zip(_LOOPING_MUSIC, randomized_looping_music):
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gRandomizedSoundTable"] + (data.constants[original_music] * 2),
                struct.pack("<H", data.constants[randomized_music])
            )

    # Randomize fanfares
    if world.options.fanfares:
        # Shuffle the lists, pair new tracks with original tracks, set the new track ids, and set new fanfare durations
        randomized_fanfares = [fanfare_name for fanfare_name in _FANFARES]
        world.random.shuffle(randomized_fanfares)

        # Prevent the evolution fanfare from receiving the poke flute by swapping it with something else.
        # The poke flute sound causes the evolution scene to get stuck for like 40 seconds
        if randomized_fanfares[_EVOLUTION_FANFARE_INDEX] == "MUS_RG_POKE_FLUTE":
            swap_index = (_EVOLUTION_FANFARE_INDEX + 1) % len(_FANFARES)
            temp = randomized_fanfares[_EVOLUTION_FANFARE_INDEX]
            randomized_fanfares[_EVOLUTION_FANFARE_INDEX] = randomized_fanfares[swap_index]
            randomized_fanfares[swap_index] = temp

        for i, fanfare_pair in enumerate(zip(_FANFARES.keys(), randomized_fanfares)):
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gRandomizedSoundTable"] + (data.constants[fanfare_pair[0]] * 2),
                struct.pack("<H", data.constants[fanfare_pair[1]])
            )
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["sFanfares"] + (i * 4) + 2,
                struct.pack("<H", _FANFARES[fanfare_pair[1]])
            )

    patch.write_file("token_data.bin", patch.get_token_binary())


def _set_encounter_tables(world: "PokemonEmeraldWorld", patch: PokemonEmeraldProcedurePatch) -> None:
    """
    Encounter tables are lists of
    struct {
        min_level:  0x01 bytes,
        max_level:  0x01 bytes,
        species_id: 0x02 bytes
    }
    """
    for map_data in world.modified_maps.values():
        tables = [map_data.land_encounters, map_data.water_encounters, map_data.fishing_encounters]
        for table in tables:
            if table is not None:
                for i, species_id in enumerate(table.slots):
                    address = table.address + 2 + (4 * i)
                    patch.write_token(APTokenTypes.WRITE, address, struct.pack("<H", species_id))


def _set_species_info(world: "PokemonEmeraldWorld", patch: PokemonEmeraldProcedurePatch, easter_egg: Tuple[int, int]) -> None:
    for species in world.modified_species.values():
        patch.write_token(APTokenTypes.WRITE, species.address + 6, struct.pack("<B", species.types[0]))
        patch.write_token(APTokenTypes.WRITE, species.address + 7, struct.pack("<B", species.types[1]))
        patch.write_token(APTokenTypes.WRITE, species.address + 8, struct.pack("<B", species.catch_rate))

        if easter_egg[0] == 3:
            patch.write_token(APTokenTypes.WRITE, species.address + 22, struct.pack("<B", easter_egg[1]))
            patch.write_token(APTokenTypes.WRITE, species.address + 23, struct.pack("<B", easter_egg[1]))
        else:
            patch.write_token(APTokenTypes.WRITE, species.address + 22, struct.pack("<B", species.abilities[0]))
            patch.write_token(APTokenTypes.WRITE, species.address + 23, struct.pack("<B", species.abilities[1]))

        for i, learnset_move in enumerate(species.learnset):
            level_move = learnset_move.level << 9 | learnset_move.move_id
            if easter_egg[0] == 2:
                level_move = learnset_move.level << 9 | easter_egg[1]

            patch.write_token(APTokenTypes.WRITE, species.learnset_address + (i * 2), struct.pack("<H", level_move))


def _set_opponents(world: "PokemonEmeraldWorld", patch: PokemonEmeraldProcedurePatch, easter_egg: Tuple[int, int]) -> None:
    for trainer in world.modified_trainers:
        party_address = trainer.party.address

        pokemon_data_size: int
        if trainer.party.pokemon_data_type in {TrainerPokemonDataTypeEnum.NO_ITEM_DEFAULT_MOVES, TrainerPokemonDataTypeEnum.ITEM_DEFAULT_MOVES}:
            pokemon_data_size = 8
        else:  # Custom Moves
            pokemon_data_size = 16

        for i, pokemon in enumerate(trainer.party.pokemon):
            pokemon_address = party_address + (i * pokemon_data_size)

            # Replace species
            patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x04, struct.pack("<H", pokemon.species_id))

            # Replace custom moves if applicable
            if trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.NO_ITEM_CUSTOM_MOVES:
                if easter_egg[0] == 2:
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x06, struct.pack("<H", easter_egg[1]))
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x08, struct.pack("<H", easter_egg[1]))
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x0A, struct.pack("<H", easter_egg[1]))
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x0C, struct.pack("<H", easter_egg[1]))
                else:
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x06, struct.pack("<H", pokemon.moves[0]))
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x08, struct.pack("<H", pokemon.moves[1]))
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x0A, struct.pack("<H", pokemon.moves[2]))
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x0C, struct.pack("<H", pokemon.moves[3]))
            elif trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES:
                if easter_egg[0] == 2:
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x08, struct.pack("<H", easter_egg[1]))
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x0A, struct.pack("<H", easter_egg[1]))
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x0C, struct.pack("<H", easter_egg[1]))
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x0E, struct.pack("<H", easter_egg[1]))
                else:
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x08, struct.pack("<H", pokemon.moves[0]))
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x0A, struct.pack("<H", pokemon.moves[1]))
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x0C, struct.pack("<H", pokemon.moves[2]))
                    patch.write_token(APTokenTypes.WRITE, pokemon_address + 0x0E, struct.pack("<H", pokemon.moves[3]))


def _set_legendary_encounters(world: "PokemonEmeraldWorld", patch: PokemonEmeraldProcedurePatch) -> None:
    for encounter in world.modified_legendary_encounters:
        patch.write_token(APTokenTypes.WRITE, encounter.address, struct.pack("<H", encounter.species_id))


def _set_misc_pokemon(world: "PokemonEmeraldWorld", patch: PokemonEmeraldProcedurePatch) -> None:
    for encounter in world.modified_misc_pokemon:
        patch.write_token(APTokenTypes.WRITE, encounter.address, struct.pack("<H", encounter.species_id))


def _set_starters(world: "PokemonEmeraldWorld", patch: PokemonEmeraldProcedurePatch) -> None:
    patch.write_token(APTokenTypes.WRITE, data.rom_addresses["sStarterMon"] + 0, struct.pack("<H", world.modified_starters[0]))
    patch.write_token(APTokenTypes.WRITE, data.rom_addresses["sStarterMon"] + 2, struct.pack("<H", world.modified_starters[1]))
    patch.write_token(APTokenTypes.WRITE, data.rom_addresses["sStarterMon"] + 4, struct.pack("<H", world.modified_starters[2]))


def _set_tm_moves(world: "PokemonEmeraldWorld", patch: PokemonEmeraldProcedurePatch, easter_egg: Tuple[int, int]) -> None:
    tmhm_list_address = data.rom_addresses["sTMHMMoves"]

    for i, move in enumerate(world.modified_tmhm_moves):
        # Don't modify HMs
        if i >= 50:
            break

        if easter_egg[0] == 2:
            patch.write_token(APTokenTypes.WRITE, tmhm_list_address + (i * 2), struct.pack("<H", easter_egg[1]))
        else:
            patch.write_token(APTokenTypes.WRITE, tmhm_list_address + (i * 2), struct.pack("<H", move))


def _set_tmhm_compatibility(world: "PokemonEmeraldWorld", patch: PokemonEmeraldProcedurePatch) -> None:
    learnsets_address = data.rom_addresses["gTMHMLearnsets"]

    for species in world.modified_species.values():
        patch.write_token(
            APTokenTypes.WRITE,
            learnsets_address + (species.species_id * 8),
            struct.pack("<Q", species.tm_hm_compatibility)
        )


def _randomize_opponent_battle_type(world: "PokemonEmeraldWorld", patch: PokemonEmeraldProcedurePatch) -> None:
    probability = world.options.double_battle_chance.value / 100

    battle_type_map = {
        0: 4,
        1: 8,
        2: 6,
        3: 13,
    }

    for trainer_data in data.trainers:
        if trainer_data.script_address != 0 and len(trainer_data.party.pokemon) > 1:
            original_battle_type = trainer_data.battle_type
            if original_battle_type in battle_type_map:  # Don't touch anything other than regular single battles
                if world.random.random() < probability:
                    # Set the trainer to be a double battle
                    patch.write_token(APTokenTypes.WRITE, trainer_data.address + 0x18, struct.pack("<B", 1))

                    # Swap the battle type in the script for the purpose of loading the right text
                    # and setting data to the right places
                    patch.write_token(
                        APTokenTypes.WRITE,
                        trainer_data.script_address + 1,
                        struct.pack("<B", battle_type_map[original_battle_type])
                    )


def _randomize_move_tutor_moves(world: "PokemonEmeraldWorld", patch: PokemonEmeraldProcedurePatch, easter_egg: Tuple[int, int]) -> None:
    FORTREE_MOVE_TUTOR_INDEX = 24

    if easter_egg[0] == 2:
        for i in range(30):
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gTutorMoves"] + (i * 2),
                struct.pack("<H", easter_egg[1])
            )
    else:
        if world.options.tm_tutor_moves:
            new_tutor_moves = []
            for i in range(30):
                new_move = get_random_move(world.random, set(new_tutor_moves) | world.blacklisted_moves | HM_MOVES)
                new_tutor_moves.append(new_move)

                patch.write_token(
                    APTokenTypes.WRITE,
                    data.rom_addresses["gTutorMoves"] + (i * 2),
                    struct.pack("<H", new_move)
                )

    # Always set Fortree move tutor to Dig
    patch.write_token(
        APTokenTypes.WRITE,
        data.rom_addresses["gTutorMoves"] + (FORTREE_MOVE_TUTOR_INDEX * 2),
        struct.pack("<H", data.constants["MOVE_DIG"])
    )

    # Modify compatibility
    if world.options.tm_tutor_compatibility.value != -1:
        for species in data.species.values():
            compatibility = bool_array_to_int([
                world.random.randrange(0, 100) < world.options.tm_tutor_compatibility.value
                for _ in range(32)
            ])

            # Make sure Dig tutor has reasonable (>=50%) compatibility
            if world.options.tm_tutor_compatibility.value < 50:
                compatibility &= ~(1 << FORTREE_MOVE_TUTOR_INDEX)
                if world.random.random() < 0.5:
                    compatibility |= 1 << FORTREE_MOVE_TUTOR_INDEX

            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["sTutorLearnsets"] + (species.species_id * 4),
                struct.pack("<I", compatibility)
            )
