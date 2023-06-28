from BaseClasses import Item, ItemClassification
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: any
    quantity: int = 1


class TLNItem(Item):
    game: str = "TLN"


item_table = {
    "Red Key":              ItemData(787801, ItemClassification.progression),
    "Yellow Key":           ItemData(787802, ItemClassification.progression),
    "Green Key":            ItemData(787803, ItemClassification.progression),
    "Blue Key":             ItemData(787804, ItemClassification.progression),
    "Purple Key":           ItemData(787805, ItemClassification.progression),

    "Sliding Knife":        ItemData(787806, ItemClassification.progression),
    "Double Jump Knife":    ItemData(787807, ItemClassification.progression),
    "Grip Knife":           ItemData(787808, ItemClassification.progression),
    "Screw Knife":          ItemData(787809, ItemClassification.progression),
    "Dash Spike":           ItemData(787810, ItemClassification.progression),
    "Ice Magatama":         ItemData(787811, ItemClassification.progression),

    "Thousand Daggers":     ItemData(787812, ItemClassification.useful),
    "Stun Knife":           ItemData(787813, ItemClassification.useful),
    "Auto Aim":             ItemData(787814, ItemClassification.useful),
    "Chainsaw":             ItemData(787815, ItemClassification.useful),
    "Shield Dagger":        ItemData(787816, ItemClassification.useful),
    "Bound Knife":          ItemData(787817, ItemClassification.useful),
    "Holy Lost Sword":      ItemData(787818, ItemClassification.useful),

    "HP Up":              ItemData(787819, ItemClassification.useful, 5),
    "MP Up":              ItemData(787824, ItemClassification.useful, 5),
    "Knife Up":           ItemData(787829, ItemClassification.useful, 5),
    "Time Up":            ItemData(787834, ItemClassification.useful, 5),
}

