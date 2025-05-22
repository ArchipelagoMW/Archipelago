from .base_logic import BaseLogicMixin, BaseLogic
from ..options import FestivalLocations
from ..stardew_rule import StardewRule
from ..strings.animal_product_names import AnimalProduct
from ..strings.book_names import Book
from ..strings.craftable_names import Fishing
from ..strings.crop_names import Fruit, Vegetable
from ..strings.festival_check_names import FestivalCheck
from ..strings.fish_names import Fish
from ..strings.forageable_names import Forageable
from ..strings.generic_names import Generic
from ..strings.machine_names import Machine
from ..strings.monster_names import Monster
from ..strings.region_names import Region


class FestivalLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.festival = FestivalLogic(*args, **kwargs)


class FestivalLogic(BaseLogic):

    def initialize_rules(self):
        self.registry.festival_rules.update({
            FestivalCheck.egg_hunt: self.logic.festival.can_win_egg_hunt(),
            FestivalCheck.strawberry_seeds: self.logic.money.can_spend(1000),
            FestivalCheck.dance: self.logic.relationship.has_hearts_with_any_bachelor(4),
            FestivalCheck.tub_o_flowers: self.logic.money.can_spend(2000),
            FestivalCheck.rarecrow_5: self.logic.money.can_spend(2500),
            FestivalCheck.luau_soup: self.logic.festival.can_succeed_luau_soup(),
            FestivalCheck.moonlight_jellies: self.logic.true_,
            FestivalCheck.moonlight_jellies_banner: self.logic.money.can_spend(800),
            FestivalCheck.starport_decal: self.logic.money.can_spend(1000),
            FestivalCheck.smashing_stone: self.logic.true_,
            FestivalCheck.grange_display: self.logic.festival.can_succeed_grange_display(),
            FestivalCheck.rarecrow_1: self.logic.true_,  # only cost star tokens
            FestivalCheck.fair_stardrop: self.logic.true_,  # only cost star tokens
            FestivalCheck.spirit_eve_maze: self.logic.true_,
            FestivalCheck.jack_o_lantern: self.logic.money.can_spend(2000),
            FestivalCheck.rarecrow_2: self.logic.money.can_spend(5000),
            FestivalCheck.fishing_competition: self.logic.festival.can_win_fishing_competition(),
            FestivalCheck.rarecrow_4: self.logic.money.can_spend(5000),
            FestivalCheck.mermaid_pearl: self.logic.has(Forageable.secret_note),
            FestivalCheck.cone_hat: self.logic.money.can_spend(2500),
            FestivalCheck.iridium_fireplace: self.logic.money.can_spend(15000),
            FestivalCheck.rarecrow_7: self.logic.money.can_spend(5000) & self.logic.museum.can_donate_museum_artifacts(20),
            FestivalCheck.rarecrow_8: self.logic.money.can_spend(5000) & self.logic.museum.can_donate_museum_items(40),
            FestivalCheck.lupini_red_eagle: self.logic.money.can_spend(1200),
            FestivalCheck.lupini_portrait_mermaid: self.logic.money.can_spend(1200),
            FestivalCheck.lupini_solar_kingdom: self.logic.money.can_spend(1200),
            FestivalCheck.lupini_clouds: self.logic.time.has_year_two & self.logic.money.can_spend(1200),
            FestivalCheck.lupini_1000_years: self.logic.time.has_year_two & self.logic.money.can_spend(1200),
            FestivalCheck.lupini_three_trees: self.logic.time.has_year_two & self.logic.money.can_spend(1200),
            FestivalCheck.lupini_the_serpent: self.logic.time.has_year_three & self.logic.money.can_spend(1200),
            FestivalCheck.lupini_tropical_fish: self.logic.time.has_year_three & self.logic.money.can_spend(1200),
            FestivalCheck.lupini_land_of_clay: self.logic.time.has_year_three & self.logic.money.can_spend(1200),
            FestivalCheck.secret_santa: self.logic.gifts.has_any_universal_love,
            FestivalCheck.legend_of_the_winter_star: self.logic.true_,
            FestivalCheck.rarecrow_3: self.logic.true_,
            FestivalCheck.all_rarecrows: self.logic.region.can_reach(Region.farm) & self.logic.festival.has_all_rarecrows(),
            FestivalCheck.calico_race: self.logic.true_,
            FestivalCheck.mummy_mask: self.logic.true_,
            FestivalCheck.calico_statue: self.logic.true_,
            FestivalCheck.emily_outfit_service: self.logic.true_,
            FestivalCheck.earthy_mousse: self.logic.true_,
            FestivalCheck.sweet_bean_cake: self.logic.true_,
            FestivalCheck.skull_cave_casserole: self.logic.true_,
            FestivalCheck.spicy_tacos: self.logic.true_,
            FestivalCheck.mountain_chili: self.logic.true_,
            FestivalCheck.crystal_cake: self.logic.true_,
            FestivalCheck.cave_kebab: self.logic.true_,
            FestivalCheck.hot_log: self.logic.true_,
            FestivalCheck.sour_salad: self.logic.true_,
            FestivalCheck.superfood_cake: self.logic.true_,
            FestivalCheck.warrior_smoothie: self.logic.true_,
            FestivalCheck.rumpled_fruit_skin: self.logic.true_,
            FestivalCheck.calico_pizza: self.logic.true_,
            FestivalCheck.stuffed_mushrooms: self.logic.true_,
            FestivalCheck.elf_quesadilla: self.logic.true_,
            FestivalCheck.nachos_of_the_desert: self.logic.true_,
            FestivalCheck.cloppino: self.logic.true_,
            FestivalCheck.rainforest_shrimp: self.logic.true_,
            FestivalCheck.shrimp_donut: self.logic.true_,
            FestivalCheck.smell_of_the_sea: self.logic.true_,
            FestivalCheck.desert_gumbo: self.logic.true_,
            FestivalCheck.free_cactis: self.logic.true_,
            FestivalCheck.monster_hunt: self.logic.monster.can_kill(Monster.serpent),
            FestivalCheck.deep_dive: self.logic.region.can_reach(Region.skull_cavern_50),
            FestivalCheck.treasure_hunt: self.logic.region.can_reach(Region.skull_cavern_25),
            FestivalCheck.touch_calico_statue: self.logic.region.can_reach(Region.skull_cavern_25),
            FestivalCheck.real_calico_egg_hunter: self.logic.region.can_reach(Region.skull_cavern_100),
            FestivalCheck.willy_challenge: self.logic.fishing.can_catch_fish(self.content.fishes[Fish.scorpion_carp]),
            FestivalCheck.desert_scholar: self.logic.true_,
            FestivalCheck.squidfest_day_1_copper: self.logic.fishing.can_catch_fish(self.content.fishes[Fish.squid]),
            FestivalCheck.squidfest_day_1_iron: self.logic.fishing.can_catch_fish(self.content.fishes[Fish.squid]) & self.logic.has(Fishing.bait),
            FestivalCheck.squidfest_day_1_gold: self.logic.fishing.can_catch_fish(self.content.fishes[Fish.squid]) & self.logic.has(Fishing.deluxe_bait),
            FestivalCheck.squidfest_day_1_iridium: self.logic.festival.can_squidfest_day_1_iridium_reward(),
            FestivalCheck.squidfest_day_2_copper: self.logic.fishing.can_catch_fish(self.content.fishes[Fish.squid]),
            FestivalCheck.squidfest_day_2_iron: self.logic.fishing.can_catch_fish(self.content.fishes[Fish.squid]) & self.logic.has(Fishing.bait),
            FestivalCheck.squidfest_day_2_gold: self.logic.fishing.can_catch_fish(self.content.fishes[Fish.squid]) & self.logic.has(Fishing.deluxe_bait),
            FestivalCheck.squidfest_day_2_iridium: self.logic.fishing.can_catch_fish(self.content.fishes[Fish.squid]) &
                                                   self.logic.fishing.has_specific_bait(self.content.fishes[Fish.squid]),
        })
        for i in range(1, 11):
            check_name = f"{FestivalCheck.trout_derby_reward_pattern}{i}"
            self.registry.festival_rules[check_name] = self.logic.fishing.can_catch_fish(self.content.fishes[Fish.rainbow_trout])

    def can_squidfest_day_1_iridium_reward(self) -> StardewRule:
        return self.logic.fishing.can_catch_fish(self.content.fishes[Fish.squid]) & self.logic.fishing.has_specific_bait(self.content.fishes[Fish.squid])

    def has_squidfest_day_1_iridium_reward(self) -> StardewRule:
        if self.options.festival_locations == FestivalLocations.option_disabled:
            return self.logic.festival.can_squidfest_day_1_iridium_reward()
        else:
            return self.logic.received(f"Book: {Book.the_art_o_crabbing}")

    def can_win_egg_hunt(self) -> StardewRule:
        return self.logic.true_

    def can_succeed_luau_soup(self) -> StardewRule:
        if self.options.festival_locations != FestivalLocations.option_hard:
            return self.logic.true_
        eligible_fish = (Fish.blobfish, Fish.crimsonfish, Fish.ice_pip, Fish.lava_eel, Fish.legend, Fish.angler, Fish.catfish, Fish.glacierfish,
                         Fish.mutant_carp, Fish.spookfish, Fish.stingray, Fish.sturgeon, Fish.super_cucumber)
        fish_rule = self.logic.has_any(*(f for f in eligible_fish if f in self.content.fishes))  # To filter stingray
        eligible_kegables = (Fruit.ancient_fruit, Fruit.apple, Fruit.banana, Forageable.coconut, Forageable.crystal_fruit, Fruit.mango, Fruit.melon,
                             Fruit.orange, Fruit.peach, Fruit.pineapple, Fruit.pomegranate, Fruit.rhubarb, Fruit.starfruit, Fruit.strawberry,
                             Forageable.cactus_fruit, Fruit.cherry, Fruit.cranberries, Fruit.grape, Forageable.spice_berry, Forageable.wild_plum,
                             Vegetable.hops, Vegetable.wheat)
        keg_rules = [self.logic.artisan.can_keg(kegable) for kegable in eligible_kegables if kegable in self.content.game_items]
        aged_rule = self.logic.has(Machine.cask) & self.logic.or_(*keg_rules)
        # There are a few other valid items, but I don't feel like coding them all
        return fish_rule | aged_rule

    def can_succeed_grange_display(self) -> StardewRule:
        if self.options.festival_locations != FestivalLocations.option_hard:
            return self.logic.true_

        # Other animal products are not counted in the animal product category
        good_animal_products = [
            AnimalProduct.duck_egg, AnimalProduct.duck_feather, AnimalProduct.egg, AnimalProduct.goat_milk, AnimalProduct.golden_egg, AnimalProduct.large_egg,
            AnimalProduct.large_goat_milk, AnimalProduct.large_milk, AnimalProduct.milk, AnimalProduct.ostrich_egg, AnimalProduct.rabbit_foot,
            AnimalProduct.void_egg, AnimalProduct.wool
        ]
        if AnimalProduct.ostrich_egg not in self.content.game_items:
            # When ginger island is excluded, ostrich egg is not available
            good_animal_products.remove(AnimalProduct.ostrich_egg)
        animal_rule = self.logic.has_any(*good_animal_products)

        artisan_rule = self.logic.artisan.can_keg(Generic.any) | self.logic.artisan.can_preserves_jar(Generic.any)

        # Salads at the bar are good enough
        cooking_rule = self.logic.money.can_spend_at(Region.saloon, 220)

        fish_rule = self.logic.fishing.can_fish_anywhere(50)

        # Hazelnut always available since the grange display is in fall
        forage_rule = self.logic.region.can_reach_any((Region.forest, Region.backwoods))

        # More than half the minerals are good enough
        mineral_rule = self.logic.action.can_open_geode(Generic.any)

        good_fruits = (fruit
                       for fruit in
                       (Fruit.apple, Fruit.banana, Forageable.coconut, Forageable.crystal_fruit, Fruit.mango, Fruit.orange, Fruit.peach, Fruit.pomegranate,
                        Fruit.strawberry, Fruit.melon, Fruit.rhubarb, Fruit.pineapple, Fruit.ancient_fruit, Fruit.starfruit)
                       if fruit in self.content.game_items)
        fruit_rule = self.logic.has_any(*good_fruits)

        good_vegetables = (vegeteable
                           for vegeteable in
                           (Vegetable.amaranth, Vegetable.artichoke, Vegetable.beet, Vegetable.cauliflower, Forageable.fiddlehead_fern, Vegetable.kale,
                            Vegetable.radish, Vegetable.taro_root, Vegetable.yam, Vegetable.red_cabbage, Vegetable.pumpkin)
                           if vegeteable in self.content.game_items)
        vegetable_rule = self.logic.has_any(*good_vegetables)

        return animal_rule & artisan_rule & cooking_rule & fish_rule & forage_rule & fruit_rule & mineral_rule & vegetable_rule

    def can_win_fishing_competition(self) -> StardewRule:
        return self.logic.fishing.can_fish(60)

    def has_all_rarecrows(self) -> StardewRule:
        rules = []
        for rarecrow_number in range(1, 9):
            rules.append(self.logic.received(f"Rarecrow #{rarecrow_number}"))
        return self.logic.and_(*rules)
