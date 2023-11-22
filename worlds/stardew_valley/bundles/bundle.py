from random import Random
from typing import List

from worlds.stardew_valley.bundles.bundle_item import BundleItem


class Bundle:
    room: str
    name: str
    items: List[BundleItem]
    number_required: int

    def __init__(self, room: str, name: str, items: List[BundleItem], number_required):
        self.room = room
        self.name = name
        self.items = items
        self.number_required = number_required

    def __repr__(self):
        return f"{self.name} -> {self.number_required} from {repr(self.items)}"


class BundleTemplate:
    room: str
    name: str
    items: List[BundleItem]
    number_possible_items: int
    number_required_items: int

    def __init__(self, room: str, name: str, items: List[BundleItem], number_possible_items: int, number_required_items: int):
        self.room = room
        self.name = name
        self.items = items
        self.number_possible_items = number_possible_items
        self.number_required_items = number_required_items

    @staticmethod
    def extend_from(template, items: List[BundleItem]):
        return BundleTemplate(template.room, template.name, items, template.number_possible_items, template.number_required_items)

    def create_bundle(self, price_difference: int, random: Random, allow_island_items: bool) -> Bundle:
        number_required = self.number_required_items + price_difference
        filtered_items = [item for item in self.items if allow_island_items or not item.requires_island]
        number_items = len(filtered_items)
        number_chosen_items = self.number_possible_items
        if number_chosen_items < number_required:
            number_chosen_items = number_required

        if number_chosen_items > number_items:
            chosen_items = random.choices(filtered_items, k=number_chosen_items)
        else:
            chosen_items = random.sample(filtered_items, number_chosen_items)
        return Bundle(self.room, self.name, chosen_items, number_required)

    @property
    def requires_island(self) -> bool:
        return False


class IslandBundleTemplate(BundleTemplate):

    @property
    def requires_island(self) -> bool:
        return True

