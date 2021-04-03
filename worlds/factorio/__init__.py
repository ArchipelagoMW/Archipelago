import logging

from BaseClasses import Region, Entrance, Location, MultiWorld, Item

from .Technologies import tech_table, requirements, ingredients, all_ingredients, recipe_sources, all_ingredients_recipe

static_nodes = {"automation", "logistics"}


def gen_factorio(world: MultiWorld, player: int):
    for tech_name, tech_id in tech_table.items():
        tech_item = Item(tech_name, True, tech_id, player)
        tech_item.game = "Factorio"
        if tech_name in static_nodes:
            loc = world.get_location(tech_name, player)
            loc.item = tech_item
            loc.locked = loc.event = True
        else:
            world.itempool.append(tech_item)
    set_rules(world, player)


def factorio_create_regions(world: MultiWorld, player: int):
    menu = Region("Menu", None, "Menu", player)
    crash = Entrance(player, "Crash Land", menu)
    menu.exits.append(crash)
    nauvis = Region("Nauvis", None, "Nauvis", player)
    nauvis.world = menu.world = world
    for tech_name, tech_id in tech_table.items():
        tech = Location(player, tech_name, tech_id, nauvis)
        nauvis.locations.append(tech)
        tech.game = "Factorio"
    for ingredient in all_ingredients_recipe:  # register science packs as events
        ingredient_location = Location(player, ingredient, 0, nauvis)
        ingredient_location.item = Item(ingredient, True, 0, player)
        ingredient_location.event = ingredient_location.locked = True
        menu.locations.append(ingredient_location)
    crash.connect(nauvis)
    world.regions += [menu, nauvis]


def set_rules(world: MultiWorld, player: int):
    if world.logic[player] != 'nologic':
        from worlds.generic import Rules
        for tech_name in tech_table:
            # vanilla layout, to be implemented
            # rules = requirements.get(tech_name, set()) | ingredients.get(tech_name, set())
            # loose nodes
            rules = ingredients.get(tech_name, set())
            if rules:
                location = world.get_location(tech_name, player)
                Rules.set_rule(location, lambda state, rules=rules: all(state.has(rule, player) for rule in rules))

        for recipe, technology in recipe_sources.items():
            Rules.set_rule(world.get_location(recipe, player), lambda state, tech=technology: state.has(tech, player))


        world.completion_condition[player] = lambda state: all(state.has(ingredient, player)
                                                               for ingredient in all_ingredients_recipe)
