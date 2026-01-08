import typing
from BaseClasses import Item

from test.bases import WorldTestBase
from .. import CrossCodeWorld
from ..types.world import WorldData
from ..types.pools import Pools

class CrossCodeTestBase(WorldTestBase):
    world: CrossCodeWorld
    game = "CrossCode"

    world_data: WorldData
    pools: Pools

    def get_items_by_name_with_precollected(self, item_names: typing.Union[str, typing.Iterable[str]]) -> typing.List[Item]:
        if isinstance(item_names, str):
            item_names = (item_names,)
        return [
            item for item in [*self.multiworld.itempool, *self.multiworld.precollected_items[self.player]]
            if item.name in item_names
        ]

    def setUp(self):
        super().setUp()
        if self.auto_construct:
            self.world_data = self.world.world_data
            self.pools = self.world.pools
