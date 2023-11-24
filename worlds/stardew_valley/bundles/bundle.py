from random import Random
from typing import List

from .bundle_item import BundleItem
from ..strings.currency_names import Currency


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
        if price_difference > 0 and self.number_possible_items > 10:
            number_required += price_difference
        number_required = max(1, number_required)
        filtered_items = [item for item in self.items if allow_island_items or not item.requires_island]
        number_items = len(filtered_items)
        number_chosen_items = self.number_possible_items
        if number_chosen_items < number_required:
            number_chosen_items = number_required

        if number_chosen_items > number_items:
            chosen_items = filtered_items + random.choices(filtered_items, k=number_chosen_items - number_items)
        else:
            chosen_items = random.sample(filtered_items, number_chosen_items)
        return Bundle(self.room, self.name, chosen_items, number_required)

    @property
    def requires_island(self) -> bool:
        return False


class CurrencyBundleTemplate(BundleTemplate):
    item: BundleItem

    def __init__(self, room: str, name: str, item: BundleItem):
        super().__init__(room, name, [item], 1, 1)
        self.item = item

    def create_bundle(self, price_difference: int, random: Random, allow_island_items: bool) -> Bundle:
        currency_amount = self.get_currency_amount(price_difference)
        return Bundle(self.room, self.name, [BundleItem(self.item.item_name, currency_amount)], 1)

    def get_currency_amount(self, price_difference):
        price_multiplier = round(1 + (price_difference * 0.4), 2)
        currency_amount = int(self.item.amount * price_multiplier)
        return currency_amount

    @property
    def requires_island(self) -> bool:
        return self.item.item_name == Currency.qi_gem or self.item.item_name == Currency.golden_walnut


class MoneyBundleTemplate(CurrencyBundleTemplate):

    def __init__(self, room: str, item: BundleItem):
        super().__init__(room, "", item)

    def create_bundle(self, price_difference: int, random: Random, allow_island_items: bool) -> Bundle:
        currency_amount = self.get_currency_amount(price_difference)
        currency_name = "g"
        if currency_amount >= 1000:
            unit_amount = currency_amount % 1000
            unit_amount = "000" if unit_amount == 0 else unit_amount
            currency_display = f"{currency_amount // 1000},{unit_amount}"
        else:
            currency_display = f"{currency_amount}"
        name = f"{currency_display}{currency_name} Bundle"
        return Bundle(self.room, name, [BundleItem(self.item.item_name, currency_amount)], 1)

    def get_currency_amount(self, price_difference):
        price_multiplier = round(1 + (price_difference * 0.4), 2)
        currency_amount = int(self.item.amount * price_multiplier)
        return currency_amount


class IslandBundleTemplate(BundleTemplate):

    @property
    def requires_island(self) -> bool:
        return True


class DeepBundleTemplate(BundleTemplate):
    categories: List[List[BundleItem]]

    def __init__(self, room: str, name: str, categories: List[List[BundleItem]], number_possible_items: int, number_required_items: int):
        super().__init__(room, name, [], number_possible_items, number_required_items)
        self.categories = categories

    def create_bundle(self, price_difference: int, random: Random, allow_island_items: bool) -> Bundle:
        number_required = self.number_required_items + price_difference
        number_categories = len(self.categories)
        number_chosen_categories = self.number_possible_items
        if number_chosen_categories < number_required:
            number_chosen_categories = number_required

        if number_chosen_categories > number_categories:
            chosen_categories = self.categories + random.choices(self.categories, k=number_chosen_categories - number_categories)
        else:
            chosen_categories = random.sample(self.categories, number_chosen_categories)

        chosen_items = []
        for category in chosen_categories:
            filtered_items = [item for item in category if allow_island_items or not item.requires_island]
            chosen_items.append(random.choice(filtered_items))

        return Bundle(self.room, self.name, chosen_items, number_required)

