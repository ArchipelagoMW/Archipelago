from .region_base import JakAndDaxterRegion
from ..options import EnableOrbsanity
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import JakAndDaxterWorld
from ..rules import can_free_scout_flies, can_fight, can_reach_orbs_level


def build_regions(level_name: str, world: "JakAndDaxterWorld") -> JakAndDaxterRegion:
    multiworld = world.multiworld
    options = world.options
    player = world.player

    # Just the starting area.
    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 4)

    first_room_upper = JakAndDaxterRegion("First Chamber (Upper)", player, multiworld, level_name, 21)

    first_room_lower = JakAndDaxterRegion("First Chamber (Lower)", player, multiworld, level_name, 0)
    first_room_lower.add_fly_locations([262193], access_rule=lambda state: can_free_scout_flies(state, player))

    first_room_orb_cache = JakAndDaxterRegion("First Chamber Orb Cache", player, multiworld, level_name, 22)

    # Need jump dive to activate button, double jump to reach blue eco to unlock cache.
    first_room_orb_cache.add_cache_locations([14507], access_rule=lambda state:
                                             state.has_all(("Jump Dive", "Double Jump"), player))

    first_hallway = JakAndDaxterRegion("First Hallway", player, multiworld, level_name, 10)
    first_hallway.add_fly_locations([131121], access_rule=lambda state: can_free_scout_flies(state, player))

    # This entire room is accessible with floating platforms and single jump.
    second_room = JakAndDaxterRegion("Second Chamber", player, multiworld, level_name, 28)

    # These items can only be gotten with jump dive to activate a button.
    second_room.add_cell_locations([45], access_rule=lambda state: state.has("Jump Dive", player))
    second_room.add_fly_locations([49, 65585], access_rule=lambda state: state.has("Jump Dive", player))

    # This is the scout fly on the way to the pipe cell, requires normal breaking moves.
    second_room.add_fly_locations([196657], access_rule=lambda state: can_free_scout_flies(state, player))

    # This orb vent and scout fly are right next to each other, can be gotten with blue eco and the floating platforms.
    second_room.add_fly_locations([393265])
    second_room.add_cache_locations([14838])

    # Named after the cell, includes the armored lurker room.
    center_complex = JakAndDaxterRegion("Center of the Complex", player, multiworld, level_name, 17)
    center_complex.add_cell_locations([51])

    color_platforms = JakAndDaxterRegion("Color Platforms", player, multiworld, level_name, 6)
    color_platforms.add_cell_locations([44], access_rule=lambda state: can_fight(state, player))

    quick_platforms = JakAndDaxterRegion("Quick Platforms", player, multiworld, level_name, 3)

    # Jump dive to activate button.
    quick_platforms.add_cell_locations([48], access_rule=lambda state: state.has("Jump Dive", player))

    first_slide = JakAndDaxterRegion("First Slide", player, multiworld, level_name, 22)

    # Raised chamber room, includes vent room with scout fly prior to second slide.
    capsule_room = JakAndDaxterRegion("Capsule Chamber", player, multiworld, level_name, 6)

    # Use jump dive to activate button inside the capsule. Blue eco vent can ready the chamber and get the scout fly.
    capsule_room.add_cell_locations([47], access_rule=lambda state:
                                    state.has("Jump Dive", player)
                                    and (state.has_any(("Double Jump", "Jump Kick"), player)
                                         or state.has_all(("Punch", "Punch Uppercut"), player)))
    capsule_room.add_fly_locations([327729])

    # You can slide to the bottom of the city, but if you spawn down there, you have no momentum from the slide.
    # So you need some kind of jump to reach this cell.
    second_slide = JakAndDaxterRegion("Second Slide", player, multiworld, level_name, 31)
    second_slide.add_cell_locations([46], access_rule=lambda state:
                                    state.has_any(("Double Jump", "Jump Kick"), player)
                                    or state.has_all(("Punch", "Punch Uppercut"), player))

    # If you can enter the helix room, you can jump or fight your way to the top. But you need some kind of movement
    # to enter it in the first place.
    helix_room = JakAndDaxterRegion("Helix Chamber", player, multiworld, level_name, 30)
    helix_room.add_cell_locations([50], access_rule=lambda state:
                                  state.has("Double Jump", player)
                                  or can_fight(state, player))

    main_area.connect(first_room_upper)                   # Run.

    first_room_upper.connect(main_area)                   # Run.
    first_room_upper.connect(first_hallway)               # Run and jump (floating platforms).
    first_room_upper.connect(first_room_lower)            # Run and jump down.

    first_room_lower.connect(first_room_upper)            # Run and jump (floating platforms).

    # Needs some movement to reach these orbs and orb cache.
    first_room_lower.connect(first_room_orb_cache, rule=lambda state:
                             state.has_all(("Jump Dive", "Double Jump"), player))
    first_room_orb_cache.connect(first_room_lower, rule=lambda state:
                                 state.has_all(("Jump Dive", "Double Jump"), player))

    first_hallway.connect(first_room_upper)                         # Run and jump down.
    first_hallway.connect(second_room)                              # Run and jump (floating platforms).

    second_room.connect(first_hallway)                              # Run and jump.
    second_room.connect(center_complex)                             # Run and jump down.

    center_complex.connect(second_room)                             # Run and jump (swim).
    center_complex.connect(color_platforms)                         # Run and jump (swim).
    center_complex.connect(quick_platforms)                         # Run and jump (swim).

    color_platforms.connect(center_complex)                         # Run and jump (swim).

    quick_platforms.connect(center_complex)                         # Run and jump (swim).
    quick_platforms.connect(first_slide)                            # Slide.

    first_slide.connect(capsule_room)                               # Slide.

    capsule_room.connect(second_slide)                              # Slide.
    capsule_room.connect(main_area, rule=lambda state:              # Chamber goes back to surface.
                         state.has("Jump Dive", player))            # (Assume one-way for sanity.)

    second_slide.connect(helix_room, rule=lambda state:                           # As stated above, you need to jump
                         state.has_any(("Double Jump", "Jump Kick"), player)      # across the dark eco pool before
                         or state.has_all(("Punch", "Punch Uppercut"), player))   # you can climb the helix room.

    helix_room.connect(quick_platforms, rule=lambda state:          # Escape to get back to here.
                       state.has("Double Jump", player)             # Capsule is a convenient exit to the level.
                       or can_fight(state, player))

    world.level_to_regions[level_name].append(main_area)
    world.level_to_regions[level_name].append(first_room_upper)
    world.level_to_regions[level_name].append(first_room_lower)
    world.level_to_regions[level_name].append(first_room_orb_cache)
    world.level_to_regions[level_name].append(first_hallway)
    world.level_to_regions[level_name].append(second_room)
    world.level_to_regions[level_name].append(center_complex)
    world.level_to_regions[level_name].append(color_platforms)
    world.level_to_regions[level_name].append(quick_platforms)
    world.level_to_regions[level_name].append(first_slide)
    world.level_to_regions[level_name].append(capsule_room)
    world.level_to_regions[level_name].append(second_slide)
    world.level_to_regions[level_name].append(helix_room)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 200 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            amount = world.orb_bundle_size * (bundle_index + 1)
            orbs.add_orb_locations(7,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, orb_amount=amount:
                                   can_reach_orbs_level(state, player, world, level, orb_amount))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return main_area
