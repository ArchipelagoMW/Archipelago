from typing import List

from ..strings.crop_names import Fruit

all_pants = []
all_considered_pants = []


class Pant:
    name: str
    required_items: List[str]

    def __init__(self, name: str, items: List[str]):
        self.name = name
        self.required_items = items


# consider_in_logic exists as a temporary measure because I don't feel like writing out the logic for every single pant at this stage,
# and I only need some of them for the meme bundle
def pant(name: str, items: str | List[str], consider_in_logic: bool = True) -> Pant:
    if isinstance(items, str):
        items = [items]
    new_pant = Pant(name, items)
    all_pants.append(new_pant)
    if consider_in_logic:
        all_considered_pants.append(new_pant)
    return new_pant


class Pants:
    shorts = pant("Shorts", [Fruit.blueberry, Fruit.grape, Fruit.hot_pepper, Fruit.melon,])
