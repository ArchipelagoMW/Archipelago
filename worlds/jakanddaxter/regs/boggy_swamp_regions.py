from BaseClasses import CollectionState
from .region_base import JakAndDaxterRegion
from ..options import EnableOrbsanity
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import JakAndDaxterWorld
from ..rules import can_fight, can_reach_orbs_level


def build_regions(level_name: str, world: "JakAndDaxterWorld") -> JakAndDaxterRegion:
    multiworld = world.multiworld
    options = world.options
    player = world.player

    # This level is full of short-medium gaps that cannot be crossed by single jump alone.
    # These helper functions list out the moves that can cross all these gaps (painting with a broad brush but...)
    def can_jump_farther(state: CollectionState, p: int) -> bool:
        return (state.has_any(("Double Jump", "Jump Kick"), p)
                or state.has_all(("Punch", "Punch Uppercut"), p))

    def can_jump_higher(state: CollectionState, p: int) -> bool:
        return (state.has("Double Jump", p)
                or state.has_all(("Crouch", "Crouch Jump"), p)
                or state.has_all(("Crouch", "Crouch Uppercut"), p)
                or state.has_all(("Punch", "Punch Uppercut"), p))

    # Orb crates and fly box in this area can be gotten with yellow eco and goggles.
    # Start with the first yellow eco cluster near first_bats and work your way backward toward the entrance.
    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 23)
    main_area.add_fly_locations([43])

    # Includes 4 orbs collectable with the blue eco vent.
    first_bats = JakAndDaxterRegion("First Bats Area", player, multiworld, level_name, 4)

    first_jump_pad = JakAndDaxterRegion("First Jump Pad", player, multiworld, level_name, 0)
    first_jump_pad.add_fly_locations([393259])

    # The tethers in this level are all out of order... a casual playthrough has the following order for the cell ID's:
    # 42, 39, 40, 41. So that is the order we're calling "first, second, third, fourth".

    # First tether cell is collectable with yellow eco and goggles.
    first_tether = JakAndDaxterRegion("First Tether", player, multiworld, level_name, 7)
    first_tether.add_cell_locations([42])

    # This rat colony has 3 orbs on top of it, requires special movement.
    first_tether_rat_colony = JakAndDaxterRegion("First Tether Rat Colony", player, multiworld, level_name, 3)

    # If quick enough, combat not required.
    second_jump_pad = JakAndDaxterRegion("Second Jump Pad", player, multiworld, level_name, 0)
    second_jump_pad.add_fly_locations([65579])

    first_pole_course = JakAndDaxterRegion("First Pole Course", player, multiworld, level_name, 28)

    # You can break this tether with a yellow eco vent and goggles,
    # but you can't reach the platform unless you can jump high.
    second_tether = JakAndDaxterRegion("Second Tether", player, multiworld, level_name, 0)
    second_tether.add_cell_locations([39], access_rule=lambda state: can_jump_higher(state, player))

    # Fly and orbs are collectable with nearby blue eco cluster.
    second_bats = JakAndDaxterRegion("Second Bats Area", player, multiworld, level_name, 27)
    second_bats.add_fly_locations([262187], access_rule=lambda state: can_jump_farther(state, player))

    third_jump_pad = JakAndDaxterRegion("Third Jump Pad (Arena)", player, multiworld, level_name, 0)
    third_jump_pad.add_cell_locations([38], access_rule=lambda state: can_fight(state, player))

    # The platform for the third tether might look high, but you can get a boost from the yellow eco vent.
    fourth_jump_pad = JakAndDaxterRegion("Fourth Jump Pad (Third Tether)", player, multiworld, level_name, 9)
    fourth_jump_pad.add_cell_locations([40])

    # Orbs collectable here with yellow eco and goggles.
    flut_flut_pad = JakAndDaxterRegion("Flut Flut Pad", player, multiworld, level_name, 36)

    flut_flut_course = JakAndDaxterRegion("Flut Flut Course", player, multiworld, level_name, 23)
    flut_flut_course.add_cell_locations([37])
    flut_flut_course.add_fly_locations([327723, 131115])

    # Includes some orbs on the way to the cabin, blue+yellow eco to collect.
    farthy_snacks = JakAndDaxterRegion("Farthy's Snacks", player, multiworld, level_name, 7)
    farthy_snacks.add_cell_locations([36])

    # Scout fly in this field can be broken with yellow eco.
    box_field = JakAndDaxterRegion("Field of Boxes", player, multiworld, level_name, 10)
    box_field.add_fly_locations([196651])

    last_tar_pit = JakAndDaxterRegion("Last Tar Pit", player, multiworld, level_name, 12)

    fourth_tether = JakAndDaxterRegion("Fourth Tether", player, multiworld, level_name, 11)
    fourth_tether.add_cell_locations([41], access_rule=lambda state: can_jump_higher(state, player))

    main_area.connect(first_bats, rule=lambda state: can_jump_farther(state, player))

    first_bats.connect(main_area)
    first_bats.connect(first_jump_pad)
    first_bats.connect(first_tether)

    first_jump_pad.connect(first_bats)

    first_tether.connect(first_bats)
    first_tether.connect(first_tether_rat_colony, rule=lambda state:
                         (state.has_all(("Roll", "Roll Jump"), player)
                          or state.has_all(("Double Jump", "Jump Kick"), player)))
    first_tether.connect(second_jump_pad)
    first_tether.connect(first_pole_course)

    first_tether_rat_colony.connect(first_tether)

    second_jump_pad.connect(first_tether)

    first_pole_course.connect(first_tether)
    first_pole_course.connect(second_tether)

    second_tether.connect(first_pole_course, rule=lambda state: can_jump_higher(state, player))
    second_tether.connect(second_bats)

    second_bats.connect(second_tether)
    second_bats.connect(third_jump_pad)
    second_bats.connect(fourth_jump_pad)
    second_bats.connect(flut_flut_pad)

    third_jump_pad.connect(second_bats)
    fourth_jump_pad.connect(second_bats)

    flut_flut_pad.connect(second_bats)
    flut_flut_pad.connect(flut_flut_course, rule=lambda state: state.has("Flut Flut", player))  # Naturally.
    flut_flut_pad.connect(farthy_snacks)

    flut_flut_course.connect(flut_flut_pad)

    farthy_snacks.connect(flut_flut_pad)
    farthy_snacks.connect(box_field, rule=lambda state: can_jump_higher(state, player))

    box_field.connect(farthy_snacks, rule=lambda state: can_jump_higher(state, player))
    box_field.connect(last_tar_pit, rule=lambda state: can_jump_farther(state, player))

    last_tar_pit.connect(box_field, rule=lambda state: can_jump_farther(state, player))
    last_tar_pit.connect(fourth_tether, rule=lambda state: can_jump_farther(state, player))

    fourth_tether.connect(last_tar_pit, rule=lambda state: can_jump_farther(state, player))
    fourth_tether.connect(main_area)  # Fall down.

    world.level_to_regions[level_name].append(main_area)
    world.level_to_regions[level_name].append(first_bats)
    world.level_to_regions[level_name].append(first_jump_pad)
    world.level_to_regions[level_name].append(first_tether)
    world.level_to_regions[level_name].append(first_tether_rat_colony)
    world.level_to_regions[level_name].append(second_jump_pad)
    world.level_to_regions[level_name].append(first_pole_course)
    world.level_to_regions[level_name].append(second_tether)
    world.level_to_regions[level_name].append(second_bats)
    world.level_to_regions[level_name].append(third_jump_pad)
    world.level_to_regions[level_name].append(fourth_jump_pad)
    world.level_to_regions[level_name].append(flut_flut_pad)
    world.level_to_regions[level_name].append(flut_flut_course)
    world.level_to_regions[level_name].append(farthy_snacks)
    world.level_to_regions[level_name].append(box_field)
    world.level_to_regions[level_name].append(last_tar_pit)
    world.level_to_regions[level_name].append(fourth_tether)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 200 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            amount = world.orb_bundle_size * (bundle_index + 1)
            orbs.add_orb_locations(8,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, orb_amount=amount:
                                   can_reach_orbs_level(state, player, world, level, orb_amount))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return main_area
