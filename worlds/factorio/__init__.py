from ..AutoWorld import World

from BaseClasses import Region, Entrance, Location, Item
from .Technologies import base_tech_table, recipe_sources, base_technology_table, advancement_technologies, \
    all_ingredient_names, required_technologies, get_rocket_requirements, rocket_recipes, \
    progressive_technology_table, common_tech_table, tech_to_progressive_lookup, progressive_tech_table, \
    get_science_pack_pools, Recipe, recipes, technology_table, tech_table
from .Shapes import get_shapes
from .Mod import generate_mod
from .Options import factorio_options


class FactorioItem(Item):
    game = "Factorio"


class Factorio(World):
    game: str = "Factorio"
    static_nodes = {"automation", "logistics", "rocket-silo"}
    custom_recipes = {}
    additional_advancement_technologies = set()
    item_names = frozenset(tech_table)
    location_names = frozenset(base_tech_table)

    item_name_to_id = tech_table
    location_name_to_id = base_tech_table

    def generate_basic(self):
        for tech_name in base_tech_table:
            if self.world.progressive:
                item_name = tech_to_progressive_lookup.get(tech_name, tech_name)
            else:
                item_name = item_name
            tech_item = self.create_item(item_name)
            if tech_name in self.static_nodes:
                self.world.get_location(tech_name, self.player).place_locked_item(tech_item)
            else:
                self.world.itempool.append(tech_item)
        map_basic_settings = self.world.world_gen[self.player].value["basic"]
        if map_basic_settings.get("seed", None) is None:  # allow seed 0
            map_basic_settings["seed"] = self.world.slot_seeds[self.player].randint(0, 2**32-1)  # 32 bit uint

    generate_output = generate_mod

    def create_regions(self):
        player = self.player
        menu = Region("Menu", None, "Menu", player, self.world)
        crash = Entrance(player, "Crash Land", menu)
        menu.exits.append(crash)
        nauvis = Region("Nauvis", None, "Nauvis", player, self.world)

        for tech_name, tech_id in base_tech_table.items():
            tech = Location(player, tech_name, tech_id, nauvis)
            nauvis.locations.append(tech)
            tech.game = "Factorio"
        location = Location(player, "Rocket Launch", None, nauvis)
        nauvis.locations.append(location)
        location.game = "Factorio"
        event = Item("Victory", True, None, player)
        event.game = "Factorio"
        self.world.push_item(location, event, False)
        location.event = location.locked = True
        for ingredient in self.world.max_science_pack[self.player].get_allowed_packs():
            location = Location(player, f"Automate {ingredient}", None, nauvis)
            location.game = "Factorio"
            nauvis.locations.append(location)
            event = Item(f"Automated {ingredient}", True, None, player)
            self.world.push_item(location, event, False)
            location.event = location.locked = True
        crash.connect(nauvis)
        self.world.regions += [menu, nauvis]

    def set_rules(self):
        world = self.world
        player = self.player
        self.custom_technologies = self.set_custom_technologies()
        self.set_custom_recipes()
        shapes = get_shapes(self)
        if world.logic[player] != 'nologic':
            from worlds.generic import Rules
            for ingredient in self.world.max_science_pack[self.player].get_allowed_packs():
                location = world.get_location(f"Automate {ingredient}", player)

                if self.world.recipe_ingredients[self.player]:
                    custom_recipe = self.custom_recipes[ingredient]

                    location.access_rule = lambda state, ingredient=ingredient, custom_recipe = custom_recipe: \
                        (ingredient not in technology_table or state.has(ingredient, player)) and \
                        all(state.has(technology.name, player) for sub_ingredient in custom_recipe.ingredients
                            for technology in required_technologies[sub_ingredient])
                else:
                    location.access_rule = lambda state, ingredient=ingredient: \
                        all(state.has(technology.name, player) for technology in required_technologies[ingredient])

            for tech_name, technology in self.custom_technologies.items():
                location = world.get_location(tech_name, player)
                Rules.set_rule(location, technology.build_rule(player))
                prequisites = shapes.get(tech_name)
                if prequisites:
                    locations = {world.get_location(requisite, player) for requisite in prequisites}
                    Rules.add_rule(location, lambda state,
                                                    locations=locations: all(state.can_reach(loc) for loc in locations))

            victory_tech_names = get_rocket_requirements(self.custom_recipes["rocket-part"])
            world.get_location("Rocket Launch", player).access_rule = lambda state: all(state.has(technology, player)
                                                                                        for technology in
                                                                                        victory_tech_names)

        world.completion_condition[player] = lambda state: state.has('Victory', player)

    def collect(self, state, item) -> bool:
        if item.advancement and item.name in progressive_technology_table:
            prog_table = progressive_technology_table[item.name].progressive
            for item_name in prog_table:
                if not state.has(item_name, item.player):
                    state.prog_items[item_name, item.player] += 1
                    return True
        return super(Factorio, self).collect(state, item)

    def get_required_client_version(self) -> tuple:
        return max((0, 1, 5), super(Factorio, self).get_required_client_version())

    options = factorio_options

    def set_custom_technologies(self):
        custom_technologies = {}
        allowed_packs = self.world.max_science_pack[self.player].get_allowed_packs()
        for technology_name, technology in base_technology_table.items():
            custom_technologies[technology_name] = technology.get_custom(self.world, allowed_packs, self.player)
        return custom_technologies

    def set_custom_recipes(self):
        original_rocket_part = recipes["rocket-part"]
        science_pack_pools = get_science_pack_pools()
        valid_pool = sorted(science_pack_pools[self.world.max_science_pack[self.player].get_max_pack()])
        self.world.random.shuffle(valid_pool)
        self.custom_recipes = {"rocket-part": Recipe("rocket-part", original_rocket_part.category,
                                                     {valid_pool[x] : 10 for x in range(3)},
                                                     original_rocket_part.products)}
        self.additional_advancement_technologies = {tech.name for tech in
                                                    self.custom_recipes["rocket-part"].recursive_unlocking_technologies}

        if self.world.recipe_ingredients[self.player]:
            valid_pool = []
            for pack in self.world.max_science_pack[self.player].get_ordered_science_packs():
                valid_pool += sorted(science_pack_pools[pack])
                self.world.random.shuffle(valid_pool)
                if pack in recipes: # skips over space science pack
                    original = recipes[pack]
                    new_ingredients = {}
                    for _ in original.ingredients:
                        new_ingredients[valid_pool.pop()] = 1
                    new_recipe = Recipe(pack, original.category, new_ingredients, original.products)
                    self.additional_advancement_technologies |= {tech.name for tech in
                                                                 new_recipe.recursive_unlocking_technologies}
                    self.custom_recipes[pack] = new_recipe

        # handle marking progressive techs as advancement
        prog_add = set()
        for tech in self.additional_advancement_technologies:
            if tech in tech_to_progressive_lookup:
                prog_add.add(tech_to_progressive_lookup[tech])
        self.additional_advancement_technologies |= prog_add

    def create_item(self, name: str) -> Item:
        assert name in tech_table
        return FactorioItem(name, name in advancement_technologies or
                            name in self.additional_advancement_technologies,
                            tech_table[name], self.player)