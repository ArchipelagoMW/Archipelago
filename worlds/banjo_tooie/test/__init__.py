from typing import Optional
from test.bases import WorldTestBase
from .. import BanjoTooieWorld


class BanjoTooieTestBase(WorldTestBase):
    game = "Banjo-Tooie"
    world: BanjoTooieWorld


class BanjoTooieHintTestBase(BanjoTooieTestBase):
    def world_setup(self, seed: Optional[int] = None) -> None:
        super().world_setup(seed)
        # fill_slot_data generates hints, so we call it after world setup
        if hasattr(self, 'world') and self.world:
            self.world.fill_slot_data()
