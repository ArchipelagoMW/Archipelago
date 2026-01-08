from __future__ import annotations

import typing as t

from .constants import AVItemType
from .items import item_data
from .options import AllowWallGrappleClips

if t.TYPE_CHECKING:
    from BaseClasses import CollectionState
    from .types import LogicContext


ALL_WEAPONS = {item.name for item in item_data.values() if item.group_name == AVItemType.WEAPON}
RANGED_WEAPONS = ALL_WEAPONS - {"Tethered Charge", "Kilver", "Distortion Field", "Multi-Disruptor", "Firewall", "Lightning Gun", "Shards", "Quantum Variegator"}


# Logic primitives that are used either independently or part of more complex expressions
def always_accessible(state: CollectionState, context: LogicContext):
    return True


def any_coat(state: CollectionState, context: LogicContext):
    return state.has_any(("Modified Lab Coat", "Trenchcoat", "Red Coat", "Progressive Coat"), context.player)


def any_glitch(state: CollectionState, context: LogicContext):
    return state.has_any(("Address Disruptor 1", "Address Disruptor 2", "Address Bomb", "Progressive Address Disruptor"), context.player)


def any_height(state: CollectionState, context: LogicContext):
    return has_trenchcoat(state, context) or has_drone_tele(state, context) or has_grapple(state, context) or has_high_jump(state, context)


def any_wall_grapple_clip(state: CollectionState, context: LogicContext):
    return has_grapple(state, context) and context.wall_grapple_clip_difficulty == AllowWallGrappleClips.option_all


def can_angle_shoot(state: CollectionState, context: LogicContext):
    return state.has_any(("Nova", "Orbital Discharge"), context.player)


def can_damage_boss(state: CollectionState, context: LogicContext):
    # We need this as Drone cannot be fired during a boss battle
    return state.has_any((*ALL_WEAPONS, "Laser Drill"), context.player) or has_red_coat(state, context)


def can_damage(state: CollectionState, context: LogicContext):
    return can_damage_boss(state, context) or has_drone(state, context)


def can_displacement_warp(state: CollectionState, context: LogicContext):
    return context.displacement_warp_enabled and has_drone(state, context)


def can_drill(state: CollectionState, context: LogicContext):
    return state.has_any(("Laser Drill", "Remote Drone", "Progressive Drone"), context.player) or has_red_coat(state, context)


def can_fly(state: CollectionState, context: LogicContext):
    return has_drone_tele(state, context) and context.flight_enabled and (
        state.has_any(("Address Disruptor 1", "Address Disruptor 2", "Progressive Address Disruptor"), context.player)
    )


def can_pierce_wall(state: CollectionState, context: LogicContext):
    return state.has_any(("Kilver", "Reverse Slicer", "FlameThrower", "Fat Beam"), context.player)


def extra_brown_height(state: CollectionState, context: LogicContext):
    return has_trenchcoat(state, context) and (
        context.brown_rocket_jump_enabled or has_high_jump(state, context)
    )


def floor_grapple_clip(state: CollectionState, context: LogicContext):
    return has_grapple(state, context) and context.floor_grapple_clip_enabled


def has_drone(state: CollectionState, context: LogicContext):
    return state.has_any(("Remote Drone", "Progressive Drone"), context.player)


def has_drone_launch(state: CollectionState, context: LogicContext):
    return state.has_all(("Remote Drone", "Enhanced Drone Launch"), context.player) or state.has("Progressive Drone", context.player, count=2)


def has_drone_tele(state: CollectionState, context: LogicContext):
    return has_drone(state, context) and state.has("Drone Teleport", context.player)


def has_fat_beam(state: CollectionState, context: LogicContext):
    return state.has("Fat Beam", context.player)


def has_glitch_2(state: CollectionState, context: LogicContext):
    return state.has_any(("Address Disruptor 2", "Address Bomb"), context.player) or state.has("Progressive Address Disruptor", context.player, count=2)


def has_glitch_bomb(state: CollectionState, context: LogicContext):
    return state.has("Address Bomb", context.player) or state.has("Progressive Address Disruptor", context.player, count=3)


def has_grapple(state: CollectionState, context: LogicContext):
    return state.has("Grapple", context.player)


def has_health_nodes(state: CollectionState, context: LogicContext):
    return not context.require_nodes or state.has("Health Node", context.player, count=3)


def has_high_jump(state: CollectionState, context: LogicContext):
    return state.has("Field Disruptor", context.player)


def has_passcode(state: CollectionState, context: LogicContext):
    return state.has("Passcode Tool", context.player)


def has_power_nodes(state: CollectionState, context: LogicContext):
    return not context.require_nodes or state.has("Power Node", context.player, count=3)


def has_red_coat(state: CollectionState, context: LogicContext):
    return state.has("Red Coat", context.player) or state.has("Progressive Coat", context.player, count=3)


def has_sudran_key(state: CollectionState, context: LogicContext):
    return state.has("Sudran Key", context.player)


def has_trenchcoat(state: CollectionState, context: LogicContext):
    return state.has_any(("Trenchcoat", "Red Coat"), context.player) or state.has("Progressive Coat", context.player, count=2)


def non_grapple_height(state: CollectionState, context: LogicContext):
    return has_trenchcoat(state, context) or has_drone_tele(state, context) or has_high_jump(state, context)


def non_jump_height(state: CollectionState, context: LogicContext):
    return has_trenchcoat(state, context) or has_drone_tele(state, context) or has_grapple(state, context)


def roof_grapple_clip(state: CollectionState, context: LogicContext):
    return has_grapple(state, context) and context.roof_grapple_clip_enabled


def swing_clip(state: CollectionState, context: LogicContext):
    return has_grapple(state, context) and context.wall_grapple_clip_difficulty >= AllowWallGrappleClips.option_swing


# Specific location checks, that are here mainly to avoid complexity in the data structure
def west_caves_pool_access(s: CollectionState, c: LogicContext):
    return (
        has_red_coat(s, c)
        or has_drone(s, c) and has_glitch_2(s, c) and (
            s.has_any(("Grapple", "Drone Teleport"), c.player) or has_trenchcoat(s, c)
        )
    )


def dingergisbar_access(s: CollectionState, c: LogicContext):
    return (
        has_passcode(s, c) and (
            has_red_coat(s, c) and (has_grapple(s, c) or has_drone_tele(s, c))
            or has_glitch_2(s, c) and has_drone_tele(s, c) and (
                has_drone_launch(s, c) or c.flight_enabled or (
                    has_trenchcoat(s, c) and (has_grapple(s, c) or c.brown_rocket_jump_enabled and has_high_jump(s, c))
                )
            )
        )
    )


def upper_eribu_bomb_access(s: CollectionState, c: LogicContext):
    return has_glitch_bomb(s, c) and (
        has_trenchcoat(s, c)
        or has_drone_tele(s, c)
        or has_high_jump(s, c) and (has_grapple(s, c) or has_drone(s, c))
    )


def bubble_jail_access(s: CollectionState, c: LogicContext):
    return (
        can_angle_shoot(s, c)
        or can_pierce_wall(s, c)
        or has_red_coat(s, c)
        or has_grapple(s, c)
        or has_drone(s, c)
        or has_trenchcoat(s, c) and can_damage_boss(s, c)
    )


def outside_lab_access(s: CollectionState, c: LogicContext):
    return has_red_coat(s, c) or has_drone(s, c) or (
        can_drill(s, c) and (can_angle_shoot(s, c) or can_pierce_wall(s, c) or has_trenchcoat(s, c) or has_grapple(s, c))
    )


def xedur_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c) or has_grapple(s, c) or has_drone(s, c) or can_pierce_wall(s, c) or can_angle_shoot(s, c)
        or has_high_jump(s, c) and can_damage(s, c)
    )


def laboratory_access(s: CollectionState, c: LogicContext):
    return (
        has_red_coat(s, c)
        or can_drill(s, c) and (has_grapple(s, c) or extra_brown_height(s, c))
    ) and (has_fat_beam(s, c) or has_passcode(s, c)) or has_drone_tele(s, c) and has_passcode(s, c)



def dalkhu_subtum_access(s: CollectionState, c: LogicContext):
    return has_passcode(s, c) and (
        has_grapple(s, c)
        or has_red_coat(s, c)
        or has_drone_tele(s, c)
        or has_drone(s, c) and any_glitch(s, c) and has_high_jump(s, c)
        or has_trenchcoat(s, c) and (has_drone(s, c) or has_high_jump(s, c))
    )


def basement_regular_access(s: CollectionState, c: LogicContext):
    return has_glitch_2(s, c) and any_coat(s, c) and (has_drone(s, c) or has_red_coat(s, c) and roof_grapple_clip(s, c))


def basic_attic_access(s: CollectionState, c: LogicContext):
    return has_red_coat(s, c) or has_grapple(s, c) or has_drone(s, c) or extra_brown_height(s, c)


def attic_transition_upper(s: CollectionState, c: LogicContext):
    return has_glitch_bomb(s, c) and (
        has_red_coat(s, c) or has_grapple(s, c) or has_drone_tele(s, c) or extra_brown_height(s, c)
    )


def attic_far_right_access(s: CollectionState, c: LogicContext):
    return (
        has_red_coat(s, c)
        or has_drone(s, c) and (
            has_grapple(s, c) or has_drone_tele(s, c) or has_high_jump(s, c) or has_drone_launch(s, c) or has_trenchcoat(s, c)
        )
        or has_trenchcoat(s, c) and (has_grapple(s, c) or has_high_jump(s, c))
    )


def elsenova_west_attic_access(s: CollectionState, c: LogicContext):
    return can_drill(s, c) and (
        has_drone_tele(s, c) or has_trenchcoat(s, c) or has_high_jump(s, c) or any_glitch(s, c)
    )


def floating_platform_access(s: CollectionState, c: LogicContext):
    return has_drone(s, c) or has_trenchcoat(s, c) or has_high_jump(s, c) or has_grapple(s, c) or any_glitch(s, c)


def zombie_tunnel_access(s: CollectionState, c: LogicContext):
    return (
        has_red_coat(s, c)
        or has_trenchcoat(s, c) and (
            c.brown_rocket_jump_enabled or has_drone_tele(s, c) or has_grapple(s, c) or has_high_jump(s, c)
        )
        or swing_clip(s, c)
    )


def lower_east_absu_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c)
        or can_drill(s, c) and (has_drone_tele(s, c) or any_glitch(s, c) or has_grapple(s, c))
    )


def telal_east_absu_access(s: CollectionState, c: LogicContext):
    # NOTE: This rule is concerned with conditions not permitted by the above access rule (Lower to East)
    # Hence really the "any" here should be white, but a higher coat works here and via Lower to East, so it's ok
    return (
        any_coat(s, c) and s.has_any(("Reverse Slicer", "Flamethrower"), c.player)
        or s.has("Range Node", c.player, count=2) and s.has("Flamethrower", c.player)
        or s.has_any(("Fat Beam", "Scissor Beam"), c.player)
    )


def east_absu_indi_tunnel_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c)
        or any_coat(s, c) and (has_drone_tele(s, c) or has_grapple(s, c))
        or swing_clip(s, c)
    )


def gated_alcove_access(s: CollectionState, c: LogicContext):
    return can_drill(s, c) and (
        any_glitch(s, c) or any_wall_grapple_clip(s, c) or any_coat(s, c)
        or s.has_any(("Flamethrower", "Scissor Beam", "Reverse Slicer", "Fat Beam"), c.player)
    )


def zi_vanilla_exit(s: CollectionState, c: LogicContext):
    # NOTE: Maybe Damage Boost here for the masochists
    return has_trenchcoat(s, c) or has_grapple(s, c) or has_drone_tele(s, c)


def furglot_tunnel_access(s: CollectionState, c: LogicContext):
    return has_glitch_2(s, c) and any_height(s, c) or has_trenchcoat(s, c) and (any_glitch(s, c) or s.has_any(RANGED_WEAPONS, c.player))


def zi_false_roof_access(s: CollectionState, c: LogicContext):
    return any_height(s, c) and (can_damage(s, c) or has_glitch_2(s, c) or has_trenchcoat(s, c))


def lower_east_zi_access(s: CollectionState, c: LogicContext):
    return has_health_nodes(s, c) and (
        can_damage(s, c) or has_glitch_2(s, c) or has_trenchcoat(s, c)
    )


def zi_drone_tunnel_access(s: CollectionState, c: LogicContext):
    return has_drone(s, c) and has_power_nodes(s, c)


def zi_indi_access(s: CollectionState, c: LogicContext):
    return (
        has_drone_tele(s, c)
        or has_red_coat(s, c)
        or has_high_jump(s, c) and has_grapple(s, c)
        or has_trenchcoat(s, c) and (
            has_high_jump(s, c) or has_grapple(s, c)
        )
    )


def can_kill_uruku(s: CollectionState, c: LogicContext):
    return (
        can_damage_boss(s, c) and any_glitch(s, c)
        or s.has_any(
            ("Fat Beam", "Voranj", "Axiom Disruptor", "Data Bomb", "Nova", "Heat Seeker", "Turbine Pulse", "Hypo-Atomizer", "Orbital Discharge", "Reflector", "Inertial Pulse", "Ion Beam"),
            c.player,
        )
    )


def uruku_bottom_access(s: CollectionState, c: LogicContext):
    return has_trenchcoat(s, c) or any_coat(s, c) and any_glitch(s, c)


def uruku_top_access(s: CollectionState, c: LogicContext):
    return (
        can_kill_uruku(s, c) and (
            can_fly(s, c)
            or has_drone_tele(s, c) and has_drone_launch(s, c)
            or has_high_jump(s, c) and has_grapple(s, c) and c.obscure_skips
            or any_glitch(s, c) and has_grapple(s, c)
        )
        or any_glitch(s, c) and (
            has_high_jump(s, c) or has_trenchcoat(s, c)
        ) and (
            can_kill_uruku(s, c) or has_trenchcoat(s, c)
        )
    )


def uruku_bottom_top_access(s: CollectionState, c: LogicContext):
    return (
        (has_red_coat(s, c) or has_trenchcoat(s, c) and has_high_jump(s, c))
        and (roof_grapple_clip(s, c) or has_grapple(s, c) and has_drone_tele(s, c))
    )


def uruku_bottom_back_ledge_access(s: CollectionState, c: LogicContext):
    return (
        can_fly(s, c) or has_drone_launch(s, c) and (
            has_red_coat(s, c) or extra_brown_height(s, c)
        )
    )


def uruku_cage_access(s: CollectionState, c: LogicContext):
    return any_coat(s, c) or floor_grapple_clip(s, c)


def above_lower_kur_save_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c)
        or has_glitch_2(s, c) and can_drill(s, c)
        or has_drone(s, c) and any_coat(s, c)
    )


def kur_gauntlet_entrance_access(s: CollectionState, c: LogicContext):
    return (
        has_grapple(s, c) and can_drill(s, c)
        or has_red_coat(s, c) and has_high_jump(s, c)
        or has_drone_tele(s, c) and (
            has_high_jump(s, c) or has_trenchcoat(s, c) or has_drone_launch(s, c)
        )
        or has_high_jump(s, c) and has_trenchcoat(s, c) and c.brown_rocket_jump_enabled and can_drill(s, c)
        or can_fly(s, c)
    )


def kur_gauntlet_roof_access(s: CollectionState, c: LogicContext):
    return (
        any_coat(s, c) and any_glitch(s, c) and has_health_nodes(s, c)
        or has_high_jump(s, c) or has_drone_launch(s, c) and (
            c.red_rocket_jump_enabled or has_drone_tele(s, c) and has_grapple(s, c)
        )
    )


def kur_gauntlet_warp(s: CollectionState, c: LogicContext):
    return can_displacement_warp(s, c) and has_trenchcoat(s, c)


def kur_gauntlet_room_reward_access(s: CollectionState, c: LogicContext):
    return has_red_coat(s, c) or has_drone(s, c) or has_trenchcoat(s, c) and can_drill(s, c)


def kur_floating_ledge_access(s: CollectionState, c: LogicContext):
    return (
        has_drone_tele(s, c)
        or has_grapple(s, c)
        or has_red_coat(s, c)
        or has_trenchcoat(s, c) and has_high_jump(s, c)
        or has_drone_launch(s, c) and (has_trenchcoat(s, c) or has_high_jump(s, c))
    )


def kur_above_twin_saves_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c)
        or any_coat(s, c) and (
            has_drone_tele(s, c)
            or has_high_jump(s, c) and (
                has_drone(s, c) or has_grapple(s, c)
            )
        )
    )


def can_kill_gir_tab(s: CollectionState, c: LogicContext):
    return has_health_nodes(s, c) and has_power_nodes(s, c) and s.has_any(
        ("Hypo-Atomizer", "Fat Beam", "Inertial Pulse", "Nova", "Voranj", "Tethered Charge", "Flamethrower", "Reverse Slicer", "Scissor"),
        c.player,
    )


def gir_tab_lower_above_access(s: CollectionState, c: LogicContext):
    return has_trenchcoat(s, c) or can_kill_gir_tab(s, c) and non_grapple_height(s, c)


def kur_indi_upper_caves_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c)
        or non_grapple_height(s, c) and (any_coat(s, c) or swing_clip(s, c))
    )


def indi_east_taxi_access(s: CollectionState, c: LogicContext):
    return has_red_coat(s, c) or has_grapple(s, c) or has_drone_tele(s, c) or has_trenchcoat(s, c) and has_high_jump(s, c)


def kur_caves_to_base_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c)
        or has_drone_tele(s, c)
        or has_grapple(s, c) and has_high_jump(s, c)
        or can_drill(s, c) and any_coat(s, c) and (has_grapple(s, c) or has_high_jump(s, c))
    )


def gir_tab_lower_entrance_access(s: CollectionState, c: LogicContext):
    return has_trenchcoat(s, c) or has_glitch_2(s, c) or has_drone_tele(s, c) and floor_grapple_clip(s, c)


def gir_tab_lower_drone_tunnel_access(s: CollectionState, c: LogicContext):
    return has_drone(s, c) and (any_glitch(s, c) or has_red_coat(s, c))


def gir_tab_upper_entrance_access(s: CollectionState, c: LogicContext):
    return (
        can_drill(s, c) and (
            has_trenchcoat(s, c) or (
                any_coat(s, c) and (
                    has_drone_tele(s, c) or has_high_jump(s, c) and has_grapple(s, c)
                )
            )
        )

    )


def gir_tab_upper_above_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c)
        or non_grapple_height(s, c) and (
            any_coat(s, c) or swing_clip(s, c)
        )
    )


def gir_tab_above_upper_access(s: CollectionState, c: LogicContext):
    return has_trenchcoat(s, c) or swing_clip(s, c) or any_coat(s, c) and non_grapple_height(s, c)


def gir_tab_grapple_cliffs_access(s: CollectionState, c: LogicContext):
    return any_coat(s, c) and can_damage(s, c) or has_fat_beam(s, c)


def grapple_cliffs_false_floor_access(s: CollectionState, c: LogicContext):
    return non_grapple_height(s, c) and (
        has_red_coat(s, c) and c.red_rocket_jump_enabled
        or has_grapple(s, c)
        or has_drone(s, c)
    )


def grapple_cliffs_shrines_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c) or has_drone_tele(s, c) or has_drone(s, c) and has_glitch_2(s, c) and any_wall_grapple_clip(s, c)
    )


def kur_mountain_base_top_access(s: CollectionState, c: LogicContext):
    return (
        has_drone_tele(s, c)
        or has_grapple(s, c) and (
            has_high_jump(s, c) or has_trenchcoat(s, c)
        )
        or has_trenchcoat(s, c) and has_high_jump(s, c)
        or has_red_coat(s, c) and c.red_rocket_jump_enabled
    )


def kur_snowy_cliffs_ledge_upper_access(s: CollectionState, c: LogicContext):
    return (
        can_fly(s, c)
        or has_glitch_2(s, c) and (
            has_grapple(s, c) or has_drone(s, c) or has_trenchcoat(s, c) and has_high_jump(s, c)
        )
        or has_drone_launch(s, c) and (
            has_red_coat(s, c) and has_high_jump(s, c)
            or has_drone_tele(s, c) and has_grapple(s, c)
        )
    )


def kur_snowy_cliffs_ledge_lower_access(s: CollectionState, c: LogicContext):
    return (
        can_fly(s, c)
        or has_drone_launch(s, c)
        or has_glitch_2(s, c) and (
            has_grapple(s, c) or has_drone(s, c) or has_trenchcoat(s, c) and has_high_jump(s, c)
        )
    )


def kur_mountain_top_peak_access(s: CollectionState, c: LogicContext):
    return (
        has_red_coat(s, c)
        or has_trenchcoat(s, c) and has_high_jump(s, c)
        or has_grapple(s, c) and (
            has_trenchcoat(s, c) or has_high_jump(s, c)
        )
        or has_drone_tele(s, c) and (
            has_high_jump(s, c) or has_trenchcoat(s, c) or has_grapple(s, c)
        )
        or can_displacement_warp(s, c) and has_drone_tele(s, c) and (
            s.has_any(
                ("Fat Beam", "Flamethrower", "Reverse Slicer", "Nova", "Voranj", "Orbital Discharge", "Scissor Beam"),
                c.player,
            )
            or s.has("Data Bomb", c.player) and s.has("Size Node", c.player, 3)
        )
    )


def kur_upper_e_kur_mah_access(s: CollectionState, c: LogicContext):
    return (
        has_red_coat(s, c) and has_drone_tele(s, c) and (
            can_fly(s, c) or has_drone_launch(s, c) or has_high_jump(s, c) and c.red_rocket_jump_enabled
        )
        or has_trenchcoat(s, c) and has_drone_tele(s, c) and (
            can_fly(s, c) or has_drone_launch(s, c) or has_high_jump(s, c) and c.brown_rocket_jump_enabled
        )
    )


def kur_peak_ledge_access(s: CollectionState, c: LogicContext):
    return (
        can_fly(s, c)
        or has_drone_tele(s, c) and has_drone_launch(s, c)
        or has_trenchcoat(s, c) and roof_grapple_clip(s, c) and has_drone(s, c)
        or has_red_coat(s, c) and roof_grapple_clip(s, c) and (
            has_drone(s, c) or has_high_jump(s, c)
        )
    )


def kur_peak_odyssey_access(s: CollectionState, c: LogicContext):
    return has_drone(s, c) and (has_power_nodes(s, c) or has_drone_tele(s, c))


def ophelia_ascent_access(s: CollectionState, c: LogicContext):
    return s.has("Vision Defeated", c.player) and (
        has_trenchcoat(s, c) or has_high_jump(s, c)
    )


def ukkin_na_secret_floor_access(s: CollectionState, c: LogicContext):
    return has_red_coat(s, c) or has_trenchcoat(s, c) and (
        has_fat_beam(s, c)
        or s.has("FlameThrower", c.player) and s.has("Size Node", c.player, count=5)
        or s.has("Reverse Slicer", c.player) and s.has("Size Node", c.player, count=3)
    )


def ukkin_na_shrine_access(s: CollectionState, c: LogicContext):
    return has_drone(s, c) and (
        has_glitch_2(s, c) or has_red_coat(s, c) or floor_grapple_clip(s, c)
    )


def ophelia_ledge_access(s: CollectionState, c: LogicContext):
    return has_drone_tele(s, c) or has_red_coat(s, c) or (
        has_trenchcoat(s, c) and has_grapple(s, c)
        or has_trenchcoat(s, c) and has_high_jump(s, c)
        or has_high_jump(s, c) and has_grapple(s, c)
    )


def ukkin_na_above_vision_chamber_access(s: CollectionState, c: LogicContext):
    return (
        can_fly(s, c)
        or has_red_coat(s, c) and (has_drone_launch(s, c) or has_grapple(s, c) and has_drone(s, c)) and (
            has_high_jump(s, c) or c.red_rocket_jump_enabled
        )
    )


def ukkin_na_indi_access(s: CollectionState, c: LogicContext):
    return any_coat(s, c) or any_wall_grapple_clip(s, c)


def indi_ukkin_na_access(s: CollectionState, c: LogicContext):
    return has_trenchcoat(s, c) and any_wall_grapple_clip(s, c)


def indi_edin_access(s: CollectionState, c: LogicContext):
    return (
        has_red_coat(s, c)
        or has_trenchcoat(s, c) and (
            has_grapple(s, c) or has_drone_tele(s, c) or has_high_jump(s, c)
        )
    )


def edin_roof_ledge_access(s: CollectionState, c: LogicContext):
    return (
        can_fly(s, c)
        or has_trenchcoat(s, c) and has_drone_launch(s, c) and has_drone_tele(s, c)
        or has_red_coat(s, c) and has_high_jump(s, c) and c.red_rocket_jump_enabled and (
            has_grapple(s, c) and has_drone_tele(s, c) or has_drone_launch(s, c)
        )
    )


def roof_cage_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c) and (
            can_fly(s, c)
            or has_high_jump(s, c) and (has_grapple(s, c) or has_drone_tele(s, c))
            or has_drone_tele(s, c) and has_drone_launch(s, c)
        )
    )


def clone_rooftop_ledge_access(s: CollectionState, c: LogicContext):
    return (
        can_fly(s, c)
        or has_trenchcoat(s, c) and has_grapple(s, c) and (
            has_drone(s, c) or roof_grapple_clip(s, c)
        )
        or has_red_coat(s, c) and has_high_jump(s, c) and has_drone_launch(s, c)  # TODO: Coyote?
    )


def clone_roof_save_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c) and any_glitch(s, c) and (
            can_fly(s, c) or has_drone_tele(s, c) and has_drone_launch(s, c)
        )
        or has_red_coat(s, c) and (
            has_grapple(s, c) or (
                has_drone_tele(s, c) and has_high_jump(s, c) and c.red_rocket_jump_enabled
            )
        )
    )


def clone_to_hangar_access(s: CollectionState, c: LogicContext):
    return (
        has_red_coat(s, c)
        or has_trenchcoat(s, c) and (
            has_drone_tele(s, c) or has_grapple(s, c) or has_high_jump(s, c)
        )
    )


def ukhu_access(s: CollectionState, c: LogicContext):
    return has_glitch_bomb(s, c) or has_red_coat(s, c) or has_trenchcoat(s, c) and (
        roof_grapple_clip(s, c) or has_high_jump(s, c) and c.obscure_skips
    )

def ukhu_exit_access(s: CollectionState, c: LogicContext):
    return has_glitch_bomb(s, c) or has_red_coat(s, c) or has_trenchcoat(s, c) and c.obscure_skips


def can_kill_ukhu(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c) and has_health_nodes(s, c) and has_power_nodes(s, c)
        and s.has_any(
            ALL_WEAPONS - {"Multi-Disruptor", "Distortion Field", "Firewall", "Kilver", "Quantum Variegator"},
            c.player,
        )
    )


def ukhu_reward_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c) and (
            has_drone_tele(s, c)
            or can_kill_ukhu(s, c) and (has_drone(s, c) or floor_grapple_clip(s, c))
        )
    )


def structure_ruins_access(s: CollectionState, c: LogicContext):
    return has_red_coat(s, c) or has_trenchcoat(s, c) and can_drill(s, c) and (
        has_drone_tele(s, c) or floor_grapple_clip(s, c)
    )


def vanilla_clone_access(s: CollectionState, c: LogicContext):
    return has_red_coat(s, c) or has_trenchcoat(s, c) and (
        has_high_jump(s, c) or has_drone_tele(s, c) or roof_grapple_clip(s, c)
    )


def edin_hangar_left_access(s: CollectionState, c: LogicContext):
    return has_glitch_bomb(s, c) or has_red_coat(s, c) and c.obscure_skips


def edin_double_check_tunnel_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c) and (
            can_fly(s, c)
            or has_drone_tele(s, c) and has_drone_launch(s, c)
            or has_high_jump(s, c) and has_grapple(s, c)
            or has_glitch_bomb(s, c) and (
                has_grapple(s, c) or has_high_jump(s, c) or has_drone_tele(s, c)
            )
        ) or has_red_coat(s, c) and has_grapple(s, c) and (
            has_high_jump(s, c) or c.red_rocket_jump_enabled
        )
    )


def e_kur_mah_upper_peak_access(s: CollectionState, c: LogicContext):
    return has_red_coat(s, c) or has_trenchcoat(s, c) and has_drone_tele(s, c)


def e_kur_mah_mid_upper_access(s: CollectionState, c: LogicContext):
    return has_red_coat(s, c) and (
        has_drone_tele(s, c) or has_grapple(s, c) or has_high_jump(s, c)
    )


def e_kur_mah_lower_mid_access(s: CollectionState, c: LogicContext):
    return (
        has_red_coat(s, c) and (
            has_drone_tele(s, c) or has_high_jump(s, c) and (
                has_grapple(s, c) or c.red_rocket_jump_enabled
            )
        )
    )


def e_kur_mah_passcode_check_access(s: CollectionState, c: LogicContext):
    return (
        has_passcode(s, c) and (
            can_fly(s, c)
            or has_trenchcoat(s, c) and has_grapple(s, c) and (
                has_high_jump(s, c) or has_drone_tele(s, c)
            )
            or has_red_coat(s, c) and has_high_jump(s, c) and has_drone_tele(s, c)
        )
    )


def e_kur_mah_drone_tunnel_access(s: CollectionState, c: LogicContext):
    return (
        can_fly(s, c)
        or has_drone(s, c) and (
            has_red_coat(s, c) and (
                has_high_jump(s, c) or has_grapple(s, c) or c.red_rocket_jump_enabled
            )
            or has_trenchcoat(s, c) and has_high_jump(s, c)
        )
    )


def e_kur_mah_lower_cliffs_access(s: CollectionState, c: LogicContext):
    return (
        has_trenchcoat(s, c) and can_drill(s, c) and (
            has_drone_tele(s, c) or has_grapple(s, c)
        )
        or has_red_coat(s, c) and (
            has_high_jump(s, c) or has_grapple(s, c)
        )
    )


def e_kur_mah_key_chamber_path_access(s: CollectionState, c: LogicContext):
    return (
        has_red_coat(s, c)
        or has_trenchcoat(s, c) and (
            has_high_jump(s, c) or has_drone_tele(s, c) or has_grapple(s, c)
        ) and (
            has_sudran_key(s, c) or floor_grapple_clip(s, c)
        )
    )


def mar_uru_access(s: CollectionState, c: LogicContext):
    return (
        has_red_coat(s, c) and (
            can_fly(s, c)
            or has_drone_tele(s, c) and (
                has_drone_launch(s, c) or has_high_jump(s, c) and c.red_rocket_jump_enabled
            )
            or has_high_jump(s, c) and has_grapple(s, c) and c.red_rocket_jump_enabled
        )
    )


def can_kill_sentinel(s: CollectionState, c: LogicContext):
    return has_health_nodes(s, c) and has_power_nodes(s, c)


# NOTE: All Mar-Uru rules assume Red
def sentinel_alcove_access(s: CollectionState, c: LogicContext):
    return can_fly(s, c) or has_high_jump(s, c) and (has_drone_tele(s, c) or c.red_rocket_jump_enabled)


def post_sentinel_access(s: CollectionState, c: LogicContext):
    return (
        can_kill_sentinel(s, c) and (
            can_fly(s, c) or has_drone_tele(s, c) and (
                has_drone_launch(s, c) or has_grapple(s, c)
            )
        )
    )

