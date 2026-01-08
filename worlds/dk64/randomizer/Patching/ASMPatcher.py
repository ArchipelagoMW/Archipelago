"""Patches assembly instructions from the overlays rather than doing changes live."""

import js
import math
import io
import randomizer.ItemPool as ItemPool
from typing import Union
from randomizer.Patching.Library.Generic import Overlay, IsItemSelected, compatible_background_textures, CustomActors, MenuTextDim, Holidays, getHoliday, getHolidaySetting
from randomizer.Patching.Library.Image import getImageFile, TextureFormat, getRandomHueShift, ExtraTextures, getBonusSkinOffset, hueShiftImageFromAddress
from randomizer.Patching.Library.ASM import *
from randomizer.Settings import Settings
from randomizer.Enums.Settings import (
    FasterChecksSelected,
    RemovedBarriersSelected,
    GalleonWaterSetting,
    ActivateAllBananaports,
    FreeTradeSetting,
    HardModeSelected,
    HardBossesSelected,
    FungiTimeSetting,
    MiscChangesSelected,
    ColorblindMode,
    DamageAmount,
    RandomModels,
    PuzzleRando,
    WinConditionComplex,
    ExtraCutsceneSkips,
    ExcludedSongs,
    ProgressiveHintItem,
    WrinklyHints,
)
from randomizer.Patching.MiscSetupChanges import SpeedUpFungiRabbit
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Levels import Levels
from randomizer.Lists.MapsAndExits import GetExitId, GetMapId
from randomizer.Enums.Models import Model, Sprite
from randomizer.Patching.Patcher import ROM, LocalROM
from randomizer.Enums.Settings import ShuffleLoadingZones
from randomizer.Enums.Types import Types
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Items import Items
from PIL import Image

KEY_FLAG_ADDRESSES = [
    0x800258FA,
    0x8002C136,
    0x80035676,
    0x8002A0C2,
    0x8002B3F6,
    0x80025C4E,
    0x800327EE,
]
REGULAR_BOSS_MAPS = [
    Maps.JapesBoss,
    Maps.AztecBoss,
    Maps.FactoryBoss,
    Maps.GalleonBoss,
    Maps.FungiBoss,
    Maps.CavesBoss,
    Maps.CastleBoss,
]
NORMAL_KEY_FLAGS = [
    0x1A,  # Key 1
    0x4A,  # Key 2
    0x8A,  # Key 3
    0xA8,  # Key 4
    0xEC,  # Key 5
    0x124,  # Key 6
    0x13D,  # Key 7
    0x17C,  # Key 8
]
ENABLE_ALL_KONG_TRANSFORMS = False
ENABLE_HITSCAN = False
DISABLE_BORDERS = False
ENABLE_MINIGAME_SPRITE_RANDO = False
ENABLE_HELM_GBS = True
ENABLE_BLAST_LZR = False
POP_TARGETTING = True
UNSHROUDED_CASTLE = False
FARPLANE_VIEW = False
KLAPTRAPS_IN_SEARCHLIGHT_SEEK = 1
FAIRY_LOAD_FIX = True
CAMERA_RESET_REDUCTION = True
PAL_DOGADON_REMATCH_FIRE = True
REMOVE_CS_BARS = False
GREATER_CAMERA_CONTROL = True
JP_TEXTBOX_SIZES = True
FRAMEBUFFER_STORE_FIX = True
BLOCK_FILE_DELETION_ON_CHECKSUM_MISMATCH = False

WARPS_JAPES = [
    0x20,  # FLAG_WARP_JAPES_W1_PORTAL,
    0x21,  # FLAG_WARP_JAPES_W1_FAR,
    0x22,  # FLAG_WARP_JAPES_W2_HIGH,
    0x23,  # FLAG_WARP_JAPES_W2_LOW,
    0x24,  # FLAG_WARP_JAPES_W3_RIGHT,
    0x25,  # FLAG_WARP_JAPES_W3_LEFT,
    0x28,  # FLAG_WARP_JAPES_W4_CLOSE,
    0x29,  # FLAG_WARP_JAPES_W4_CRANKY,
    0x26,  # FLAG_WARP_JAPES_W5_SHELLHIVE,
    0x27,  # FLAG_WARP_JAPES_W5_TOP,
]

WARPS_AZTEC = [
    0x4F,  # FLAG_WARP_AZTEC_W1_PORTAL,
    0x50,  # FLAG_WARP_AZTEC_W1_CANDY,
    0x51,  # FLAG_WARP_AZTEC_W2_TEMPLE,
    0x52,  # FLAG_WARP_AZTEC_W2_TOTEM,
    0x53,  # FLAG_WARP_AZTEC_W3_CRANKY,
    0x54,  # FLAG_WARP_AZTEC_W3_TOTEM,
    0x55,  # FLAG_WARP_AZTEC_W4_TOTEM,
    0x56,  # FLAG_WARP_AZTEC_W4_FUNKY,
    0x57,  # FLAG_WARP_AZTEC_W5_TOTEM,
    0x2F5,  # AZTEC_SNOOPW5, # Custom Flag
    0x58,  # FLAG_WARP_LLAMA_W1_HIGH,
    0x59,  # FLAG_WARP_LLAMA_W1_LOW,
    0x5A,  # FLAG_WARP_LLAMA_W2_FAR,
    0x5B,  # FLAG_WARP_LLAMA_W2_LOW,
]

WARPS_FACTORY = [
    0x8D,  # FLAG_WARP_FACTORY_W1_FOYER,
    0x8E,  # FLAG_WARP_FACTORY_W1_STORAGE,
    0x8F,  # FLAG_WARP_FACTORY_W2_FOYER,
    0x90,  # FLAG_WARP_FACTORY_W2_RND,
    0x91,  # FLAG_WARP_FACTORY_W3_FOYER,
    0x92,  # FLAG_WARP_FACTORY_W3_SNIDE,
    0x93,  # FLAG_WARP_FACTORY_W4_TOP,
    0x94,  # FLAG_WARP_FACTORY_W4_BOTTOM,
    0x95,  # FLAG_WARP_FACTORY_W5_FUNKY,
    0x96,  # FLAG_WARP_FACTORY_W5_ARCADE,
]

WARPS_GALLEON = [
    0xB1,  # FLAG_WARP_GALLEON_W1_LIGHTHOUSE,
    0xB2,  # FLAG_WARP_GALLEON_W1_CRANKY,
    0xAB,  # FLAG_WARP_GALLEON_W2_2DS,
    0xAC,  # FLAG_WARP_GALLEON_W2_CRANKY,
    0xAD,  # FLAG_WARP_GALLEON_W3_SNIDE,
    0xAE,  # FLAG_WARP_GALLEON_W3_CRANKY,
    0xAF,  # FLAG_WARP_GALLEON_W4_SEAL,
    0x2F6,  # GALLEON_TOWERW4, # Activating the gold tower warp despawns Diddy's GB
    0xA9,  # FLAG_WARP_GALLEON_W5_5DS,
    0xAA,  # FLAG_WARP_GALLEON_W5_LIGHTHOUSE,
]

WARPS_FUNGI = [
    0xED,  # FLAG_WARP_FUNGI_W1_MILL,
    0xEE,  # FLAG_WARP_FUNGI_W1_CLOCK,
    0xEF,  # FLAG_WARP_FUNGI_W2_CLOCK,
    0xF0,  # FLAG_WARP_FUNGI_W2_FUNKY,
    0xF1,  # FLAG_WARP_FUNGI_W3_CLOCK,
    0xF2,  # FLAG_WARP_FUNGI_W3_MUSH,
    0xF3,  # FLAG_WARP_FUNGI_W4_CLOCK,
    0xF4,  # FLAG_WARP_FUNGI_W4_OWL,
    0xF5,  # FLAG_WARP_FUNGI_W5_LOW,
    0xF6,  # FLAG_WARP_FUNGI_W5_HIGH,
]

WARPS_CAVES = [
    0x11B,  # FLAG_WARP_CAVES_W1_5DI,
    0x11C,  # FLAG_WARP_CAVES_W1_PORTAL,
    0x11D,  # FLAG_WARP_CAVES_W2_PORTAL,
    0x11E,  # FLAG_WARP_CAVES_W2_FAR,
    0x123,  # FLAG_WARP_CAVES_W3_5DI,
    0x2F7,  # CAVES_HIDDENW3,
    0x11F,  # FLAG_WARP_CAVES_W4_FAR,
    0x120,  # FLAG_WARP_CAVES_W4_5DI,
    0x121,  # FLAG_WARP_CAVES_W5_5DC,
    0x122,  # FLAG_WARP_CAVES_W5_PILLAR,
]

WARPS_CASTLE = [
    0x147,  # FLAG_WARP_CASTLE_W1_HUB,
    0x148,  # FLAG_WARP_CASTLE_W1_FAR,
    0x149,  # FLAG_WARP_CASTLE_W2_HUB,
    0x14A,  # FLAG_WARP_CASTLE_W2_HIGH,
    0x14B,  # FLAG_WARP_CASTLE_W3_HUB,
    0x14C,  # FLAG_WARP_CASTLE_W3_HIGH,
    0x14D,  # FLAG_WARP_CASTLE_W4_HUB,
    0x14E,  # FLAG_WARP_CASTLE_W4_HIGH,
    0x14F,  # FLAG_WARP_CASTLE_W5_HUB,
    0x150,  # FLAG_WARP_CASTLE_W5_HIGH,
    0x151,  # FLAG_WARP_CRYPT_W1_CLOSE,
    0x152,  # FLAG_WARP_CRYPT_W1_FAR,
    0x153,  # FLAG_WARP_CRYPT_W2_CLOSE,
    0x154,  # FLAG_WARP_CRYPT_W2_FAR,
    0x155,  # FLAG_WARP_CRYPT_W3_CLOSE,
    0x156,  # FLAG_WARP_CRYPT_W3_FAR,
]

WARPS_ISLES = [
    0x1B1,  # FLAG_WARP_ISLES_W1_RING,
    0x1B2,  # FLAG_WARP_ISLES_W1_FAR,
    0x1B3,  # FLAG_WARP_ISLES_W2_RING,
    0x1B4,  # FLAG_WARP_ISLES_W2_FAR,
    0x1B5,  # FLAG_WARP_ISLES_W3_RING,
    0x1B6,  # FLAG_WARP_ISLES_W3_FAR,
    0x1B7,  # FLAG_WARP_ISLES_W4_RING,
    0x1B8,  # FLAG_WARP_ISLES_W4_HIGH,
    0x1BA,  # FLAG_WARP_ISLES_W5_RING,
    0x1B9,  # FLAG_WARP_ISLES_W5_FAR,
]

WARPS_HELM_LOBBY = [
    0x1A1,  # Near Warp
    0x1A2,  # Far Warp
]

WARPS_TOTAL = [
    WARPS_JAPES,
    WARPS_AZTEC,
    WARPS_FACTORY,
    WARPS_GALLEON,
    WARPS_FUNGI,
    WARPS_CAVES,
    WARPS_CASTLE,
    WARPS_ISLES,
    WARPS_HELM_LOBBY,
]


class ColorBlindCrosshair:
    """Store all information regarding a colorblind crosshair color data."""

    def __init__(self, regular: int, homing: int, sniper: int):
        """Initialize with given parameters."""
        self.regular = regular
        self.homing = homing
        self.sniper = sniper

    def writeRGBColors(self, ROM_COPY, offset_dict: dict, value: int, upper_address: int, lower_address: int):
        """Write the RGB colors to ROM."""
        hi = value >> 8
        lo = ((value & 0xFF) << 8) | 0xFF
        writeValue(ROM_COPY, upper_address, Overlay.Static, hi, offset_dict)
        writeValue(ROM_COPY, lower_address, Overlay.Static, lo, offset_dict)


CROSSHAIRS = {
    ColorblindMode.off: ColorBlindCrosshair(0xC80000, 0x00C800, 0xFFD700),
    ColorblindMode.prot: ColorBlindCrosshair(0x0072FF, 0xFFFFFF, 0xFDE400),
    ColorblindMode.deut: ColorBlindCrosshair(0x318DFF, 0xFFFFFF, 0xE3A900),
    ColorblindMode.trit: ColorBlindCrosshair(0xC72020, 0xFFFFFF, 0x13C4D8),
}


def fixLankyIncompatibility(ROM_COPY: ROM):
    """Ensure compatibility with .lanky files created during a specific time frame."""
    offset_dict = populateOverlayOffsets(ROM_COPY)
    if readValue(ROM_COPY, 0x80602AB0, Overlay.Static, offset_dict, 4) != 0x0C180917:
        writeValue(ROM_COPY, 0x80602AAC, Overlay.Static, 0x27A40018, offset_dict, 4)  # addiu $a0, $sp, 0x18


def patchAssemblyCosmetic(ROM_COPY: ROM, settings: Settings, has_dom: bool = True):
    """Patch assembly instructions that pertain to cosmetic changes."""
    offset_dict = populateOverlayOffsets(ROM_COPY)
    holiday = getHoliday(settings)

    troff_light = 1 if settings.troff_brighten else 0.15
    writeFloat(ROM_COPY, 0x8075B8B0, Overlay.Static, troff_light, offset_dict)

    if settings.remove_water_oscillation:
        writeValue(ROM_COPY, 0x80661B54, Overlay.Static, 0, offset_dict, 4)  # Remove Ripple Timer 0
        writeValue(ROM_COPY, 0x80661B64, Overlay.Static, 0, offset_dict, 4)  # Remove Ripple Timer 1
        writeValue(ROM_COPY, 0x8068BDF4, Overlay.Static, 0, offset_dict, 4)  # Disable rocking in Seasick Ship
        writeValue(ROM_COPY, 0x8068BDFC, Overlay.Static, 0x1000, offset_dict)  # Disable rocking in Mech Fish
        writeValue(ROM_COPY, 0x805FCCEE, Overlay.Static, 0, offset_dict)  # Disable seasick camera effect

    writeValue(ROM_COPY, 0x8075F602, Overlay.Static, settings.caves_tomato_model + 1, offset_dict)
    writeValue(ROM_COPY, 0x8075F4E2, Overlay.Static, settings.fungi_tomato_model + 1, offset_dict)
    writeValue(ROM_COPY, 0x806F0376, Overlay.Static, settings.bother_klaptrap_model + 1, offset_dict)
    writeValue(ROM_COPY, 0x806C8B42, Overlay.Static, settings.bother_klaptrap_model + 1, offset_dict)

    if settings.rabbit_model == Model.Beetle:
        writeValue(ROM_COPY, 0x8075F242, Overlay.Static, Model.Beetle + 1, offset_dict)  # Rabbit Race
        # Animation scale
        writeValue(ROM_COPY, 0x806BE942, Overlay.Static, 0x285, offset_dict)
        writeValue(ROM_COPY, 0x806BEFC2, Overlay.Static, 0x282, offset_dict)
        writeValue(ROM_COPY, 0x806BF052, Overlay.Static, 0x282, offset_dict)
        writeValue(ROM_COPY, 0x806BF066, Overlay.Static, 0x282, offset_dict)
        writeValue(ROM_COPY, 0x806BF0C2, Overlay.Static, 0x281, offset_dict)
        writeValue(ROM_COPY, 0x806BF1D2, Overlay.Static, 0x281, offset_dict)
        writeValue(ROM_COPY, 0x806BEA8A, Overlay.Static, 0x281, offset_dict)
        writeValue(ROM_COPY, 0x806BEB6A, Overlay.Static, 0x282, offset_dict)
        writeValue(ROM_COPY, 0x806BF1DE, Overlay.Static, 0x282, offset_dict)
        writeValue(ROM_COPY, 0x8075F244, Overlay.Static, 0x282, offset_dict)
        writeValue(ROM_COPY, 0x806BE9B2, Overlay.Static, 0x287, offset_dict)
        writeValue(ROM_COPY, 0x806BED5E, Overlay.Static, 0x288, offset_dict)
        SpeedUpFungiRabbit(ROM_COPY, 1.62)
        # Chunky 5DI
        writeValue(ROM_COPY, 0x8075F3F2, Overlay.Static, Model.Beetle + 1, offset_dict)
        writeValue(ROM_COPY, 0x806B23C6, Overlay.Static, 0x287, offset_dict)

    # Misc Model Swaps
    writeValue(ROM_COPY, 0x8002A55E, Overlay.Bonus, settings.panic_klaptrap_model + 1, offset_dict)
    writeValue(ROM_COPY, 0x8002C22E, Overlay.Bonus, settings.seek_klaptrap_model + 1, offset_dict)
    writeValue(ROM_COPY, 0x80028776, Overlay.Bonus, settings.turtle_model + 1, offset_dict)
    writeValue(ROM_COPY, 0x8002A656, Overlay.Bonus, settings.panic_fairy_model + 1, offset_dict)
    writeValue(ROM_COPY, 0x8074F212, Overlay.Static, settings.piano_burp_model + 1, offset_dict)
    writeValue(ROM_COPY, 0x8075F122, Overlay.Static, settings.spotlight_fish_model + 1, offset_dict)
    writeValue(ROM_COPY, 0x80755758, Overlay.Static, settings.candy_cutscene_model + 1, offset_dict)
    writeValue(ROM_COPY, 0x8075575A, Overlay.Static, settings.funky_cutscene_model + 1, offset_dict)
    writeValue(ROM_COPY, 0x8075578C, Overlay.Static, settings.boot_cutscene_model + 1, offset_dict)

    # Refill Count
    if ENABLE_MINIGAME_SPRITE_RANDO:
        projectile_mapping = {
            Sprite.BouncingMelon: Sprite.VerticalRollingMelon,
            Sprite.BouncingOrange: Sprite.Orange,
        }
        is_new_sprite = settings.minigame_melon_sprite != Sprite.BouncingMelon
        projectile_sprite = projectile_mapping.get(settings.minigame_melon_sprite, settings.minigame_melon_sprite)
        is_small_sprite = settings.minigame_melon_sprite in (Sprite.BouncingMelon, Sprite.BouncingOrange)
        hi = getHi(int(settings.minigame_melon_sprite)) if is_new_sprite else 0x8072
        lo = getLo(int(settings.minigame_melon_sprite)) if is_new_sprite else 0xFFD4
        proj_hi = getHi(int(projectile_sprite)) if is_new_sprite else 0x8072
        proj_lo = getLo(int(projectile_sprite)) if is_new_sprite else 0x0020
        writeValue(ROM_COPY, 0x8002737E, Overlay.Bonus, hi, offset_dict)
        writeValue(ROM_COPY, 0x8002739A, Overlay.Bonus, lo, offset_dict)
        writeValue(ROM_COPY, 0x80027366, Overlay.Bonus, 0x3F80 if is_small_sprite else 0x3F33, offset_dict)
        writeValue(ROM_COPY, 0x8069274E, Overlay.Static, proj_hi, offset_dict)
        writeValue(ROM_COPY, 0x8069275A, Overlay.Static, proj_lo, offset_dict)
        writeValue(ROM_COPY, 0x80027448, Overlay.Bonus, 0x3C073F80, offset_dict, 4)  # Ensure melon sfx is always usual pitch

    # Skybox Handler
    skybox_rgba = None
    random_skybox = False
    if settings.colorblind_mode != ColorblindMode.off:
        skybox_rgba = [0x31, 0x33, 0x38]
    elif getHolidaySetting(settings):
        skybox_rgba = [0, 0, 0]
    elif settings.misc_cosmetics:
        random_skybox = True
    if skybox_rgba is not None or random_skybox:
        for x in range(8):
            used_arr = skybox_rgba
            if random_skybox:
                used_arr = [settings.random.randint(0, 255), settings.random.randint(0, 255), settings.random.randint(0, 255)]
            if used_arr is not None:
                for zi, z in enumerate(used_arr):
                    writeValue(ROM_COPY, 0x80754EF8 + (12 * x) + zi, Overlay.Static, z, offset_dict, 1)
                # Calculate secondary blend
                backup_rgb = used_arr.copy()
                exceeded = False
                for y in range(3):
                    used_arr[y] = int(used_arr[y] * 1.2)
                    if used_arr[y] > 255:
                        exceeded = True
                if exceeded:
                    for y in range(3):
                        used_arr[y] = int(backup_rgb[y] * 0.8)
                # Write secondary blend
                for y in range(3):
                    for zi, z in enumerate(used_arr):
                        writeValue(ROM_COPY, 0x80754EF8 + (12 * x) + ((y + 1) * 3) + zi, Overlay.Static, z, offset_dict, 1)
        writeValue(ROM_COPY, 0x8075E1EC, Overlay.Static, 0x80708234, offset_dict, 4)

    writeValue(ROM_COPY, 0x8064F052, Overlay.Static, settings.wrinkly_rgb[0], offset_dict)
    writeValue(ROM_COPY, 0x8064F04A, Overlay.Static, settings.wrinkly_rgb[1], offset_dict)
    writeValue(ROM_COPY, 0x8064F046, Overlay.Static, settings.wrinkly_rgb[2], offset_dict)
    if settings.misc_cosmetics:
        # Menu Background
        if settings.menu_texture_index is not None:
            writeValue(ROM_COPY, 0x8070761A, Overlay.Static, 0, offset_dict)
            dimensions = compatible_background_textures[settings.menu_texture_index].dim
            if dimensions == MenuTextDim.size_w32_h32:
                writeValue(ROM_COPY, 0x8070762E, Overlay.Static, 0xFFE0, offset_dict)
                writeValue(ROM_COPY, 0x8070727E, Overlay.Static, 0xC07C, offset_dict)
                writeValue(ROM_COPY, 0x80707222, Overlay.Static, 0x073F, offset_dict)
            elif dimensions == MenuTextDim.size_w64_h32:
                writeValue(ROM_COPY, 0x8070762E, Overlay.Static, 0xFFE0, offset_dict)
                writeValue(ROM_COPY, 0x8070727E, Overlay.Static, 0xC07C, offset_dict)
                writeValue(ROM_COPY, 0x80707616, Overlay.Static, 0x40, offset_dict)
                writeValue(ROM_COPY, 0x80707272, Overlay.Static, 0xF, offset_dict)
                writeValue(ROM_COPY, 0x80707226, Overlay.Static, 0xF080, offset_dict)
                writeValue(ROM_COPY, 0x8070725A, Overlay.Static, 0x2000, offset_dict)
                writeValue(ROM_COPY, 0x807072A2, Overlay.Static, 0x0100, offset_dict)
            writeValue(
                ROM_COPY,
                0x80707126,
                Overlay.Static,
                compatible_background_textures[settings.menu_texture_index].table,
                offset_dict,
            )
            menu_background_rgba = 0x505050FF
            if compatible_background_textures[settings.menu_texture_index].is_color:
                menu_background_rgba = 0x000020FF  # TODO: Get colors working properly
            writeValue(ROM_COPY, 0x8075EAE4, Overlay.Static, menu_background_rgba, offset_dict, 4)
            writeValue(ROM_COPY, 0x80754CEC, Overlay.Static, settings.menu_texture_index, offset_dict)

    crosshair_img = 113 if settings.crosshair_outline else 0x38
    writeValue(ROM_COPY, 0x806FFAFE, Overlay.Static, crosshair_img, offset_dict)
    writeValue(ROM_COPY, 0x806FF116, Overlay.Static, crosshair_img, offset_dict)
    writeValue(ROM_COPY, 0x806B78DA, Overlay.Static, crosshair_img, offset_dict)

    if IsItemSelected(settings.songs_excluded, settings.excluded_songs_selected, ExcludedSongs.pause_music, False):
        writeValue(ROM_COPY, 0x805FC890, Overlay.Static, 0, offset_dict, 4)  # Pause Theme
        writeValue(ROM_COPY, 0x805FC89C, Overlay.Static, 0, offset_dict, 4)  # Pause Start Theme
    if IsItemSelected(settings.songs_excluded, settings.excluded_songs_selected, ExcludedSongs.wrinkly, False):
        writeValue(ROM_COPY, 0x8064F180, Overlay.Static, 0, offset_dict, 4)  # Wrinkly Theme
    if IsItemSelected(settings.songs_excluded, settings.excluded_songs_selected, ExcludedSongs.transformation, False):
        writeValue(ROM_COPY, 0x8067E9E4, Overlay.Static, 0, offset_dict, 4)  # Transform Theme
        writeValue(ROM_COPY, 0x8067F7C0, Overlay.Static, 0, offset_dict, 4)  # Transform Theme
    if IsItemSelected(settings.songs_excluded, settings.excluded_songs_selected, ExcludedSongs.sub_areas, False):
        # writeValue(ROM_COPY, 0x806025BC, Overlay.Static, 0, offset_dict, 4) # Disable `playLevelMusic` - Map Load
        writeValue(ROM_COPY, 0x8061DF74, Overlay.Static, 0, offset_dict, 4)  # Disable `playLevelMusic`
        writeValue(ROM_COPY, 0x806DB98C, Overlay.Static, 0, offset_dict, 4)  # Disable `playLevelMusic`
        writeValue(ROM_COPY, 0x806034F2, Overlay.Static, 0, offset_dict)  # Set Japes count to 0
        writeValue(ROM_COPY, 0x80603556, Overlay.Static, 0, offset_dict)  # Set Az Beetle count to 0
        writeValue(ROM_COPY, 0x80603542, Overlay.Static, 0, offset_dict)  # Set Factory count to 0
        writeValue(ROM_COPY, 0x8060356A, Overlay.Static, 0, offset_dict)  # Set Factory Car count to 0
        writeValue(ROM_COPY, 0x8060351A, Overlay.Static, 0, offset_dict)  # Set Galleon count to 0
        # writeValue(ROM_COPY, 0x80603592, Overlay.Static, 0, offset_dict) # Set Isles count to 0
        writeValue(ROM_COPY, 0x80603506, Overlay.Static, 0, offset_dict)  # Set Aztec count to 0
        writeValue(ROM_COPY, 0x8060352E, Overlay.Static, 0, offset_dict)  # Set Galleon Seal count to 0
        writeValue(ROM_COPY, 0x806035C6, Overlay.Static, 0, offset_dict)  # Set Fungi count to 0
        writeValue(ROM_COPY, 0x8060357E, Overlay.Static, 0, offset_dict)  # Set Fungi Cart count to 0
        writeValue(ROM_COPY, 0x806035BA, Overlay.Static, 0, offset_dict)  # Set TGrounds count to 0
    if settings.music_disable_reverb:
        # Disable volume changes that would counteract the dynamic reverb's volume loss
        writeValue(ROM_COPY, 0x80603DB8, Overlay.Static, 0x10000011, offset_dict, 4)  # B 80603E00

    # Holiday Mode Stuff
    if holiday == Holidays.Halloween:
        writeValue(ROM_COPY, 0x800271F2, Overlay.Bonus, Model.Krossbones + 1, offset_dict)  # Green
        writeValue(ROM_COPY, 0x80027216, Overlay.Bonus, Model.RoboKremling + 1, offset_dict)  # Red
        writeValue(ROM_COPY, 0x8075E0B8, Overlay.Static, 0x807080E0, offset_dict, 4)  # Makes isles reference Castle skybox data
        # Chains
        writeValue(ROM_COPY, 0x8069901A, Overlay.Static, 0xE, offset_dict)  # Vine param
        writeValue(ROM_COPY, 0x8069903A, Overlay.Static, 0xE, offset_dict)  # Vine param
        writeValue(ROM_COPY, 0x80698754, Overlay.Static, 0, offset_dict, 4)  # Cancel branch
        writeValue(ROM_COPY, 0x80698B6C, Overlay.Static, 0, offset_dict, 4)  # Cancel branch
        writeValue(ROM_COPY, 0x80698B74, Overlay.Static, 0x1000, offset_dict)  # Force branch
    elif holiday == Holidays.Christmas:
        # Make santa visit Isles
        writeValue(ROM_COPY, 0x8070637E, Overlay.Static, 115, offset_dict)  # Moon Image
        writeValue(ROM_COPY, 0x8075E0B8, Overlay.Static, 0x807080E0, offset_dict, 4)  # Makes isles reference Castle skybox data
        writeValue(ROM_COPY, 0x806682C8, Overlay.Static, 0x240E0004, offset_dict, 4)  # Set ground sfx to snow
        writeValue(ROM_COPY, 0x806682CC, Overlay.Static, 0x240C0004, offset_dict, 4)  # Set ground sfx to snow
        writeValue(ROM_COPY, 0x806682DC, Overlay.Static, 0x240E0004, offset_dict, 4)  # Set ground sfx to snow
    elif holiday == Holidays.Anniv25:
        # Change barrel base sprite
        writeValue(ROM_COPY, 0x80721458, Overlay.Static, getBonusSkinOffset(ExtraTextures.Anniv25Barrel), offset_dict)
    # Smoother Camera
    if settings.smoother_camera:
        camera_change_cooldown = 5
        writeValue(ROM_COPY, 0x806EA238, Overlay.Static, 0, offset_dict, 4)  # Disable it requiring a new input
        writeValue(ROM_COPY, 0x806EA2A4, Overlay.Static, 0, offset_dict, 4)  # Disable it requiring a new input
        camera_change_amount = 5 * (camera_change_cooldown - 2)
        addr = getROMAddress(0x806EA25E, Overlay.Static, offset_dict)
        ROM_COPY.seek(addr)
        val = int.from_bytes(ROM_COPY.readBytes(2), "big")
        if (val & 0x8000) == 0:  # Is Mirror Mode
            camera_change_amount = -camera_change_amount
        writeValue(ROM_COPY, 0x806EA256, Overlay.Static, camera_change_cooldown, offset_dict)
        writeValue(ROM_COPY, 0x806EA25E, Overlay.Static, -camera_change_amount, offset_dict, 2, True)
        writeValue(ROM_COPY, 0x806EA2C2, Overlay.Static, camera_change_cooldown, offset_dict)
        writeValue(ROM_COPY, 0x806EA2CA, Overlay.Static, camera_change_amount, offset_dict, 2, True)

    if GREATER_CAMERA_CONTROL:
        NULL_FUNCTION = 0x806E1864
        TURN_FUNCTION = 0x806EA628
        FUNCTION_TABLE = {
            # 0x24: 0x806E607C,  # R_FUNCTION
            0x34: 0x806EA200,  # CL_FUNCTION
            0x38: 0x806EA26C,  # CR_FUNCTION
        }

        for x in range(107):
            if x in (0, 4):
                continue
            rom_base_addr = getROMAddress(0x80751004 + (0x44 * x), Overlay.Static, offset_dict)
            ROM_COPY.seek(rom_base_addr + 4)
            always_function = int.from_bytes(ROM_COPY.readBytes(4), "big")
            if always_function == TURN_FUNCTION:
                # If you can turn the camera with the control stick, ban using the C buttons for that
                continue
            for offset in FUNCTION_TABLE:
                ROM_COPY.seek(rom_base_addr + offset)
                original_function = int.from_bytes(ROM_COPY.readBytes(4), "big")
                if original_function == NULL_FUNCTION:
                    ROM_COPY.seek(rom_base_addr + offset)
                    ROM_COPY.writeMultipleBytes(FUNCTION_TABLE[offset], 4)

    # Crosshair
    if settings.colorblind_mode != ColorblindMode.off:
        writeValue(ROM_COPY, 0x8069E974, Overlay.Static, 0x1000, offset_dict)  # Force first option
        writeValue(ROM_COPY, 0x8069E9B0, Overlay.Static, 0, offset_dict, 4)  # Prevent write
        writeValue(ROM_COPY, 0x8069E9B4, Overlay.Static, 0, offset_dict, 4)  # Prevent write
        writeValue(ROM_COPY, 0x8069E9BC, Overlay.Static, 0, offset_dict, 4)  # Prevent write
    ref_crosshair = CROSSHAIRS[settings.colorblind_mode]
    ref_crosshair.writeRGBColors(ROM_COPY, offset_dict, ref_crosshair.sniper, 0x806FFA92, 0x806FFA96)
    ref_crosshair.writeRGBColors(ROM_COPY, offset_dict, ref_crosshair.homing, 0x806FFA76, 0x806FFA7A)
    ref_crosshair.writeRGBColors(ROM_COPY, offset_dict, ref_crosshair.regular, 0x806FF0C6, 0x806FF0CA)
    ref_crosshair.writeRGBColors(ROM_COPY, offset_dict, ref_crosshair.homing, 0x806FF0AA, 0x806FF0AE)
    if has_dom:
        if settings.override_cosmetics:
            enemy_setting = RandomModels[js.document.getElementById("random_enemy_colors").value]
        else:
            enemy_setting = settings.random_enemy_colors
        if enemy_setting != RandomModels.off:
            # Jumpman and DK
            jumpman_addresses = [
                0x8003B180,
                0x8003B3C8,
                0x8003B858,
                0x8003BAA0,
                0x8003BCE8,
                0x8003BF30,
                0x8003C178,
                0x8003C3C0,
                0x8003C608,
                0x8003C850,
                0x8003CA98,
                0x8003CCE0,
                0x8003B610,
                0x8003CF28,
                0x8003D170,
                0x8003D3B8,
                0x8003D600,
                0x8003D848,
                0x8003DA90,  # 8px version
            ]
            dk_addresses = [
                0x8003E9F0,
                0x800424D0,
                0x800463F0,
                0x800473B8,
                0x80048380,
                0x80049348,
                0x80040540,
                0x80041508,
                0x80043498,
                0x80044460,
                0x80045428,
            ]
            jumpman_shift = getRandomHueShift()  # 16x16 except for 1 image
            dk_shift = getRandomHueShift()  # 48x48
            for addr in jumpman_addresses:
                width = 16
                if addr == 0x8003DA90:
                    width = 8
                rom_addr = getROMAddress(addr, Overlay.Arcade, offset_dict)
                hueShiftImageFromAddress(ROM_COPY, rom_addr, width, width, TextureFormat.RGBA5551, jumpman_shift)
            for addr in dk_addresses:
                rom_addr = getROMAddress(addr, Overlay.Arcade, offset_dict)
                hueShiftImageFromAddress(ROM_COPY, rom_addr, 48, 41, TextureFormat.RGBA5551, dk_shift)


def isFasterCheckEnabled(spoiler, fast_check: FasterChecksSelected):
    """Determine if a faster check setting is enabled."""
    return IsItemSelected(spoiler.settings.faster_checks_enabled, spoiler.settings.faster_checks_selected, fast_check)


def isQoLEnabled(spoiler, misc_change: MiscChangesSelected):
    """Determine if a faster check setting is enabled."""
    return IsItemSelected(spoiler.settings.quality_of_life, spoiler.settings.misc_changes_selected, misc_change)


FLAG_ABILITY_CAMERA = 0x2FD


def expandSaveFile(ROM_COPY: LocalROM, static_expansion: int, actor_count: int, offset_dict: dict):
    """Expand Save file."""
    expansion = static_expansion + actor_count
    flag_block_size = 0x320 + expansion
    targ_gb_bits = 7  # Max 127
    GB_LEVEL_COUNT = 9 if ENABLE_HELM_GBS else 8
    added_bits = (targ_gb_bits - 3) * 8
    if ENABLE_HELM_GBS:
        added_bits += targ_gb_bits + 7 + 7
    kong_var_size = 0xA1 + added_bits
    file_info_location = flag_block_size + (5 * kong_var_size)
    file_default_size = file_info_location + 0x72
    # Flag Block Size
    writeValue(ROM_COPY, 0x8060E36A, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060E31E, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060E2C6, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D54A, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D4A2, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D45E, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D3C6, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D32E, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D23E, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060CF62, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060CC52, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060C78A, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060C352, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060BF96, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060BA7A, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060BEC6, Overlay.Static, file_info_location, offset_dict)
    # Increase GB Storage Size
    writeValue(ROM_COPY, 0x8060BE12, Overlay.Static, targ_gb_bits, offset_dict)  # Bit Size
    writeValue(ROM_COPY, 0x8060BE06, Overlay.Static, targ_gb_bits * GB_LEVEL_COUNT, offset_dict)  # Allocation for all levels
    writeValue(ROM_COPY, 0x8060BE26, Overlay.Static, 0x40C0, offset_dict)  # SLL 2 -> SLL 3
    writeValue(ROM_COPY, 0x8060BCC0, Overlay.Static, 0x24090000 | kong_var_size, offset_dict, 4)  # ADDIU $t1, $r0, kong_var_size
    writeValue(ROM_COPY, 0x8060BCC4, Overlay.Static, 0x01C90019, offset_dict, 4)  # MULTU $t1, $t6
    writeValue(ROM_COPY, 0x8060BCC8, Overlay.Static, 0x00004812, offset_dict, 4)  # MFLO $t1
    writeValue(ROM_COPY, 0x8060BCCC, Overlay.Static, 0, offset_dict, 4)  # NOP
    writeValue(ROM_COPY, 0x8060BE3A, Overlay.Static, 7 * GB_LEVEL_COUNT, offset_dict)
    writeValue(ROM_COPY, 0x8060BE6E, Overlay.Static, 7 * GB_LEVEL_COUNT, offset_dict)
    writeValue(ROM_COPY, 0x8060DFDE, Overlay.Static, GB_LEVEL_COUNT, offset_dict)
    writeValue(ROM_COPY, 0x8060DD42, Overlay.Static, GB_LEVEL_COUNT, offset_dict)
    writeValue(ROM_COPY, 0x806FB42E, Overlay.Static, int(math.ceil(GB_LEVEL_COUNT / 4) * 4), offset_dict)
    writeValue(ROM_COPY, 0x80029982, Overlay.Menu, int(math.ceil(GB_LEVEL_COUNT / 4) * 4), offset_dict)
    # Model 2 Start
    writeValue(ROM_COPY, 0x8060C2F2, Overlay.Static, flag_block_size, offset_dict)
    writeValue(ROM_COPY, 0x8060BCDE, Overlay.Static, flag_block_size, offset_dict)
    # Reallocate Balloons + Patches
    writeValue(ROM_COPY, 0x80688BCE, Overlay.Static, 0x320 + static_expansion, offset_dict)  # Reallocated to just before model 2 block


class MinigameImageLoader:
    """Class to store information regarding the image loader for an 8-bit minigame reward."""

    def __init__(
        self,
        file_name: str = None,
        table_index: int = 0,
        file_index: int = 0,
        width: int = 0,
        height: int = 0,
        tex_format: TextureFormat = TextureFormat.RGBA5551,
    ):
        """Initialize with given parameters."""
        self.pull_from_repo = file_name is not None
        if self.pull_from_repo:
            self.file_name = file_name
        else:
            self.table_index = table_index
            self.file_index = file_index
            self.width = width
            self.height = height
            self.tex_format = tex_format

    def getImageBytes(self, ROM_COPY: Union[LocalROM, ROM], sub_dir: str, targ_width: int, targ_height: int, output_format: TextureFormat, flip: bool = True) -> bytes:
        """Convert associated image to bytes that can be written to ROM."""
        output_image = None
        if self.pull_from_repo:
            output_image = Image.open(io.BytesIO(js.getFile(f"base-hack/assets/arcade_jetpac/{sub_dir}/{self.file_name}.png")))
        else:
            new_im = getImageFile(ROM_COPY, self.table_index, self.file_index, self.table_index != 7, self.width, self.height, self.tex_format)
            if self.width != self.height:
                dim = max(self.width, self.height)
                dx = int((dim - self.width) / 2)
                dy = int((dim - self.height) / 2)
                temp_im = Image.new(mode="RGBA", size=(dim, dim))
                temp_im.paste(new_im, (dx, dy), new_im)
                new_im = temp_im
            output_image = new_im.resize((targ_width, targ_height))
            if flip:
                output_image = output_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        if output_image is None:
            return None
        px = output_image.load()
        by_data = []
        for y in range(targ_height):
            for x in range(targ_width):
                px_data = px[x, y]
                if output_format == TextureFormat.RGBA5551:
                    # Arcade
                    val = 1 if px_data[3] > 128 else 0
                    for c in range(3):
                        local_channel = (px_data[c] >> 3) & 0x1F
                        shift = 1 + (5 * (2 - c))
                        val |= local_channel << shift
                    v0 = (val >> 8) & 0xFF
                    v1 = val & 0xFF
                    by_data.extend([v0, v1])
                elif output_format == TextureFormat.I8:
                    # Jetpac
                    total = 0
                    for c in range(3):
                        total += px_data[c]
                    intensity = int(total / 3)
                    by_data.append(intensity & 0xFF)
        return bytes(bytearray(by_data))


class Minigame8BitImage:
    """Class to store information regarding the image processing for an 8-bit minigame reward."""

    def __init__(self, permissable_items: list[Items], arcade_image: MinigameImageLoader, jetpac_image: MinigameImageLoader):
        """Initialize with given parameters."""
        self.permissable_items = permissable_items.copy()
        self.arcade_image = arcade_image
        self.jetpac_image = jetpac_image


def alter8bitRewardImages(ROM_COPY, offset_dict: dict, arcade_item: Items = Items.NintendoCoin, jetpac_item: Items = Items.RarewareCoin):
    """Alter the image that is displayed in DK Arcade/Jetpac for their respective rewards."""
    colorless_potions = (
        ItemPool.ImportantSharedMoves + ItemPool.JunkSharedMoves + ItemPool.TrainingBarrelAbilities() + ItemPool.ClimbingAbilities() + [Items.Shockwave, Items.Camera, Items.CameraAndShockwave]
    )
    # Image.open(f"{hash_dir}rw_coin.png").resize(dim).save(f"{arcade_dir}rwcoin.png")  # Rareware Coin
    # Image.open(f"{hash_dir}melon_slice.png").resize(dim).save(f"{arcade_dir}melon.png")  # Watermelon Slice
    db = [
        Minigame8BitImage([Items.Donkey], MinigameImageLoader("dk"), MinigameImageLoader("kong")),
        Minigame8BitImage([Items.Diddy], MinigameImageLoader("diddy"), MinigameImageLoader("kong")),
        Minigame8BitImage([Items.Lanky], MinigameImageLoader("lanky"), MinigameImageLoader("kong")),
        Minigame8BitImage([Items.Tiny], MinigameImageLoader("tiny"), MinigameImageLoader("kong")),
        Minigame8BitImage([Items.Chunky], MinigameImageLoader("chunky"), MinigameImageLoader("kong")),
        Minigame8BitImage([Items.Bean], MinigameImageLoader("bean"), MinigameImageLoader("bean")),
        Minigame8BitImage([Items.Pearl], MinigameImageLoader("pearl"), MinigameImageLoader("pearl")),
        Minigame8BitImage(ItemPool.DonkeyMoves, MinigameImageLoader("potion_dk"), MinigameImageLoader("potion")),
        Minigame8BitImage(ItemPool.DiddyMoves, MinigameImageLoader("potion_diddy"), MinigameImageLoader("potion")),
        Minigame8BitImage(ItemPool.LankyMoves, MinigameImageLoader("potion_lanky"), MinigameImageLoader("potion")),
        Minigame8BitImage(ItemPool.TinyMoves, MinigameImageLoader("potion_tiny"), MinigameImageLoader("potion")),
        Minigame8BitImage(ItemPool.ChunkyMoves, MinigameImageLoader("potion_chunky"), MinigameImageLoader("potion")),
        Minigame8BitImage(colorless_potions, MinigameImageLoader("potion_any"), MinigameImageLoader("potion")),
        Minigame8BitImage([Items.BattleCrown], MinigameImageLoader(None, 25, 5893, 44, 44), MinigameImageLoader("crown")),
        Minigame8BitImage(
            [Items.BananaFairy],
            MinigameImageLoader(None, 25, 0x16ED, 32, 32, TextureFormat.RGBA32),
            MinigameImageLoader("fairy"),
        ),
        Minigame8BitImage([Items.GoldenBanana], MinigameImageLoader(None, 25, 5468, 44, 44), MinigameImageLoader("gb")),
        Minigame8BitImage(ItemPool.Blueprints(), MinigameImageLoader(None, 25, 0x1593, 48, 42), MinigameImageLoader("blueprint")),
        Minigame8BitImage(ItemPool.Keys(), MinigameImageLoader(None, 25, 5877, 44, 44), MinigameImageLoader("key")),
        Minigame8BitImage([Items.BananaMedal], MinigameImageLoader(None, 25, 0x156C, 44, 44), MinigameImageLoader("medal")),
        Minigame8BitImage([Items.JunkMelon], MinigameImageLoader(None, 7, 0x142, 48, 42), MinigameImageLoader("melon")),
        Minigame8BitImage([Items.NintendoCoin], None, MinigameImageLoader("nintendo")),
        Minigame8BitImage([Items.RarewareCoin], MinigameImageLoader(None, 25, 5905, 44, 44), None),
        Minigame8BitImage([Items.RainbowCoin], MinigameImageLoader(None, 25, 5963, 48, 44), MinigameImageLoader("rainbow")),
        Minigame8BitImage(
            ItemPool.HintItems(),
            MinigameImageLoader(None, 25, 0x1775, 64, 64, TextureFormat.IA8),
            MinigameImageLoader("hint"),
        ),
        Minigame8BitImage([Items.ArchipelagoItem], MinigameImageLoader("ap"), MinigameImageLoader("ap")),
    ]
    arcade_image_data = None
    jetpac_image_data = None
    for item in db:
        if arcade_item in item.permissable_items:
            arcade_image_data = item.arcade_image
        if jetpac_item in item.permissable_items:
            jetpac_image_data = item.jetpac_image
    im_data = {
        "arcade": arcade_image_data,
        "jetpac": jetpac_image_data,
    }
    for minigame in im_data:
        if im_data[minigame] is None:
            continue
        dim = 20
        ovl = Overlay.Arcade
        addr = 0x8003AE58
        bytes_per_px = 2
        output_format = TextureFormat.RGBA5551
        if minigame == "jetpac":
            dim = 16
            ovl = Overlay.Jetpac
            addr = 0x8002D868
            bytes_per_px = 1
            output_format = TextureFormat.I8
        write = im_data[minigame].getImageBytes(ROM_COPY, minigame, dim, dim, output_format)
        output_addr = getROMAddress(addr, ovl, offset_dict)
        if len(write) > math.ceil(dim * dim * bytes_per_px):
            raise Exception(
                f"Cannot write 8-bit minigame image to ROM. Too big. Minigame: {minigame}, Arcade Item: {arcade_item}, Jetpac Item: {jetpac_item}, Size: {len(write)}, cap: {math.ceil(dim * dim * bytes_per_px)}"
            )
        ROM_COPY.seek(output_addr)
        ROM_COPY.writeBytes(write)


def writeActorHealth(ROM_COPY, actor_index: int, new_health: int):
    """Write actor health value."""
    start = getSym("actor_health_damage") + (4 * actor_index)
    writeValue(ROM_COPY, start, Overlay.Custom, new_health, {})


def updateActorFunctionInt(ROM_COPY, actor_index: int, new_function: int):
    """Update the actor function in the table based on a int value."""
    start = getSym("actor_functions") + (4 * actor_index)
    writeValue(ROM_COPY, start, Overlay.Custom, new_function, {}, 4)


def updateActorFunction(ROM_COPY, actor_index: int, new_function_sym: str):
    """Update the actor function in the table based on a sym value."""
    start = getSym("actor_functions") + (4 * actor_index)
    writeLabelValue(ROM_COPY, start, Overlay.Custom, new_function_sym, {})


def writeSingleOwnership(ROM_COPY, index, kong):
    """Write the ownership of a particular item to a kong."""
    start = getSym("new_flag_mapping") + (index * 8) + 6
    writeValue(ROM_COPY, start, Overlay.Custom, kong + 2, {}, 1)


def writeKongItemOwnership(ROM_COPY, settings: Settings):
    """Write the item ownership for kong rando."""
    starting_kong = settings.starting_kong
    diddy_freer = settings.diddy_freeing_kong
    lanky_freer = settings.lanky_freeing_kong
    tiny_freer = settings.tiny_freeing_kong
    chunky_freer = settings.chunky_freeing_kong
    no_arcade_r1 = IsItemSelected(settings.faster_checks_enabled, settings.faster_checks_selected, FasterChecksSelected.factory_arcade_round_1)
    writeSingleOwnership(ROM_COPY, 1, diddy_freer)
    writeSingleOwnership(ROM_COPY, 2, diddy_freer)
    writeSingleOwnership(ROM_COPY, 22, tiny_freer)
    writeSingleOwnership(ROM_COPY, 27, lanky_freer)
    writeSingleOwnership(ROM_COPY, 39, chunky_freer)
    writeSingleOwnership(ROM_COPY, 97, starting_kong)
    if no_arcade_r1:
        start = getSym("new_flag_mapping") + (41 * 8)
        writeValue(ROM_COPY, start, Overlay.Custom, Maps.FactoryBaboonBlast, {}, 1)
        writeValue(ROM_COPY, start + 2, Overlay.Custom, 0, {})


def disableDynamicReverb(ROM_COPY: ROM):
    """Disable the dynamic FXMix (Reverb) that would otherwise be applied in tunnels and underwater."""
    for index in range(1, 175):
        offset_dict = populateOverlayOffsets(ROM_COPY)
        ram_address = 0x80745658 + (index * 2)
        rom_address = getROMAddress(ram_address, Overlay.Static, offset_dict)
        ROM_COPY.seek(rom_address)
        original_value = int.from_bytes(ROM_COPY.readBytes(2), "big")
        original_value &= 0xFFFE
        writeValue(ROM_COPY, 0x80745658 + (index * 2), Overlay.Static, original_value, offset_dict)


boss_maps = [
    Maps.JapesBoss,
    Maps.AztecBoss,
    Maps.FactoryBoss,
    Maps.GalleonBoss,
    Maps.FungiBoss,
    Maps.CavesBoss,
    Maps.CastleBoss,
    Maps.KroolDonkeyPhase,
    Maps.KroolDiddyPhase,
    Maps.KroolLankyPhase,
    Maps.KroolTinyPhase,
    Maps.KroolChunkyPhase,
    Maps.KroolShoe,
]
k_rool_maps = [
    Maps.KroolDonkeyPhase,
    Maps.KroolDiddyPhase,
    Maps.KroolLankyPhase,
    Maps.KroolTinyPhase,
    Maps.KroolChunkyPhase,
]

IS_FINAL_BOSS_BIT = 0x200


def fixBossProperties(ROM_COPY: LocalROM, offset_dict: dict, settings: Settings):
    """Fix all boss map properties to account for the correct attributes."""
    # 02
    writeValue(ROM_COPY, 0x805FF476, Overlay.Static, IS_FINAL_BOSS_BIT, offset_dict)  # 805ff474 - Transition song playing (checks bit is not set)
    # 80618640 - SFX play from actor (checks bit is not set)
    # 806206fc - something with mini
    # 80621790 - rocket something
    # 80621888 - ????
    # 80621A30 - ????
    # 80621AC8 - ????
    # 80622248 - ????
    # 806223C4 - ????
    # 80624718 - ????
    # 806286DC - Warp actor to vehicle
    # 8067EA94 - Barrel code
    # 8067F3A4 - Play transform barrel song
    # 8067F7E8 - Transform cooldown
    # 80680200 - Cannon Barrel
    # 806802AC - Cannon Barrel
    # 80680434 - Cannon Barrel
    # 8068210C - Rocketbarrel HUD
    # 806C3008 - Cutscene Models
    # 806C308C - Cutscene Models
    # 806C7FD4 - Refilling health if dead (if not set)
    # 806D2EAC - Rocketbarrel something
    # 806D3164 - Rocketbarrel something
    # 806D7ABC - Play "knockout" sfx on death
    # 806D9A04 - Noclip for instrument
    # 806D9A7C - Trombone volume
    # 806E5430 - Noclip for instrument
    # 806EA0D8 - Zoom level
    # 806ECD24 - Jump Y Vel
    # 806ECDF8 - Damage take
    # 806EE804 - Cancel trombone music
    # 806EE83C - Damage take something
    # 806F058C - Play instrument cutscene
    # 806F12C8 - Play gone song
    writeValue(ROM_COPY, 0x8071288A, Overlay.Static, IS_FINAL_BOSS_BIT, offset_dict)  # 80712888 - Deathwarp location (should change this)
    # 80712C34 - Helm Timer init
    # 80712F34 - Warp after beating KR in main menu
    # 80726CDC - If off, and enemy id != 4 and actor_type != fairy, set props bitfield

    # 20
    # 8061bfb0 - Camera stuff
    writeHook(ROM_COPY, 0x806A895C, Overlay.Static, "checkKRoolPause", offset_dict)
    writeValue(ROM_COPY, 0x806A8970, Overlay.Static, 0x10200009, offset_dict, 4)  # beqz $at, 0x9

    for map_id in boss_maps:
        check_map = map_id
        if check_map == Maps.KroolShoe:
            check_map = Maps.KroolTinyPhase
        rom_address = getROMAddress(0x8074482C + (12 * map_id) + 4, Overlay.Static, offset_dict)
        ROM_COPY.seek(rom_address)
        raw_value = int.from_bytes(ROM_COPY.readBytes(4), "big")
        is_final_boss = check_map in settings.krool_order
        is_krool = check_map in k_rool_maps
        is_shoe = map_id == Maps.KroolShoe
        if is_final_boss:
            raw_value |= IS_FINAL_BOSS_BIT
        ROM_COPY.seek(rom_address)
        ROM_COPY.writeMultipleBytes(raw_value, 4)


def patchVersionStack(ROM_COPY: LocalROM, settings: Settings):
    """Patch the version number into the stack trace."""
    offset_dict = populateOverlayOffsets(ROM_COPY)
    VERSION_STRING_START = getSym("version_string")
    source_string = settings.branch.upper()[0]
    if source_string is None:
        source_string = "U"
    major = settings.version.split(".")[0]
    addr = getROMAddress(VERSION_STRING_START, Overlay.Custom, offset_dict)
    string_to_write = f"DK64R {major}.0{source_string}\n"
    if len(string_to_write) >= 0x10:
        raise Exception("Invalid stack trace string")
    ROM_COPY.seek(addr)
    ROM_COPY.writeBytes(bytes(string_to_write, "ascii"))


def patchAssembly(ROM_COPY, spoiler):
    """Patch all assembly instructions."""
    patchVersionStack(ROM_COPY, spoiler.settings)
    offset_dict = populateOverlayOffsets(ROM_COPY)
    settings = spoiler.settings
    file_init_flags = [
        0x167,  # FLAG_TNS_0,
        0x188,  # FLAG_TNS_1,
        0x311,  # FLAG_TNS_2,
        0x175,  # FLAG_BUY_INSTRUMENT,
        0x176,  # FLAG_BUY_GUNS,
        0x6D,  # FLAG_HATCH,
        0x00,  # FLAG_FIRSTJAPESGATE,
        0x17E,  # FLAG_FTT_BLOCKER,
        0x18C,  # FLAG_FIRST_COIN_COLLECTION
        0x164,  # BBlast first time cutscene
    ]

    ACTOR_DEF_START = getSym("actor_defs")
    ACTOR_MASTER_TYPE_START = getSym("actor_master_types")
    ACTOR_COLLISION_START = getSym("actor_collisions")
    ACTOR_HEALTH_START = getSym("actor_health_damage")

    alter8bitRewardImages(ROM_COPY, offset_dict, spoiler.arcade_item_reward, spoiler.jetpac_item_reward)
    fixBossProperties(ROM_COPY, offset_dict, settings)

    writeValue(ROM_COPY, 0x8060E04C, Overlay.Static, 0, offset_dict, 4)  # Prevent moves overwrite
    writeValue(ROM_COPY, 0x8060DDAA, Overlay.Static, 0, offset_dict)  # Writes readfile data to moves
    writeValue(ROM_COPY, 0x806C9CDE, Overlay.Static, 7, offset_dict)  # GiveEverything, write to bitfield. Seems to be unused but might as well
    writeValue(ROM_COPY, 0x8074DC84, Overlay.Static, 0x53, offset_dict)  # Increase PAAD size
    writeValue(ROM_COPY, 0x8060EEE0, Overlay.Static, 0x240E0000, offset_dict, 4)  # Disable Graphical Debugger. ADDIU $t6, $r0, 0
    writeValue(ROM_COPY, 0x806416BC, Overlay.Static, 0, offset_dict, 4)  # Prevent parent map check in cross-map object change communications
    writeValue(ROM_COPY, 0x806AF75C, Overlay.Static, 0x1000, offset_dict)  # New Kop Code
    writeValue(ROM_COPY, 0x806CBD78, Overlay.Static, 0x18400005, offset_dict, 4)  # BLEZ $v0, 0x5 - Decrease in health occurs if trap bubble active
    writeValue(ROM_COPY, 0x806A65B8, Overlay.Static, 0x240A0006, offset_dict, 4)  # Always ensure chunky bunch sprite (Rock Bunch)
    writeValue(ROM_COPY, 0x806A64B0, Overlay.Static, 0x240A0004, offset_dict, 4)  # Always ensure lanky coin sprite (Rabbit Race 1 Reward)
    writeValue(ROM_COPY, 0x8060036A, Overlay.Static, 0xFF, offset_dict)  # Fix game crash upon exiting a bonus with no parent
    writeValue(ROM_COPY, 0x806F88A8, Overlay.Static, 0x1000, offset_dict)  # Force disable coin cheat
    writeValue(ROM_COPY, 0x805FEA14, Overlay.Static, 0, offset_dict, 4)  # Prevent Enguarde arena setting kong as Enguarde
    writeValue(ROM_COPY, 0x805FEA08, Overlay.Static, 0, offset_dict, 4)  # Prevent Rambi arena setting kong as Rambi

    writeFunction(ROM_COPY, 0x805FC164, Overlay.Static, "cFuncLoop", offset_dict)  # Main Function Loop
    writeFunction(ROM_COPY, 0x8060CB7C, Overlay.Static, "fixChimpyCamBug", offset_dict)  # Fix bug with PJ
    writeFunction(ROM_COPY, 0x805FEBC0, Overlay.Static, "parseCutsceneData", offset_dict)  # modifyCutsceneHook
    writeFunction(ROM_COPY, 0x807313A4, Overlay.Static, "checkVictory_flaghook", offset_dict)  # perm flag set hook
    writeFunction(ROM_COPY, 0x806C3B5C, Overlay.Static, "mermaidCheck", offset_dict)  # Mermaid Check
    writeFunction(ROM_COPY, 0x806ADA70, Overlay.Static, "HandleSpiderSilkSpawn", offset_dict)  # Fix some silk memes

    if ENABLE_HITSCAN:
        writeFunction(ROM_COPY, 0x80694FAC, Overlay.Static, "movePelletWrapper", offset_dict)

    if DISABLE_BORDERS:
        writeValue(ROM_COPY, 0x805FBAB4, Overlay.Static, 0x1000FFC7, offset_dict, 4)  # Disable borders around game. Has "quirks"

    if UNSHROUDED_CASTLE:
        # Credit: Retroben
        writeFloatUpper(ROM_COPY, 0x80663CB6, Overlay.Static, 8000, offset_dict)

    if FARPLANE_VIEW:
        # Credit: Retroben
        writeValue(ROM_COPY, 0x80663D24, Overlay.Static, 0x240B1F40, offset_dict, 4)
        writeValue(ROM_COPY, 0x80663D30, Overlay.Static, 0x240B1F40, offset_dict, 4)
        writeValue(ROM_COPY, 0x8062F09C, Overlay.Static, 0x240F1F40, offset_dict, 4)

    # Kong Model Swap handlers
    writeFunction(ROM_COPY, 0x806C871C, Overlay.Static, "adjustGunBone", offset_dict)
    writeFunction(ROM_COPY, 0x806E2A34, Overlay.Static, "adjustGunBone", offset_dict)
    writeFunction(ROM_COPY, 0x80683194, Overlay.Static, "updateKongTB", offset_dict)
    writeFunction(ROM_COPY, 0x80031DE4, Overlay.Boss, "updateActorHandStates", offset_dict)
    writeFunction(ROM_COPY, 0x80031F68, Overlay.Boss, "updateActorHandStates", offset_dict)
    writeFunction(ROM_COPY, 0x80682FC4, Overlay.Static, "updateActorHandStates", offset_dict)
    writeFunction(ROM_COPY, 0x806839FC, Overlay.Static, "updateActorHandStates", offset_dict)
    writeFunction(ROM_COPY, 0x806BFC5C, Overlay.Static, "updateActorHandStates", offset_dict)
    writeFunction(ROM_COPY, 0x806C1A50, Overlay.Static, "updateActorHandStates", offset_dict)
    writeFunction(ROM_COPY, 0x806C1B8C, Overlay.Static, "updateActorHandStates", offset_dict)
    writeFunction(ROM_COPY, 0x806C1D4C, Overlay.Static, "updateActorHandStates", offset_dict)
    writeFunction(ROM_COPY, 0x806C88CC, Overlay.Static, "updateActorHandStates", offset_dict)
    writeFunction(ROM_COPY, 0x80029F78, Overlay.Bonus, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x8002CBD4, Overlay.Menu, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x80026904, Overlay.Multiplayer, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x8062806C, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x8068F128, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806BFB64, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806C10D8, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806C2FA0, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806E2A1C, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806EAC54, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806EC060, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806ED12C, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806EDE60, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806F114C, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806F11D4, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806F11F0, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806F120C, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806F1228, Overlay.Static, "clearGunHandler", offset_dict)
    writeLabelValue(ROM_COPY, 0x80746D8C, Overlay.Static, "clearGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806BFB40, Overlay.Static, "pullOutGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806C8C54, Overlay.Static, "pullOutGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806EAC44, Overlay.Static, "pullOutGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806EB850, Overlay.Static, "pullOutGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806EDE24, Overlay.Static, "pullOutGunHandler", offset_dict)
    writeFunction(ROM_COPY, 0x806F77EC, Overlay.Static, "pullOutGunHandler", offset_dict)
    writeLabelValue(ROM_COPY, 0x80746D90, Overlay.Static, "pullOutGunHandler", offset_dict)

    writeHook(ROM_COPY, 0x8063EE08, Overlay.Static, "InstanceScriptCheck", offset_dict)
    writeHook(ROM_COPY, 0x80731168, Overlay.Static, "checkFlag_ItemRando", offset_dict)
    writeHook(ROM_COPY, 0x807312F8, Overlay.Static, "setFlag_ItemRando", offset_dict)
    writeHook(ROM_COPY, 0x8069840C, Overlay.Static, "VineCode", offset_dict)
    writeHook(ROM_COPY, 0x80698420, Overlay.Static, "VineShowCode", offset_dict)
    writeHook(ROM_COPY, 0x8063ED7C, Overlay.Static, "HandleSlamCheck", offset_dict)
    writeHook(ROM_COPY, 0x806FF384, Overlay.Static, "ModifyCameraColor", offset_dict)
    writeHook(ROM_COPY, 0x8061E684, Overlay.Static, "SkipCutscenePans", offset_dict)
    writeHook(ROM_COPY, 0x80648364, Overlay.Static, "ShopImageHandler", offset_dict)
    writeHook(ROM_COPY, 0x806EA70C, Overlay.Static, "InvertCameraControls", offset_dict)
    writeHook(ROM_COPY, 0x8061CE38, Overlay.Static, "PlayCutsceneVelocity", offset_dict)
    writeHook(ROM_COPY, 0x80677C14, Overlay.Static, "FixPufftossInvalidWallCollision", offset_dict)
    writeHook(ROM_COPY, 0x8060DFF4, Overlay.Static, "SaveToFileFixes", offset_dict)
    writeHook(ROM_COPY, 0x806F6EA0, Overlay.Static, "BarrelMovesFixes", offset_dict)
    writeHook(ROM_COPY, 0x806E4930, Overlay.Static, "ChimpyChargeFix", offset_dict)
    writeHook(ROM_COPY, 0x806E48AC, Overlay.Static, "OStandFix", offset_dict)
    writeHook(ROM_COPY, 0x8067ECB8, Overlay.Static, "HunkyChunkyFix2", offset_dict)
    writeHook(ROM_COPY, 0x805FC3FC, Overlay.Static, "EarlyFrameCode", offset_dict)
    writeHook(ROM_COPY, 0x8071417C, Overlay.Static, "displayListCode", offset_dict)
    writeHook(ROM_COPY, 0x806F8610, Overlay.Static, "GiveItemPointerToMulti", offset_dict)
    writeHook(ROM_COPY, 0x8060005C, Overlay.Static, "getLobbyExit", offset_dict)
    writeHook(ROM_COPY, 0x8060DEF4, Overlay.Static, "SaveHelmHurryCheck", offset_dict)
    writeHook(ROM_COPY, 0x806F3E74, Overlay.Static, "AutowalkFix", offset_dict)
    writeHook(ROM_COPY, 0x80610948, Overlay.Static, "DynamicCodeFixes", offset_dict)
    writeHook(ROM_COPY, 0x80689534, Overlay.Static, "tagPreventCode", offset_dict)
    writeHook(ROM_COPY, 0x806BD328, Overlay.Static, "KeyCompressionCode", offset_dict)
    writeHook(ROM_COPY, 0x8067B684, Overlay.Static, "CannonForceCode", offset_dict)
    writeHook(ROM_COPY, 0x806F9F88, Overlay.Static, "HUDDisplayCode", offset_dict)
    writeHook(ROM_COPY, 0x806E22B0, Overlay.Static, "HomingDisable", offset_dict)
    writeHook(ROM_COPY, 0x806EB574, Overlay.Static, "HomingHUDHandle", offset_dict)
    writeHook(ROM_COPY, 0x806324C4, Overlay.Static, "DKCollectableFix", offset_dict)
    writeHook(ROM_COPY, 0x806AF70C, Overlay.Static, "GuardDeathHandle", offset_dict)
    writeHook(ROM_COPY, 0x806AE55C, Overlay.Static, "GuardAutoclear", offset_dict)
    writeHook(ROM_COPY, 0x80637148, Overlay.Static, "ObjectRotate", offset_dict)
    writeHook(ROM_COPY, 0x8063365C, Overlay.Static, "WriteDefaultShopBone", offset_dict)
    writeHook(ROM_COPY, 0x806A86FC, Overlay.Static, "PauseControl_Control", offset_dict)
    writeHook(ROM_COPY, 0x806AA414, Overlay.Static, "PauseControl_Sprite", offset_dict)
    writeHook(ROM_COPY, 0x806A7474, Overlay.Static, "disableHelmKeyBounce", offset_dict)
    writeHook(ROM_COPY, 0x80600674, Overlay.Static, "updateLag", offset_dict)
    writeHook(ROM_COPY, 0x806FC990, Overlay.Static, "ApplyTextRecolorHints", offset_dict)

    if CAMERA_RESET_REDUCTION:
        # Credit: Retroben
        writeValue(ROM_COPY, 0x8061BDF0, Overlay.Static, 0x1000, offset_dict)
        writeValue(ROM_COPY, 0x8061BE12, Overlay.Static, 0x0001, offset_dict)
        writeValue(ROM_COPY, 0x8061BE18, Overlay.Static, 0x1000, offset_dict)

    if PAL_DOGADON_REMATCH_FIRE:
        writeValue(ROM_COPY, 0x80691E36, Overlay.Static, 166, offset_dict)  # PAL = 200 * (50 / 60)

    if REMOVE_CS_BARS:
        writeValue(ROM_COPY, 0x805FBC2C, Overlay.Static, 0x0060C825, offset_dict, 4)  # Remove screen divisor capping
        writeValue(ROM_COPY, 0x805FBC38, Overlay.Static, 0x00A04025, offset_dict, 4)  # Remove screen divisor capping

    # Boss stuff
    writeHook(ROM_COPY, 0x80028CCC, Overlay.Boss, "KRoolLankyPhaseFix", offset_dict)
    if IsItemSelected(settings.hard_bosses, settings.hard_bosses_selected, HardBossesSelected.kut_out_phase_rando, False):
        writeHook(ROM_COPY, 0x80032570, Overlay.Boss, "KKOPhaseHandler", offset_dict)
        writeHook(ROM_COPY, 0x80031B2C, Overlay.Boss, "KKOInitPhase", offset_dict)
        writeValue(ROM_COPY, 0x8003259A, Overlay.Boss, 4, offset_dict, 2)  # KKO Last Phase Check
        writeValue(ROM_COPY, 0x80032566, Overlay.Boss, settings.kko_phase_order[1], offset_dict, 2)  # KKO Last Phase Check
    if settings.shorten_boss:
        writeActorHealth(ROM_COPY, 185, 3)  # Dillo Health 4 -> 3
        writeActorHealth(ROM_COPY, 236, int(3 + (62 * (2 / 3))))  # Dogadon Health 65 -> 44
        writeActorHealth(ROM_COPY, 251, 3)  # Spider Boss Health 6 -> 3
        writeHook(ROM_COPY, 0x80035120, Overlay.Boss, "MadJackShort", offset_dict)
        writeValue(ROM_COPY, 0x800350D2, Overlay.Boss, 2, offset_dict, 2)  # Mad Jack Cutscene Memery
        writeHook(ROM_COPY, 0x80029AAC, Overlay.Boss, "PufftossShort", offset_dict)
        writeHook(ROM_COPY, 0x8002ACB0, Overlay.Boss, "DogadonRematchShort", offset_dict)
        writeHook(ROM_COPY, 0x800257CC, Overlay.Boss, "DilloRematchShort", offset_dict)
        writeValue(ROM_COPY, 0x800322BA, Overlay.Boss, 2, offset_dict, 2)  # Kut Out hit limit
        writeHook(ROM_COPY, 0x8002DB10, Overlay.Boss, "DKPhaseShort", offset_dict)
        writeValue(ROM_COPY, 0x8002E52A, Overlay.Boss, 2, offset_dict, 2)  # Diddy Phase Hit Count
        writeValue(ROM_COPY, 0x8002EF02, Overlay.Boss, 2, offset_dict, 2)  # Lanky Phase Hit Count
        writeHook(ROM_COPY, 0x80030370, Overlay.Boss, "TinyPhaseShort", offset_dict)
        writeHook(ROM_COPY, 0x800314B4, Overlay.Boss, "ChunkyPhaseShort", offset_dict)
    writeValue(ROM_COPY, 0x80031378, Overlay.Boss, 0x0C1837B2, offset_dict, 4)  # Call save

    # Change pause menu background design
    writeValue(ROM_COPY, 0x806A84F4, Overlay.Static, 0, offset_dict, 4)  # Enable framebuffer clear on pause menu
    writeValue(ROM_COPY, 0x806A90E8, Overlay.Static, 0, offset_dict, 4)  # Disable Screen Shake
    writeValue(ROM_COPY, 0x806AC056, Overlay.Static, 120, offset_dict)  # Changes darkness opacity

    # Beaver Bother fix
    writeHook(ROM_COPY, 0x806AD740, Overlay.Static, "unscareBeaver", offset_dict)
    writeHook(ROM_COPY, 0x806AD728, Overlay.Static, "scareBeaver", offset_dict)
    writeValue(ROM_COPY, 0x806B674E, Overlay.Static, 0xC, offset_dict)  # Increase the scare duration

    # T&S Div-by-0 error
    writeHook(ROM_COPY, 0x8064D8E0, Overlay.Static, "tns_pad_height_patch", offset_dict)
    writeHook(ROM_COPY, 0x8064D9D8, Overlay.Static, "tns_pad_height_patch_0", offset_dict)
    writeHook(ROM_COPY, 0x806BE0FC, Overlay.Static, "scoff_patch", offset_dict)
    for index, count in enumerate(settings.BossBananas):
        writeValue(ROM_COPY, 0x807446C0 + (2 * index), Overlay.Static, count, offset_dict)

    # Make chunky translucent during the HC section of Chunky Phase
    writeHook(ROM_COPY, 0x806CB778, Overlay.Static, "makeKongTranslucent", offset_dict)

    writeFunction(ROM_COPY, 0x80704568, Overlay.Static, "spawnOverlayText", offset_dict)

    writeValue(ROM_COPY, 0x807563B4, Overlay.Static, 1, offset_dict, 1)  # Enable stack trace

    writeFunction(ROM_COPY, 0x806DF3F8, Overlay.Static, "getHomingCountWithAbilityCheck", offset_dict)
    writeFunction(ROM_COPY, 0x806EB560, Overlay.Static, "getHomingCountWithAbilityCheck", offset_dict)
    writeValue(ROM_COPY, 0x806F90C8, Overlay.Static, 0x24040000 | (20 * 150), offset_dict, 4)  # set min coconuts to 3000 (20 crystals)

    # Damage mask
    damage_addrs = [0x806EE138, 0x806EE330, 0x806EE480, 0x806EEA20, 0x806EEEA4, 0x806EF910, 0x806EF9D0, 0x806F5860]
    for addr in damage_addrs:
        writeFunction(ROM_COPY, addr, Overlay.Static, "applyDamageMask", offset_dict)
    writeFunction(ROM_COPY, 0x80031524, Overlay.Boss, "applyDamageMask", offset_dict)

    writeFunction(ROM_COPY, 0x806D2FC0, Overlay.Static, "fixRBSlowTurn", offset_dict)  # Slow Turn Fix
    writeFunction(ROM_COPY, 0x80712EC4, Overlay.Static, "postKRoolSaveCheck", offset_dict)  # LZ Save
    writeFunction(ROM_COPY, 0x806380B0, Overlay.Static, "handleModelTwoOpacity", offset_dict)  # Opacity Fixes

    # Level Index Fixes
    for map_index in (Maps.OrangeBarrel, Maps.BarrelBarrel, Maps.VineBarrel, Maps.DiveBarrel):
        writeValue(ROM_COPY, 0x807445E0 + map_index, Overlay.Static, 9, offset_dict, 1)  # Write Training level index to LEVEL_BONUS
    # Mermaid
    writeValue(ROM_COPY, 0x806C3B64, Overlay.Static, 0x1000, offset_dict)  # Force to branch
    writeValue(ROM_COPY, 0x806C3BD0, Overlay.Static, 0x1000, offset_dict)  # Force to branch
    writeValue(ROM_COPY, 0x806C3C20, Overlay.Static, 0, offset_dict, 4)  # NOP - Cancel control state write
    writeValue(ROM_COPY, 0x806C3C2C, Overlay.Static, 0, offset_dict, 4)  # NOP - Cancel control state progress write
    # Silk Memes
    writeValue(ROM_COPY, 0x806ADA6C, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x806ADA78, Overlay.Static, 0, offset_dict, 4)
    # Fix Spider Crashes
    writeValue(ROM_COPY, 0x8075F46C, Overlay.Static, 0x2F5, offset_dict)
    writeValue(ROM_COPY, 0x806ADA26, Overlay.Static, 0x2F5, offset_dict)  # This might fix spawning if set on non-init
    writeValue(ROM_COPY, 0x806ADA2A, Overlay.Static, 0x2F5, offset_dict)
    writeValue(ROM_COPY, 0x806ADA32, Overlay.Static, 0x2F5, offset_dict)
    writeValue(ROM_COPY, 0x806ADBC6, Overlay.Static, 0x2F5, offset_dict)
    writeValue(ROM_COPY, 0x806ADC66, Overlay.Static, 0x2F5, offset_dict)
    writeValue(ROM_COPY, 0x806ADD3A, Overlay.Static, 0x2F5, offset_dict)
    # Decouple Camera from Shockwave
    writeValue(ROM_COPY, 0x806E9812, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Usage
    writeValue(ROM_COPY, 0x806AB0F6, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Isles Fairies Display
    writeValue(ROM_COPY, 0x806AAFB6, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Other Fairies Display
    writeValue(ROM_COPY, 0x806AA762, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Film Display
    writeValue(ROM_COPY, 0x8060D986, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Film Refill
    writeValue(ROM_COPY, 0x806F6F76, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Film Refill
    writeValue(ROM_COPY, 0x806F916A, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Film max#
    if settings.bonus_barrel_rando:
        # Disable training pre-checks
        writeValue(ROM_COPY, 0x80698386, Overlay.Static, 0, offset_dict)  # Disable ability to use vines in vine barrel unless you have vines
        writeValue(ROM_COPY, 0x806E426C, Overlay.Static, 0, offset_dict, 4)  # Disable ability to pick up objects in barrel barrel unless you have barrels
        writeValue(ROM_COPY, 0x806E7736, Overlay.Static, 0, offset_dict)  # Disable ability to dive in dive barrel unless you have dive
        writeValue(ROM_COPY, 0x806E2D8A, Overlay.Static, 0, offset_dict)  # Disable ability to throw oranges in orange barrel unless you have oranges
    writeFunction(ROM_COPY, 0x80698368, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Vines doesn't check FLUT
    writeFunction(ROM_COPY, 0x8072F190, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Vines doesn't check FLUT
    writeFunction(ROM_COPY, 0x806E4250, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Barrels doesn't check FLUT
    writeFunction(ROM_COPY, 0x806E7718, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Dive doesn't check FLUT
    writeFunction(ROM_COPY, 0x806E2D6C, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Oranges doesn't check FLUT
    # Files
    balloon_patch_count = 150
    static_expansion = 0x100
    if settings.enemy_drop_rando:
        static_expansion += 427  # Total Enemies
    if settings.archipelago:
        static_expansion += 1000  # Archipelago Flag size
    expandSaveFile(ROM_COPY, static_expansion, balloon_patch_count, offset_dict)
    # 1-File Fixes
    writeValue(ROM_COPY, 0x8060CF34, Overlay.Static, 0x240E0001, offset_dict, 4)  # Slot 1
    writeValue(ROM_COPY, 0x8060CF38, Overlay.Static, 0x240F0002, offset_dict, 4)  # Slot 2
    writeValue(ROM_COPY, 0x8060CF3C, Overlay.Static, 0x24180003, offset_dict, 4)  # Slot 3
    writeValue(ROM_COPY, 0x8060CF40, Overlay.Static, 0x240D0000, offset_dict, 4)  # Slot 0
    writeValue(ROM_COPY, 0x8060D3AC, Overlay.Static, 0, offset_dict, 4)  # Prevent EEPROM Shuffle
    writeValue(ROM_COPY, 0x8060DCE8, Overlay.Static, 0, offset_dict, 4)  # Prevent EEPROM Shuffle
    writeValue(ROM_COPY, 0x8060CD1A, Overlay.Static, 1, offset_dict)  # File Loop Cancel 2
    writeValue(ROM_COPY, 0x8060CE7E, Overlay.Static, 1, offset_dict)  # File Loop Cancel 3
    writeValue(ROM_COPY, 0x8060CE5A, Overlay.Static, 1, offset_dict)  # File Loop Cancel 4
    writeValue(ROM_COPY, 0x8060CF0E, Overlay.Static, 1, offset_dict)  # File Loop Cancel 5
    writeValue(ROM_COPY, 0x8060CF26, Overlay.Static, 1, offset_dict)  # File Loop Cancel 6
    writeValue(ROM_COPY, 0x8060D106, Overlay.Static, 1, offset_dict)  # File Loop Cancel 8
    writeValue(ROM_COPY, 0x8060D43E, Overlay.Static, 1, offset_dict)  # File Loop Cancel 8
    writeValue(ROM_COPY, 0x8060CD08, Overlay.Static, 0x26670000, offset_dict, 4)  # Save to File - File Index
    writeValue(ROM_COPY, 0x8060CE48, Overlay.Static, 0x26670000, offset_dict, 4)  # Save to File - File Index
    writeValue(ROM_COPY, 0x8060CF04, Overlay.Static, 0x26270000, offset_dict, 4)  # Save to File - File Index
    writeValue(ROM_COPY, 0x8060BFA4, Overlay.Static, 0x252A0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060E378, Overlay.Static, 0x258D0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D33C, Overlay.Static, 0x254B0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D470, Overlay.Static, 0x256C0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D4B0, Overlay.Static, 0x252A0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D558, Overlay.Static, 0x258D0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060CF74, Overlay.Static, 0x25090000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D24C, Overlay.Static, 0x25AE0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060C84C, Overlay.Static, 0xA02067C8, offset_dict, 4)  # Force file 0
    writeValue(ROM_COPY, 0x8060C654, Overlay.Static, 0x24040000, offset_dict, 4)  # Force file 0 - Save
    writeValue(ROM_COPY, 0x8060C664, Overlay.Static, 0xAFA00034, offset_dict, 4)  # Force file 0 - Save
    writeValue(ROM_COPY, 0x8060C6C4, Overlay.Static, 0x24040000, offset_dict, 4)  # Force file 0 - Read
    writeValue(ROM_COPY, 0x8060C6D4, Overlay.Static, 0xAFA00034, offset_dict, 4)  # Force file 0 - Read
    writeValue(ROM_COPY, 0x8060D294, Overlay.Static, 0, offset_dict, 4)  # Cartridge EEPROM Wipe cancel
    # File Select
    writeValue(ROM_COPY, 0x80028CB0, Overlay.Menu, 0xA0600000, offset_dict, 4)  # SB $r0, 0x0 (v0) - Always view file index 0
    writeValue(ROM_COPY, 0x80028CC4, Overlay.Menu, 0, offset_dict, 4)  # Prevent file index overwrite
    writeValue(ROM_COPY, 0x80028F88, Overlay.Menu, 0, offset_dict, 4)  # File 2 render
    writeValue(ROM_COPY, 0x80028F60, Overlay.Menu, 0, offset_dict, 4)  # File 2 Opacity
    writeValue(ROM_COPY, 0x80028FCC, Overlay.Menu, 0, offset_dict, 4)  # File 3 render
    writeValue(ROM_COPY, 0x80028FA4, Overlay.Menu, 0, offset_dict, 4)  # File 3 Opacity
    writeValue(ROM_COPY, 0x80028DB8, Overlay.Menu, 0x1040000A, offset_dict, 4)  # BEQ $v0, $r0, 0xA - Change text signal
    writeValue(ROM_COPY, 0x80028CA6, Overlay.Menu, 5, offset_dict)  # Change selecting orange to delete confirm screen

    # Move Decoupling
    # Strong Kong
    writeValue(ROM_COPY, 0x8067ECFC, Overlay.Static, 0x30810002, offset_dict, 4)  # ANDI $at $a0 2
    writeValue(ROM_COPY, 0x8067ED00, Overlay.Static, 0x50200003, offset_dict, 4)  # BEQL $at $r0 3
    # Rocketbarrel
    writeValue(ROM_COPY, 0x80682024, Overlay.Static, 0x31810002, offset_dict, 4)  # ANDI $at $t4 2
    writeValue(ROM_COPY, 0x80682028, Overlay.Static, 0x50200006, offset_dict, 4)  # BEQL $at $r0 0x6
    # OSprint
    writeValue(ROM_COPY, 0x8067ECE0, Overlay.Static, 0x30810004, offset_dict, 4)  # ANDI $at $a0 4
    writeValue(ROM_COPY, 0x8067ECE4, Overlay.Static, 0x10200002, offset_dict, 4)  # BEQZ $at, 2
    # Mini Monkey
    writeValue(ROM_COPY, 0x8067EC80, Overlay.Static, 0x30830001, offset_dict, 4)  # ANDI $v1 $a0 1
    writeValue(ROM_COPY, 0x8067EC84, Overlay.Static, 0x18600002, offset_dict, 4)  # BLEZ $v1 2
    # Hunky Chunky (Not Dogadon)
    writeValue(ROM_COPY, 0x8067ECA0, Overlay.Static, 0x30810001, offset_dict, 4)  # ANDI $at $a0 1
    writeValue(ROM_COPY, 0x8067ECA4, Overlay.Static, 0x18200002, offset_dict, 4)  # BLEZ $at 2
    # PTT
    writeValue(ROM_COPY, 0x806E20F0, Overlay.Static, 0x31010002, offset_dict, 4)  # ANDI $at $t0 2
    writeValue(ROM_COPY, 0x806E20F4, Overlay.Static, 0x5020000F, offset_dict, 4)  # BEQL $at $r0 0xF
    # PPunch
    writeValue(ROM_COPY, 0x806E48F4, Overlay.Static, 0x31810002, offset_dict, 4)  # ANDI $at $t4 2
    writeValue(ROM_COPY, 0x806E48F8, Overlay.Static, 0x50200074, offset_dict, 4)  # BEQL $at $r0 0xF

    # Disable Sniper Scope Overlay
    writeValue(ROM_COPY, 0x806FF80C, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FF85C, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FF8AC, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FF8FC, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FF940, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FF988, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FF9D0, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0
    writeValue(ROM_COPY, 0x806FFA18, Overlay.Static, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $r0

    writeValue(ROM_COPY, 0x806A7564, Overlay.Static, 0xC4440080, offset_dict, 4)  # Crown default floor will be it's initial Y spawn position. Fixes a crash on N64

    # Expand Display List
    writeValue(ROM_COPY, 0x805FE56A, Overlay.Static, 8000, offset_dict)
    writeValue(ROM_COPY, 0x805FE592, Overlay.Static, 0x4100, offset_dict)  # SLL 4 (Doubles display list size)
    # Sniper Scope Check
    writeValue(ROM_COPY, 0x806D2988, Overlay.Static, 0x93190002, offset_dict, 4)  # LBU $t9, 0x2 ($t8)
    writeValue(ROM_COPY, 0x806D2990, Overlay.Static, 0x33210004, offset_dict, 4)  # ANDI $at, $t9, 0x4
    writeValue(ROM_COPY, 0x806D299C, Overlay.Static, 0x1020, offset_dict)  # BEQ $at, $r0
    # EEPROM Patch
    writeValue(ROM_COPY, 0x8060D588, Overlay.Static, 0, offset_dict, 4)  # NOP
    # TEMPORARY FIX FOR SAVE BUG
    writeValue(ROM_COPY, 0x8060D790, Overlay.Static, 0, offset_dict, 4)  # NOP
    # Cancel Tamper
    writeValue(ROM_COPY, 0x8060AEFC, Overlay.Static, 0, offset_dict, 4)  # NOP
    writeValue(ROM_COPY, 0x80611788, Overlay.Static, 0, offset_dict, 4)  # NOP
    # Fix HUD if DK not free
    writeValue(ROM_COPY, 0x806FA324, Overlay.Static, 0, offset_dict, 4)  # NOP
    writeValue(ROM_COPY, 0x807505AE, Overlay.Static, 385, offset_dict)  # Set Flag to DK Flag
    # Fix CB Spawning
    writeValue(ROM_COPY, 0x806A7882, Overlay.Static, 385, offset_dict)  # DK Balloon
    # Fix Boss Doors if DK not free
    writeValue(ROM_COPY, 0x80649358, Overlay.Static, 0, offset_dict, 4)  # NOP
    # Fix Pause Menu
    writeValue(ROM_COPY, 0x806ABFF8, Overlay.Static, 0, offset_dict, 4)  # NOP (Write of first slot to 1)
    writeValue(ROM_COPY, 0x806AC002, Overlay.Static, 0x530, offset_dict)
    writeValue(ROM_COPY, 0x806AC006, Overlay.Static, 0x5B0, offset_dict)
    writeValue(ROM_COPY, 0x8075054D, Overlay.Static, 0xD7, offset_dict, 1)  # Change DK Q Mark to #FFD700
    if ENABLE_HELM_GBS:
        writeValue(ROM_COPY, 0x806A9C80, Overlay.Static, 0, offset_dict, 4)  # Level check NOP
        writeValue(ROM_COPY, 0x806A9E54, Overlay.Static, 0, offset_dict, 4)  # Level check NOP
    # Kop Idle Guarantee
    writeFunction(ROM_COPY, 0x806AF7F8, Overlay.Static, "setKopIdleGuarantee", offset_dict)
    writeFunction(ROM_COPY, 0x806AF89C, Overlay.Static, "giveKopIdleGuarantee", offset_dict)
    # Guard Animation Fix
    writeValue(ROM_COPY, 0x806AF8C6, Overlay.Static, 0x2C1, offset_dict)
    # Remove flare effect from guards
    writeValue(ROM_COPY, 0x806AE440, Overlay.Static, 0, offset_dict, 4)
    # Boost Diddy/Tiny's Barrel Speed
    writeFloat(ROM_COPY, 0x807533A0, Overlay.Static, 240, offset_dict)  # Diddy Ground
    writeFloat(ROM_COPY, 0x807533A8, Overlay.Static, 240, offset_dict)  # Tiny Ground
    writeFloat(ROM_COPY, 0x807533DC, Overlay.Static, 260, offset_dict)  # Lanky Air
    writeFloat(ROM_COPY, 0x807533E0, Overlay.Static, 260, offset_dict)  # Tiny Air
    # Bump Model Two Allowance
    writeValue(ROM_COPY, 0x80632026, Overlay.Static, 550, offset_dict)  # Japes
    writeValue(ROM_COPY, 0x80632006, Overlay.Static, 550, offset_dict)  # Aztec
    writeValue(ROM_COPY, 0x80631FF6, Overlay.Static, 550, offset_dict)  # Factory
    writeValue(ROM_COPY, 0x80632016, Overlay.Static, 550, offset_dict)  # Galleon
    writeValue(ROM_COPY, 0x80631FE6, Overlay.Static, 550, offset_dict)  # Fungi
    writeValue(ROM_COPY, 0x80632036, Overlay.Static, 550, offset_dict)  # Others

    writeFunction(ROM_COPY, 0x80732314, Overlay.Static, "CrashHandler", offset_dict)
    writeFunction(ROM_COPY, 0x8073231C, Overlay.Static, "CrashHandler", offset_dict)
    writeFunction(ROM_COPY, 0x807322DC, Overlay.Static, "getFaultedThread", offset_dict)
    # Deathwarp Handle
    writeFunction(ROM_COPY, 0x8071292C, Overlay.Static, "WarpHandle", offset_dict)  # Check if in Helm, in which case, apply transition
    writeFunction(ROM_COPY, 0x806AD750, Overlay.Static, "beaverExtraHitHandle", offset_dict)  # Remove buff until we think of something better

    if ENABLE_ALL_KONG_TRANSFORMS:
        transform_barrel_collisions = [
            0x8074B190,  # Hunky
            0x8074B1A0,  # Mini
            0x8074B1B0,  # Rocket
            0x8074B1C0,  # OSprint
            0x8074B1D0,  # Strong Kong
        ]
        for col in transform_barrel_collisions:
            writeValue(ROM_COPY, col, Overlay.Static, 0xFFFF, offset_dict)  # Set these barrels to check collisions with all kongs
        writeValue(ROM_COPY, 0x8067EC58, Overlay.Static, 0x8CE20058, offset_dict, 4)  # Move actor check earlier on
        writeValue(ROM_COPY, 0x8067EC5C, Overlay.Static, 0x2C460007, offset_dict, 4)  # SLTIU a2, v0, 0x7
        writeValue(ROM_COPY, 0x8067EC60, Overlay.Static, 0x2C410007, offset_dict, 4)  # SLTIU at, v0, 0x7
        writeValue(ROM_COPY, 0x8067EC64, Overlay.Static, 0x2C4A0007, offset_dict, 4)  # SLTIU t2, v0, 0x7
        writeValue(ROM_COPY, 0x8067ECBC, Overlay.Static, 0x2C410007, offset_dict, 4)  # SLTIU at, v0, 0x7
        writeValue(ROM_COPY, 0x8067ECC4, Overlay.Static, 0x2C410007, offset_dict, 4)  # SLTIU at, v0, 0x7
        writeValue(ROM_COPY, 0x8067ECCC, Overlay.Static, 0x2C410007, offset_dict, 4)  # SLTIU at, v0, 0x7
        writeValue(ROM_COPY, 0x8067EC6C, Overlay.Static, 0x10200008, offset_dict, 4)  # BEQZ at, 8 (mini)
        writeValue(ROM_COPY, 0x8067EC90, Overlay.Static, 0x10C00007, offset_dict, 4)  # BEQZ a2, 7 (hunky)
        writeValue(ROM_COPY, 0x8067ECB0, Overlay.Static, 0x10C00006, offset_dict, 4)  # BEQZ a2, 6 (hunky)
        writeValue(ROM_COPY, 0x8067ECD0, Overlay.Static, 0x10C00007, offset_dict, 4)  # BEQZ a2, 7 (sprint)
        writeValue(ROM_COPY, 0x8067ECF0, Overlay.Static, 0x11400006, offset_dict, 4)  # BEQZ t2, 6 (strong)
        writeValue(ROM_COPY, 0x8067ED0C, Overlay.Static, 0x2C410007, offset_dict, 4)  # SLTIU at, v0, 0x7
        writeValue(ROM_COPY, 0x8067ECF0, Overlay.Static, 0x50200005, offset_dict, 4)  # BEQZL at, 5 (enguarde)
        writeValue(ROM_COPY, 0x80682008, Overlay.Static, 0x8D4B0058, offset_dict, 4)  # Move actor check for RB earlier on
        writeValue(ROM_COPY, 0x80682010, Overlay.Static, 0x2D610007, offset_dict, 4)  # SLTIU at, t3, 0x7
        writeValue(ROM_COPY, 0x80682014, Overlay.Static, 0x5020000B, offset_dict, 4)  # BEQZL at, 0xB (RB)

    if settings.cannons_require_blast:
        # Make Cannon Barrels require BBlast
        writeHook(ROM_COPY, 0x8067FE28, Overlay.Static, "makeCannonsRequireBlast", offset_dict)
        writeHook(ROM_COPY, 0x806806B4, Overlay.Static, "fixCannonBlastNoclip", offset_dict)

    # Item Rando
    # Item Get
    item_get_addrs = [
        0x806F64C8,
        0x806F6BA8,
        0x806F7740,
        0x806F7764,
        0x806F7774,
        0x806F7798,
        0x806F77B0,
        0x806F77C4,
        0x806F7804,
        0x806F781C,
    ]
    for addr in item_get_addrs:
        writeFunction(ROM_COPY, addr, Overlay.Static, "getItem", offset_dict)  # Modify Function Call
    writeFunction(ROM_COPY, 0x806F6350, Overlay.Static, "getObjectCollectability", offset_dict)  # Modify Function Call
    writeFunction(ROM_COPY, 0x8070E1F0, Overlay.Static, "handleDynamicItemText", offset_dict)  # Handle Dynamic Text Item Name
    writeFunction(ROM_COPY, 0x806A7AEC, Overlay.Static, "BalloonShoot", offset_dict)  # Balloon Shoot Hook
    # Rainbow Coins
    writeFunction(ROM_COPY, 0x806A222C, Overlay.Static, "getPatchFlag", offset_dict)  # Get Patch Flags
    writeFunction(ROM_COPY, 0x806A2058, Overlay.Static, "getPatchFlag", offset_dict)  # Get Patch Flags
    writeValue(ROM_COPY, 0x80688C8E, Overlay.Static, 0x30, offset_dict)  # Reduce scope of detecting if balloon or patch, so patches don't have dynamic flags
    writeFunction(ROM_COPY, 0x80680AE8, Overlay.Static, "alterBonusVisuals", offset_dict)  # Get Bonus Flag Check
    writeFunction(ROM_COPY, 0x806A206C, Overlay.Static, "getDirtPatchSkin", offset_dict)  # Get Dirt Flag Check
    writeFunction(ROM_COPY, 0x80681854, Overlay.Static, "getBonusFlag", offset_dict)  # Get Bonus Flag Check
    writeFunction(ROM_COPY, 0x806C63A8, Overlay.Static, "getBonusFlag", offset_dict)  # Get Bonus Flag Check
    writeFunction(ROM_COPY, 0x806F78B8, Overlay.Static, "getKongFromBonusFlag", offset_dict)  # Reward Table Kong Check
    # Check Screen
    writeFunction(ROM_COPY, 0x806A9F98, Overlay.Static, "pauseScreen3And4Header", offset_dict)  # Header
    writeFunction(ROM_COPY, 0x806AA03C, Overlay.Static, "pauseScreen3And4Counter", offset_dict)  # Counter
    writeFunction(ROM_COPY, 0x806A86BC, Overlay.Static, "changePauseScreen", offset_dict)  # Change screen hook
    writeFunction(ROM_COPY, 0x806A8D20, Overlay.Static, "changeSelectedLevel", offset_dict)  # Change selected level on checks screen
    writeFunction(ROM_COPY, 0x806A84F8, Overlay.Static, "checkItemDB", offset_dict)  # Populate Item Databases
    writeFunction(ROM_COPY, 0x806A9978, Overlay.Static, "displayHintRegion", offset_dict)  # Display hint region
    writeValue(ROM_COPY, 0x806A94CC, Overlay.Static, 0x2C610003, offset_dict, 4)  # SLTIU $at, $v1, 0x3 (Changes render check for <3 rather than == 3)
    writeValue(ROM_COPY, 0x806A94D0, Overlay.Static, 0x10200298, offset_dict, 4)  # BEQZ $at, 0x298 (Changes render check for <3 rather than == 3)
    writeValue(ROM_COPY, 0x806A932A, Overlay.Static, 12500, offset_dict)  # Increase memory allocated for displaying the Pause menu (fixes hints corrupting the heap)
    if settings.progressive_hint_item == ProgressiveHintItem.req_cb:
        writeFunction(ROM_COPY, 0x806AB4C4, Overlay.Static, "displayCBCount", offset_dict)
    # Restore unused events
    writeValue(ROM_COPY, 0x800336A4, Overlay.Menu, 7, offset_dict)  # Play cutscene 7 (Overwrites one of the leg shakes)
    writeValue(ROM_COPY, 0x800336A6, Overlay.Menu, 150, offset_dict)  # Set duration as 150
    writeValue(ROM_COPY, 0x8003371A, Overlay.Menu, 8, offset_dict)  # Play cutscene 8
    writeValue(ROM_COPY, 0x8003371C, Overlay.Menu, 150, offset_dict)  # Set duration as 150
    writeFloatUpper(ROM_COPY, 0x800283D2, Overlay.Menu, 11, offset_dict)  # Set randomization function to use 11 values
    writeValue(ROM_COPY, 0x80028412, Overlay.Menu, 11 + 1, offset_dict)  # Set cap to 12
    writeValue(ROM_COPY, 0x8002845A, Overlay.Menu, 11 + 1, offset_dict)  # Set cap to 12
    if settings.shuffle_items:
        writeHook(ROM_COPY, 0x806A6708, Overlay.Static, "SpriteFix", offset_dict)
        writeFunction(ROM_COPY, 0x806A78A8, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Balloon: Kong Check
        writeFunction(ROM_COPY, 0x806AAB3C, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Pause: BP Get
        writeFunction(ROM_COPY, 0x806AAB9C, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Pause: BP In
        writeFunction(ROM_COPY, 0x806AAD70, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Pause: Fairies
        writeFunction(ROM_COPY, 0x806AAF70, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Pause: Crowns
        writeFunction(ROM_COPY, 0x806AB064, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Pause: Isle Crown 1
        writeFunction(ROM_COPY, 0x806AB0B4, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Pause: Isle Crown 2
        writeFunction(ROM_COPY, 0x806ABF00, Overlay.Static, "checkFlagDuplicate", offset_dict)  # File Percentage: Keys
        writeFunction(ROM_COPY, 0x806ABF78, Overlay.Static, "checkFlagDuplicate", offset_dict)  # File Percentage: Crowns
        writeFunction(ROM_COPY, 0x806ABFA8, Overlay.Static, "checkFlagDuplicate", offset_dict)  # File Percentage: NCoin
        writeFunction(ROM_COPY, 0x806ABFBC, Overlay.Static, "checkFlagDuplicate", offset_dict)  # File Percentage: RCoin
        writeFunction(ROM_COPY, 0x806AC00C, Overlay.Static, "checkFlagDuplicate", offset_dict)  # File Percentage: Kongs
        writeFunction(ROM_COPY, 0x806BD304, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Key flag check: K. Lumsy
        writeFunction(ROM_COPY, 0x80731A6C, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Count flag-kong array
        writeFunction(ROM_COPY, 0x80731AE8, Overlay.Static, "checkFlagDuplicate", offset_dict)  # Count flag array
        writeFunction(ROM_COPY, 0x806B1E48, Overlay.Static, "countFlagsForKongFLUT", offset_dict)  # Kasplat Check Flag
        writeValue(ROM_COPY, 0x806F56F8, Overlay.Static, 0, offset_dict, 4)  # Disable Flag Set for blueprints
        writeFunction(ROM_COPY, 0x806F938C, Overlay.Static, "banana_medal_acquisition", offset_dict)  # Medal Give
        writeValue(ROM_COPY, 0x806F9394, Overlay.Static, 0, offset_dict, 4)
        writeFunction(ROM_COPY, 0x806F5564, Overlay.Static, "itemGrabHook", offset_dict)  # Item Get Hook - Post Flag
        writeFunction(ROM_COPY, 0x806A6CA8, Overlay.Static, "canItemPersist", offset_dict)  # Item Despawn Check
        writeValue(ROM_COPY, 0x806A741C, Overlay.Static, 0, offset_dict, 4)  # Prevent Key Twinkly Sound
        writeFunction(ROM_COPY, 0x80688714, Overlay.Static, "setupHook", offset_dict)  # Setup Load Hook
        # Fairy Adjustments
        writeFunction(ROM_COPY, 0x8072728C, Overlay.Static, "spawnCharSpawnerActor", offset_dict)  # Spawn 1
        writeValue(ROM_COPY, 0x80727290, Overlay.Static, 0x36050000, offset_dict, 4)  # ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        writeFunction(ROM_COPY, 0x8072777C, Overlay.Static, "spawnCharSpawnerActor", offset_dict)  # Spawn 2
        writeValue(ROM_COPY, 0x80727780, Overlay.Static, 0x36050000, offset_dict, 4)  # ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        writeFunction(ROM_COPY, 0x807277D0, Overlay.Static, "spawnCharSpawnerActor", offset_dict)  # Spawn 3
        writeValue(ROM_COPY, 0x807277D4, Overlay.Static, 0x36050000, offset_dict, 4)  # ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        writeFunction(ROM_COPY, 0x80727B88, Overlay.Static, "spawnCharSpawnerActor", offset_dict)  # Spawn 4
        writeValue(ROM_COPY, 0x80727B8C, Overlay.Static, 0x36050000, offset_dict, 4)  # ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        writeFunction(ROM_COPY, 0x80727C10, Overlay.Static, "spawnCharSpawnerActor", offset_dict)  # Spawn 4
        writeValue(ROM_COPY, 0x80727C14, Overlay.Static, 0x36050000, offset_dict, 4)  # ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        writeFunction(ROM_COPY, 0x806C5F04, Overlay.Static, "giveFairyItem", offset_dict)  # Fairy Flag Set
        # Rainbow Coins
        writeFunction(ROM_COPY, 0x806A2268, Overlay.Static, "spawnDirtPatchReward", offset_dict)  # Spawn Reward
        # Mill GB
        writeFunction(ROM_COPY, 0x806F633C, Overlay.Static, "isObjectTangible_detailed", offset_dict)  # Change object tangibility check function

        writeValue(ROM_COPY, 0x806C5C7C, Overlay.Static, 0, offset_dict, 4)  # Cancel out fairy draw distance reduction
        writeFunction(ROM_COPY, 0x806C63BC, Overlay.Static, "spawnRewardAtActor", offset_dict)  # Spawn Squawks Reward
        writeFunction(ROM_COPY, 0x806C4654, Overlay.Static, "spawnMinecartReward", offset_dict)  # Spawn Squawks Reward - Minecart
        writeFunction(ROM_COPY, 0x8002501C, Overlay.Bonus, "spawnCrownReward", offset_dict)  # Crown Spawn
        writeFunction(ROM_COPY, 0x80028650, Overlay.Boss, "spawnBossReward", offset_dict)  # Key Spawn

        writeFunction(ROM_COPY, 0x80027E68, Overlay.Critter, "fairyQueenCutsceneInit", offset_dict)  # BFI, Init Cutscene Setup
        writeFunction(ROM_COPY, 0x80028104, Overlay.Critter, "fairyQueenCutsceneCheck", offset_dict)  # BFI, Cutscene Play
        writeFunction(ROM_COPY, 0x80028014, Overlay.Critter, "fairyQueenCheckSpeedup", offset_dict)  # BFI, Cutscene Prep
        # Flag Stuff
        writeFunction(ROM_COPY, 0x80024CF0, Overlay.Menu, "countFlagsDuplicate", offset_dict)  # Flag change to FLUT
        writeFunction(ROM_COPY, 0x80024854, Overlay.Menu, "checkFlagDuplicate", offset_dict)  # Flag change to FLUT
        writeFunction(ROM_COPY, 0x80024880, Overlay.Menu, "checkFlagDuplicate", offset_dict)  # Flag change to FLUT
        writeFunction(ROM_COPY, 0x800248B0, Overlay.Menu, "setFlagDuplicate", offset_dict)  # Flag change to FLUT
        # Pause Stuff
        writeFunction(ROM_COPY, 0x806A9D50, Overlay.Static, "handleOutOfCounters", offset_dict)  # Print out of counter, depending on item rando state
        writeFunction(ROM_COPY, 0x806A9EFC, Overlay.Static, "handleOutOfCounters", offset_dict)  # Print out of counter, depending on item rando state
        writeValue(ROM_COPY, 0x806A9C80, Overlay.Static, 0, offset_dict, 4)  # Show counter on Helm Menu - Kong specific screeen
        writeValue(ROM_COPY, 0x806A9E54, Overlay.Static, 0, offset_dict, 4)  # Show counter on Helm Menu - All Kongs screen
        # writeValue(ROM_COPY, 0x806AA860, Overlay.Static, 0x31EF0007, offset_dict, 4) # ANDI $t7, $t7, 7 - Show GB (Kong Specific)
        # writeValue(ROM_COPY, 0x806AADC4, Overlay.Static, 0x33390007, offset_dict, 4) # ANDI $t9, $t9, 7 - Show GB (All Kongs)
        # writeValue(ROM_COPY, 0x806AADC8, Overlay.Static, 0xAFB90058, offset_dict, 4) # SW $t9, 0x58 ($sp) - Show GB (All Kongs)
        # Actors with special spawning conditions
        writeValue(ROM_COPY, 0x806B4E1A, Overlay.Static, getActorIndex(spoiler.aztec_vulture_actor), offset_dict)
        writeValue(ROM_COPY, 0x8069C266, Overlay.Static, getActorIndex(spoiler.japes_rock_actor), offset_dict)
        # Melon Crates
        writeLabelValue(ROM_COPY, 0x80747EB0, Overlay.Static, "melonCrateItemHandler", offset_dict)
    # Initialize fixed item scales
    writeFunction(ROM_COPY, 0x806F4918, Overlay.Static, "writeItemScale", offset_dict)  # Write scale to collision info
    writeValue(ROM_COPY, 0x806F491C, Overlay.Static, 0x87A40066, offset_dict, 4)
    # LH $a0, 0x66 ($sp)
    writeValue(ROM_COPY, 0x806F4C6E, Overlay.Static, 0x20, offset_dict)  # Change size
    writeValue(ROM_COPY, 0x806F4C82, Overlay.Static, 0x20, offset_dict)  # Change size
    writeFunction(ROM_COPY, 0x806F515C, Overlay.Static, "writeItemActorScale", offset_dict)  # Write actor scale to collision info
    writeFunction(ROM_COPY, 0x80681910, Overlay.Static, "spawnBonusReward", offset_dict)  # Spawn Bonus Reward
    writeValue(ROM_COPY, 0x806C46AA, Overlay.Static, 0x4100, offset_dict)  # Bring squawks closer to the player for minecarts (X)
    writeValue(ROM_COPY, 0x806C46E2, Overlay.Static, 0x4100, offset_dict)  # Bring squawks closer to the player for minecarts (Z)
    writeValue(ROM_COPY, 0x806C45C2, Overlay.Static, 0x0013, offset_dict)  # Y Offset squawks reward

    if settings.fast_warps:
        writeValue(ROM_COPY, 0x806EE692, Overlay.Static, 0x54, offset_dict)
        writeFunction(ROM_COPY, 0x806DC2AC, Overlay.Static, "fastWarp", offset_dict)  # Modify Function Call

    # Collision fixes
    QUAD_SIZE = 100
    writeValue(ROM_COPY, 0x806F4ACA, Overlay.Static, QUAD_SIZE, offset_dict)
    writeValue(ROM_COPY, 0x806F4BF0, Overlay.Static, 0x240A0000 | QUAD_SIZE, offset_dict, 4)  # addiu $t2, $zero, QUAD_SIZE
    writeValue(ROM_COPY, 0x806F4BF4, Overlay.Static, 0x01510019, offset_dict, 4)  # multu $t2, $s1
    writeValue(ROM_COPY, 0x806F4BF8, Overlay.Static, 0x00008812, offset_dict, 4)  # mflo $s1
    writeValue(ROM_COPY, 0x806F4BFC, Overlay.Static, 0, offset_dict, 4)  # NOP
    writeValue(ROM_COPY, 0x806F4C00, Overlay.Static, 0, offset_dict, 4)  # NOP
    writeValue(ROM_COPY, 0x806F4C16, Overlay.Static, QUAD_SIZE, offset_dict)
    writeValue(ROM_COPY, 0x806F4C52, Overlay.Static, QUAD_SIZE, offset_dict)

    writeFunction(ROM_COPY, 0x806F502C, Overlay.Static, "getCollisionSquare_New", offset_dict)  # Assigning hitbox to data table
    writeFunction(ROM_COPY, 0x806F5134, Overlay.Static, "getCollisionSquare_New", offset_dict)  # Assigning hitbox to data table
    writeFunction(ROM_COPY, 0x806F6A0C, Overlay.Static, "checkForValidCollision", offset_dict)  # Detecting if object is inside current quadrant
    writeFunction(ROM_COPY, 0x806F6A2C, Overlay.Static, "checkForValidCollision", offset_dict)  # Detecting if object is inside current quadrant

    # Make BBBash reference the internal hit counter rather than the displayed one
    writeValue(ROM_COPY, 0x8002B4DE, Overlay.Bonus, 0x2A, offset_dict)
    writeValue(ROM_COPY, 0x8002B502, Overlay.Bonus, 0x2A, offset_dict)
    writeValue(ROM_COPY, 0x8002B55A, Overlay.Bonus, 0x2A, offset_dict)

    # Alter amount of Klaptraps in Searchlight seek
    writeValue(ROM_COPY, 0x8002C1FA, Overlay.Bonus, KLAPTRAPS_IN_SEARCHLIGHT_SEEK, offset_dict)
    writeValue(ROM_COPY, 0x8002C1D2, Overlay.Bonus, KLAPTRAPS_IN_SEARCHLIGHT_SEEK, offset_dict)

    writeFunction(ROM_COPY, 0x8062F084, Overlay.Static, "setFog", offset_dict)

    # Fix issues where multiple loaded fairies will only allow 1 fairy to be referenced
    if FAIRY_LOAD_FIX:
        # Paad Offset | Actor offset | var name
        # 038         | 1B0          | ScreenX
        # 03A         | 1B2          | ScreenY
        # 03C         | 1B4          | Dist
        # 03E         | 1B6          | In Range
        FAIRY_SCREEN_X = 0x1B0
        FAIRY_SCREEN_Y = 0x1B2
        FAIRY_SCREEN_DIST = 0x1B4
        FAIRY_SCREEN_RANGE = 0x1B6
        writeValue(ROM_COPY, 0x806C5DA0, Overlay.Static, 0x8D4CBB40, offset_dict, 4)  # lw $t4, 0xBB40 ($t2) - Get current actor pointer
        writeValue(ROM_COPY, 0x806C5DA4, Overlay.Static, 0x2550D580, offset_dict, 4)  # addiu $s0, $t2, 0xD580 - Get extra player pointer addr (Overwritten)
        writeValue(ROM_COPY, 0x806C5DA8, Overlay.Static, 0x8D4AC924, offset_dict, 4)  # lw $t2, 0xC924 ($t2) - Get char change pointer (overwritten)
        writeValue(ROM_COPY, 0x806C5DAC, Overlay.Static, 0x85820000 | FAIRY_SCREEN_X, offset_dict, 4)  # lh $v0, 0x01B0 ($t4) - Get screen X in fairy storage
        writeValue(ROM_COPY, 0x806C5DB0, Overlay.Static, 0xC5500284, offset_dict, 4)  # lwc1 $f16, 0x0284 ($t2) - Get some char spawner attr (Overwritten)
        # writeValue(ROM_COPY, 0x806C5DB8, Overlay.Static, 0xA5800000 | FAIRY_SCREEN_RANGE, offset_dict, 4)  # sh $zero, 0x1B6 ($t4) - Store fairy not in box
        writeValue(ROM_COPY, 0x806C5DB8, Overlay.Static, 0x00000000, offset_dict, 4)  # NOP
        writeValue(ROM_COPY, 0x806C5DCC, Overlay.Static, 0x00000000, offset_dict, 4)  # NOP
        writeValue(ROM_COPY, 0x806C5DD0, Overlay.Static, 0x85820000 | FAIRY_SCREEN_Y, offset_dict, 4)  # lh $v0, 0x01B2 ($t4) - Get screen Y in fairy storage
        if not isQoLEnabled(spoiler, MiscChangesSelected.better_fairy_camera):
            writeValue(ROM_COPY, 0x806C5DE4, Overlay.Static, 0x00000000, offset_dict, 4)  # NOP
            writeValue(ROM_COPY, 0x806C5DE8, Overlay.Static, 0x858B0000 | FAIRY_SCREEN_DIST, offset_dict, 4)  # lh $t3, 0x01B4 ($t4) - Get max dist in fairy storage
        writeValue(ROM_COPY, 0x806C5E00, Overlay.Static, 0x45000016, offset_dict, 4)  # bc1f 0x16 - Free up one slot so we can store the box addr
        writeValue(ROM_COPY, 0x806C5E08, Overlay.Static, 0x24010001, offset_dict, 4)  # li $at, 1 - Shift this one addr earlier
        writeValue(ROM_COPY, 0x806C5E0C, Overlay.Static, 0xA5810000 | FAIRY_SCREEN_RANGE, offset_dict, 4)  # sh $at, 0x1b6 ($t4) - Store fairy as in box
        writeValue(
            ROM_COPY, 0x806C5E10, Overlay.Static, 0x904D01EC, offset_dict, 4
        )  # lbu $t5 0x01EC ($v0) - Fix the reference address since we're no longer storing a copy of extra player pointer to t4
        # Storage
        writeHook(ROM_COPY, 0x806C5FA8, Overlay.Static, "storeFairyData", offset_dict)
        # Check
        writeValue(ROM_COPY, 0x806C5EA8, Overlay.Static, 0x3C108080, offset_dict, 4)  # lui $s0, 0x8080
        writeValue(ROM_COPY, 0x806C5EAC, Overlay.Static, 0x8E0ABB40, offset_dict, 4)  # lw $t2, 0xBB40 ($s0)
        writeValue(ROM_COPY, 0x806C5EB0, Overlay.Static, 0x854A0000 | FAIRY_SCREEN_RANGE, offset_dict, 4)  # lh $t2, 0x01B6 ($t2)
        writeValue(ROM_COPY, 0x806C5EB4, Overlay.Static, 0x1140001B, offset_dict, 4)  # beqz $t2, 0x1B
        # Face controllers
        writeHook(ROM_COPY, 0x806C5E88, Overlay.Static, "setSadFace", offset_dict)
        writeHook(ROM_COPY, 0x806C5E3C, Overlay.Static, "setHappyFace", offset_dict)
        writeFunction(ROM_COPY, 0x806CAAA0, Overlay.Static, "resetPictureStatus", offset_dict)

        # Thankfully currentactor is loaded into a0.
        # I don't think we can sneak in creating the other JALs necessary to calculate distance.
        # We could make this part of "better fairy camera"? This means those calcuations don't need to be made.

    if JP_TEXTBOX_SIZES:
        needs_textboxes_for_hints = False
        if settings.progressive_hint_item == ProgressiveHintItem.off:  # Progressive hints are disabled, hints are on doors
            if settings.wrinkly_hints != WrinklyHints.off:  # Hints have something of value
                needs_textboxes_for_hints = True
        if settings.item_reward_previews:  # Textboxes will detail information about the item
            needs_textboxes_for_hints = True
        if needs_textboxes_for_hints:
            writeValue(ROM_COPY, 0x8075A788, Overlay.Static, 0x40026666, offset_dict, 4)
            writeValue(ROM_COPY, 0x8075A78C, Overlay.Static, 0x60000000, offset_dict, 4)
            writeValue(ROM_COPY, 0x8075A790, Overlay.Static, 0x4064B333, offset_dict, 4)
            writeValue(ROM_COPY, 0x8075A794, Overlay.Static, 0x20000000, offset_dict, 4)
            writeFloat(ROM_COPY, 0x8075A7A0, Overlay.Static, 165.6, offset_dict)
            writeFloat(ROM_COPY, 0x8075A7A4, Overlay.Static, 96.6, offset_dict)
            writeValue(ROM_COPY, 0x8075A7A8, Overlay.Static, 0x4056A666, offset_dict, 4)
            writeValue(ROM_COPY, 0x8075A7AC, Overlay.Static, 0x60000000, offset_dict, 4)
            writeValue(ROM_COPY, 0x8075E4A0, Overlay.Static, 0x40633333, offset_dict, 4)
            writeValue(ROM_COPY, 0x8075E4A4, Overlay.Static, 0x20000000, offset_dict, 4)
            writeValue(ROM_COPY, 0x806A42B6, Overlay.Static, 0x6000, offset_dict)  # Increase a malloc
            writeValue(ROM_COPY, 0x806F8C20, Overlay.Static, 0x5000, offset_dict)  # Remove GB HUD

    if FRAMEBUFFER_STORE_FIX:
        writeHook(ROM_COPY, 0x8070A848, Overlay.Static, "disableFBStore", offset_dict)
        writeHook(ROM_COPY, 0x8070B05C, Overlay.Static, "disableFBZip0", offset_dict)
        writeHook(ROM_COPY, 0x80709BC4, Overlay.Static, "disableFBZip1", offset_dict)
        writeHook(ROM_COPY, 0x8061134C, Overlay.Static, "disableFBZip2", offset_dict)
        writeHook(ROM_COPY, 0x80629230, Overlay.Static, "disableFBMisc", offset_dict)

    # Spawn Enemy Drops function
    enemy_drop_addrs = [
        0x806AD40C,
        0x806AED14,
        0x806AF5A4,
        0x806B0218,
        0x806B0704,
        0x806B0C8C,
        0x806B1C88,
        0x806B4744,
        0x806B5B90,
        0x806B61E0,
        0x806B744C,
        0x806B9AB4,
    ]
    for addr in enemy_drop_addrs:
        writeFunction(ROM_COPY, addr, Overlay.Static, "spawnEnemyDrops", offset_dict)

    if settings.no_healing:
        writeValue(ROM_COPY, 0x80683A34, Overlay.Static, 0, offset_dict, 4)  # Cancel Tag Health Refill
        writeValue(ROM_COPY, 0x806CB340, Overlay.Static, 0, offset_dict, 4)  # Voiding
        writeValue(ROM_COPY, 0x806DEFE4, Overlay.Static, 0, offset_dict, 4)  # Fairies
        writeValue(ROM_COPY, 0x806A6EA8, Overlay.Static, 0, offset_dict, 4)  # Bonus Barrels
        writeValue(ROM_COPY, 0x800289B0, Overlay.Boss, 0, offset_dict, 4)  # K Rool between-phase health refilll
    else:
        writeValue(ROM_COPY, 0x806A6EA8, Overlay.Static, 0x0C1C2519, offset_dict, 4)  # Set Bonus Barrel to refill health
        writeFunction(ROM_COPY, 0x80025564, Overlay.Boss, "refillHealthOnInit", offset_dict)  # Army Dillo
        writeFunction(ROM_COPY, 0x8002A9B0, Overlay.Boss, "refillHealthOnInit", offset_dict)  # Dogadon
        writeFunction(ROM_COPY, 0x80033B70, Overlay.Boss, "refillHealthOnInit", offset_dict)  # Mad Jack
        writeFunction(ROM_COPY, 0x800294C0, Overlay.Boss, "refillHealthOnInit", offset_dict)  # Pufftoss
        writeFunction(ROM_COPY, 0x80031C6C, Overlay.Boss, "refillPlayerHealthKKO", offset_dict)  # KKO

    if settings.warp_to_isles:
        writeHook(ROM_COPY, 0x806A995C, Overlay.Static, "PauseExtraSlotCode", offset_dict)
        writeHook(ROM_COPY, 0x806A9818, Overlay.Static, "PauseExtraHeight", offset_dict)
        writeHook(ROM_COPY, 0x806A87BC, Overlay.Static, "PauseExtraSlotClamp0", offset_dict)
        writeHook(ROM_COPY, 0x806A8760, Overlay.Static, "PauseExtraSlotClamp1", offset_dict)
        writeHook(ROM_COPY, 0x806A8804, Overlay.Static, "PauseExtraSlotCustomCode", offset_dict)
        writeHook(ROM_COPY, 0x806A9898, Overlay.Static, "PauseCounterCap", offset_dict)
        # Pause Menu Exit To Isles Slot
        writeValue(ROM_COPY, 0x806A85EE, Overlay.Static, 4, offset_dict)  # Yes/No Prompt
        writeValue(ROM_COPY, 0x806A8716, Overlay.Static, 4, offset_dict)  # Yes/No Prompt
        # writeValue(ROM_COPY, 0x806A87BE, Overlay.Static, 3, offset_dict)
        writeValue(ROM_COPY, 0x806A880E, Overlay.Static, 4, offset_dict)  # Yes/No Prompt
        # writeValue(ROM_COPY, 0x806A8766, Overlay.Static, 4, offset_dict)
        writeValue(ROM_COPY, 0x806A986A, Overlay.Static, 4, offset_dict)  # Yes/No Prompt
        writeValue(ROM_COPY, 0x806A9990, Overlay.Static, 0x2A210000 | 0x270, offset_dict, 4)  # SLTI $at, $s1, 0x270 (y_cap = 0x270)

    # Big Head Static stuff
    writeValue(ROM_COPY, 0x80612E98, Overlay.Static, 0xA4850172, offset_dict, 4)  # sh $a1, 0x172 ($a0)
    writeValue(ROM_COPY, 0x80612E9E, Overlay.Static, 0xBB30, offset_dict)  # change lhu offset

    # Fix fairies to not drain items
    writeFunction(ROM_COPY, 0x806DEFFC, Overlay.Static, "refillIfRefillable", offset_dict)

    if settings.item_reward_previews:
        writeValue(ROM_COPY, 0x8002489C, Overlay.Race, 0, offset_dict, 4)  # Beetle Races
        writeValue(ROM_COPY, 0x8002BA9C, Overlay.Race, 0, offset_dict, 4)  # Castle Car Race
        writeValue(ROM_COPY, 0x80028580, Overlay.Race, 0, offset_dict, 4)  # Factory Car Race

    # Pause Stuff
    FLAG_BP_JAPES_DK_HAS = 0x1D5
    # Prevent GBs being required to view extra screens
    writeValue(ROM_COPY, 0x806A8624, Overlay.Static, 0, offset_dict, 4)  # GBs doesn't lock other pause screens
    writeValue(ROM_COPY, 0x806AB468, Overlay.Static, 0, offset_dict, 4)  # Show R/Z Icon
    writeValue(ROM_COPY, 0x806AB318, Overlay.Static, 0x24060001, offset_dict, 4)  # ADDIU $a2, $r0, 1
    writeValue(ROM_COPY, 0x806AB31C, Overlay.Static, 0xA466C83C, offset_dict, 4)  # SH $a2, 0xC83C ($v1) | Overwrite trap func, Replace with overwrite of wheel segments
    writeValue(ROM_COPY, 0x8075056C, Overlay.Static, 201, offset_dict)  # Change GB Item cap to 201
    # In-Level IGT
    writeFunction(ROM_COPY, 0x8060DF28, Overlay.Static, "updateLevelIGT", offset_dict)
    # Modify Function Call
    writeFunction(ROM_COPY, 0x806ABB0C, Overlay.Static, "printLevelIGT", offset_dict)
    # Modify Function Call
    writeValue(ROM_COPY, 0x806ABB32, Overlay.Static, 106, offset_dict)  # Adjust kong name height
    # Disable Item Checks
    writeValue(ROM_COPY, 0x806AB2E8, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x806AB360, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x806ABFCE, Overlay.Static, FLAG_BP_JAPES_DK_HAS, offset_dict)  # Change BP trigger to being collecting BP rather than turning it in
    if isQoLEnabled(spoiler, MiscChangesSelected.fast_pause_transitions):
        writeFloat(ROM_COPY, 0x8075AC00, Overlay.Static, 1.3, offset_dict)  # Pause Menu Progression Rate
        writeValue(ROM_COPY, 0x806A901C, Overlay.Static, 4, offset_dict, 4)  # NOP - Remove thud
    writeFunction(ROM_COPY, 0x806A84C8, Overlay.Static, "updateFileVariables", offset_dict)  # Update file variables to transfer old locations to current

    updateActorFunction(ROM_COPY, 340, "handleBugEnemy")

    writeFunction(ROM_COPY, 0x80714168, Overlay.Static, "fixHelmTimerDisable", offset_dict)

    if Types.Hint in spoiler.settings.shuffled_location_types:
        writeValue(ROM_COPY, 0x8069E18C, Overlay.Static, 0x00003025, offset_dict, 4)  # or a2, zero, zero

    # Alter data for zinger flamethrower enemy
    writeValue(ROM_COPY, 0x8075F210, Overlay.Static, 345 + (CustomActors.ZingerFlamethrower - 0x8000), offset_dict)
    writeValue(ROM_COPY, 0x8075F212, Overlay.Static, Model.Zinger + 1, offset_dict)
    writeValue(ROM_COPY, 0x8075F214, Overlay.Static, 0x250, offset_dict)
    writeValue(ROM_COPY, 0x8075F216, Overlay.Static, 0, offset_dict)
    writeValue(ROM_COPY, 0x8075F218, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x8075F21C, Overlay.Static, 0xAA460508, offset_dict, 4)
    writeValue(ROM_COPY, 0x8075F220, Overlay.Static, 0x08020A0A, offset_dict, 4)
    writeValue(ROM_COPY, 0x8075F224, Overlay.Static, 0x5E5E0100, offset_dict, 4)

    # Make Flame Zingers not lag the game *as* bad
    writeValue(ROM_COPY, 0x806B3E36, Overlay.Static, 3, offset_dict)  # Change flame-spitting to once every 3f
    writeValue(ROM_COPY, 0x806B3E38, Overlay.Static, 0x5700, offset_dict)  # BEQL -> BNEL

    # Alter data for bug enemy
    writeValue(ROM_COPY, 0x8075F0F0, Overlay.Static, 345 + (CustomActors.Scarab - 0x8000), offset_dict)
    writeValue(ROM_COPY, 0x8075F0F2, Overlay.Static, 0x118 + 1, offset_dict)
    writeValue(ROM_COPY, 0x8075F0F4, Overlay.Static, 0x281, offset_dict)
    writeValue(ROM_COPY, 0x8075F0F6, Overlay.Static, 0, offset_dict)
    writeValue(ROM_COPY, 0x8075F0F8, Overlay.Static, 1, offset_dict, 4)
    writeValue(ROM_COPY, 0x8075F0FC, Overlay.Static, 0xAA465A1E, offset_dict, 4)
    writeValue(ROM_COPY, 0x8075F100, Overlay.Static, 0x05030602, offset_dict, 4)
    writeValue(ROM_COPY, 0x8075F104, Overlay.Static, 0x5E5E0164, offset_dict, 4)
    writeValue(ROM_COPY, 0x8074B21E, Overlay.Static, 0xFF8, offset_dict)  # Allow other moves to knock down the bug
    writeLabelValue(ROM_COPY, 0x8074B244, Overlay.Static, "fixed_scarab_collision", offset_dict)  # Collision

    # Statistics
    writeFunction(ROM_COPY, 0x806C8ED0, Overlay.Static, "updateTagStat", offset_dict)
    writeFunction(ROM_COPY, 0x805FE86C, Overlay.Static, "updateEnemyKillStat", offset_dict)  # Also updates K. Rool kong for MJ/Doga 2
    writeFunction(ROM_COPY, 0x806E9C50, Overlay.Static, "updateFairyStat", offset_dict)
    writeFunction(ROM_COPY, 0x806C7298, Overlay.Static, "createEndSeqCreditsFile", offset_dict)

    if isQoLEnabled(spoiler, MiscChangesSelected.remove_extraneous_cutscenes):
        writeValue(ROM_COPY, 0x80024174, Overlay.Boss, 0, offset_dict, 4)  # Japes Dillo Long Intro
        writeValue(ROM_COPY, 0x80025CAC, Overlay.Boss, 0, offset_dict, 4)  # Japes Dillo Long Intro
        writeValue(ROM_COPY, 0x800291E8, Overlay.Boss, 0, offset_dict, 4)  # Generic Boss Intros
        writeValue(ROM_COPY, 0x8002B480, Overlay.Boss, 0, offset_dict, 4)  # Fungi Dogadon Long Intro
        writeValue(ROM_COPY, 0x80033BB4, Overlay.Boss, 0, offset_dict, 4)  # Mad Jack Long Intro
        writeValue(ROM_COPY, 0x8074452C, Overlay.Static, 1, offset_dict, 1)  # Story Skip starts with on

    # Flag Mapping
    flag_map_hi = getHiSym("new_flag_mapping")
    flag_map_lo = getLoSym("new_flag_mapping")
    flag_map_count = getVar("gb_dictionary_count")
    writeKongItemOwnership(ROM_COPY, settings)
    writeValue(ROM_COPY, 0x8073150A, Overlay.Static, flag_map_hi, offset_dict)
    writeValue(ROM_COPY, 0x8073151E, Overlay.Static, flag_map_lo, offset_dict)
    writeValue(ROM_COPY, 0x8073151A, Overlay.Static, flag_map_count, offset_dict)
    writeValue(ROM_COPY, 0x807315EA, Overlay.Static, flag_map_hi, offset_dict)
    writeValue(ROM_COPY, 0x807315FE, Overlay.Static, flag_map_lo, offset_dict)
    writeValue(ROM_COPY, 0x807315FA, Overlay.Static, flag_map_count, offset_dict)
    writeValue(ROM_COPY, 0x80731666, Overlay.Static, flag_map_hi, offset_dict)
    writeValue(ROM_COPY, 0x80731676, Overlay.Static, flag_map_lo, offset_dict)
    writeValue(ROM_COPY, 0x80731672, Overlay.Static, flag_map_count, offset_dict)

    writeHook(ROM_COPY, 0x8072F3DC, Overlay.Static, "blockTreeClimbing", offset_dict)
    if settings.enable_tag_anywhere:
        # Reduce TA Cooldown
        writeFunction(ROM_COPY, 0x806F5BE8, Overlay.Static, "tagAnywhereAmmo", offset_dict)
        writeFunction(ROM_COPY, 0x806F5A08, Overlay.Static, "tagAnywhereBunch", offset_dict)
        writeFunction(ROM_COPY, 0x806F6CB4, Overlay.Static, "tagAnywhereInit", offset_dict)
        # Fix Origin Warp with TA
        writeFunction(ROM_COPY, 0x8072F1E8, Overlay.Static, "handleGrabbingLock", offset_dict)
        writeFunction(ROM_COPY, 0x806CAB68, Overlay.Static, "handleLedgeLock", offset_dict)
        writeFunction(ROM_COPY, 0x8072F458, Overlay.Static, "handleActionSet", offset_dict)  # Actor grabbables
        writeFunction(ROM_COPY, 0x8072F46C, Overlay.Static, "handleActionSet", offset_dict)  # Model 2 grabbables
        writeFunction(ROM_COPY, 0x806CFC64, Overlay.Static, "handleActionSet", offset_dict)  # Ledge Grabbing
        writeFunction(ROM_COPY, 0x806E5418, Overlay.Static, "handleActionSet", offset_dict)  # Instrument Play
        writeFunction(ROM_COPY, 0x806E6064, Overlay.Static, "handleActionSet", offset_dict)  # Gun Pull

    if settings.bonus_barrel_auto_complete:
        writeValue(ROM_COPY, 0x806818DE, Overlay.Static, 0x4248, offset_dict)  # Make Aztec Lobby GB spawn above the trapdoor)
        writeValue(ROM_COPY, 0x80681690, Overlay.Static, 0, offset_dict, 4)  # Make some barrels not play a cutscene
        writeValue(ROM_COPY, 0x8068188C, Overlay.Static, 0, offset_dict, 4)  # Prevent disjoint mechanic for Caves/Fungi BBlast Bonus
        writeValue(ROM_COPY, 0x80681898, Overlay.Static, 0x1000, offset_dict)
        writeValue(ROM_COPY, 0x8068191C, Overlay.Static, 0, offset_dict, 4)  # Remove Oh Banana
        writeValue(ROM_COPY, 0x80680986, Overlay.Static, 0xFFFE, offset_dict)  # Prevent Factory BBBandit Bonus dropping
        writeValue(ROM_COPY, 0x806809C8, Overlay.Static, 0x1000, offset_dict)  # Prevent Fungi TTTrouble Bonus dropping
        writeValue(ROM_COPY, 0x80681962, Overlay.Static, 1, offset_dict)  # Make bonus noclip
        writeFunction(ROM_COPY, 0x80681158, Overlay.Static, "completeBonus", offset_dict)

    if settings.helm_hurry:
        writeFunction(ROM_COPY, 0x806A8A18, Overlay.Static, "QuitGame", offset_dict)  # Save game on quit
        writeValue(ROM_COPY, 0x80713CCC, Overlay.Static, 0, offset_dict, 4)  # Prevent Helm Timer Disable
        writeValue(ROM_COPY, 0x80713CD8, Overlay.Static, 0, offset_dict, 4)  # Prevent Shutdown Song Playing
        writeValue(ROM_COPY, 0x8071256A, Overlay.Static, 15, offset_dict)  # Init Helm Timer = 15 minutes
        writeFunction(ROM_COPY, 0x807125A4, Overlay.Static, "initHelmHurry", offset_dict)  # Change write
        writeFunction(ROM_COPY, 0x80713DE0, Overlay.Static, "finishHelmHurry", offset_dict)  # Change write
        writeValue(ROM_COPY, 0x807125CC, Overlay.Static, 0, offset_dict, 4)  # Prevent Helm Timer Overwrite
        writeValue(ROM_COPY, 0x807095BE, Overlay.Static, 0x2D4, offset_dict)  # Change Zipper with K. Rool Laugh
    elif IsItemSelected(settings.hard_mode, settings.hard_mode_selected, HardModeSelected.strict_helm_timer, False):
        # We cannot have both helm hurry and strict helm timer. Make helm hurry the most dominant setting
        writeValue(ROM_COPY, 0x8071256A, Overlay.Static, 0, offset_dict)  # Set start time of helm to 0 seconds

    if settings.wrinkly_location_rando or settings.remove_wrinkly_puzzles:
        writeValue(ROM_COPY, 0x8064F170, Overlay.Static, 0, offset_dict, 4)  # Prevent edge cases for Aztec Chunky/Fungi Wheel
        writeFunction(ROM_COPY, 0x8069E154, Overlay.Static, "getWrinklyLevelIndex", offset_dict)  # Modify Function Call

    if settings.tns_location_rando:
        # Adjust warp code to make camera be behind player, loading portal
        writeValue(ROM_COPY, 0x806C97D0, Overlay.Static, 0xA06E0007, offset_dict, 4)  # SB $t6, 0x7 ($v1)

    if IsItemSelected(settings.cb_rando_enabled, settings.cb_rando_list_selected, Levels.JungleJapes):
        writeValue(ROM_COPY, 0x8069C2FC, Overlay.Static, 0, offset_dict, 4)  # Japes Bunch
    if IsItemSelected(settings.cb_rando_enabled, settings.cb_rando_list_selected, Levels.DKIsles):
        writeFunction(ROM_COPY, 0x806ABF48, Overlay.Static, "getMedalCount", offset_dict)
        writeValue(ROM_COPY, 0x806AA458, Overlay.Static, 0, offset_dict, 4)  # Show CBs on Pause Menu (Main Screen)
        writeValue(ROM_COPY, 0x806AA858, Overlay.Static, 0, offset_dict, 4)  # Show CBs on Pause Menu (Level Kong Screen)
        # TODO: Work on Level Totals screen - this one is a bit more complicated

    writeFunction(ROM_COPY, 0x8002D6A8, Overlay.Bonus, "warpOutOfArenas", offset_dict)  # Enable the two arenas to be minigames
    writeFunction(ROM_COPY, 0x8002D31C, Overlay.Bonus, "ArenaTagKongCode", offset_dict)  # Tag Rambi/Enguarde Instantly
    writeFunction(ROM_COPY, 0x8002D6DC, Overlay.Bonus, "ArenaEarlyCompletionCheck", offset_dict)  # Check completion

    writeFunction(ROM_COPY, 0x8002D20C, Overlay.Boss, "SpiderBossExtraCode", offset_dict)  # Handle preventing spider boss being re-fightable

    # HUD Reallocation
    writeFunction(ROM_COPY, 0x806F48C8, Overlay.Static, "allocateHUD", offset_dict)
    writeFunction(ROM_COPY, 0x806C9C60, Overlay.Static, "allocateHUD", offset_dict)
    writeFunction(ROM_COPY, 0x806C90A8, Overlay.Static, "allocateHUD", offset_dict)
    writeFunction(ROM_COPY, 0x8002664C, Overlay.Menu, "allocateHUD", offset_dict)
    writeFunction(ROM_COPY, 0x806F97D8, Overlay.Static, "getHUDSprite_Complex", offset_dict)
    writeFunction(ROM_COPY, 0x806BE4E4, Overlay.Static, "getHUDSprite_Complex", offset_dict)
    writeFunction(ROM_COPY, 0x806AB588, Overlay.Static, "getHUDSprite_Complex", offset_dict)
    writeFunction(ROM_COPY, 0x806F98E4, Overlay.Static, "initHUDDirection", offset_dict)  # HUD Direction
    writeFunction(ROM_COPY, 0x806F9A00, Overlay.Static, "initHUDDirection", offset_dict)  # HUD Direction
    writeFunction(ROM_COPY, 0x806F9A78, Overlay.Static, "initHUDDirection", offset_dict)  # HUD Direction
    writeFunction(ROM_COPY, 0x806F9BC0, Overlay.Static, "initHUDDirection", offset_dict)  # HUD Direction
    writeFunction(ROM_COPY, 0x806F9D14, Overlay.Static, "initHUDDirection", offset_dict)  # HUD Direction
    writeHook(ROM_COPY, 0x80639F44, Overlay.Static, "disableRouletteNumbers", offset_dict)  # Disable Roulette numbers during pause
    writeHook(ROM_COPY, 0x806F93E0, Overlay.Static, "updateBarrierNumbers", offset_dict)  # Update barrier numbers

    writeFunction(ROM_COPY, 0x806D9E08, Overlay.Static, "fixUpdraftBug", offset_dict)  # Updraft fix

    if settings.perma_death:
        writeValue(ROM_COPY, 0x8064EC00, Overlay.Static, 0x24020001, offset_dict, 4)
        writeHook(ROM_COPY, 0x80682F2C, Overlay.Static, "permaLossTagCheck", offset_dict)
        writeHook(ROM_COPY, 0x80683620, Overlay.Static, "permaLossTagSet", offset_dict)
        writeHook(ROM_COPY, 0x806840C4, Overlay.Static, "permaLossTagDisplayCheck", offset_dict)

    if isFasterCheckEnabled(spoiler, FasterChecksSelected.factory_toy_monster_fight):
        writeValue(ROM_COPY, 0x806BBB22, Overlay.Static, 5, offset_dict)  # Chunky toy box speedup
        writeActorHealth(ROM_COPY, 228, 12)  # Change BHDM Health (16 -> 12)

    if isFasterCheckEnabled(spoiler, FasterChecksSelected.jetpac):
        writeValue(ROM_COPY, 0x80027DCA, Overlay.Jetpac, 2500, offset_dict)  # Jetpac score requirement

    if isFasterCheckEnabled(spoiler, FasterChecksSelected.forest_owl_race):
        writeValue(ROM_COPY, 0x806C58D6, Overlay.Static, 8, offset_dict)  # Owl ring amount
        writeValue(ROM_COPY, 0x806C5B16, Overlay.Static, 8, offset_dict)  # Owl ring amount

    if isFasterCheckEnabled(spoiler, FasterChecksSelected.forest_rabbit_race):
        writeValue(ROM_COPY, 0x806BEDFC, Overlay.Static, 0, offset_dict, 4)  # Spawn banana coins on beating rabbit 2 (Beating round 2 branches to banana coin spawning label before continuing)
        file_init_flags.append(0xF8)  # Rabbit Race Round 1

    if isFasterCheckEnabled(spoiler, FasterChecksSelected.caves_ice_tomato_minigame):
        writeValue(ROM_COPY, 0x806BC582, Overlay.Static, 30, offset_dict)  # Ice Tomato Timer

    if isFasterCheckEnabled(spoiler, FasterChecksSelected.factory_car_race):
        writeValue(ROM_COPY, 0x8002D03A, Overlay.Race, 1, offset_dict)  # Factory Car Race 1 Lap

    if isFasterCheckEnabled(spoiler, FasterChecksSelected.castle_car_race):
        writeValue(ROM_COPY, 0x8002D096, Overlay.Race, 1, offset_dict)  # Castle Car Race 1 Lap

    if isFasterCheckEnabled(spoiler, FasterChecksSelected.galleon_seal_race):
        writeValue(ROM_COPY, 0x8002D0E2, Overlay.Race, 1, offset_dict)  # Seal Race 1 Lap

    if settings.galleon_water_internal == GalleonWaterSetting.raised:
        file_init_flags.append(0xA0)  # Galleon Water Raised

    kong_flags = [0x181, 0x006, 0x046, 0x042, 0x075]
    if settings.starting_kongs_count == 5:
        file_init_flags.extend(kong_flags.copy())
    else:
        for x in spoiler.settings.starting_kong_list:
            file_init_flags.append(kong_flags[x])

    if settings.activate_all_bananaports == ActivateAllBananaports.isles:
        file_init_flags.extend(WARPS_ISLES.copy())
    elif settings.activate_all_bananaports == ActivateAllBananaports.isles_inc_helm_lobby:
        file_init_flags.extend(WARPS_ISLES.copy())
        file_init_flags.extend(WARPS_HELM_LOBBY.copy())
    elif settings.activate_all_bananaports == ActivateAllBananaports.all:
        for lvl in WARPS_TOTAL:
            file_init_flags.extend(lvl.copy())

    SCREEN_SHAKE_CAP = 7
    screen_shake_cap_patch = {
        0x8061F0C8: [
            0x30A500FF,  # andi a1, a1, 0xFF
            0x2CC10000 | SCREEN_SHAKE_CAP,  # sltiu at, a2, SCREEN_SHAKE_CAP
            0x50200001,  # beql at, r0, 1
            0x24060000 | SCREEN_SHAKE_CAP,  # addiu a2, r0, SCREEN_SHAKE_CAP
            0x24010001,  # li at, 1
        ],
        0x8061F0E4: [
            0x00063082,  # srl a2, a2, 2
            0x00000000,  # nop
        ],
    }
    for addr_head in screen_shake_cap_patch:
        for offset, value in enumerate(screen_shake_cap_patch[addr_head]):
            writeValue(ROM_COPY, addr_head + (4 * offset), Overlay.Static, value, offset_dict, 4)

    if IsItemSelected(settings.hard_mode, settings.hard_mode_selected, HardModeSelected.angry_caves, False):
        writeValue(ROM_COPY, 0x807480F4, Overlay.Static, 1, offset_dict, 4)  # Constant rockfall
        writeValue(ROM_COPY, 0x807480FC, Overlay.Static, 15, offset_dict, 4)  # Increase rockfall spawn rate (Every 20f -> 15f)
        writeValue(ROM_COPY, 0x806466D4, Overlay.Static, 0, offset_dict, 4)  # Kosha is alive no matter what
        writeValue(ROM_COPY, 0x806465DC, Overlay.Static, 0x1000, offset_dict)  # Kosha is alive no matter what
        accel = -90
        if settings.damage_amount in (DamageAmount.quad, DamageAmount.ohko):
            # Lower the velocity to make it a little fairer in scenarios where you're gonna die from not too many hits
            accel = -45
        writeFloat(ROM_COPY, 0x80750398, Overlay.Static, accel, offset_dict)  # Stalactite Acceleration
        writeValue(ROM_COPY, 0x806A04E2, Overlay.Static, 0, offset_dict)  # Disable cam shake
        writeValue(ROM_COPY, 0x806A051C, Overlay.Static, 0x1000001D, offset_dict, 4)  # Disable particles, lag reasons
        writeFunction(ROM_COPY, 0x806464C4, Overlay.Static, "spawnStalactite", offset_dict)
        writeValue(ROM_COPY, 0x806A04F6, Overlay.Static, 50, offset_dict)  # Reduce volume of stalactite crash
    elif isQoLEnabled(spoiler, MiscChangesSelected.calm_caves):
        file_init_flags.append(0x12C)  # Giant Kosha Dead

    if settings.free_trade_setting != FreeTradeSetting.none:
        # Non-BP Items
        writeValue(ROM_COPY, 0x807319C0, Overlay.Static, 0x00001025, offset_dict, 4)  # OR $v0, $r0, $r0 - Make all reward spots think no kong
        # writeValue(ROM_COPY, 0x80632E94, Overlay.Static, 0x00001025, offset_dict, 4)  # OR $v0, $r0, $r0 - Make flag mapping think no kong
        writeFunction(ROM_COPY, 0x80632E94, Overlay.Static, "getItemRequiredKong", offset_dict)  # Get required kong for item, used to set Stump GB as Tiny

        if settings.free_trade_setting == FreeTradeSetting.major_collectibles:
            writeValue(ROM_COPY, 0x806F56F8, Overlay.Static, 0, offset_dict, 4)  # Disable Flag Set for blueprints
            writeValue(ROM_COPY, 0x806A606C, Overlay.Static, 0, offset_dict, 4)  # Disable translucency for blueprints

    writeFunction(ROM_COPY, 0x806B26A0, Overlay.Static, "fireballEnemyDeath", offset_dict)
    if Types.Enemies in settings.shuffled_location_types:
        # Dropsanity
        writeFunction(ROM_COPY, 0x80729E54, Overlay.Static, "indicateCollectionStatus", offset_dict)
        writeValue(ROM_COPY, 0x807278CA, Overlay.Static, 0xFFF, offset_dict)  # Disable enemy switching in Fungi
        writeFunction(ROM_COPY, 0x806BB310, Overlay.Static, "rulerEnemyDeath", offset_dict)
        writeHook(ROM_COPY, 0x806680B4, Overlay.Static, "checkBeforeApplyingQuicksand", offset_dict)
        writeValue(ROM_COPY, 0x806680B8, Overlay.Static, 0x8E2C0058, offset_dict, 4)  # LW $t4, 0x58 ($s1)

    remove_blockers = False
    if remove_blockers:
        for x in range(8):
            file_init_flags.append(0x1CD + x)  # B. Locker clear flag

    if IsItemSelected(settings.hard_mode, settings.hard_mode_selected, HardModeSelected.hard_enemies, False):
        writeValue(ROM_COPY, 0x806B12DA, Overlay.Static, 0x3A9, offset_dict)  # Kasplat Shockwave Chance
        writeValue(ROM_COPY, 0x806B12FE, Overlay.Static, 0x3B3, offset_dict)  # Kasplat Shockwave Chance
        writeActorHealth(ROM_COPY, 259, 9)  # Increase kop health

    if IsItemSelected(settings.hard_mode, settings.hard_mode_selected, HardModeSelected.lower_max_refill_amounts, False):
        writeValue(ROM_COPY, 0x806F8F68, Overlay.Static, 0x24090000, offset_dict, 4)  # Standard Ammo: change from `(1 << ammo_belt) * 50` to a flat 50
        writeValue(ROM_COPY, 0x806F8FE4, Overlay.Static, 0x24190000, offset_dict, 4)  # Homing Ammo: change from `(1 << ammo_belt) * 50` to a flat 50
        writeValue(ROM_COPY, 0x806F9056, Overlay.Static, 5, offset_dict)  # Oranges: change from `(5 * ammo_belt) + 20` to `(5 * ammo_belt) + 5`
        writeValue(ROM_COPY, 0x806F90B6, Overlay.Static, 10 * 150, offset_dict)  # Crystals: change from `20 + fairy_count` to `10 + fairy_count`
        writeValue(ROM_COPY, 0x806F9186, Overlay.Static, 3, offset_dict)  # Film: change from `10 + fairy_count` to `3 + fairy_count`
        writeValue(ROM_COPY, 0x806F90C8, Overlay.Static, 0x24040000 | (10 * 150), offset_dict, 4)  # set min coconuts to 1500 (10 crystals)

    if IsItemSelected(settings.hard_mode, settings.hard_mode_selected, HardModeSelected.water_is_lava, False):
        writeValue(ROM_COPY, 0x806677C4, Overlay.Static, 0, offset_dict, 4)  # Dynamic Surfaces
        # Static Surfaces
        writeValue(ROM_COPY, 0x80667ED2, Overlay.Static, 0x81, offset_dict)
        writeValue(ROM_COPY, 0x80667EDA, Overlay.Static, 0x81, offset_dict)
        writeValue(ROM_COPY, 0x80667EEE, Overlay.Static, 0x81, offset_dict)
        writeValue(ROM_COPY, 0x80667EFA, Overlay.Static, 0x81, offset_dict)
        writeFunction(ROM_COPY, 0x8062F3F0, Overlay.Static, "replaceWaterTexture", offset_dict)  # Static water textures

    is_dark_world = IsItemSelected(settings.hard_mode, settings.hard_mode_selected, HardModeSelected.donk_in_the_dark_world, False)
    is_sky = IsItemSelected(settings.hard_mode, settings.hard_mode_selected, HardModeSelected.donk_in_the_sky, False)
    is_memory_challenge = is_dark_world and is_sky
    is_dark_world = is_dark_world and not is_memory_challenge
    is_sky = is_sky and not is_memory_challenge
    if is_dark_world or is_memory_challenge:
        writeFunction(ROM_COPY, 0x8062F230, Overlay.Static, "alterChunkLighting", offset_dict)
        writeFunction(ROM_COPY, 0x8065121C, Overlay.Static, "alterChunkLighting", offset_dict)
        writeFunction(ROM_COPY, 0x8062F2CC, Overlay.Static, "alterChunkData", offset_dict)
        writeFunction(ROM_COPY, 0x806C9DF8, Overlay.Static, "shineLight", offset_dict)
        writeFunction(ROM_COPY, 0x806C9E28, Overlay.Static, "shineLight", offset_dict)
        writeFunction(ROM_COPY, 0x806C9E58, Overlay.Static, "shineLight", offset_dict)
        writeFunction(ROM_COPY, 0x806C9E88, Overlay.Static, "shineLight", offset_dict)
        writeFunction(ROM_COPY, 0x806C9EB8, Overlay.Static, "shineLight", offset_dict)
        writeFunction(ROM_COPY, 0x806C9EE8, Overlay.Static, "shineLight", offset_dict)
        writeFunction(ROM_COPY, 0x806C9F2C, Overlay.Static, "shineLight", offset_dict)
        writeFunction(ROM_COPY, 0x806C9F5C, Overlay.Static, "shineLight", offset_dict)
        # Fungi Time of Day
        writeFloat(ROM_COPY, 0x80748280, Overlay.Static, 0, offset_dict)
        writeFloat(ROM_COPY, 0x80748284, Overlay.Static, 0, offset_dict)
        writeFloat(ROM_COPY, 0x80748288, Overlay.Static, 0, offset_dict)
        writeFloat(ROM_COPY, 0x8074828C, Overlay.Static, 0, offset_dict)
        writeFloat(ROM_COPY, 0x80748290, Overlay.Static, 0, offset_dict)
        writeFloat(ROM_COPY, 0x80748294, Overlay.Static, 0, offset_dict)
        # Troff n Scoff
        writeFloat(ROM_COPY, 0x8075B8B4, Overlay.Static, 0, offset_dict)
        writeFloat(ROM_COPY, 0x8075B8B8, Overlay.Static, 0, offset_dict)
        # Rain
        writeValue(ROM_COPY, 0x8068B6AE, Overlay.Static, 0, offset_dict)
        # Isles
        writeValue(ROM_COPY, 0x8068B518, Overlay.Static, 0, offset_dict, 4)
        # Disable some lights
        writeValue(ROM_COPY, 0x8065F1A0, Overlay.Static, 0xA1600000, offset_dict, 4)
        if is_dark_world:
            # Main Menu
            writeValue(ROM_COPY, 0x800304E4, Overlay.Menu, 0, offset_dict, 4)
    if is_sky or is_memory_challenge:
        writeFunction(ROM_COPY, 0x80656538, Overlay.Static, "displayNoGeoChunk", offset_dict)
        writeFunction(ROM_COPY, 0x806562C0, Overlay.Static, "displayNoGeoChunk", offset_dict)
        writeFunction(ROM_COPY, 0x80656380, Overlay.Static, "displayNoGeoChunk", offset_dict)
        writeFunction(ROM_COPY, 0x806565F8, Overlay.Static, "displayNoGeoChunk", offset_dict)

    if settings.medal_cb_req > 0:
        writeValue(ROM_COPY, 0x806F934E, Overlay.Static, settings.medal_cb_req, offset_dict)  # Acquisition
        writeValue(ROM_COPY, 0x806F935A, Overlay.Static, settings.medal_cb_req, offset_dict)  # Acquisition
        writeValue(ROM_COPY, 0x806AA942, Overlay.Static, settings.medal_cb_req, offset_dict)  # Pause Menu Tick

    if settings.fungi_time_internal == FungiTimeSetting.dusk:
        writeValue(ROM_COPY, 0x806C5614, Overlay.Static, 0x50000006, offset_dict, 4)
        writeValue(ROM_COPY, 0x806BE8F8, Overlay.Static, 0x50000008, offset_dict, 4)

    if settings.enable_tag_anywhere:
        writeValue(ROM_COPY, 0x806F6D94, Overlay.Static, 0, offset_dict, 4)  # Prevent delayed collection
        writeValue(ROM_COPY, 0x806F5B68, Overlay.Static, 0x1000, offset_dict)  # Standard Ammo
        writeValue(ROM_COPY, 0x806F59A8, Overlay.Static, 0x1000, offset_dict)  # Bunch
        writeValue(ROM_COPY, 0x806F6CAC, Overlay.Static, 0x9204001A, offset_dict, 4)  # LBU $a0, 0x1A ($s0)
        writeValue(ROM_COPY, 0x806F6CB0, Overlay.Static, 0x86060002, offset_dict, 4)  # LH $a2, 0x2 ($s0)
        writeValue(ROM_COPY, 0x806F53AC, Overlay.Static, 0, offset_dict, 4)  # Prevent LZ case
        writeValue(ROM_COPY, 0x806C7088, Overlay.Static, 0x1000, offset_dict)  # Mech fish dying

    if settings.puzzle_rando_difficulty != PuzzleRando.off:
        # Alter diddy R&D
        diddy_rnd_code_writes = [
            # Code 0: 4231
            0x8064E06A,
            0x8064E066,
            0x8064E062,
            0x8064E05E,
            # Code 1: 3124
            0x8064E046,
            0x8064E042,
            0x8064E03E,
            0x8064E00E,
            # Code 2: 1342
            0x8064E026,
            0x8064E022,
            0x8064E01E,
            0x8064E01A,
        ]
        for code_index, code in enumerate(settings.diddy_rnd_doors):
            for sub_index, item in enumerate(code):
                writeValue(ROM_COPY, diddy_rnd_code_writes[(4 * code_index) + sub_index], Overlay.Static, item + 1, offset_dict)

        # DK Face Puzzle
        dk_face_puzzle_register_values = [0x80, 0x95, 0x83, 0x82]  # 0 = r0, 1 = s5, 2 = v1, 3 = v0
        dk_face_puzzle_addresses = [
            0x8064AD11,
            0x8064AD15,
            0x8064AD01,
            0x8064AD19,
            0x8064AD1D,
            0x8064AD05,
            0x8064AD21,
            0x8064AD09,
            0x8064AD29,
        ]
        for index, address in enumerate(dk_face_puzzle_addresses):
            if spoiler.dk_face_puzzle[index] is not None:
                reg_value = dk_face_puzzle_register_values[spoiler.dk_face_puzzle[index]]
                writeValue(ROM_COPY, address, Overlay.Static, reg_value, offset_dict, 1)

        # Chunky Face Puzzle
        chunky_face_puzzle_register_values = [0x40, 0x54, 0x48, 0x44]  # 0 = r0, 1 = s4, 2 = t0, 3 = a0
        chunky_face_puzzle_addresses = [
            0x8064A2ED,
            0x8064A2F1,
            0x8064A2D5,
            0x8064A2F5,
            0x8064A2F9,
            0x8064A2FD,
            0x8064A2DD,
            0x8064A301,
            0x8064A305,
        ]
        for index, address in enumerate(chunky_face_puzzle_addresses):
            if spoiler.chunky_face_puzzle[index] is not None:
                reg_value = chunky_face_puzzle_register_values[spoiler.chunky_face_puzzle[index]]
                writeValue(ROM_COPY, address, Overlay.Static, reg_value, offset_dict, 1)

        for index, value in enumerate(spoiler.arcade_order):
            writeValue(ROM_COPY, 0x8004A788 + index, Overlay.Arcade, value, offset_dict, 1)

    if isQoLEnabled(spoiler, MiscChangesSelected.fast_picture_taking):
        # Fast Camera Photo
        writeValue(ROM_COPY, 0x80699454, Overlay.Static, 0x5000, offset_dict)  # Fast tick/no mega-slowdown on Biz
        writeValue(ROM_COPY, 0x806992B6, Overlay.Static, 0x14, offset_dict)  # No wait for camera film development
        writeValue(ROM_COPY, 0x8069932A, Overlay.Static, 0x14, offset_dict)
    if isQoLEnabled(spoiler, MiscChangesSelected.lowered_aztec_lobby_bonus):
        # Lower Aztec Lobby Bonus
        writeValue(ROM_COPY, 0x80680D56, Overlay.Static, 0x7C, offset_dict)  # 0x89 if this needs to be unreachable without PTT
    if isQoLEnabled(spoiler, MiscChangesSelected.small_bananas_always_visible):
        writeValue(ROM_COPY, 0x806324D4, Overlay.Static, 0x24020001, offset_dict, 4)  # ADDIU $v0, $r0, 1. Disable kong flag check
        writeValue(ROM_COPY, 0x806A78C4, Overlay.Static, 0, offset_dict, 4)  # NOP. Disable kong flag check
    if isQoLEnabled(spoiler, MiscChangesSelected.fast_hints):
        writeValue(ROM_COPY, 0x8069E0F6, Overlay.Static, 1, offset_dict)
        writeValue(ROM_COPY, 0x8069E112, Overlay.Static, 1, offset_dict)
        writeValue(ROM_COPY, 0x80758BC9, Overlay.Static, 0xAE, offset_dict, 1)  # Quadruple Growth Speed (8E -> AE)
        writeValue(ROM_COPY, 0x80758BD1, Overlay.Static, 0xAE, offset_dict, 1)  # Quadruple Shrink Speed (8E -> AE)
        writeFunction(ROM_COPY, 0x806A5C30, Overlay.Static, "quickWrinklyTextboxes", offset_dict)
    writeFunction(ROM_COPY, 0x80713258, Overlay.Static, "skipDKTV", offset_dict)
    if isQoLEnabled(spoiler, MiscChangesSelected.fast_boot):
        # Remove DKTV - Game Over
        writeValue(ROM_COPY, 0x8071319E, Overlay.Static, 0x50, offset_dict)
        writeValue(ROM_COPY, 0x807131AA, Overlay.Static, 5, offset_dict)
        # Remove DKTV - End Seq
        writeValue(ROM_COPY, 0x8071401E, Overlay.Static, 0x50, offset_dict)
        writeValue(ROM_COPY, 0x8071404E, Overlay.Static, 5, offset_dict)
    # Set NFR song to unused coin pickup, which is replaced by the windows 95 theme
    writeValue(ROM_COPY, 0x80745D20, Overlay.Static, 7, offset_dict, 1)
    for index, kong in enumerate(settings.kutout_kongs):
        writeValue(ROM_COPY, 0x80035B44 + index, Overlay.Boss, kong, offset_dict, 1)
    if isQoLEnabled(spoiler, MiscChangesSelected.fast_transform_animation):
        writeValue(ROM_COPY, 0x8067EAB2, Overlay.Static, 1, offset_dict)  # OSprint
        writeValue(ROM_COPY, 0x8067EAC6, Overlay.Static, 1, offset_dict)  # HC Dogadon 2
        writeValue(ROM_COPY, 0x8067EACA, Overlay.Static, 1, offset_dict)  # Others
        writeValue(ROM_COPY, 0x8067EA92, Overlay.Static, 1, offset_dict)  # Others 2
        writeValue(ROM_COPY, 0x80681F06, Overlay.Static, 1, offset_dict)  # Rocketbarrel
    if isQoLEnabled(spoiler, MiscChangesSelected.animal_buddies_grab_items):
        # Transformations can pick up other's collectables
        writeValue(ROM_COPY, 0x806F6330, Overlay.Static, 0x96AC036E, offset_dict, 4)  # Collection
        # Collection
        writeValue(ROM_COPY, 0x806F68A0, Overlay.Static, 0x95B8036E, offset_dict, 4)  # DK Collection
        writeValue(ROM_COPY, 0x806F68DC, Overlay.Static, 0x952C036E, offset_dict, 4)  # Diddy Collection
        writeValue(ROM_COPY, 0x806F6914, Overlay.Static, 0x95F9036E, offset_dict, 4)  # Tiny Collection
        writeValue(ROM_COPY, 0x806F694C, Overlay.Static, 0x95AE036E, offset_dict, 4)  # Lanky Collection
        writeValue(ROM_COPY, 0x806F6984, Overlay.Static, 0x952B036E, offset_dict, 4)  # Chunky Collection
        # Opacity
        writeValue(ROM_COPY, 0x80637998, Overlay.Static, 0x95B9036E, offset_dict, 4)  # DK Opacity
        writeValue(ROM_COPY, 0x806379E8, Overlay.Static, 0x95CF036E, offset_dict, 4)  # Diddy Opacity
        writeValue(ROM_COPY, 0x80637A28, Overlay.Static, 0x9589036E, offset_dict, 4)  # Tiny Opacity
        writeValue(ROM_COPY, 0x80637A68, Overlay.Static, 0x954B036E, offset_dict, 4)  # Chunky Opacity
        writeValue(ROM_COPY, 0x80637AA8, Overlay.Static, 0x9708036E, offset_dict, 4)  # Lanky Opacity
        # CB/Coin rendering
        writeValue(ROM_COPY, 0x806394FC, Overlay.Static, 0x958B036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639540, Overlay.Static, 0x9728036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639584, Overlay.Static, 0x95AE036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639430, Overlay.Static, 0x95CD036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x806393EC, Overlay.Static, 0x9519036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x806395C8, Overlay.Static, 0x952A036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x8063960C, Overlay.Static, 0x95F8036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639474, Overlay.Static, 0x9549036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x806393A8, Overlay.Static, 0x956C036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x806394B8, Overlay.Static, 0x970F036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639650, Overlay.Static, 0x956C036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639710, Overlay.Static, 0x9549036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639750, Overlay.Static, 0x970F036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x806396D0, Overlay.Static, 0x95CD036E, offset_dict, 4)  # Rendering
        writeValue(ROM_COPY, 0x80639690, Overlay.Static, 0x9519036E, offset_dict, 4)  # Rendering
    if isQoLEnabled(spoiler, MiscChangesSelected.reduced_lag):
        writeValue(ROM_COPY, 0x80748010, Overlay.Static, 0x8064F2F0, offset_dict, 4)  # Cancel Sandstorm
        # No Rain
        writeFloat(ROM_COPY, 0x8075E3E0, Overlay.Static, 0, offset_dict)  # Set Isles Rain Radius to 0
        writeValue(ROM_COPY, 0x8068AF90, Overlay.Static, 0, offset_dict, 4)  # Disable weather
    if isQoLEnabled(spoiler, MiscChangesSelected.homing_balloons):
        writeValue(ROM_COPY, 0x80694F6A, Overlay.Static, 10, offset_dict)  # Coconut
        writeValue(ROM_COPY, 0x80692B82, Overlay.Static, 10, offset_dict)  # Peanuts
        writeValue(ROM_COPY, 0x8069309A, Overlay.Static, 10, offset_dict)  # Grape
        writeValue(ROM_COPY, 0x80695406, Overlay.Static, 10, offset_dict)  # Feather
        writeValue(ROM_COPY, 0x80694706, Overlay.Static, 10, offset_dict)  # Pineapple
    if isQoLEnabled(spoiler, MiscChangesSelected.better_fairy_camera):
        # Increased range for fairy shots
        screen_x_center = 160
        screen_y_center = 120
        screen_x_dist = 24  # Usually 16
        screen_y_dist = 24  # Usually 16
        fairy_range = 1000
        writeValue(ROM_COPY, 0x806C5DB6, Overlay.Static, screen_x_center - screen_x_dist, offset_dict)  # X Minimum
        writeValue(ROM_COPY, 0x806C5DC6, Overlay.Static, screen_x_center + screen_x_dist, offset_dict)  # X Maximum
        writeValue(ROM_COPY, 0x806C5DD6, Overlay.Static, screen_y_center - screen_y_dist, offset_dict)  # Y Minimum
        writeValue(ROM_COPY, 0x806C5DDE, Overlay.Static, screen_y_center + screen_y_dist, offset_dict)  # Y Maximum
        writeValue(ROM_COPY, 0x806C5DE8, Overlay.Static, 0x240B0000 | fairy_range, offset_dict, 4)  # Force max acceptable dist to 1000
    writeValue(ROM_COPY, 0x80032096, Overlay.Arcade, 0, offset_dict)  # Disable Nin 1981 flicker
    writeValue(ROM_COPY, 0x8002672A, Overlay.Arcade, 0xFFFF, offset_dict)  # Disable Donkey Kong logo title flicker
    if isQoLEnabled(spoiler, MiscChangesSelected.vanilla_bug_fixes):
        # Race Hoop 3D
        writeValue(ROM_COPY, 0x806C4DB4, Overlay.Static, 0x24050113, offset_dict, 4)  # Change model of race hoop
        writeValue(ROM_COPY, ACTOR_MASTER_TYPE_START + 24, Overlay.Custom, 2, offset_dict, 1)  # Change race hoop to interpret as 3D Model
        race_hoop_addresses = [0x8069B060, 0x8069B08C, 0x8069B0AC, 0x8069B0B4, 0x8069B0BC, 0x8069B0C8, 0x8069B050, 0x8069B05C]
        for addr in race_hoop_addresses:
            writeValue(ROM_COPY, addr, Overlay.Static, 0, offset_dict, 4)
        # Fix K Rool Cutscene Bug
        writeValue(ROM_COPY, 0x800359A6, Overlay.Boss, 3, offset_dict)
        writeFunction(ROM_COPY, 0x806BE8D8, Overlay.Static, "RabbitRaceInfiniteCode", offset_dict)  # Modify Function Call
        writeFunction(ROM_COPY, 0x8067C168, Overlay.Static, "fixDilloTNTPads", offset_dict)  # Modify Function Call
        writeFunction(ROM_COPY, 0x806E5C04, Overlay.Static, "fixCrownEntrySKong", offset_dict)  # Modify Function Call
        writeFloat(ROM_COPY, 0x807482A4, Overlay.Static, 0.1, offset_dict)  # Increase Fungi lighting transition rate
        # Race Hoop
        writeFunction(ROM_COPY, 0x8069B13C, Overlay.Static, "renderHoop", offset_dict)
        writeFunction(ROM_COPY, 0x8069B0EC, Overlay.Static, "fixRaceHoopCode", offset_dict)
        # Squawks w/ Spotlight Behavior
        writeValue(ROM_COPY, 0x806C6BAE, Overlay.Static, 0, offset_dict)
        # Feathers are sprites
        writeValue(ROM_COPY, ACTOR_DEF_START + (24 * 0x30) + 2, Overlay.Custom, 0, offset_dict)  # Model
        writeValue(ROM_COPY, ACTOR_MASTER_TYPE_START + 43, Overlay.Custom, 4, offset_dict, 1)  # Master Type
        writeFloat(ROM_COPY, 0x80753E38, Overlay.Static, 350, offset_dict)  # Speed
        updateActorFunction(ROM_COPY, 43, "OrangeGunCode")
        # Fix gun slide (kinda)
        writeValue(ROM_COPY, 0x80751A2C, Overlay.Static, 0x806E2F3C, offset_dict, 4)  # Make it so that you can use Z to enter aim
        # Flags
        file_init_flags.append(0x309)  # Cranky FTT

    writeLabelValue(ROM_COPY, 0x80748014, Overlay.Static, "spawnWrinklyWrapper", offset_dict)  # Change function to include setFlag call
    updateActorFunctionInt(ROM_COPY, 212, 0x806AD54C)  # Set Gold Beaver as Blue Beaver Code
    writeLabelValue(ROM_COPY, 0x80748064, Overlay.Static, "change_object_scripts", offset_dict)  # Object Instance Scripts

    writeFunction(ROM_COPY, 0x806A8844, Overlay.Static, "helmTime_restart", offset_dict)  # Modify Function Call
    writeFunction(ROM_COPY, 0x806A89E8, Overlay.Static, "helmTime_exitBonus", offset_dict)  # Modify Function Call
    writeFunction(ROM_COPY, 0x806A89F8, Overlay.Static, "helmTime_exitRace", offset_dict)  # Modify Function Call
    writeFunction(ROM_COPY, 0x806A89C4, Overlay.Static, "helmTime_exitLevel", offset_dict)  # Modify Function Call
    writeFunction(ROM_COPY, 0x806A89B4, Overlay.Static, "helmTime_exitBoss", offset_dict)  # Modify Function Call
    writeFunction(ROM_COPY, 0x806A8988, Overlay.Static, "helmTime_exitKRool", offset_dict)  # Modify Function Call
    if isQoLEnabled(spoiler, MiscChangesSelected.hint_textbox_hold):
        writeHook(ROM_COPY, 0x8070E83C, Overlay.Static, "TextHandler", offset_dict)
    if isQoLEnabled(spoiler, MiscChangesSelected.brighten_mad_maze_maul_enemies):
        writeHook(ROM_COPY, 0x80631380, Overlay.Static, "brightenMMMEnemies", offset_dict)
    if isQoLEnabled(spoiler, MiscChangesSelected.global_instrument):
        writeValue(ROM_COPY, 0x8060DC04, Overlay.Static, 0, offset_dict, 4)  # nop out
        writeFunction(ROM_COPY, 0x8060DB50, Overlay.Static, "newInstrumentRefill", offset_dict)  # New code to set the instrument refill count
        writeFunction(ROM_COPY, 0x806AA728, Overlay.Static, "QoL_DisplayInstrument", offset_dict)  # display number on pause menu
        writeValue(ROM_COPY, 0x806F891C, Overlay.Static, 0x27D502FE, offset_dict, 4)  # addiu $s5, $s8, 0x2FE - Infinite Instrument Energy
        writeValue(ROM_COPY, 0x806F8934, Overlay.Static, 0xA7C202FE, offset_dict, 4)  # sh $v0, 0x2FE ($fp) - Store item count pointer
        writeFunction(ROM_COPY, 0x806A7DD4, Overlay.Static, "getInstrumentRefillCount", offset_dict)  # Correct refill instruction - Headphones
        writeFunction(ROM_COPY, 0x806F92B8, Overlay.Static, "correctRefillCap", offset_dict)  # Correct refill instruction - changeCollectable
        writeValue(ROM_COPY, 0x806A7C04, Overlay.Static, 0x00A0C025, offset_dict, 4)  # or $t8, $a1, $zero
        updateActorFunction(ROM_COPY, 128, "HeadphonesCodeContainer")
    if isQoLEnabled(spoiler, MiscChangesSelected.remove_extraneous_cutscenes):
        # K. Lumsy
        writeValue(ROM_COPY, 0x80750680, Overlay.Static, 0x22, offset_dict)
        writeValue(ROM_COPY, 0x80750682, Overlay.Static, 0x1, offset_dict)
        writeFunction(ROM_COPY, 0x806BDC24, Overlay.Static, "initiateTransition", offset_dict)  # Change takeoff warp func
        writeValue(ROM_COPY, 0x806BDC8C, Overlay.Static, 0x1000, offset_dict)  # Apply no cutscene to all keys
        writeValue(ROM_COPY, 0x806BDC3C, Overlay.Static, 0x1000, offset_dict)  # Apply shorter timer to all keys
        # Fast Vulture
        writeFunction(ROM_COPY, 0x806C50BC, Overlay.Static, "clearVultureCutscene", offset_dict)  # Modify Function Call
        # Speedy T&S Turn-Ins
        writeValue(ROM_COPY, 0x806BE3E0, Overlay.Static, 0, offset_dict, 4)  # NOP
        # Remove final mermaid text
        writeValue(ROM_COPY, 0x806C3E10, Overlay.Static, 0, offset_dict, 4)
        writeValue(ROM_COPY, 0x806C3E20, Overlay.Static, 0, offset_dict, 4)
        # Cutscene FTT Flags
        file_init_flags.extend(
            [
                0x163,  # FLAG_FTT_BANANAPORT,
                0x166,  # FLAG_FTT_CROWNPAD,
                0x168,  # FLAG_FTT_MINIMONKEY,
                0x169,  # FLAG_FTT_HUNKYCHUNKY,
                0x16A,  # FLAG_FTT_ORANGSPRINT,
                0x16B,  # FLAG_FTT_STRONGKONG,
                0x16C,  # FLAG_FTT_RAINBOWCOIN,
                0x16D,  # FLAG_FTT_RAMBI,
                0x16E,  # FLAG_FTT_ENGUARDE,
                0x16F,  # FLAG_FTT_DIDDY,
                0x170,  # FLAG_FTT_LANKY,
                0x171,  # FLAG_FTT_TINY,
                0x172,  # FLAG_FTT_CHUNKY,
                0x174,  # FLAG_FTT_SNIDE,
                0x178,  # FLAG_FTT_WRINKLY,
                0x307,  # FLAG_FTT_FUNKY,
                0x308,  # FLAG_FTT_SNIDE0,
                0x309,  # FLAG_FTT_CRANKY,
                0x30A,  # FLAG_FTT_CANDY,
                0x30B,  # FLAG_FTT_JAPES,
                0x313,  # FLAG_FTT_AZTEC,
                0x30C,  # FLAG_FTT_FACTORY,
                0x30D,  # FLAG_FTT_GALLEON,
                0x30E,  # FLAG_FTT_FUNGI,
                0x30F,  # FLAG_FTT_CAVES,
                0x310,  # FLAG_FTT_CASTLE,
                0x312,  # FLAG_FTT_HELM,
                0x11A,  # FLAG_INTRO_CAVES,
                0xC2,  # FLAG_INTRO_GALLEON,
                0x100,  # FLAG_FTT_TIMESWITCH,
                0x101,  # FLAG_INTRO_FUNGI,
                0x12F,  # FLAG_FTT_DK5DI,
                0x15D,  # FLAG_INTRO_CASTLE,
                0x2A,  # FLAG_CUTSCENE_DIDDYHELPME,
                0x1B,  # FLAG_INTRO_JAPES,
                0x5F,  # FLAG_INTRO_AZTEC,
                0x5D,  # FLAG_CUTSCENE_LANKYHELPME,
                0x5E,  # FLAG_CUTSCENE_TINYHELPME,
                0x8C,  # FLAG_INTRO_FACTORY,
                0xC3,  # FLAG_CUTSCENE_WATERRAISED,
                0xC4,  # FLAG_CUTSCENE_WATERLOWERED,
                0xFF,  # FLAG_CUTSCENE_CLOCK,
                0x115,  # FLAG_CUTSCENE_ROTATING,
                0x12B,  # FLAG_CUTSCENE_KOSHA,
                0x17A,  # FLAG_WATERFALL,
                0x5C,  # FLAG_CUTSCENE_LLAMA,
                0x305,  # FLAG_WARP_HELM_W1_NEAR
            ]
        )

    # Actor Expansion
    # Definitions
    actor_def_hi = getHiSym("actor_defs")
    actor_def_lo = getLoSym("actor_defs")
    writeValue(ROM_COPY, 0x8068926A, Overlay.Static, actor_def_hi, offset_dict)
    writeValue(ROM_COPY, 0x8068927A, Overlay.Static, actor_def_lo, offset_dict)
    writeValue(ROM_COPY, 0x806892D2, Overlay.Static, actor_def_hi, offset_dict)
    writeValue(ROM_COPY, 0x806892D6, Overlay.Static, actor_def_lo, offset_dict)
    writeValue(ROM_COPY, 0x8068945A, Overlay.Static, actor_def_hi, offset_dict)
    writeValue(ROM_COPY, 0x80689466, Overlay.Static, actor_def_lo, offset_dict)
    def_limit = getVar("DEFS_LIMIT")
    writeValue(ROM_COPY, 0x8068928A, Overlay.Static, def_limit, offset_dict)
    writeValue(ROM_COPY, 0x80689452, Overlay.Static, def_limit, offset_dict)
    # Functions
    actor_function_hi = getHiSym("actor_functions")
    actor_function_lo = getLoSym("actor_functions")
    writeValue(ROM_COPY, 0x806788F2, Overlay.Static, actor_function_hi, offset_dict)
    writeValue(ROM_COPY, 0x8067890E, Overlay.Static, actor_function_lo, offset_dict)
    writeValue(ROM_COPY, 0x80678A3E, Overlay.Static, actor_function_hi, offset_dict)
    writeValue(ROM_COPY, 0x80678A52, Overlay.Static, actor_function_lo, offset_dict)
    # writeLabelValue(ROM_COPY, 0x8076152C, Overlay.Static, "actor_functions", offset_dict)
    # writeLabelValue(ROM_COPY, 0x80764768, Overlay.Static, "actor_functions", offset_dict)
    # Collision
    actor_col_hi_info = getHi(ACTOR_COLLISION_START + 0)
    actor_col_lo_info = getLo(ACTOR_COLLISION_START + 0)
    actor_col_hi_unk4 = getHi(ACTOR_COLLISION_START + 4)
    actor_col_lo_unk4 = getLo(ACTOR_COLLISION_START + 4)
    writeValue(ROM_COPY, 0x8067586A, Overlay.Static, actor_col_hi_info, offset_dict)
    writeValue(ROM_COPY, 0x80675876, Overlay.Static, actor_col_lo_info, offset_dict)
    writeValue(ROM_COPY, 0x806759F2, Overlay.Static, actor_col_hi_unk4, offset_dict)
    writeValue(ROM_COPY, 0x80675A02, Overlay.Static, actor_col_lo_unk4, offset_dict)
    writeValue(ROM_COPY, 0x8067620E, Overlay.Static, actor_col_hi_unk4, offset_dict)
    writeValue(ROM_COPY, 0x8067621E, Overlay.Static, actor_col_lo_unk4, offset_dict)
    # Health
    actor_health_hi_health = getHi(ACTOR_HEALTH_START + 0)
    actor_health_lo_health = getLo(ACTOR_HEALTH_START + 0)
    actor_health_hi_dmg = getHi(ACTOR_HEALTH_START + 2)
    actor_health_lo_dmg = getLo(ACTOR_HEALTH_START + 2)
    writeValue(ROM_COPY, 0x806761D6, Overlay.Static, actor_health_hi_health, offset_dict)
    writeValue(ROM_COPY, 0x806761E2, Overlay.Static, actor_health_lo_health, offset_dict)
    writeValue(ROM_COPY, 0x806761F2, Overlay.Static, actor_health_hi_dmg, offset_dict)
    writeValue(ROM_COPY, 0x806761FE, Overlay.Static, actor_health_lo_dmg, offset_dict)
    # Interactions
    actor_interaction_hi = getHiSym("actor_interactions")
    actor_interaction_lo = getLoSym("actor_interactions")
    writeValue(ROM_COPY, 0x806781BA, Overlay.Static, actor_interaction_hi, offset_dict)
    writeValue(ROM_COPY, 0x8067820A, Overlay.Static, actor_interaction_lo, offset_dict)
    writeValue(ROM_COPY, 0x8067ACCA, Overlay.Static, actor_interaction_hi, offset_dict)
    writeValue(ROM_COPY, 0x8067ACDA, Overlay.Static, actor_interaction_lo, offset_dict)
    # Master Type
    actor_mtype_hi = getHiSym("actor_master_types")
    actor_mtype_lo = getLoSym("actor_master_types")
    writeValue(ROM_COPY, 0x80677EF6, Overlay.Static, actor_mtype_hi, offset_dict)
    writeValue(ROM_COPY, 0x80677F02, Overlay.Static, actor_mtype_lo, offset_dict)
    writeValue(ROM_COPY, 0x80677FCA, Overlay.Static, actor_mtype_hi, offset_dict)
    writeValue(ROM_COPY, 0x80677FD2, Overlay.Static, actor_mtype_lo, offset_dict)
    writeValue(ROM_COPY, 0x80678CDA, Overlay.Static, actor_mtype_hi, offset_dict)
    writeValue(ROM_COPY, 0x80678CE6, Overlay.Static, actor_mtype_lo, offset_dict)
    # Paad
    writeValue(ROM_COPY, 0x8067805E, Overlay.Static, getHiSym("actor_extra_data_sizes"), offset_dict)
    writeValue(ROM_COPY, 0x80678062, Overlay.Static, getLoSym("actor_extra_data_sizes"), offset_dict)

    # Uncontrollable Fixes
    writeFunction(ROM_COPY, 0x806F56E0, Overlay.Static, "getFlagIndex_Corrected", offset_dict)  # BP Acquisition - Correct for character
    writeFunction(ROM_COPY, 0x806F9374, Overlay.Static, "getFlagIndex_MedalCorrected", offset_dict)  # Medal Acquisition - Correct for character
    # Inverted Controls Option
    writeValue(ROM_COPY, 0x8060D04C, Overlay.Static, 0x1000, offset_dict)  # Prevent inverted controls overwrite
    # Disable Sprint Music in Fungi Forest
    writeFunction(ROM_COPY, 0x8067F3DC, Overlay.Static, "playTransformationSong", offset_dict)
    # GetOut Timer
    writeValue(ROM_COPY, 0x806B7ECA, Overlay.Static, 125, offset_dict)  # 0x8078 for center-bottom ms timer
    # Fix Tag Barrel Background Kong memes
    writeFunction(ROM_COPY, 0x806839F0, Overlay.Static, "tagBarrelBackgroundKong", offset_dict)
    # Better Collision
    writeFunction(ROM_COPY, 0x806F6618, Overlay.Static, "checkModelTwoItemCollision", offset_dict)
    writeFunction(ROM_COPY, 0x806F662C, Overlay.Static, "checkModelTwoItemCollision", offset_dict)
    # Dive Check
    writeFunction(ROM_COPY, 0x806E9658, Overlay.Static, "CanDive_WithCheck", offset_dict)
    writeFunction(ROM_COPY, 0x806DEFDC, Overlay.Static, "dropWrapper", offset_dict)
    # Prevent Japes Dillo Cutscene for the key acquisition
    writeValue(ROM_COPY, 0x806EFCEC, Overlay.Static, 0x1000, offset_dict)
    # Make getting out of spider traps easier on controllers
    writeLabelValue(ROM_COPY, 0x80752ADC, Overlay.Static, "exitTrapBubbleController", offset_dict)
    # Inverted Controls Option
    writeValue(ROM_COPY, 0x8060D01A, Overlay.Static, getHiSym("InvertedControls"), offset_dict)  # Change language store to inverted controls store
    writeValue(ROM_COPY, 0x8060D01E, Overlay.Static, getLoSym("InvertedControls"), offset_dict)  # Change language store to inverted controls store

    writeFunction(ROM_COPY, 0x80602AB0, Overlay.Static, "filterSong", offset_dict)
    writeValue(ROM_COPY, 0x80602AAC, Overlay.Static, 0x27A40018, offset_dict, 4)  # addiu $a0, $sp, 0x18I
    # Decompressed Overlays
    overlays_being_decompressed = [
        0x08,  # Cutscenes
        0x09,  # Setup
        0x0A,  # Instance Scripts
        0x0C,  # Text
        0x10,  # Character Spawners
        0x12,  # Loading Zones
        0x18,  # Checkpoints
    ]
    for ovl in overlays_being_decompressed:
        writeValue(ROM_COPY, 0x80748E18 + ovl, Overlay.Static, 0, offset_dict, 1)

    if settings.more_cutscene_skips == ExtraCutsceneSkips.off:
        # Wipe all CS Data
        ROM_COPY.seek(0x1FF3800)
        for x in range(432):
            ROM_COPY.writeMultipleBytes(0, 4)
    else:
        if settings.shuffle_items:
            CUTSCENE_UNSKIPS = [
                {
                    # Diddy Prod Spawn
                    "map_id": Maps.FranticFactory,
                    "cutscene": 2,
                },
                {
                    # Tiny Prod Peek
                    "map_id": Maps.FranticFactory,
                    "cutscene": 3,
                },
                {
                    # Lanky Prod Peek
                    "map_id": Maps.FranticFactory,
                    "cutscene": 4,
                },
                {
                    # Chunky Prod Spawn
                    "map_id": Maps.FranticFactory,
                    "cutscene": 5,
                },
                {
                    # Free Llama
                    "map_id": Maps.AngryAztec,
                    "cutscene": 14,
                },
                {
                    # Tiny Barrel Spawn
                    "map_id": Maps.ForestGiantMushroom,
                    "cutscene": 0,
                },
                {
                    # Cannon GB Spawn
                    "map_id": Maps.ForestGiantMushroom,
                    "cutscene": 1,
                },
                {
                    # Greenhouse Intro
                    "map_id": Maps.CastleGreenhouse,
                    "cutscene": 0,
                },
                {
                    # Dungeon Lanky Trombone Bonus
                    "map_id": Maps.CastleDungeon,
                    "cutscene": 0,
                },
            ]
            for data in CUTSCENE_UNSKIPS:
                map_id = data["map_id"]
                cutscene = data["cutscene"]
                shift = cutscene & 0x1F
                offset = 0 if cutscene < 32 else 1
                comp = 0xFFFFFFFF - (1 << shift)
                addr = 0x1FF3800 + (8 * map_id) + (4 * offset)
                ROM_COPY.seek(addr)
                original = int.from_bytes(ROM_COPY.readBytes(4), "big")
                ROM_COPY.seek(addr)
                ROM_COPY.writeMultipleBytes(original & comp, 4)
        writeFunction(ROM_COPY, 0x80628508, Overlay.Static, "renderScreenTransitionCheck", offset_dict)  # Remove transition effects if skipped cutscene
        if settings.more_cutscene_skips == ExtraCutsceneSkips.press:
            writeFunction(ROM_COPY, 0x8061DD80, Overlay.Static, "pressSkipHandler", offset_dict)  # Handler for press start to skip

    # Music Fix
    writeValue(ROM_COPY, 0x807452B0, Overlay.Static, 0xD00, offset_dict, 4)
    writeValue(ROM_COPY, 0x80600DA2, Overlay.Static, 0x38, offset_dict)
    writeValue(ROM_COPY, 0x80600DA6, Overlay.Static, 0x70, offset_dict)

    # Diddy Slam Crash Fix
    writeHook(ROM_COPY, 0x80609338, Overlay.Static, "fixDiddySlamCrash", offset_dict)

    # Fix Null Lag Boost
    writeHook(ROM_COPY, 0x806CCA90, Overlay.Static, "fixNullLagBoost", offset_dict)

    # Adjust Exit File
    writeFunction(ROM_COPY, 0x805FEAE4, Overlay.Static, "loadExits", offset_dict)
    writeHook(ROM_COPY, 0x806C97E0, Overlay.Static, "adjustExitRead", offset_dict)
    writeValue(ROM_COPY, 0x805FF1CC, Overlay.Static, 0x2009FFFF, offset_dict, 4)  # Set default void location to be exit -1 instead of exit 0
    writeValue(ROM_COPY, 0x805FF220, Overlay.Static, 0x87A9, offset_dict)  # Change LHU to LH
    writeValue(ROM_COPY, 0x805FF278, Overlay.Static, 0x87A9, offset_dict)  # Change LHU to LH
    writeValue(ROM_COPY, 0x805FF2D0, Overlay.Static, 0x87A9, offset_dict)  # Change LHU to LH

    # Boot setup checker optimization
    writeFunction(ROM_COPY, 0x805FEB00, Overlay.Static, "bootSpeedup", offset_dict)  # Modify Function Call
    writeValue(ROM_COPY, 0x805FEB08, Overlay.Static, 0, offset_dict, 4)  # Cancel 2nd check

    # Crowd Control Stuff
    writeFunction(ROM_COPY, 0x805FEDC8, Overlay.Static, "handleGamemodeWrapper", offset_dict)  # disable skipping the rap
    writeFloat(ROM_COPY, 0x8075EB4C, Overlay.Static, -2.5, offset_dict)  # Have the initial moonkick accel reading from a "const" addr
    writeValue(ROM_COPY, 0x806EB618, Overlay.Static, 0x3C018076, offset_dict, 4)  # LUI $at, 0x8076
    writeValue(ROM_COPY, 0x806EB61C, Overlay.Static, 0xC426EB4C, offset_dict, 4)  # LWC1 $f6, 0xEB4C ($at)
    writeFunction(ROM_COPY, 0x806CA7D4, Overlay.Static, "fakeGetOut", offset_dict)

    # Golden Banana Requirements
    order = 0
    for count in settings.BLockerEntryCount:
        ROM_COPY.seek(settings.rom_data + 0x17E + order)
        ROM_COPY.writeMultipleBytes(int(settings.BLockerEntryItems[order]), 1)
        writeValue(ROM_COPY, 0x807446D0 + (2 * order), Overlay.Static, count, offset_dict)
        order += 1

    # Jetpac Requirement
    written_requirement = settings.medal_requirement
    if written_requirement != 15:
        if written_requirement < 0:
            written_requirement = 0
        elif written_requirement > 40:
            written_requirement = 40
        writeValue(ROM_COPY, 0x80026513, Overlay.Menu, written_requirement, offset_dict, 1)  # Actual requirement
        writeValue(ROM_COPY, 0x8002644B, Overlay.Menu, written_requirement, offset_dict, 1)  # Text variable
        writeValue(ROM_COPY, 0x80027583, Overlay.Menu, written_requirement, offset_dict, 1)  # Text Variable

    # Boss Key Mapping
    for i in range(7):
        for j in range(7):
            if REGULAR_BOSS_MAPS[i] == settings.boss_maps[j]:
                writeValue(ROM_COPY, KEY_FLAG_ADDRESSES[i], Overlay.Boss, NORMAL_KEY_FLAGS[j], offset_dict)

    # Race Coin Requirements
    race_offset_data = {
        Maps.CavesLankyRace: [0x800247C2],
        Maps.AztecTinyRace: [0x800247DA],
        Maps.FactoryTinyRace: [0x800285A2, 0x8002888E, 0x80028A0A],
        Maps.GalleonSealRace: [0x8002A232, 0x8002A08E],
        Maps.CastleTinyRace: [0x8002BAB6, 0x8002B6D6],
        Maps.JapesMinecarts: [0x806C4912],
        Maps.ForestMinecarts: [0x806C4956],
        Maps.CastleMinecarts: [0x806C499A],
    }
    static_overlay_races = [Maps.JapesMinecarts, Maps.ForestMinecarts, Maps.CastleMinecarts]
    for map_id in race_offset_data:
        if map_id in spoiler.coin_requirements:
            for addr in race_offset_data[map_id]:
                overlay = Overlay.Static if map_id in static_overlay_races else Overlay.Race
                writeValue(ROM_COPY, addr, overlay, spoiler.coin_requirements[map_id], offset_dict)

    # BFI
    writeFunction(ROM_COPY, 0x80028080, Overlay.Critter, "displayBFIMoveText", offset_dict)  # BFI Text Display
    if settings.rareware_gb_fairies > 0:
        writeValue(ROM_COPY, 0x80027E70, Overlay.Critter, 0x2C410000 | settings.rareware_gb_fairies, offset_dict, 4)  # SLTIU $at, $v0, count
        writeValue(ROM_COPY, 0x80027E74, Overlay.Critter, 0x1420, offset_dict)  # BNEZ $at, 0x6
    if settings.win_condition_item == WinConditionComplex.dk_rap_items:
        writeValue(ROM_COPY, 0x8071280E, Overlay.Static, Maps.DKRap, offset_dict)  # End Sequence destination map
        writeValue(ROM_COPY, 0x80712816, Overlay.Static, 0, offset_dict)  # End Sequence cutscene
        writeValue(ROM_COPY, 0x8075E650, Overlay.Static, 0x807141D4, offset_dict, 4)  # Alter jump table entry
        writeValue(ROM_COPY, 0x80712E76, Overlay.Static, 0x1644, offset_dict)  # Demo Fadeout Timer
        # Speed up end sequence a little bit to fit within the confines of the rap
        for index in range(21):
            ROM_COPY.seek(0x1FFF800 + (index * 6))
            duration = int.from_bytes(ROM_COPY.readBytes(2), "big")
            cooldown = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if duration == 0xFFFF and cooldown == 0xFFFF:
                # Terminating card, do not alter values
                break
            else:
                scale_down = 0.8
                ROM_COPY.seek(0x1FFF800 + (index * 6))
                ROM_COPY.writeMultipleBytes(int(duration * scale_down), 2)
                ROM_COPY.writeMultipleBytes(int(cooldown * scale_down), 2)

    # TBarrel/BFI Rewards
    # writeValue(ROM_COPY, 0x80681CE2, Overlay.Static, 0, offset_dict)
    # writeValue(ROM_COPY, 0x80681CFA, Overlay.Static, 1, offset_dict)
    # writeValue(ROM_COPY, 0x80681D06, Overlay.Static, 2, offset_dict)
    # writeValue(ROM_COPY, 0x80681D12, Overlay.Static, 3, offset_dict)
    # writeValue(ROM_COPY, 0x80681C8A, Overlay.Static, 0, offset_dict)
    # writeValue(ROM_COPY, 0x800295F6, Overlay.Critter, 0, offset_dict)
    # writeValue(ROM_COPY, 0x80029606, Overlay.Critter, 1, offset_dict)
    # writeValue(ROM_COPY, 0x800295FE, Overlay.Critter, 3, offset_dict)
    # writeValue(ROM_COPY, 0x800295DA, Overlay.Critter, 2, offset_dict)
    writeValue(ROM_COPY, 0x80027F2A, Overlay.Critter, 4, offset_dict)
    writeValue(ROM_COPY, 0x80027E1A, Overlay.Critter, 4, offset_dict)
    # writeFunction(ROM_COPY, 0x80681D38, Overlay.Static, "getLocationStatus", offset_dict)  # Get TBarrels Move
    # writeFunction(ROM_COPY, 0x80681C98, Overlay.Static, "getLocationStatus", offset_dict)  # Get TBarrels Move
    # writeFunction(ROM_COPY, 0x80029610, Overlay.Critter, "setLocationStatus", offset_dict)  # Set TBarrels Move
    writeFunction(ROM_COPY, 0x80027F24, Overlay.Critter, "setLocationStatus", offset_dict)  # Set BFI Move
    writeFunction(ROM_COPY, 0x80027E20, Overlay.Critter, "getLocationStatus", offset_dict)  # Get BFI Move
    writeValue(ROM_COPY, 0x80681DE4, Overlay.Static, 0x5000, offset_dict)
    writeHook(ROM_COPY, 0x80680AD4, Overlay.Static, "expandTBarrelResponse", offset_dict)  # Allow Training Barrels to disappear if already beaten
    writeValue(ROM_COPY, 0x80681C16, Overlay.Static, 0xF, offset_dict)  # Disregard most special code from a bonus

    writeValue(ROM_COPY, 0x8069215E, Overlay.Static, 0x3F, offset_dict)  # Reduce fireball collision volume

    # Helm Warp Handler
    writeFunction(ROM_COPY, 0x8068B04C, Overlay.Static, "WarpToHelm", offset_dict)
    writeValue(ROM_COPY, 0x8068B054, Overlay.Static, 0x5000, offset_dict)
    writeFunction(ROM_COPY, 0x80640720, Overlay.Static, "portalWarpFix", offset_dict)
    writeValue(ROM_COPY, 0x806406F4, Overlay.Static, 0x2006FFFF, offset_dict, 4)

    writeFunction(ROM_COPY, 0x8064070C, Overlay.Static, "DetermineLevel_NewLevel", offset_dict)
    for index, data in enumerate(settings.level_portal_destinations):
        writeValue(ROM_COPY, 0x8074809C + (2 * index), Overlay.Static, data["map"], offset_dict)
        writeValue(ROM_COPY, 0x807480AC + (2 * index), Overlay.Static, data["exit"], offset_dict, 2, True)
        if data["map"] != Maps.CreepyCastle and data["exit"] != -1:
            writeValue(ROM_COPY, 0x807480BC + (2 * index), Overlay.Static, 0, offset_dict)
    for index, map_id in enumerate(settings.level_void_maps):
        writeValue(ROM_COPY, 0x80744748 + (2 * index), Overlay.Static, map_id, offset_dict)

    # Write Mech Fish entry
    writeValue(ROM_COPY, 0x806C6DC6, Overlay.Static, settings.mech_fish_entrance["map"], offset_dict)
    exit_val = settings.mech_fish_entrance["exit"]
    if exit_val == -1:
        exit_val = 0xFFFF
    writeValue(ROM_COPY, 0x806C6DD0, Overlay.Static, 0x20050000 | exit_val, offset_dict, 4)
    # Misc LZR Stuff
    if settings.shuffle_loading_zones == ShuffleLoadingZones.all and spoiler.shuffled_exit_instructions is not None:
        # K Rool Exit
        krool_exit_map = Maps.Isles
        krool_exit_exit = 12
        writeValue(ROM_COPY, 0x806A8986, Overlay.Static, krool_exit_map, offset_dict)
        writeValue(ROM_COPY, 0x806A898E, Overlay.Static, krool_exit_exit, offset_dict)
        writeValue(ROM_COPY, 0x80628032, Overlay.Static, krool_exit_map, offset_dict)
        writeValue(ROM_COPY, 0x8062803A, Overlay.Static, krool_exit_exit, offset_dict)
        # Race Exits
        exit_data = [
            {
                "race_map": Maps.JapesMinecarts,
                "tied_transition": Transitions.JapesCartsToMain,
            },
            {
                "race_map": Maps.AztecTinyRace,
                "tied_transition": Transitions.AztecRaceToMain,
            },
            {
                "race_map": Maps.FactoryTinyRace,
                "tied_transition": Transitions.FactoryRaceToRandD,
            },
            {
                "race_map": Maps.GalleonSealRace,
                "tied_transition": Transitions.GalleonSealToShipyard,
            },
            {
                "race_map": Maps.ForestMinecarts,
                "tied_transition": Transitions.ForestCartsToMain,
            },
            {
                "race_map": Maps.CavesLankyRace,
                "tied_transition": Transitions.CavesRaceToMain,
            },
            {
                "race_map": Maps.CastleMinecarts,
                "tied_transition": Transitions.CastleCartsToCrypt,
            },
            {
                "race_map": Maps.CastleTinyRace,
                "tied_transition": Transitions.CastleRaceToMuseum,
            },
        ]
        for race_index, race_exit in enumerate(exit_data):
            if race_exit["tied_transition"] in spoiler.shuffled_exit_data:
                address_head = 0x807447A0 + (12 * race_index)
                shuffled_back = spoiler.shuffled_exit_data[race_exit["tied_transition"]]
                writeValue(ROM_COPY, address_head + 0, Overlay.Static, race_exit["race_map"], offset_dict, 4)
                writeValue(ROM_COPY, address_head + 4, Overlay.Static, GetMapId(settings, shuffled_back.regionId), offset_dict, 4)
                writeValue(ROM_COPY, address_head + 8, Overlay.Static, GetExitId(shuffled_back), offset_dict, 4)
        if ENABLE_BLAST_LZR:
            addr_hi = getHiSym("blastWarpHandler")
            addr_lo = getLoSym("blastWarpHandler")
            writeValue(ROM_COPY, 0x806E5A4A, Overlay.Static, addr_hi, offset_dict)
            writeValue(ROM_COPY, 0x806E5A4E, Overlay.Static, addr_lo, offset_dict)

    # Boss Mapping
    for i in range(7):
        boss_map = settings.boss_maps[i]
        boss_kong = settings.boss_kongs[i]
        writeValue(ROM_COPY, 0x80744700 + (i * 2), Overlay.Static, boss_map, offset_dict)
        writeValue(ROM_COPY, 0x807446F0 + i, Overlay.Static, boss_kong, offset_dict, 1)
        writeValue(ROM_COPY, 0x807445E0 + boss_map, Overlay.Static, i, offset_dict, 1)

    writeHook(ROM_COPY, 0x806C3260, Overlay.Static, "fixLankyPhaseHandState", offset_dict)  # Ensures K Rool has a head in the end cutscene if in Lanky Phase
    vanilla_props_values = {
        Maps.JapesBoss: 1,
        Maps.AztecBoss: 1,
        Maps.FactoryBoss: 1,
        Maps.GalleonBoss: 1,
        Maps.FungiBoss: 1,
        Maps.CavesBoss: 1,
        Maps.CastleBoss: 1,
        Maps.KroolDonkeyPhase: 0x23,
        Maps.KroolDiddyPhase: 0x23,
        Maps.KroolLankyPhase: 0x22,
        Maps.KroolTinyPhase: 0x23,
        Maps.KroolShoe: 3,
        Maps.KroolChunkyPhase: 0x23,
    }
    # for map_id in settings.krool_order:
    #     writeValue(ROM_COPY, 0x807445E0 + map_id, Overlay.Static, 8, offset_dict, 1)
    #     if map_id not in [
    #         Maps.KroolDonkeyPhase,
    #         Maps.KroolDiddyPhase,
    #         Maps.KroolLankyPhase,
    #         Maps.KroolTinyPhase,
    #         Maps.KroolChunkyPhase,
    #     ]:
    #         writeValue(ROM_COPY, 0x8074482C + (12 * map_id) + 4, Overlay.Static, 3, offset_dict, 4)
    # Got a bunch of stuff to fix with this
    # for map_id in vanilla_props_values:
    #     new_value = vanilla_props_values[map_id]
    #     if (map_id in settings.krool_order) or (map_id == Maps.KroolShoe and Maps.KroolTinyPhase in settings.krool_order):
    #         new_value |= 0x200  # Deathwarp
    #         new_value |= 0x2  # Is K. Rool
    #     else:
    #         new_value &= 0xFFFFFDFF  # Deathwarp
    #         new_value &= 0xFFFFFFFD  # Not K. Rool
    #     writeValue(ROM_COPY, 0x8074482C + (12 * map_id) + 4, Overlay.Static, new_value, offset_dict, 4)
    # writeValue(ROM_COPY, 0x8071288A, Overlay.Static, 0x200, offset_dict)
    writeFunction(ROM_COPY, 0x80628034, Overlay.Static, "exitBoss", offset_dict)

    boss_complete_functions = [
        0x8002590C,  # Dillo 1
        0x80025C90,  # Dillo 2
        0x8002A108,  # Puff
        0x8002B424,  # Dog 2
        0x8002C154,  # Dog 1
        0x800327FC,  # KKO
        0x80035670,  # MJ
        0x8002DBD0,  # K Rool - DK
        0x8002E718,  # K Rool - Diddy
        0x8002F050,  # K Rool - Lanky
        0x8002FAF4,  # K Rool - Tiny
        0x800319B8,  # K Rool - Chunky
    ]
    for addr in boss_complete_functions:
        writeFunction(ROM_COPY, addr, Overlay.Boss, "completeBoss", offset_dict)

    writeValue(ROM_COPY, 0x80024266, Overlay.Bonus, 1, offset_dict)  # Set Minigame oranges as infinite

    # Adjust Krazy KK Flicker Speeds (Non-ASM)
    # Defaults: 48/30. Start: 60. Flicker Thresh: -30. Scaling: 2.7
    writeValue(ROM_COPY, 0x800293E6, Overlay.Bonus, 130, offset_dict)  # V Easy
    writeValue(ROM_COPY, 0x800293FA, Overlay.Bonus, 130, offset_dict)  # Easy
    writeValue(ROM_COPY, 0x8002940E, Overlay.Bonus, 81, offset_dict)  # Medium
    writeValue(ROM_COPY, 0x80029422, Overlay.Bonus, 81, offset_dict)  # Hard
    writeValue(ROM_COPY, 0x800295D2, Overlay.Bonus, 162, offset_dict)  # Start
    writeValue(ROM_COPY, 0x800297D8, Overlay.Bonus, 0x916B, offset_dict)  # LB -> LBU
    writeValue(ROM_COPY, 0x800297CE, Overlay.Bonus, -81, offset_dict, 2, True)  # Flicker Threshold

    # Change MJ phase reset differential to 40.0f units
    writeValue(ROM_COPY, 0x80033B26, Overlay.Boss, 0x4220, offset_dict)  # Jumping Around
    writeValue(ROM_COPY, 0x800331AA, Overlay.Boss, 0x4220, offset_dict)  # Random Square
    writeValue(ROM_COPY, 0x800339EE, Overlay.Boss, 0x4220, offset_dict)  # Stationary

    if IsItemSelected(settings.hard_bosses, settings.hard_bosses_selected, HardBossesSelected.fast_mad_jack, False):
        # MJ Fast Jumps
        for x in range(5):
            speed = 2 if x == 0 else 3
            writeFloat(ROM_COPY, 0x80036C40 + (4 * x), Overlay.Boss, speed, offset_dict)  # Phase x Jump speed
        writeValue(ROM_COPY, 0x8003343A, Overlay.Boss, 0x224, offset_dict)  # Force fast jumps

    if IsItemSelected(settings.hard_bosses, settings.hard_bosses_selected, HardBossesSelected.k_rool_toes_rando, False):
        # Random Toes
        for x in range(5):
            writeValue(ROM_COPY, 0x80036950 + (4 * x) + 2, Overlay.Boss, settings.toe_order[x], offset_dict, 1)
            writeValue(ROM_COPY, 0x80036968 + (4 * x) + 2, Overlay.Boss, settings.toe_order[x + 5], offset_dict, 1)

    if IsItemSelected(settings.hard_bosses, settings.hard_bosses_selected, HardBossesSelected.beta_lanky_phase, False):
        # Spawn a K Rool balloon into the fight to trigger K Rool
        writeFunction(ROM_COPY, 0x806A7AA8, Overlay.Static, "popExistingBalloon", offset_dict)
        writeFunction(ROM_COPY, 0x8002EB64, Overlay.Boss, "spawnKRoolLankyBalloon", offset_dict)
        addr = 0x8074482C + (12 * Maps.KroolLankyPhase) + 0
        rom_addr = getROMAddress(addr, Overlay.Static, offset_dict)
        ROM_COPY.seek(rom_addr)
        val = int.from_bytes(ROM_COPY.readBytes(4), "big")
        val &= ~0x200  # Re-enables guns
        writeValue(ROM_COPY, addr, Overlay.Static, val, offset_dict, 4)
        if settings.more_cutscene_skips == ExtraCutsceneSkips.auto:
            writeValue(ROM_COPY, 0x8002EC50, Overlay.Boss, 0, offset_dict, 4)
            writeValue(ROM_COPY, 0x8002EC64, Overlay.Boss, 0, offset_dict, 4)
            writeValue(ROM_COPY, 0x8002EC70, Overlay.Boss, 0, offset_dict, 4)
            writeValue(ROM_COPY, 0x8002EC82, Overlay.Boss, 2, offset_dict)
        if POP_TARGETTING:
            PEEL_DURATION = 35  # In seconds. Vanilla is 20
            writeFunction(ROM_COPY, 0x8002ED28, Overlay.Boss, "handleKRoolDirecting", offset_dict)
            writeValue(ROM_COPY, 0x8002E866, Overlay.Boss, PEEL_DURATION * 30, offset_dict)
        # Fixes a bug if someone pops a balloon whilst K Rool has slipped where the hit doesn't count
        writeFunction(ROM_COPY, 0x8002EF40, Overlay.Boss, "incHitCounter", offset_dict)
        writeValue(ROM_COPY, 0x8002EFAC, Overlay.Boss, 0, offset_dict, 4)

    # Training
    writeValue(ROM_COPY, 0x80029610, Overlay.Critter, 0, offset_dict, 4)  # Disable set flag
    writeFunction(ROM_COPY, 0x80029638, Overlay.Critter, "warpOutOfTraining", offset_dict)
    writeValue(ROM_COPY, 0x80029644, Overlay.Critter, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x8002968E, Overlay.Critter, 1, offset_dict)  # Set timer to 1
    # writeValue(ROM_COPY, 0x80029314, Overlay.Critter, 0x2406000A, offset_dict, 4) # Set ticking timer to 10s
    # B. Locker Stuff
    writeValue(ROM_COPY, 0x80027970, Overlay.Critter, 0x1000, offset_dict)  # Prevent Helm Lobby B. Locker requiring Chunky
    writeValue(ROM_COPY, 0x800275E8, Overlay.Critter, 0x1000, offset_dict)  # Prevent checking the cheat stuff
    writeFunction(ROM_COPY, 0x80027570, Overlay.Critter, "displayBlockerItemOnHUD", offset_dict)
    writeFunction(ROM_COPY, 0x800279D0, Overlay.Critter, "getCountOfBlockerRequiredItem", offset_dict)
    writeFunction(ROM_COPY, 0x8002792C, Overlay.Critter, "getCountOfBlockerRequiredItem", offset_dict)
    writeFunction(ROM_COPY, 0x800278EC, Overlay.Critter, "displayCountOnBLockerTeeth", offset_dict)
    writeFunction(ROM_COPY, 0x800275AC, Overlay.Critter, "displayCountOnBLockerTeeth", offset_dict)
    writeHook(ROM_COPY, 0x800275BC, Overlay.Critter, "fixBLockerRange", offset_dict)

    if settings.has_password:
        writeHook(ROM_COPY, 0x80028CC8, Overlay.Menu, "GoToPassword", offset_dict)  # Enables handler of whether to go to the password screen or not
        # Overwrite screen 6 with password data. Used to be multiplayer, but we've jettisoned that
        writeFunction(ROM_COPY, 0x800306AC, Overlay.Menu, "password_screen_gfx", offset_dict)
        writeFunction(ROM_COPY, 0x800306D4, Overlay.Menu, "password_screen_init", offset_dict)
        writeFunction(ROM_COPY, 0x800306C4, Overlay.Menu, "password_screen_code", offset_dict)

    # Menu/Shop Stuff
    # Menu/Shop: Force enable cheats
    writeValue(ROM_COPY, 0x800280DC, Overlay.Menu, 0x1000, offset_dict)  # Force access to mystery menu
    writeValue(ROM_COPY, 0x80028A40, Overlay.Menu, 0x1000, offset_dict)  # Force opaqueness
    writeValue(ROM_COPY, 0x8002EA7C, Overlay.Menu, 0x1000, offset_dict)  # Disable Cutscene Menu
    writeValue(ROM_COPY, 0x8002EAF8, Overlay.Menu, 0x1000, offset_dict)  # Disable Minigames Menu
    writeValue(ROM_COPY, 0x8002EB70, Overlay.Menu, 0x1000, offset_dict)  # Disable Bosses Menu
    writeValue(ROM_COPY, 0x8002EBE8, Overlay.Menu, 0, offset_dict, 4)  # Disable Krusha Menu
    writeValue(ROM_COPY, 0x8002EC18, Overlay.Menu, 0x1000, offset_dict)  # Enable Cheats Menu
    writeValue(ROM_COPY, 0x8002E8D8, Overlay.Menu, 0x240E0004, offset_dict, 4)  # Force cheats menu to start on page 4
    writeValue(ROM_COPY, 0x8002E8F4, Overlay.Menu, 0x1000, offset_dict)  # Disable edge cases
    writeValue(ROM_COPY, 0x8002E074, Overlay.Menu, 0xA06F0000, offset_dict, 4)  # overflow loop to 1
    writeValue(ROM_COPY, 0x8002E0F0, Overlay.Menu, 0x5C400004, offset_dict, 4)  # underflow loop from 1
    writeValue(ROM_COPY, 0x8002EA3A, Overlay.Menu, 0xFFFE, offset_dict)  # Disable option 1 load
    writeValue(ROM_COPY, 0x8002EA4C, Overlay.Menu, 0xA0600003, offset_dict, 4)  # Force Krusha to 0
    writeValue(ROM_COPY, 0x8002EA64, Overlay.Menu, 0xA64B0008, offset_dict, 4)  # Disable option 1 write
    # Menu/Shop: Snide's
    writeValue(ROM_COPY, 0x8002402C, Overlay.Menu, 0x240E000C, offset_dict, 4)  # No extra contraption cutscenes
    writeValue(ROM_COPY, 0x80024054, Overlay.Menu, 0x24080001, offset_dict, 4)  # 1 GB Turn in
    # Menu/Shop: Candy's
    writeValue(ROM_COPY, 0x80027678, Overlay.Menu, 0x1000, offset_dict)  # Patch Candy's Shop Glitch
    writeValue(ROM_COPY, 0x8002769C, Overlay.Menu, 0x1000, offset_dict)  # Patch Candy's Shop Glitch
    # Menu/Shop: Disable Multiplayer
    writeValue(ROM_COPY, 0x800280B0, Overlay.Menu, 0, offset_dict, 4)  # Disable access
    writeValue(ROM_COPY, 0x80028A8C, Overlay.Menu, 0, offset_dict, 4)  # Lower Sprite Opacity
    # Menu/Shop: Cross Kong Purchases
    writeValue(ROM_COPY, 0x80025EA0, Overlay.Menu, 0x90850004, offset_dict, 4)  # Change target kong (Progressive) # LBU     a1, 0x4 (a0)
    writeValue(ROM_COPY, 0x80025E80, Overlay.Menu, 0x90850004, offset_dict, 4)  # Change target kong (Bitfield) # LBU    a1, 0x4 (a0)
    writeValue(ROM_COPY, 0x80025F70, Overlay.Menu, 0x93060005, offset_dict, 4)  # Change price deducted # LBU    a2, 0x5 (t8)
    writeValue(ROM_COPY, 0x80026200, Overlay.Menu, 0x90CF0005, offset_dict, 4)  # Change price check # LBU   t7, 0x5 (a2)
    writeValue(ROM_COPY, 0x80027AE0, Overlay.Menu, 0x910F0004, offset_dict, 4)  # Change Special Moves Text # LBU    t7, 0x4 (t0)
    writeValue(ROM_COPY, 0x80027BA0, Overlay.Menu, 0x91180004, offset_dict, 4)  # Change Gun Text # LBU  t8, 0x4 (t0)
    writeValue(ROM_COPY, 0x80027C14, Overlay.Menu, 0x910C0004, offset_dict, 4)  # Change Instrument Text # LBU   t4, 0x4 (t0)
    writeValue(ROM_COPY, 0x80026C08, Overlay.Menu, 0x91790011, offset_dict, 4)  # Fix post-special move text # LBU   t9, 0x11 (t3)
    writeValue(ROM_COPY, 0x80026C00, Overlay.Menu, 0x916D0004, offset_dict, 4)  # Fix post-special move text # LBU   t5, 0x4 (t3)
    # Menu/Shop: Move Bitfield
    writeValue(ROM_COPY, 0x80025E9C, Overlay.Menu, 0x0C009751, offset_dict, 4)  # Change writing of move to "write bitfield move" function call
    writeValue(ROM_COPY, 0x8002E266, Overlay.Menu, 7, offset_dict)  # Enguarde Arena Movement Write
    writeValue(ROM_COPY, 0x8002F01E, Overlay.Menu, 7, offset_dict)  # Rambi Arena Movement Write
    # Menu/Shop: Change move purchase
    writeFunction(ROM_COPY, 0x80026720, Overlay.Menu, "getNextMovePurchase", offset_dict)
    writeFunction(ROM_COPY, 0x8002683C, Overlay.Menu, "getNextMovePurchase", offset_dict)
    # Menu/Shop: Write Modified purchase move stuff
    writeFunction(ROM_COPY, 0x80027324, Overlay.Menu, "purchaseFirstMoveHandler", offset_dict)
    if not settings.fast_start_beginning_of_game:
        writeFunction(ROM_COPY, 0x80027150, Overlay.Menu, "checkFirstMovePurchase", offset_dict)
    writeFunction(ROM_COPY, 0x8002691C, Overlay.Menu, "purchaseMove", offset_dict)
    writeFunction(ROM_COPY, 0x800270B8, Overlay.Menu, "showPostMoveText", offset_dict)
    writeFunction(ROM_COPY, 0x80026508, Overlay.Menu, "canPlayJetpac", offset_dict)
    writeValue(ROM_COPY, 0x80026F64, Overlay.Menu, 0, offset_dict, 4)  # Disable check for whether you have a move before giving donation at shop
    writeValue(ROM_COPY, 0x80026F68, Overlay.Menu, 0, offset_dict, 4)  # Disable check for whether you have a move before giving donation at shop
    # Menu/Shop: Shop Hints
    if settings.enable_shop_hints:
        writeFunction(ROM_COPY, 0x8002661C, Overlay.Menu, "getMoveHint", offset_dict)
        writeFunction(ROM_COPY, 0x800265F0, Overlay.Menu, "getMoveHint", offset_dict)
    # Menu/Shop: Visual Changes
    writeFunction(ROM_COPY, 0x80030604, Overlay.Menu, "file_progress_screen_code", offset_dict)  # New file progress code
    writeFunction(ROM_COPY, 0x80029FE0, Overlay.Menu, "wipeFileMod", offset_dict)  # Wipe File Hook
    writeFunction(ROM_COPY, 0x80028C88, Overlay.Menu, "enterFileProgress", offset_dict)  # Enter File Progress Screen Hook
    writeValue(ROM_COPY, 0x80029818, Overlay.Menu, 0, offset_dict, 4)  # Hide A
    writeValue(ROM_COPY, 0x80029840, Overlay.Menu, 0, offset_dict, 4)  # Hide B
    # writeValue(ROM_COPY, 0x80029874, Overlay.Menu, 0, offset_dict, 4) # Hide GB
    writeValue(ROM_COPY, 0x8002986E, Overlay.Menu, 198, offset_dict)  # Move GB to right
    writeValue(ROM_COPY, 0x80029872, Overlay.Menu, 114, offset_dict)  # Move GB down
    writeValue(ROM_COPY, 0x8002985A, Overlay.Menu, 0, offset_dict)  # Change sprite mode for GB
    writeFloat(ROM_COPY, 0x80033CA8, Overlay.Menu, 0.4, offset_dict)  # Change GB Scale
    # Menu/Shop: File Select
    writeFunction(ROM_COPY, 0x80028D04, Overlay.Menu, "changeFileSelectAction", offset_dict)  # File select change action
    writeFunction(ROM_COPY, 0x80028D10, Overlay.Menu, "changeFileSelectAction_0", offset_dict)  # File select change action
    writeFunction(ROM_COPY, 0x80029A70, Overlay.Menu, "getGamePercentage", offset_dict)
    writeValue(ROM_COPY, 0x80028EF8, Overlay.Menu, 0, offset_dict, 4)  # Joystick
    # Menu/Shop: Options
    writeValue(ROM_COPY, 0x800338FC, Overlay.Menu, 5, offset_dict, 1)  # 5 Options
    writeValue(ROM_COPY, 0x8002DA86, Overlay.Menu, 1, offset_dict)  # Cap to 1
    writeValue(ROM_COPY, 0x8002DA46, Overlay.Menu, getHiSym("InvertedControls"), offset_dict)  # Up/Down Edit
    writeValue(ROM_COPY, 0x8002DA4E, Overlay.Menu, getLoSym("InvertedControls"), offset_dict)  # Up/Down Edit
    writeValue(ROM_COPY, 0x8002DA1E, Overlay.Menu, getHiSym("InvertedControls"), offset_dict)  # Up/Down Edit
    writeValue(ROM_COPY, 0x8002DA22, Overlay.Menu, getLoSym("InvertedControls"), offset_dict)  # Up/Down Edit
    writeValue(ROM_COPY, 0x8002DADE, Overlay.Menu, getHiSym("InvertedControls"), offset_dict)  # Save to global
    writeValue(ROM_COPY, 0x8002DAE2, Overlay.Menu, getLoSym("InvertedControls"), offset_dict)  # Save to global
    writeValue(ROM_COPY, 0x8002DA88, Overlay.Menu, 0x1000, offset_dict)  # Prevent Language Update
    writeFunction(ROM_COPY, 0x8002DEC4, Overlay.Menu, "displayInverted", offset_dict)  # Modify Function Call
    # Menu/Shop: Mystery
    move_levels = (1, 1, 3, 1, 7, 1, 1, 7)
    for index, value in enumerate(move_levels):
        writeValue(ROM_COPY, 0x80033938 + (8 * index) + 4, Overlay.Menu, value, offset_dict, 1)
    # Menu/Shop: Misc Shop Stuff
    writeHook(ROM_COPY, 0x800260E0, Overlay.Menu, "CrankyDecouple", offset_dict)
    writeHook(ROM_COPY, 0x800260A8, Overlay.Menu, "ForceToBuyMoveInOneLevel", offset_dict)
    writeValue(ROM_COPY, 0x80026160, Overlay.Menu, 0, offset_dict, 4)
    writeHook(ROM_COPY, 0x80026140, Overlay.Menu, "PriceKongStore", offset_dict)
    writeHook(ROM_COPY, 0x80025FC0, Overlay.Menu, "CharacterCollectableBaseModify", offset_dict)
    writeHook(ROM_COPY, 0x800260F0, Overlay.Menu, "SetMoveBaseBitfield", offset_dict)
    writeHook(ROM_COPY, 0x8002611C, Overlay.Menu, "SetMoveBaseProgressive", offset_dict)
    writeHook(ROM_COPY, 0x80026924, Overlay.Menu, "AlwaysCandyInstrument", offset_dict)
    writeValue(ROM_COPY, 0x80026072, Overlay.Menu, getHiSym("CrankyMoves_New"), offset_dict)
    writeValue(ROM_COPY, 0x8002607A, Overlay.Menu, getLoSym("CrankyMoves_New"), offset_dict)
    writeValue(ROM_COPY, 0x8002607E, Overlay.Menu, getHiSym("CandyMoves_New"), offset_dict)
    writeValue(ROM_COPY, 0x80026086, Overlay.Menu, getLoSym("CandyMoves_New"), offset_dict)
    writeValue(ROM_COPY, 0x8002608A, Overlay.Menu, getHiSym("FunkyMoves_New"), offset_dict)
    writeValue(ROM_COPY, 0x8002608E, Overlay.Menu, getLoSym("FunkyMoves_New"), offset_dict)

    # Mill and Crypt Levers
    # Mill Levers
    if settings.mill_levers[0] > 0:
        sequence_length = 0
        sequence_ended = False
        sequence_pattern = [0] * 5
        for x in range(5):
            if not sequence_ended:
                if settings.mill_levers[x] == 0:
                    sequence_ended = True
                else:
                    sequence_length += 1
        writeValue(ROM_COPY, 0x8064E4CE, Overlay.Static, sequence_length, offset_dict)
        for x in range(sequence_length):
            sequence_pattern[x] = settings.mill_levers[(sequence_length - 1) - x]
        for xi, x in enumerate(sequence_pattern):
            writeValue(ROM_COPY, 0x807482E0 + xi, Overlay.Static, x, offset_dict, 1)
    # Crypt Levers
    if settings.crypt_levers[0] > 0:
        sequence = [0] * 3
        for x in range(3):
            sequence[x] = settings.crypt_levers[2 - x]
        for xi, x in enumerate(sequence):
            writeValue(ROM_COPY, 0x807482E8 + xi, Overlay.Static, x, offset_dict, 1)

    if IsItemSelected(settings.hard_mode, settings.hard_mode_selected, HardModeSelected.shuffled_jetpac_enemies, False):
        order = settings.jetpac_enemy_order
        functions = [
            0x80029884,
            0x8002992C,
            0x80029AF8,
            0x80029E0C,
            0x8002A2AC,
            0x8002A6C0,
            0x8002A8F0,
            0x8002A944,
        ]
        for slot_index, enemy_index in enumerate(order):
            writeValue(ROM_COPY, 0x8002E8F4 + (4 * slot_index), Overlay.Jetpac, functions[enemy_index], offset_dict, 4)
    writeFunction(ROM_COPY, 0x80025034, Overlay.Jetpac, "loadJetpacSprites_handler", offset_dict)
    writeValue(ROM_COPY, 0x800281AC, Overlay.Jetpac, 0x5000, offset_dict)  # Make Rareware Coin permanent once spawned until collected

    writeValue(ROM_COPY, 0x806BA5A8, Overlay.Static, 0x1D800003, offset_dict, 4)  # Fix some health oversights by making death if health <= 0 instead of == 0
    writeValue(ROM_COPY, 0x806BA50E, Overlay.Static, 20, offset_dict)  # Change BHDM Cooldown

    if settings.mirror_mode:
        # Invert Aspect
        writeValue(ROM_COPY, 0x80006070, Overlay.Boot, 0x3C048000, offset_dict, 4)  # Invert Aspect - LUI a0, 0x8000
        writeValue(ROM_COPY, 0x80006074, Overlay.Boot, 0x00E43826, offset_dict, 4)  # Invert Aspect - XOR a3, a3, a0
        # Invert X Axis input
        writeFunction(ROM_COPY, 0x8060AC60, Overlay.Static, "parseControllerInput", offset_dict)
        # Invert camera directions
        writeValue(ROM_COPY, 0x806EA25E, Overlay.Static, 45, offset_dict, 2, True)
        writeValue(ROM_COPY, 0x806EA2CA, Overlay.Static, -45, offset_dict, 2, True)
        # Fix chunk rendering
        writeValue(ROM_COPY, 0x80657F2C, Overlay.Static, 0x0082082A, offset_dict, 4)
        writeValue(ROM_COPY, 0x80657F7C, Overlay.Static, 0x0046082A, offset_dict, 4)
        # Fix cannon game
        writeValue(ROM_COPY, 0x807599B0, Overlay.Static, 0xBF, offset_dict, 1)
        # Skybox
        writeValue(ROM_COPY, 0x8068BD0C, Overlay.Static, 0x46103201, offset_dict, 4)
        writeValue(ROM_COPY, 0x80706A54, Overlay.Static, 0x03194023, offset_dict, 4)
        # Invert G_TRI2 Call
        writeValue(ROM_COPY, 0x8065DFBE, Overlay.Static, 0x0206, offset_dict)
        writeValue(ROM_COPY, 0x8065DFC6, Overlay.Static, 0x0604, offset_dict)
        # Invert pan
        writeHook(ROM_COPY, 0x80737708, Overlay.Static, "invertPan", offset_dict)

    if IsItemSelected(settings.hard_mode, settings.hard_mode_selected, HardModeSelected.reduced_fall_damage_threshold, False):
        writeFloatUpper(ROM_COPY, 0x806D3682, Overlay.Static, 100, offset_dict)  # Change fall too far threshold
        writeFunction(ROM_COPY, 0x806D36B4, Overlay.Static, "fallDamageWrapper", offset_dict)
        writeFunction(ROM_COPY, 0x8067F540, Overlay.Static, "transformBarrelImmunity", offset_dict)
        writeFunction(ROM_COPY, 0x8068B178, Overlay.Static, "factoryShedFallImmunity", offset_dict)

    # Increase Arcade Lives
    writeValue(ROM_COPY, 0x80024F10, Overlay.Arcade, 0x240E0005, offset_dict, 4)  # ADDIU $t6, $r0, 0x5 - Set Arcade Lives
    writeValue(ROM_COPY, 0x80024F2A, Overlay.Arcade, 0xC71B, offset_dict)
    writeValue(ROM_COPY, 0x80024F2C, Overlay.Arcade, 0xA0CEC71B, offset_dict, 4)  # SB $t6, 0xC71B ($a2)
    writeValue(ROM_COPY, 0x80024688, Overlay.Arcade, 0x1000, offset_dict)  # Disable lives bonus for reaching 10k points
    writeValue(ROM_COPY, 0x8002B7A4, Overlay.Arcade, 0, offset_dict, 4)  # Disable death removing lives
    # Address of Nintendo Coin Image write: 0x8002E8B4/0x8002E8C0
    writeFunction(ROM_COPY, 0x80024D5C, Overlay.Arcade, "arcadeExit", offset_dict)
    writeFunction(ROM_COPY, 0x800257B4, Overlay.Arcade, "arcadeExit", offset_dict)
    writeFunction(ROM_COPY, 0x8002B6D4, Overlay.Arcade, "arcadeExit", offset_dict)
    writeFunction(ROM_COPY, 0x8002FA58, Overlay.Arcade, "arcadeExit", offset_dict)
    # Fix arcade level setting logic
    writeFunction(ROM_COPY, 0x80024F34, Overlay.Arcade, "determineArcadeLevel", offset_dict)  # Change log
    writeValue(ROM_COPY, 0x80024F70, Overlay.Arcade, 0, offset_dict, 4)  # Prevent level set
    writeValue(ROM_COPY, 0x80024F50, Overlay.Arcade, 0, offset_dict, 4)  # Prevent level set
    # Arcade Level Order Rando
    writeFunction(ROM_COPY, 0x8002F7BC, Overlay.Arcade, "HandleArcadeVictory", offset_dict)
    writeFunction(ROM_COPY, 0x8002FA68, Overlay.Arcade, "HandleArcadeVictory", offset_dict)
    writeValue(ROM_COPY, 0x8002FA24, Overlay.Arcade, 0x1000, offset_dict)

    writeLabelValue(ROM_COPY, 0x80748088, Overlay.Static, "CrownDoorCheck", offset_dict)  # Update check on Crown Door

    # Fast Start: Beginning of game
    if settings.fast_start_beginning_of_game:
        writeValue(ROM_COPY, 0x80714540, Overlay.Static, 0, offset_dict, 4)
        file_init_flags.extend(
            [
                0x1BB,  # Japes Open
                0x186,  # Escape Cutscene
                0x17F,  # Training Barrels Spawned
                0x180,  # First Slam Given
            ]
        )
    else:
        writeValue(ROM_COPY, 0x80755F4C, Overlay.Static, 0, offset_dict)  # Remove escape cutscene
    if settings.auto_keys:
        file_init_flags.append(0x1BB)  # Japes Open
    barrier_flags = {
        RemovedBarriersSelected.japes_shellhive_gate: [0x7],
        RemovedBarriersSelected.aztec_tunnel_door: [0x4E],
        RemovedBarriersSelected.factory_testing_gate: [0x6E],
        RemovedBarriersSelected.galleon_lighthouse_gate: [0x9B],
        RemovedBarriersSelected.forest_green_tunnel: [0xCF, 0xD0],  # Feather, Pineapple
        RemovedBarriersSelected.forest_yellow_tunnel: [0xD2],
        RemovedBarriersSelected.aztec_5dtemple_switches: [0x37],
        RemovedBarriersSelected.factory_production_room: [0x6F],
        RemovedBarriersSelected.galleon_seasick_ship: [0x9C],
        RemovedBarriersSelected.caves_igloo_pads: [0x128],
        RemovedBarriersSelected.galleon_shipyard_area_gate: [0xA1],
        RemovedBarriersSelected.caves_ice_walls: [266, 267, 265],  # Entrance, Snide, Giant Boulder
        RemovedBarriersSelected.galleon_treasure_room: [0xA2],
        RemovedBarriersSelected.aztec_tiny_temple_ice: [0x45],
    }
    for barrier in barrier_flags:
        if IsItemSelected(settings.remove_barriers_enabled, settings.remove_barriers_selected, barrier):
            file_init_flags.extend(barrier_flags[barrier])

    writeFunction(ROM_COPY, 0x80682A98, Overlay.Static, "resetCannonGameState", offset_dict)

    if settings.enemy_kill_crown_timer:
        writeFunction(ROM_COPY, 0x8072AC80, Overlay.Static, "handleCrownTimer", offset_dict)
        writeFunction(ROM_COPY, 0x806AEEBC, Overlay.Static, "klumpCrownHandler", offset_dict)

    # Enable oranges in Crowns
    writeHook(ROM_COPY, 0x806E6000, Overlay.Static, "DisableGunInCrowns", offset_dict)
    for map_id in (
        Maps.JapesCrown,
        Maps.AztecCrown,
        Maps.FactoryCrown,
        Maps.GalleonCrown,
        Maps.ForestCrown,
        Maps.CavesCrown,
        Maps.CastleCrown,
        Maps.HelmCrown,
        Maps.LobbyCrown,
        Maps.SnidesCrown,
    ):
        writeValue(ROM_COPY, 0x8074482C + (12 * map_id), Overlay.Static, 0x01120402, offset_dict, 4)
    # Disable pickup respawn in spider boss (temporary)
    writeValue(ROM_COPY, 0x8074482C + (12 * Maps.ForestSpider), Overlay.Static, 0x00000141, offset_dict, 4)

    # Remove troll flame in 75m
    writeValue(ROM_COPY, 0x80028FE4, Overlay.Arcade, 0xAC800018, offset_dict, 4)  # sw $zero, 0x18 ($ao). Sets obj type to 0

    # Patch Enemy Collision
    writeLabelValue(ROM_COPY, 0x8074B53C, Overlay.Static, "fixed_shockwave_collision", offset_dict)  # Purple Klaptrap
    writeLabelValue(ROM_COPY, 0x8074B4EC, Overlay.Static, "fixed_shockwave_collision", offset_dict)  # Red Klaptrap
    writeLabelValue(ROM_COPY, 0x8074BC24, Overlay.Static, "fixed_shockwave_collision", offset_dict)  # Book
    writeLabelValue(ROM_COPY, 0x8074BBF0, Overlay.Static, "fixed_bug_collision", offset_dict)  # All Zingers & Bats & the bug
    writeLabelValue(ROM_COPY, 0x8074B6B8, Overlay.Static, "fixed_dice_collision", offset_dict)  # Mr. Dice (Both), Sir Domino, Ruler
    writeLabelValue(ROM_COPY, 0x8074B4C4, Overlay.Static, "fixed_klap_collision", offset_dict)  # Green Klaptrap, Skeleton Klaptrap

    if not settings.disable_racing_patches:
        writeValue(ROM_COPY, 0x806D0328, Overlay.Static, 0x1000, offset_dict)  # Disable Fungi OSprint Slowdown
        writeValue(ROM_COPY, 0x806CBE04, Overlay.Static, 0x1000, offset_dict)  # Disable Fungi OSprint Slowdown
        writeFloat(ROM_COPY, 0x807532E4, Overlay.Static, 90, offset_dict)  # Set Chunky pickup speed to 90 (instead of 100)
        writeValue(ROM_COPY, 0x806BEB76, Overlay.Static, 0x3FE8, offset_dict)  # Tone down the rabbit race 1 speed to 0.75x rather than 1.0x

    # Expand Path Allocation
    writeValue(ROM_COPY, 0x80722E56, Overlay.Static, getHiSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x80722E7A, Overlay.Static, getLoSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x80722FF6, Overlay.Static, getHiSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x80722FFE, Overlay.Static, getLoSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x80723026, Overlay.Static, getHiSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x8072302E, Overlay.Static, getLoSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x80723CF6, Overlay.Static, getHiSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x80723D06, Overlay.Static, getLoSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x80723FEA, Overlay.Static, getHiSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x80723FEE, Overlay.Static, getLoSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x807241CE, Overlay.Static, getHiSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x807241DE, Overlay.Static, getLoSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x80724312, Overlay.Static, getHiSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x8072431E, Overlay.Static, getLoSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x807245DE, Overlay.Static, getHiSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x807245E6, Overlay.Static, getLoSym("balloon_path_pointers"), offset_dict)
    writeValue(ROM_COPY, 0x80722E92, Overlay.Static, getVar("path_cap"), offset_dict)

    # Expand Enemy Drops Table
    writeValue(ROM_COPY, 0x806A5CA6, Overlay.Static, getHiSym("drops"), offset_dict, 2)
    writeValue(ROM_COPY, 0x806A5CB6, Overlay.Static, getLoSym("drops"), offset_dict, 2)
    writeValue(ROM_COPY, 0x806A5CBA, Overlay.Static, getHiSym("drops"), offset_dict, 2)
    writeValue(ROM_COPY, 0x806A5CBE, Overlay.Static, getLoSym("drops"), offset_dict, 2)
    writeValue(ROM_COPY, 0x806A5CD2, Overlay.Static, getHiSym("drops"), offset_dict, 2)
    writeValue(ROM_COPY, 0x806A5CD6, Overlay.Static, getLoSym("drops"), offset_dict, 2)

    # Pause Sprite Expansion / Carousel Init Functions
    writeValue(ROM_COPY, 0x806AB35A, Overlay.Static, getHiSym("file_sprites"), offset_dict)
    writeValue(ROM_COPY, 0x806AB35E, Overlay.Static, getLoSym("file_sprites"), offset_dict)
    writeValue(ROM_COPY, 0x806AB2CA, Overlay.Static, getHiSym("file_items"), offset_dict)
    writeValue(ROM_COPY, 0x806AB2DA, Overlay.Static, getLoSym("file_items"), offset_dict)
    writeValue(ROM_COPY, 0x806A9FC2, Overlay.Static, getHiSym("file_items"), offset_dict)
    writeValue(ROM_COPY, 0x806AA036, Overlay.Static, getLoSym("file_items"), offset_dict)
    writeValue(ROM_COPY, 0x806AA00E, Overlay.Static, getHiSym("file_item_caps"), offset_dict)
    writeValue(ROM_COPY, 0x806AA032, Overlay.Static, getLoSym("file_item_caps"), offset_dict)
    writeFunction(ROM_COPY, 0x806AB3C4, Overlay.Static, "updatePauseScreenWheel", offset_dict)  # Change Wheel to scroller
    writeValue(ROM_COPY, 0x806AB3B4, Overlay.Static, 0xAFB00018, offset_dict, 4)  # SW $s0, 0x18 ($sp). Change last param to index
    writeValue(ROM_COPY, 0x806AB3A0, Overlay.Static, 0xAFA90014, offset_dict, 4)  # SW $t1, 0x14 ($sp). Change 2nd-to-last param to local index
    writeValue(ROM_COPY, 0x806AB444, Overlay.Static, 0, offset_dict, 4)  # Prevent joystick sprite rendering
    writeFunction(ROM_COPY, 0x806AB528, Overlay.Static, "handleSpriteCode", offset_dict)  # Change sprite control function
    writeValue(ROM_COPY, 0x806AB52C, Overlay.Static, 0x8FA40060, offset_dict, 4)  # LW $a0, 0x60 ($sp). Change param
    writeValue(ROM_COPY, 0x806A8DB2, Overlay.Static, 0x0029, offset_dict)  # Swap left/right direction
    writeValue(ROM_COPY, 0x806A8DBA, Overlay.Static, 0xFFD8, offset_dict)  # Swap left/right direction
    writeValue(ROM_COPY, 0x806A8DB4, Overlay.Static, 0x5420, offset_dict)  # BEQL -> BNEL
    writeValue(ROM_COPY, 0x806A8DF0, Overlay.Static, 0x1020, offset_dict)  # BNE -> BEQ
    writeFunction(ROM_COPY, 0x806A9F74, Overlay.Static, "pauseScreen3And4ItemName", offset_dict)  # Item Name"

    # Write File init flags - Always keep at the end
    file_init_flags = list(set(file_init_flags))  # Make sure it only contains unique values
    if len(file_init_flags) > 0x3FF:
        raise Exception("Too many file init flags. Please report this to the devs with a setting string.")
    ROM_COPY.seek(0x1FFD800)
    for flag in file_init_flags:
        ROM_COPY.writeMultipleBytes(flag, 2)
    ROM_COPY.writeMultipleBytes(0xFFFF, 2)

    # Settings to check usage
    # faster_checks.rabbit_race
    # quality_of_life.caves_kosha_dead
    # galleon_water_raised
