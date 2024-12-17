import typing

from ..Enum import StartRoomDifficulty

from ..PrimeOptions import DoorColorRandomization

from ..data.StartRoomData import get_available_start_rooms

from ..data.RoomNames import RoomName
from ..Config import make_config
from Fill import distribute_items_restrictive
from ..Items import SuitUpgrade
from .. import MetroidPrimeWorld
from . import MetroidPrimeTestBase, MetroidPrimeWithOverridesTestBase

if typing.TYPE_CHECKING:
    from .. import MetroidPrimeWorld


class TestStartingBeamRandomization(MetroidPrimeTestBase):
    options = {
        "randomize_starting_beam": True,
    }

    def test_power_beam_is_not_the_starting_weapon_when_randomized(self):
        self.world.generate_early()
        world: "MetroidPrimeWorld" = self.world
        world.create_items()
        self.assertGreater(len(world.multiworld.precollected_items[world.player]), 0)
        self.assertNotIn(
            SuitUpgrade.Power_Beam.value,
            [item.name for item in world.multiworld.precollected_items[world.player]],
        )

    def test_hive_mecha_is_disabled_if_starting_at_landing_site_and_power_beam_is_not_starting_weapon(
        self,
    ):
        self.world_setup()  # type: ignore
        world: "MetroidPrimeWorld" = self.world
        distribute_items_restrictive(self.multiworld)
        config = make_config(world)
        self.assertEqual(config["gameConfig"]["removeHiveMecha"], True)


class TestStartingBeamRandomizationDisabled(MetroidPrimeTestBase):
    options = {
        "randomize_starting_beam": False,
    }

    def test_power_beam_is_the_starting_weapon_when_not_randomized(self):
        self.world.generate_early()
        world: "MetroidPrimeWorld" = self.world
        world.create_items()
        self.assertGreater(len(world.multiworld.precollected_items[world.player]), 0)
        self.assertIn(
            SuitUpgrade.Power_Beam.value,
            [item.name for item in world.multiworld.precollected_items[world.player]],
        )

    def test_hive_mecha_is_not_disabled_if_starting_at_landing_site_and_power_beam_is_starting_weapon(
        self,
    ):
        self.world_setup()  # type: ignore
        world: "MetroidPrimeWorld" = self.world
        distribute_items_restrictive(self.multiworld)
        config = make_config(world)
        self.assertEqual(config["gameConfig"]["removeHiveMecha"], False)


class TestStartingBeamRandomizationWithStartingRoomNoDoorColorRando(
    MetroidPrimeWithOverridesTestBase
):
    options = {
        "randomize_starting_beam": True,
    }

    def test_start_rooms_with_required_beam_are_excluded_if_door_color_rando_is_not_on(
        self,
    ):
        start_rooms = get_available_start_rooms(
            self.world, StartRoomDifficulty.Safe.value
        )
        self.assertNotIn(RoomName.Tower_Chamber.value, start_rooms)


class TestStartingBeamRandomizationWithStartingRoomDoorColorRando(
    MetroidPrimeWithOverridesTestBase
):
    options = {
        "randomize_starting_beam": True,
        "door_color_randomization": DoorColorRandomization.option_regional,
    }

    def test_start_rooms_with_required_beam_are_included_if_door_color_rando_is_on(
        self,
    ):
        start_rooms = get_available_start_rooms(
            self.world, StartRoomDifficulty.Safe.value
        )
        self.assertIn(RoomName.Tower_Chamber.value, start_rooms)
