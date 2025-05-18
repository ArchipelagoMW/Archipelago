from typing import List

from worlds.stardew_valley.strings.animal_product_names import AnimalProduct
from worlds.stardew_valley.strings.artisan_good_names import ArtisanGood
from worlds.stardew_valley.strings.forageable_names import Forageable

all_shirts = []
all_considered_shirts = []


class Shirt:
    name: str
    required_items: List[str]
    requires_cloth: bool

    def __init__(self, name: str, items: List[str], requires_cloth: bool = True):
        self.name = name
        self.required_items = items
        self.requires_cloth = requires_cloth

    def get_all_required_items(self):
        items = [i for i in self.required_items]
        if self.requires_cloth:
            items.append(ArtisanGood.cloth)
        return items


# consider_in_logic exists as a temporary measure because I don't feel like writing out the logic for every single shirt at this stage,
# and I only need some of them for the meme bundle
def shirt(name: str, items: str | List[str], requires_cloth: bool = True, consider_in_logic: bool = True) -> Shirt:
    if isinstance(items, str):
        items = [items]
    new_shirt = Shirt(name, items, requires_cloth)
    all_shirts.append(new_shirt)
    if consider_in_logic:
        all_considered_shirts.append(new_shirt)
    return new_shirt


class Shirts:
    vacation = shirt("Vacation Shirt", Forageable.coconut)
    green_jacket = shirt("Green Jacket Shirt", AnimalProduct.duck_egg)
