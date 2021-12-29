import typing


def create_regions(world, player: int):
    from . import create_region
    from .Locations import base_location_table, diary_location_table
    from .Items import LegacyItem

    locations: typing.List[str] = []

    # Add required locations.
    locations += [location for location in base_location_table]
    locations += [location for location in diary_location_table]

    # Add chests per settings.
    fairies = int(world.fairy_chests_per_zone[player])
    for i in range(0, fairies):
        locations += [f"Castle Hamson Fairy Chest {i + 1}"]
        locations += [f"Forest Abkhazia Fairy Chest {i + 1}"]
        locations += [f"The Maya Fairy Chest {i + 1}"]
        locations += [f"The Land of Darkness Fairy Chest {i + 1}"]

    chests = int(world.chests_per_zone[player])
    for i in range(0, chests):
        locations += [f"Castle Hamson Chest {i + 1}"]
        locations += [f"Forest Abkhazia Chest {i + 1}"]
        locations += [f"The Maya Chest {i + 1}"]
        locations += [f"The Land of Darkness Chest {i + 1}"]

    # Set up the regions correctly.
    world.regions += [
        create_region(world, player, "Menu", None, ["Outside Castle Hamson"]),
        create_region(world, player, "Castle Hamson", locations),
    ]

    # Connect entrances and set up events.
    world.get_entrance("Outside Castle Hamson", player).connect(world.get_region("Castle Hamson", player))
    world.get_location("Castle Hamson", player).place_locked_item(LegacyItem("Defeated Khindr", player, True))
    world.get_location("Forest Abkhazia", player).place_locked_item(LegacyItem("Defeated Alexander", player, True))
    world.get_location("The Maya", player).place_locked_item(LegacyItem("Defeated Ponce de Leon", player, True))
    world.get_location("The Land of Darkness", player).place_locked_item(LegacyItem("Defeated Herodotus", player, True))
    world.get_location("Victory", player).place_locked_item(LegacyItem("Victory", player, True))
