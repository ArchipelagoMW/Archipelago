"""Write ASM data for cosmetic elements."""

import random
from randomizer.Patching.Library.ASM import *
from randomizer.Patching.Library.Generic import (
    getHoliday,
    Holidays,
    getHolidaySetting,
    compatible_background_textures,
    MenuTextDim,
    IsColorOptionSelected,
    IsDDMSSelected,
)
from randomizer.Patching.Library.Image import getBonusSkinOffset, ExtraTextures, getRandomHueShift, hueShiftImageFromAddress, TextureFormat, hueShiftColor
from randomizer.Patching.MiscSetupChanges import SpeedUpFungiRabbit
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Models import Model, Sprite
from randomizer.Enums.Settings import ColorblindMode, ExcludedSongs, KongModels, ColorOptions
from randomizer.Patching.Patcher import ROM


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


ENABLE_MINIGAME_SPRITE_RANDO = False
GREATER_CAMERA_CONTROL = True
CROSSHAIRS = {
    ColorblindMode.off: ColorBlindCrosshair(0xC80000, 0x00C800, 0xFFD700),
    ColorblindMode.prot: ColorBlindCrosshair(0x0072FF, 0xFFFFFF, 0xFDE400),
    ColorblindMode.deut: ColorBlindCrosshair(0x318DFF, 0xFFFFFF, 0xE3A900),
    ColorblindMode.trit: ColorBlindCrosshair(0xC72020, 0xFFFFFF, 0x13C4D8),
}


def modelCosmetics(ROM_COPY: ROM, settings, offset_dict: dict):
    """Write cosmetic options related to models."""
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

    kong_model_setting_values = [
        settings.kong_model_dk,
        settings.kong_model_diddy,
        settings.kong_model_lanky,
        settings.kong_model_tiny,
        settings.kong_model_chunky,
    ]
    for kong_index, value in enumerate(kong_model_setting_values):
        if value in (KongModels.cranky, KongModels.candy, KongModels.funky):
            writeValue(ROM_COPY, 0x8075C410 + (kong_index * 0x10) + 0xC, Overlay.Static, 0, offset_dict, 4)
        elif value == KongModels.disco_chunky and kong_index == Kongs.chunky:
            writeValue(ROM_COPY, 0x806CF37C, Overlay.Static, 0, offset_dict, 4)  # Fix object holding
            writeValue(ROM_COPY, 0x806F1274, Overlay.Static, 0, offset_dict, 4)  # Prevent model change for GGone
            writeValue(ROM_COPY, 0x806CBB84, Overlay.Static, 0, offset_dict, 4)  # Enable opacity filter GGone
            writeValue(ROM_COPY, 0x8075BF3E, Overlay.Static, 0x2F5C, offset_dict)  # Make CS Model Behave normally
    if settings.beetle_model == Model.Rabbit:
        writeValue(ROM_COPY, 0x8075ECD2, Overlay.Static, 0x47, offset_dict)  # Model
        writeValue(ROM_COPY, 0x8075ECD4, Overlay.Static, 0x309, offset_dict)
        writeValue(ROM_COPY, 0x80024ADE, Overlay.Race, 0x305, offset_dict)
        writeValue(ROM_COPY, 0x80025006, Overlay.Race, 0x305, offset_dict)
        writeValue(ROM_COPY, 0x800241E6, Overlay.Race, 0x303, offset_dict)
        writeValue(ROM_COPY, 0x800251B2, Overlay.Race, 0x307, offset_dict)
        writeValue(ROM_COPY, 0x80025246, Overlay.Race, 0x308, offset_dict)
        # Fix spinning
        writeValue(ROM_COPY, 0x80025112, Overlay.Race, 0xEE, offset_dict)
        writeValue(ROM_COPY, 0x80025114, Overlay.Race, 0x0140C021, offset_dict, 4)

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

    writeValue(ROM_COPY, 0x8064F052, Overlay.Static, settings.wrinkly_rgb[0], offset_dict)
    writeValue(ROM_COPY, 0x8064F04A, Overlay.Static, settings.wrinkly_rgb[1], offset_dict)
    writeValue(ROM_COPY, 0x8064F046, Overlay.Static, settings.wrinkly_rgb[2], offset_dict)


def holidayCosmetics(ROM_COPY: ROM, settings, offset_dict: dict):
    """Write cosmetic optiosn related to Holiday mode."""
    holiday = getHoliday(settings)
    # Skybox Handler
    skybox_rgba = None
    random_skybox = False
    if settings.colorblind_mode != ColorblindMode.off:
        skybox_rgba = [0x31, 0x33, 0x38]
    elif getHolidaySetting(settings):
        skybox_rgba = [0, 0, 0]
    elif IsColorOptionSelected(settings, ColorOptions.environment):
        random_skybox = True
    if skybox_rgba is not None or random_skybox:
        for x in range(8):
            used_arr = skybox_rgba
            if random_skybox:
                used_arr = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            if used_arr is not None:
                # Calculate secondary blend
                backup_rgb = used_arr.copy()
                exceeded = False
                for y in range(3):
                    used_arr[y] = int(used_arr[y] * 2)
                    if used_arr[y] > 255:
                        exceeded = True
                if exceeded:
                    for y in range(3):
                        used_arr[y] = int(backup_rgb[y] * 0.3)
                used_arr = list(hueShiftColor(tuple(used_arr), 60))
                # Write secondary blend
                for y in range(4):
                    for zi, z in enumerate(used_arr):
                        channel = z
                        if y == 0:
                            channel = backup_rgb[zi]
                        writeValue(ROM_COPY, 0x80754EF8 + (12 * x) + (y * 3) + zi, Overlay.Static, channel, offset_dict, 1)
        writeValue(ROM_COPY, 0x8075E1EC, Overlay.Static, 0x80708234, offset_dict, 4)
        # Improve blend code
        writeValue(ROM_COPY, 0x80754D7A, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 2
        writeValue(ROM_COPY, 0x80754D8A, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 3
        writeValue(ROM_COPY, 0x80754D9A, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 2
        writeValue(ROM_COPY, 0x80754DAA, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 3
        writeValue(ROM_COPY, 0x80754DBA, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 2
        writeValue(ROM_COPY, 0x80754DCA, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 3
        #
        writeValue(ROM_COPY, 0x80754DFA, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 2
        writeValue(ROM_COPY, 0x80754E0A, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 3
        writeValue(ROM_COPY, 0x80754E1A, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 2
        writeValue(ROM_COPY, 0x80754E2A, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 3
        writeValue(ROM_COPY, 0x80754E3A, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 2
        writeValue(ROM_COPY, 0x80754E4A, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 3
        #
        writeValue(ROM_COPY, 0x80754E7A, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 2
        writeValue(ROM_COPY, 0x80754E8A, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 3
        writeValue(ROM_COPY, 0x80754E9A, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 2
        writeValue(ROM_COPY, 0x80754EAA, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 3
        writeValue(ROM_COPY, 0x80754EBA, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 2
        writeValue(ROM_COPY, 0x80754ECA, Overlay.Static, 0x3C0, offset_dict)  # Adjust y of vtx 3
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


def musicCosmetics(ROM_COPY: ROM, settings, offset_dict: dict):
    """Write cosmetic options related to music."""
    if IsDDMSSelected(settings.excluded_songs_selected, ExcludedSongs.pause_music):
        writeValue(ROM_COPY, 0x805FC890, Overlay.Static, 0, offset_dict, 4)  # Pause Theme
        writeValue(ROM_COPY, 0x805FC89C, Overlay.Static, 0, offset_dict, 4)  # Pause Start Theme
    if IsDDMSSelected(settings.excluded_songs_selected, ExcludedSongs.wrinkly):
        writeValue(ROM_COPY, 0x8064F180, Overlay.Static, 0, offset_dict, 4)  # Wrinkly Theme
    if IsDDMSSelected(settings.excluded_songs_selected, ExcludedSongs.transformation):
        writeValue(ROM_COPY, 0x8067E9E4, Overlay.Static, 0, offset_dict, 4)  # Transform Theme
        writeValue(ROM_COPY, 0x8067F7C0, Overlay.Static, 0, offset_dict, 4)  # Transform Theme
    if IsDDMSSelected(settings.excluded_songs_selected, ExcludedSongs.sub_areas):
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
    if settings.music_rando_enabled:
        writeFloat(ROM_COPY, 0x807565D8, Overlay.Static, 1, offset_dict)  # Funky and Candy volumes
        writeValue(ROM_COPY, 0x80604B50, Overlay.Static, 0, offset_dict, 4)  # Disable galleon outside track isolation
        writeValue(ROM_COPY, 0x80604A54, Overlay.Static, 0, offset_dict, 4)  # Disable galleon outside track isolation
        writeValue(ROM_COPY, 0x80028F3E, Overlay.Boss, 10000, offset_dict)  # Crowd Volume
        writeValue(ROM_COPY, 0x8002904E, Overlay.Boss, 10000, offset_dict)  # Crowd Volume
        writeValue(ROM_COPY, 0x80025192, Overlay.Bonus, 10000, offset_dict)  # Crowd Volume
        writeValue(ROM_COPY, 0x80025166, Overlay.Bonus, 10000, offset_dict)  # Crowd Volume
        writeValue(ROM_COPY, 0x80025112, Overlay.Bonus, 10000, offset_dict)  # Crowd Volume


def arcadeCosmetics(ROM_COPY: ROM, settings, offset_dict: dict):
    """Write cosmetic options related to arcade."""
    if IsColorOptionSelected(settings, ColorOptions.enemies):
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
        dk_shift = getRandomHueShift()  # 48x48
        for addr in dk_addresses:
            rom_addr = getROMAddress(addr, Overlay.Arcade, offset_dict)
            hueShiftImageFromAddress(ROM_COPY, rom_addr, 48, 41, TextureFormat.RGBA5551, dk_shift)
    if IsColorOptionSelected(settings, ColorOptions.playable_characters):
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

        jumpman_shift = getRandomHueShift()  # 16x16 except for 1 image
        for addr in jumpman_addresses:
            width = 16
            if addr == 0x8003DA90:
                width = 8
            rom_addr = getROMAddress(addr, Overlay.Arcade, offset_dict)
            hueShiftImageFromAddress(ROM_COPY, rom_addr, width, width, TextureFormat.RGBA5551, jumpman_shift)


def cameraCosmetics(ROM_COPY: ROM, settings, offset_dict: dict):
    """Write cosmetic options related to the camera and HUD."""
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

    crosshair_img = 113 if settings.crosshair_outline else 0x38
    writeValue(ROM_COPY, 0x806FFAFE, Overlay.Static, crosshair_img, offset_dict)
    writeValue(ROM_COPY, 0x806FF116, Overlay.Static, crosshair_img, offset_dict)
    writeValue(ROM_COPY, 0x806B78DA, Overlay.Static, crosshair_img, offset_dict)


def jetpacCosmetics(ROM_COPY: ROM, settings, offset_dict: dict):
    """Write cosmetic options related to jetpac."""
    # Jetpac colors
    JETPAC_RANDOM_COLORS = False
    if JETPAC_RANDOM_COLORS:
        JETPAC_FUEL = 0x0000FF  # Default 0xFF00FF
        writeValue(ROM_COPY, 0x8002DD50, Overlay.Jetpac, (JETPAC_FUEL << 8) | 1, offset_dict, 4)  # Fuel Color
        # Rocket gauge is decided by func_jetpac_080027BE8, but it's weird because it just zeros out
        #   the green channel rather than setting a new value
        #
        JETPAC_PLATFORM_COLORS = [
            {
                "intensity": [0x88],
                "channels": [False, True, True],
            },
            {
                "intensity": [0x59],
                "channels": [True, False, True],
            },
        ]
        # Platform 0
        writeValue(ROM_COPY, 0x80028C4A, Overlay.Jetpac, JETPAC_PLATFORM_COLORS[0]["intensity"][0], offset_dict)
        for plat_index, plat in enumerate([0x80028C4C, 0x80028C54, 0x80028C58]):
            j_channel_enabled = JETPAC_PLATFORM_COLORS[0]["channels"][plat_index]
            base = 0xAFAE0000 if j_channel_enabled else 0xAFA00000
            writeValue(ROM_COPY, plat, Overlay.Jetpac, base | (0x10 + (4 * plat_index)), offset_dict, 4)
        # Platform 1
        writeValue(ROM_COPY, 0x80028C72, Overlay.Jetpac, JETPAC_PLATFORM_COLORS[0]["intensity"][0], offset_dict)
        for plat_index, plat in enumerate([0x80028C74, 0x80028C88, 0x80028C90]):
            j_channel_enabled = JETPAC_PLATFORM_COLORS[0]["channels"][plat_index]
            base = 0xAFAF0000 if j_channel_enabled else 0xAFA00000
            writeValue(ROM_COPY, plat, Overlay.Jetpac, base | (0x10 + (4 * plat_index)), offset_dict, 4)
        # Platform 2
        writeValue(ROM_COPY, 0x80028C9A, Overlay.Jetpac, JETPAC_PLATFORM_COLORS[0]["intensity"][0], offset_dict)
        for plat_index, plat in enumerate([0x80028C9C, 0x80028CB0, 0x80028CB8]):
            j_channel_enabled = JETPAC_PLATFORM_COLORS[0]["channels"][plat_index]
            base = 0xAFB80000 if j_channel_enabled else 0xAFA00000
            writeValue(ROM_COPY, plat, Overlay.Jetpac, base | (0x10 + (4 * plat_index)), offset_dict, 4)
        # Base Platform
        writeValue(ROM_COPY, 0x80028CC2, Overlay.Jetpac, JETPAC_PLATFORM_COLORS[1]["intensity"][0], offset_dict)
        writeValue(ROM_COPY, 0x80028CC6, Overlay.Jetpac, JETPAC_PLATFORM_COLORS[1]["intensity"][0], offset_dict)
        for plat_index, plat in enumerate([0x80028CC8, 0x80028CCC, 0x80028CE4]):
            j_channel_enabled = JETPAC_PLATFORM_COLORS[1]["channels"][plat_index]
            base = 0xAFA80000 if j_channel_enabled else 0xAFA00000
            writeValue(ROM_COPY, plat, Overlay.Jetpac, base | (0x10 + (4 * plat_index)), offset_dict, 4)


def otherCosmetics(ROM_COPY: ROM, settings, offset_dict: dict):
    """Write cosmetic options related to other elements."""
    troff_light = 1 if settings.troff_brighten else 0.15
    writeFloat(ROM_COPY, 0x8075B8B0, Overlay.Static, troff_light, offset_dict)

    if settings.remove_water_oscillation:
        writeValue(ROM_COPY, 0x80661B54, Overlay.Static, 0, offset_dict, 4)  # Remove Ripple Timer 0
        writeValue(ROM_COPY, 0x80661B64, Overlay.Static, 0, offset_dict, 4)  # Remove Ripple Timer 1
        writeValue(ROM_COPY, 0x8068BDF4, Overlay.Static, 0, offset_dict, 4)  # Disable rocking in Seasick Ship
        writeValue(ROM_COPY, 0x8068BDFC, Overlay.Static, 0x1000, offset_dict)  # Disable rocking in Mech Fish
        writeValue(ROM_COPY, 0x805FCCEE, Overlay.Static, 0, offset_dict)  # Disable seasick camera effect

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

    # ------------------------
    # SOUND / DISPLAY SETTINGS
    # ------------------------
    # Sound Type
    writeValue(ROM_COPY, 0x80745844, Overlay.Static, int(settings.sound_type), offset_dict, 1)

    # Widescreen
    writeValue(ROM_COPY, 0x807444C0, Overlay.Static, int(settings.anamorphic_widescreen), offset_dict, 1)

    # SFX Volume
    sfx_volume = 40
    if settings.sfx_volume is not None and settings.sfx_volume != "":
        sfx_volume = int(settings.sfx_volume / 2.5)
    writeValue(ROM_COPY, 0x8074583C, Overlay.Static, sfx_volume, offset_dict, 1)
    # Music Volume
    music_volume = 40
    if settings.music_volume is not None and settings.music_volume != "":
        music_volume = int(settings.music_volume / 2.5)
    writeValue(ROM_COPY, 0x80745840, Overlay.Static, music_volume, offset_dict, 1)
