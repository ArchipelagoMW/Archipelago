
from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import APQuestWorld


def create_and_connect_regions(world: "APQuestWorld"):
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: "APQuestWorld"):
    # Creating a region is as simple as calling its constructor.
    overworld = Region("Overworld", world.player, world.multiworld)
    top_left_room = Region("Top Left Room", world.player, world.multiworld)
    bottom_right_room = Region("Bottom Right Room", world.player, world.multiworld)
    right_room = Region("Right Room", world.player, world.multiworld)
    final_boss_room = Region("Final Boss Room", world.player, world.multiworld)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += [overworld, top_left_room, bottom_right_room, right_room, final_boss_room]


def connect_regions(world: "APQuestWorld"):
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    overworld = world.get_region("Overworld")
    top_left_room = world.get_region("Top Left Room")
    bottom_right_room = world.get_region("Bottom Right Room")
    right_room = world.get_region("Right Room")
    final_boss_room = world.get_region("Final Boss Room")

    # Okay, now we can get connecting. For this, we need to create Entrances.
    # Entrances are inherently one-way, but crucially, AP assumes you can always return to the origin region.
    # One way to create an Entrance is by calling the Entrance constructor.
    overworld_to_bottom_right_room = Entrance(
        world.player, "Overworld to Bottom Right Room", parent=overworld
    )
    overworld.exits.append(overworld_to_bottom_right_room)

    # You can then connect the Entrance to the target region.
    overworld_to_bottom_right_room.connect(bottom_right_room)

    # An even easier way is to use the region.connect helper.
    overworld.connect(right_room, "Overworld to Right Room")
    right_room.connect(final_boss_room, "Right Room to Final Boss Room")

    # The region.connect helper even allows adding a rule immediately.
    # We'll talk more about rule creation in the set_all_rules() function in rules.py.
    overworld.connect(top_left_room, "Overworld to Top Left Room", lambda state: state.has("Key", world.player))
