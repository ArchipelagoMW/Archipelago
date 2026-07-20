from BaseClasses import CollectionState, Item

from .item_utils import collection_item_maximum


class CMCollectionState:
    """Caps effective AP item counts and preserves removable excess copies."""

    def __init__(self, world) -> None:
        self.world = world

    def is_effective_collection(
        self,
        state: CollectionState,
        item: Item,
    ) -> bool:
        maximum = collection_item_maximum(self.world.options, item.name)
        return (
            maximum > 0
            and state.count(item.name, self.world.player) < maximum
        )

    def record_excess_collection(
        self,
        state: CollectionState,
        item: Item,
    ) -> bool:
        if collection_item_maximum(self.world.options, item.name) <= 0:
            return False
        if self.is_effective_collection(state, item):
            return False
        state.prog_items[self.world.player][self._excess_key(item.name)] += 1
        return True

    def remove_excess_collection(
        self,
        state: CollectionState,
        item: Item,
    ) -> bool:
        key = self._excess_key(item.name)
        excess = state.prog_items[self.world.player][key]
        if excess <= 0:
            return False
        state.prog_items[self.world.player][key] -= 1
        return True

    @staticmethod
    def _excess_key(item_name: str) -> str:
        return f"_checksmate_excess:{item_name}"
