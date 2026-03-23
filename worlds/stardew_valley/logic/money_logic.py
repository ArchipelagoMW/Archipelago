from Options import DeathLink
from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from ..content.vanilla.qi_board import qi_board_content_pack
from ..data.shop import ShopSource, HatMouseSource
from ..stardew_rule import StardewRule, True_, HasProgressionPercent, False_, true_
from ..strings.animal_names import Animal
from ..strings.ap_names.ap_option_names import CustomLogicOptionName
from ..strings.ap_names.event_names import Event
from ..strings.artisan_good_names import ArtisanGood
from ..strings.building_names import Building
from ..strings.crop_names import Vegetable
from ..strings.currency_names import Currency, MemeCurrency
from ..strings.food_names import Beverage
from ..strings.region_names import Region, LogicRegion
from ..strings.season_names import Season

qi_gem_rewards = ("100 Qi Gems", "50 Qi Gems", "40 Qi Gems", "35 Qi Gems", "25 Qi Gems",
                  "20 Qi Gems", "15 Qi Gems", "10 Qi Gems")


class MoneyLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.money = MoneyLogic(*args, **kwargs)


class MoneyLogic(BaseLogic):

    @cache_self1
    def can_have_earned_total(self, amount: int) -> StardewRule:

        if CustomLogicOptionName.nightmare_money in self.options.custom_logic:
            amount /= 20
        elif CustomLogicOptionName.extreme_money in self.options.custom_logic:
            amount /= 8
        elif CustomLogicOptionName.hard_money in self.options.custom_logic:
            amount /= 2
        elif CustomLogicOptionName.easy_money in self.options.custom_logic:
            amount *= 4

        if amount <= 1000:
            return self.logic.true_

        shipping_rule = self.logic.shipping.can_use_shipping_bin
        pierre_rule = self.logic.region.can_reach_all(Region.pierre_store, Region.forest)
        willy_rule = self.logic.region.can_reach_all(Region.fish_shop, LogicRegion.fishing)
        clint_rule = self.logic.region.can_reach_all(Region.blacksmith, Region.mines_floor_5)
        robin_rule = self.logic.region.can_reach_all(Region.carpenter, Region.secret_woods)
        farming_rule = self.logic.farming.can_plant_and_grow_item(Season.not_winter)

        if amount <= 2000:
            selling_any_rule = shipping_rule | pierre_rule | willy_rule | clint_rule | robin_rule
            return selling_any_rule

        if amount <= 3000:
            selling_any_rule = shipping_rule | pierre_rule | willy_rule
            return selling_any_rule

        if amount <= 5000:
            selling_all_rule = shipping_rule | (pierre_rule & farming_rule) | (pierre_rule & willy_rule & clint_rule & robin_rule)
            return selling_all_rule

        if amount <= 10000:
            return shipping_rule & farming_rule

        seed_rules = self.logic.region.can_reach(Region.pierre_store)
        if amount <= 40000:
            return shipping_rule & seed_rules & farming_rule

        percent_progression_items_needed = min(90, amount // 20000)
        return shipping_rule & seed_rules & farming_rule & HasProgressionPercent(self.player, percent_progression_items_needed)

    @cache_self1
    def can_spend(self, amount: int) -> StardewRule:
        if self.options.starting_money == -1:
            return True_()
        spend_earned_multiplier = 5  # We assume that if you earned 5x an amount, you can reasonably spend that amount on things
        return self.logic.money.can_have_earned_total(amount * spend_earned_multiplier)

    # Should be cached
    def can_spend_at(self, region: str, amount: int) -> StardewRule:
        return self.logic.region.can_reach(region) & self.logic.money.can_spend(amount)

    def can_shop_from_hat_mouse(self, source: HatMouseSource) -> StardewRule:
        money_rule = self.logic.money.can_spend(source.price) if source.price is not None else true_
        region_rule = self.logic.region.can_reach(LogicRegion.hat_mouse)
        requirements_rule = self.logic.requirement.meet_all_requirements(source.unlock_requirements) if source.unlock_requirements is not None else true_
        return money_rule & region_rule & requirements_rule

    @cache_self1
    def can_shop_from(self, source: ShopSource) -> StardewRule:
        season_rule = self.logic.season.has_any(source.seasons)
        if source.currency == Currency.money:
            money_rule = self.logic.money.can_spend(source.price) if source.price is not None else true_
        else:
            money_rule = self.logic.money.can_trade_at(source.shop_region, source.currency, source.price) if source.price is not None else true_

        item_rules = []
        if source.items_price is not None:
            for price, item in source.items_price:
                item_rules.append(self.logic.grind.can_grind_item(price, item))

        region_rule = self.logic.region.can_reach(source.shop_region)

        return self.logic.and_(season_rule, money_rule, *item_rules, region_rule)

    # Should be cached
    def can_trade(self, currency: str, amount: int) -> StardewRule:
        if amount == 0:
            return self.logic.true_

        if currency == Currency.money or currency == MemeCurrency.bank_money:
            return self.can_spend(amount)
        if currency == Currency.star_token:
            return self.logic.region.can_reach(LogicRegion.fair)
        if currency == Currency.qi_coin:
            return self.logic.region.can_reach(Region.casino) & self.logic.time.has_lived_months(amount // 1000)
        if currency == Currency.qi_gem:
            if self.content.is_enabled(qi_board_content_pack):
                return self.logic.received(Event.received_qi_gems, amount * 3)
            return self.logic.region.can_reach_all(Region.qi_walnut_room, Region.saloon) & self.can_have_earned_total(5000)
        if currency == Currency.golden_walnut:
            return self.can_spend_walnut(amount)

        if currency == MemeCurrency.code or currency == MemeCurrency.energy or currency == MemeCurrency.blood:
            return self.logic.true_
        if currency == MemeCurrency.clic and amount < 100:
            return self.logic.true_
        if currency == MemeCurrency.clic or currency == MemeCurrency.time:
            return self.logic.time.has_lived_months(1)

        if currency == MemeCurrency.steps and amount < 6000:
            return self.logic.true_
        if currency == MemeCurrency.steps:
            return self.logic.time.has_lived_months(amount // 10000)

        if currency == MemeCurrency.cookies:
            return self.logic.time.has_lived_months(amount // 10000)
        if currency == MemeCurrency.child:
            return self.logic.relationship.has_children(1)
        if currency == MemeCurrency.dead_crops:
            return self.logic.season.has_all() & self.logic.skill.can_get_farming_xp & self.logic.money.can_spend(amount * 100)
        if currency == MemeCurrency.dead_pumpkins:
            return self.logic.season.has(Season.fall) & self.logic.season.has_any([Season.spring, Season.summer, Season.winter]) & \
                self.logic.has(Vegetable.pumpkin) & self.logic.money.can_spend(amount * 100)
        if currency == MemeCurrency.missed_fish:
            return self.logic.fishing.can_catch_many_fish(max(1, amount // 4))
        if currency == MemeCurrency.honeywell:
            return self.logic.has(ArtisanGood.honey) & self.logic.building.has_building(Building.well)
        if currency == MemeCurrency.goat:
            return self.logic.animal.has_animal(Animal.goat)

        if currency == MemeCurrency.sleep_days:
            if not self.options.multiple_day_sleep_enabled.value:
                return self.logic.false_
            if amount > 200:
                return self.logic.region.can_reach(Region.farm_house) & self.logic.season.has(Season.winter)
            return self.logic.region.can_reach(Region.farm_house)

        if currency == MemeCurrency.time_elapsed:
            if amount <= 1000:
                return self.logic.true_
            if amount <= 1400:
                return self.logic.has(Beverage.coffee)
            if amount <= 1800:
                return self.logic.building.has_building(Building.stable)
            return self.logic.has(Beverage.coffee) & self.logic.building.has_building(Building.stable)

        if currency == MemeCurrency.deathlinks:
            if self.options.death_link == DeathLink.option_true:
                return self.logic.time.has_lived_months(amount)
            return self.logic.false_

        return self.logic.grind.can_grind_item(amount, currency)

    # Should be cached
    def can_trade_at(self, region: str, currency: str, amount: int) -> StardewRule:
        if amount == 0:
            return True_()
        if currency == Currency.money:
            return self.logic.money.can_spend_at(region, amount)

        return self.logic.region.can_reach(region) & self.can_trade(currency, amount)

    def can_spend_walnut(self, amount: int) -> StardewRule:
        return False_()
