"""Write ASM data for the hard mode elements."""

from enum import IntEnum
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.ASM import *
from randomizer.Patching.Library.Generic import IsDDMSSelected
from randomizer.Patching.Library.ItemRando import CustomActors
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Settings import HardModeSelected, DamageAmount, MiscChangesSelected, HardBossesSelected, ExtraCutsceneSkips

POP_TARGETTING = True


class KKOPhaseBehavior(IntEnum):
    """KKO Phase Behavior enum."""

    normal = 0
    two_kko = 1
    aha = 2
    rapid_rotation = 3


def writeActorHealth(ROM_COPY, actor_index: int, new_health: int):
    """Write actor health value."""
    start = getSym("actor_health_damage") + (4 * actor_index)
    writeValue(ROM_COPY, start, Overlay.Custom, new_health, {})


def angryCaves(ROM_COPY: LocalROM, settings, offset_dict: dict, file_init_flags: list) -> list:
    """All changes related to angry caves."""
    if IsDDMSSelected(settings.hard_mode_selected, HardModeSelected.angry_caves):
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
    elif IsDDMSSelected(settings.misc_changes_selected, MiscChangesSelected.calm_caves):
        file_init_flags.append(0x12C)  # Giant Kosha Dead
    return file_init_flags


def hardEnemies(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to hard enemies."""
    if IsDDMSSelected(settings.hard_mode_selected, HardModeSelected.hard_enemies):
        writeValue(ROM_COPY, 0x806B12DA, Overlay.Static, 0x3A9, offset_dict)  # Kasplat Shockwave Chance
        writeValue(ROM_COPY, 0x806B12FE, Overlay.Static, 0x3B3, offset_dict)  # Kasplat Shockwave Chance
        for actor in (259, CustomActors.GuardTag, CustomActors.GuardDisableA, CustomActors.GuardDisableZ, CustomActors.GuardGetOut):
            writeActorHealth(ROM_COPY, actor, 9)  # Increase kop health


def weakAnkles(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to reduced fall damage threshold."""
    if IsDDMSSelected(settings.hard_mode_selected, HardModeSelected.reduced_fall_damage_threshold):
        writeFloatUpper(ROM_COPY, 0x806D3682, Overlay.Static, 100, offset_dict)  # Change fall too far threshold
        writeFunction(ROM_COPY, 0x806D36B4, Overlay.Static, "fallDamageWrapper", offset_dict)
        writeFunction(ROM_COPY, 0x8067F540, Overlay.Static, "transformBarrelImmunity", offset_dict)
        writeFunction(ROM_COPY, 0x8068B178, Overlay.Static, "factoryShedFallImmunity", offset_dict)


def mirrorMode(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to mirror mode."""
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


def shuffleJetpacEnemies(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to shuffling Jetpac enemies."""
    if IsDDMSSelected(settings.hard_mode_selected, HardModeSelected.shuffled_jetpac_enemies):
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


def donkInTheManySettings(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to dark world/sky/fire sea."""
    if IsDDMSSelected(settings.hard_mode_selected, HardModeSelected.water_is_lava):
        writeValue(ROM_COPY, 0x806677C4, Overlay.Static, 0, offset_dict, 4)  # Dynamic Surfaces
        # Static Surfaces
        writeValue(ROM_COPY, 0x80667ED2, Overlay.Static, 0x81, offset_dict)
        writeValue(ROM_COPY, 0x80667EDA, Overlay.Static, 0x81, offset_dict)
        writeValue(ROM_COPY, 0x80667EEE, Overlay.Static, 0x81, offset_dict)
        writeValue(ROM_COPY, 0x80667EFA, Overlay.Static, 0x81, offset_dict)
        writeFunction(ROM_COPY, 0x8062F3F0, Overlay.Static, "replaceWaterTexture", offset_dict)  # Static water textures
    is_dark_world = IsDDMSSelected(settings.hard_mode_selected, HardModeSelected.donk_in_the_dark_world)
    is_sky = IsDDMSSelected(settings.hard_mode_selected, HardModeSelected.donk_in_the_sky)
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


def lowerReplenishibles(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to lower replenishible amounts."""
    if IsDDMSSelected(settings.hard_mode_selected, HardModeSelected.lower_max_refill_amounts):
        writeValue(ROM_COPY, 0x806F8F68, Overlay.Static, 0x24090000, offset_dict, 4)  # Standard Ammo: change from `(1 << ammo_belt) * 50` to a flat 50
        writeValue(ROM_COPY, 0x806F8FE4, Overlay.Static, 0x24190000, offset_dict, 4)  # Homing Ammo: change from `(1 << ammo_belt) * 50` to a flat 50
        writeValue(ROM_COPY, 0x806F9056, Overlay.Static, 5, offset_dict)  # Oranges: change from `(5 * ammo_belt) + 20` to `(5 * ammo_belt) + 5`
        writeValue(ROM_COPY, 0x806F90B6, Overlay.Static, 10 * 150, offset_dict)  # Crystals: change from `20 + fairy_count` to `10 + fairy_count`
        writeValue(ROM_COPY, 0x806F9186, Overlay.Static, 3, offset_dict)  # Film: change from `10 + fairy_count` to `3 + fairy_count`
        writeValue(ROM_COPY, 0x806F90C8, Overlay.Static, 0x24040000 | (10 * 150), offset_dict, 4)  # set min coconuts to 1500 (10 crystals)


def getKKOPhasePosition(settings, behavior: KKOPhaseBehavior) -> int:
    """Get the phase index of a certain phase pattern."""
    for index, phase in enumerate(settings.kko_phase_order):
        if phase == behavior:
            return index
    return 0xFF


def hardBosses(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to hard bossees."""
    if IsDDMSSelected(settings.hard_bosses_selected, HardBossesSelected.kut_out_phase_rando):
        writeValue(ROM_COPY, 0x800320DE, Overlay.Boss, getKKOPhasePosition(settings, KKOPhaseBehavior.aha), offset_dict)
        writeValue(ROM_COPY, 0x80032166, Overlay.Boss, getKKOPhasePosition(settings, KKOPhaseBehavior.aha), offset_dict)
        writeValue(ROM_COPY, 0x800321F6, Overlay.Boss, getKKOPhasePosition(settings, KKOPhaseBehavior.aha), offset_dict)
        writeValue(ROM_COPY, 0x80032202, Overlay.Boss, getKKOPhasePosition(settings, KKOPhaseBehavior.rapid_rotation), offset_dict)
        # 0x80032566 = enemy spawn check
        # 0x8003259A = last phase check
        writeValue(ROM_COPY, 0x80032816, Overlay.Boss, getKKOPhasePosition(settings, KKOPhaseBehavior.rapid_rotation), offset_dict)
        writeValue(ROM_COPY, 0x80032876, Overlay.Boss, getKKOPhasePosition(settings, KKOPhaseBehavior.aha), offset_dict)
        writeValue(ROM_COPY, 0x800329D6, Overlay.Boss, getKKOPhasePosition(settings, KKOPhaseBehavior.two_kko), offset_dict)
        writeValue(ROM_COPY, 0x8003305E, Overlay.Boss, getKKOPhasePosition(settings, KKOPhaseBehavior.two_kko), offset_dict)
    if IsDDMSSelected(settings.hard_bosses_selected, HardBossesSelected.fast_mad_jack):
        # MJ Fast Jumps
        for x in range(5):
            speed = 2 if x == 0 else 3
            writeFloat(ROM_COPY, 0x80036C40 + (4 * x), Overlay.Boss, speed, offset_dict)  # Phase x Jump speed
        writeValue(ROM_COPY, 0x8003343A, Overlay.Boss, 0x224, offset_dict)  # Force fast jumps

    if IsDDMSSelected(settings.hard_bosses_selected, HardBossesSelected.k_rool_toes_rando):
        # Random Toes
        for x in range(5):
            writeValue(ROM_COPY, 0x80036950 + (4 * x) + 2, Overlay.Boss, settings.toe_order[x], offset_dict, 1)
            writeValue(ROM_COPY, 0x80036968 + (4 * x) + 2, Overlay.Boss, settings.toe_order[x + 5], offset_dict, 1)

    if IsDDMSSelected(settings.hard_bosses_selected, HardBossesSelected.beta_lanky_phase):
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


def hitless(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """Items related to hitless."""
    if settings.wipe_file_on_death:
        writeFunction(ROM_COPY, 0x8071292C, Overlay.Static, "hitlessDeath", offset_dict)
        writeFunction(ROM_COPY, 0x807128FC, Overlay.Static, "hitlessDeath", offset_dict)
        writeFunction(ROM_COPY, 0x807128C8, Overlay.Static, "hitlessDeath", offset_dict)
