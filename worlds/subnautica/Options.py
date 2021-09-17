from Options import Choice


class ItemPool(Choice):
    """Valuable item pool moves all not progression relevant items to starting inventory and
    creates random duplicates of important items in their place."""
    option_standard = 0
    option_valuable = 1


options = {
    "item_pool": ItemPool
}
