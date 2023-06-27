from BaseClasses import Item, ItemClassification
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: any


class TLNItem(Item):
    game: str = "TouhouLunaNights"

# CHANGE IDS
item_table = {
    "Red Key": ItemData(787801, ItemClassification.progression),
    "Yellow Key": ItemData(787801, ItemClassification.progression),
    "Green Key": ItemData(787801, ItemClassification.progression),
    "Blue Key": ItemData(787801, ItemClassification.progression),
    "Purple Key": ItemData(787801, ItemClassification.progression),
    "Sliding Knife": ItemData(787802, ItemClassification.progression),
    "Double Jump Knife": ItemData(787803, ItemClassification.progression),
    "Grip Knife": ItemData(787804, ItemClassification.progression), 
    "Screw Knife": ItemData(787805, ItemClassification.progression),
    "Dash Spike": ItemData(787805, ItemClassification.progression),
    "Ice Magatama": ItemData(787805, ItemClassification.progression),
    "Thousand Daggers": ItemData(787805, ItemClassification.useful),
    "Stun Knife": ItemData(787805, ItemClassification.useful),
    "Auto Aim": ItemData(787805, ItemClassification.useful),
    "Chainsaw": ItemData(787805, ItemClassification.useful),
    "Shield Dagger": ItemData(787805, ItemClassification.useful),
    "Bound Knife": ItemData(787805, ItemClassification.useful),
    "Holy Lost Sword": ItemData(787805, ItemClassification.useful),
    "HP Up": ItemData(787806, (ItemClassification.useful, 5)),
    "MP Up": ItemData(787807, (ItemClassification.useful, 5)),
    "Knife Up": ItemData(787808, (ItemClassification.useful, 5)),
    "Time Up": ItemData(787809, (ItemClassification.useful, 5))
}
