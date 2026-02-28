"""Apply Patch data to the ROM."""

import json
import os
from datetime import datetime as Datetime
from datetime import timezone
import time
from tempfile import mktemp
from randomizer.Enums.Settings import (
    BananaportRando,
    CBRequirement,
    CrownEnemyDifficulty,
    DamageAmount,
    FasterChecksSelected,
    FungiTimeSetting,
    GalleonWaterSetting,
    HardModeSelected,
    HardBossesSelected,
    MiscChangesSelected,
    ProgressiveHintItem,
    PuzzleRando,
    RemovedBarriersSelected,
    RandomStartingRegion,
    ShockwaveStatus,
    ShuffleLoadingZones,
    SlamRequirement,
    WinConditionComplex,
    WrinklyHints,
)
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
import randomizer.ItemPool as ItemPool
from randomizer.Enums.Items import Items
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Maps import Maps
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Lists.EnemyTypes import Enemies, EnemySelector
from randomizer.Lists.HardMode import HardSelector
from randomizer.Lists.Multiselectors import QoLSelector, RemovedBarrierSelector, FasterCheckSelector
from randomizer.Patching.BananaPlacer import randomize_cbs
from randomizer.Patching.BananaPortRando import randomize_bananaport, move_bananaports
from randomizer.Patching.BarrelRando import randomize_barrels
from randomizer.Patching.CoinPlacer import randomize_coins, place_mayhem_coins
from randomizer.Patching.Cosmetics.TextRando import writeBootMessages
from randomizer.Patching.Cosmetics.Puzzles import updateMillLeverTexture, updateCryptLeverTexture, updateDiddyDoors, updateHelmFaces, updateSnidePanel
from randomizer.Patching.CosmeticColors import (
    applyHelmDoorCosmetics,
    applyKongModelSwaps,
    showWinCondition,
)
from randomizer.Patching.CratePlacer import randomize_melon_crate
from randomizer.Patching.CrownPlacer import randomize_crown_pads
from randomizer.Patching.DoorPlacer import place_door_locations, remove_existing_indicators, alterStoryCutsceneWarps
from randomizer.Patching.EnemyRando import randomize_enemies
from randomizer.Patching.EntranceRando import (
    enableTriggerText,
    filterEntranceType,
    randomize_entrances,
    placeLevelOrder,
)
from randomizer.Patching.FairyPlacer import PlaceFairies
from randomizer.Patching.ItemRando import place_randomized_items, alterTextboxRequirements, calculateInitFileScreen, place_spoiler_hint_data
from randomizer.Patching.KasplatLocationRando import randomize_kasplat_locations
from randomizer.Patching.KongRando import apply_kongrando_cosmetic
from randomizer.Patching.Library.Generic import setItemReferenceName, addNewScript, IsItemSelected, getProgHintBarrierItem, getHintRequirementBatch, IsDDMSSelected
from randomizer.Patching.Library.Assets import CompTextFiles, ItemPreview
from randomizer.Patching.MiscSetupChanges import (
    randomize_setup,
    updateKrushaMoveNames,
    updateRandomSwitches,
    updateSwitchsanity,
    remove5DSCameraPoint,
)
from randomizer.Patching.MoveLocationRando import place_pregiven_moves, randomize_moves
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.PhaseRando import randomize_helm, randomize_krool
from randomizer.Patching.PriceRando import randomize_prices
from randomizer.Patching.PuzzleRando import randomize_puzzles, shortenCastleMinecart
from randomizer.Patching.ShopRandomizer import ApplyShopRandomizer
from randomizer.Patching.UpdateHints import (
    PushHints,
    replaceIngameText,
    PushItemLocations,
    PushHelpfulHints,
    PushHintTiedRegions,
)
from randomizer.Patching.ASMPatcher import patchAssembly
from randomizer.Patching.MirrorMode import ApplyMirrorMode
from randomizer.CompileHints import getHelmOrderHint

# from randomizer.Spoiler import Spoiler


class BooleanProperties:
    """Class to store data relating to boolean properties."""

    def __init__(self, check, offset, target=1):
        """Initialize with given data."""
        self.check = check
        self.offset = offset
        self.target = target


def writeMultiselector(
    enabled_selections: list,
    selector: list[dict],
    selection_enum,
    data_length: int,
    ROM_COPY: LocalROM,
    write_start: int,
):
    """Write multiselector choices to ROM."""
    write_data = [0] * data_length
    for item in selector:
        if item["shift"] >= 0:
            if selection_enum[item["value"]] in enabled_selections:
                offset = int(item["shift"] >> 3)
                check = int(item["shift"] % 8)
                write_data[offset] |= 0x80 >> check
    ROM_COPY.seek(write_start)
    for byte_data in write_data:
        ROM_COPY.writeMultipleBytes(byte_data, 1)


def encPass(spoiler) -> int:
    """Encrypt the password."""
    # Try to import randomizer.Encryption encrypt function, if we can pass all args to it.
    try:
        from randomizer.Encryption import encrypt

        return encrypt(spoiler)
    except Exception as e:
        print(e)
        return 0, 0


def patching_response(spoiler):
    """Apply the patch data to the ROM in the local server to be returned to the client."""
    # Make sure we re-load the seed id
    spoiler.settings.set_seed()

    # Write date to ROM for debugging purposes
    try:
        temp_json = json.loads(spoiler.json)
    except Exception:
        temp_json = {"Settings": {}}
    dt = Datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    temp_json["Settings"]["Generation Timestamp"] = dt
    spoiler.json = json.dumps(temp_json, indent=4)
    ROM_COPY = LocalROM()
    ROM_COPY.seek(0x1FFF200)
    ROM_COPY.writeBytes(dt.encode("ascii"))
    # Initialize Text Changes
    spoiler.text_changes = {}

    # Starting index for our settings
    sav = spoiler.settings.rom_data

    # Shuffle Levels
    if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
        ROM_COPY.seek(sav + 0)
        ROM_COPY.write(1)

        # Update Level Order
        vanilla_lobby_entrance_order = [
            Transitions.IslesMainToJapesLobby,
            Transitions.IslesMainToAztecLobby,
            Transitions.IslesMainToFactoryLobby,
            Transitions.IslesMainToGalleonLobby,
            Transitions.IslesMainToForestLobby,
            Transitions.IslesMainToCavesLobby,
            Transitions.IslesMainToCastleLobby,
            Transitions.IslesMainToHelmLobby,
        ]
        vanilla_lobby_exit_order = [
            Transitions.IslesJapesLobbyToMain,
            Transitions.IslesAztecLobbyToMain,
            Transitions.IslesFactoryLobbyToMain,
            Transitions.IslesGalleonLobbyToMain,
            Transitions.IslesForestLobbyToMain,
            Transitions.IslesCavesLobbyToMain,
            Transitions.IslesCastleLobbyToMain,
            Transitions.IslesHelmLobbyToMain,
        ]
        level_order = []
        for level in vanilla_lobby_entrance_order:
            level_order.append(vanilla_lobby_exit_order.index(spoiler.shuffled_exit_data[int(level)].reverse))
        placeLevelOrder(spoiler, level_order, ROM_COPY)

    ROM_COPY.seek(sav + 0x151)
    ROM_COPY.writeMultipleBytes(spoiler.settings.starting_kong, 1)

    boolean_props = [
        BooleanProperties(spoiler.settings.fast_start_beginning_of_game, 0x2E),  # Fast Start Game
        BooleanProperties(spoiler.settings.enable_tag_anywhere, 0x30),  # Tag Anywhere
        BooleanProperties(spoiler.settings.no_melons, 0x128),  # No Melon Drops
        BooleanProperties(spoiler.settings.bonus_barrel_auto_complete, 0x126),  # Auto-Complete Bonus Barrels
        BooleanProperties(spoiler.settings.warp_to_isles, 0x135),  # Warp to Isles
        BooleanProperties(spoiler.settings.perma_death, 0x14D),  # Permadeath
        BooleanProperties(spoiler.settings.ice_traps_damage, 0x150),  # Enable Ice Trap Damage
        BooleanProperties(spoiler.settings.shorten_boss, 0x13B),  # Shorten Boss Fights
        BooleanProperties(spoiler.settings.fast_warps, 0x13A),  # Fast Warps
        BooleanProperties(spoiler.settings.auto_keys, 0x15B),  # Auto-Turn Keys
        BooleanProperties(spoiler.settings.tns_location_rando, 0x10E),  # T&S Portal Location Rando
        BooleanProperties(IsItemSelected(spoiler.settings.cb_rando_enabled, spoiler.settings.cb_rando_list_selected, Levels.DKIsles), 0x10B),  # 5 extra medal handling
        BooleanProperties(spoiler.settings.helm_hurry, 0xAE),  # Helm Hurry
        BooleanProperties(spoiler.settings.wrinkly_available, 0x52),  # Remove Wrinkly Kong Checks
        BooleanProperties(
            spoiler.settings.bananaport_rando in (BananaportRando.crossmap_coupled, BananaportRando.crossmap_decoupled),
            0x47,
        ),  # Parent Map Filter
        BooleanProperties(spoiler.settings.shop_indicator, 0x134, 2),  # Shop Indicator
        BooleanProperties(spoiler.settings.open_lobbies, 0x14C, 0xFF),  # Open Lobbies
        BooleanProperties(spoiler.settings.item_reward_previews, 0x101, 255),  # Bonus Matches Contents
        BooleanProperties(spoiler.settings.portal_numbers, 0x11E),  # Portal Numbers
        BooleanProperties(spoiler.settings.sprint_barrel_requires_sprint, 0x2F),  # Sprint Barrel requires OSprint
        BooleanProperties(spoiler.settings.fix_lanky_tiny_prod, 0x114),  # Fix Lanky Tiny Prod
        BooleanProperties(spoiler.settings.enemy_kill_crown_timer, 0x35),  # Enemy crown timer reduction
        BooleanProperties(spoiler.settings.race_coin_rando, 0x94),  # Race Coin Location Rando
        BooleanProperties(spoiler.settings.disable_racing_patches, 0x91),  # Disable Racing Patches
        BooleanProperties(spoiler.settings.shops_dont_cost, 0x95),  # Shops don't cost
        BooleanProperties(spoiler.settings.snide_reward_rando, 0x69),  # Snides has rewards
    ]

    for prop in boolean_props:
        if prop.check:
            ROM_COPY.seek(sav + prop.offset)
            ROM_COPY.write(prop.target)

    # Fast Hideout
    ROM_COPY.seek(sav + 0x031)
    # The HelmSetting enum is indexed to allow this.
    ROM_COPY.write(int(spoiler.settings.helm_setting))

    # Crown Door & Coin Door
    # Crown Door
    ROM_COPY.seek(sav + 0x4C)
    ROM_COPY.write(int(spoiler.settings.crown_door_item))
    ROM_COPY.write(spoiler.settings.crown_door_item_count)
    # Coin Door
    ROM_COPY.seek(sav + 0x4E)
    ROM_COPY.write(int(spoiler.settings.coin_door_item))
    ROM_COPY.write(spoiler.settings.coin_door_item_count)

    kong_free_switches = [
        Switches.JapesFreeKong,
        Switches.AztecLlamaPuzzle,
        Switches.AztecOKONGPuzzle,
        Switches.FactoryFreeKong,
    ]
    if spoiler.settings.switchsanity_enabled:
        for slot in spoiler.settings.switchsanity_data:
            ROM_COPY.seek(sav + spoiler.settings.switchsanity_data[slot].rom_offset)
            pad_kong = spoiler.settings.switchsanity_data[slot].kong
            pad_type = spoiler.settings.switchsanity_data[slot].switch_type
            if slot == Switches.IslesMonkeyport:
                if pad_kong == Kongs.lanky:
                    ROM_COPY.writeMultipleBytes(2, 1)
                elif pad_kong == Kongs.donkey:
                    ROM_COPY.writeMultipleBytes(1, 1)
            elif slot == Switches.IslesHelmLobbyGone:
                if pad_type == SwitchType.MiscActivator:
                    if pad_kong == Kongs.donkey:
                        ROM_COPY.writeMultipleBytes(6, 1)
                    elif pad_kong == Kongs.diddy:
                        ROM_COPY.writeMultipleBytes(7, 1)
                elif pad_type != SwitchType.PadMove:
                    ROM_COPY.writeMultipleBytes(int(pad_kong) + 1, 1)
            elif slot in kong_free_switches:
                ROM_COPY.writeMultipleBytes(int(pad_kong), 1)
            else:
                ROM_COPY.writeMultipleBytes(int(pad_kong) + 1, 1)

    slam_req_values = {
        SlamRequirement.green: 1,
        SlamRequirement.blue: 2,
        SlamRequirement.red: 3,
    }
    ROM_COPY.seek(sav + 0x1E3)
    ROM_COPY.write(slam_req_values[spoiler.settings.chunky_phase_slam_req_internal])

    # Camera unlocked
    given_moves = []
    if spoiler.settings.shockwave_status == ShockwaveStatus.start_with:
        given_moves.extend([39, 40])  # 39 = Camera, 40 = Shockwave
        setItemReferenceName(spoiler, Items.CameraAndShockwave, 0, "Extra Training", 0)
    move_bitfields = [0] * 6
    for move in given_moves:
        offset = int(move >> 3)
        check = int(move % 8)
        move_bitfields[offset] |= 0x80 >> check
    for offset, value in enumerate(move_bitfields):
        ROM_COPY.seek(sav + 0xD5 + offset)
        ROM_COPY.writeMultipleBytes(value, 1)

    writeMultiselector(
        spoiler.settings.misc_changes_selected,
        QoLSelector,
        MiscChangesSelected,
        4,
        ROM_COPY,
        sav + 0x0B0,
    )
    writeMultiselector(
        spoiler.settings.remove_barriers_selected,
        RemovedBarrierSelector,
        RemovedBarriersSelected,
        2,
        ROM_COPY,
        sav + 0x1DE,
    )
    writeMultiselector(
        spoiler.settings.faster_checks_selected,
        FasterCheckSelector,
        FasterChecksSelected,
        2,
        ROM_COPY,
        sav + 0x1E0,
    )
    writeMultiselector(
        spoiler.settings.hard_mode_selected,
        HardSelector,
        HardModeSelected,
        1,
        ROM_COPY,
        sav + 0x0C6,
    )

    is_dw = IsDDMSSelected(spoiler.settings.hard_mode_selected, HardModeSelected.donk_in_the_dark_world)
    is_sky = IsDDMSSelected(spoiler.settings.hard_mode_selected, HardModeSelected.donk_in_the_sky)
    if is_dw and is_sky:
        # Memory Challenge
        ROM_COPY.seek(sav + 0x0C6)
        old = int.from_bytes(ROM_COPY.readBytes(1), "big")
        ROM_COPY.seek(sav + 0x0C6)
        ROM_COPY.write(old | 0x8 | 0x2)
    elif is_dw and not is_sky:
        # Dark world only
        ROM_COPY.seek(sav + 0x0C6)
        old = int.from_bytes(ROM_COPY.readBytes(1), "big")
        ROM_COPY.seek(sav + 0x0C6)
        ROM_COPY.write(old | 0x8)
    elif is_sky and not is_dw:
        # Sky only
        ROM_COPY.seek(sav + 0x0C6)
        old = int.from_bytes(ROM_COPY.readBytes(1), "big")
        ROM_COPY.seek(sav + 0x0C6)
        ROM_COPY.write(old | 0x4)

    # Damage amount
    damage_multipliers = {
        DamageAmount.default: 1,
        DamageAmount.double: 2,
        DamageAmount.quad: 4,
        DamageAmount.ohko: 12,
    }
    ROM_COPY.seek(sav + 0x097)
    ROM_COPY.write(damage_multipliers[spoiler.settings.damage_amount])

    ROM_COPY.seek(sav + 0x0C5)
    ROM_COPY.write(int(Types.Enemies in spoiler.settings.shuffled_location_types))

    ROM_COPY.seek(sav + 0x0C2)
    hints_in_pool_handler = 0
    if Types.Hint in spoiler.settings.shuffled_location_types:
        hints_in_pool_handler = 1
        if spoiler.settings.progressive_hint_item != ProgressiveHintItem.off:
            hints_in_pool_handler = 2
    ROM_COPY.write(int(hints_in_pool_handler))

    # Progressive Hints
    count = 0
    if spoiler.settings.progressive_hint_item != ProgressiveHintItem.off:
        count = spoiler.settings.progressive_hint_count
        ROM_COPY.seek(sav + 0x0C3)
        ROM_COPY.write(getProgHintBarrierItem(spoiler.settings.progressive_hint_item))
        for x in range(10):
            ROM_COPY.seek(sav + 0x98 + (x * 2))
            ROM_COPY.writeMultipleBytes(getHintRequirementBatch(x, count), 2)
    ROM_COPY.seek(sav + 0x115)
    ROM_COPY.writeMultipleBytes(count, 1)

    # Microhints
    ROM_COPY.seek(sav + 0x102)
    # The MicrohintsEnabled enum is indexed to allow this.
    ROM_COPY.write(int(spoiler.settings.microhints_enabled))

    # Cutscene Skip Setting
    ROM_COPY.seek(sav + 0x116)
    # The MicrohintsEnabled enum is indexed to allow this.
    ROM_COPY.write(int(spoiler.settings.more_cutscene_skips))

    # Helm Hurry
    helm_hurry_bonuses = [
        spoiler.settings.helmhurry_list_starting_time,
        spoiler.settings.helmhurry_list_golden_banana,
        spoiler.settings.helmhurry_list_blueprint,
        spoiler.settings.helmhurry_list_company_coins,
        spoiler.settings.helmhurry_list_move,
        spoiler.settings.helmhurry_list_banana_medal,
        spoiler.settings.helmhurry_list_rainbow_coin,
        spoiler.settings.helmhurry_list_boss_key,
        spoiler.settings.helmhurry_list_battle_crown,
        spoiler.settings.helmhurry_list_bean,
        spoiler.settings.helmhurry_list_pearl,
        spoiler.settings.helmhurry_list_kongs,
        spoiler.settings.helmhurry_list_fairies,
        spoiler.settings.helmhurry_list_colored_bananas,
        spoiler.settings.helmhurry_list_ice_traps,
    ]
    ROM_COPY.seek(sav + 0xE2)
    for bonus in helm_hurry_bonuses:
        if bonus < 0:
            bonus += 65536
        ROM_COPY.writeMultipleBytes(bonus, 2)

    # Activate Bananaports
    ROM_COPY.seek(sav + 0x138)
    # The ActivateAllBananaports enum is indexed to allow this.
    ROM_COPY.write(int(spoiler.settings.activate_all_bananaports))

    # Fast GBs - Change jetpac text
    if IsDDMSSelected(spoiler.settings.faster_checks_selected, FasterChecksSelected.jetpac):
        data = {"textbox_index": ItemPreview.JetpacIntro, "mode": "replace", "search": "5000", "target": "2500"}
        for file in [CompTextFiles.PreviewsFlavor, CompTextFiles.PreviewsNormal]:
            if file in spoiler.text_changes:
                spoiler.text_changes[file].append(data)
            else:
                spoiler.text_changes[file] = [data]

    if IsDDMSSelected(spoiler.settings.hard_bosses_selected, HardBossesSelected.kut_out_phase_rando):
        # KKO Phase Order
        for phase_slot in range(3):
            ROM_COPY.seek(sav + 0x17B + phase_slot)
            ROM_COPY.write(spoiler.settings.kko_phase_order[phase_slot])

    # Win Condition
    win_con_table = {
        WinConditionComplex.beat_krool: {
            "index": 0,
        },
        WinConditionComplex.get_key8: {
            "index": 1,
        },
        WinConditionComplex.get_keys_3_and_8: {
            "index": 7,
        },
        WinConditionComplex.krem_kapture: {
            "index": 2,
        },
        WinConditionComplex.dk_rap_items: {
            "index": 4,
        },
        WinConditionComplex.krools_challenge: {
            "index": 5,
        },
        WinConditionComplex.kill_the_rabbit: {
            "index": 6,
        },
        WinConditionComplex.req_bean: {
            "index": 3,
            "item": 0xA,
        },
        WinConditionComplex.req_bp: {
            "index": 3,
            "item": 4,
        },
        WinConditionComplex.req_companycoins: {
            "index": 3,
            "item": 8,
        },
        WinConditionComplex.req_crown: {
            "index": 3,
            "item": 7,
        },
        WinConditionComplex.req_fairy: {
            "index": 3,
            "item": 5,
        },
        WinConditionComplex.req_gb: {
            "index": 3,
            "item": 3,
        },
        WinConditionComplex.req_pearl: {
            "index": 3,
            "item": 0xB,
        },
        WinConditionComplex.req_key: {
            "index": 3,
            "item": 6,
        },
        WinConditionComplex.req_medal: {
            "index": 3,
            "item": 9,
        },
        WinConditionComplex.req_rainbowcoin: {
            "index": 3,
            "item": 0xC,
        },
        WinConditionComplex.req_bonuses: {
            "index": 3,
            "item": 0x11,
        },
        WinConditionComplex.req_bosses: {
            "index": 3,
            "item": 0x10,
        },
    }
    win_con = spoiler.settings.win_condition_item
    win_con_data = win_con_table.get(win_con, None)
    if win_con_data is not None:
        ROM_COPY.seek(sav + 0x11D)
        ROM_COPY.write(win_con_data["index"])
        if "item" in win_con_data:
            ROM_COPY.seek(sav + 0xC0)
            ROM_COPY.write(win_con_data["item"])
            ROM_COPY.write(spoiler.settings.win_condition_count)

    # Fungi Time of Day
    fungi_times = (FungiTimeSetting.day, FungiTimeSetting.night, FungiTimeSetting.dusk, FungiTimeSetting.progressive)
    progressive_removals = [5, 4]  # Day Switch, Night Switch
    dusk_removals = {
        Maps.FungiForest: [
            5,  # Day Switch
            4,  # Night Switch
            0xC,  # Day Gate - Mill Front Entry
            0xE,  # Day Gate - Punch Door
            0x12,  # Day Gate - Snide Area
            8,  # Night Gate - Mill Lanky Attic
            0xB,  # Night Gate - Mill Winch Attic
            0xD,  # Night Gate - Dark Attic
            0x11,  # Night Gate - Thornvine Area
            0x2A,  # Night Gate - Mill GB
            0x53,  # Night Gate - Owl Tree Diddy Coins
            0x48,  # Night Gate - Beanstalk T&S
            0x1F1,  # Night Gate - Mushroom Night Door
            0x46,  # Night Gate - Crown Trapdoor
        ],
        Maps.ForestGiantMushroom: [0x11],  # Night Gate - GMush Interior
        Maps.ForestMillFront: [0xB],  # Night Gate - Mill Front
        Maps.ForestMillBack: [
            0xF,  # Night Gate - Mill Rear
            0x2,  # Night Gate - Spider Web
        ],
    }
    time_val = spoiler.settings.fungi_time_internal
    if time_val in fungi_times:
        ROM_COPY.seek(sav + 0x1DB)
        ROM_COPY.write(fungi_times.index(time_val))
        if time_val == FungiTimeSetting.progressive:
            addNewScript(ROM_COPY, Maps.FungiForest, progressive_removals, ScriptTypes.DeleteItem)
        elif time_val == FungiTimeSetting.dusk:
            for map_val in dusk_removals:
                addNewScript(ROM_COPY, map_val, dusk_removals[map_val], ScriptTypes.DeleteItem)

    # Galleon Water Level
    if spoiler.settings.galleon_water_internal == GalleonWaterSetting.raised:
        ROM_COPY.seek(sav + 0x1DC)
        ROM_COPY.writeMultipleBytes(1, 1)

    if spoiler.settings.fast_start_beginning_of_game:
        # Write a null move to this spot if fast start beginning of game is on
        ROM_COPY.seek(spoiler.settings.move_location_data + (125 * 6))
        ROM_COPY.writeMultipleBytes(0, 2)
        ROM_COPY.writeMultipleBytes(0, 4)

    # ROM Flags
    rom_flags = 0
    rom_flags |= 0x80 if spoiler.settings.enable_plandomizer else 0
    rom_flags |= 0x40 if spoiler.settings.generate_spoilerlog else 0
    rom_flags |= 0x20 if spoiler.settings.has_password else 0
    rom_flags |= 0x10 if spoiler.settings.archipelago else 0
    if spoiler.settings.archipelago:
        # Write spoiler.settings.player_name to ROM ASCII only
        ROM_COPY.seek(0x1FF3000)
        # Player name
        player_name = spoiler.settings.player_name[:16]
        # if we're shot on characters, pad with null bytes if we're short on characters
        if len(player_name) < 16:
            player_name += "\0" * (16 - len(player_name))
        # Convert playername to a bytestring and write it to the ROM
        bytestring = str(player_name).encode("ascii")
        ROM_COPY.writeBytes(bytestring)
    ROM_COPY.seek(sav + 0xC4)
    ROM_COPY.writeMultipleBytes(rom_flags, 1)
    password = None
    if spoiler.settings.has_password:
        ROM_COPY.seek(sav + 0x1B0)
        byte_data, password = encPass(spoiler)
        ROM_COPY.writeMultipleBytes(byte_data, 4)

    # Set K. Rool ship spawn method
    ROM_COPY.seek(sav + 0x1B6)
    # Write the user's setting directly - beat_krool/krools_challenge will use key-based spawning unless this is explicitly enabled
    ROM_COPY.writeMultipleBytes(spoiler.settings.win_condition_spawns_ship, 1)

    # Mill Levers
    if spoiler.settings.mill_levers[0] > 0:
        mill_text = ""
        for x in range(5):
            if spoiler.settings.mill_levers[x] > 0:
                mill_text += str(spoiler.settings.mill_levers[x])
        # Change default wrinkly hint
        if spoiler.settings.wrinkly_hints == WrinklyHints.off:
            if (
                IsDDMSSelected(
                    spoiler.settings.faster_checks_selected,
                    FasterChecksSelected.forest_mill_conveyor,
                )
                or spoiler.settings.puzzle_rando_difficulty != PuzzleRando.off
            ):
                data = {"textbox_index": 21, "mode": "replace", "search": "21132", "target": mill_text}
                for file in [CompTextFiles.Wrinkly]:
                    if file in spoiler.text_changes:
                        spoiler.text_changes[file].append(data)
                    else:
                        spoiler.text_changes[file] = [data]

    ROM_COPY.seek(sav + 0x36)
    ROM_COPY.write(spoiler.settings.rareware_gb_fairies)

    ROM_COPY.seek(sav + 0x1EB)
    ROM_COPY.write(spoiler.settings.mermaid_gb_pearls)

    if spoiler.settings.random_starting_region_new != RandomStartingRegion.off:
        ROM_COPY.seek(sav + 0x10C)
        ROM_COPY.write(spoiler.settings.starting_region["map"])
        exit_val = spoiler.settings.starting_region["exit"]
        if exit_val == -1:
            exit_val = 0xFF
        ROM_COPY.write(exit_val)
    if spoiler.settings.alter_switch_allocation:
        ROM_COPY.seek(sav + 0x103)
        ROM_COPY.write(1)
        for x in range(7):  # Shouldn't need index 8 since Helm has no slam switches in it
            ROM_COPY.seek(sav + 0x104 + x)
            ROM_COPY.write(spoiler.settings.switch_allocation[x])
    # Dartboard order
    ROM_COPY.seek(sav + 0x173)
    for x in range(6):
        ROM_COPY.writeMultipleBytes(spoiler.settings.dartboard_order[x], 1)

    ROM_COPY.seek(sav + 0x060)
    for x in spoiler.settings.medal_cb_req_level:
        ROM_COPY.writeMultipleBytes(x, 1)
    if Types.HalfMedal in spoiler.settings.shuffled_location_types:
        ROM_COPY.seek(sav + 0x068)
        ROM_COPY.write(1)

    # Helm Required Minigames - Always set to 2 for now
    ROM_COPY.seek(sav + 0x2D)
    ROM_COPY.write(int(spoiler.settings.helm_room_bonus_count))

    if spoiler.settings.wrinkly_hints != WrinklyHints.off:
        getHelmOrderHint(spoiler)
    randomize_entrances(spoiler, ROM_COPY)
    randomize_moves(spoiler, ROM_COPY)
    randomize_prices(spoiler, ROM_COPY)
    randomize_krool(spoiler, ROM_COPY)
    randomize_helm(spoiler, ROM_COPY)
    randomize_barrels(spoiler, ROM_COPY)
    move_bananaports(spoiler, ROM_COPY)  # Has to be before randomize_bananaport
    randomize_bananaport(spoiler, ROM_COPY)
    randomize_kasplat_locations(spoiler, ROM_COPY)
    randomize_enemies(spoiler, ROM_COPY)
    apply_kongrando_cosmetic(ROM_COPY)
    randomize_setup(spoiler, ROM_COPY)
    randomize_puzzles(spoiler, ROM_COPY)
    randomize_cbs(spoiler, ROM_COPY)
    randomize_coins(spoiler, ROM_COPY)
    place_mayhem_coins(spoiler, ROM_COPY)
    ApplyShopRandomizer(spoiler, ROM_COPY)
    remove5DSCameraPoint(spoiler, ROM_COPY)
    alterTextboxRequirements(spoiler)
    spoiler.arcade_item_reward = Items.NintendoCoin
    spoiler.jetpac_item_reward = Items.RarewareCoin
    place_randomized_items(spoiler, ROM_COPY)  # Has to be after kong rando cosmetic and moves
    place_spoiler_hint_data(sav, spoiler, ROM_COPY)
    # Arcade detection for colorblind mode
    arcade_item_index = 0
    potion_pools = [
        ItemPool.DonkeyMoves,
        ItemPool.DiddyMoves,
        ItemPool.LankyMoves,
        ItemPool.TinyMoves,
        ItemPool.ChunkyMoves,
        ItemPool.ImportantSharedMoves + ItemPool.JunkSharedMoves + ItemPool.TrainingBarrelAbilities() + ItemPool.ClimbingAbilities() + [Items.Shockwave, Items.Camera, Items.CameraAndShockwave],
    ]
    for index, lst in enumerate(potion_pools):
        if spoiler.arcade_item_reward in lst:
            arcade_item_index = 1 + index
    ROM_COPY.seek(sav + 0x15A)
    ROM_COPY.writeMultipleBytes(arcade_item_index, 1)
    # Other funcs
    place_pregiven_moves(spoiler, ROM_COPY)
    remove_existing_indicators(spoiler, ROM_COPY)
    place_door_locations(spoiler, ROM_COPY)
    randomize_crown_pads(spoiler, ROM_COPY)
    randomize_melon_crate(spoiler, ROM_COPY)
    PlaceFairies(spoiler, ROM_COPY)
    filterEntranceType(ROM_COPY)
    updateKrushaMoveNames(spoiler)
    updateSwitchsanity(spoiler, ROM_COPY)
    updateRandomSwitches(spoiler, ROM_COPY)  # Has to be after all setup changes that may alter the item type of slam switches
    PushItemLocations(spoiler, ROM_COPY)

    if spoiler.settings.wrinkly_hints != WrinklyHints.off:
        PushHints(spoiler, ROM_COPY)
        if spoiler.settings.dim_solved_hints:
            PushHelpfulHints(spoiler, ROM_COPY)
    if Types.Hint in spoiler.settings.shuffled_location_types and spoiler.settings.progressive_hint_item == ProgressiveHintItem.off:
        PushHintTiedRegions(spoiler, ROM_COPY)

    writeBootMessages(ROM_COPY, spoiler)
    enableTriggerText(spoiler, ROM_COPY)
    shortenCastleMinecart(spoiler, ROM_COPY)
    alterStoryCutsceneWarps(spoiler, ROM_COPY)

    if "PYTEST_CURRENT_TEST" not in os.environ:
        replaceIngameText(spoiler, ROM_COPY)
        updateMillLeverTexture(spoiler.settings, ROM_COPY)
        updateCryptLeverTexture(spoiler.settings, ROM_COPY)
        updateDiddyDoors(spoiler.settings, ROM_COPY)
        applyHelmDoorCosmetics(spoiler.settings, ROM_COPY)
        applyKongModelSwaps(spoiler.settings, ROM_COPY)
        updateHelmFaces(spoiler.settings, ROM_COPY)
        updateSnidePanel(spoiler.settings, ROM_COPY)
        showWinCondition(spoiler.settings, ROM_COPY)

        patchAssembly(ROM_COPY, spoiler)
        calculateInitFileScreen(spoiler, ROM_COPY)
        ApplyMirrorMode(spoiler.settings, ROM_COPY)

    # Apply Hash
    order = 0
    for count in spoiler.settings.seed_hash:
        ROM_COPY.seek(sav + 0x129 + order)
        ROM_COPY.write(count)
        order += 1

    # Create a dummy time to attach to the end of the file name non decimal
    str(time.time()).replace(".", "")
    if "PYTEST_CURRENT_TEST" not in os.environ:
        created_tempfile = mktemp()
        delta_tempfile = mktemp()
        # Write the LocalROM.rom bytesIo to a file
        with open(created_tempfile, "wb") as f:
            f.write(ROM_COPY.rom.getvalue())

        import pyxdelta

        pyxdelta.run("dk64.z64", created_tempfile, delta_tempfile)
        # Read the patch file
        with open(delta_tempfile, "rb") as f:
            patch = f.read()
        # Delete the patch.z64 file
        os.remove(created_tempfile)
        os.remove(delta_tempfile)
    else:
        patch = None
    del ROM_COPY
    return patch, password


def FormatSpoiler(value):
    """Format the values passed to the settings table into a more readable format.

    Args:
        value (str) or (bool)
    """
    string = str(value)
    formatted = string.replace("_", " ")
    result = formatted.title()
    return result
