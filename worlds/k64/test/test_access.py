from . import K64TestBase
from .. import K64World
from ..names import ItemName


class TestAccess(K64TestBase):
    def test_crystals(self):
        world = self.world
        assert isinstance(world, K64World)
        self.collect_by_name([ItemName.waddle_dee, ItemName.adeleine, ItemName.king_dedede])
        shards = self.get_items_by_name(ItemName.crystal_shard)
        for i, shard_requirement in enumerate(world.boss_requirements, 1):
            shard_num = self.count(ItemName.crystal_shard)
            self.collect(shards[shard_num:shard_requirement])
            self.assertTrue(self.count(ItemName.crystal_shard) == shard_requirement)
            self.assertTrue(self.can_reach_entrance(f"To Level {i + 1}"))
