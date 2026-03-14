from .base_logic import BaseLogic, BaseLogicMixin
from ..data.craftable_data import all_crafting_recipes_by_name
from ..data.recipe_data import all_cooking_recipes_by_name
from ..locations import LocationTags, locations_by_tag
from ..mods.mod_data import ModNames
from ..options import options
from ..stardew_rule import StardewRule
from ..strings.ap_names.ap_option_names import SecretsanityOptionName
from ..strings.building_names import Building
from ..strings.crop_names import Fruit
from ..strings.quest_names import Quest
from ..strings.region_names import Region
from ..strings.season_names import Season
from ..strings.wallet_item_names import Wallet


class GoalLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.goal = GoalLogic(*args, **kwargs)


class GoalLogic(BaseLogic):

    def can_complete_community_center(self) -> StardewRule:
        return self.logic.bundle.can_complete_community_center

    def can_finish_grandpa_evaluation(self) -> StardewRule:
        # https://stardewvalleywiki.com/Grandpa
        rules_worth_a_point = [
            self.logic.money.can_have_earned_total(50_000),
            self.logic.money.can_have_earned_total(100_000),
            self.logic.money.can_have_earned_total(200_000),
            self.logic.money.can_have_earned_total(300_000),
            self.logic.money.can_have_earned_total(500_000),
            self.logic.money.can_have_earned_total(1_000_000),  # first point
            self.logic.money.can_have_earned_total(1_000_000),  # second point
            self.logic.skill.has_total_level(30),
            self.logic.skill.has_total_level(50),
            self.logic.museum.can_complete_museum(),
            # Catching every fish not expected
            # Shipping every item not expected
            self.logic.relationship.can_get_married() & self.logic.building.has_building(Building.kids_room),
            self.logic.relationship.has_hearts_with_n(5, 8),  # 5 Friends
            self.logic.relationship.has_hearts_with_n(10, 8),  # 10 friends
            self.logic.pet.has_pet_hearts(5),  # Max Pet
            self.logic.bundle.can_complete_community_center,  # 1 point for Community Center Completion
            self.logic.bundle.can_complete_community_center,  # Ceremony first point
            self.logic.bundle.can_complete_community_center,  # Ceremony second point
            self.logic.received(Wallet.skull_key),
            self.logic.wallet.has_rusty_key(),
        ]
        return self.logic.count(12, *rules_worth_a_point)

    def can_complete_bottom_of_the_mines(self) -> StardewRule:
        # The location is in the bottom of the mines region, so no actual rule is required
        return self.logic.true_

    def can_complete_cryptic_note(self) -> StardewRule:
        return self.logic.quest.can_complete_quest(Quest.cryptic_note)

    def can_complete_master_angler(self) -> StardewRule:
        if not self.content.features.fishsanity.is_enabled:
            return self.logic.fishing.can_catch_every_fish()

        rules = [self.logic.fishing.has_max_fishing]

        rules.extend(
            self.logic.fishing.can_catch_fish_for_fishsanity(fish)
            for fish in self.content.fishes.values()
            if self.content.features.fishsanity.is_included(fish)
        )

        return self.logic.and_(*rules)

    def can_complete_complete_collection(self) -> StardewRule:
        return self.logic.museum.can_complete_museum()

    def can_complete_full_house(self) -> StardewRule:
        return self.logic.relationship.has_children(2) & self.logic.relationship.can_reproduce()

    def can_complete_greatest_walnut_hunter(self) -> StardewRule:
        return self.logic.walnut.has_walnut(130)

    def can_complete_protector_of_the_valley(self) -> StardewRule:
        return self.logic.monster.can_complete_all_monster_slaying_goals()

    def can_complete_full_shipment(self, all_location_names_in_slot: list[str]) -> StardewRule:
        if self.options.shipsanity == options.Shipsanity.option_none:
            return self.logic.shipping.can_ship_everything()

        rules = [self.logic.building.has_building(Building.shipping_bin)]

        for shipsanity_location in locations_by_tag[LocationTags.SHIPSANITY]:
            if shipsanity_location.name not in all_location_names_in_slot:
                continue
            rules.append(self.logic.region.can_reach_location(shipsanity_location.name))
        return self.logic.and_(*rules)

    def can_complete_gourmet_chef(self) -> StardewRule:
        cooksanity_prefix = "Cook "
        all_recipes_names = []
        for location in locations_by_tag[LocationTags.COOKSANITY]:
            if not self.content.are_all_enabled(location.content_packs):
                continue
            all_recipes_names.append(location.name[len(cooksanity_prefix):])
        all_recipes = [all_cooking_recipes_by_name[recipe_name] for recipe_name in all_recipes_names]
        return self.logic.and_(*(self.logic.cooking.can_cook(recipe) for recipe in all_recipes))

    def can_complete_craft_master(self) -> StardewRule:
        craftsanity_prefix = "Craft "
        all_recipes_names = []
        exclude_masteries = not self.content.features.skill_progression.are_masteries_shuffled
        for location in locations_by_tag[LocationTags.CRAFTSANITY]:
            if not location.name.startswith(craftsanity_prefix):
                continue
            # FIXME Remove when recipes are in content packs
            if exclude_masteries and LocationTags.REQUIRES_MASTERIES in location.tags:
                continue
            if not self.content.are_all_enabled(location.content_packs):
                continue
            all_recipes_names.append(location.name[len(craftsanity_prefix):])
        all_recipes = [all_crafting_recipes_by_name[recipe_name] for recipe_name in all_recipes_names]
        return self.logic.and_(*(self.logic.crafting.can_craft(recipe) for recipe in all_recipes))

    def can_complete_legend(self) -> StardewRule:
        return self.logic.money.can_have_earned_total(10_000_000)

    def can_complete_mystery_of_the_stardrop(self) -> StardewRule:
        other_rules = []
        number_of_stardrops_to_receive = 0
        number_of_stardrops_to_receive += 1  # The Mines level 100
        number_of_stardrops_to_receive += 1  # Museum Stardrop
        number_of_stardrops_to_receive += 1  # Krobus Stardrop

        # Master Angler Stardrop
        if self.content.features.fishsanity.is_enabled:
            number_of_stardrops_to_receive += 1
        else:
            other_rules.append(self.logic.fishing.can_catch_every_fish())

        if self.options.festival_locations == options.FestivalLocations.option_disabled:  # Fair Stardrop
            other_rules.append(self.logic.season.has(Season.fall))
        else:
            number_of_stardrops_to_receive += 1

        # Spouse Stardrop
        if self.content.features.friendsanity.is_enabled:
            number_of_stardrops_to_receive += 1
        else:
            other_rules.append(self.logic.relationship.has_hearts_with_any_bachelor(13))

        # Old Master Cannoli
        if SecretsanityOptionName.easy in self.options.secretsanity:
            number_of_stardrops_to_receive += 1
        else:
            other_rules.append(self.logic.has(Fruit.sweet_gem_berry) & self.logic.region.can_reach(Region.secret_woods))

        if self.content.is_enabled(ModNames.deepwoods):  # Petting the Unicorn
            number_of_stardrops_to_receive += 1

        return self.logic.received("Stardrop", number_of_stardrops_to_receive) & self.logic.and_(*other_rules, allow_empty=True)

    def can_complete_mad_hatter(self, all_location_names_in_slot: list[str]) -> StardewRule:
        if not self.content.features.hatsanity.is_enabled:
            raise Exception("Cannot play Mad Hatter Goal without Hatsanity")

        rules = []

        for hatsanity_location in locations_by_tag[LocationTags.HATSANITY]:
            if hatsanity_location.name not in all_location_names_in_slot:
                continue
            rules.append(self.logic.region.can_reach_location(hatsanity_location.name))
        return self.logic.and_(*rules)

    def can_complete_ultimate_foodie(self, all_location_names_in_slot: list[str]) -> StardewRule:
        if not self.options.eatsanity.value:
            raise Exception("Cannot play Ultimate Foodie Goal without Eatsanity")

        rules = []

        for eatsanity_location in locations_by_tag[LocationTags.EATSANITY]:
            if eatsanity_location.name not in all_location_names_in_slot:
                continue
            rules.append(self.logic.region.can_reach_location(eatsanity_location.name))
        return self.logic.and_(*rules)

    def can_complete_allsanity(self) -> StardewRule:
        return self.logic.has_progress_percent(100)

    def can_complete_perfection(self) -> StardewRule:
        return self.logic.has_progress_percent(100)
