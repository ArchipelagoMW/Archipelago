import typing
from ..Config import make_config
from Fill import distribute_items_restrictive
from ..Items import SuitUpgrade
from .. import MetroidPrimeWorld
from . import MetroidPrimeTestBase

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
