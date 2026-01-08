from __future__ import annotations

from dataclasses import dataclass

from . import conditions
from .constants import AVArea, AVRegions, AP_ID_BASE
from .types import AccessRule


@dataclass
class AVLocationData:
    id: int
    area_name: str
    location_name: str
    region_name: str
    access_rule: AccessRule

    def __post_init__(self):
        self.id += AP_ID_BASE
        self.name = f'{self.area_name} - {self.location_name}' if self.area_name else self.location_name


# Start Region, Destination Region, Access Rule, Bidirectional
# NOTE: several regions are bidirectional=False if they are dead-ends without spawns to avoid creating an unnecessary entrance
entrance_data: tuple[tuple[str, str, AccessRule, bool]] = (
    (AVRegions.WEST_ERIBU, AVRegions.UPPER_ERIBU, conditions.can_damage, True),
    (AVRegions.WEST_ERIBU, AVRegions.DINGER_GISBAR, conditions.dingergisbar_access, False),
    (AVRegions.WEST_ERIBU, AVRegions.LABORATORY, conditions.can_displacement_warp, False),
    (AVRegions.DINGER_GISBAR, AVRegions.BLURST, conditions.always_accessible, False),
    (AVRegions.UPPER_ERIBU, AVRegions.XEDUR, conditions.xedur_access, False),
    (AVRegions.UPPER_ERIBU, AVRegions.LABORATORY, conditions.laboratory_access, False),
    (AVRegions.UPPER_ERIBU, AVRegions.LOWER_ERIBU, conditions.can_drill, True),
    (AVRegions.UPPER_ERIBU, AVRegions.LOWER_ERIBU, conditions.floor_grapple_clip, False, "Eribu Grapple Clip Exit"),
    (AVRegions.LOWER_ERIBU, AVRegions.ERIBU_UKKIN_NA, lambda s, c: conditions.has_glitch_2(s, c) or conditions.has_red_coat(s, c), True),
    (AVRegions.ERIBU_UKKIN_NA, AVRegions.WEST_UKKIN_NA_EXIT, conditions.always_accessible, True),
    (
        AVRegions.LOWER_ERIBU,
        AVRegions.ERIBU_INDI,
        lambda s, c: conditions.has_drone_tele(s, c) or conditions.has_trenchcoat(s, c) or conditions.has_grapple(s, c),
        False,
    ),
    (AVRegions.ERIBU_INDI, AVRegions.LOWER_ERIBU, conditions.any_height, False),
    (AVRegions.ERIBU_INDI, AVRegions.WEST_INDI, conditions.always_accessible, True),
    (AVRegions.LOWER_ERIBU, AVRegions.WEST_ABSU, conditions.always_accessible, True),
    (AVRegions.WEST_ABSU, AVRegions.WEST_ATTIC, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.can_drill(s, c), True),
    (AVRegions.WEST_ABSU, AVRegions.ELSENOVA, conditions.can_drill, True),
    (AVRegions.WEST_ABSU, AVRegions.ELSENOVA, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.roof_grapple_clip(s, c), False, "Elsenova Roof Grapple Entrance"),
    (AVRegions.WEST_ABSU, AVRegions.ABSU_BASEMENT, conditions.basement_regular_access, False),
    (
        AVRegions.WEST_ABSU,
        AVRegions.LOWER_ABSU,
        lambda s, c: conditions.can_pierce_wall(s, c) or conditions.any_coat(s, c) or conditions.any_wall_grapple_clip(s, c),
        False,
    ),
    (
        AVRegions.LOWER_ABSU,
        AVRegions.WEST_ABSU,
        lambda s, c: conditions.can_damage(s, c) or conditions.any_coat(s, c),
        False,
    ),
    (AVRegions.WEST_ATTIC, AVRegions.EAST_ATTIC, conditions.attic_transition_upper, True),
    (AVRegions.WEST_ATTIC, AVRegions.EAST_ATTIC, lambda s, c: conditions.can_drill(s, c) and conditions.has_glitch_2(s, c), False, "West to East Attic Default"),
    (AVRegions.EAST_ATTIC, AVRegions.WEST_ATTIC, lambda s, c: conditions.can_drill(s, c) and conditions.has_glitch_2(s, c), False, "East to West Attic Default"),
    (AVRegions.WEST_ATTIC, AVRegions.ELSENOVA, conditions.can_drill, False),
    (AVRegions.ELSENOVA, AVRegions.WEST_ATTIC, conditions.elsenova_west_attic_access, False),
    (AVRegions.EAST_ATTIC, AVRegions.ELSENOVA, conditions.has_glitch_2, True),
    (
        AVRegions.ELSENOVA,
        AVRegions.LOWER_ABSU,
        lambda s, c: conditions.can_pierce_wall(s, c) or conditions.any_coat(s, c) or conditions.any_wall_grapple_clip(s, c),
        False,
    ),
    (
        AVRegions.LOWER_ABSU,
        AVRegions.ELSENOVA,
        lambda s, c: conditions.can_damage(s, c) or conditions.any_coat(s, c),
        False,
    ),
    (
        AVRegions.LOWER_ABSU,
        AVRegions.ABSU_BASEMENT,
        lambda s, c: conditions.can_displacement_warp(s, c) and conditions.has_red_coat(s, c) or conditions.floor_grapple_clip(s, c),
        False,
    ),
    (AVRegions.LOWER_ABSU, AVRegions.TELAL, lambda s, c: conditions.can_damage_boss(s, c) or conditions.any_coat(s, c), False),
    (AVRegions.LOWER_ABSU, AVRegions.LOWER_CORRIDOR, lambda s, c: conditions.can_drill(s, c) or conditions.has_trenchcoat(s, c), True),
    (AVRegions.LOWER_CORRIDOR, AVRegions.EAST_ABSU, conditions.lower_east_absu_access, False),
    (AVRegions.LOWER_CORRIDOR, AVRegions.EAST_ABSU_DRONE, conditions.has_drone_launch, False),
    (AVRegions.TELAL, AVRegions.EAST_ABSU, conditions.telal_east_absu_access, False),
    (AVRegions.TELAL, AVRegions.EAST_ABSU_DRONE, conditions.has_drone_launch, False),
    (AVRegions.EAST_ABSU, AVRegions.EAST_ABSU_DRONE, conditions.has_drone, False),
    (AVRegions.EAST_ABSU, AVRegions.LOWER_CORRIDOR, lambda s, c: conditions.can_drill(s, c) or conditions.has_trenchcoat(s, c) or conditions.any_glitch(s, c), False),
    (AVRegions.EAST_ABSU, AVRegions.TELAL, conditions.any_height, False),
    (AVRegions.EAST_ABSU, AVRegions.INDI_TUNNEL, conditions.east_absu_indi_tunnel_access, False),
    (AVRegions.INDI_TUNNEL, AVRegions.EAST_ABSU, lambda s, c: conditions.swing_clip(s, c) or conditions.any_coat(s, c), False),
    (AVRegions.INDI_TUNNEL, AVRegions.INDI, conditions.non_grapple_height, False),
    (AVRegions.EAST_ABSU, AVRegions.ABSU_ZI, conditions.always_accessible, True),

    (AVRegions.ABSU_ZI, AVRegions.LOWER_ZI, conditions.always_accessible, False),
    (AVRegions.LOWER_ZI, AVRegions.ABSU_ZI, conditions.zi_vanilla_exit, False),
    (AVRegions.LOWER_ZI, AVRegions.UPPER_ZI, conditions.non_grapple_height, False),
    (AVRegions.UPPER_ZI, AVRegions.LOWER_ZI, conditions.always_accessible, False),
    (AVRegions.LOWER_ZI, AVRegions.EAST_ZI, conditions.lower_east_zi_access, True),
    (AVRegions.UPPER_ZI, AVRegions.EAST_ZI, conditions.always_accessible, False),
    (AVRegions.EAST_ZI, AVRegions.UPPER_ZI, conditions.any_height, False),
    (AVRegions.EAST_ZI, AVRegions.PREVIEW_ROOM, lambda s, c: conditions.any_coat(s, c) and conditions.any_height(s, c), False),
    (AVRegions.EAST_ZI, AVRegions.LOWER_CAVES, conditions.always_accessible, True),
    (AVRegions.UPPER_ZI, AVRegions.PREVIEW_ROOM, conditions.floor_grapple_clip, False),
    (AVRegions.UPPER_ZI, AVRegions.URUKU, conditions.non_grapple_height, False),
    (AVRegions.URUKU, AVRegions.UPPER_ZI, conditions.always_accessible, False),
    (AVRegions.URUKU, AVRegions.ZI_INDI, conditions.zi_indi_access, False),
    (AVRegions.ZI_INDI, AVRegions.URUKU, conditions.any_height, False),
    (AVRegions.ZI_INDI, AVRegions.INDI, conditions.always_accessible, True),

    (AVRegions.URUKU, AVRegions.URUKU_TOP, conditions.uruku_top_access, False),
    (AVRegions.URUKU, AVRegions.URUKU_BOTTOM, conditions.uruku_bottom_access, False),
    (AVRegions.URUKU_TOP, AVRegions.URUKU_BOTTOM, conditions.always_accessible, False),
    (AVRegions.URUKU_BOTTOM, AVRegions.URUKU_TOP, conditions.uruku_bottom_top_access, False),
    (AVRegions.URUKU_TOP, AVRegions.URUKU_BACK_LEDGE, conditions.has_grapple, False),
    (AVRegions.URUKU_BOTTOM, AVRegions.URUKU_BACK_LEDGE, conditions.uruku_bottom_back_ledge_access, False),

    (AVRegions.LOWER_CAVES, AVRegions.GAUNTLET_ENTRANCE, conditions.kur_gauntlet_entrance_access, False),
    (AVRegions.GAUNTLET_ENTRANCE, AVRegions.GAUNTLET_ROOF, conditions.kur_gauntlet_roof_access, False),
    (AVRegions.GAUNTLET_ENTRANCE, AVRegions.GIR_TAB_LOWER_ENTRANCE, conditions.can_displacement_warp, False),
    (AVRegions.GAUNTLET_ENTRANCE, AVRegions.MOUNTAIN_BASE, conditions.can_displacement_warp, False),
    (AVRegions.GAUNTLET_ROOF, AVRegions.MOUNTAIN_PEAK, conditions.kur_gauntlet_warp, False),
    (AVRegions.GAUNTLET_ROOF, AVRegions.DRONE_ODYSSEY, conditions.kur_gauntlet_warp, False),
    (AVRegions.GAUNTLET_ROOF, AVRegions.GAUNTLET_REWARD, conditions.kur_gauntlet_room_reward_access, False),
    (AVRegions.LOWER_CAVES, AVRegions.GAUNTLET_REWARD, lambda s, c: conditions.has_fat_beam(s, c) and conditions.has_trenchcoat(s, c), False),
    (AVRegions.LOWER_CAVES, AVRegions.KUR_INDI, lambda s, c: conditions.any_coat(s, c) or conditions.any_wall_grapple_clip(s, c), False),
    (AVRegions.KUR_INDI, AVRegions.LOWER_CAVES, lambda s, c: conditions.any_coat(s, c) or conditions.floor_grapple_clip(s, c), False),
    (AVRegions.UPPER_CAVES, AVRegions.KUR_INDI, lambda s, c: conditions.any_coat(s, c) or conditions.floor_grapple_clip(s, c), False),
    (AVRegions.KUR_INDI, AVRegions.UPPER_CAVES, conditions.kur_indi_upper_caves_access, False),
    (AVRegions.UPPER_CAVES, AVRegions.KUR_EDIN, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.has_glitch_2(s, c), True),
    (AVRegions.KUR_EDIN, AVRegions.EAST_EDIN, conditions.always_accessible, True),

    (AVRegions.UPPER_CAVES, AVRegions.MOUNTAIN_BASE, conditions.kur_caves_to_base_access, False),
    (AVRegions.MOUNTAIN_BASE, AVRegions.UPPER_CAVES, conditions.always_accessible, False),
    (AVRegions.MOUNTAIN_BASE, AVRegions.GIR_TAB_LOWER_ENTRANCE, conditions.gir_tab_lower_entrance_access, False),
    (AVRegions.GIR_TAB_LOWER_ENTRANCE, AVRegions.MOUNTAIN_BASE, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.has_glitch_2(s, c), False),
    (AVRegions.GIR_TAB_LOWER_ENTRANCE, AVRegions.ABOVE_GIR_TAB, conditions.gir_tab_lower_above_access, False),
    (AVRegions.ABOVE_GIR_TAB, AVRegions.GIR_TAB_LOWER_ENTRANCE, conditions.can_kill_gir_tab, False),
    (AVRegions.MOUNTAIN_BASE, AVRegions.GIR_TAB_UPPER_ENTRANCE, conditions.gir_tab_upper_entrance_access, False),
    (AVRegions.GIR_TAB_UPPER_ENTRANCE, AVRegions.MOUNTAIN_BASE, lambda s, c: conditions.can_drill(s, c) and conditions.any_height(s, c), False),
    (AVRegions.GIR_TAB_UPPER_ENTRANCE, AVRegions.ABOVE_GIR_TAB, conditions.gir_tab_upper_above_access, False),
    (AVRegions.ABOVE_GIR_TAB, AVRegions.GIR_TAB_UPPER_ENTRANCE, conditions.gir_tab_above_upper_access, False),
    (AVRegions.ABOVE_GIR_TAB, AVRegions.GRAPPLE_CLIFFS, conditions.gir_tab_grapple_cliffs_access, False),
    (AVRegions.GRAPPLE_CLIFFS, AVRegions.ABOVE_GIR_TAB, conditions.can_damage, False),
    (AVRegions.GRAPPLE_CLIFFS, AVRegions.LOWER_E_KUR_MAH, conditions.has_red_coat, False),

    (AVRegions.MOUNTAIN_BASE, AVRegions.MOUNTAIN_TOP, conditions.kur_mountain_base_top_access, False),
    (AVRegions.MOUNTAIN_TOP, AVRegions.MOUNTAIN_BASE, conditions.always_accessible, False),
    (AVRegions.MOUNTAIN_TOP, AVRegions.MOUNTAIN_PEAK, conditions.kur_mountain_top_peak_access, False),
    (AVRegions.MOUNTAIN_PEAK, AVRegions.MOUNTAIN_TOP, conditions.always_accessible, False),

    (AVRegions.MOUNTAIN_PEAK, AVRegions.UPPER_E_KUR_MAH, conditions.kur_upper_e_kur_mah_access, False),
    (AVRegions.MOUNTAIN_PEAK, AVRegions.DRONE_ODYSSEY, conditions.kur_peak_odyssey_access, False),

    (AVRegions.WEST_INDI, AVRegions.INDI, conditions.any_height, False),
    (AVRegions.INDI, AVRegions.WEST_INDI, conditions.always_accessible, False),
    (AVRegions.INDI, AVRegions.INDI_TUNNEL, conditions.always_accessible, False),
    (AVRegions.INDI, AVRegions.LOWER_EDIN, conditions.indi_edin_access, False),
    (AVRegions.INDI, AVRegions.EAST_INDI, conditions.always_accessible, False),
    (AVRegions.INDI, AVRegions.BLURST, conditions.always_accessible, False),
    (AVRegions.EAST_INDI, AVRegions.INDI, conditions.indi_east_taxi_access, False),
    (AVRegions.KUR_INDI, AVRegions.EAST_INDI, conditions.always_accessible, True),
    (AVRegions.INDI, AVRegions.SOUTH_UKKIN_NA_EXIT, conditions.indi_ukkin_na_access, False),

    (AVRegions.WEST_UKKIN_NA_EXIT, AVRegions.UKKIN_NA_BASE, conditions.any_coat, True),
    (AVRegions.UKKIN_NA_BASE, AVRegions.VISION, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.has_high_jump(s, c), False),
    (AVRegions.UKKIN_NA_BASE, AVRegions.OPHELIA, conditions.ophelia_ascent_access, True),
    (AVRegions.OPHELIA, AVRegions.BLURST, conditions.has_trenchcoat, False),
    (AVRegions.OPHELIA, AVRegions.SOUTH_UKKIN_NA_EXIT, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.swing_clip(s, c), False),
    (AVRegions.SOUTH_UKKIN_NA_EXIT, AVRegions.OPHELIA, lambda s, c: conditions.any_coat(s, c) or conditions.swing_clip(s, c), False),
    (AVRegions.SOUTH_UKKIN_NA_EXIT, AVRegions.EAST_UKKIN_NA_EXIT, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.swing_clip(s, c), True),
    (AVRegions.EAST_UKKIN_NA_EXIT, AVRegions.LOWER_EDIN, conditions.always_accessible, True),
    (AVRegions.SOUTH_UKKIN_NA_EXIT, AVRegions.INDI, conditions.ukkin_na_indi_access, False),

    (AVRegions.LOWER_EDIN, AVRegions.UKHU, conditions.ukhu_access, False),
    (AVRegions.UKHU, AVRegions.LOWER_EDIN, conditions.ukhu_exit_access, False),
    (AVRegions.LOWER_EDIN, AVRegions.CLONE, conditions.vanilla_clone_access, False),
    (AVRegions.CLONE, AVRegions.LOWER_EDIN, conditions.has_trenchcoat, False),
    (AVRegions.LOWER_EDIN, AVRegions.HANGAR, conditions.edin_hangar_left_access, True),
    (AVRegions.CLONE, AVRegions.HANGAR, conditions.clone_to_hangar_access, False),
    (AVRegions.HANGAR, AVRegions.EAST_EDIN, conditions.has_glitch_bomb, True),
    (AVRegions.LOWER_EDIN, AVRegions.INDI, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.floor_grapple_clip(s, c), False),

    (AVRegions.UPPER_E_KUR_MAH, AVRegions.KEY_CHAMBER, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.has_drone_tele(s, c), False),
    (AVRegions.UPPER_E_KUR_MAH, AVRegions.MOUNTAIN_PEAK, conditions.e_kur_mah_upper_peak_access, False),
    (AVRegions.KEY_CHAMBER, AVRegions.MID_E_KUR_MAH, lambda s, c: conditions.floor_grapple_clip(s, c), False),
    (AVRegions.UPPER_E_KUR_MAH, AVRegions.MID_E_KUR_MAH, lambda s, c: conditions.has_red_coat(s, c) or conditions.has_sudran_key(s, c), False),
    (AVRegions.MID_E_KUR_MAH, AVRegions.UPPER_E_KUR_MAH, conditions.e_kur_mah_mid_upper_access, False),
    (AVRegions.MID_E_KUR_MAH, AVRegions.LOWER_E_KUR_MAH, conditions.always_accessible, False),
    (AVRegions.LOWER_E_KUR_MAH, AVRegions.MID_E_KUR_MAH, conditions.e_kur_mah_lower_mid_access, False),
    (AVRegions.LOWER_E_KUR_MAH, AVRegions.GRAPPLE_CLIFFS, conditions.e_kur_mah_lower_cliffs_access, False),

    (AVRegions.OPHELIA, AVRegions.MAR_URU_ENTRANCE, conditions.mar_uru_access, False),
    (AVRegions.MAR_URU_ENTRANCE, AVRegions.POST_SENTINEL, conditions.post_sentinel_access, False),
    (AVRegions.POST_SENTINEL, AVRegions.SENTRY_BOT_ROOM, lambda s, c: conditions.has_glitch_2(s, c) or conditions.floor_grapple_clip(s, c), False),
    (AVRegions.POST_SENTINEL, AVRegions.ATHETOS, conditions.always_accessible, False),

    # Microregions (Separated for sanity)
    (AVRegions.EAST_ABSU, AVRegions.EA_LEDGE, lambda s, c: conditions.can_drill(s, c) or conditions.any_glitch(s, c), False),
    (AVRegions.EAST_ABSU_DRONE, AVRegions.EA_LEDGE, conditions.always_accessible, False),
    (AVRegions.EAST_ABSU, AVRegions.EA_BEHIND_TELAL, conditions.always_accessible, False),
    (AVRegions.EAST_ABSU_DRONE, AVRegions.EA_BEHIND_TELAL, conditions.always_accessible, False),
    (AVRegions.EAST_ABSU, AVRegions.EA_ALCOVE, conditions.can_drill, False),
    (AVRegions.EAST_ABSU_DRONE, AVRegions.EA_ALCOVE, conditions.always_accessible, False),
    (AVRegions.EAST_ABSU, AVRegions.EA_HIDDEN_SHRINE, lambda s, c: conditions.any_wall_grapple_clip(s, c) or conditions.any_coat(s, c) and conditions.any_height(s, c), False),
    (AVRegions.EAST_ABSU_DRONE, AVRegions.EA_HIDDEN_SHRINE, conditions.always_accessible, False),
    (AVRegions.EAST_ABSU, AVRegions.EA_CHASM_TUNNEL, conditions.has_red_coat, False),
    (AVRegions.EAST_ABSU_DRONE, AVRegions.EA_CHASM_TUNNEL, conditions.always_accessible, False),
    (AVRegions.EAST_ABSU, AVRegions.EA_ZI_ENTRANCE, conditions.can_drill, False),
    (AVRegions.EAST_ABSU_DRONE, AVRegions.EA_ZI_ENTRANCE, conditions.always_accessible, False),
)


location_data: tuple[AVLocationData] = (
    AVLocationData(0, AVArea.ERIBU, 'Starter Weapon', AVRegions.WEST_ERIBU, conditions.always_accessible),
    AVLocationData(1, AVArea.ERIBU, 'Wheelchair Room', AVRegions.WEST_ERIBU, lambda s, c: conditions.can_displacement_warp(s, c) or conditions.has_drone_tele(s, c)),
    AVLocationData(2, AVArea.ERIBU, 'Primordial Cave Lower', AVRegions.WEST_ERIBU, conditions.west_caves_pool_access),

    AVLocationData(3, AVArea.ERIBU, 'Primordial Cave Upper', AVRegions.DINGER_GISBAR, conditions.always_accessible),

    AVLocationData(4, AVArea.ERIBU, 'Right Tower', AVRegions.UPPER_ERIBU, conditions.can_damage),
    AVLocationData(5, AVArea.ERIBU, 'Left Tower', AVRegions.UPPER_ERIBU, conditions.upper_eribu_bomb_access),
    AVLocationData(6, AVArea.ERIBU, 'Bubble Shrine', AVRegions.UPPER_ERIBU, conditions.bubble_jail_access),
    AVLocationData(7, AVArea.ERIBU, 'Outside Upper Passcode Room', AVRegions.UPPER_ERIBU, conditions.outside_lab_access),

    AVLocationData(8, AVArea.ERIBU, 'Xedur Reward', AVRegions.XEDUR, conditions.can_damage_boss),
    AVLocationData(9, AVArea.ERIBU, 'Below Xedur', AVRegions.XEDUR, conditions.can_drill),

    AVLocationData(10, AVArea.ERIBU, 'Upper Passcode Room', AVRegions.LABORATORY, conditions.always_accessible),

    AVLocationData(
        11,
        AVArea.ERIBU, 'Sentry Bot Tunnel',
        AVRegions.LOWER_ERIBU,
        lambda s, c: conditions.has_drone(s, c) and (conditions.floor_grapple_clip(s, c) or conditions.has_glitch_bomb(s, c)),
    ),
    AVLocationData(
        12,
        AVArea.ERIBU, 'Outside Lower Passcode Room',
        AVRegions.LOWER_ERIBU,
        lambda s, c: conditions.any_glitch(s, c) and conditions.can_damage(s, c) or conditions.has_drone(s, c) or conditions.has_grapple(s, c) or conditions.has_trenchcoat(s, c),
    ),
    AVLocationData(13, AVArea.ERIBU, 'Lower Passcode Room', AVRegions.LOWER_ERIBU, conditions.dalkhu_subtum_access),
    AVLocationData(14, AVArea.ERIBU, 'Path to Absu', AVRegions.LOWER_ERIBU, conditions.always_accessible),

    AVLocationData(
        15,
        AVArea.ERIBU, 'Path to Indi Ceiling',
        AVRegions.ERIBU_INDI,
        lambda s, c: (
            conditions.has_red_coat(s, c) and (conditions.has_grapple(s, c) or conditions.has_high_jump(s, c))
            or conditions.has_drone_tele(s, c) and conditions.any_coat(s, c)
        )
    ),

    AVLocationData(16, AVArea.ABSU, 'Entrance Shaft', AVRegions.WEST_ABSU, conditions.can_drill),
    AVLocationData(
        17,
        AVArea.ABSU, 'Absu - Entrance Shaft Vault',
        AVRegions.WEST_ABSU,
        lambda s, c: conditions.has_red_coat(s, c) or conditions.any_glitch(s, c) and (conditions.any_coat(s, c) or conditions.can_pierce_wall(s, c)),
    ),
    AVLocationData(18, AVArea.ABSU, 'Under Entrance Shaft', AVRegions.WEST_ABSU, conditions.has_drone),
    AVLocationData(19, AVArea.ABSU, 'Deep Under Entrance Shaft', AVRegions.WEST_ABSU, lambda s, c: conditions.has_drone_tele(s, c) and conditions.has_trenchcoat(s, c)),

    AVLocationData(20, AVArea.ABSU, 'Switch Cage', AVRegions.WEST_ATTIC, lambda s, c: conditions.can_pierce_wall(s, c) or conditions.any_coat(s, c)),
    AVLocationData(21, AVArea.ABSU, 'Attic Left Shrine', AVRegions.WEST_ATTIC, conditions.basic_attic_access),
    AVLocationData(22, AVArea.ABSU, 'Attic Between Glitch Barriers', AVRegions.WEST_ATTIC, conditions.attic_transition_upper),

    AVLocationData(23, AVArea.ABSU, 'Attic Right Shrine', AVRegions.EAST_ATTIC, conditions.basic_attic_access),
    AVLocationData(24, AVArea.ABSU, 'Attic Upper Alcove', AVRegions.EAST_ATTIC, conditions.attic_far_right_access),

    AVLocationData(25, AVArea.ABSU, 'Elsenova', AVRegions.ELSENOVA, conditions.always_accessible),

    AVLocationData(26, AVArea.ABSU, 'Behind Glitch Barrier', AVRegions.ABSU_BASEMENT, conditions.always_accessible),

    AVLocationData(27, AVArea.ABSU, 'Cell Near Elsenova', AVRegions.LOWER_ABSU, lambda s, c: conditions.any_coat(s, c) or conditions.floor_grapple_clip(s, c)),
    AVLocationData(28, AVArea.ABSU, 'Lowest Point', AVRegions.LOWER_ABSU, lambda s, c: conditions.any_coat(s, c) or conditions.floor_grapple_clip(s, c)),

    AVLocationData(29, AVArea.ABSU, 'Floating Platform', AVRegions.LOWER_CORRIDOR, conditions.floating_platform_access),

    AVLocationData(31, AVArea.ABSU, 'Telal Reward', AVRegions.TELAL, conditions.can_damage),

    AVLocationData(32, AVArea.ABSU, 'Path to Indi Side Room', AVRegions.INDI_TUNNEL, conditions.any_height),

    AVLocationData(33, AVArea.ABSU, 'Trapped Diatoms', AVRegions.EA_LEDGE, conditions.always_accessible),
    AVLocationData(30, AVArea.ABSU, 'Lava Hall', AVRegions.EAST_ABSU, conditions.zombie_tunnel_access),
    AVLocationData(34, AVArea.ABSU, 'Shaft Behind Telal', AVRegions.EA_BEHIND_TELAL, conditions.always_accessible),
    AVLocationData(35, AVArea.ABSU, 'Green Wall Alcove', AVRegions.EA_ALCOVE, conditions.always_accessible),
    AVLocationData(36, AVArea.ABSU, 'Hidden Shrine', AVRegions.EA_HIDDEN_SHRINE, conditions.always_accessible),
    AVLocationData(37, AVArea.ABSU, 'Chasm Room Tunnel', AVRegions.EA_CHASM_TUNNEL, conditions.always_accessible),
    AVLocationData(38, AVArea.ABSU, 'Gated Alcove', AVRegions.EAST_ABSU, conditions.gated_alcove_access),
    AVLocationData(39, AVArea.ABSU, 'Shrine Behind Glitch', AVRegions.EAST_ABSU, lambda s, c: conditions.has_red_coat(s, c) or conditions.has_glitch_2(s, c) and conditions.can_drill(s, c)),
    AVLocationData(40, AVArea.ABSU, 'Path to Zi', AVRegions.EA_ZI_ENTRANCE, conditions.always_accessible),

    AVLocationData(41, AVArea.ZI, 'False Wall Near Lower Save', AVRegions.LOWER_ZI, lambda s, c: conditions.any_coat(s, c) and conditions.any_height(s, c)),
    AVLocationData(42, AVArea.ZI, 'Disappointment Hill', AVRegions.LOWER_ZI, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.has_drone_tele(s, c) or conditions.has_high_jump(s, c)),
    AVLocationData(
        43,
        AVArea.ZI, 'Ceiling Secret Near Lower Save',
        AVRegions.LOWER_ZI,
        lambda s, c: conditions.can_drill(s, c) and (conditions.has_trenchcoat(s, c) or conditions.has_drone_tele(s, c) or conditions.has_high_jump(s, c)),
    ),
    AVLocationData(44, AVArea.ZI, 'Furglot Tunnel', AVRegions.LOWER_ZI, conditions.furglot_tunnel_access),
    AVLocationData(45, AVArea.ZI, 'False Ceiling Alcove', AVRegions.LOWER_ZI, conditions.zi_false_roof_access),

    AVLocationData(46, AVArea.ZI, 'Above Veruska', AVRegions.EAST_ZI, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.has_drone(s, c)),
    AVLocationData(47, AVArea.ZI, 'Behind Veruska Left', AVRegions.EAST_ZI, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.has_drone(s, c)),
    AVLocationData(48, AVArea.ZI, 'Behind Veruska Right', AVRegions.EAST_ZI, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.has_drone(s, c)),

    AVLocationData(49, AVArea.ZI, 'Ceiling Secret Above Preview Room', AVRegions.UPPER_ZI, lambda s, c: conditions.has_red_coat(s, c) or conditions.has_drone(s, c) or conditions.can_drill(s, c) and conditions.any_height(s, c)),
    AVLocationData(50, AVArea.ZI, 'Drone Quest Upper', AVRegions.UPPER_ZI, conditions.zi_drone_tunnel_access),
    AVLocationData(51, AVArea.ZI, 'Drone Quest Lower', AVRegions.UPPER_ZI, conditions.zi_drone_tunnel_access),

    AVLocationData(52, AVArea.ZI, 'Preview Room', AVRegions.PREVIEW_ROOM, conditions.always_accessible),

    AVLocationData(53, AVArea.ZI, 'Uruku Reward', AVRegions.URUKU_BOTTOM, conditions.always_accessible),
    AVLocationData(54, AVArea.ZI, 'Uruku Cage', AVRegions.URUKU_TOP, conditions.uruku_cage_access),
    AVLocationData(55, AVArea.ZI, 'Behind Uruku Ceiling Ledge', AVRegions.URUKU_BACK_LEDGE, conditions.always_accessible),

    AVLocationData(56, AVArea.KUR, 'Drone Tunnel Before Gauntlet', AVRegions.LOWER_CAVES, conditions.has_drone),
    AVLocationData(57, AVArea.KUR, 'High Jump Shrine', AVRegions.LOWER_CAVES, conditions.always_accessible),
    AVLocationData(58, AVArea.KUR, 'High Jump Shrine False Wall', AVRegions.LOWER_CAVES, lambda s, c: conditions.has_drone(s, c) or conditions.any_height(s, c)),
    AVLocationData(59, AVArea.KUR, 'Above Lower Save', AVRegions.LOWER_CAVES, conditions.above_lower_kur_save_access),

    AVLocationData(60, AVArea.KUR, 'Gauntlet Reward', AVRegions.GAUNTLET_REWARD, conditions.always_accessible),

    AVLocationData(61, AVArea.KUR, 'Main Shaft', AVRegions.UPPER_CAVES, conditions.always_accessible),

    AVLocationData(62, AVArea.KUR, 'Drone Side Quest', AVRegions.MOUNTAIN_BASE, lambda s, c: conditions.has_red_coat(s, c) or conditions.has_drone(s, c)),
    AVLocationData(63, AVArea.KUR, 'Above Twin Save Rooms', AVRegions.MOUNTAIN_BASE, conditions.kur_above_twin_saves_access),
    AVLocationData(64, AVArea.KUR, 'Watch for Rolling Rocks', AVRegions.MOUNTAIN_BASE, conditions.kur_floating_ledge_access),
    AVLocationData(65, AVArea.KUR, 'Inside Cliff', AVRegions.MOUNTAIN_BASE, conditions.has_red_coat),

    AVLocationData(67, AVArea.KUR, 'Drone Odyssey Secret', AVRegions.DRONE_ODYSSEY, conditions.always_accessible),
    AVLocationData(68, AVArea.KUR, 'Drone Odyssey Reward', AVRegions.DRONE_ODYSSEY, conditions.always_accessible),

    AVLocationData(66, AVArea.KUR, 'Shrine Before Drone Odyssey', AVRegions.MOUNTAIN_TOP, conditions.has_drone),
    AVLocationData(69, AVArea.KUR, 'Snowy Cliffs Ledge Upper', AVRegions.MOUNTAIN_TOP, conditions.kur_snowy_cliffs_ledge_upper_access),
    AVLocationData(70, AVArea.KUR, 'Snowy Cliffs Ledge Lower', AVRegions.MOUNTAIN_TOP, conditions.kur_snowy_cliffs_ledge_lower_access),
    AVLocationData(71, AVArea.KUR, 'Loop Room', AVRegions.MOUNTAIN_TOP, conditions.always_accessible),
    AVLocationData(72, AVArea.KUR, 'Peak Cliff Ledge', AVRegions.MOUNTAIN_TOP, conditions.kur_peak_ledge_access),

    AVLocationData(73, AVArea.KUR, 'Gir-Tab Lower Entrance Drone Tunnel', AVRegions.GIR_TAB_LOWER_ENTRANCE, conditions.gir_tab_lower_drone_tunnel_access),

    AVLocationData(74, AVArea.KUR, 'Gir-Tab Upper Entrance', AVRegions.GIR_TAB_UPPER_ENTRANCE, conditions.always_accessible),

    AVLocationData(75, AVArea.KUR, 'Cliffs Behind Gir-Tab Near Crumble Floor', AVRegions.GRAPPLE_CLIFFS, conditions.grapple_cliffs_false_floor_access),
    AVLocationData(76, AVArea.KUR, 'Cliffs Behind Gir-Tab Shrine', AVRegions.GRAPPLE_CLIFFS, conditions.grapple_cliffs_shrines_access),
    AVLocationData(77, AVArea.KUR, 'Cliffs Behind Gir-Tab Above Shrine', AVRegions.GRAPPLE_CLIFFS, conditions.grapple_cliffs_shrines_access),

    AVLocationData(78, AVArea.INDI, 'Path to Eribu', AVRegions.WEST_INDI, conditions.has_drone),
    AVLocationData(79, AVArea.INDI, 'Outside Save', AVRegions.INDI, conditions.has_trenchcoat),

    AVLocationData(81, AVArea.UKKIN_NA, 'Below Long Fall', AVRegions.UKKIN_NA_BASE, conditions.has_trenchcoat),

    AVLocationData(80, AVArea.UKKIN_NA, 'Long Fall', AVRegions.OPHELIA, conditions.has_trenchcoat),
    AVLocationData(82, AVArea.UKKIN_NA, 'Secret Room Above Lower Save', AVRegions.OPHELIA, conditions.ukkin_na_secret_floor_access),
    AVLocationData(83, AVArea.UKKIN_NA, 'Past the Slugs', AVRegions.OPHELIA, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.has_drone(s, c)),
    AVLocationData(84, AVArea.UKKIN_NA, 'Midway Shaft Lower', AVRegions.OPHELIA, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.swing_clip(s, c)),
    AVLocationData(85, AVArea.UKKIN_NA, 'Midway Shaft Upper', AVRegions.OPHELIA, conditions.always_accessible),
    AVLocationData(86, AVArea.UKKIN_NA, 'Secret Room Below Upper Save', AVRegions.OPHELIA, conditions.ukkin_na_shrine_access),
    AVLocationData(87, AVArea.UKKIN_NA, 'Above Vision Room', AVRegions.OPHELIA, conditions.ukkin_na_above_vision_chamber_access),
    AVLocationData(88, AVArea.UKKIN_NA, 'Vision Room Tunnel', AVRegions.OPHELIA, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.has_drone(s, c)),
    AVLocationData(89, AVArea.UKKIN_NA, 'Outside Ophelia', AVRegions.OPHELIA, conditions.always_accessible),
    AVLocationData(90, AVArea.UKKIN_NA, 'Above Ophelia', AVRegions.OPHELIA, conditions.ophelia_ledge_access),

    AVLocationData(91, AVArea.EDIN, 'Ceiling Near Ukkin-Na', AVRegions.LOWER_EDIN, conditions.edin_roof_ledge_access),
    AVLocationData(92, AVArea.EDIN, 'Sky Cage', AVRegions.LOWER_EDIN, conditions.roof_cage_access),
    AVLocationData(93, AVArea.EDIN, 'Central Ruins Glitch Alcove', AVRegions.LOWER_EDIN, conditions.has_glitch_bomb),
    AVLocationData(94, AVArea.EDIN, 'Secret Tunnel Near Indi', AVRegions.LOWER_EDIN, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.has_drone(s, c)),

    AVLocationData(95, AVArea.EDIN, 'Before Clone Path', AVRegions.CLONE, lambda s, c: conditions.any_glitch(s, c) or conditions.can_drill(s, c)),
    AVLocationData(96, AVArea.EDIN, 'Clone Path Inside Blocks', AVRegions.CLONE, lambda s, c: conditions.any_glitch(s, c) or conditions.can_drill(s, c)),
    AVLocationData(97, AVArea.EDIN, 'Clone Path Rooftop Ledge', AVRegions.CLONE, conditions.clone_rooftop_ledge_access),
    AVLocationData(98, AVArea.EDIN, 'Clone Path Roof Before Save', AVRegions.CLONE, conditions.clone_roof_save_access),

    AVLocationData(99, AVArea.EDIN, 'False Wall Shrine', AVRegions.UKHU, conditions.always_accessible),
    AVLocationData(100, AVArea.EDIN, 'Ukhu Path Drone Tunnel', AVRegions.UKHU, lambda s, c: conditions.has_drone_tele(s, c) and conditions.has_trenchcoat(s, c)),
    AVLocationData(101, AVArea.EDIN, 'Ukhu Path Side Room', AVRegions.UKHU, lambda s, c: conditions.has_drone_tele(s, c) and conditions.has_trenchcoat(s, c)),
    AVLocationData(102, AVArea.EDIN, 'Ukhu Path Ruins', AVRegions.UKHU, conditions.structure_ruins_access),
    AVLocationData(103, AVArea.EDIN, 'Ukhu Reward', AVRegions.UKHU, conditions.ukhu_reward_access),

    AVLocationData(104, AVArea.EDIN, 'Main Hangar', AVRegions.HANGAR, conditions.always_accessible),

    AVLocationData(105, AVArea.EDIN, 'Double Check Tunnel Left', AVRegions.EAST_EDIN, conditions.edin_double_check_tunnel_access),
    AVLocationData(106, AVArea.EDIN, 'Double Check Tunnel Right', AVRegions.EAST_EDIN, conditions.edin_double_check_tunnel_access),

    AVLocationData(107, AVArea.E_KUR_MAH, 'Entry Chamber Breakable Wall', AVRegions.UPPER_E_KUR_MAH, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.can_drill(s, c)),
    AVLocationData(108, AVArea.E_KUR_MAH, 'Key Door on Quarry Path', AVRegions.UPPER_E_KUR_MAH, lambda s, c: conditions.has_red_coat(s, c) or conditions.has_sudran_key(s, c)),

    AVLocationData(109, AVArea.E_KUR_MAH, 'Quarry Upper', AVRegions.KEY_CHAMBER, conditions.always_accessible),
    AVLocationData(110, AVArea.E_KUR_MAH, 'Quarry Lower', AVRegions.KEY_CHAMBER, conditions.always_accessible),

    AVLocationData(111, AVArea.E_KUR_MAH, 'East Shaft Wall Alcove', AVRegions.MID_E_KUR_MAH, conditions.has_red_coat),

    AVLocationData(112, AVArea.E_KUR_MAH, 'Passcode Alcove', AVRegions.LOWER_E_KUR_MAH, conditions.e_kur_mah_passcode_check_access),
    AVLocationData(113, AVArea.E_KUR_MAH, 'Hidden Drone Tunnel', AVRegions.LOWER_E_KUR_MAH, conditions.e_kur_mah_drone_tunnel_access),
    AVLocationData(114, AVArea.E_KUR_MAH, 'Final Chamber Upper', AVRegions.LOWER_E_KUR_MAH, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.can_drill(s, c)),
    AVLocationData(115, AVArea.E_KUR_MAH, 'Final Chamber Lower', AVRegions.LOWER_E_KUR_MAH, conditions.has_red_coat),

    AVLocationData(116, AVArea.MAR_URU, 'Sentinel Reward', AVRegions.POST_SENTINEL, conditions.sentinel_alcove_access),
    AVLocationData(117, AVArea.MAR_URU, 'Quantum Sentry', AVRegions.SENTRY_BOT_ROOM, conditions.always_accessible),
    AVLocationData(118, AVArea.MAR_URU, 'Quantum Sentry Basement', AVRegions.SENTRY_BOT_ROOM, conditions.always_accessible),
    AVLocationData(119, AVArea.MAR_URU, 'Quantum Sentry Basement Secret', AVRegions.SENTRY_BOT_ROOM, conditions.always_accessible),
    AVLocationData(120, AVArea.MAR_URU, 'Inside Corridor Block', AVRegions.POST_SENTINEL, conditions.always_accessible),
    AVLocationData(121, AVArea.MAR_URU, 'Before Laser Bot Puzzle', AVRegions.POST_SENTINEL, conditions.always_accessible),
    AVLocationData(122, AVArea.MAR_URU, 'Laser Bot Puzzle', AVRegions.POST_SENTINEL, lambda s, c: conditions.has_glitch_2(s, c) or conditions.has_fat_beam(s, c)),
    AVLocationData(123, AVArea.MAR_URU, 'Athethos Ascent Drone Tunnel', AVRegions.POST_SENTINEL, conditions.has_drone),

    AVLocationData(124, '', 'Glitch a Blurst', AVRegions.BLURST, conditions.any_glitch),
)


LOCATION_NAME_TO_ID: dict[str, int] = {
    data.name: data.id for data in location_data
}

def build_location_groups() -> dict[str, set[str]]:
    location_groups = {}
    for area in AVArea:
        location_groups[area.value] = {location.name for location in location_data if location.area_name == area}

    return location_groups
