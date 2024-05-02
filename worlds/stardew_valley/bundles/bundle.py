from dataclasses import dataclass
from random import Random
from typing import List

from .bundle_item import BundleItem
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

    def __init__(self, room: str, name: str, items: List[BundleItem], number_possible_items: int, number_required_items: int):
        self.room = room
        self.name = name
        self.items = items
        self.number_possible_items = number_possible_items
        self.number_required_items = number_required_items

    @staticmethod
    def extend_from(template, items: List[BundleItem]):
        return BundleTemplate(template.room, template.name, items, template.number_possible_items, template.number_required_items)

    def create_bundle(self, bundle_price_option: BundlePrice, random: Random, options: StardewValleyOptions) -> Bundle:
        if bundle_price_option == BundlePrice.option_minimum:
            number_required = 1
        elif bundle_price_option == BundlePrice.option_maximum:
            number_required = 8
        else:
            number_required = self.number_required_items + bundle_price_option.value
        number_required = max(1, number_required)
        filtered_items = [item for item in self.items if item.can_appear(options)]
        number_items = len(filtered_items)
        number_chosen_items = self.number_possible_items
        if number_chosen_items < number_required:
            number_chosen_items = number_required

        if number_chosen_items > number_items:
            chosen_items = filtered_items + random.choices(filtered_items, k=number_chosen_items - number_items)
        else:
            chosen_items = random.sample(filtered_items, number_chosen_items)
        return Bundle(self.room, self.name, chosen_items, number_required)

    def can_appear(self, options: StardewValleyOptions) -> bool:
        return True


class CurrencyBundleTemplate(BundleTemplate):
    item: BundleItem

    def __init__(self, room: str, name: str, item: BundleItem):
        super().__init__(room, name, [item], 1, 1)
        self.item = item

    def create_bundle(self, bundle_price_option: BundlePrice, random: Random, options: StardewValleyOptions) -> Bundle:
        currency_amount = self.get_currency_amount(bundle_price_option)
        return Bundle(self.room, self.name, [BundleItem(self.item.item_name, currency_amount)], 1)

    def get_currency_amount(self, bundle_price_option: BundlePrice):
        if bundle_price_option == BundlePrice.option_minimum:
            price_multiplier = 0.1
        elif bundle_price_option == BundlePrice.option_maximum:
            price_multiplier = 4
        else:
            price_multiplier = round(1 + (bundle_price_option.value * 0.4), 2)

        currency_amount = int(self.item.amount * price_multiplier)
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

    def __init__(self, room: str, item: BundleItem):
        super().__init__(room, "", item)

    def create_bundle(self, bundle_price_option: BundlePrice, random: Random, options: StardewValleyOptions) -> Bundle:
        currency_amount = self.get_currency_amount(bundle_price_option)
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
        if bundle_price_option == BundlePrice.option_minimum:
            price_multiplier = 0.1
        elif bundle_price_option == BundlePrice.option_maximum:
            price_multiplier = 4
        else:
            price_multiplier = round(1 + (bundle_price_option.value * 0.4), 2)
        currency_amount = int(self.item.amount * price_multiplier)
        return currency_amount


class IslandBundleTemplate(BundleTemplate):
    def can_appear(self, options: StardewValleyOptions) -> bool:
        return options.exclude_ginger_island == ExcludeGingerIsland.option_false


class FestivalBundleTemplate(BundleTemplate):
    def can_appear(self, options: StardewValleyOptions) -> bool:
        return options.festival_locations != FestivalLocations.option_disabled


class DeepBundleTemplate(BundleTemplate):
    categories: List[List[BundleItem]]

    def __init__(self, room: str, name: str, categories: List[List[BundleItem]], number_possible_items: int, number_required_items: int):
        super().__init__(room, name, [], number_possible_items, number_required_items)
        self.categories = categories

    def create_bundle(self, bundle_price_option: BundlePrice, random: Random, options: StardewValleyOptions) -> Bundle:
        if bundle_price_option == BundlePrice.option_minimum:
            number_required = 1
        elif bundle_price_option == BundlePrice.option_maximum:
            number_required = 8
        else:
            number_required = self.number_required_items + bundle_price_option.value
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
            filtered_items = [item for item in category if item.can_appear(options)]
            chosen_items.append(random.choice(filtered_items))

        return Bundle(self.room, self.name, chosen_items, number_required)
