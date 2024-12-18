from test.bases import WorldTestBase
from .. import ZillionWorld


class ZillionTestBase(WorldTestBase):
    game = "Zillion"

    def ensure_gun_3_requirement(self) -> None:
        """
        There's a low probability that gun 3 is not required.

        This makes sure that gun 3 is required by making all the canisters
        in O-7 (including key word canisters) require gun 3.
        """
        z_world = self.multiworld.worlds[1]
        assert isinstance(z_world, ZillionWorld)
        assert z_world.zz_system.randomizer
        for zz_loc_name, zz_loc in z_world.zz_system.randomizer.locations.items():
            if zz_loc_name.startswith("r15c6"):
                zz_loc.req.gun = 3
