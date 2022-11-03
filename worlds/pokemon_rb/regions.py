
from BaseClasses import MultiWorld, Region, Entrance, RegionType, LocationProgressType
from worlds.generic.Rules import add_item_rule
from .locations import location_data, PokemonRBLocation


def create_region(world: MultiWorld, player: int, name: str, locations_per_region=None, exits=None):
    ret = Region(name, RegionType.Generic, name, player, world)
    for location in locations_per_region.get(name, []):
        if (world.randomize_hidden_items[player].value or "Hidden" not in location.name) and \
                (world.extra_key_items[player].value or name != "Rock Tunnel B1F" or "Item" not in location.name) and \
                (world.tea[player].value or location.name != "Celadon City - Mansion Lady"):
            location.parent_region = ret
            ret.locations.append(location)
            if world.randomize_hidden_items[player].value == 2 and "Hidden" in location.name:
                location.progress_type = LocationProgressType.EXCLUDED
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))
    locations_per_region[name] = []
    return ret


def create_regions(world: MultiWorld, player: int):
    locations_per_region = {}
    for location in location_data:
        locations_per_region.setdefault(location.region, [])
        locations_per_region[location.region].append(PokemonRBLocation(player, location.name, location.address,
                                                                       location.rom_address))
    regions = [
        create_region(world, player, "Menu", locations_per_region),
        create_region(world, player, "Anywhere", locations_per_region),
        create_region(world, player, "Fossil", locations_per_region),
        create_region(world, player, "Pallet Town", locations_per_region),
        create_region(world, player, "Route 1", locations_per_region),
        create_region(world, player, "Viridian City", locations_per_region),
        create_region(world, player, "Viridian City North", locations_per_region),
        create_region(world, player, "Viridian Gym", locations_per_region),
        create_region(world, player, "Route 2", locations_per_region),
        create_region(world, player, "Route 2 East", locations_per_region),
        create_region(world, player, "Diglett's Cave", locations_per_region),
        create_region(world, player, "Route 22", locations_per_region),
        create_region(world, player, "Route 23", locations_per_region),
        create_region(world, player, "Viridian Forest", locations_per_region),
        create_region(world, player, "Pewter City", locations_per_region),
        create_region(world, player, "Pewter Gym", locations_per_region),
        create_region(world, player, "Route 3", locations_per_region),
        create_region(world, player, "Mt Moon 1F", locations_per_region),
        create_region(world, player, "Mt Moon B1F", locations_per_region),
        create_region(world, player, "Mt Moon B2F", locations_per_region),
        create_region(world, player, "Route 4", locations_per_region),
        create_region(world, player, "Cerulean City", locations_per_region),
        create_region(world, player, "Cerulean Gym", locations_per_region),
        create_region(world, player, "Route 24", locations_per_region),
        create_region(world, player, "Route 25", locations_per_region),
        create_region(world, player, "Route 9", locations_per_region),
        create_region(world, player, "Route 10 North", locations_per_region),
        create_region(world, player, "Rock Tunnel 1F", locations_per_region),
        create_region(world, player, "Rock Tunnel B1F", locations_per_region),
        create_region(world, player, "Power Plant", locations_per_region),
        create_region(world, player, "Route 10 South", locations_per_region),
        create_region(world, player, "Lavender Town", locations_per_region),
        create_region(world, player, "Pokemon Tower 1F", locations_per_region),
        create_region(world, player, "Pokemon Tower 2F", locations_per_region),
        create_region(world, player, "Pokemon Tower 3F", locations_per_region),
        create_region(world, player, "Pokemon Tower 4F", locations_per_region),
        create_region(world, player, "Pokemon Tower 5F", locations_per_region),
        create_region(world, player, "Pokemon Tower 6F", locations_per_region),
        create_region(world, player, "Pokemon Tower 7F", locations_per_region),
        create_region(world, player, "Route 5", locations_per_region),
        create_region(world, player, "Saffron City", locations_per_region),
        create_region(world, player, "Saffron Gym", locations_per_region),
        create_region(world, player, "Copycat's House", locations_per_region),
        create_region(world, player, "Underground Tunnel North-South", locations_per_region),
        create_region(world, player, "Route 6", locations_per_region),
        create_region(world, player, "Vermilion City", locations_per_region),
        create_region(world, player, "Vermilion Gym", locations_per_region),
        create_region(world, player, "S.S. Anne 1F", locations_per_region),
        create_region(world, player, "S.S. Anne B1F", locations_per_region),
        create_region(world, player, "S.S. Anne 2F", locations_per_region),
        create_region(world, player, "Route 11", locations_per_region),
        create_region(world, player, "Route 11 East", locations_per_region),
        create_region(world, player, "Route 12 North", locations_per_region),
        create_region(world, player, "Route 12 South", locations_per_region),
        create_region(world, player, "Route 12 Grass", locations_per_region),
        create_region(world, player, "Route 12 West", locations_per_region),
        create_region(world, player, "Route 7", locations_per_region),
        create_region(world, player, "Underground Tunnel West-East", locations_per_region),
        create_region(world, player, "Route 8", locations_per_region),
        create_region(world, player, "Route 8 Grass", locations_per_region),
        create_region(world, player, "Celadon City", locations_per_region),
        create_region(world, player, "Celadon Prize Corner", locations_per_region),
        create_region(world, player, "Celadon Gym", locations_per_region),
        create_region(world, player, "Route 16", locations_per_region),
        create_region(world, player, "Route 16 North", locations_per_region),
        create_region(world, player, "Route 17", locations_per_region),
        create_region(world, player, "Route 18", locations_per_region),
        create_region(world, player, "Fuchsia City", locations_per_region),
        create_region(world, player, "Fuchsia Gym", locations_per_region),
        create_region(world, player, "Safari Zone Gate", locations_per_region),
        create_region(world, player, "Safari Zone Center", locations_per_region),
        create_region(world, player, "Safari Zone East", locations_per_region),
        create_region(world, player, "Safari Zone North", locations_per_region),
        create_region(world, player, "Safari Zone West", locations_per_region),
        create_region(world, player, "Route 15", locations_per_region),
        create_region(world, player, "Route 14", locations_per_region),
        create_region(world, player, "Route 13", locations_per_region),
        create_region(world, player, "Route 19", locations_per_region),
        create_region(world, player, "Route 20 East", locations_per_region),
        create_region(world, player, "Route 20 West", locations_per_region),
        create_region(world, player, "Seafoam Islands 1F", locations_per_region),
        create_region(world, player, "Seafoam Islands B1F", locations_per_region),
        create_region(world, player, "Seafoam Islands B2F", locations_per_region),
        create_region(world, player, "Seafoam Islands B3F", locations_per_region),
        create_region(world, player, "Seafoam Islands B4F", locations_per_region),
        create_region(world, player, "Cinnabar Island", locations_per_region),
        create_region(world, player, "Cinnabar Gym", locations_per_region),
        create_region(world, player, "Route 21", locations_per_region),
        create_region(world, player, "Silph Co 1F", locations_per_region),
        create_region(world, player, "Silph Co 2F", locations_per_region),
        create_region(world, player, "Silph Co 3F", locations_per_region),
        create_region(world, player, "Silph Co 4F", locations_per_region),
        create_region(world, player, "Silph Co 5F", locations_per_region),
        create_region(world, player, "Silph Co 6F", locations_per_region),
        create_region(world, player, "Silph Co 7F", locations_per_region),
        create_region(world, player, "Silph Co 8F", locations_per_region),
        create_region(world, player, "Silph Co 9F", locations_per_region),
        create_region(world, player, "Silph Co 10F", locations_per_region),
        create_region(world, player, "Silph Co 11F", locations_per_region),
        create_region(world, player, "Rocket Hideout B1F", locations_per_region),
        create_region(world, player, "Rocket Hideout B2F", locations_per_region),
        create_region(world, player, "Rocket Hideout B3F", locations_per_region),
        create_region(world, player, "Rocket Hideout B4F", locations_per_region),
        create_region(world, player, "Pokemon Mansion 1F", locations_per_region),
        create_region(world, player, "Pokemon Mansion 2F", locations_per_region),
        create_region(world, player, "Pokemon Mansion 3F", locations_per_region),
        create_region(world, player, "Pokemon Mansion B1F", locations_per_region),
        create_region(world, player, "Victory Road 1F", locations_per_region),
        create_region(world, player, "Victory Road 2F", locations_per_region),
        create_region(world, player, "Victory Road 3F", locations_per_region),
        create_region(world, player, "Indigo Plateau", locations_per_region),
        create_region(world, player, "Cerulean Cave 1F", locations_per_region),
        create_region(world, player, "Cerulean Cave 2F", locations_per_region),
        create_region(world, player, "Cerulean Cave B1F", locations_per_region),
        create_region(world, player, "Evolution", locations_per_region),
        ]
    world.regions += regions
    connect(world, player, "Menu", "Anywhere", one_way=True)
    connect(world, player, "Menu", "Pallet Town", one_way=True)
    connect(world, player, "Menu", "Fossil", lambda state: state.pokemon_rb_fossil_checks(
        state.multiworld.second_fossil_check_condition[player].value, player), one_way=True)
    connect(world, player, "Pallet Town", "Route 1")
    connect(world, player, "Route 1", "Viridian City")
    connect(world, player, "Viridian City", "Route 22")
    connect(world, player, "Route 22", "Route 23",
            lambda state: state.pokemon_rb_has_badges(state.multiworld.victory_road_condition[player].value, player) and
                          state.pokemon_rb_can_surf(player))
    connect(world, player, "Viridian City North", "Viridian Gym", lambda state:
                     state.pokemon_rb_has_badges(state.multiworld.viridian_gym_condition[player].value, player), one_way=True)
    connect(world, player, "Route 2", "Route 2 East", lambda state: state.pokemon_rb_can_cut(player))
    connect(world, player, "Route 2 East", "Diglett's Cave", lambda state: state.pokemon_rb_can_cut(player))
    connect(world, player, "Route 2", "Viridian City North")
    connect(world, player, "Route 2", "Viridian Forest")
    connect(world, player, "Route 2", "Pewter City")
    connect(world, player, "Pewter City", "Pewter Gym", one_way=True)
    connect(world, player, "Pewter City", "Route 3")
    connect(world, player, "Route 4", "Route 3", one_way=True)
    connect(world, player, "Mt Moon 1F", "Mt Moon B1F", one_way=True)
    connect(world, player, "Mt Moon B1F", "Mt Moon B2F", one_way=True)
    connect(world, player, "Mt Moon B1F", "Route 4", one_way=True)
    connect(world, player, "Route 4", "Cerulean City")
    connect(world, player, "Cerulean City", "Cerulean Gym", one_way=True)
    connect(world, player, "Cerulean City", "Route 24", one_way=True)
    connect(world, player, "Route 24", "Route 25", one_way=True)
    connect(world, player, "Cerulean City", "Route 9", lambda state: state.pokemon_rb_can_cut(player))
    connect(world, player, "Route 9", "Route 10 North")
    connect(world, player, "Route 10 North", "Rock Tunnel 1F", lambda state: state.pokemon_rb_can_flash(player))
    connect(world, player, "Route 10 North", "Power Plant", lambda state: state.pokemon_rb_can_surf(player) and
            (state.has("Plant Key", player) or not state.multiworld.extra_key_items[player].value), one_way=True)
    connect(world, player, "Rock Tunnel 1F", "Route 10 South", lambda state: state.pokemon_rb_can_flash(player))
    connect(world, player, "Rock Tunnel 1F", "Rock Tunnel B1F")
    connect(world, player, "Lavender Town", "Pokemon Tower 1F", one_way=True)
    connect(world, player, "Lavender Town", "Pokemon Tower 1F", one_way=True)
    connect(world, player, "Pokemon Tower 1F", "Pokemon Tower 2F", one_way=True)
    connect(world, player, "Pokemon Tower 2F", "Pokemon Tower 3F", one_way=True)
    connect(world, player, "Pokemon Tower 3F", "Pokemon Tower 4F", one_way=True)
    connect(world, player, "Pokemon Tower 4F", "Pokemon Tower 5F", one_way=True)
    connect(world, player, "Pokemon Tower 5F", "Pokemon Tower 6F", one_way=True)
    connect(world, player, "Pokemon Tower 6F", "Pokemon Tower 7F", lambda state: state.has("Silph Scope", player))
    connect(world, player, "Cerulean City", "Route 5")
    connect(world, player, "Route 5", "Saffron City", lambda state: state.pokemon_rb_can_pass_guards(player))
    connect(world, player, "Route 5", "Underground Tunnel North-South")
    connect(world, player, "Route 6", "Underground Tunnel North-South")
    connect(world, player, "Route 6", "Saffron City", lambda state: state.pokemon_rb_can_pass_guards(player))
    connect(world, player, "Route 7", "Saffron City", lambda state: state.pokemon_rb_can_pass_guards(player))
    connect(world, player, "Route 8", "Saffron City", lambda state: state.pokemon_rb_can_pass_guards(player))
    connect(world, player, "Saffron City", "Copycat's House", lambda state: state.has("Silph Co Liberated", player), one_way=True)
    connect(world, player, "Saffron City", "Saffron Gym", lambda state: state.has("Silph Co Liberated", player), one_way=True)
    connect(world, player, "Route 6", "Vermilion City")
    connect(world, player, "Vermilion City", "Vermilion Gym", lambda state: state.pokemon_rb_can_surf(player) or state.pokemon_rb_can_cut(player), one_way=True)
    connect(world, player, "Vermilion City", "S.S. Anne 1F", lambda state: state.has("S.S. Ticket", player), one_way=True)
    connect(world, player, "S.S. Anne 1F", "S.S. Anne 2F", one_way=True)
    connect(world, player, "S.S. Anne 1F", "S.S. Anne B1F", one_way=True)
    connect(world, player, "Vermilion City", "Route 11")
    connect(world, player, "Vermilion City", "Diglett's Cave")
    connect(world, player, "Route 12 West", "Route 11 East", lambda state: state.pokemon_rb_can_strength(player) or not state.multiworld.extra_strength_boulders[player].value)
    connect(world, player, "Route 12 North", "Route 12 South", lambda state: state.has("Poke Flute", player) or state.pokemon_rb_can_surf( player))
    connect(world, player, "Route 12 West", "Route 12 North", lambda state: state.has("Poke Flute", player))
    connect(world, player, "Route 12 West", "Route 12 South", lambda state: state.has("Poke Flute", player))
    connect(world, player, "Route 12 South", "Route 12 Grass", lambda state: state.pokemon_rb_can_cut(player))
    connect(world, player, "Route 12 North", "Lavender Town")
    connect(world, player, "Route 7", "Lavender Town")
    connect(world, player, "Route 10 South", "Lavender Town")
    connect(world, player, "Route 7", "Underground Tunnel West-East")
    connect(world, player, "Route 8", "Underground Tunnel West-East")
    connect(world, player, "Route 8", "Celadon City")
    connect(world, player, "Route 8", "Route 8 Grass", lambda state: state.pokemon_rb_can_cut(player), one_way=True)
    connect(world, player, "Route 7", "Celadon City")
    connect(world, player, "Celadon City", "Celadon Gym", lambda state: state.pokemon_rb_can_cut(player), one_way=True)
    connect(world, player, "Celadon City", "Celadon Prize Corner")
    connect(world, player, "Celadon City", "Route 16")
    connect(world, player, "Route 16", "Route 16 North", lambda state: state.pokemon_rb_can_cut(player), one_way=True)
    connect(world, player, "Route 16", "Route 17", lambda state: state.has("Poke Flute", player) and state.has("Bicycle", player))
    connect(world, player, "Route 17", "Route 18", lambda state: state.has("Bicycle", player))
    connect(world, player, "Fuchsia City", "Fuchsia Gym", one_way=True)
    connect(world, player, "Fuchsia City", "Route 18")
    connect(world, player, "Fuchsia City", "Safari Zone Gate", one_way=True)
    connect(world, player, "Safari Zone Gate", "Safari Zone Center", lambda state: state.has("Safari Pass", player) or not state.multiworld.extra_key_items[player].value, one_way=True)
    connect(world, player, "Safari Zone Center", "Safari Zone East", one_way=True)
    connect(world, player, "Safari Zone Center", "Safari Zone West", one_way=True)
    connect(world, player, "Safari Zone Center", "Safari Zone North", one_way=True)
    connect(world, player, "Fuchsia City", "Route 15")
    connect(world, player, "Route 15", "Route 14")
    connect(world, player, "Route 14", "Route 13")
    connect(world, player, "Route 13", "Route 12 South", lambda state: state.pokemon_rb_can_strength(player) or state.pokemon_rb_can_surf(player) or not state.multiworld.extra_strength_boulders[player].value)
    connect(world, player, "Fuchsia City", "Route 19", lambda state: state.pokemon_rb_can_surf(player))
    connect(world, player, "Route 20 East", "Route 19")
    connect(world, player, "Route 20 West", "Cinnabar Island", lambda state: state.pokemon_rb_can_surf(player))
    connect(world, player, "Route 20 West", "Seafoam Islands 1F")
    connect(world, player, "Route 20 East", "Seafoam Islands 1F", one_way=True)
    connect(world, player, "Seafoam Islands 1F", "Route 20 East", lambda state: state.pokemon_rb_can_strength(player), one_way=True)
    connect(world, player, "Viridian City", "Viridian City North", lambda state: state.has("Oak's Parcel", player) or state.multiworld.old_man[player].value == 2 or state.pokemon_rb_can_cut(player))
    connect(world, player, "Route 3", "Mt Moon 1F", one_way=True)
    connect(world, player, "Route 11", "Route 11 East", lambda state: state.pokemon_rb_can_strength(player))
    connect(world, player, "Cinnabar Island", "Cinnabar Gym", lambda state: state.has("Secret Key", player), one_way=True)
    connect(world, player, "Cinnabar Island", "Pokemon Mansion 1F", lambda state: state.has("Mansion Key", player) or not state.multiworld.extra_key_items[player].value, one_way=True)
    connect(world, player, "Seafoam Islands 1F", "Seafoam Islands B1F", one_way=True)
    connect(world, player, "Seafoam Islands B1F", "Seafoam Islands B2F", one_way=True)
    connect(world, player, "Seafoam Islands B2F", "Seafoam Islands B3F", one_way=True)
    connect(world, player, "Seafoam Islands B3F", "Seafoam Islands B4F", one_way=True)
    connect(world, player, "Route 21", "Cinnabar Island", lambda state: state.pokemon_rb_can_surf(player))
    connect(world, player, "Pallet Town", "Route 21", lambda state: state.pokemon_rb_can_surf(player))
    connect(world, player, "Saffron City", "Silph Co 1F", lambda state: state.has("Fuji Saved", player), one_way=True)
    connect(world, player, "Silph Co 1F", "Silph Co 2F", one_way=True)
    connect(world, player, "Silph Co 2F", "Silph Co 3F", one_way=True)
    connect(world, player, "Silph Co 3F", "Silph Co 4F", one_way=True)
    connect(world, player, "Silph Co 4F", "Silph Co 5F", one_way=True)
    connect(world, player, "Silph Co 5F", "Silph Co 6F", one_way=True)
    connect(world, player, "Silph Co 6F", "Silph Co 7F", one_way=True)
    connect(world, player, "Silph Co 7F", "Silph Co 8F", one_way=True)
    connect(world, player, "Silph Co 8F", "Silph Co 9F", one_way=True)
    connect(world, player, "Silph Co 9F", "Silph Co 10F", one_way=True)
    connect(world, player, "Silph Co 10F", "Silph Co 11F", one_way=True)
    connect(world, player, "Celadon City", "Rocket Hideout B1F", lambda state: state.has("Hideout Key", player) or not state.multiworld.extra_key_items[player].value, one_way=True)
    connect(world, player, "Rocket Hideout B1F", "Rocket Hideout B2F", one_way=True)
    connect(world, player, "Rocket Hideout B2F", "Rocket Hideout B3F", one_way=True)
    connect(world, player, "Rocket Hideout B3F", "Rocket Hideout B4F", one_way=True)
    connect(world, player, "Pokemon Mansion 1F", "Pokemon Mansion 2F", one_way=True)
    connect(world, player, "Pokemon Mansion 2F", "Pokemon Mansion 3F", one_way=True)
    connect(world, player, "Pokemon Mansion 1F", "Pokemon Mansion B1F", one_way=True)
    connect(world, player, "Route 23", "Victory Road 1F", lambda state: state.pokemon_rb_can_strength(player), one_way=True)
    connect(world, player, "Victory Road 1F", "Victory Road 2F", one_way=True)
    connect(world, player, "Victory Road 2F", "Victory Road 3F", one_way=True)
    connect(world, player, "Victory Road 2F", "Indigo Plateau", lambda state: state.pokemon_rb_has_badges(state.multiworld.elite_four_condition[player], player), one_way=True)
    connect(world, player, "Cerulean City", "Cerulean Cave 1F", lambda state:
            state.pokemon_rb_cerulean_cave(state.multiworld.cerulean_cave_condition[player].value + (state.multiworld.extra_key_items[player].value * 4), player) and
            state.pokemon_rb_can_surf(player), one_way=True)
    connect(world, player, "Cerulean Cave 1F", "Cerulean Cave 2F", one_way=True)
    connect(world, player, "Cerulean Cave 1F", "Cerulean Cave B1F", lambda state: state.pokemon_rb_can_surf(player), one_way=True)
    if world.worlds[player].fly_map != "Pallet Town":
        connect(world, player, "Menu", world.worlds[player].fly_map, lambda state: state.pokemon_rb_can_fly(player), one_way=True,
                name="Fly to " + world.worlds[player].fly_map)


def connect(world: MultiWorld, player: int, source: str, target: str, rule: callable = lambda state: True, one_way=False, name=None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if name is None:
        name = source + " to " + target

    connection = Entrance(
        player,
        name,
        source_region
    )

    connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
    if not one_way:
        connect(world, player, target, source, rule, True)
