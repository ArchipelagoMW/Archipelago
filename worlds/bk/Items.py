import typing
from BaseClasses import Item, ItemClassification

base_item_id = 130000


class ItemData:
    def __init__(self, ap_code: int, game_code: int = 0x00,
                 classification: ItemClassification = ItemClassification.filler, quantity: int = 1):
        self.ap_code = None if ap_code is None else ap_code + base_item_id
        self.game_code = game_code
        self.classification = classification
        self. quantity = quantity


class BKItem(Item):
    game: str = "Banjo-Kazooie"


moves_table = {
    "Jump": ItemData(0, 0x0a, ItemClassification.progression),
    "Feathery Flap": ItemData(1, 0x07, ItemClassification.progression),
    "Flap Flip": ItemData(2, 0x08, ItemClassification.progression),
    "Swim": ItemData(3, 0x0f, ItemClassification.progression),
    "Climb": ItemData(4, 0x05, ItemClassification.progression),
    "Beak Barge": ItemData(5, 0x00, ItemClassification.progression),
    "Claw Swipe": ItemData(6, 0x04, ItemClassification.progression),
    "Roll": ItemData(7, 0x0c, ItemClassification.progression),
    "Rat-A-Tat Rap": ItemData(8, 0x0b, ItemClassification.progression),
    "Eggs": ItemData(9, 0x06, ItemClassification.progression),
    "Talon Trot": ItemData(10, 0x10, ItemClassification.progression),
    "Beak Buster": ItemData(11, 0x02, ItemClassification.progression),
    "Flight": ItemData(12, 0x09, ItemClassification.progression),
    "Shock Spring Jump": ItemData(13, 0x0d, ItemClassification.progression),
    "Wonderwing": ItemData(14, 0x12, ItemClassification.progression),
    "Wading Boots": ItemData(15, 0x0e, ItemClassification.progression),
    "Beak Bomb": ItemData(16, 0x01, ItemClassification.progression),
    "Turbo Talon Trot": ItemData(17, 0x11, ItemClassification.progression)
}

item_table = {
    **moves_table
}