import logging
from typing import List, Dict

from BaseClasses import Region, Entrance, Location, MultiWorld, Item
from Options import TechTreeLayout
from .Technologies import tech_table, recipe_sources, technology_table, advancement_technologies, required_technologies

static_nodes = {"automation", "logistics"}


def gen_factorio(world: MultiWorld, player: int):
    for tech_name, tech_id in tech_table.items():
        tech_item = Item(tech_name, tech_name in advancement_technologies, tech_id, player)
        tech_item.game = "Factorio"
        if tech_name in static_nodes:
            loc = world.get_location(tech_name, player)
            loc.item = tech_item
            loc.locked = True
            loc.event = tech_item.advancement
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


def get_shapes(world: MultiWorld, player: int) -> Dict[str, List[str]]:
    prerequisites = {}
    if world.tech_tree_layout[player].value == TechTreeLayout.option_small_diamonds:
        tech_names: List[str] = list(set(technology_table)-static_nodes)
        tech_names.sort()
        world.random.shuffle(tech_names)
        while len(tech_names) > 4:
            slice = tech_names[:4]
            tech_names = tech_names[4:]
            slice.sort(key=lambda tech_name: len(technology_table[tech_name].ingredients))
            diamond_0, diamond_1, diamond_2, diamond_3 = slice

            #   0    |
            # 1   2  |
            #   3    V
            prerequisites[diamond_3] = [diamond_1, diamond_2]
            prerequisites[diamond_2] = prerequisites[diamond_1] = [diamond_0]
    world.tech_tree_layout_prerequisites[player] = prerequisites
    return prerequisites


def set_rules(world: MultiWorld, player: int):
    shapes = get_shapes(world, player)
    if world.logic[player] != 'nologic':
        from worlds.generic import Rules
        allowed_packs = world.max_science_pack[player].get_allowed_packs()
        for tech_name, technology in technology_table.items():
            # loose nodes
            location = world.get_location(tech_name, player)
            Rules.set_rule(location, technology.build_rule(allowed_packs, player))
            prequisites = shapes.get(tech_name)
            if prequisites:
                locations = [world.get_location(requisite, player) for requisite in prequisites]
                Rules.add_rule(location, lambda state,
                                                locations=locations: all(state.can_reach(loc) for loc in locations))


        # get all technologies
        world.completion_condition[player] = lambda state: all(state.has(technology, player)
                                                               for technology in advancement_technologies)
