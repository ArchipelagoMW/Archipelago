from test.bases import WorldTestBase, TestBase


class MindustryTestBase(WorldTestBase, TestBase):
    game = "Mindustry"

    def has_all_items_in_itempool(self, items: list[str]) -> bool:
        """Verify that all items are present in the item pool."""
        has_items = False
        item_count = 0

        for item in items:
            if item in self.multiworld.itempool:
                item_count += 1

        if item_count == len(items):
            has_items = True

        return has_items

    def has_no_items_in_itempool(self, items: list[str]) -> bool:
        """Verify that no item in the items list are present in the item pool."""
        has_none = True
        item_count = 0

        for item in items:
            if item in self.multiworld.itempool:
                item_count += 1

        if item_count > 0:
            has_none = False

        return has_none

    def has_amount_in_itempool(self, progressive_item : str, amount: int) -> bool:
        """Verify that the progressive item is x amount of time in the item pool."""
        valid_amount = False
        item_count = 0

        for item in self.multiworld.itempool:
            if item.name == progressive_item:
                item_count += 1

        if item_count == amount:
            valid_amount = True

        return valid_amount
