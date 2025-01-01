import math
from dataclasses import dataclass
from random import Random
from typing import List, Tuple

from .bundle_item import BundleItem
from ..content import StardewContent
from ..options import BundlePrice, StardewValleyOptions, ExcludeGingerIsland, FestivalLocations
from ..strings.currency_names import Currency


@dataclass
class Bundle:
    room: str
    name: str
    items: List[BundleItem]
    number_required: int

    def __repr__(self):
        return f"{self.name} -> {self.number_required} from {repr(self.items)}"


@dataclass
class BundleTemplate:
    room: str
    name: str
    items: List[BundleItem]
    number_possible_items: int
    number_required_items: int

    def __init__(self, room: str, name: str, items: List[BundleItem], number_possible_items: int,
                 number_required_items: int):
        self.room = room
        self.name = name
        self.items = items
        self.number_possible_items = number_possible_items
        self.number_required_items = number_required_items

    @staticmethod
    def extend_from(template, items: List[BundleItem]):
        return BundleTemplate(template.room, template.name, items, template.number_possible_items,
                              template.number_required_items)

    def create_bundle(self, random: Random, content: StardewContent, options: StardewValleyOptions) -> Bundle:
        number_required, price_multiplier = get_bundle_final_prices(options.bundle_price, self.number_required_items, False)
        filtered_items = [item for item in self.items if item.can_appear(content, options)]
        number_items = len(filtered_items)
        number_chosen_items = self.number_possible_items
        if number_chosen_items < number_required:
            number_chosen_items = number_required

        if number_chosen_items > number_items:
            chosen_items = filtered_items + random.choices(filtered_items, k=number_chosen_items - number_items)
        else:
            chosen_items = random.sample(filtered_items, number_chosen_items)
        chosen_items = [item.as_amount(max(1, math.floor(item.amount * price_multiplier))) for item in chosen_items]
        return Bundle(self.room, self.name, chosen_items, number_required)

    def can_appear(self, options: StardewValleyOptions) -> bool:
        return True


class CurrencyBundleTemplate(BundleTemplate):
    item: BundleItem

    def __init__(self, room: str, name: str, item: BundleItem):
        super().__init__(room, name, [item], 1, 1)
        self.item = item

    def create_bundle(self, random: Random, content: StardewContent, options: StardewValleyOptions) -> Bundle:
        currency_amount = self.get_currency_amount(options.bundle_price)
        return Bundle(self.room, self.name, [BundleItem(self.item.item_name, currency_amount)], 1)

    def get_currency_amount(self, bundle_price_option: BundlePrice):
        _, price_multiplier = get_bundle_final_prices(bundle_price_option, self.number_required_items, True)
        currency_amount = max(1, int(self.item.amount * price_multiplier))
        return currency_amount

    def can_appear(self, options: StardewValleyOptions) -> bool:
        if options.exclude_ginger_island == ExcludeGingerIsland.option_true:
            if self.item.item_name == Currency.qi_gem or self.item.item_name == Currency.golden_walnut or self.item.item_name == Currency.cinder_shard:
                return False
        if options.festival_locations == FestivalLocations.option_disabled:
            if self.item.item_name == Currency.star_token:
                return False
        return True


class MoneyBundleTemplate(CurrencyBundleTemplate):

    def __init__(self, room: str, default_name: str, item: BundleItem):
        super().__init__(room, default_name, item)

    def create_bundle(self, random: Random, content: StardewContent, options: StardewValleyOptions) -> Bundle:
        currency_amount = self.get_currency_amount(options.bundle_price)
        currency_name = "g"
        if currency_amount >= 1000:
            unit_amount = currency_amount % 1000
            unit_amount = "000" if unit_amount == 0 else unit_amount
            currency_display = f"{currency_amount // 1000},{unit_amount}"
        else:
            currency_display = f"{currency_amount}"
        name = f"{currency_display}{currency_name} Bundle"
        return Bundle(self.room, name, [BundleItem(self.item.item_name, currency_amount)], 1)

    def get_currency_amount(self, bundle_price_option: BundlePrice):
        _, price_multiplier = get_bundle_final_prices(bundle_price_option, self.number_required_items, True)
        currency_amount = max(1, int(self.item.amount * price_multiplier))
        return currency_amount


class IslandBundleTemplate(BundleTemplate):
    def can_appear(self, options: StardewValleyOptions) -> bool:
        return options.exclude_ginger_island == ExcludeGingerIsland.option_false


class FestivalBundleTemplate(BundleTemplate):
    def can_appear(self, options: StardewValleyOptions) -> bool:
        return options.festival_locations != FestivalLocations.option_disabled


class DeepBundleTemplate(BundleTemplate):
    categories: List[List[BundleItem]]

    def __init__(self, room: str, name: str, categories: List[List[BundleItem]], number_possible_items: int,
                 number_required_items: int):
        super().__init__(room, name, [], number_possible_items, number_required_items)
        self.categories = categories

    def create_bundle(self, random: Random, content: StardewContent, options: StardewValleyOptions) -> Bundle:
        number_required, price_multiplier = get_bundle_final_prices(options.bundle_price, self.number_required_items, False)
        number_categories = len(self.categories)
        number_chosen_categories = self.number_possible_items
        if number_chosen_categories < number_required:
            number_chosen_categories = number_required

        if number_chosen_categories > number_categories:
            chosen_categories = self.categories + random.choices(self.categories,
                                                                 k=number_chosen_categories - number_categories)
        else:
            chosen_categories = random.sample(self.categories, number_chosen_categories)

        chosen_items = []
        for category in chosen_categories:
            filtered_items = [item for item in category if item.can_appear(content, options)]
            chosen_items.append(random.choice(filtered_items))

        chosen_items = [item.as_amount(max(1, math.floor(item.amount * price_multiplier))) for item in chosen_items]
        return Bundle(self.room, self.name, chosen_items, number_required)


def get_bundle_final_prices(bundle_price_option: BundlePrice, default_required_items: int, is_currency: bool) -> Tuple[int, float]:
    number_required_items = get_number_required_items(bundle_price_option, default_required_items)
    price_multiplier = get_price_multiplier(bundle_price_option, is_currency)
    return number_required_items, price_multiplier


def get_number_required_items(bundle_price_option: BundlePrice, default_required_items: int) -> int:
    if bundle_price_option == BundlePrice.option_minimum:
        return 1
    if bundle_price_option == BundlePrice.option_maximum:
        return 8
    number_required = default_required_items + bundle_price_option.value
    return min(8, max(1, number_required))


def get_price_multiplier(bundle_price_option: BundlePrice, is_currency: bool) -> float:
    if bundle_price_option == BundlePrice.option_minimum:
        return 0.1 if is_currency else 0.2
    if bundle_price_option == BundlePrice.option_maximum:
        return 4 if is_currency else 1.4
    price_factor = 0.4 if is_currency else (0.2 if bundle_price_option.value <= 0 else 0.1)
    price_multiplier_difference = bundle_price_option.value * price_factor
    price_multiplier = 1 + price_multiplier_difference
    return round(price_multiplier, 2)
