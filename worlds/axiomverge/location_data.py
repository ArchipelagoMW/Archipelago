from __future__ import annotations

from dataclasses import dataclass

from . import conditions
from .constants import AVArea, AVRegion, AP_ID_BASE
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
    (AVRegion.WEST_ERIBU, AVRegion.UPPER_ERIBU, conditions.can_damage, True),
    (AVRegion.WEST_ERIBU, AVRegion.DINGER_GISBAR, conditions.dingergisbar_access, False),
    (AVRegion.WEST_ERIBU, AVRegion.LABORATORY, conditions.can_displacement_warp, False),
    (AVRegion.DINGER_GISBAR, AVRegion.BLURST, conditions.always_accessible, False),
    (AVRegion.UPPER_ERIBU, AVRegion.XEDUR, conditions.xedur_access, False),
    (AVRegion.UPPER_ERIBU, AVRegion.LABORATORY, conditions.laboratory_access, False),
    (AVRegion.UPPER_ERIBU, AVRegion.LOWER_ERIBU, conditions.can_drill, True),
    (AVRegion.UPPER_ERIBU, AVRegion.LOWER_ERIBU, conditions.floor_grapple_clip, False, "Eribu Grapple Clip Exit"),
    (AVRegion.LOWER_ERIBU, AVRegion.ERIBU_UKKIN_NA, lambda s, c: conditions.has_glitch_2(s, c) or conditions.has_red_coat(s, c), True),
    (AVRegion.ERIBU_UKKIN_NA, AVRegion.WEST_UKKIN_NA_EXIT, conditions.always_accessible, True),
    (
        AVRegion.LOWER_ERIBU,
        AVRegion.ERIBU_INDI,
        lambda s, c: conditions.has_drone_tele(s, c) or conditions.has_trenchcoat(s, c) or conditions.has_grapple(s, c),
        False,
    ),
    (AVRegion.ERIBU_INDI, AVRegion.LOWER_ERIBU, conditions.any_height, False),
    (AVRegion.ERIBU_INDI, AVRegion.WEST_INDI, conditions.always_accessible, True),
    (AVRegion.LOWER_ERIBU, AVRegion.WEST_ABSU, conditions.always_accessible, True),
    (AVRegion.WEST_ABSU, AVRegion.WEST_ATTIC, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.can_drill(s, c), True),
    (AVRegion.WEST_ABSU, AVRegion.ELSENOVA, conditions.can_drill, True),
    (AVRegion.WEST_ABSU, AVRegion.ELSENOVA, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.roof_grapple_clip(s, c), False, "Elsenova Roof Grapple Entrance"),
    (AVRegion.WEST_ABSU, AVRegion.ABSU_BASEMENT, conditions.basement_regular_access, False),
    (
        AVRegion.WEST_ABSU,
        AVRegion.LOWER_ABSU,
        lambda s, c: conditions.can_pierce_wall(s, c) or conditions.any_coat(s, c) or conditions.any_wall_grapple_clip(s, c),
        False,
    ),
    (
        AVRegion.LOWER_ABSU,
        AVRegion.WEST_ABSU,
        lambda s, c: conditions.can_damage(s, c) or conditions.any_coat(s, c),
        False,
    ),
    (AVRegion.WEST_ATTIC, AVRegion.EAST_ATTIC, conditions.attic_transition_upper, True),
    (AVRegion.WEST_ATTIC, AVRegion.ATTIC_JUNCTION, conditions.can_drill, True),
    (AVRegion.ATTIC_JUNCTION, AVRegion.EAST_ATTIC, conditions.has_glitch_2, True),

    (AVRegion.ATTIC_JUNCTION, AVRegion.ELSENOVA, conditions.always_accessible, False),
    (AVRegion.ELSENOVA, AVRegion.ATTIC_JUNCTION, conditions.elsenova_junction_access, False),

    (
        AVRegion.ELSENOVA,
        AVRegion.LOWER_ABSU,
        lambda s, c: conditions.can_pierce_wall(s, c) or conditions.any_coat(s, c) or conditions.any_wall_grapple_clip(s, c),
        False,
    ),
    (
        AVRegion.LOWER_ABSU,
        AVRegion.ELSENOVA,
        lambda s, c: conditions.can_damage(s, c) or conditions.any_coat(s, c),
        False,
    ),
    (
        AVRegion.LOWER_ABSU,
        AVRegion.ABSU_BASEMENT,
        lambda s, c: conditions.can_displacement_warp(s, c) and conditions.has_red_coat(s, c) or conditions.floor_grapple_clip(s, c),
        False,
    ),
    (AVRegion.LOWER_ABSU, AVRegion.TELAL, lambda s, c: conditions.can_damage_boss(s, c) or conditions.any_coat(s, c), False),
    (AVRegion.TELAL, AVRegion.LOWER_ABSU, conditions.absu_telal_backtrack, False),
    (AVRegion.LOWER_ABSU, AVRegion.LOWER_CORRIDOR, lambda s, c: conditions.can_drill(s, c) or conditions.has_trenchcoat(s, c), True),
    (AVRegion.LOWER_CORRIDOR, AVRegion.EAST_ABSU, conditions.lower_east_absu_access, False),
    (AVRegion.LOWER_CORRIDOR, AVRegion.EAST_ABSU_DRONE, conditions.has_drone_launch, False),
    (AVRegion.TELAL, AVRegion.EAST_ABSU, conditions.telal_east_absu_access, False),
    (AVRegion.TELAL, AVRegion.EAST_ABSU_DRONE, conditions.has_drone_launch, False),
    (AVRegion.EAST_ABSU, AVRegion.EAST_ABSU_DRONE, conditions.has_drone, False),
    (AVRegion.EAST_ABSU, AVRegion.LOWER_CORRIDOR, lambda s, c: conditions.can_drill(s, c) or conditions.has_trenchcoat(s, c) or conditions.any_glitch(s, c), False),
    (AVRegion.EAST_ABSU, AVRegion.TELAL, conditions.any_height, False),
    (AVRegion.EAST_ABSU, AVRegion.INDI_TUNNEL, conditions.east_absu_indi_tunnel_access, False),
    (AVRegion.INDI_TUNNEL, AVRegion.EAST_ABSU, lambda s, c: conditions.swing_clip(s, c) or conditions.any_coat(s, c), False),
    (AVRegion.INDI_TUNNEL, AVRegion.INDI, conditions.non_grapple_height, False),
    (AVRegion.EAST_ABSU, AVRegion.ABSU_ZI, conditions.always_accessible, True),

    (AVRegion.ABSU_ZI, AVRegion.LOWER_ZI, conditions.always_accessible, False),
    (AVRegion.LOWER_ZI, AVRegion.ABSU_ZI, conditions.zi_vanilla_exit, False),
    (AVRegion.LOWER_ZI, AVRegion.UPPER_ZI, conditions.non_grapple_height, False),
    (AVRegion.UPPER_ZI, AVRegion.LOWER_ZI, conditions.always_accessible, False),
    (AVRegion.LOWER_ZI, AVRegion.ZI_CORRIDOR, conditions.zi_corridor_access, True),
    (AVRegion.ZI_CORRIDOR, AVRegion.EAST_ZI, conditions.zi_corridor_access, True),
    (AVRegion.UPPER_ZI, AVRegion.EAST_ZI, conditions.always_accessible, False),
    (AVRegion.EAST_ZI, AVRegion.UPPER_ZI, lambda s, c: conditions.any_height(s, c) and conditions.has_ranged_weapon(s, c), False),
    (AVRegion.EAST_ZI, AVRegion.PREVIEW_ROOM, lambda s, c: conditions.any_coat(s, c) and conditions.any_height(s, c), False),
    (AVRegion.EAST_ZI, AVRegion.LOWER_CAVES, conditions.always_accessible, True),
    (AVRegion.UPPER_ZI, AVRegion.PREVIEW_ROOM, conditions.floor_grapple_clip, False),
    (AVRegion.UPPER_ZI, AVRegion.URUKU, conditions.non_grapple_height, False),
    (AVRegion.URUKU, AVRegion.UPPER_ZI, conditions.always_accessible, False),
    (AVRegion.URUKU, AVRegion.ZI_INDI, conditions.zi_indi_access, False),
    (AVRegion.ZI_INDI, AVRegion.URUKU, conditions.any_height, False),
    (AVRegion.ZI_INDI, AVRegion.INDI, conditions.always_accessible, True),

    (AVRegion.URUKU, AVRegion.URUKU_TOP, conditions.uruku_top_access, False),
    (AVRegion.URUKU, AVRegion.URUKU_BOTTOM, conditions.uruku_bottom_access, False),
    (AVRegion.URUKU_TOP, AVRegion.URUKU_BOTTOM, conditions.always_accessible, False),
    (AVRegion.URUKU_BOTTOM, AVRegion.URUKU_TOP, conditions.uruku_bottom_top_access, False),
    (AVRegion.URUKU_TOP, AVRegion.URUKU_BACK_LEDGE, conditions.has_grapple, False),
    (AVRegion.URUKU_BOTTOM, AVRegion.URUKU_BACK_LEDGE, conditions.uruku_bottom_back_ledge_access, False),

    (AVRegion.LOWER_CAVES, AVRegion.GAUNTLET_ENTRANCE, conditions.kur_gauntlet_entrance_access, False),
    (AVRegion.GAUNTLET_ENTRANCE, AVRegion.GAUNTLET_ROOF, conditions.kur_gauntlet_roof_access, False),
    (AVRegion.GAUNTLET_ENTRANCE, AVRegion.GIR_TAB_LOWER_ENTRANCE, conditions.can_displacement_warp, False),
    (AVRegion.GAUNTLET_ENTRANCE, AVRegion.MOUNTAIN_BASE, conditions.can_displacement_warp, False),
    (AVRegion.GAUNTLET_ROOF, AVRegion.MOUNTAIN_PEAK, conditions.kur_gauntlet_warp, False),
    (AVRegion.GAUNTLET_ROOF, AVRegion.DRONE_ODYSSEY, conditions.kur_gauntlet_warp, False),
    (AVRegion.GAUNTLET_ROOF, AVRegion.GAUNTLET_REWARD, conditions.kur_gauntlet_room_reward_access, False),
    (AVRegion.LOWER_CAVES, AVRegion.GAUNTLET_REWARD, lambda s, c: conditions.has_fat_beam(s, c) and conditions.has_trenchcoat(s, c), False),
    (AVRegion.LOWER_CAVES, AVRegion.KUR_INDI, lambda s, c: conditions.any_coat(s, c) or conditions.any_wall_grapple_clip(s, c), False),
    (AVRegion.KUR_INDI, AVRegion.LOWER_CAVES, lambda s, c: conditions.any_coat(s, c) or conditions.floor_grapple_clip(s, c), False),
    (AVRegion.UPPER_CAVES, AVRegion.KUR_INDI, lambda s, c: conditions.any_coat(s, c) or conditions.floor_grapple_clip(s, c), False),
    (AVRegion.KUR_INDI, AVRegion.UPPER_CAVES, conditions.kur_indi_upper_caves_access, False),
    (AVRegion.UPPER_CAVES, AVRegion.KUR_EDIN, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.has_glitch_2(s, c), True),
    (AVRegion.KUR_EDIN, AVRegion.EAST_EDIN, conditions.always_accessible, True),

    (AVRegion.UPPER_CAVES, AVRegion.MOUNTAIN_BASE, conditions.kur_caves_to_base_access, False),
    (AVRegion.MOUNTAIN_BASE, AVRegion.UPPER_CAVES, conditions.always_accessible, False),
    (AVRegion.MOUNTAIN_BASE, AVRegion.GIR_TAB_LOWER_ENTRANCE, conditions.gir_tab_lower_entrance_access, False),
    (AVRegion.GIR_TAB_LOWER_ENTRANCE, AVRegion.MOUNTAIN_BASE, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.has_glitch_2(s, c), False),
    (AVRegion.GIR_TAB_LOWER_ENTRANCE, AVRegion.ABOVE_GIR_TAB, conditions.gir_tab_lower_above_access, False),
    (AVRegion.ABOVE_GIR_TAB, AVRegion.GIR_TAB_LOWER_ENTRANCE, conditions.always_accessible, False),
    (AVRegion.MOUNTAIN_MID, AVRegion.GIR_TAB_UPPER_ENTRANCE, conditions.gir_tab_upper_entrance_access, False),
    (AVRegion.GIR_TAB_UPPER_ENTRANCE, AVRegion.MOUNTAIN_BASE, lambda s, c: conditions.can_drill(s, c) and conditions.any_height(s, c), False),
    (AVRegion.GIR_TAB_UPPER_ENTRANCE, AVRegion.ABOVE_GIR_TAB, conditions.gir_tab_upper_above_access, False),
    (AVRegion.ABOVE_GIR_TAB, AVRegion.GIR_TAB_UPPER_ENTRANCE, conditions.gir_tab_above_upper_access, False),
    (AVRegion.ABOVE_GIR_TAB, AVRegion.GRAPPLE_CLIFFS, conditions.gir_tab_grapple_cliffs_access, False),
    (AVRegion.ABOVE_GIR_TAB, AVRegion.LOWER_E_KUR_MAH, conditions.has_red_coat, False),

    (AVRegion.MOUNTAIN_BASE, AVRegion.MOUNTAIN_MID, conditions.kur_mountain_base_mid_access, False),
    (AVRegion.MOUNTAIN_MID, AVRegion.MOUNTAIN_TOP, conditions.kur_mountain_mid_top_access, False),
    (AVRegion.MOUNTAIN_TOP, AVRegion.MOUNTAIN_BASE, lambda s, c: conditions.any_coat(s, c) or conditions.any_height(s, c), False),
    (AVRegion.MOUNTAIN_TOP, AVRegion.MOUNTAIN_PEAK, conditions.kur_mountain_top_peak_access, False),
    (AVRegion.MOUNTAIN_PEAK, AVRegion.MOUNTAIN_TOP, conditions.always_accessible, False),

    (AVRegion.MOUNTAIN_PEAK, AVRegion.UPPER_E_KUR_MAH, conditions.kur_upper_e_kur_mah_access, False),
    (AVRegion.MOUNTAIN_PEAK, AVRegion.DRONE_ODYSSEY, conditions.kur_peak_odyssey_access, False),

    (AVRegion.WEST_INDI, AVRegion.INDI, conditions.any_height, False),
    (AVRegion.INDI, AVRegion.WEST_INDI, conditions.always_accessible, False),
    (AVRegion.INDI, AVRegion.INDI_TUNNEL, conditions.always_accessible, False),
    (AVRegion.INDI, AVRegion.LOWER_EDIN_RIGHT, conditions.indi_edin_access, False),
    (AVRegion.INDI, AVRegion.EAST_INDI, conditions.always_accessible, False),
    (AVRegion.INDI, AVRegion.BLURST, conditions.always_accessible, False),
    (AVRegion.EAST_INDI, AVRegion.INDI, conditions.indi_east_taxi_access, False),
    (AVRegion.KUR_INDI, AVRegion.EAST_INDI, conditions.always_accessible, True),
    (AVRegion.INDI, AVRegion.SOUTH_UKKIN_NA_EXIT, conditions.indi_ukkin_na_access, False),

    (AVRegion.WEST_UKKIN_NA_EXIT, AVRegion.UKKIN_NA_BASE, conditions.any_coat, True),
    (AVRegion.UKKIN_NA_BASE, AVRegion.OPHELIA, conditions.non_grapple_height, False),
    (AVRegion.OPHELIA, AVRegion.BLURST, conditions.has_trenchcoat, False),
    (AVRegion.UKKIN_NA_BASE, AVRegion.SOUTH_UKKIN_NA_EXIT, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.swing_clip(s, c), False),
    (AVRegion.SOUTH_UKKIN_NA_EXIT, AVRegion.UKKIN_NA_BASE, lambda s, c: conditions.any_coat(s, c) or conditions.swing_clip(s, c), False),
    (AVRegion.SOUTH_UKKIN_NA_EXIT, AVRegion.EAST_UKKIN_NA_EXIT, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.swing_clip(s, c), True),
    (AVRegion.EAST_UKKIN_NA_EXIT, AVRegion.LOWER_EDIN_LEFT, conditions.always_accessible, True),
    (AVRegion.SOUTH_UKKIN_NA_EXIT, AVRegion.INDI, conditions.ukkin_na_indi_access, False),

    (AVRegion.LOWER_EDIN_LEFT, AVRegion.EDIN_WALL, conditions.edin_wall_access, False),
    (AVRegion.EDIN_WALL, AVRegion.LOWER_EDIN_LEFT, conditions.always_accessible, False),
    (AVRegion.EDIN_WALL, AVRegion.UKHU_TOWER, conditions.ukhu_access, False),
    (AVRegion.UKHU_TOWER, AVRegion.UKHU, conditions.has_trenchcoat, False),
    (AVRegion.UKHU_TOWER, AVRegion.EDIN_WALL, conditions.ukhu_exit_access, False),
    (AVRegion.EDIN_WALL, AVRegion.LOWER_EDIN_RIGHT, conditions.always_accessible, False),
    (AVRegion.LOWER_EDIN_RIGHT, AVRegion.EDIN_WALL, conditions.edin_wall_access, False),
    (AVRegion.LOWER_EDIN_RIGHT, AVRegion.CLONE, conditions.vanilla_clone_access, False),
    (AVRegion.CLONE, AVRegion.LOWER_EDIN_RIGHT, conditions.has_trenchcoat, False),
    (AVRegion.LOWER_EDIN_RIGHT, AVRegion.HANGAR, conditions.edin_hangar_left_access, True),
    (AVRegion.CLONE, AVRegion.HANGAR, conditions.clone_to_hangar_access, False),
    (AVRegion.HANGAR, AVRegion.EAST_EDIN, conditions.has_glitch_bomb, True),
    (AVRegion.LOWER_EDIN_RIGHT, AVRegion.INDI, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.floor_grapple_clip(s, c), False),

    (AVRegion.UPPER_E_KUR_MAH, AVRegion.KEY_CHAMBER, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.has_drone_tele(s, c), False),
    (AVRegion.UPPER_E_KUR_MAH, AVRegion.MOUNTAIN_PEAK, conditions.e_kur_mah_upper_peak_access, False),
    (AVRegion.KEY_CHAMBER, AVRegion.MID_E_KUR_MAH, lambda s, c: conditions.floor_grapple_clip(s, c), False),
    (AVRegion.UPPER_E_KUR_MAH, AVRegion.MID_E_KUR_MAH, lambda s, c: conditions.has_red_coat(s, c) or conditions.has_sudran_key(s, c), False),
    (AVRegion.MID_E_KUR_MAH, AVRegion.UPPER_E_KUR_MAH, conditions.e_kur_mah_mid_upper_access, False),
    (AVRegion.MID_E_KUR_MAH, AVRegion.LOWER_E_KUR_MAH, conditions.always_accessible, False),
    (AVRegion.LOWER_E_KUR_MAH, AVRegion.MID_E_KUR_MAH, conditions.e_kur_mah_lower_mid_access, False),
    (AVRegion.LOWER_E_KUR_MAH, AVRegion.GRAPPLE_CLIFFS, conditions.e_kur_mah_lower_cliffs_access, False),

    (AVRegion.OPHELIA, AVRegion.MAR_URU_ENTRANCE, conditions.mar_uru_access, False),
    (AVRegion.MAR_URU_ENTRANCE, AVRegion.POST_SENTINEL, conditions.post_sentinel_access, False),
    (AVRegion.POST_SENTINEL, AVRegion.SENTRY_BOT_ROOM, lambda s, c: conditions.has_glitch_2(s, c) or conditions.floor_grapple_clip(s, c), False),
    (AVRegion.POST_SENTINEL, AVRegion.ATHETOS, conditions.always_accessible, False),

    # Microregions (Separated for sanity)
    (AVRegion.EAST_ABSU, AVRegion.EA_LEDGE, lambda s, c: conditions.can_drill(s, c) or conditions.any_glitch(s, c), False),
    (AVRegion.EAST_ABSU_DRONE, AVRegion.EA_LEDGE, conditions.always_accessible, False),
    (AVRegion.EAST_ABSU, AVRegion.EA_BEHIND_TELAL, conditions.always_accessible, False),
    (AVRegion.EAST_ABSU_DRONE, AVRegion.EA_BEHIND_TELAL, conditions.always_accessible, False),
    (AVRegion.EAST_ABSU, AVRegion.EA_ALCOVE, conditions.can_drill, False),
    (AVRegion.EAST_ABSU_DRONE, AVRegion.EA_ALCOVE, conditions.always_accessible, False),
    (AVRegion.EAST_ABSU, AVRegion.EA_HIDDEN_SHRINE, lambda s, c: conditions.any_wall_grapple_clip(s, c) or conditions.any_coat(s, c) and conditions.any_height(s, c), False),
    (AVRegion.EAST_ABSU_DRONE, AVRegion.EA_HIDDEN_SHRINE, conditions.always_accessible, False),
    (AVRegion.EAST_ABSU, AVRegion.EA_CHASM_TUNNEL, conditions.has_red_coat, False),
    (AVRegion.EAST_ABSU_DRONE, AVRegion.EA_CHASM_TUNNEL, conditions.always_accessible, False),
    (AVRegion.EAST_ABSU, AVRegion.EA_ZI_ENTRANCE, conditions.can_drill, False),
    (AVRegion.EAST_ABSU_DRONE, AVRegion.EA_ZI_ENTRANCE, conditions.always_accessible, False),
)


location_data: tuple[AVLocationData] = (
    AVLocationData(0, AVArea.ERIBU, 'Starter Weapon', AVRegion.WEST_ERIBU, conditions.always_accessible),
    AVLocationData(1, AVArea.ERIBU, 'Wheelchair Room', AVRegion.WEST_ERIBU, conditions.wheelchair_room_access),
    AVLocationData(2, AVArea.ERIBU, 'Primordial Cave Lower', AVRegion.WEST_ERIBU, conditions.west_caves_pool_access),

    AVLocationData(3, AVArea.ERIBU, 'Primordial Cave Upper', AVRegion.DINGER_GISBAR, conditions.always_accessible),

    AVLocationData(4, AVArea.ERIBU, 'Right Tower', AVRegion.UPPER_ERIBU, conditions.can_damage),
    AVLocationData(5, AVArea.ERIBU, 'Left Tower', AVRegion.UPPER_ERIBU, conditions.upper_eribu_bomb_access),
    AVLocationData(6, AVArea.ERIBU, 'Bubble Shrine', AVRegion.UPPER_ERIBU, conditions.bubble_jail_access),
    AVLocationData(7, AVArea.ERIBU, 'Outside Upper Passcode Room', AVRegion.UPPER_ERIBU, conditions.outside_lab_access),

    AVLocationData(8, AVArea.ERIBU, 'Xedur Reward', AVRegion.XEDUR, conditions.can_damage_boss),
    AVLocationData(9, AVArea.ERIBU, 'Below Xedur', AVRegion.XEDUR, conditions.can_drill),

    AVLocationData(10, AVArea.ERIBU, 'Upper Passcode Room', AVRegion.LABORATORY, conditions.always_accessible),

    AVLocationData(
        11,
        AVArea.ERIBU, 'Sentry Bot Tunnel',
        AVRegion.LOWER_ERIBU,
        conditions.eribu_sentry_bot_tunnel_access,
    ),
    AVLocationData(
        12,
        AVArea.ERIBU, 'Outside Lower Passcode Room',
        AVRegion.LOWER_ERIBU,
        lambda s, c: conditions.any_glitch(s, c) and conditions.can_damage(s, c) or conditions.has_drone(s, c) or conditions.has_grapple(s, c) or conditions.has_trenchcoat(s, c),
    ),
    AVLocationData(13, AVArea.ERIBU, 'Lower Passcode Room', AVRegion.LOWER_ERIBU, conditions.dalkhu_subtum_access),
    AVLocationData(14, AVArea.ERIBU, 'Path to Absu', AVRegion.LOWER_ERIBU, conditions.always_accessible),

    AVLocationData(
        15,
        AVArea.ERIBU, 'Path to Indi Ceiling',
        AVRegion.ERIBU_INDI,
        lambda s, c: (
            conditions.has_red_coat(s, c) and (conditions.has_grapple(s, c) or conditions.has_high_jump(s, c))
            or conditions.has_drone_tele(s, c) and conditions.any_coat(s, c)
        )
    ),

    AVLocationData(16, AVArea.ABSU, 'Entrance Shaft', AVRegion.WEST_ABSU, conditions.can_drill),
    AVLocationData(
        17,
        AVArea.ABSU, 'Entrance Shaft Vault',
        AVRegion.WEST_ABSU,
        lambda s, c: conditions.has_red_coat(s, c) or conditions.any_glitch(s, c) and (conditions.any_coat(s, c) or conditions.can_pierce_wall(s, c)),
    ),
    AVLocationData(18, AVArea.ABSU, 'Under Entrance Shaft', AVRegion.WEST_ABSU, conditions.has_drone),
    AVLocationData(19, AVArea.ABSU, 'Deep Under Entrance Shaft', AVRegion.WEST_ABSU, lambda s, c: conditions.has_drone_tele(s, c) and conditions.has_trenchcoat(s, c)),

    AVLocationData(20, AVArea.ABSU, 'Switch Cage', AVRegion.WEST_ATTIC, lambda s, c: conditions.can_pierce_wall(s, c) or conditions.any_coat(s, c)),
    AVLocationData(21, AVArea.ABSU, 'Attic Left Shrine', AVRegion.WEST_ATTIC, conditions.basic_attic_access),
    AVLocationData(22, AVArea.ABSU, 'Attic Between Glitch Barriers', AVRegion.WEST_ATTIC, conditions.attic_transition_upper),

    AVLocationData(23, AVArea.ABSU, 'Attic Right Shrine', AVRegion.EAST_ATTIC, conditions.basic_attic_access),
    AVLocationData(24, AVArea.ABSU, 'Attic Upper Alcove', AVRegion.EAST_ATTIC, conditions.attic_far_right_access),

    AVLocationData(25, AVArea.ABSU, 'Elsenova', AVRegion.ELSENOVA, conditions.always_accessible),

    AVLocationData(26, AVArea.ABSU, 'Behind Glitch Barrier', AVRegion.ABSU_BASEMENT, conditions.always_accessible),

    AVLocationData(27, AVArea.ABSU, 'Cell Near Elsenova', AVRegion.LOWER_ABSU, lambda s, c: conditions.any_coat(s, c) or conditions.floor_grapple_clip(s, c)),
    AVLocationData(28, AVArea.ABSU, 'Lowest Point', AVRegion.LOWER_ABSU, lambda s, c: conditions.any_coat(s, c) or conditions.floor_grapple_clip(s, c)),

    AVLocationData(29, AVArea.ABSU, 'Floating Platform', AVRegion.LOWER_CORRIDOR, conditions.floating_platform_access),

    AVLocationData(31, AVArea.ABSU, 'Telal Reward', AVRegion.TELAL, conditions.can_damage),

    AVLocationData(32, AVArea.ABSU, 'Path to Indi Side Room', AVRegion.INDI_TUNNEL, conditions.any_height),

    AVLocationData(33, AVArea.ABSU, 'Trapped Diatoms', AVRegion.EA_LEDGE, conditions.always_accessible),
    AVLocationData(30, AVArea.ABSU, 'Lava Hall', AVRegion.EAST_ABSU, conditions.zombie_tunnel_access),
    AVLocationData(34, AVArea.ABSU, 'Shaft Behind Telal', AVRegion.EA_BEHIND_TELAL, conditions.always_accessible),
    AVLocationData(35, AVArea.ABSU, 'Green Wall Alcove', AVRegion.EA_ALCOVE, conditions.always_accessible),
    AVLocationData(36, AVArea.ABSU, 'Hidden Shrine', AVRegion.EA_HIDDEN_SHRINE, conditions.always_accessible),
    AVLocationData(37, AVArea.ABSU, 'Chasm Room Tunnel', AVRegion.EA_CHASM_TUNNEL, conditions.always_accessible),
    AVLocationData(38, AVArea.ABSU, 'Gated Alcove', AVRegion.EAST_ABSU, conditions.gated_alcove_access),
    AVLocationData(39, AVArea.ABSU, 'Shrine Behind Glitch', AVRegion.EAST_ABSU, lambda s, c: conditions.has_red_coat(s, c) or conditions.has_glitch_2(s, c) and conditions.can_drill(s, c)),
    AVLocationData(40, AVArea.ABSU, 'Path to Zi', AVRegion.EA_ZI_ENTRANCE, conditions.always_accessible),

    AVLocationData(41, AVArea.ZI, 'False Wall Near Lower Save', AVRegion.LOWER_ZI, lambda s, c: conditions.any_coat(s, c) and conditions.any_height(s, c)),
    AVLocationData(42, AVArea.ZI, 'Disappointment Hill', AVRegion.LOWER_ZI, conditions.non_grapple_height),
    AVLocationData(
        43,
        AVArea.ZI, 'Ceiling Secret Near Lower Save',
        AVRegion.LOWER_ZI,
        conditions.zi_lower_save_secret_access,
    ),
    AVLocationData(44, AVArea.ZI, 'Furglot Tunnel', AVRegion.LOWER_ZI, conditions.furglot_tunnel_access),

    AVLocationData(45, AVArea.ZI, 'False Ceiling Alcove', AVRegion.ZI_CORRIDOR, lambda s, c: conditions.any_height(s, c) or conditions.has_drone(s, c)),

    AVLocationData(46, AVArea.ZI, 'Above Veruska', AVRegion.EAST_ZI, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.has_drone(s, c)),
    AVLocationData(47, AVArea.ZI, 'Behind Veruska Left', AVRegion.EAST_ZI, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.has_drone(s, c)),
    AVLocationData(48, AVArea.ZI, 'Behind Veruska Right', AVRegion.EAST_ZI, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.has_drone(s, c)),

    AVLocationData(49, AVArea.ZI, 'Ceiling Secret Above Preview Room', AVRegion.UPPER_ZI, lambda s, c: conditions.has_red_coat(s, c) or conditions.has_drone(s, c) or conditions.can_drill(s, c) and conditions.any_height(s, c)),
    AVLocationData(50, AVArea.ZI, 'Drone Quest Upper', AVRegion.UPPER_ZI, conditions.zi_drone_tunnel_access),
    AVLocationData(51, AVArea.ZI, 'Drone Quest Lower', AVRegion.UPPER_ZI, conditions.zi_drone_tunnel_access),

    AVLocationData(52, AVArea.ZI, 'Preview Room', AVRegion.PREVIEW_ROOM, conditions.always_accessible),

    AVLocationData(53, AVArea.ZI, 'Uruku Reward', AVRegion.URUKU_BOTTOM, conditions.always_accessible),
    AVLocationData(54, AVArea.ZI, 'Uruku Cage', AVRegion.URUKU_TOP, conditions.uruku_cage_access),
    AVLocationData(55, AVArea.ZI, 'Behind Uruku Ceiling Ledge', AVRegion.URUKU_BACK_LEDGE, conditions.always_accessible),

    AVLocationData(56, AVArea.KUR, 'Drone Tunnel Before Gauntlet', AVRegion.LOWER_CAVES, conditions.has_drone),
    AVLocationData(57, AVArea.KUR, 'High Jump Shrine', AVRegion.LOWER_CAVES, conditions.always_accessible),
    AVLocationData(58, AVArea.KUR, 'High Jump Shrine False Wall', AVRegion.LOWER_CAVES, lambda s, c: conditions.has_drone(s, c) or conditions.any_height(s, c)),
    AVLocationData(59, AVArea.KUR, 'Above Lower Save', AVRegion.LOWER_CAVES, conditions.above_lower_kur_save_access),
    AVLocationData(61, AVArea.KUR, 'Main Shaft', AVRegion.LOWER_CAVES, conditions.kur_main_shaft_access),

    AVLocationData(60, AVArea.KUR, 'Gauntlet Reward', AVRegion.GAUNTLET_REWARD, conditions.always_accessible),

    AVLocationData(62, AVArea.KUR, 'Drone Side Quest', AVRegion.MOUNTAIN_BASE, lambda s, c: conditions.has_red_coat(s, c) or conditions.has_drone(s, c)),

    AVLocationData(63, AVArea.KUR, 'Above Twin Save Rooms', AVRegion.MOUNTAIN_MID, conditions.kur_above_twin_saves_access),
    AVLocationData(64, AVArea.KUR, 'Watch for Rolling Rocks', AVRegion.MOUNTAIN_MID, conditions.kur_floating_ledge_access),
    AVLocationData(65, AVArea.KUR, 'Inside Cliff', AVRegion.MOUNTAIN_MID, conditions.has_red_coat),

    AVLocationData(67, AVArea.KUR, 'Drone Odyssey Secret', AVRegion.DRONE_ODYSSEY, conditions.always_accessible),
    AVLocationData(68, AVArea.KUR, 'Drone Odyssey Reward', AVRegion.DRONE_ODYSSEY, lambda s, c: conditions.has_power_nodes(s, c, 3)),

    AVLocationData(66, AVArea.KUR, 'Shrine Before Drone Odyssey', AVRegion.MOUNTAIN_TOP, conditions.has_drone),
    AVLocationData(69, AVArea.KUR, 'Snowy Cliffs Ledge Upper', AVRegion.MOUNTAIN_TOP, conditions.kur_snowy_cliffs_ledge_upper_access),
    AVLocationData(70, AVArea.KUR, 'Snowy Cliffs Ledge Lower', AVRegion.MOUNTAIN_TOP, conditions.kur_snowy_cliffs_ledge_lower_access),
    AVLocationData(71, AVArea.KUR, 'Loop Room', AVRegion.MOUNTAIN_TOP, conditions.always_accessible),

    AVLocationData(72, AVArea.KUR, 'Peak Cliff Ledge', AVRegion.MOUNTAIN_PEAK, conditions.kur_peak_ledge_access),

    AVLocationData(73, AVArea.KUR, 'Gir-Tab Lower Entrance Drone Tunnel', AVRegion.GIR_TAB_LOWER_ENTRANCE, conditions.gir_tab_lower_drone_tunnel_access),

    AVLocationData(74, AVArea.KUR, 'Gir-Tab Upper Entrance', AVRegion.GIR_TAB_UPPER_ENTRANCE, conditions.always_accessible),

    AVLocationData(75, AVArea.KUR, 'Cliffs Behind Gir-Tab Near Crumble Floor', AVRegion.GRAPPLE_CLIFFS, conditions.grapple_cliffs_false_floor_access),
    AVLocationData(76, AVArea.KUR, 'Cliffs Behind Gir-Tab Shrine', AVRegion.GRAPPLE_CLIFFS, conditions.grapple_cliffs_shrines_access),
    AVLocationData(77, AVArea.KUR, 'Cliffs Behind Gir-Tab Above Shrine', AVRegion.GRAPPLE_CLIFFS, conditions.grapple_cliffs_shrines_upper_access),

    AVLocationData(78, AVArea.INDI, 'Path to Eribu', AVRegion.WEST_INDI, conditions.has_drone),
    AVLocationData(79, AVArea.INDI, 'Outside Save', AVRegion.INDI, conditions.has_trenchcoat),

    AVLocationData(81, AVArea.UKKIN_NA, 'Below Long Fall', AVRegion.UKKIN_NA_BASE, conditions.has_trenchcoat),

    AVLocationData(80, AVArea.UKKIN_NA, 'Long Fall', AVRegion.OPHELIA, conditions.has_trenchcoat),
    AVLocationData(82, AVArea.UKKIN_NA, 'Secret Room Above Lower Save', AVRegion.OPHELIA, conditions.ukkin_na_secret_floor_access),
    AVLocationData(83, AVArea.UKKIN_NA, 'Past the Slugs', AVRegion.OPHELIA, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.has_drone(s, c)),
    AVLocationData(84, AVArea.UKKIN_NA, 'Midway Shaft Lower', AVRegion.OPHELIA, lambda s, c: conditions.has_trenchcoat(s, c) or conditions.swing_clip(s, c)),
    AVLocationData(85, AVArea.UKKIN_NA, 'Midway Shaft Upper', AVRegion.OPHELIA, conditions.always_accessible),
    AVLocationData(86, AVArea.UKKIN_NA, 'Secret Room Below Upper Save', AVRegion.OPHELIA, conditions.ukkin_na_shrine_access),
    AVLocationData(87, AVArea.UKKIN_NA, 'Above Vision Room', AVRegion.OPHELIA, conditions.ukkin_na_above_vision_chamber_access),
    AVLocationData(88, AVArea.UKKIN_NA, 'Vision Room Tunnel', AVRegion.OPHELIA, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.has_drone(s, c)),
    AVLocationData(89, AVArea.UKKIN_NA, 'Outside Ophelia', AVRegion.OPHELIA, conditions.always_accessible),
    AVLocationData(90, AVArea.UKKIN_NA, 'Above Ophelia', AVRegion.OPHELIA, conditions.ophelia_ledge_access),

    AVLocationData(91, AVArea.EDIN, 'Ceiling Near Ukkin-Na', AVRegion.LOWER_EDIN_LEFT, conditions.edin_roof_ledge_access),

    AVLocationData(92, AVArea.EDIN, 'Sky Cage', AVRegion.EDIN_WALL, conditions.roof_cage_access),

    AVLocationData(93, AVArea.EDIN, 'Central Ruins Glitch Alcove', AVRegion.LOWER_EDIN_RIGHT, conditions.has_glitch_bomb),
    AVLocationData(94, AVArea.EDIN, 'Secret Tunnel Near Indi', AVRegion.LOWER_EDIN_RIGHT, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.has_drone(s, c)),

    AVLocationData(95, AVArea.EDIN, 'Before Clone Path', AVRegion.CLONE, lambda s, c: conditions.any_glitch(s, c) or conditions.can_drill(s, c)),
    AVLocationData(96, AVArea.EDIN, 'Clone Path Inside Blocks', AVRegion.CLONE, lambda s, c: conditions.any_glitch(s, c) or conditions.can_drill(s, c)),
    AVLocationData(97, AVArea.EDIN, 'Clone Path Rooftop Ledge', AVRegion.CLONE, conditions.clone_rooftop_ledge_access),
    AVLocationData(98, AVArea.EDIN, 'Clone Path Roof Before Save', AVRegion.CLONE, conditions.clone_roof_save_access),

    AVLocationData(99, AVArea.EDIN, 'False Wall Shrine', AVRegion.UKHU_TOWER, conditions.always_accessible),
    AVLocationData(100, AVArea.EDIN, 'Ukhu Path Drone Tunnel', AVRegion.UKHU_TOWER, lambda s, c: conditions.has_drone_tele(s, c) and conditions.has_trenchcoat(s, c)),
    AVLocationData(101, AVArea.EDIN, 'Ukhu Path Side Room', AVRegion.UKHU_TOWER, lambda s, c: conditions.has_drone_tele(s, c) and conditions.has_trenchcoat(s, c)),
    AVLocationData(102, AVArea.EDIN, 'Ukhu Path Ruins', AVRegion.UKHU_TOWER, conditions.structure_ruins_access),

    AVLocationData(103, AVArea.EDIN, 'Ukhu Reward', AVRegion.UKHU, conditions.ukhu_reward_access),

    AVLocationData(104, AVArea.EDIN, 'Main Hangar', AVRegion.HANGAR, conditions.always_accessible),

    AVLocationData(105, AVArea.EDIN, 'Double Check Tunnel Left', AVRegion.EAST_EDIN, conditions.edin_double_check_tunnel_access),
    AVLocationData(106, AVArea.EDIN, 'Double Check Tunnel Right', AVRegion.EAST_EDIN, conditions.edin_double_check_tunnel_access),

    AVLocationData(107, AVArea.E_KUR_MAH, 'Entry Chamber Breakable Wall', AVRegion.UPPER_E_KUR_MAH, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.can_drill(s, c)),
    AVLocationData(108, AVArea.E_KUR_MAH, 'Key Door on Quarry Path', AVRegion.UPPER_E_KUR_MAH, lambda s, c: conditions.has_red_coat(s, c) or conditions.has_sudran_key(s, c)),

    AVLocationData(109, AVArea.E_KUR_MAH, 'Quarry Upper', AVRegion.KEY_CHAMBER, conditions.always_accessible),
    AVLocationData(110, AVArea.E_KUR_MAH, 'Quarry Lower', AVRegion.KEY_CHAMBER, conditions.always_accessible),

    AVLocationData(111, AVArea.E_KUR_MAH, 'East Shaft Wall Alcove', AVRegion.MID_E_KUR_MAH, conditions.has_red_coat),

    AVLocationData(112, AVArea.E_KUR_MAH, 'Passcode Alcove', AVRegion.LOWER_E_KUR_MAH, conditions.e_kur_mah_passcode_check_access),
    AVLocationData(113, AVArea.E_KUR_MAH, 'Hidden Drone Tunnel', AVRegion.LOWER_E_KUR_MAH, conditions.e_kur_mah_drone_tunnel_access),
    AVLocationData(114, AVArea.E_KUR_MAH, 'Final Chamber Upper', AVRegion.LOWER_E_KUR_MAH, lambda s, c: conditions.has_trenchcoat(s, c) and conditions.can_drill(s, c)),
    AVLocationData(115, AVArea.E_KUR_MAH, 'Final Chamber Lower', AVRegion.LOWER_E_KUR_MAH, conditions.has_red_coat),

    AVLocationData(116, AVArea.MAR_URU, 'Sentinel Reward', AVRegion.POST_SENTINEL, conditions.sentinel_alcove_access),
    AVLocationData(117, AVArea.MAR_URU, 'Quantum Sentry', AVRegion.SENTRY_BOT_ROOM, conditions.always_accessible),
    AVLocationData(118, AVArea.MAR_URU, 'Quantum Sentry Basement', AVRegion.SENTRY_BOT_ROOM, conditions.always_accessible),
    AVLocationData(119, AVArea.MAR_URU, 'Quantum Sentry Basement Secret', AVRegion.SENTRY_BOT_ROOM, conditions.always_accessible),
    AVLocationData(120, AVArea.MAR_URU, 'Inside Corridor Block', AVRegion.POST_SENTINEL, conditions.always_accessible),
    AVLocationData(121, AVArea.MAR_URU, 'Before Laser Bot Puzzle', AVRegion.POST_SENTINEL, conditions.always_accessible),
    AVLocationData(122, AVArea.MAR_URU, 'Laser Bot Puzzle', AVRegion.POST_SENTINEL, lambda s, c: conditions.has_glitch_2(s, c) or conditions.has_fat_beam(s, c)),
    AVLocationData(123, AVArea.MAR_URU, 'Athethos Ascent Drone Tunnel', AVRegion.POST_SENTINEL, conditions.has_drone),

    AVLocationData(124, '', 'Glitched Blurst Item', AVRegion.BLURST, conditions.any_glitch),
)
