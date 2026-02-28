"""Patches assembly instructions from the overlays rather than doing changes live."""

import js
import math
import io
import randomizer.ItemPool as ItemPool
from typing import Union
from randomizer.Patching.Library.Assets import getPointerLocation
from randomizer.Patching.Library.Generic import Overlay, IsItemSelected, TableNames, IsDDMSSelected
from randomizer.Patching.Library.Image import getImageFile, TextureFormat
from randomizer.Patching.Library.ItemRando import CustomActors
from randomizer.Patching.Library.ASM import *
from randomizer.Settings import Settings
from randomizer.Enums.Settings import (
    FasterChecksSelected,
    RemovedBarriersSelected,
    GalleonWaterSetting,
    ActivateAllBananaports,
    FreeTradeSetting,
    HardModeSelected,
    FungiTimeSetting,
    MiscChangesSelected,
    PuzzleRando,
    WinConditionComplex,
    ExtraCutsceneSkips,
    ProgressiveHintItem,
    WrinklyHints,
)
from randomizer.Enums.Enemies import Enemies
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Lists.MapsAndExits import GetExitId, GetMapId
from randomizer.Enums.Models import Model
from randomizer.Patching.Patcher import ROM, LocalROM
from randomizer.Enums.Settings import ShuffleLoadingZones, MinigamesListSelected
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Enums.Types import Types, BarrierItems
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Items import Items
from randomizer.Patching.ASM.Actors import *
from randomizer.Patching.ASM.Cosmetic import *
from randomizer.Patching.ASM.Items import *
from randomizer.Patching.ASM.Kaizo import *
from randomizer.Patching.ASM.Save import saveUpdates
from randomizer.Patching.ASM.TextFiles import writeNewTextFiles
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
ENABLE_BLAST_LZR = False
UNSHROUDED_CASTLE = False
FARPLANE_VIEW = False
KLAPTRAPS_IN_SEARCHLIGHT_SEEK = 1
CAMERA_RESET_REDUCTION = True
PAL_DOGADON_REMATCH_FIRE = True
REMOVE_CS_BARS = False
JP_TEXTBOX_SIZES = True
FRAMEBUFFER_STORE_FIX = True
BLOCK_FILE_DELETION_ON_CHECKSUM_MISMATCH = False
HARDER_CRUSHERS = True
BOULDERS_DONT_DESTROY = True
CAN_THROW_KEGS = True
CAN_THROW_APPLES = True
DISABLE_LONG_JUMP = False

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


def fixLankyIncompatibility(ROM_COPY: ROM):
    """Ensure compatibility with .lanky files created during a specific time frame."""
    offset_dict = populateOverlayOffsets(ROM_COPY)
    if readValue(ROM_COPY, 0x80602AB0, Overlay.Static, offset_dict, 4) != 0x0C180917:
        writeValue(ROM_COPY, 0x80602AAC, Overlay.Static, 0x27A40018, offset_dict, 4)  # addiu $a0, $sp, 0x18


def patchAssemblyCosmetic(ROM_COPY: ROM, settings: Settings, has_dom: bool = True):
    """Patch assembly instructions that pertain to cosmetic changes."""
    offset_dict = populateOverlayOffsets(ROM_COPY)
    jetpacCosmetics(ROM_COPY, settings, offset_dict)
    if has_dom:
        arcadeCosmetics(ROM_COPY, settings, offset_dict)
    modelCosmetics(ROM_COPY, settings, offset_dict)
    holidayCosmetics(ROM_COPY, settings, offset_dict)
    musicCosmetics(ROM_COPY, settings, offset_dict)
    cameraCosmetics(ROM_COPY, settings, offset_dict)
    otherCosmetics(ROM_COPY, settings, offset_dict)


def isFasterCheckEnabled(spoiler, fast_check: FasterChecksSelected):
    """Determine if a faster check setting is enabled."""
    return IsDDMSSelected(spoiler.settings.faster_checks_selected, fast_check)


def isQoLEnabled(spoiler, misc_change: MiscChangesSelected):
    """Determine if a faster check setting is enabled."""
    return IsDDMSSelected(spoiler.settings.misc_changes_selected, misc_change)


def writeItemReferenceFlags(ROM_COPY: LocalROM, flag_list: list):
    """Write the list of item reference flags to ROM."""
    ram_addr = getSym("itemloc_flags")
    offset_dict = populateOverlayOffsets(ROM_COPY)
    addr = getROMAddress(ram_addr, Overlay.Custom, offset_dict)
    for xi, x in enumerate(flag_list):
        if x is not None:
            ROM_COPY.seek(addr + (xi * 2))
            ROM_COPY.writeMultipleBytes(x, 2)


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
        other_images: list[int] = None,
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
            self.other_images = other_images

    def getImageBytes(self, ROM_COPY: Union[LocalROM, ROM], sub_dir: str, targ_width: int, targ_height: int, output_format: TextureFormat, flip: bool = True) -> bytes:
        """Convert associated image to bytes that can be written to ROM."""
        output_image = None
        if self.pull_from_repo:
            output_image = Image.open(io.BytesIO(js.getFile(f"base-hack/assets/arcade_jetpac/{sub_dir}/{self.file_name}.png")))
        else:
            new_im = getImageFile(ROM_COPY, self.table_index, self.file_index, self.table_index != 7, self.width, self.height, self.tex_format)
            width = self.width
            height = self.height
            if self.other_images is not None:
                if len(self.other_images) == 1:
                    width *= 2
                elif len(self.other_images) == 3:
                    width *= 2
                    height *= 2
                else:
                    raise Exception("Invalid other images length. Unable to correctly patch")
                base_im = Image.new(mode="RGBA", size=(width, height))
                base_im.paste(new_im, (0, 0), new_im)
                for img_index, other_image in enumerate(self.other_images):
                    new_im = getImageFile(ROM_COPY, self.table_index, other_image, self.table_index != 7, self.width, self.height, self.tex_format)
                    x_offset = self.width
                    y_offset = 0
                    if img_index == 1:
                        x_offset = 0
                    if img_index > 0:
                        y_offset = self.height
                    base_im.paste(new_im, (x_offset, y_offset), new_im)
                new_im = base_im
            if width != height:
                dim = max(width, height)
                dx = int((dim - width) / 2)
                dy = int((dim - height) / 2)
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
        Minigame8BitImage([Items.Pearl, Items.FillerPearl], MinigameImageLoader("pearl"), MinigameImageLoader("pearl")),
        Minigame8BitImage(ItemPool.DonkeyMoves, MinigameImageLoader("potion_dk"), MinigameImageLoader("potion")),
        Minigame8BitImage(ItemPool.DiddyMoves, MinigameImageLoader("potion_diddy"), MinigameImageLoader("potion")),
        Minigame8BitImage(ItemPool.LankyMoves, MinigameImageLoader("potion_lanky"), MinigameImageLoader("potion")),
        Minigame8BitImage(ItemPool.TinyMoves, MinigameImageLoader("potion_tiny"), MinigameImageLoader("potion")),
        Minigame8BitImage(ItemPool.ChunkyMoves, MinigameImageLoader("potion_chunky"), MinigameImageLoader("potion")),
        Minigame8BitImage(colorless_potions, MinigameImageLoader("potion_any"), MinigameImageLoader("potion")),
        Minigame8BitImage([Items.BattleCrown, Items.FillerCrown], MinigameImageLoader(None, 25, 5893, 44, 44), MinigameImageLoader("crown")),
        Minigame8BitImage(
            [Items.BananaFairy, Items.FillerFairy],
            MinigameImageLoader(None, 25, 0x16ED, 32, 32, TextureFormat.RGBA32),
            MinigameImageLoader("fairy"),
        ),
        Minigame8BitImage([Items.GoldenBanana, Items.FillerBanana], MinigameImageLoader(None, 25, 5468, 44, 44), MinigameImageLoader("gb")),
        Minigame8BitImage(ItemPool.Blueprints(), MinigameImageLoader(None, 25, 0x1593, 48, 42), MinigameImageLoader("blueprint")),
        Minigame8BitImage(ItemPool.Keys(), MinigameImageLoader(None, 25, 5877, 44, 44), MinigameImageLoader("key")),
        Minigame8BitImage([Items.BananaMedal, Items.FillerMedal], MinigameImageLoader(None, 25, 0x156C, 44, 44), MinigameImageLoader("medal")),
        Minigame8BitImage([Items.JunkMelon], MinigameImageLoader(None, 7, 0x142, 48, 42), MinigameImageLoader("melon")),
        Minigame8BitImage([Items.NintendoCoin], None, MinigameImageLoader("nintendo")),
        Minigame8BitImage([Items.RarewareCoin], MinigameImageLoader(None, 25, 5905, 44, 44), None),
        Minigame8BitImage([Items.RainbowCoin, Items.FillerRainbowCoin], MinigameImageLoader(None, 25, 5963, 48, 44), MinigameImageLoader("rainbow")),
        Minigame8BitImage(
            ItemPool.HintItems(),
            MinigameImageLoader(None, 25, 0x1775, 64, 64, TextureFormat.IA8),
            MinigameImageLoader("hint"),
        ),
        Minigame8BitImage([Items.ArchipelagoItem], MinigameImageLoader("ap"), MinigameImageLoader("ap")),
        Minigame8BitImage([Items.SpecialArchipelagoItem], MinigameImageLoader("ap_useful"), MinigameImageLoader("ap")),
        Minigame8BitImage([Items.FoolsArchipelagoItem], MinigameImageLoader("ap_junk"), MinigameImageLoader("ap")),
        Minigame8BitImage([Items.TrapArchipelagoItem], MinigameImageLoader("ap_trap"), MinigameImageLoader("ap")),
        Minigame8BitImage(
            [Items.Cranky],
            MinigameImageLoader(None, 25, 0x1387, 32, 32, TextureFormat.RGBA5551, [0x1388, 0x1389, 0x138A]),
            MinigameImageLoader("kong"),
        ),
        Minigame8BitImage(
            [Items.Funky],
            MinigameImageLoader(None, 25, 0x172F, 32, 32, TextureFormat.RGBA5551, [0x1730, 0x1731, 0x1732]),
            MinigameImageLoader("kong"),
        ),
        Minigame8BitImage(
            [Items.Candy],
            MinigameImageLoader(None, 25, 0x172A, 32, 32, TextureFormat.RGBA5551, [0x172B, 0x172C, 0x172D]),
            MinigameImageLoader("kong"),
        ),
        Minigame8BitImage(
            [Items.Snide],
            MinigameImageLoader(None, 25, 0x172E, 64, 32, TextureFormat.RGBA5551),
            MinigameImageLoader("kong"),
        ),
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
    writeValue(ROM_COPY, 0x8071288A, Overlay.Static, IS_FINAL_BOSS_BIT, offset_dict)  # 80712888 - Deathwarp location (should change this)

    # 20
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


def getModelTwoAllowances(ROM_COPY: LocalROM) -> dict:
    """Get the total amount of model 2 items in each map."""
    max_default = 0
    output = {}
    for x in range(216):
        file_start = getPointerLocation(TableNames.Setups, x)
        ROM_COPY.seek(file_start)
        model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        if x in (7, 0x1A, 0x1E, 0x26, 0x30):
            output[x] = model2_count
        elif max_default < model2_count:
            max_default = model2_count
    output["default"] = max_default
    return output


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

    writeValue(ROM_COPY, 0x8068ABEA, Overlay.Static, getHiSym("replacement_lobbies_array"), offset_dict)
    writeValue(ROM_COPY, 0x8068ABEE, Overlay.Static, getLoSym("replacement_lobbies_array"), offset_dict)
    writeValue(ROM_COPY, 0x8060005A, Overlay.Static, getHiSym("replacement_lobbies_array"), offset_dict)
    writeValue(ROM_COPY, 0x8060006E, Overlay.Static, getLoSym("replacement_lobbies_array"), offset_dict)

    ACTOR_DEF_START = getSym("actor_defs")
    ACTOR_MASTER_TYPE_START = getSym("actor_master_types")

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
    writeFunction(ROM_COPY, 0x80712558, Overlay.Static, "getTurnedCount", offset_dict)  # Blueprint Turn-ins
    writeValue(ROM_COPY, 0x80712552, Overlay.Static, -1, offset_dict, 2, True)

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

    writeHook(ROM_COPY, 0x8061A4C8, Overlay.Static, "AlterHeadSize", offset_dict)
    writeHook(ROM_COPY, 0x806198D4, Overlay.Static, "AlterHeadSize_0", offset_dict)

    writeHook(ROM_COPY, 0x8063EE08, Overlay.Static, "InstanceScriptCheck", offset_dict)
    writeHook(ROM_COPY, 0x806FF384, Overlay.Static, "ModifyCameraColor", offset_dict)
    writeHook(ROM_COPY, 0x8061E684, Overlay.Static, "SkipCutscenePans", offset_dict)
    writeHook(ROM_COPY, 0x806EA70C, Overlay.Static, "InvertCameraControls", offset_dict)
    writeHook(ROM_COPY, 0x8061CE38, Overlay.Static, "PlayCutsceneVelocity", offset_dict)
    writeHook(ROM_COPY, 0x80677C14, Overlay.Static, "FixPufftossInvalidWallCollision", offset_dict)
    writeHook(ROM_COPY, 0x805FC3FC, Overlay.Static, "EarlyFrameCode", offset_dict)
    writeHook(ROM_COPY, 0x8071417C, Overlay.Static, "displayListCode", offset_dict)
    writeHook(ROM_COPY, 0x806F8610, Overlay.Static, "GiveItemPointerToMulti", offset_dict)
    writeHook(ROM_COPY, 0x8060005C, Overlay.Static, "getLobbyExit", offset_dict)
    writeHook(ROM_COPY, 0x8060DEF4, Overlay.Static, "SaveHelmHurryCheck", offset_dict)
    writeHook(ROM_COPY, 0x806F3E74, Overlay.Static, "AutowalkFix", offset_dict)
    writeHook(ROM_COPY, 0x80610948, Overlay.Static, "DynamicCodeFixes", offset_dict)
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

    writeValue(ROM_COPY, 0x8002DECE, Overlay.Bonus, 0x58, offset_dict, 1)

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
    hardBosses(ROM_COPY, settings, offset_dict)
    hitless(ROM_COPY, settings, offset_dict)
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
    if IsDDMSSelected(settings.minigames_list_selected, MinigamesListSelected.training_minigames):
        # Disable training pre-checks
        writeValue(ROM_COPY, 0x80698386, Overlay.Static, 0, offset_dict)  # Disable ability to use vines in vine barrel unless you have vines
        writeValue(ROM_COPY, 0x806E426C, Overlay.Static, 0, offset_dict, 4)  # Disable ability to pick up objects in barrel barrel unless you have barrels
        writeValue(ROM_COPY, 0x806E7736, Overlay.Static, 0, offset_dict)  # Disable ability to dive in dive barrel unless you have dive
        writeValue(ROM_COPY, 0x806E2D8A, Overlay.Static, 0, offset_dict)  # Disable ability to throw oranges in orange barrel unless you have oranges

    saveUpdates(ROM_COPY, settings, offset_dict)
    writeNewTextFiles(ROM_COPY, offset_dict)
    collisionUpdates(ROM_COPY, settings, offset_dict)

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
    allowances = getModelTwoAllowances(ROM_COPY)
    buffer = 25
    writeValue(ROM_COPY, 0x80632026, Overlay.Static, allowances[7] + buffer, offset_dict)  # Japes
    writeValue(ROM_COPY, 0x80632006, Overlay.Static, allowances[0x26] + buffer, offset_dict)  # Aztec
    writeValue(ROM_COPY, 0x80631FF6, Overlay.Static, allowances[0x1A] + buffer, offset_dict)  # Factory
    writeValue(ROM_COPY, 0x80632016, Overlay.Static, allowances[0x1E] + buffer, offset_dict)  # Galleon
    writeValue(ROM_COPY, 0x80631FE6, Overlay.Static, allowances[0x30] + buffer, offset_dict)  # Fungi
    writeValue(ROM_COPY, 0x80632036, Overlay.Static, allowances["default"] + buffer, offset_dict)  # Others

    writeFunction(ROM_COPY, 0x80732314, Overlay.Static, "CrashHandler", offset_dict)
    writeFunction(ROM_COPY, 0x8073231C, Overlay.Static, "CrashHandler", offset_dict)
    writeFunction(ROM_COPY, 0x807322DC, Overlay.Static, "getFaultedThread", offset_dict)
    # Deathwarp Handle
    if not settings.wipe_file_on_death:
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
    # Restore unused events
    writeValue(ROM_COPY, 0x800336A4, Overlay.Menu, 7, offset_dict)  # Play cutscene 7 (Overwrites one of the leg shakes)
    writeValue(ROM_COPY, 0x800336A6, Overlay.Menu, 150, offset_dict)  # Set duration as 150
    writeValue(ROM_COPY, 0x8003371A, Overlay.Menu, 8, offset_dict)  # Play cutscene 8
    writeValue(ROM_COPY, 0x8003371C, Overlay.Menu, 150, offset_dict)  # Set duration as 150
    writeFloatUpper(ROM_COPY, 0x800283D2, Overlay.Menu, 11, offset_dict)  # Set randomization function to use 11 values
    writeValue(ROM_COPY, 0x80028412, Overlay.Menu, 11 + 1, offset_dict)  # Set cap to 12
    writeValue(ROM_COPY, 0x8002845A, Overlay.Menu, 11 + 1, offset_dict)  # Set cap to 12

    grabUpdates(ROM_COPY, settings, offset_dict, spoiler)
    adjustKongModelHandlers(ROM_COPY, settings, offset_dict)
    krushaChanges(ROM_COPY, settings, offset_dict)
    raceCoinRandoASMChanges(ROM_COPY, settings, offset_dict, spoiler)
    if settings.fast_warps:
        writeValue(ROM_COPY, 0x806EE692, Overlay.Static, 0x54, offset_dict)
        writeFunction(ROM_COPY, 0x806DC2AC, Overlay.Static, "fastWarp", offset_dict)  # Modify Function Call

    # Make BBBash reference the internal hit counter rather than the displayed one
    writeValue(ROM_COPY, 0x8002B4DE, Overlay.Bonus, 0x2A, offset_dict)
    writeValue(ROM_COPY, 0x8002B502, Overlay.Bonus, 0x2A, offset_dict)
    writeValue(ROM_COPY, 0x8002B55A, Overlay.Bonus, 0x2A, offset_dict)

    # Alter amount of Klaptraps in Searchlight seek
    writeValue(ROM_COPY, 0x8002C1FA, Overlay.Bonus, KLAPTRAPS_IN_SEARCHLIGHT_SEEK, offset_dict)
    writeValue(ROM_COPY, 0x8002C1D2, Overlay.Bonus, KLAPTRAPS_IN_SEARCHLIGHT_SEEK, offset_dict)

    writeFunction(ROM_COPY, 0x8062F084, Overlay.Static, "setFog", offset_dict)
    fairyFix(ROM_COPY, settings, offset_dict)

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

    updateActorFunction(ROM_COPY, 340, "handleBugEnemy")

    writeFunction(ROM_COPY, 0x80714168, Overlay.Static, "fixHelmTimerDisable", offset_dict)

    if Types.Hint in spoiler.settings.shuffled_location_types:
        writeFunction(ROM_COPY, 0x8069E188, Overlay.Static, "loadWrinklyTextWrapper", offset_dict)
    writeFunction(ROM_COPY, 0x806FC7B8, Overlay.Static, "getCharWidthMask", offset_dict)
    writeFunction(ROM_COPY, 0x806FBE44, Overlay.Static, "getCharWidthMask", offset_dict)

    # Alter data for zinger flamethrower enemy
    writeValue(ROM_COPY, 0x8075F210, Overlay.Static, CustomActors.ZingerFlamethrower, offset_dict)
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
    writeValue(ROM_COPY, 0x8075F0F0, Overlay.Static, CustomActors.Scarab, offset_dict)
    writeValue(ROM_COPY, 0x8075F0F2, Overlay.Static, 0x118 + 1, offset_dict)
    writeValue(ROM_COPY, 0x8075F0F4, Overlay.Static, 0x281, offset_dict)
    writeValue(ROM_COPY, 0x8075F0F6, Overlay.Static, 0, offset_dict)
    writeValue(ROM_COPY, 0x8075F0F8, Overlay.Static, 1, offset_dict, 4)
    writeValue(ROM_COPY, 0x8075F0FC, Overlay.Static, 0xAA465A1E, offset_dict, 4)
    writeValue(ROM_COPY, 0x8075F100, Overlay.Static, 0x05030602, offset_dict, 4)
    writeValue(ROM_COPY, 0x8075F104, Overlay.Static, 0x5E5E0164, offset_dict, 4)
    writeValue(ROM_COPY, 0x8074B21E, Overlay.Static, 0xFF8, offset_dict)  # Allow other moves to knock down the bug
    writeLabelValue(ROM_COPY, 0x8074B244, Overlay.Static, "fixed_scarab_collision", offset_dict)  # Collision
    # Alter data for custom item
    CHAR_SPAWNER_DATA_SIZE = 0x18
    for x in range(6):
        source_addr = getROMAddress(0x8075EB80 + (0x13 * CHAR_SPAWNER_DATA_SIZE) + (x * 4), Overlay.Static, offset_dict)
        target_addr = getROMAddress(0x8075EB80 + (Enemies.CharSpawnerItem * CHAR_SPAWNER_DATA_SIZE) + (x * 4), Overlay.Static, offset_dict)
        ROM_COPY.seek(source_addr)
        val = int.from_bytes(ROM_COPY.readBytes(4), "big")
        ROM_COPY.seek(target_addr)
        ROM_COPY.writeMultipleBytes(val, 4)
    writeValue(ROM_COPY, 0x8075EB80 + (Enemies.CharSpawnerItem * CHAR_SPAWNER_DATA_SIZE), Overlay.Static, 141, offset_dict)
    guard_extra_data = {
        CustomActors.GuardDisableA: (Enemies.GuardDisableA, 0x13B),
        CustomActors.GuardDisableZ: (Enemies.GuardDisableZ, 0x13B),
        CustomActors.GuardTag: (Enemies.GuardTag, 0x13C),
        CustomActors.GuardGetOut: (Enemies.GuardGetOut, 0x13A),
    }
    for new_actor, data in guard_extra_data.items():
        new_enemy = data[0]
        new_model = data[1]
        for x in range(6):
            source_addr = getROMAddress(0x8075EB80 + (Enemies.Guard * CHAR_SPAWNER_DATA_SIZE) + (x * 4), Overlay.Static, offset_dict)
            target_addr = getROMAddress(0x8075EB80 + (new_enemy * CHAR_SPAWNER_DATA_SIZE) + (x * 4), Overlay.Static, offset_dict)
            ROM_COPY.seek(source_addr)
            val = int.from_bytes(ROM_COPY.readBytes(4), "big")
            ROM_COPY.seek(target_addr)
            ROM_COPY.writeMultipleBytes(val, 4)
        writeValue(ROM_COPY, 0x8075EB80 + (new_enemy * CHAR_SPAWNER_DATA_SIZE), Overlay.Static, new_actor, offset_dict)
        writeValue(ROM_COPY, 0x8075EB80 + (new_enemy * CHAR_SPAWNER_DATA_SIZE) + 2, Overlay.Static, new_model, offset_dict)
    writeFunction(ROM_COPY, 0x806AE4C4, Overlay.Static, "renderKopLightHandler", offset_dict)

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

    writeHook(ROM_COPY, 0x8072F3DC, Overlay.Static, "blockTreeClimbing", offset_dict)

    writeFunction(ROM_COPY, 0x80618148, Overlay.Static, "getProjectileCount_modified", offset_dict)
    writeFunction(ROM_COPY, 0x80682890, Overlay.Static, "getProjectileCount_modified", offset_dict)
    writeFunction(ROM_COPY, 0x806829D4, Overlay.Static, "getProjectileCount_modified", offset_dict)
    writeFunction(ROM_COPY, 0x806E2344, Overlay.Static, "getProjectileCount_modified", offset_dict)
    writeFunction(ROM_COPY, 0x806E2D3C, Overlay.Static, "getProjectileCount_modified", offset_dict)
    # Button Ban Controls
    writeFunction(ROM_COPY, 0x8071294C, Overlay.Static, "applyButtonBansInternals", offset_dict)
    writeValue(ROM_COPY, 0x80712982, Overlay.Static, getHiSym("enabled_buttons"), offset_dict)
    writeValue(ROM_COPY, 0x80712986, Overlay.Static, getLoSym("enabled_buttons"), offset_dict)

    # Pushable Crate speeds (just to make it make a bit more sense) - introduce character diversity
    push_speeds = [100, 60, 40, 40, 130]
    for index, value in enumerate(push_speeds):
        writeFloat(ROM_COPY, 0x807534E4 + (4 * index), Overlay.Static, value, offset_dict)

    # Reduce TA Cooldown
    writeFunction(ROM_COPY, 0x806F5BE8, Overlay.Static, "tagAnywhereAmmo", offset_dict)
    writeFunction(ROM_COPY, 0x806F5A08, Overlay.Static, "tagAnywhereBunch", offset_dict)
    writeFunction(ROM_COPY, 0x806F6CB4, Overlay.Static, "tagAnywhereInit", offset_dict)
    # Fix Origin Warp with TA
    writeFunction(ROM_COPY, 0x8072F1E8, Overlay.Static, "handleGrabbingLock", offset_dict)
    writeFunction(ROM_COPY, 0x806CAB68, Overlay.Static, "handleLedgeLock", offset_dict)
    writeFunction(ROM_COPY, 0x80678F18, Overlay.Static, "handlePushLock", offset_dict)
    writeFunction(ROM_COPY, 0x8072F458, Overlay.Static, "handleActionSet", offset_dict)  # Actor grabbables
    writeFunction(ROM_COPY, 0x8072F46C, Overlay.Static, "handleActionSet", offset_dict)  # Model 2 grabbables
    writeFunction(ROM_COPY, 0x806CFC64, Overlay.Static, "handleActionSet", offset_dict)  # Ledge Grabbing
    writeFunction(ROM_COPY, 0x806E5418, Overlay.Static, "handleActionSet", offset_dict)  # Instrument Play
    writeFunction(ROM_COPY, 0x806E6064, Overlay.Static, "handleActionSet", offset_dict)  # Gun Pull
    #
    writeValue(ROM_COPY, 0x806F6D94, Overlay.Static, 0, offset_dict, 4)  # Prevent delayed collection
    writeValue(ROM_COPY, 0x806F5B68, Overlay.Static, 0x1000, offset_dict)  # Standard Ammo
    writeValue(ROM_COPY, 0x806F59A8, Overlay.Static, 0x1000, offset_dict)  # Bunch
    writeValue(ROM_COPY, 0x806F6CA8, Overlay.Static, 0x00052C03, offset_dict, 4)  # SRA $a1, $a1, 0x10
    writeValue(ROM_COPY, 0x806F6CAC, Overlay.Static, 0x9204001A, offset_dict, 4)  # LBU $a0, 0x1A ($s0)
    writeValue(ROM_COPY, 0x806F6CB0, Overlay.Static, 0x86060002, offset_dict, 4)  # LH $a2, 0x2 ($s0)
    writeValue(ROM_COPY, 0x806F6CB8, Overlay.Static, 0x86070000, offset_dict, 4)  # LH #a3, 0x0 ($s0)
    writeValue(ROM_COPY, 0x806F53AC, Overlay.Static, 0, offset_dict, 4)  # Prevent LZ case
    writeValue(ROM_COPY, 0x806C7088, Overlay.Static, 0x1000, offset_dict)  # Mech fish dying

    if settings.bonus_barrel_auto_complete:
        writeValue(ROM_COPY, 0x806818DE, Overlay.Static, 0x4248, offset_dict)  # Make Aztec Lobby GB spawn above the trapdoor)
        writeValue(ROM_COPY, 0x80681690, Overlay.Static, 0, offset_dict, 4)  # Make some barrels not play a cutscene
        writeValue(ROM_COPY, 0x8068188C, Overlay.Static, 0, offset_dict, 4)  # Prevent disjoint mechanic for Caves/Fungi BBlast Bonus
        writeValue(ROM_COPY, 0x80681898, Overlay.Static, 0x1000, offset_dict)
        writeValue(ROM_COPY, 0x8068191C, Overlay.Static, 0, offset_dict, 4)  # Remove Oh Banana
        writeValue(ROM_COPY, 0x80680986, Overlay.Static, 0xFFFE, offset_dict)  # Prevent Factory BBBandit Bonus dropping
        writeValue(ROM_COPY, 0x806809C8, Overlay.Static, 0x1000, offset_dict)  # Prevent Fungi TTTrouble Bonus dropping
        writeValue(ROM_COPY, 0x80681962, Overlay.Static, 1, offset_dict)  # Make bonus noclip
        writeValue(ROM_COPY, 0x8068183C, Overlay.Static, 0, offset_dict, 4)  # Remove the explosion
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
    elif IsDDMSSelected(settings.hard_mode_selected, HardModeSelected.strict_helm_timer):
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
        writeValue(ROM_COPY, 0x806AA458, Overlay.Static, 0, offset_dict, 4)  # Show CBs on Pause Menu (Main Screen)
        writeValue(ROM_COPY, 0x806AA858, Overlay.Static, 0, offset_dict, 4)  # Show CBs on Pause Menu (Level Kong Screen)
        # TODO: Work on Level Totals screen - this one is a bit more complicated

    writeFunction(ROM_COPY, 0x8002D6A8, Overlay.Bonus, "warpOutOfArenas", offset_dict)  # Enable the two arenas to be minigames
    writeFunction(ROM_COPY, 0x8002D31C, Overlay.Bonus, "ArenaTagKongCode", offset_dict)  # Tag Rambi/Enguarde Instantly
    writeFunction(ROM_COPY, 0x8002D6DC, Overlay.Bonus, "ArenaEarlyCompletionCheck", offset_dict)  # Check completion

    writeFunction(ROM_COPY, 0x8002D20C, Overlay.Boss, "SpiderBossExtraCode", offset_dict)  # Handle preventing spider boss being re-fightable

    pauseUpdates(ROM_COPY, settings, offset_dict)

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

    if settings.activate_all_bananaports == ActivateAllBananaports.isles:
        file_init_flags.extend(WARPS_ISLES.copy())
    elif settings.activate_all_bananaports == ActivateAllBananaports.isles_inc_helm_lobby:
        file_init_flags.extend(WARPS_ISLES.copy())
        file_init_flags.extend(WARPS_HELM_LOBBY.copy())
    elif settings.activate_all_bananaports == ActivateAllBananaports.all:
        for lvl in WARPS_TOTAL:
            file_init_flags.extend(lvl.copy())

    if settings.shuffle_items:
        for item in spoiler.item_assignment:
            if item.can_have_item and not item.is_shop and item.old_item not in (Types.Cranky, Types.Candy, Types.Funky, Types.Snide):
                if item.location < Locations.TurnInDKIslesDonkeyBlueprint or item.location > Locations.TurnInCreepyCastleChunkyBlueprint:
                    if item.new_type is None or item.new_type == Types.NoItem:
                        file_init_flags.append(item.old_flag)
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

    file_init_flags = angryCaves(ROM_COPY, settings, offset_dict, file_init_flags)

    # Bonus barrel kong check
    writeValue(ROM_COPY, 0x8073199E, Overlay.Static, getVar("BONUS_DATA_COUNT"), offset_dict)  # Set bonus count
    writeValue(ROM_COPY, 0x807319CA, Overlay.Static, 8, offset_dict)  # Set size of item
    writeValue(ROM_COPY, 0x80731996, Overlay.Static, getHiSym("bonus_data"), offset_dict)
    writeValue(ROM_COPY, 0x807319A2, Overlay.Static, getLoSym("bonus_data"), offset_dict)

    if settings.free_trade_setting:
        # Non-BP Items
        writeValue(ROM_COPY, 0x807319C0, Overlay.Static, 0x00001025, offset_dict, 4)  # OR $v0, $r0, $r0 - Make all reward spots think no kong
        # writeValue(ROM_COPY, 0x80632E94, Overlay.Static, 0x00001025, offset_dict, 4)  # OR $v0, $r0, $r0 - Make flag mapping think no kong
        writeFunction(ROM_COPY, 0x80632E94, Overlay.Static, "getItemRequiredKong", offset_dict)  # Get required kong for item, used to set Stump GB as Tiny
        writeValue(ROM_COPY, 0x806F56F8, Overlay.Static, 0, offset_dict, 4)  # Disable Flag Set for blueprints
        writeValue(ROM_COPY, 0x806A606C, Overlay.Static, 0, offset_dict, 4)  # Disable translucency for blueprints

    writeFunction(ROM_COPY, 0x806B26A0, Overlay.Static, "fireballEnemyDeath", offset_dict)
    if Types.Enemies in settings.shuffled_location_types:
        # Dropsanity
        writeFunction(ROM_COPY, 0x80729E54, Overlay.Static, "indicateCollectionStatus", offset_dict)
        writeValue(ROM_COPY, 0x807278CA, Overlay.Static, 0xFFF, offset_dict)  # Disable enemy switching in Fungi
        writeFunction(ROM_COPY, 0x806BB310, Overlay.Static, "rulerEnemyDeath", offset_dict)
        writeFunction(ROM_COPY, 0x806ADFC0, Overlay.Static, "tomatoDeath", offset_dict)
        writeHook(ROM_COPY, 0x806680B4, Overlay.Static, "checkBeforeApplyingQuicksand", offset_dict)
        writeValue(ROM_COPY, 0x806680B8, Overlay.Static, 0x8E2C0058, offset_dict, 4)  # LW $t4, 0x58 ($s1)

    remove_blockers = False
    if remove_blockers:
        for x in range(8):
            file_init_flags.append(0x1CD + x)  # B. Locker clear flag

    hardEnemies(ROM_COPY, settings, offset_dict)
    lowerReplenishibles(ROM_COPY, settings, offset_dict)

    donkInTheManySettings(ROM_COPY, settings, offset_dict)
    writeValue(ROM_COPY, 0x806AA8E8, Overlay.Static, 0x00005825, offset_dict, 4)  # Disable rendering the medal icon in the pause menu

    if settings.fungi_time_internal == FungiTimeSetting.dusk:
        writeValue(ROM_COPY, 0x806C5614, Overlay.Static, 0x50000006, offset_dict, 4)
        writeValue(ROM_COPY, 0x806BE8F8, Overlay.Static, 0x50000008, offset_dict, 4)
        # Coloring
        if not IsDDMSSelected(settings.hard_mode_selected, HardModeSelected.donk_in_the_dark_world):
            writeFloat(ROM_COPY, 0x80748280, Overlay.Static, 0.6, offset_dict)
            writeFloat(ROM_COPY, 0x80748284, Overlay.Static, 0.6, offset_dict)
            writeFloat(ROM_COPY, 0x80748288, Overlay.Static, 0.3, offset_dict)
            writeFloat(ROM_COPY, 0x8074828C, Overlay.Static, 0.6, offset_dict)
            writeFloat(ROM_COPY, 0x80748290, Overlay.Static, 0.6, offset_dict)
            writeFloat(ROM_COPY, 0x80748294, Overlay.Static, 0.3, offset_dict)
    elif not IsDDMSSelected(settings.hard_mode_selected, HardModeSelected.donk_in_the_dark_world):
        writeFloat(ROM_COPY, 0x80748288, Overlay.Static, 0.3, offset_dict)

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

    # Jetpac Platforms
    if settings.puzzle_rando_difficulty in (PuzzleRando.medium, PuzzleRando.hard, PuzzleRando.chaos):
        # Move platforms
        writeValue(ROM_COPY, 0x80028C5E, Overlay.Jetpac, settings.jetpac_platform_data[0][0], offset_dict)
        writeValue(ROM_COPY, 0x80028C62, Overlay.Jetpac, settings.jetpac_platform_data[0][1], offset_dict)
        writeValue(ROM_COPY, 0x80028C6A, Overlay.Jetpac, settings.jetpac_platform_data[0][2], offset_dict)
        writeValue(ROM_COPY, 0x80028C7E, Overlay.Jetpac, settings.jetpac_platform_data[1][0], offset_dict)
        writeValue(ROM_COPY, 0x80028C82, Overlay.Jetpac, settings.jetpac_platform_data[1][1], offset_dict)
        writeValue(ROM_COPY, 0x80028C86, Overlay.Jetpac, settings.jetpac_platform_data[1][2], offset_dict)
        writeValue(ROM_COPY, 0x80028CA6, Overlay.Jetpac, settings.jetpac_platform_data[2][0], offset_dict)
        writeValue(ROM_COPY, 0x80028CAA, Overlay.Jetpac, settings.jetpac_platform_data[2][1], offset_dict)
        writeValue(ROM_COPY, 0x80028CAE, Overlay.Jetpac, settings.jetpac_platform_data[2][2], offset_dict)
        # Move Rocket segments
        px_0 = settings.jetpac_platform_data[0][0]
        py_0 = settings.jetpac_platform_data[0][1]
        pw_0 = settings.jetpac_platform_data[0][2]
        px_1 = settings.jetpac_platform_data[1][0]
        py_1 = settings.jetpac_platform_data[1][1]
        pw_1 = settings.jetpac_platform_data[1][2]
        writeFloatUpper(ROM_COPY, 0x800276DA, Overlay.Jetpac, px_0 + (pw_0 * 4), offset_dict)
        writeFloatUpper(ROM_COPY, 0x800276E2, Overlay.Jetpac, py_0 - 16, offset_dict)
        writeFloatUpper(ROM_COPY, 0x800276EA, Overlay.Jetpac, px_1 + (pw_1 * 4), offset_dict)
        writeFloatUpper(ROM_COPY, 0x800276F2, Overlay.Jetpac, py_1 - 16, offset_dict)

    writeHook(ROM_COPY, 0x805FE954, Overlay.Static, "ArcadeMapCheck", offset_dict)
    writeHook(ROM_COPY, 0x80024FD4, Overlay.Arcade, "ArcadeIntroCheck", offset_dict)
    writeFunction(ROM_COPY, 0x800288FC, Overlay.Jetpac, "completeJetpac", offset_dict)
    writeFunction(ROM_COPY, 0x80024BD0, Overlay.Jetpac, "exitJetpac", offset_dict)
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
    else:
        writeFunction(ROM_COPY, 0x806324D4, Overlay.Static, "getKongOwnershipFromFlag", offset_dict)
    writeFunction(ROM_COPY, 0x8064936C, Overlay.Static, "getKongOwnershipFromFlag", offset_dict)
    writeFunction(ROM_COPY, 0x80682F40, Overlay.Static, "getKongOwnershipFromFlag", offset_dict)
    writeFunction(ROM_COPY, 0x806840D8, Overlay.Static, "getKongOwnershipFromFlag", offset_dict)
    writeFunction(ROM_COPY, 0x806FA340, Overlay.Static, "getKongOwnershipFromFlag", offset_dict)
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
    writeHook(ROM_COPY, 0x806A88C8, Overlay.Static, "ExitMapHook", offset_dict)
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

    expandActorTable(ROM_COPY, settings, offset_dict)
    writeValue(ROM_COPY, 0x80755DCC, Overlay.Static, 93, offset_dict)

    # Uncontrollable Fixes
    writeFunction(ROM_COPY, 0x806F56E0, Overlay.Static, "getFlagIndex_Corrected", offset_dict)  # BP Acquisition - Correct for character
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
        TableNames.Cutscenes,
        TableNames.Setups,
        TableNames.InstanceScripts,
        TableNames.Text,
        TableNames.Spawners,
        TableNames.Triggers,
        TableNames.RaceCheckpoints,
    ]
    overlays_being_compressed = [
        TableNames.Unknown6,
    ]
    for ovl in overlays_being_decompressed:
        writeValue(ROM_COPY, 0x80748E18 + ovl, Overlay.Static, 0, offset_dict, 1)
    for ovl in overlays_being_compressed:
        writeValue(ROM_COPY, 0x80748E18 + ovl, Overlay.Static, 1, offset_dict, 1)

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

    # Make music uncompressed
    writeValue(ROM_COPY, 0x8060A2A8, Overlay.Static, 0x00001025, offset_dict, 4)  # or v0, zero, zero
    writeValue(ROM_COPY, 0x8060A32C, Overlay.Static, 0, offset_dict, 4)  # nop
    writeValue(ROM_COPY, 0x8060A31E, Overlay.Static, 0, offset_dict)
    writeValue(ROM_COPY, 0x8060A30A, Overlay.Static, 0, offset_dict)

    # Make music not interrupt itself
    writeFunction(ROM_COPY, 0x8060A378, Overlay.Static, "playMusicDontStop", offset_dict)

    # Soundplayer Fix
    writeValue(ROM_COPY, 0x80735C9E, Overlay.Static, 0xFFFF, offset_dict)  # initSoundPlayer creates the event
    writeValue(ROM_COPY, 0x80735D0E, Overlay.Static, 0xFFFF, offset_dict)  # __sndpVoiceHandler checks for the event
    writeValue(ROM_COPY, 0x80735D26, Overlay.Static, 0xFFFF, offset_dict)  # __sndpVoiceHandler creates the event

    if HARDER_CRUSHERS:
        writeValue(ROM_COPY, 0x8064C520, Overlay.Static, 0xA218006E, offset_dict, 4)  # Make the crushers in Factory Crusher Room always damage you
    # Diddy Slam Crash Fix
    writeHook(ROM_COPY, 0x80609338, Overlay.Static, "fixDiddySlamCrash", offset_dict)

    # Fix Null Lag Boost
    writeHook(ROM_COPY, 0x806CCA90, Overlay.Static, "fixNullLagBoost", offset_dict)

    if settings.win_condition_spawns_ship and not (settings.helm_hurry and settings.archipelago):
        writeValue(ROM_COPY, 0x80029706, Overlay.Menu, getHiSym("k_rool_text"), offset_dict)
        writeValue(ROM_COPY, 0x8002970A, Overlay.Menu, getLoSym("k_rool_text"), offset_dict)
        writeFloatUpper(ROM_COPY, 0x800296D2, Overlay.Menu, 280, offset_dict)
        writeFloatUpper(ROM_COPY, 0x800296D6, Overlay.Menu, 192, offset_dict)
        writeValue(ROM_COPY, 0x8002974E, Overlay.Menu, 0x3ECC, offset_dict)
        writeValue(ROM_COPY, 0x80029752, Overlay.Menu, 0xCCCD, offset_dict)
        writeFloat(ROM_COPY, 0x80033CA4, Overlay.Menu, 1, offset_dict)
    else:
        writeValue(ROM_COPY, 0x8002975C, Overlay.Menu, 0x02401025, offset_dict, 4)
        writeValue(ROM_COPY, 0x80029760, Overlay.Menu, 0, offset_dict, 4)

    if settings.less_fragile_boulders:
        # Thrown boulders/vases/etc require getting thrown at a wall to destroy
        writeValue(ROM_COPY, 0x8069C1C2, Overlay.Static, 4, offset_dict)  # Contact with wall: Destroy
        writeValue(ROM_COPY, 0x8069C99E, Overlay.Static, 2, offset_dict)  # Contact with floor: Remain intact
        writeValue(ROM_COPY, 0x8069C9CA, Overlay.Static, 2, offset_dict)  # Contact with water: Remain intact
    if CAN_THROW_KEGS:
        # Can throw keys
        writeValue(ROM_COPY, 0x806E4C8C, Overlay.Static, 0, offset_dict, 4)  # Kegs (Grounded)
        writeValue(ROM_COPY, 0x806E4D30, Overlay.Static, 0, offset_dict, 4)  # Kegs (Non-Grounded)
    if CAN_THROW_APPLES:
        # Can throw the Apple
        writeValue(ROM_COPY, 0x806E4C94, Overlay.Static, 0, offset_dict, 4)  # Apple (Grounded)
        writeValue(ROM_COPY, 0x806E4D38, Overlay.Static, 0, offset_dict, 4)  # Apple (Non-Grounded)

    if DISABLE_LONG_JUMP:
        writeFloatUpper(ROM_COPY, 0x806E30E6, Overlay.Static, 8000000, offset_dict)
        writeValue(ROM_COPY, 0x806D81E4, Overlay.Static, 0, offset_dict, 4)  # Removes a set to 0 for backflips, making them feel better

    if settings.shops_dont_cost:
        writeValue(ROM_COPY, 0x8064EA8C, Overlay.Static, 0, offset_dict, 4)  # Remove Arcade Costing Coins

    # Adjust Exit File
    writeFunction(ROM_COPY, 0x805FEAE4, Overlay.Static, "loadExits", offset_dict)
    writeHook(ROM_COPY, 0x806C97E0, Overlay.Static, "adjustExitRead", offset_dict)
    writeValue(ROM_COPY, 0x805FF1CC, Overlay.Static, 0x2009FFFF, offset_dict, 4)  # Set default void location to be exit -1 instead of exit 0
    writeValue(ROM_COPY, 0x805FF220, Overlay.Static, 0x87A9, offset_dict)  # Change LHU to LH
    writeValue(ROM_COPY, 0x805FF278, Overlay.Static, 0x87A9, offset_dict)  # Change LHU to LH
    writeValue(ROM_COPY, 0x805FF2D0, Overlay.Static, 0x87A9, offset_dict)  # Change LHU to LH

    if IsDDMSSelected(settings.hard_mode_selected, HardModeSelected.fast_balloons):
        writeFunction(ROM_COPY, 0x806A7774, Overlay.Static, "setHardPathSpeed", offset_dict)

    # Boot setup checker optimization
    writeFunction(ROM_COPY, 0x805FEB00, Overlay.Static, "bootSpeedup", offset_dict)  # Modify Function Call
    writeValue(ROM_COPY, 0x805FEB08, Overlay.Static, 0, offset_dict, 4)  # Cancel 2nd check

    # Crowd Control Stuff
    writeFunction(ROM_COPY, 0x805FEDC8, Overlay.Static, "handleGamemodeWrapper", offset_dict)  # disable skipping the rap
    writeFloat(ROM_COPY, 0x8075EB4C, Overlay.Static, -2.5, offset_dict)  # Have the initial moonkick accel reading from a "const" addr
    writeValue(ROM_COPY, 0x806EB618, Overlay.Static, 0x3C018076, offset_dict, 4)  # LUI $at, 0x8076
    writeValue(ROM_COPY, 0x806EB61C, Overlay.Static, 0xC426EB4C, offset_dict, 4)  # LWC1 $f6, 0xEB4C ($at)
    writeFunction(ROM_COPY, 0x806CA7D4, Overlay.Static, "fakeGetOut", offset_dict)
    writeHook(ROM_COPY, 0x8065F228, Overlay.Static, "storeWaterSurfaceCount", offset_dict)

    # Golden Banana Requirements
    order = 0
    for count in settings.BLockerEntryCount:
        ROM_COPY.seek(settings.rom_data + 0x17E + order)
        ROM_COPY.writeMultipleBytes(int(settings.BLockerEntryItems[order]), 1)
        writeValue(ROM_COPY, 0x807446D0 + (2 * order), Overlay.Static, count, offset_dict)
        order += 1

    # Jetpac Requirement
    written_requirement = settings.medal_requirement
    writeValue(ROM_COPY, 0x80026513, Overlay.Menu, written_requirement, offset_dict, 1)  # Actual requirement
    writeValue(ROM_COPY, 0x8002644B, Overlay.Menu, written_requirement, offset_dict, 1)  # Text variable
    writeValue(ROM_COPY, 0x80027583, Overlay.Menu, written_requirement, offset_dict, 1)  # Text Variable

    # Boss Key Mapping
    for i in range(7):
        for j in range(7):
            if REGULAR_BOSS_MAPS[i] == settings.boss_maps[j]:
                writeValue(ROM_COPY, KEY_FLAG_ADDRESSES[i], Overlay.Boss, NORMAL_KEY_FLAGS[j], offset_dict)

    # BFI
    writeFunction(ROM_COPY, 0x80028080, Overlay.Critter, "displayBFIMoveText", offset_dict)  # BFI Text Display
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
    elif settings.win_condition_item == WinConditionComplex.kill_the_rabbit:
        writeFunction(ROM_COPY, 0x806B2320, Overlay.Static, "winRabbitSeed", offset_dict)
        writeValue(ROM_COPY, 0x806B231A, Overlay.Static, 40, offset_dict)  # Change song that plays to success (for the laughs)
        # Make sure the rabbit always is there, even if the check is done
        writeValue(ROM_COPY, 0x80755E2C, Overlay.Static, 0, offset_dict)  # Set flag to 0 (always set)
        writeValue(ROM_COPY, 0x80755E2E, Overlay.Static, 1, offset_dict, 1)  # Set rabbit to spawn with this flag
        # Make sure the cutscene doesn't play if the rabbit reward has already been given
        writeFunction(ROM_COPY, 0x806B23B4, Overlay.Static, "safeguardRabbitReward", offset_dict)
        # Change the tied trigger map for the cutscene so that it always plays (allows you to kill the rabbit after getting it's check)
        writeValue(ROM_COPY, 0x80755F10, Overlay.Static, 0xFF, offset_dict, 1)
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

    # Pause Carousel
    check_term = getEnum("CHECK_TERMINATOR")
    writeValue(ROM_COPY, 0x806AB3F6, Overlay.Static, check_term, offset_dict)
    file_item_end = getSym("pause_items") + (8 * (check_term - 1)) + 6
    writeValue(ROM_COPY, 0x806AB2CE, Overlay.Static, getHi(file_item_end), offset_dict)
    writeValue(ROM_COPY, 0x806AB2D6, Overlay.Static, getLo(file_item_end), offset_dict)

    # HUD
    writeValue(ROM_COPY, 0x806FB246, Overlay.Static, getEnum("ITEMID_TERMINATOR"), offset_dict)
    writeValue(ROM_COPY, 0x806FABAA, Overlay.Static, getEnum("ITEMID_TERMINATOR"), offset_dict)
    writeValue(ROM_COPY, 0x806F9992, Overlay.Static, getEnum("ITEMID_RESERVED_FUNKY"), offset_dict)
    writeValue(ROM_COPY, 0x806F99AA, Overlay.Static, getEnum("ITEMID_RESERVED_CRANKY"), offset_dict)
    writeValue(ROM_COPY, 0x806F9986, Overlay.Static, getEnum("ITEMID_RESERVED_SCOFF"), offset_dict)
    writeValue(ROM_COPY, 0x806F99C6, Overlay.Static, getEnum("ITEMID_RESERVED_CANDY"), offset_dict)
    writeValue(ROM_COPY, 0x806F99DA, Overlay.Static, getEnum("ITEMID_RESERVED_DK"), offset_dict)

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

    # Boss Mapping
    for i in range(7):
        boss_map = settings.boss_maps[i]
        boss_kong = settings.boss_kongs[i]
        writeValue(ROM_COPY, 0x80744700 + (i * 2), Overlay.Static, boss_map, offset_dict)
        writeValue(ROM_COPY, 0x807446F0 + i, Overlay.Static, boss_kong, offset_dict, 1)
    for boss_map in boss_maps:
        writeValue(ROM_COPY, 0x807445E0 + boss_map, Overlay.Static, 0xD, offset_dict, 1)  # Set map as a shared map

    # Music Writes
    writeFunction(ROM_COPY, 0x80024AE0, Overlay.Bonus, "playBonusSong", offset_dict)
    writeFunction(ROM_COPY, 0x80025B6C, Overlay.Bonus, "playBonusSong", offset_dict)
    writeFunction(ROM_COPY, 0x80027EBC, Overlay.Bonus, "playBonusSong", offset_dict)
    writeFunction(ROM_COPY, 0x80028468, Overlay.Bonus, "playBonusSong", offset_dict)
    writeFunction(ROM_COPY, 0x80029B5C, Overlay.Bonus, "playBonusSong", offset_dict)
    writeFunction(ROM_COPY, 0x8002AA64, Overlay.Bonus, "playBonusSong", offset_dict)
    writeFunction(ROM_COPY, 0x8002B6F8, Overlay.Bonus, "playBonusSong", offset_dict)
    writeFunction(ROM_COPY, 0x8002C6D8, Overlay.Bonus, "playBonusSong", offset_dict)
    writeFunction(ROM_COPY, 0x80025300, Overlay.Minecart, "playBonusSong", offset_dict)
    writeFunction(ROM_COPY, 0x8002936C, Overlay.Critter, "playBonusSong", offset_dict)
    writeFunction(ROM_COPY, 0x806BBAC8, Overlay.Static, "playBossSong", offset_dict)
    writeFunction(ROM_COPY, 0x805FED60, Overlay.Static, "playSongWCheck", offset_dict)
    writeFunction(ROM_COPY, 0x8061E280, Overlay.Static, "playSongWCheck", offset_dict)
    writeFunction(ROM_COPY, 0x80629014, Overlay.Static, "playSongWCheck", offset_dict)  # also cancels Chunky Phase music
    writeFunction(ROM_COPY, 0x8064142C, Overlay.Static, "playSongWCheck", offset_dict)
    writeFunction(ROM_COPY, 0x8064143C, Overlay.Static, "playSongWCheck", offset_dict)
    writeFunction(ROM_COPY, 0x80628E40, Overlay.Static, "stopBossSong", offset_dict)  # Dogadon1, Mad Jack, Dillo2, Dillo1, Pufftoss, Dogadon2
    writeFunction(ROM_COPY, 0x80032788, Overlay.Boss, "playNotBossSong", offset_dict)  # King Kut Out, because who needs consistency, right?
    writeFunction(ROM_COPY, 0x80605600, Overlay.Static, "resetBossSong", offset_dict)  # Prevent assumption "current_boss_music != 0, so boss music is playing" from being incorrect

    writeHook(ROM_COPY, 0x806E563C, Overlay.Static, "AnyInsPadCheck", offset_dict)

    # Adding Fairy slow pitch variant
    writeValue(ROM_COPY, 0x8074564E, Overlay.Static, 0x7FFF, offset_dict)
    writeValue(ROM_COPY, 0x807457B6, Overlay.Static, 0x925, offset_dict)
    MUSIC_MIDI_OFFSET = 0x807FFA00
    SONG_COUNT = 176
    writeValue(ROM_COPY, 0x8060A2B6, Overlay.Static, getHi(MUSIC_MIDI_OFFSET), offset_dict)
    writeValue(ROM_COPY, 0x8060A2BA, Overlay.Static, getLo(MUSIC_MIDI_OFFSET), offset_dict)
    writeValue(ROM_COPY, 0x806010B2, Overlay.Static, getHi(MUSIC_MIDI_OFFSET), offset_dict)
    writeValue(ROM_COPY, 0x806010BA, Overlay.Static, getLo(MUSIC_MIDI_OFFSET), offset_dict)
    writeValue(ROM_COPY, 0x806010DA, Overlay.Static, getHi(MUSIC_MIDI_OFFSET), offset_dict)
    writeValue(ROM_COPY, 0x806010DE, Overlay.Static, getLo(MUSIC_MIDI_OFFSET), offset_dict)
    writeValue(ROM_COPY, 0x806010EE, Overlay.Static, (SONG_COUNT + 1) * 4, offset_dict)

    #
    writeHook(ROM_COPY, 0x806C3260, Overlay.Static, "fixLankyPhaseHandState", offset_dict)  # Ensures K Rool has a head in the end cutscene if in Lanky Phase
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

    # Alt Minecart Mayhem:
    if settings.alt_minecart_mayhem:
        SIZE_DEFS = getSym("actor_extra_data_sizes")
        NEW_SIZE = getSym("mayhem_minecart_size")
        writeValue(ROM_COPY, SIZE_DEFS + (87 * 4), Overlay.Custom, NEW_SIZE, offset_dict, 4)  # Increase size
        writeValue(ROM_COPY, 0x80025340, Overlay.Minecart, 0, offset_dict, 4)  # Remove timer spawn
        writeValue(ROM_COPY, 0x80025350, Overlay.Minecart, 0, offset_dict, 4)  # Prevent action on parent
        writeFunction(ROM_COPY, 0x80025070, Overlay.Minecart, "initMMayhem", offset_dict)  # Init requirements
        writeFunction(ROM_COPY, 0x80025160, Overlay.Minecart, "renderGetWrapper", offset_dict)  # Render the get counter
        writeHook(ROM_COPY, 0x80025214, Overlay.Minecart, "checkNewMayhemWin", offset_dict)
        writeValue(ROM_COPY, 0x8002407C, Overlay.Minecart, 0, offset_dict, 4)  # Prevent action on parent
        writeValue(ROM_COPY, 0x80024084, Overlay.Minecart, 0, offset_dict, 4)  # Prevent action on parent
        writeValue(ROM_COPY, 0x80024140, Overlay.Minecart, 0, offset_dict, 4)  # Prevent action on parent
        writeValue(ROM_COPY, 0x80024148, Overlay.Minecart, 0, offset_dict, 4)  # Prevent action on parent

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
    if settings.snide_reward_rando:
        writeFunction(ROM_COPY, 0x80632188, Overlay.Static, "isModelTwoTiedFlag_new", offset_dict)  # Update setup to account for snide
        writeValue(ROM_COPY, 0x8063218C, Overlay.Static, 0x02202825, offset_dict, 4)  # Modify arg
        writeValue(ROM_COPY, 0x800248B0, Overlay.Menu, 0, offset_dict, 4)  # Remove flag set
        writeValue(ROM_COPY, 0x800248C0, Overlay.Menu, 0, offset_dict, 4)  # Remove increment
        writeHook(ROM_COPY, 0x8002480C, Overlay.Menu, "HandleSnideEndReward_finish", offset_dict)
    else:
        writeValue(ROM_COPY, 0x80024054, Overlay.Menu, 0x24080001, offset_dict, 4)  # 1 GB Turn in
        writeHook(ROM_COPY, 0x8002480C, Overlay.Menu, "HandleSnideEndReward", offset_dict)
    # Menu/Shop: Candy's
    writeValue(ROM_COPY, 0x80027678, Overlay.Menu, 0x1000, offset_dict)  # Patch Candy's Shop Glitch
    writeValue(ROM_COPY, 0x8002769C, Overlay.Menu, 0x1000, offset_dict)  # Patch Candy's Shop Glitch
    # Menu/Shop: Disable Multiplayer
    writeValue(ROM_COPY, 0x800280B0, Overlay.Menu, 0, offset_dict, 4)  # Disable access
    writeValue(ROM_COPY, 0x80028A8C, Overlay.Menu, 0, offset_dict, 4)  # Lower Sprite Opacity
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

    shuffleJetpacEnemies(ROM_COPY, settings, offset_dict)
    writeFunction(ROM_COPY, 0x80025034, Overlay.Jetpac, "loadJetpacSprites_handler", offset_dict)
    writeValue(ROM_COPY, 0x800281AC, Overlay.Jetpac, 0x5000, offset_dict)  # Make Rareware Coin permanent once spawned until collected

    writeValue(ROM_COPY, 0x806BA5A8, Overlay.Static, 0x1D800003, offset_dict, 4)  # Fix some health oversights by making death if health <= 0 instead of == 0
    writeValue(ROM_COPY, 0x806BA50E, Overlay.Static, 20, offset_dict)  # Change BHDM Cooldown

    mirrorMode(ROM_COPY, settings, offset_dict)
    weakAnkles(ROM_COPY, settings, offset_dict)

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
    writeValue(ROM_COPY, 0x80024F24, Overlay.Arcade, 0, offset_dict, 4)  # Disable this only being present for story arcade
    writeFunction(ROM_COPY, 0x80024F34, Overlay.Arcade, "determineArcadeLevel", offset_dict)  # Change log
    writeValue(ROM_COPY, 0x80024F70, Overlay.Arcade, 0, offset_dict, 4)  # Prevent level set
    writeValue(ROM_COPY, 0x80024F50, Overlay.Arcade, 0, offset_dict, 4)  # Prevent level set
    # Arcade Level Order Rando
    writeFunction(ROM_COPY, 0x8002F7BC, Overlay.Arcade, "HandleArcadeVictory", offset_dict)
    writeFunction(ROM_COPY, 0x8002FA68, Overlay.Arcade, "HandleArcadeVictory", offset_dict)
    writeValue(ROM_COPY, 0x8002FA24, Overlay.Arcade, 0x1000, offset_dict)

    writeLabelValue(ROM_COPY, 0x80748088, Overlay.Static, "CrownDoorCheck", offset_dict)  # Update check on Crown Door

    writeHook(ROM_COPY, 0x806321FC, Overlay.Static, "SetupModelTwoHandler", offset_dict)  # Setup transfer for model 2
    writeHook(ROM_COPY, 0x806F7924, Overlay.Static, "ActorToModelTwoHandler", offset_dict)  # Actor transfer for model 2
    writeHook(ROM_COPY, 0x8063BA04, Overlay.Static, "ModelTwoToSetupState", offset_dict)  # Model 2 transfer to setup

    # Rainbow Ammo Static Functions
    writeFunction(ROM_COPY, 0x80694E14, Overlay.Static, "colorRainbowAmmo", offset_dict)  # Coconut Code
    writeFunction(ROM_COPY, 0x80692A34, Overlay.Static, "colorRainbowAmmo", offset_dict)  # Peanut Code
    writeFunction(ROM_COPY, 0x80692F44, Overlay.Static, "colorRainbowAmmo", offset_dict)  # Grape Code
    # writeFunction(ROM_COPY, 0x80695444, Overlay.Static, "colorRainbowAmmo", offset_dict)  # Feather Code
    writeFunction(ROM_COPY, 0x806945B0, Overlay.Static, "colorRainbowAmmo", offset_dict)  # Pineapple Code
    writeHook(ROM_COPY, 0x806F97A8, Overlay.Static, "loadHUDFunction", offset_dict)  # HUD Code
    writeHook(ROM_COPY, 0x806AB528, Overlay.Static, "loadPauseHUDFunction", offset_dict)  # HUD Code - Pause Menu
    writeValue(ROM_COPY, 0x80690CD0, Overlay.Static, 0, offset_dict, 4)  # Disable hud sprite duping
    writeValue(ROM_COPY, 0x80690CD8, Overlay.Static, 0, offset_dict, 4)  # Disable hud sprite duping
    writeValue(ROM_COPY, 0x80690D00, Overlay.Static, 0, offset_dict, 4)  # Disable hud sprite duping

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
        for x in range(4):
            patchBonus(ROM_COPY, 95 + x, offset_dict, flag=0)
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
        RemovedBarriersSelected.helm_punch_gates: [0x2A2, 0x2A3, 0x2A4, 0x2A5],
        RemovedBarriersSelected.helm_star_gates: [0x2A1],
    }
    for barrier in barrier_flags:
        if IsDDMSSelected(settings.remove_barriers_selected, barrier):
            file_init_flags.extend(barrier_flags[barrier])

    writeFunction(ROM_COPY, 0x80682A98, Overlay.Static, "resetCannonGameState", offset_dict)

    # Switchsanity
    helm_lobby_ssanity_data = settings.switchsanity_data[Switches.IslesHelmLobbyGone]
    if helm_lobby_ssanity_data.kong != Kongs.chunky or helm_lobby_ssanity_data.switch_type != SwitchType.PadMove:
        # Something other than gone
        writeValue(ROM_COPY, 0x80680E3A, Overlay.Static, getHiSym("bonus_shown"), offset_dict)
        writeValue(ROM_COPY, 0x80680E3C, Overlay.Static, 0x91EF0000 | getLoSym("bonus_shown"), offset_dict, 4)  # lbu $t7, lo(bonus_shown) ($t7)
        writeValue(ROM_COPY, 0x80680E48, Overlay.Static, 0, offset_dict, 4)  # nop
        writeValue(ROM_COPY, 0x80680E54, Overlay.Static, 0x51E00009, offset_dict, 4)  # beql $t7, $zero, 0x9
    mport_ssanity_data = settings.switchsanity_data[Switches.IslesMonkeyport]
    if mport_ssanity_data.kong == Kongs.donkey and mport_ssanity_data.switch_type == SwitchType.PadMove:
        # Blast
        writeValue(ROM_COPY, 0x806E5A4A, Overlay.Static, getHiSym("blastWarpHandler"), offset_dict)
        writeValue(ROM_COPY, 0x806E5A4E, Overlay.Static, getLoSym("blastWarpHandler"), offset_dict)

    if settings.enemy_kill_crown_timer:
        writeFunction(ROM_COPY, 0x8072AC80, Overlay.Static, "handleCrownTimer", offset_dict)
        writeFunction(ROM_COPY, 0x806AEEBC, Overlay.Static, "klumpCrownHandler", offset_dict)

    if settings.crown_door_item == BarrierItems.Nothing:
        file_init_flags.append(0x304)
    if settings.coin_door_item == BarrierItems.Nothing:
        file_init_flags.append(0x303)

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

    # Replace ; with &
    writeValue(ROM_COPY, 0x80754AC2, Overlay.Static, 38, offset_dict, 1)  # Replace the character checking
    writeValue(ROM_COPY, 0x807548D8, Overlay.Static, 122, offset_dict)  # Character start
    writeValue(ROM_COPY, 0x807548DA, Overlay.Static, 11, offset_dict, 1)  # Character width

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
    dropTableUpdates(ROM_COPY, settings, offset_dict)

    # Write File init flags - Always keep at the end
    file_init_flags = list(set(file_init_flags))  # Make sure it only contains unique values
    if len(file_init_flags) > 0x3FF:
        raise Exception("Too many file init flags. Please report this to the devs with a setting string.")
    ROM_COPY.seek(0x1FFD800)
    for flag in file_init_flags:
        ROM_COPY.writeMultipleBytes(flag, 2)
    ROM_COPY.writeMultipleBytes(0xFFFF, 2)
