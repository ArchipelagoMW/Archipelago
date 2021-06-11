from ..BaseWorld import World


from BaseClasses import Region, Entrance, Location, MultiWorld, Item
from .Technologies import tech_table, recipe_sources, technology_table, advancement_technologies, \
    all_ingredient_names, required_technologies, get_rocket_requirements, rocket_recipes
from .Shapes import get_shapes

class Factorio(World):
    def generate_basic(self, world: MultiWorld, player: int):
        static_nodes = world._static_nodes = {"automation", "logistics"}  # turn dynamic/option?
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
        world.custom_data[player]["custom_technologies"] = custom_technologies = set_custom_technologies(world, player)
        set_rules(world, player, custom_technologies)

def gen_factorio(world: MultiWorld, player: int):
    static_nodes = world._static_nodes = {"automation", "logistics"}  # turn dynamic/option?
    victory_tech_names = get_rocket_requirements(frozenset(rocket_recipes[world.max_science_pack[player].value]))
    for tech_name, tech_id in tech_table.items():
        tech_item = Item(tech_name, tech_name in advancement_technologies or tech_name in victory_tech_names,
                         tech_id, player)
        tech_item.game = "Factorio"
        if tech_name in static_nodes:
            world.get_location(tech_name, player).place_locked_item(tech_item)
        else:
            world.itempool.append(tech_item)
    world.custom_data[player]["custom_technologies"] = custom_technologies = set_custom_technologies(world, player)
    set_rules(world, player, custom_technologies)


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
    location = Location(player, "Rocket Launch", None, nauvis)
    nauvis.locations.append(location)
    event = Item("Victory", True, None, player)
    world.push_item(location, event, False)
    location.event = location.locked = True
    for ingredient in all_ingredient_names:
        location = Location(player, f"Automate {ingredient}", None, nauvis)
        nauvis.locations.append(location)
        event = Item(f"Automated {ingredient}", True, None, player)
        world.push_item(location, event, False)
        location.event = location.locked = True
    crash.connect(nauvis)
    world.regions += [menu, nauvis]


def set_custom_technologies(world: MultiWorld, player: int):
    custom_technologies = {}
    world_custom = getattr(world, "_custom_technologies", {})
    world_custom[player] = custom_technologies
    world._custom_technologies = world_custom
    allowed_packs = world.max_science_pack[player].get_allowed_packs()
    for technology_name, technology in technology_table.items():
        custom_technologies[technology_name] = technology.get_custom(world, allowed_packs, player)
    return custom_technologies


def set_rules(world: MultiWorld, player: int, custom_technologies):
    shapes = get_shapes(world, player)
    if world.logic[player] != 'nologic':
        from worlds.generic import Rules
        for ingredient in all_ingredient_names:
            location = world.get_location(f"Automate {ingredient}", player)
            location.access_rule = lambda state, ingredient=ingredient: \
                all(state.has(technology.name, player) for technology in required_technologies[ingredient])
        for tech_name, technology in custom_technologies.items():
            location = world.get_location(tech_name, player)
            Rules.set_rule(location, technology.build_rule(player))
            prequisites = shapes.get(tech_name)
            if prequisites:
                locations = {world.get_location(requisite, player) for requisite in prequisites}
                Rules.add_rule(location, lambda state,
                                                locations=locations: all(state.can_reach(loc) for loc in locations))
            # get all science pack technologies (but not the ability to craft them)
        victory_tech_names = get_rocket_requirements(frozenset(rocket_recipes[world.max_science_pack[player].value]))
        world.get_location("Rocket Launch", player).access_rule = lambda state: all(state.has(technology, player)
                                                                                    for technology in
                                                                                    victory_tech_names)

    world.completion_condition[player] = lambda state: state.has('Victory', player)
