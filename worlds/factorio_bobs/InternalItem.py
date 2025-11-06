from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Technology

from concurrent.futures import ThreadPoolExecutor

from .FactorioUtils import FactorioElement, load_json_data

pool = ThreadPoolExecutor(1)

recipes_future = pool.submit(load_json_data, "recipes")
resources_future = pool.submit(load_json_data, "resources")
machines_future = pool.submit(load_json_data, "machines")
fluids_future = pool.submit(load_json_data, "fluids")
items_future = pool.submit(load_json_data, "items")

Category = str

def ingredient_score(ingredients: dict[InternalItem, float]):
    cost = 0

    for ingredient, amount in ingredients.items():
        cost += ingredient.get_score() * amount
    return cost

# step 1: find root (finding loops can be incorporated into this)
# step 2: find non-recursive ingredients
#

recipe_path: list[tuple[InternalItem, Recipe]] = []
failure_state = False
class InternalItem(FactorioElement):
    evaluating: set[InternalItem] = set()
    __req_categories: set[Category]
    def __init__(self, name: str, is_fluid: bool):
        self.name = name
        self.is_fluid = is_fluid
        self.recipes: set[Recipe] = set()
        self.is_used_in: set[Recipe] = set()

        self.best_recipe: Recipe | None = None
        self.root_item = False

        self.non_recursive_raw_ingredients: dict[InternalItem, float] = {}
        self.non_recursive_best_recipe: Recipe | None = None
        self.recursive_loops: set[RecursiveRecipeLoop] = set()
        self.has_recursive_recipe = False
        self.best_loop = None

        self.__raw_ingredients: dict[InternalItem, float] = {}
        self.__ingredient_unlocking_technologies: set[Technology] = set()
        self.__req_categories: set[Category] = set()

    def get_raw_ingredients(self) -> dict[InternalItem, float]:
        return self.eval()[0]

    def eval(self) -> tuple[dict[InternalItem, float], Recipe | None, set[Technology], set[Category]]:
        if (self.__raw_ingredients
                and not any(loop.entry and loop.get_recipe(self) == self.best_recipe for loop in self.recursive_loops)): #  and loop.get_recipe(self) == self.best_recipe
            return (self.__raw_ingredients, self.best_recipe,
                    self.__ingredient_unlocking_technologies, self.__req_categories)
        # no cache calculate

        if len(self.recipes) == 0:
            # must be an unknown method for item to spontaneously exist
            if self.name not in rel_cost:
                print(f"spontaneously existing item ({self.name}) doesn't have a cost, defaulting to 1")
            self.non_recursive_raw_ingredients = {self: 1}
            self.__raw_ingredients = {self: 1}
            return self.__raw_ingredients, None, set(), set()

        InternalItem.evaluating.add(self)
        for loop in self.recursive_loops:
            loop.enter_loop(self)

        if self.root_item:
            recipe_path.append((self, self.best_recipe))
            (self.__raw_ingredients, self.__ingredient_unlocking_technologies,
             self.__req_categories) = self.best_recipe.eval()
            recipe_path.pop()

            if not self.__raw_ingredients:
                self.__raw_ingredients = {self: 1}

            self.non_recursive_best_recipe = self.best_recipe
            self.non_recursive_raw_ingredients = self.__raw_ingredients
            InternalItem.evaluating.remove(self)
            return (self.__raw_ingredients, self.best_recipe,
                    self.__ingredient_unlocking_technologies, self.__req_categories)


        lowest_score = float('inf')
        best_recipe = None
        best_tech = set()
        best_categories = set()
        best_raw_ingredients = {}
        for recipe in self.recipes:
            recipe_path.append((self, recipe))
            raw_ingredients, tech, cat = recipe.eval()
            recipe_path.pop()

            if not raw_ingredients:
                continue

            recipe_score = ingredient_score(raw_ingredients) / recipe.products[self]
            if recipe_score < lowest_score:
                lowest_score = recipe_score
                best_recipe = recipe
                best_tech = tech
                best_categories = cat
                best_raw_ingredients = {ingredient: cost / recipe.products[self] for ingredient, cost in raw_ingredients.items()}

        for loop in self.recursive_loops:
            loop.exit_loop(self)

        if any(loop.entry for loop in self.recursive_loops):
            # in loop, calculation not valid for cache or recursive calculation
            InternalItem.evaluating.remove(self)
            return best_raw_ingredients, best_recipe, best_tech, best_categories

        if not best_raw_ingredients:
            # initial item must have unknown generation
            best_raw_ingredients = {self: 1}
            if self.name not in rel_cost:
                print(f"spontaneously existing sample item ({self.name}) doesn't have a cost, defaulting to 1")

        self.non_recursive_raw_ingredients = best_raw_ingredients
        self.non_recursive_best_recipe = best_recipe
        # todo non_recursive_tech

        if not self.recursive_loops or True: # todo fix recursion
            self.__raw_ingredients = best_raw_ingredients
            self.best_recipe = best_recipe
            self.__ingredient_unlocking_technologies = best_tech
            self.__req_categories = best_categories
            InternalItem.evaluating.remove(self)
            return (self.__raw_ingredients, self.best_recipe,
                    self.__ingredient_unlocking_technologies, self.__req_categories)

        # recursive calculate
        raise NotImplementedError("recursion takes too long and should be implemented yet. How did you get here?")
        # todo recursive tech handling & categories

        for loop in self.recursive_loops:
            loop.enter_loop(self)

        non_recursive_score = lowest_score
        best_loop = None
        for loop in self.recursive_loops:
            loop_ingredients = loop.get_cost(self)

            if loop_ingredients[self] >= 1: # costs more for the loop
                continue

            discount = loop_ingredients[self]
            del loop_ingredients[self]

            raw_loop_ingredients = {}
            for loop_ingredient, loop_amount in loop_ingredients.items():
                raw_ingredients = loop_ingredient.get_raw_ingredients()

                for ingredient, amount in raw_ingredients.items():
                    if ingredient in raw_loop_ingredients:
                        raw_loop_ingredients[ingredient] += amount * loop_amount
                    else:
                        raw_loop_ingredients[ingredient] = amount * loop_amount

            self.has_recursive_recipe = True

            recipe_score = ingredient_score(raw_loop_ingredients) + non_recursive_score * discount

            if recipe_score < lowest_score:
                lowest_score = recipe_score
                best_loop = loop
                best_raw_ingredients = raw_loop_ingredients
                for ingredient, amount in self.non_recursive_raw_ingredients.items():
                    if ingredient in best_raw_ingredients:
                        best_raw_ingredients[ingredient] += amount * discount
                    else:
                        best_raw_ingredients[ingredient] = amount * discount

        for loop in self.recursive_loops:
            loop.exit_loop(self)

        self.__raw_ingredients = best_raw_ingredients
        self.best_loop = best_loop
        if best_loop is None:
            self.best_recipe = best_recipe
        else:
            self.best_recipe = best_loop.get_recipe(self)

        InternalItem.evaluating.remove(self)
        return self.__raw_ingredients

    def get_score(self) -> float:
        if self.name in rel_cost:
            return rel_cost[self.name]
        raw_ingredients = self.get_raw_ingredients()
        if len(raw_ingredients) == 1 and self in raw_ingredients:
            return 1
        return ingredient_score(self.get_raw_ingredients())

    def all_unlocking_technologies(self) -> set[Technology]:
        if self in InternalItem.evaluating:
            return set()

        _,_,all_unlocking_technologies, categories = self.eval()
        all_unlocking_technologies = all_unlocking_technologies.copy()
        categories = categories.copy()

        for category in categories:
            all_unlocking_technologies |= machine_per_category[category].all_unlocking_technologies()

        return all_unlocking_technologies

    def invalidate_cache(self):
        self.__raw_ingredients = set()
        self.best_recipe = None
        self.__ingredient_unlocking_technologies = set()
        self.__req_categories = set()

    def set_cache(self, raw_ingredients: dict[InternalItem, float], best_recipe : Recipe | None,
                  ingredient_tech: set[Technology], req_categories: set[Category]):
        self.__raw_ingredients = raw_ingredients
        self.best_recipe = best_recipe
        self.__ingredient_unlocking_technologies = ingredient_tech
        self.__req_categories = req_categories


class RecursiveRecipeLoop:
    # entered_loops = 0
    existing_loops = set()

    def __init__(self, start) -> None:
        start_index = 0
        try:
            while recipe_path[start_index][0] != start:
                start_index += 1
        except IndexError:
            Exception(f"history: {recipe_path}, item: {start}, index: {start_index}")

        self.recipes: tuple[tuple[InternalItem, Recipe], ...] = tuple(recipe_path[start_index:])
        self.entry: InternalItem | None = start
        try:
            self.blocked: Recipe | None = self.recipes[0][1]
        except IndexError:
            Exception(f"history: {recipe_path}, item: {start}, index: {start_index}")
        # RecursiveRecipeLoop.entered_loops += 1

        # make the start of self.recipes stable for hash
        hashed_recipes = tuple(hash(recipe) for recipe in self.recipes)
        first_recipe = min(hashed_recipes)
        first_recipe_index = hashed_recipes.index(first_recipe)
        self.recipes = self.recipes[first_recipe_index:] + self.recipes[:first_recipe_index]

        if self in RecursiveRecipeLoop.existing_loops:
            return
        RecursiveRecipeLoop.existing_loops.add(self)
        if not len(RecursiveRecipeLoop.existing_loops) % 100:
            print(f"recursive loops: {len(RecursiveRecipeLoop.existing_loops)}\n"
                  f"loop: {self.recipes}")

        for item, _ in self.recipes:
            item.recursive_loops.add(self)

    def __hash__(self) -> int:
        return hash(self.recipes)

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)

    def enter_loop(self, item: InternalItem) -> bool:
        if self.entry:
            return False
        self.entry = item
        # RecursiveRecipeLoop.entered_loops += 1
        for index, (loop_item, _) in enumerate(self.recipes):
            if item == loop_item:
                self.blocked = self.recipes[index-1][1]
                # excluded_recipes.add(self.blocked)
                break

        return True

    def exit_loop(self, item: InternalItem) -> bool:
        if not self.entry:
            raise Exception("exiting_loop called without entry")
        if item != self.entry:
            return False
        self.entry = None
        # excluded_recipes.remove(self.blocked)
        self.blocked = None
        return True

    # what would getting one of the item from the loop cost
    def get_cost(self, item: InternalItem) -> dict[InternalItem, float]:
        item_index = 0
        while self.recipes[item_index][0] != item:
            item_index += 1
        recipes = self.recipes[item_index:] + self.recipes[:item_index]

        loop_ingredients: dict[InternalItem, float] = {}
        ingredients = {item: 1}
        for index, (current_item, recipe) in enumerate(recipes):
            amount_wanted = ingredients[current_item]
            produced = recipe.products[current_item]
            ingredients = {ingredient: (cost/produced) * amount_wanted
                           for ingredient, cost in recipe.ingredients.items()}

            for ingredient, cost in ingredients.items():
                if index + 1 != len(recipes) and ingredient == recipes[index+1][0]:
                    continue
                if ingredient not in loop_ingredients:
                    loop_ingredients[ingredient] = cost
                else:
                    loop_ingredients[ingredient] += cost

        return loop_ingredients

    def get_recipe(self, item: InternalItem):
        item_index = 0
        while self.recipes[item_index][0] != item:
            item_index += 1
        return self.recipes[item_index][1]

all_ingredients: dict[str, InternalItem] = {}
valid_ingredients: dict[str, InternalItem] = {}
fluids: set[str] = set(fluids_future.result())
del fluids_future

def register_iternal_items():
    invalid_items = {"pistol", "fluid-unknown"} | {f"parameter-{i}" for i in range(10)}

    global all_ingredients, valid_ingredients, fluids, items_future

    for fluid in fluids:
        if fluid in invalid_items:
            continue
        ingredient = InternalItem(fluid, True)
        all_ingredients[fluid] = ingredient
        valid_ingredients[fluid] = ingredient

    item_stack_sizes: dict[str, int] = items_future.result()
    del items_future

    for item, stack_size in item_stack_sizes.items():
        if item in invalid_items:
            continue
        ingredient = InternalItem(item, False)
        all_ingredients[item] = ingredient
        if stack_size > 1:
            valid_ingredients[item] = ingredient

    all_ingredients["rocket-part"] = InternalItem("rocket-part", False)

register_iternal_items()


root_categories = {"basic-solid", "basic-fluid", "water", "bob-air-pump"}

recipeProcessingSet = set()
lastLoopRecipe: Recipe | None = None

class Recipe(FactorioElement):
    name: str
    category: str
    ingredients: dict[InternalItem, float]
    products: dict[InternalItem, float]
    energy: float

    def __init__(self, name: str, category: str, ingredients_raw: dict[InternalItem | str, float],
                 products_raw: dict[InternalItem | str, float], energy: float):
        self.name = name
        # TODO add check for category
        self.category = category
        self.energy = energy
        self.productivity = False
        self.__raw_ingredients: dict[InternalItem, float] = {}
        self.__all_unlocking_technologies: set[Technology] = set()
        self.__all_categories: set[Category] = set()

        self.ingredients = {}
        for ingredient, amount in ingredients_raw.items():
            if type(ingredient) is InternalItem:
                self.ingredients[ingredient] = amount
            elif type(ingredient) is str:
                assert ingredient in all_ingredients, (f"Unknown ingredient: {ingredient}", f"In recipe {self.name}")
                self.ingredients[all_ingredients[ingredient]] = amount
            else:
                raise TypeError(f"Unknown ingredient type: {ingredient} \nIn recipe {self.name}")

        self.products = {}
        for product, amount in products_raw.items():
            if type(product) is InternalItem:
                self.products[product] = amount
            elif type(product) is str:
                assert product in all_ingredients, (f"Unknown product: {product}", f"In recipe {self.name}")
                self.products[all_ingredients[product]] = amount
            else:
                raise TypeError(f"Unknown product type: {product} \nIn recipe {self.name}")

        for product in self.products.keys():
            product.recipes.add(self)
            product.invalidate_cache()

        for ingredient in self.ingredients.keys():
            ingredient.is_used_in.add(self)

        if category in root_categories:
            for product, produced in self.products.items():
                product.root_item = True
                product.best_recipe = self
                product.best_non_recursive_recipe = self
                # if ingredients:
                #     for ingredient, cost in ingredients.items():
                #         product.raw_ingredients |= {ingredient: cost/produced}
                # else:
                #     if self.name not in rel_cost:
                #         print(f"spontaneously existing item ({product.name}) doesn't have a cost, default to 1")
                #     product.raw_ingredients = {product: 1}
                #     product.raw_eval = True

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def remove(self):
        del recipes[self.name]
        for product in self.products.keys():
            product.recipes.remove(self)
            if self == product.best_recipe:
                product.invalidate_cache()

        for ingredient in self.ingredients.keys():
            ingredient.is_used_in.remove(self)

    @property
    def crafting_machine(self) -> Machine:
        """cheapest crafting machine name able to run this recipe"""
        return machine_per_category[self.category]

    @property
    def unlocking_technologies(self) -> set[Technology]:
        """Unlocked by any of the returned technologies. Empty set indicates a starting recipe."""
        from .Technologies import technology_table
        return {technology_table[tech_name] for tech_name in recipe_sources.get(self.name, ())}

    def all_unlocking_technologies(self) -> set[Technology]:
        _, technologies, all_categories = self.eval()
        for category in all_categories:
            technologies |= machine_per_category[category].all_unlocking_technologies()
        return technologies


    @property
    def total_energy(self) -> float:
        """Total required energy (crafting time) for single craft"""
        # TODO: multiply mining energy by 2 since drill has 0.5 speed
        total_energy = self.energy
        for ingredient, cost in self.ingredients.items():
            ingredient.get_raw_ingredients()
            if ingredient.best_recipe:
                total_energy += ingredient.best_recipe.total_energy / ingredient.best_recipe.products[ingredient] * cost
            # if ingredient in craftable:
            #     selected_recipe_energy = float('inf')
            #     for ingredient_recipe in all_product_sources[ingredient]:
            #         craft_count = max((n for name, n in ingredient_recipe.products.items() if name == ingredient))
            #         recipe_energy = ingredient_recipe.total_energy / craft_count * cost
            #         if recipe_energy < selected_recipe_energy:
            #             selected_recipe_energy = recipe_energy
            #     total_energy += selected_recipe_energy
        return total_energy

    def get_raw_ingredients(self) -> dict[InternalItem, float]:
        return self.eval()[0]


    def eval(self) -> tuple[dict[InternalItem, float], set[Technology], set[Category]]:
        invalid_cache = any(loop.entry for ingredient in self.ingredients for loop in ingredient.recursive_loops) # todo less invalidation possible?

        if self.__raw_ingredients and not invalid_cache:
            return self.__raw_ingredients, self.__all_unlocking_technologies, self.__all_categories
        invalid = False

        base_tech = self.unlocking_technologies
        req_categories = {self.category}
        ingredients = {}
        for ingredient, cost in self.ingredients.items():
            if ingredient in InternalItem.evaluating:
                # recursion occured log and bounce
                RecursiveRecipeLoop(ingredient)
                return {}, set(), set() # todo fix recursion
                invalid = True
                continue

            raw_ingredients, _, tech, cat = ingredient.eval()
            if not raw_ingredients:
                # not currently a valid path fail
                return {}, set(), set()

            base_tech |= tech
            req_categories |= cat
            for raw_ingredient, raw_cost in raw_ingredients.items():
                if raw_ingredient not in ingredients:
                    ingredients[raw_ingredient] = raw_cost * cost
                else:
                    ingredients[raw_ingredient] += raw_cost * cost

        if invalid:
            return {}, set(), set()

        if not invalid_cache:
            self.__raw_ingredients = ingredients
            self.__all_unlocking_technologies = base_tech
            self.__all_categories = req_categories

        return ingredients, base_tech, req_categories

class Machine(FactorioElement):
    evaluating: set[Machine] = set()
    def __init__(self, name, categories):
        self.name: str = name
        self.item: InternalItem | None
        if self.name != "character":
            self.item = all_ingredients[name]
        else:
            self.item = None
        self.categories: set = categories

    def all_unlocking_technologies(self) -> set[Technology]:
        if self.item:
            if self in Machine.evaluating:
                return set()
            Machine.evaluating.add(self)
            tech = self.item.all_unlocking_technologies()
            Machine.evaluating.remove(self)
            return tech
        else:
            return set()


recipe_sources: dict[str, set[str]] = {}  # recipe_name -> technology source
mining_with_fluid_sources: set[str] = set()


recipes: dict[str, Recipe] = {}
# all_product_sources: Dict[str, Set[Recipe]] = {"character": set()}
# add uranium mining to logic graph. TODO: add to automatic extractor for mod support
raw_recipes = recipes_future.result()
del recipes_future
for resource_name, resource_data in resources_future.result().items():
    raw_recipes[f"mining-{resource_name}"] = {
        "ingredients": {resource_data["required_fluid"]: resource_data["fluid_amount"]}
        if "required_fluid" in resource_data else {},
        "products": {data["name"]: data["amount"] for data in resource_data["products"].values()},
        "energy": resource_data["mining_time"],
        "category": resource_data["category"]
    }
    if "required_fluid" in resource_data:
        recipe_sources.setdefault(f"mining-{resource_name}", set()).update(mining_with_fluid_sources)
del resources_future

for recipe_name, recipe_data in raw_recipes.items():
    # example:
    # "accumulator":{"ingredients":{"iron-plate":2,"battery":5},"products":{"accumulator":1},"category":"crafting"}
    # FIXME: add mining?
    if (("barrel" in recipe_data["products"] and recipe_name != "barrel")
            or ("bob-gas-canister" in recipe_data["products"] and recipe_name != "bob-gas-canister")
            or ("bob-empty-canister" in recipe_data["products"] and recipe_name != "bob-empty-canister")
            or (recipe_data["category"] == "parameters")):
        continue


    recipe = Recipe(recipe_name, recipe_data["category"],
                    {all_ingredients[ingredient]: amount for ingredient, amount in recipe_data["ingredients"].items()},
                    {all_ingredients[product]: amount for product, amount in recipe_data["products"].items()},
                    recipe_data["energy"] if "energy" in recipe_data else 0)
    recipes[recipe_name] = recipe

    # if (set(recipe.products).isdisjoint(set(recipe.ingredients)) # prevents loop recipes like uranium centrifuging
    #         and ("barrel" not in recipe.products or recipe.name == "barrel")
    #         and ("bob-gas-canister" not in recipe.products or recipe.name == "bob-gas-canister")
    #         and ("bob-empty-canister" not in recipe.products or recipe.name == "bob-empty-canister")
    #         and not recipe_name.endswith("-reprocessing")):
        # for product_name in recipe.products:
        #     all_product_sources.setdefault(product_name, set()).add(recipe)
imported_recipes: dict[str, Recipe] = recipes.copy()

# name, category, ingredients_name, products_name, energy
custom_recipes_prototype: list[tuple[str, Category, dict[str, float], dict[str, float], float]] = [
    ("bob-small-alien-artifact", "advanced-crafting", {"bob-laser-rifle-battery": 1}, {"bob-small-alien-artifact": 1}, 5),
    ("bob-small-alien-artifact-red", "advanced-crafting", {"bob-laser-rifle-battery-ruby": 1}, {"bob-small-alien-artifact-red": 1}, 5),
    ("bob-small-alien-artifact-orange", "advanced-crafting", {"bob-laser-rifle-battery-topaz": 1}, {"bob-small-alien-artifact-orange": 1}, 5),
    ("bob-small-alien-artifact-yellow", "advanced-crafting", {"bob-laser-rifle-battery-diamond": 1}, {"bob-small-alien-artifact-yellow": 1}, 5),
    ("bob-small-alien-artifact-green", "advanced-crafting", {"bob-laser-rifle-battery-emerald": 1}, {"bob-small-alien-artifact-green": 1}, 5),
    ("bob-small-alien-artifact-blue", "advanced-crafting", {"bob-laser-rifle-battery-sapphire": 1}, {"bob-small-alien-artifact-blue": 1}, 5),
    ("bob-small-alien-artifact-purple", "advanced-crafting", {"bob-laser-rifle-battery-amethyst": 1}, {"bob-small-alien-artifact-purple": 1}, 5),
]
global_custom_recipes: dict[str, Recipe] = {}
for custom_recipe_prototype in custom_recipes_prototype:
    # TODO add optional crafting_machine_tints
    # TODO add group for AP recipes
    # TODO add support for custom techs for recipes
    recipe = Recipe(custom_recipe_prototype[0], custom_recipe_prototype[1],
                                                 custom_recipe_prototype[2],
                                                 custom_recipe_prototype[3],
                                                 custom_recipe_prototype[4])
    recipes[custom_recipe_prototype[0]] = recipe
    global_custom_recipes[custom_recipe_prototype[0]] = recipe


machines: dict[str, Machine] = {}

for name, categories in machines_future.result().items():
    machine = Machine(name, set(categories))
    machines[name] = machine

# add electric mining drill as a crafting machine to resolve basic-solid (mining)
# machines["electric-mining-drill"] = Machine("electric-mining-drill", {"basic-solid"})
machines["pumpjack"] = Machine("pumpjack", {"basic-fluid"})
machines["assembling-machine-1"].categories.add("crafting-with-fluid")  # mod enables this
machines["character"].categories.add("basic-crafting")  # somehow this is implied and not exported
machines["character"].categories.add("basic-solid")

machines["bob-water-miner-1"] = Machine("bob-water-miner-1", {"water"})
machines["bob-steam-mining-drill"] = Machine("bob-steam-mining-drill", {"basic-solid"})

del machines_future

def load_precalc():
    from .Technologies import technology_table
    precalc = load_json_data("precalc")

    for item_name, result in precalc.items():
        item = all_ingredients[item_name]
        item.set_cache({all_ingredients[ingredient_name]: cost for ingredient_name, cost in result["raw_ingredients"].items()},
                       recipes[result["best_recipe"]] if result["best_recipe"] else None,
                       {technology_table[tech] for tech in result["technologies"]},
                       set(result["category"]))


# build requirements graph for all technology ingredients

rel_cost = {
    "iron-ore": 1,
    "copper-ore": 1,
    "stone": 1,
    "crude-oil": 1,
    "water": 0.5,
    "coal": 1,
    "raw-fish": float("inf"),
    "steam": 0.5,
    "depleted-uranium-fuel-cell": float("inf"),
    "bob-depleted-thorium-fuel-cell": float("inf"),
    "bob-depleted-deuterium-fuel-cell": float("inf"),
    "bob-liquid-air": 0.5,
    "bob-lithia-water": 1,
}

invalid_ingredients = {"raw-fish",
                       "depleted-uranium-fuel-cell",
                       "bob-depleted-thorium-fuel-cell",
                       "bob-depleted-deuterium-fuel-cell",
                       "bob-fusion-catalyst"}

artifacts = {"bob-small-alien-artifact",
             "bob-small-alien-artifact-red",
             "bob-small-alien-artifact-orange",
             "bob-small-alien-artifact-yellow",
             "bob-small-alien-artifact-green",
             "bob-small-alien-artifact-blue",
             "bob-small-alien-artifact-purple"}

machine_per_category = {"crafting": machines["character"],
                        "basic-crafting": machines["character"],
                        "advanced-crafting": machines["bob-steam-assembling-machine"],
                        "crafting-with-fluid": machines["bob-steam-assembling-machine"],
                        "smelting": machines["stone-furnace"],
                        "oil-processing": machines["oil-refinery"],
                        "chemistry": machines["chemical-plant"],
                        "centrifuging": machines["centrifuge"],
                        "rocket-building": machines["rocket-silo"],
                        "basic-fluid": machines["pumpjack"],
                        "basic-solid": machines["character"],
                        "parameters": machines["stone-furnace"],
                        "bob-chemical-furnace": machines["bob-stone-chemical-furnace"],
                        "water": machines["bob-water-miner-1"],
                        "bob-void-fluid": machines["bob-void-pump"],
                        "electronics": machines["bob-electronics-machine-1"],
                        "electronics-with-fluid": machines["bob-electronics-machine-1"],
                        "bob-air-pump": machines["bob-air-pump"],
                        "bob-water-pump": machines["bob-water-pump"],
                        "barrelling": machines["bob-water-pump"],
                        "bob-greenhouse": machines["bob-greenhouse"],
                        "bob-electrolysis": machines["bob-electrolyser"],
                        "bob-distillery": machines["bob-distillery"],
                        "bob-mixing-furnace": machines["bob-stone-mixing-furnace"],
                        }

# cleanup async helpers
pool.shutdown()
del pool
