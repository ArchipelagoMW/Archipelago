from test.bases import TestBase, WorldTestBase
from .. import MinecraftWorld, MinecraftOptions


class MCTestBase(WorldTestBase, TestBase):
    game = "Minecraft"
    player: int = 1

    def _create_items(self, items, player):
        singleton = False
        if isinstance(items, str):
            items = [items]
            singleton = True
        ret = [self.multiworld.worlds[player].create_item(item) for item in items]
        if singleton:
            return ret[0]
        return ret

    def _get_items(self, item_pool, all_except):
        if all_except and len(all_except) > 0:
            items = self.multiworld.itempool[:]
            items = [item for item in items if item.name not in all_except]
            items.extend(self._create_items(item_pool[0], 1))
        else:
            items = self._create_items(item_pool[0], 1)
        return self.get_state(items)

    def _get_items_partial(self, item_pool, missing_item):
        new_items = item_pool[0].copy()
        new_items.remove(missing_item)
        items = self._create_items(new_items, 1)
        return self.get_state(items)
            
