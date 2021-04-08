import logging

from BaseClasses import Region, Entrance, Location, MultiWorld, Item

from .Technologies import tech_table, recipe_sources, technology_table

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
    crash.connect(nauvis)
    world.regions += [menu, nauvis]


def set_rules(world: MultiWorld, player: int):
    if world.logic[player] != 'nologic':
        from worlds.generic import Rules
        for tech_name, technology in technology_table.items():
            # loose nodes
            rules = technology.get_required_technologies()
            if rules:
                location = world.get_location(tech_name, player)
                Rules.set_rule(location, lambda state, rules=rules: all(state.has(rule, player) for rule in rules))

        # get all technologies
        world.completion_condition[player] = lambda state: all(state.has(technology, player)
                                                               for technology in tech_table)
