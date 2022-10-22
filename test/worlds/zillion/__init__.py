from typing import cast
from test.worlds.test_base import WorldTestBase
from worlds.zillion.region import ZillionLocation


class ZillionTestBase(WorldTestBase):
    game = "Zillion"

    def world_setup(self) -> None:
        super().world_setup()
        # make sure game requires gun 3 for tests
        for location in self.world.get_locations():
            if location.name.startswith("O-7"):  # O-7 door is required
                location = cast(ZillionLocation, location)
                location.zz_loc.req.gun = 3
