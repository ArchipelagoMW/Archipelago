
from BaseClasses import MultiWorld, Region, Entrance, LocationProgressType
from .locations import location_data, PokemonRBLocation
from .map_shuffle import warp_data


def create_region(world: MultiWorld, player: int, name: str, locations_per_region=None, exits=None):
    ret = Region(name, player, world)
    for location in locations_per_region.get(name, []):
        location.parent_region = ret
        ret.locations.append(location)
        if world.randomize_hidden_items[player] == "exclude" and "Hidden" in location.name:
            location.progress_type = LocationProgressType.EXCLUDED
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))
    locations_per_region[name] = []
    return ret


def create_regions(multiworld: MultiWorld, player: int):
    locations_per_region = {}
    for location in location_data:
        locations_per_region.setdefault(location.region, [])
        if location.inclusion(multiworld, player):
            locations_per_region[location.region].append(PokemonRBLocation(player, location.name, location.address,
                                                                           location.rom_address, location.type,
                                                                           location.level))

    regions = [create_region(multiworld, player, region, locations_per_region) for region in warp_data]
    multiworld.regions += regions
    if __debug__:
        for region in locations_per_region:
            assert not locations_per_region[region], f"locations not assigned to region {region}"
    connect(multiworld, player, "Menu", "Anywhere", one_way=True)
    connect(multiworld, player, "Menu", "Pallet Town", one_way=True)
    connect(multiworld, player, "Menu", "Pokedex", one_way=True)
    connect(multiworld, player, "Menu", "Fossil", lambda state: state.pokemon_rb_fossil_checks(
        state.multiworld.second_fossil_check_condition[player].value, player), one_way=True)
    connect(multiworld, player, "Pallet Town", "Route 1")
    connect(multiworld, player, "Route 1", "Viridian City")
    connect(multiworld, player, "Viridian City", "Route 22")
    connect(multiworld, player, "Route 2-SW", "Route 2-Grass", one_way=True)
    connect(multiworld, player, "Route 2-NW", "Route 2-Grass", one_way=True)
    connect(multiworld, player, "Route 22 Gate-S", "Route 22 Gate-N",
            lambda state: state.pokemon_rb_has_badges(state.multiworld.victory_road_condition[player].value, player))
    connect(multiworld, player, "Route 23-S", "Route 23-C",
            lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Viridian City-N", "Viridian City-G", lambda state:
                     state.pokemon_rb_has_badges(state.multiworld.viridian_gym_condition[player].value, player), one_way=True)
    connect(multiworld, player, "Viridian City-G", "Viridian City-N", one_way=True)
    connect(multiworld, player, "Route 2-SW", "Route 2-SE", lambda state: state.pokemon_rb_can_cut(player))
    # connect(multiworld, player, "Route 2 Northeast", "Diglett's Cave")
    # connect(multiworld, player, "Route 2 Southeast", "Route 2 Gate")
    # connect(multiworld, player, "Route 2 Northeast", "Route 2 Gate")
    connect(multiworld, player, "Route 2-NW", "Route 2-NE", lambda state: state.pokemon_rb_can_cut(player))
    connect(multiworld, player, "Route 2-SW", "Viridian City-N")
    # connect(multiworld, player, "Route 2 South", "Viridian Forest")
    # connect(multiworld, player, "Route 2 North", "Viridian Forest")
    connect(multiworld, player, "Route 2-NW", "Pewter City")
    # connect(multiworld, player, "Pewter City", "Pewter Gym", one_way=True)
    connect(multiworld, player, "Pewter City", "Route 3")
    connect(multiworld, player, "Route 4-W", "Route 3")
    connect(multiworld, player, "Route 24", "Cerulean City-Water", one_way=True)
    connect(multiworld, player, "Cerulean City-Water", "Route 4-Lass", lambda state: state.pokemon_rb_can_surf(player), one_way=True)
    # connect(multiworld, player, "Mt Moon 1F", "Mt Moon B1F")
    # connect(multiworld, player, "Mt Moon B1F", "Mt Moon B2F")
    # connect(multiworld, player, "Mt Moon B2F", "Mt Moon B1F-Exit", one_way=True)
    # connect(multiworld, player, "Mt Moon B1F", "Route 4", one_way=True)
    connect(multiworld, player, "Route 4-E", "Cerulean City")
    # connect(multiworld, player, "Cerulean City", "Cerulean Gym", one_way=True)
    connect(multiworld, player, "Cerulean City", "Route 24", one_way=True)
    connect(multiworld, player, "Cerulean City-Outskirts", "Route 9", lambda state: state.pokemon_rb_can_cut(player))
    connect(multiworld, player, "Cerulean City-Outskirts", "Route 5")
    connect(multiworld, player, "Route 24", "Route 25", one_way=True)
    connect(multiworld, player, "Route 9", "Route 10-N")
    connect(multiworld, player, "Route 10-N", "Route 10-C", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Route 10-N", "Route 10-P", lambda state: state.has("Plant Key", player) or not state.multiworld.extra_key_items[player].value, one_way=True)
    connect(multiworld, player, "Route 10-P", "Route 10-C", one_way=True)

    connect(multiworld, player, "Route 5 Gate-N", "Route 5 Gate-S", lambda state: state.pokemon_rb_can_pass_guards(player))
    connect(multiworld, player, "Route 6 Gate-N", "Route 6 Gate-S", lambda state: state.pokemon_rb_can_pass_guards(player))
    connect(multiworld, player, "Route 7 Gate-W", "Route 7 Gate-E", lambda state: state.pokemon_rb_can_pass_guards(player))
    connect(multiworld, player, "Route 8 Gate-W", "Route 8 Gate-E", lambda state: state.pokemon_rb_can_pass_guards(player))
    connect(multiworld, player, "Saffron City", "Route 5-S")
    connect(multiworld, player, "Saffron City", "Route 6-N")
    connect(multiworld, player, "Saffron City", "Route 7-E")
    connect(multiworld, player, "Saffron City", "Route 8-W")
    connect(multiworld, player, "Saffron City", "Saffron City-Copycat", lambda state: state.has("Silph Co Liberated", player))
    connect(multiworld, player, "Saffron City", "Saffron City-G", lambda state: state.has("Silph Co Liberated", player))
    connect(multiworld, player, "Saffron City", "Saffron City-Silph", lambda state: state.has("Fuji Saved", player))
    connect(multiworld, player, "Route 6", "Vermilion City")
    connect(multiworld, player, "Vermilion City", "Vermilion City-G", lambda state: state.pokemon_rb_can_surf(player) or state.pokemon_rb_can_cut(player))
    connect(multiworld, player, "Vermilion City", "Vermilion City-Dock", lambda state: state.has("S.S. Ticket", player))
    # connect(multiworld, player, "S.S. Anne 1F", "S.S. Anne 2F", one_way=True)
    # connect(multiworld, player, "S.S. Anne 2F", "S.S. Anne 3F", one_way=True)
    # connect(multiworld, player, "S.S. Anne 1F", "S.S. Anne B1F", one_way=True)
    connect(multiworld, player, "Vermilion City", "Route 11")
    # connect(multiworld, player, "Route 11", "Diglett's Cave")
    # connect(multiworld, player, "Route 12 West", "Route 11 East", lambda state: state.pokemon_rb_can_strength(player) or not state.multiworld.extra_strength_boulders[player].value)
    connect(multiworld, player, "Route 12-N", "Route 12-S", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Route 12-W", "Route 11-E", lambda state: state.has("Poke Flute", player))
    connect(multiworld, player, "Route 12-W", "Route 12-N", lambda state: state.has("Poke Flute", player))
    connect(multiworld, player, "Route 12-W", "Route 12-S", lambda state: state.has("Poke Flute", player))
    connect(multiworld, player, "Route 12-S", "Route 12-Grass", lambda state: state.pokemon_rb_can_cut(player), one_way=True)
    connect(multiworld, player, "Route 12-L", "Lavender Town")
    connect(multiworld, player, "Route 10-S", "Lavender Town")
    connect(multiworld, player, "Route 8-W", "Saffron City")
    connect(multiworld, player, "Route 8", "Lavender Town")
    connect(multiworld, player, "Route 8", "Route 8-Grass", lambda state: state.pokemon_rb_can_cut(player), one_way=True)
    connect(multiworld, player, "Route 7", "Celadon City")
    connect(multiworld, player, "Celadon City", "Celadon City-G", lambda state: state.pokemon_rb_can_cut(player))
    connect(multiworld, player, "Celadon City", "Route 16-E")
    connect(multiworld, player, "Route 16-E", "Route 16-NE", lambda state: state.pokemon_rb_can_cut(player))
    connect(multiworld, player, "Route 16-E", "Route 16-C", lambda state: state.has("Poke Flute", player))
    connect(multiworld, player, "Route 17", "Route 16-SW")
    connect(multiworld, player, "Route 17", "Route 18-W")
    connect(multiworld, player, "Pokemon Mansion 2F", "Pokemon Mansion 2F-NW", one_way=True)
    connect(multiworld, player, "Safari Zone Gate-S", "Safari Zone Gate-N", lambda state: state.has("Safari Pass", player) or not state.multiworld.extra_key_items[player].value, one_way=True)
    # connect(multiworld, player, "Safari Zone Center", "Safari Zone East", one_way=True)
    # connect(multiworld, player, "Safari Zone Center", "Safari Zone West", one_way=True)
    # connect(multiworld, player, "Safari Zone Center", "Safari Zone North", one_way=True)
    connect(multiworld, player, "Fuchsia City", "Route 15-W")
    connect(multiworld, player, "Route 15", "Route 14")
    connect(multiworld, player, "Route 14", "Route 14-Grass", lambda state: state.pokemon_rb_can_cut(player), one_way=True)
    connect(multiworld, player, "Route 14", "Route 13")
    connect(multiworld, player, "Route 13", "Route 13-E", lambda state: state.pokemon_rb_can_strength(player) or state.pokemon_rb_can_surf(player) or not state.multiworld.extra_strength_boulders[player].value)
    connect(multiworld, player, "Route 12-S", "Route 13-E")
    connect(multiworld, player, "Fuchsia City", "Route 19-N")
    connect(multiworld, player, "Route 19-N", "Route 19-S", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Route 20-E", "Route 20-IE", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Route 20-E", "Route 19-S")
    connect(multiworld, player, "Route 20-W", "Cinnabar Island", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Route 20-IW", "Route 20-W", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Route 20-E", "Route 20-Water", one_way=True)
    connect(multiworld, player, "Route 20-W", "Route 20-Water", one_way=True)
    connect(multiworld, player, "Mt Moon B1F-W", "Mt Moon B1F-Wild", one_way=True)
    connect(multiworld, player, "Mt Moon B1F-C", "Mt Moon B1F-Wild", one_way=True)
    connect(multiworld, player, "Mt Moon B1F-NE", "Mt Moon B1F-Wild", one_way=True)
    connect(multiworld, player, "Mt Moon B1F-SE", "Mt Moon B1F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 2F-N", "Cerulean Cave 2F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 2F-E", "Cerulean Cave 2F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 2F-W", "Cerulean Cave 2F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-NW", "Seafoam Islands B2F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-NE", "Seafoam Islands B2F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-SW", "Seafoam Islands B2F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-NE", "Seafoam Islands B2F-Wild", one_way=True)
    # connect(multiworld, player, "Route 20 West", "Seafoam Islands 1F")
    # connect(multiworld, player, "Route 20 East", "Seafoam Islands 1F", one_way=True)
    # connect(multiworld, player, "Seafoam Islands 1F", "Route 20-East", lambda state: state.pokemon_rb_can_strength(player), one_way=True)
    connect(multiworld, player, "Viridian City", "Viridian City-N", lambda state: state.has("Oak's Parcel", player) or state.multiworld.old_man[player].value == 2 or state.pokemon_rb_can_cut(player))
    # connect(multiworld, player, "Route 3", "Mt Moon 1F", one_way=True)
    connect(multiworld, player, "Route 11", "Route 11-C", lambda state: state.pokemon_rb_can_strength(player) or not state.multiworld.extra_strength_boulders[player])
    connect(multiworld, player, "Cinnabar Island", "Cinnabar Island-G", lambda state: state.has("Secret Key", player) and state.pokemon_rb_cinnabar_gym(player), one_way=True)
    connect(multiworld, player, "Cinnabar Island", "Cinnabar Island-M", lambda state: state.has("Mansion Key", player) or not state.multiworld.extra_key_items[player].value, one_way=True)
    # connect(multiworld, player, "Seafoam Islands 1F", "Seafoam Islands B1F", one_way=True)
    # connect(multiworld, player, "Seafoam Islands B1F", "Seafoam Islands B2F", one_way=True)
    # connect(multiworld, player, "Seafoam Islands B2F", "Seafoam Islands B3F", one_way=True)
    # connect(multiworld, player, "Seafoam Islands B3F", "Seafoam Islands B4F", one_way=True)
    # connect(multiworld, player, "Seafoam Islands B4F", "Seafoam Islands Exit", lambda state: state.pokemon_rb_can_strength(player), one_way=True)
    connect(multiworld, player, "Route 21", "Cinnabar Island", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Pallet Town", "Route 21", lambda state: state.pokemon_rb_can_surf(player))
    # connect(multiworld, player, "Saffron City", "Silph Co 1F", lambda state: state.has("Fuji Saved", player), one_way=True)
    # connect(multiworld, player, "Silph Co 1F", "Silph Co 2F", one_way=True)
    # connect(multiworld, player, "Silph Co 2F", "Silph Co 3F", one_way=True)
    # connect(multiworld, player, "Silph Co 3F", "Silph Co 4F", one_way=True)
    # connect(multiworld, player, "Silph Co 4F", "Silph Co 5F", one_way=True)
    # connect(multiworld, player, "Silph Co 5F", "Silph Co 6F", one_way=True)
    # connect(multiworld, player, "Silph Co 6F", "Silph Co 7F", one_way=True)
    # connect(multiworld, player, "Silph Co 7F", "Silph Co 8F", one_way=True)
    # connect(multiworld, player, "Silph Co 8F", "Silph Co 9F", one_way=True)
    # connect(multiworld, player, "Silph Co 9F", "Silph Co 10F", one_way=True)
    # connect(multiworld, player, "Silph Co 10F", "Silph Co 11F", one_way=True)
    # connect(multiworld, player, "Celadon City", "Rocket Hideout B1F", lambda state: state.has("Hideout Key", player) or not state.multiworld.extra_key_items[player].value, one_way=True)
    # connect(multiworld, player, "Rocket Hideout B1F", "Rocket Hideout B2F", one_way=True)
    # connect(multiworld, player, "Rocket Hideout B2F", "Rocket Hideout B3F", one_way=True)
    # connect(multiworld, player, "Rocket Hideout B3F", "Rocket Hideout B4F", one_way=True)
    # connect(multiworld, player, "Pokemon Mansion 1F", "Pokemon Mansion 2F", one_way=True)
    # connect(multiworld, player, "Pokemon Mansion 2F", "Pokemon Mansion 3F", one_way=True)
    # connect(multiworld, player, "Pokemon Mansion 1F", "Pokemon Mansion B1F", one_way=True)
    # # connect(multiworld, player, "Route 23", "Victory Road 1F", lambda state: state.pokemon_rb_can_strength(player), one_way=True)
    # connect(multiworld, player, "Victory Road 1F", "Victory Road 2F", one_way=True)
    # connect(multiworld, player, "Victory Road 2F", "Victory Road 3F", one_way=True)
    connect(multiworld, player, "Silph Co 2F", "Silph Co 2F-NW", lambda state: state.pokemon_rb_card_key(2, player))
    connect(multiworld, player, "Silph Co 2F", "Silph Co 2F-SW", lambda state: state.pokemon_rb_card_key(2, player))
    connect(multiworld, player, "Silph Co 3F", "Silph Co 3F-C", lambda state: state.pokemon_rb_card_key(3, player))
    connect(multiworld, player, "Silph Co 3F-W", "Silph Co 3F-C", lambda state: state.pokemon_rb_card_key(3, player))
    connect(multiworld, player, "Silph Co 4F", "Silph Co 4F-N", lambda state: state.pokemon_rb_card_key(4, player))
    connect(multiworld, player, "Silph Co 4F", "Silph Co 4F-W", lambda state: state.pokemon_rb_card_key(4, player))
    connect(multiworld, player, "Silph Co 5F", "Silph Co 5F-NW", lambda state: state.pokemon_rb_card_key(5, player))
    connect(multiworld, player, "Silph Co 5F", "Silph Co 5F-SW", lambda state: state.pokemon_rb_card_key(5, player))
    connect(multiworld, player, "Silph Co 6F", "Silph Co 6F-SW", lambda state: state.pokemon_rb_card_key(6, player))
    connect(multiworld, player, "Silph Co 7F", "Silph Co 7F-E", lambda state: state.pokemon_rb_card_key(7, player))
    connect(multiworld, player, "Silph Co 7F-SE", "Silph Co 7F-E", lambda state: state.pokemon_rb_card_key(7, player))
    connect(multiworld, player, "Silph Co 8F", "Silph Co 8F-W", lambda state: state.pokemon_rb_card_key(8, player))
    connect(multiworld, player, "Silph Co 9F", "Silph Co 9F-SW", lambda state: state.pokemon_rb_card_key(9, player))
    connect(multiworld, player, "Silph Co 9F-NW", "Silph Co 9F-SW", lambda state: state.pokemon_rb_card_key(9, player))
    connect(multiworld, player, "Silph Co 10F", "Silph Co 10F-SE", lambda state: state.pokemon_rb_card_key(10, player))
    connect(multiworld, player, "Silph Co 11F-W", "Silph Co 11F-C", lambda state: state.pokemon_rb_card_key(11, player))
    connect(multiworld, player, "Route 23-N", "Indigo Plateau", lambda state: state.pokemon_rb_has_badges(state.multiworld.elite_four_condition[player], player), one_way=True)
    connect(multiworld, player, "Cerulean City-Water", "Cerulean City-Cave", lambda state:
            state.pokemon_rb_cerulean_cave(state.multiworld.cerulean_cave_condition[player].value + (state.multiworld.extra_key_items[player].value * 4), player) and
            state.pokemon_rb_can_surf(player), one_way=True)
    # connect(multiworld, player, "Cerulean Cave 1F", "Cerulean Cave 2F", one_way=True)
    # connect(multiworld, player, "Cerulean Cave 1F", "Cerulean Cave B1F", lambda state: state.pokemon_rb_can_surf(player), one_way=True)
    if multiworld.worlds[player].fly_map != "Pallet Town":
        connect(multiworld, player, "Menu", multiworld.worlds[player].fly_map, lambda state: state.pokemon_rb_can_fly(player), one_way=True,
                name="Fly to " + multiworld.worlds[player].fly_map)

    # for connection in connecting_interior_warps:
    #     connect(multiworld, player, connection[0], connection[1])
    for region, entrances in warp_data.items():
        for entrance in entrances:
            connect(multiworld, player, region, entrance["to"]["map"])


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
