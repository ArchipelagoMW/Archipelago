from typing import List

from ..strings.animal_product_names import AnimalProduct
from ..strings.forageable_names import Forageable
from ..strings.material_names import Material

all_shirts = []
all_considered_shirts = []


class Shirt:
    name: str
    required_items: List[str]

    def __init__(self, name: str, items: List[str]):
        self.name = name
        self.required_items = items


# consider_in_logic exists as a temporary measure because I don't feel like writing out the logic for every single shirt at this stage,
# and I only need some of them for the meme bundle
def shirt(name: str, items: str | List[str], consider_in_logic: bool = True) -> Shirt:
    if isinstance(items, str):
        items = [items]
    new_shirt = Shirt(name, items)
    all_shirts.append(new_shirt)
    if consider_in_logic:
        all_considered_shirts.append(new_shirt)
    return new_shirt


class Shirts:
    basic_shirt = shirt("Shirt", Material.clay)
    vacation = shirt("Vacation Shirt", Forageable.coconut)
    green_jacket = shirt("Green Jacket Shirt", AnimalProduct.duck_egg)
