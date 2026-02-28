"""Write ASM data for the actor elements."""

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Settings import KongModels
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.ASM import *


def expandActorTable(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to the expansion of the actor table."""
    # Actor Expansion
    ACTOR_COLLISION_START = getSym("actor_collisions")
    ACTOR_HEALTH_START = getSym("actor_health_damage")
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


def adjustKongModelHandlers(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to the handling of kong model changes."""
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


def updateActorFunction(ROM_COPY, actor_index: int, new_function_sym: str):
    """Update the actor function in the table based on a sym value."""
    start = getSym("actor_functions") + (4 * actor_index)
    writeLabelValue(ROM_COPY, start, Overlay.Custom, new_function_sym, {})


def updateActorFunctionInt(ROM_COPY, actor_index: int, new_function: int):
    """Update the actor function in the table based on a int value."""
    start = getSym("actor_functions") + (4 * actor_index)
    writeValue(ROM_COPY, start, Overlay.Custom, new_function, {}, 4)


ORANGE_GUN_SFX = 400
ORANGE_GUN_VARIANCE = 5
KONG_PELLETS = [48, 36, 42, 43, 38]


def krushaChanges(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """Coding changes relevant for Krusha."""
    # These would normally reside in Cosmetic.py, but Krusha is a non-cosmetic model swap, so it has to reside in here

    kong_model_setting_values = [
        settings.kong_model_dk,
        settings.kong_model_diddy,
        settings.kong_model_lanky,
        settings.kong_model_tiny,
        settings.kong_model_chunky,
    ]
    for kong_index, value in enumerate(kong_model_setting_values):
        if value in (KongModels.krool_cutscene, KongModels.krool_fight, KongModels.krusha):
            writeValue(ROM_COPY, 0x80753568 + (2 * kong_index), Overlay.Static, 175, offset_dict)  # Krusha sliding speed
            writeValue(ROM_COPY, 0x8074AB5A, Overlay.Static, 0x0040, offset_dict)  # Enables Krusha's spin attack to knock kasplats down
            writeValue(ROM_COPY, 0x8071AAC4, Overlay.Static, 0, offset_dict, 4)
            writeValue(ROM_COPY, 0x8075DBB4 + (kong_index << 2), Overlay.Static, 0x806FAE0C, offset_dict, 4)
            writeValue(ROM_COPY, 0x806E240A, Overlay.Static, 0x3E80, offset_dict)
            # Krusha properties
            ledge_hang_y = 0x80753D70
            ledge_hang_y_0 = 0x80753D8C
            potion_anim = 0x8075D380
            writeFloat(ROM_COPY, ledge_hang_y + (4 * kong_index), Overlay.Static, 31, offset_dict)
            writeFloat(ROM_COPY, ledge_hang_y_0 + (4 * kong_index), Overlay.Static, 14, offset_dict)
            writeValue(ROM_COPY, potion_anim + (2 * kong_index), Overlay.Static, 0xE, offset_dict)
            writeFunction(ROM_COPY, 0x80677E94, Overlay.Static, "adjustAnimationTables", offset_dict)  # Give Krusha animations to slot
            updateActorFunctionInt(ROM_COPY, 2 + kong_index, 0x806C9F44)
            updateActorFunction(ROM_COPY, KONG_PELLETS[kong_index], "OrangeGunCode")
            start = getSym("actor_health_damage") + (4 * KONG_PELLETS[kong_index]) + 2
            writeValue(ROM_COPY, start, Overlay.Custom, 3, offset_dict)
            # Update names
            if value == KongModels.krusha:
                writeValue(ROM_COPY, 0x8074E780 + (4 * kong_index), Overlay.Static, 0x80759288, offset_dict, 4)
                writeValue(ROM_COPY, 0x8074E85C + (4 * kong_index), Overlay.Static, 6, offset_dict, 4)
            else:
                writeValue(ROM_COPY, 0x8074E85C + (4 * kong_index), Overlay.Static, 7, offset_dict, 4)
            writeHook(ROM_COPY, 0x806F97B8, Overlay.Static, "FixKrushaAmmoHUDColor", offset_dict)
            writeHook(ROM_COPY, 0x806F97E8, Overlay.Static, "FixKrushaAmmoHUDSize", offset_dict)
            if kong_index == Kongs.donkey:
                writeValue(ROM_COPY, 0x806F0AFE, Overlay.Static, 0, offset_dict)  # Remove gun from hands in Tag Barrel
                writeValue(ROM_COPY, 0x806F0AF0, Overlay.Static, 0x24050001, offset_dict, 4)  # Fix Hand State
                writeValue(ROM_COPY, 0x806D5EC4, Overlay.Static, 0, offset_dict, 4)  # Prevent Moving Ground Attack pop up
                writeValue(ROM_COPY, 0x8064AF5E, Overlay.Static, 5, offset_dict)  # Reduce slam range for DK Dungeon GB Slam
                writeValue(ROM_COPY, 0x806E2AA2, Overlay.Static, ORANGE_GUN_SFX, offset_dict)  # SFX
                writeValue(ROM_COPY, 0x806E2AA6, Overlay.Static, ORANGE_GUN_VARIANCE, offset_dict)  # Variance
            elif kong_index == Kongs.diddy:
                writeValue(ROM_COPY, 0x806F0A6C, Overlay.Static, 0x0C1A29D9, offset_dict, 4)  # Replace hand state call
                writeValue(ROM_COPY, 0x806F0A78, Overlay.Static, 0, offset_dict, 4)  # Replace hand state call
                writeValue(ROM_COPY, 0x806E4938, Overlay.Static, 0, offset_dict, 4)  # Always run adapt code
                writeValue(ROM_COPY, 0x806E4940, Overlay.Static, 0, offset_dict, 4)  # NOP Animation calls
                writeValue(ROM_COPY, 0x806E4950, Overlay.Static, 0, offset_dict, 4)  # NOP Animation calls
                writeValue(ROM_COPY, 0x806E4958, Overlay.Static, 0, offset_dict, 4)  # NOP Animation calls
                writeValue(ROM_COPY, 0x806E499C, Overlay.Static, 0, offset_dict, 4)  # NOP Animation calls
                writeValue(ROM_COPY, 0x806E49C8, Overlay.Static, 0, offset_dict, 4)  # NOP Animation calls
                writeValue(ROM_COPY, 0x806E49F0, Overlay.Static, 0, offset_dict, 4)  # NOP Animation calls
                writeValue(ROM_COPY, 0x806CF5F0, Overlay.Static, 0x5000, offset_dict)  # Prevent blink special cases
                writeValue(ROM_COPY, 0x806CF76C, Overlay.Static, 0, offset_dict, 4)  # Prevent blink special cases
                writeValue(ROM_COPY, 0x806832B8, Overlay.Static, 0, offset_dict, 4)  # Prevent tag blinking
                writeValue(ROM_COPY, 0x806C1050, Overlay.Static, 0, offset_dict, 4)  # Prevent Cutscene Kong blinking
                writeValue(ROM_COPY, 0x8075D19F, Overlay.Static, 0xA0, offset_dict, 1)  # Fix Gun Firing
                writeValue(ROM_COPY, 0x80749764, Overlay.Static, 10, offset_dict)  # Fix Diddy Swimming (A)
                writeValue(ROM_COPY, 0x80749758, Overlay.Static, 10, offset_dict)  # Fix Diddy Swimming (B)
                writeValue(ROM_COPY, 0x8074974C, Overlay.Static, 10, offset_dict)  # Fix Diddy Swimming (Z/First Person)
                writeValue(ROM_COPY, 0x806E2AB2, Overlay.Static, ORANGE_GUN_SFX, offset_dict)  # SFX
                writeFunction(ROM_COPY, 0x806E495C, Overlay.Static, "adaptKrushaZBAnimation_Charge", offset_dict)  # Allow Krusha to use slide move if fast enough (Charge)
                writeFunction(ROM_COPY, 0x806141B4, Overlay.Static, "DiddySwimFix", offset_dict)  # Fix Diddy's Swim Animation
                writeFunction(ROM_COPY, 0x806E903C, Overlay.Static, "MinecartJumpFix", offset_dict)  # Fix Diddy Minecart Jump
                writeFunction(ROM_COPY, 0x806D259C, Overlay.Static, "MinecartJumpFix_0", offset_dict)  # Fix Diddy Minecart Jump
            elif kong_index == Kongs.lanky:
                writeValue(ROM_COPY, 0x806F0ABE, Overlay.Static, 0, offset_dict)  # Remove gun from hands in Tag Barrel
                writeValue(ROM_COPY, 0x806E48B4, Overlay.Static, 0, offset_dict, 4)  # Always run `adaptKrushaZBAnimation`
                writeValue(ROM_COPY, 0x806F0AB0, Overlay.Static, 0x24050001, offset_dict, 4)  # Fix Hand State
                writeValue(ROM_COPY, 0x80749C74, Overlay.Static, 10, offset_dict)  # Fix Lanky Swimming (A)
                writeValue(ROM_COPY, 0x80749C80, Overlay.Static, 10, offset_dict)  # Fix Lanky Swimming (B)
                writeValue(ROM_COPY, 0x80749CA4, Overlay.Static, 10, offset_dict)  # Fix Lanky Swimming (Z/First Person)
                writeValue(ROM_COPY, 0x806E2A7E, Overlay.Static, ORANGE_GUN_SFX, offset_dict)  # SFX
                writeValue(ROM_COPY, 0x806E2A86, Overlay.Static, ORANGE_GUN_VARIANCE, offset_dict)  # Variance
                writeFunction(ROM_COPY, 0x806E48BC, Overlay.Static, "adaptKrushaZBAnimation_PunchOStand", offset_dict)  # Allow Krusha to use slide move if fast enough (OStand)
                writeFunction(ROM_COPY, 0x806141B4, Overlay.Static, "DiddySwimFix", offset_dict)  # Fix Lanky's Swim Animation
            elif kong_index == Kongs.tiny:
                writeValue(ROM_COPY, 0x806F0ADE, Overlay.Static, 0, offset_dict)  # Remove gun from hands in Tag Barrel
                writeValue(ROM_COPY, 0x806E47F8, Overlay.Static, 0, offset_dict, 4)  # Prevent slide bounce
                writeValue(ROM_COPY, 0x806CF784, Overlay.Static, 0x5000, offset_dict)  # Prevent blink special cases
                writeValue(ROM_COPY, 0x806832C0, Overlay.Static, 0x5000, offset_dict)  # Prevent tag blinking
                writeValue(ROM_COPY, 0x806C1058, Overlay.Static, 0, offset_dict, 4)  # Prevent Cutscene Kong blinking
                writeValue(ROM_COPY, 0x806F0AD0, Overlay.Static, 0x24050001, offset_dict, 4)  # Fix Hand State
                writeValue(ROM_COPY, 0x806E2A8A, Overlay.Static, ORANGE_GUN_SFX, offset_dict)  # SFX
                writeValue(ROM_COPY, 0x806E2A90, Overlay.Static, 0x24030000 | ORANGE_GUN_VARIANCE, offset_dict, 4)  # Variance
                writeFloat(ROM_COPY, 0x80753E38, Overlay.Static, 350, offset_dict)
                writeValue(ROM_COPY, getSym("actor_defs") + (24 * 0x30) + 2, Overlay.Custom, 0, offset_dict)  # Model
                writeValue(ROM_COPY, getSym("actor_master_types") + 43, Overlay.Custom, 4, offset_dict, 1)  # Master Type
            elif kong_index == Kongs.chunky:
                writeValue(ROM_COPY, 0x806CF37C, Overlay.Static, 0, offset_dict, 4)  # Fix object holding
                writeValue(ROM_COPY, 0x806F1274, Overlay.Static, 0, offset_dict, 4)  # Prevent model change for GGone
                writeValue(ROM_COPY, 0x806CBB84, Overlay.Static, 0, offset_dict, 4)  # Enable opacity filter GGone
                writeValue(ROM_COPY, 0x806E48F8, Overlay.Static, 0, offset_dict, 4)  # Always run `adaptKrushaZBAnimation`
                writeValue(ROM_COPY, 0x806F0A9E, Overlay.Static, 0, offset_dict)  # Remove gun from hands in Tag Barrel
                writeValue(ROM_COPY, 0x806F0A90, Overlay.Static, 0x24050001, offset_dict, 4)  # Fix Hand State
                writeFunction(ROM_COPY, 0x806E4900, Overlay.Static, "adaptKrushaZBAnimation_PunchOStand", offset_dict)  # Allow Krusha to use slide move if fast enough (PPunch)
