from . import ZillionTestBase

from .. import ZillionWorld


class SeedTest(ZillionTestBase):
    auto_construct = False

    def test_reproduce_seed(self) -> None:
        self.world_setup(42)
        z_world = self.multiworld.worlds[1]
        assert isinstance(z_world, ZillionWorld)
        r = z_world.zz_system.randomizer
        assert r
        randomized_requirements_first = tuple(
            location.req.gun
            for location in r.locations.values()
        )

        self.world_setup(42)
        z_world = self.multiworld.worlds[1]
        assert isinstance(z_world, ZillionWorld)
        r = z_world.zz_system.randomizer
        assert r
        randomized_requirements_second = tuple(
            location.req.gun
            for location in r.locations.values()
        )

        assert randomized_requirements_first == randomized_requirements_second
