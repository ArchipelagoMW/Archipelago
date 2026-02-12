from __future__ import annotations

import collections
import logging
import random
import typing

from .FactorioModpack import FactorioModpack
from .APModpackManager import get_items, get_locations, items_to_id, get_item_groups, get_location_groups, modpacks
import Utils
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification, CollectionState
from NetUtils import JSONMessagePart
from Options import OptionError
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch as launch_component
from worlds.generic import Rules
from .Mod import generate_mod
from .FactorioOptions import (FactorioOptions, Silo, Satellite, TechTreeInformation, Goal,
                              TechCostDistribution, option_groups)
from .FactorioRules import RecipeRule, InternalItemRule, TechRule, AndRule, OrRule, process_yaml_rule
from .RandomGameItems import RandomGameItems
from .RecipeEngine import GameRecipe, GameItem, DefinitionSource, TechCatalyst, Category, OneItemCatalyst
from .Shapes import get_shapes
from .FactorioSettings import FactorioSettings
from .Technologies import Technology

modpacks: dict[str, FactorioModpack]

def launch_client(*args: str):
    from .Client import launch
    launch_component(launch, name="Factorio Bob's Client", args=args)


components.append(Component("FactorioBobs Client", func=launch_client, component_type=Type.CLIENT))


class FactorioBobsWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Factorio software on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Berserker, Farrak Kilhn"]
    )]
    option_groups = option_groups


class FactorioItem(Item):
    game = "Factorio Bob's"


class FactorioBobs(World):
    """
    Factorio is a game about automation. You play as an engineer who has crash landed on the planet
    Nauvis, an inhospitable world filled with dangerous creatures called biters. Build a factory,
    research new technologies, and become more efficient in your quest to build a rocket and return home.
    """
    SLOT_RANDOM_SEED_KEY = "seeded_random_seed"
    SLOT_RANDOM_RECIPES_KEY = "recipes"
    SLOT_LOCATION_COUNT_KEY = "location_count"
    SLOT_OPTIONS_KEY = "options"

    logger: logging.Logger

    game = "Factorio Bob's"
    location_pool: list[FactorioScienceLocation]

    item_name_to_id = get_items()
    location_name_to_id = get_locations()
    item_name_groups = get_item_groups()
    location_name_groups = get_location_groups()

    web = FactorioBobsWeb()
    options_dataclass = FactorioOptions
    options: FactorioOptions

    required_client_version = (0, 6, 0)
    if Utils.version_tuple < required_client_version:
        raise Exception(f"Update Archipelago to use this world ({game}).")
    tech_tree_layout_prerequisites: typing.Dict[FactorioScienceLocation, typing.Set[FactorioScienceLocation]]
    skip_silo: bool = False
    origin_region_name = "Nauvis"
    science_locations: typing.List[FactorioScienceLocation]
    removed_technologies: typing.Set[str]
    settings: typing.ClassVar[FactorioSettings]
    trap_names: tuple[str] = ("Evolution", "Attack", "Teleport", "Grenade", "Cluster Grenade", "Artillery",
                              "Atomic Rocket", "Atomic Cliff Remover", "Inventory Spill")
    want_progressives: dict[str, bool] = collections.defaultdict(lambda: False)

    seeded_random_seed: int
    seeded_random: random.Random

    modpack: FactorioModpack

    def __init__(self, world, player: int):
        super(FactorioBobs, self).__init__(world, player)
        self.additional_logic: dict[int, AndRule] = {}
        self.progression_technologies: set[Technology] = set()
        self.custom_recipes : typing.Dict[str, GameRecipe] = {}
        self.custom_products: dict[str, GameItem] = {}
        self.science_locations = []
        self.tech_tree_layout_prerequisites = {}
        self.modpack: FactorioModpack | None = None
        self.removed_technologies: set[str] = set()

        self.logger = logging.getLogger(f"{self.game}:{self.player}")

        self.set_seeded_random_seed(self.random.getrandbits(64))

    def set_seeded_random_seed(self, seed: int):
        self.seeded_random_seed = seed
        self.seeded_random = random.Random(self.seeded_random_seed)

    def get_allowed_packs(self) -> set[str]:
        return set(self.modpack.ordered_science_packs[:self.options.number_of_science_packs.value])

    generate_output = generate_mod

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, typing.Any]) -> dict[str, typing.Any]:
        if FactorioBobs.SLOT_RANDOM_RECIPES_KEY not in slot_data:
            temp_slot_data = {FactorioBobs.SLOT_RANDOM_RECIPES_KEY: {}}
            for key, value in slot_data.items():
                if key in FactorioBobs.SLOT_RANDOM_SEED_KEY:
                    temp_slot_data[FactorioBobs.SLOT_RANDOM_SEED_KEY] = value
                    continue
                temp_slot_data[FactorioBobs.SLOT_RANDOM_RECIPES_KEY][key] = value
            slot_data = temp_slot_data
        return slot_data

    # and this is how we tell Universal Tracker we don't need the yaml
    ut_can_gen_without_yaml = True

    def generate_early(self) -> None:
        modpack_name = self.options.packname.current_key
        if modpack_name not in modpacks:
            raise Exception(f"Modpack name '{modpack_name}' not found.")
        self.modpack = modpacks[modpack_name]
        self.modpack.init_pack_check()

        self.removed_technologies = self.modpack.removed_technologies.copy()
        self.options.number_of_science_packs.value = min(len(self.modpack.ordered_science_packs), self.options.number_of_science_packs.value)

        # if max < min, then swap max and min
        if self.options.max_tech_cost < self.options.min_tech_cost:
            self.options.min_tech_cost.value, self.options.max_tech_cost.value = \
                self.options.max_tech_cost.value, self.options.min_tech_cost.value
        self.skip_silo = self.options.silo.value == Silo.option_spawn
        self.want_progressives = collections.defaultdict(
            lambda: self.options.progressive.want_progressives(self.random))

        if not hasattr(self.multiworld, "generation_is_fake"):
            self.set_custom_recipes()
        elif hasattr(self.multiworld, "re_gen_passthrough") and self.game in self.multiworld.re_gen_passthrough:
            slot_data = self.multiworld.re_gen_passthrough[self.game]
            self.logger.error(f"SLOT_DATA: {slot_data}")
            if FactorioBobs.SLOT_RANDOM_SEED_KEY in slot_data:
                self.set_seeded_random_seed(slot_data[FactorioBobs.SLOT_RANDOM_SEED_KEY])
            slot_recipes = slot_data[FactorioBobs.SLOT_RANDOM_RECIPES_KEY]
            for product_name, ingredients_name in slot_recipes.items():
                new_ingredients = {}
                liquids_used = 0
                for ingredient_name in ingredients_name:
                    ingredient = self.modpack.recipe_engine.get_game_item(ingredient_name)
                    if ingredient.is_fluid:
                        liquids_used += 1
                    new_ingredients[ingredient] = 1

                custom_products = {}
                if product_name not in self.custom_products:
                    self.custom_products[product_name] = GameItem(self.modpack.recipe_engine, product_name,
                                                                  DefinitionSource.WORLD)
                custom_products[self.custom_products[product_name]] = 1
                self.custom_recipes[product_name] = GameRecipe(self.modpack.recipe_engine, product_name,
                                                               DefinitionSource.WORLD, self.get_category(new_ingredients),
                                                               new_ingredients, custom_products,
                                                               1)
                self.custom_products[product_name].crafted_by.add(self.custom_recipes[product_name])
                # print(f"{[x for x in self.custom_recipes[product_name].products]}: {[x for x in self.custom_recipes[product_name].ingredients]}")
            self.options.additional_logic.value = self.options.additional_logic.option_none
            slot_options = slot_data[FactorioBobs.SLOT_OPTIONS_KEY]
            self.options.tech_cost_mix.value = slot_options[self.options.tech_cost_mix.display_name]
            self.options.number_of_science_packs.value = slot_options[self.options.number_of_science_packs.display_name]

        if self.options.additional_logic.value == self.options.additional_logic.option_none:
            self.additional_logic = {}
        elif self.options.additional_logic.value == self.options.additional_logic.option_default:
            self.additional_logic = {complexity:
                                        process_yaml_rule(yaml_rule, self.modpack)
                                     for complexity, yaml_rule in self.modpack.default_options["additional_logic"].items()}
        elif self.options.additional_logic.value == self.options.additional_logic.option_custom:
            self.additional_logic = {complexity:
                                        process_yaml_rule(yaml_rule, self.modpack)
                                     for complexity, yaml_rule in self.options.custom_additional_logic.value.items()}
        else:
            raise OptionError("additional_logic is invalid type")


        for complexity, rule in self.additional_logic.items():
            if complexity <= self.options.number_of_science_packs.value:
                for tech in rule.needed_items():
                    self.progression_technologies.add(self.modpack.technology_table[tech])

        # handle marking progressive techs as advancement
        prog_add = set()
        for tech in self.progression_technologies:
            if tech.name in self.modpack.tech_to_progressive_lookup:
                prog_add.add(self.modpack.technology_table[self.modpack.tech_to_progressive_lookup[tech.name]])
        self.progression_technologies |= prog_add

    def create_regions(self):
        player = self.player
        nauvis = Region(self.origin_region_name, player, self.multiworld)

        location_count = len(self.modpack.base_technology_table) - len(self.modpack.removed_technologies) - self.skip_silo

        for name in self.trap_names:
            name = name.replace(" ", "_").lower()+"_traps"
            location_count += getattr(self.options, name)

        location_pool = []

        for pack in range(self.options.number_of_science_packs.value):
            location_pool.extend(self.modpack.location_pools[pack])

        if (hasattr(self.multiworld, "re_gen_passthrough") # if regen and have location count
                and FactorioBobs.SLOT_LOCATION_COUNT_KEY in self.multiworld.re_gen_passthrough[self.game]):
            location_count = self.multiworld.re_gen_passthrough[self.game][FactorioBobs.SLOT_LOCATION_COUNT_KEY]

        if (hasattr(self.multiworld, "re_gen_passthrough")  # if regen and doesn't have seed then fallback
                and FactorioBobs.SLOT_RANDOM_SEED_KEY not in self.multiworld.re_gen_passthrough[self.game]):
            print("No random seed in slot_data, falling back to old behavior be careful around science pack skips")
            self.options.tech_cost_mix.value = 100
            location_names = location_pool
        else: # normal gen
            try:
                location_names = self.seeded_random.sample(location_pool, location_count)
            except ValueError as e:
                # should be "ValueError: Sample larger than population or is negative"
                raise Exception("Too many traps for too few locations. Either decrease the trap count, "
                                f"or increase the location count (higher max science pack). (Player {self.player})") from e

        self.science_locations = [FactorioScienceLocation(player, loc_name, self.location_name_to_id[loc_name], nauvis, self.modpack)
                                  for loc_name in location_names]
        distribution: TechCostDistribution = self.options.tech_cost_distribution
        min_cost = self.options.min_tech_cost.value
        max_cost = self.options.max_tech_cost.value
        if distribution == distribution.option_even:
            rand_values = (self.seeded_random.randint(min_cost, max_cost) for _ in self.science_locations)
        else:
            mode = {distribution.option_low: min_cost,
                    distribution.option_middle: (min_cost+max_cost)//2,
                    distribution.option_high: max_cost}[distribution.value]
            rand_values = (self.seeded_random.triangular(min_cost, max_cost, mode) for _ in self.science_locations)
        rand_values = sorted(rand_values)
        if self.options.ramping_tech_costs:
            def sorter(loc: FactorioScienceLocation):
                return loc.complexity, loc.rel_cost
        else:
            def sorter(loc: FactorioScienceLocation):
                return loc.rel_cost
        for i, location in enumerate(sorted(self.science_locations, key=sorter)):
            location.count = rand_values[i]
        del rand_values
        nauvis.locations.extend(self.science_locations)
        location = FactorioLocation(player, "Rocket Launch", None, nauvis)
        nauvis.locations.append(location)
        event = FactorioItem("Victory", ItemClassification.progression, None, player)
        location.place_locked_item(event)

        for ingredient in sorted(self.get_allowed_packs()):
            location = FactorioLocation(player, f"Automate {ingredient}", None, nauvis)
            nauvis.locations.append(location)
            event = FactorioItem(f"Automated {ingredient}", ItemClassification.progression, None, player)
            location.place_locked_item(event)

        self.multiworld.regions.append(nauvis)

    def create_items(self) -> None:
        self.custom_technologies = self.set_custom_technologies()
        for trap_name in self.trap_names:
            self.multiworld.itempool.extend(self.create_item(f"{trap_name} Trap") for _ in
                                            range(getattr(self.options,
                                                          f"{trap_name.lower().replace(' ', '_')}_traps")))

        cost_sorted_locations = sorted(self.science_locations, key=lambda location: (location.complexity, location.rel_cost))
        special_index = self.modpack.forced_locations
        loc: FactorioScienceLocation
        if self.options.tech_tree_information == TechTreeInformation.option_full:
            # mark all locations as pre-hinted
            for loc in self.science_locations:
                loc.revealed = True
        if self.skip_silo:
            self.removed_technologies |= {"rocket-silo"}
        for tech_name in self.modpack.base_technology_table.keys():
            if tech_name not in self.removed_technologies:
                progressive_item_name = self.modpack.tech_to_progressive_lookup.get(tech_name, tech_name)
                want_progressive = self.want_progressives[progressive_item_name]
                item_name = progressive_item_name if want_progressive else tech_name
                tech_item = self.create_item(item_name)
                index = special_index.get(tech_name, None)
                if index is None:
                    self.multiworld.itempool.append(tech_item)
                else:
                    loc = cost_sorted_locations[index]
                    if index >= 0:
                        # beginning techs - limit cost to 10
                        # as automation is not achievable yet and hand-crafting for hours is not fun gameplay
                        loc.count = min(loc.count, 10)
                    loc.place_locked_item(tech_item)
                    loc.revealed = True

    def get_filler_item_name(self) -> str:
        tech_name: str = self.random.choice(tuple(self.modpack.technology_table.keys()))
        progressive_item_name: str = self.modpack.tech_to_progressive_lookup.get(tech_name, tech_name)
        want_progressive: bool = self.want_progressives[progressive_item_name]
        return progressive_item_name if want_progressive else tech_name

    def set_rules(self):
        player = self.player
        shapes = get_shapes(self)

        science_packs = self.modpack.ordered_science_packs[:self.options.number_of_science_packs]
        for complexity, science_pack in enumerate(science_packs, start=1):
            if science_pack == "automation-science-pack":
                continue
            location = self.get_location(f"Automate {science_pack}")
            optimized_rule = self.get_science_pack_rule(complexity)
            Rules.set_rule(location, lambda state, location_rule = optimized_rule: location_rule.eval(self, state))

        for location in self.science_locations:
            Rules.set_rule(location, lambda state: True)
            for ingredient_name in location.ingredients:
                Rules.add_rule(location, lambda state, lambda_ingredient=ingredient_name: state.has(f"Automated {lambda_ingredient}", player))
            # Rules.set_rule(location, lambda state, ingredients=frozenset(location.ingredients):
            #     all(state.has(f"Automated {ingredient}", player) for ingredient in ingredients))
            prerequisites = shapes.get(location)
            if prerequisites:
                Rules.add_rule(location, lambda state, locations=frozenset(prerequisites):
                    all(state.can_reach(loc) for loc in locations))

        victory_tech: set[Technology] = set()
        if self.options.silo != Silo.option_spawn:
            victory_tech |= self.get_item_tech_req("rocket-silo")
            victory_tech |= self.get_item_tech_req("cargo-landing-pad")
        victory_tech |= self.get_item_tech_req("rocket-part")
        if self.options.goal == Goal.option_satellite:
            victory_tech |= self.get_item_tech_req("satellite")
        victory_tech_names = set(tech.name for tech in victory_tech)
        if self.options.silo == Silo.option_spawn:
            victory_tech_names -= {"rocket-silo"}
        else:
            victory_tech_names |= {"rocket-silo"}
        self.get_location("Rocket Launch").access_rule = lambda state: all(state.has(technology, player)
                                                                           for technology in
                                                                           victory_tech_names)
        self.multiworld.completion_condition[player] = lambda state: state.has('Victory', player)

    def get_science_pack_rule(self, complexity: int) -> FactorioRules.Rule:
        science_pack = self.modpack.ordered_science_packs[complexity-1]
        science_pack_item: GameItem = self.get_internal_item(science_pack)
        if complexity in self.additional_logic:
            rule = AndRule(InternalItemRule(science_pack_item), self.additional_logic[complexity])
        else:
            rule = InternalItemRule(science_pack_item)
        return rule.optimize()

    def get_internal_item(self, name: str) -> GameItem:
        return self.custom_products[name] if name in self.custom_products \
            else self.modpack.recipe_engine.get_game_item(name)

    def get_item_tech_req(self, item_name: str) -> set[Technology]: # todo this is temp replace this with bootstrap
        if item_name not in self.custom_recipes:
            item = self.modpack.recipe_engine.get_game_item(item_name)
            if not item.has_calculated_raw:
                raise RuntimeError(f"Item {item_name} has no calculated raw data, run GenPrecalc on pack")
            return item.get_req_techs()
        recipe = self.custom_recipes[item_name]
        req = set()
        for item in recipe.ingredients:
            if not item.has_calculated_raw:
                raise RuntimeError(f"Item {item_name} has no calculated raw data, run GenPrecalc on pack")
            req |= item.get_req_techs()

        for catalyst in recipe.technologies:
            req.add(catalyst.tech)

        ordered_machines = sorted(recipe.category.machines, key=lambda m: m.score)
        for machine in ordered_machines:
            if machine.is_valid:
                req |= machine.get_req_techs()
                break

        for catalyst in recipe.needed_items:
            item = catalyst.item
            if item.is_valid:
                req |= item.get_req_techs()
                break
            else:
                raise RuntimeError(f"Item {item_name} is invalid")
        return req

    def generate_basic(self):
        start_location_hints: typing.Set[str] = self.options.start_location_hints.value

        for loc in self.science_locations:
            # show start_location_hints ingame
            if loc.name in start_location_hints:
                loc.revealed = True
            # make spoiler match mod info
            elif loc.revealed:
                start_location_hints.add(loc.name)

    def collect_item(self, state, item, remove=False):
        if item.advancement and item.name in self.modpack.progressive_technology_table:
            prog_table = self.modpack.progressive_technology_table[item.name].progressive
            if remove:
                for item_name in reversed(prog_table):
                    if state.has(item_name, item.player):
                        return item_name
            else:
                for item_name in prog_table:
                    if not state.has(item_name, item.player):
                        return item_name

        return super(FactorioBobs, self).collect_item(state, item, remove)

    @classmethod
    def stage_write_spoiler(cls, world, spoiler_handle):
        factorio_players = world.get_game_players(cls.game)
        spoiler_handle.write('\n\nFactorioBobs Recipes:\n')
        for player in factorio_players:
            name = world.get_player_name(player)
            for recipe in world.worlds[player].custom_recipes.values():
                spoiler_handle.write(f"\n{recipe.name} ({name}): {recipe.ingredients} -> {recipe.products}")

    @staticmethod
    def get_category(ingredients: typing.Iterable[GameItem], preferred="crafting") -> str: # todo extract number of fluid input for categories
        num_liquids = sum(1 for ingredient in ingredients if ingredient.is_fluid)
        categories = {0: preferred,
                      1: "crafting-with-fluid",
                      2: "chemistry"}
        return categories[num_liquids]

    def make_custom_recipe(self, name:str, products: dict[GameItem, int], ingredients_num: int, energy: int,
                           pool: RandomGameItems, pool_index: int, allow_liquids: int = 2, category = "crafting")-> GameRecipe:
        # assert len(pool) >= ingredients_num, f"Can't pick {ingredients_num} many items from pool {pool}."
        new_ingredients = {}
        liquids_used = 0
        bad_items: list[GameItem] = []
        if self.options.no_earlier_pools.value:
            get_item = lambda: pool.pop_item_from_pool(pool_index)
        else:
            get_item = lambda: pool.pop_item_from_pool(0, pool_index)

        for _ in range(ingredients_num):
            new_ingredient = get_item()
            while liquids_used == allow_liquids and new_ingredient.is_fluid:
                # liquids already at max for current recipe.
                # Return the liquid to the pool and get a new lambda_ingredient.
                bad_items.append(new_ingredient)
                new_ingredient: GameItem = get_item()
            if new_ingredient.is_fluid:
                liquids_used += 1
            new_ingredients[new_ingredient] = 1

        custom_products = {}
        for product, amount in products.items():
            if product.name not in self.custom_products:
                self.custom_products[product.name] = GameItem(self.modpack.recipe_engine, product.name,
                                                              DefinitionSource.WORLD, product.is_fluid)
            custom_products[self.custom_products[product.name]] = amount
        recipe = GameRecipe(self.modpack.recipe_engine, name, DefinitionSource.WORLD,
                            self.get_category(new_ingredients, category), new_ingredients,
                      custom_products, energy)
        return recipe

    def make_balanced_recipe(self, original: GameRecipe, pool: RandomGameItems, pool_index = -1, factor: float = 1,
                             allow_liquids: int = 2, ingredients_offset: int = 0) -> GameRecipe:
        """Generate a recipe from pool with time and cost similar to original * factor"""
        new_ingredients = {}
        target_energy = int(sum(ingredient.score * count for ingredient, count in original.ingredients.items()) * factor)
        target_num_ingredients = len(original.ingredients) + ingredients_offset
        remaining_energy = target_energy
        remaining_num_ingredients = target_num_ingredients
        bad_items: list[GameItem] = []
        liquids_used = 0
        if self.options.no_earlier_pools.value:
            get_item = lambda: pool.pop_item_from_pool(pool_index)
        else:
            get_item = lambda: pool.pop_item_from_pool(0, pool_index)

        # fill all but one slot with random ingredients, last with a good match
        while remaining_num_ingredients > 0:
            ingredient = get_item()
            if not ingredient.is_valid_pool:
                continue
            assert ingredient.has_calculated_raw, f"{ingredient}: Calculated raw not available"
            if liquids_used == allow_liquids and ingredient.is_fluid:
                continue  # can't use this ingredient as we already have maximum liquid in our recipe.
            ingredient_energy = ingredient.score
            if remaining_num_ingredients == 1:
                max_energy = 1.1 * remaining_energy
                min_energy = 0.9 * remaining_energy
            else:
                max_energy = remaining_energy * 0.75
                min_energy = (remaining_energy - max_energy) / remaining_num_ingredients
            min_num_energy = min_energy / ingredient_energy
            max_num_energy = max_energy / ingredient_energy
            min_num = int(max(1, min_num_energy))
            max_num = int(min(1000, max_num_energy))
            if min_num > max_num:
                bad_items.append(ingredient)
                continue  # can't use that ingredient
            num = self.random.randint(min_num, max_num)
            new_ingredients[ingredient] = num
            remaining_energy -= num * ingredient_energy
            remaining_num_ingredients -= 1
            if ingredient.is_fluid:
                liquids_used += 1

        # fill failed slots with whatever we got
        pool.return_items(bad_items)
        bad_items = []
        while remaining_num_ingredients > 0 and pool:
            ingredient: GameItem = get_item()
            if not ingredient.is_valid_pool:
                continue
            if not ingredient.has_calculated_raw:
                raise RuntimeError(f"{ingredient}: Calculated raw not available")
            if liquids_used == allow_liquids and ingredient.is_fluid:
                bad_items.append(ingredient)
                continue  # can't use this lambda_ingredient as we already have maximum liquid in our recipe.

            ingredient_energy = ingredient.score
            num_energy = remaining_energy / ingredient_energy / remaining_num_ingredients
            num = int(num_energy)
            if num < 1:
                bad_items.append(ingredient)
                continue

            new_ingredients[ingredient] = num
            remaining_energy -= num * ingredient_energy
            remaining_num_ingredients -= 1
            if ingredient.is_fluid:
                liquids_used += 1


        if remaining_num_ingredients > 1:
            self.logger.warning("could not randomize recipe")

        pool.return_items(bad_items)

        custom_products = {}
        for product, amount in original.products.items():
            if product.name not in self.custom_products:
                self.custom_products[product.name] = GameItem(self.modpack.recipe_engine, product.name,
                                                              DefinitionSource.WORLD, product.is_fluid)
            custom_products[self.custom_products[product.name]] = amount

        recipe = GameRecipe(self.modpack.recipe_engine, original.name, DefinitionSource.WORLD,
                            self.get_category(new_ingredients, original.category.name), new_ingredients,
                      custom_products, original.energy)
        return recipe

    def set_custom_technologies(self):
        custom_technologies = {}
        allowed_packs = self.get_allowed_packs()
        for technology_name, technology in self.modpack.base_technology_table.items():
            custom_technologies[technology_name] = technology.get_custom(self, allowed_packs, self.player)
        return custom_technologies

    def set_custom_recipes(self):
        # for name, item in all_ingredients.items():
        #     print(f"{name}: {item.get_raw_ingredients()}")
        ingredients_offset = self.options.recipe_ingredients_offset

        pools = RandomGameItems(self)

        for index, pack in enumerate(self.modpack.ordered_science_packs[:self.options.number_of_science_packs.value]):
            if self.options.recipe_ingredients or not self.modpack.recipe_engine.get_game_item(pack).best_recipes:
                pack_item = self.modpack.recipe_engine.get_game_item(pack)
                return_amount = index//2 + 1
                new_recipe = self.make_custom_recipe(pack, {pack_item: return_amount},
                                                     index//2 + 2 + ingredients_offset.value,
                                                     return_amount*5, pools, index)
                new_recipe.productivity = True
                self.custom_recipes[pack] = new_recipe

        original_rocket_part = self.modpack.recipe_engine.recipes["rocket-part"]
        custom_rocket_part = GameItem(self.modpack.recipe_engine, "rocket-part", DefinitionSource.WORLD, False)
        self.custom_products[custom_rocket_part.name] = custom_rocket_part
        self.custom_recipes["rocket-part"] = GameRecipe(self.modpack.recipe_engine, "rocket-part", DefinitionSource.WORLD,
                                                        original_rocket_part.category,
                                                     {pools.pop_item_from_pool(-1): 10 for _ in range(3 + ingredients_offset)},
                                                     {custom_rocket_part: 1},
                                                     original_rocket_part.energy)
        self.custom_recipes["rocket-part"].productivity = True

        if self.options.silo.value == Silo.option_randomize_recipe:
            old_recipe = self.modpack.recipe_engine.recipes["rocket-silo"]
            new_recipe = self.make_balanced_recipe(
                old_recipe, pools, -1,
                factor=self.options.number_of_science_packs.value / len(self.modpack.ordered_science_packs),
                ingredients_offset=ingredients_offset.value)
            self.custom_recipes["rocket-silo"] = new_recipe

        if self.options.satellite.value == Satellite.option_randomize_recipe:
            old_recipe = self.modpack.recipe_engine.recipes["satellite"]
            new_recipe = self.make_balanced_recipe(
                old_recipe, pools, -1,
                factor=self.options.number_of_science_packs.value / len(self.modpack.ordered_science_packs),
                ingredients_offset=ingredients_offset.value)
            self.custom_recipes["satellite"] = new_recipe

        bridge = GameItem(self.modpack.recipe_engine, "ap-energy-bridge", DefinitionSource.WORLD, False)
        self.custom_products["ap-energy-bridge"] = bridge
        new_recipe = self.make_custom_recipe(bridge.name, {bridge: 1}, 6+ingredients_offset.value, 10,
            pools, 0)
        for ingredient_name in new_recipe.ingredients:
            new_recipe.ingredients[ingredient_name] = self.random.randint(50, 500)
        self.custom_recipes[bridge.name] = new_recipe

        needed_items = {self.get_internal_item(pack) for pack in self.get_allowed_packs()}
        needed_items.add(self.custom_products["rocket-part"])
        if self.options.silo != Silo.option_spawn:
            needed_items.add(self.get_internal_item("rocket-silo"))
            needed_items.add(self.get_internal_item("cargo-landing-pad"))
        if self.options.goal.value == Goal.option_satellite:
            needed_items.add(self.get_internal_item("satellite"))

        for item in needed_items:
            self.progression_technologies |= self.get_item_tech_req(item.name)


    def create_item(self, name: str) -> FactorioItem:
        if not self.modpack:
            return FactorioItem(name,
                                ItemClassification.filler,
                                items_to_id[name], self.player)

        if name in self.modpack.technology_table.keys():  # is a Technology
            if self.modpack.technology_table[name] in self.progression_technologies:
                classification = ItemClassification.progression
            else:
                classification = ItemClassification.filler
            return FactorioItem(name,
                                classification,
                                items_to_id[name], self.player)

        item = FactorioItem(name,
                            ItemClassification.trap if name.endswith("Trap") else ItemClassification.filler,
                            items_to_id[name], self.player)
        return item

    def fill_slot_data(self):
        slot_data: dict[str, typing.Any] = {FactorioBobs.SLOT_RANDOM_SEED_KEY: self.seeded_random_seed,
                                            FactorioBobs.SLOT_LOCATION_COUNT_KEY: len(self.science_locations),
                                            FactorioBobs.SLOT_OPTIONS_KEY: {
                                            self.options.tech_cost_mix.display_name: self.options.tech_cost_mix.value,
                                            self.options.number_of_science_packs.display_name: self.options.number_of_science_packs.value,
                                            },
                                            FactorioBobs.SLOT_RANDOM_RECIPES_KEY: {}}
        for recipe in self.custom_recipes.values():
            ingredients = []
            for ingredient in recipe.ingredients:
                ingredients.append(ingredient.name)
            slot_data[FactorioBobs.SLOT_RANDOM_RECIPES_KEY][recipe.name] = ingredients
        return slot_data

    def explain_more(self, argument: str, state: CollectionState) -> list[JSONMessagePart]:
        split_arg = argument.split("-")
        if len(split_arg) == 2:
            complexity = int(split_arg[1])
            science_pack_name = self.modpack.ordered_science_packs[complexity]
            rule = self.get_science_pack_rule(complexity)
            needed_items = {item for item in rule.needed_items() if not state.has(item, self.player)}
            ingredients = self.get_internal_item(science_pack_name).best_recipe.ingredients # todo fix
            return [{"text": f"pack name: {science_pack_name}\n"},
                    {"text": f"ingredients: {ingredients}\n"},
                    {"text": f"needed items: {needed_items}\n"}]
        elif len(split_arg) == 3:
            # if FactorioBobs.SLOT_RANDOM_SEED_KEY not in self.multiworld.re_gen_passthrough[self.game]:
            #     return [{"text": "Unknown science pack requirements: game generated on old world\n"}] # todo enable check
            locations = {location.name: location for location in self.science_locations}
            if argument not in locations:
                return [{"text": "Unknown location\n"}] # todo add fuzzy
            packs_required = [(complexity, pack)
                              for complexity, pack in enumerate(self.modpack.ordered_science_packs)
                              if pack in locations[argument].ingredients]
            packs_needed = [(complexity, pack) for complexity, pack in packs_required
                            if not state.has(f"Automated {pack}", self.player)]
            return [{"text": f"science pack requirements: {packs_required}\n"},
                    {"text": f"science pack not craftable: {packs_needed}\n"}]
        else:
            return [{"text": "Invalid argument only input science pack/location\n"}]

class FactorioLocation(Location):
    game: str = FactorioBobs.game


class FactorioScienceLocation(FactorioLocation):
    complexity: int
    revealed: bool = False

    # Factorio technology properties:
    ingredients: typing.Dict[str, int]
    count: int = 0

    def __init__(self, player: int, name: str, address: int, parent: Region, modpack: FactorioModpack):
        super(FactorioScienceLocation, self).__init__(player, name, address, parent)
        # "AP-{Complexity}-{Cost}"
        split_name = self.name.split("-")
        self.complexity = int(split_name[1]) - 1
        self.rel_cost = int(split_name[2])

        self.ingredients = {modpack.ordered_science_packs[self.complexity]: 1}
        world: World = parent.multiworld.worlds[self.player]
        assert type(world) is FactorioBobs
        world: FactorioBobs
        for complexity in range(self.complexity):
            if (world.options.tech_cost_mix >
                    world.seeded_random.randint(0, 99)):
                self.ingredients[modpack.ordered_science_packs[complexity]] = 1

    @property
    def factorio_ingredients(self) -> typing.List[typing.Tuple[str, int]]:
        return [(name, count) for name, count in self.ingredients.items()]
