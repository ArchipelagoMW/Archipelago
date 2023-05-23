
from BaseClasses import MultiWorld, Region, Entrance, LocationProgressType, ItemClassification
from .items import item_table
from .locations import location_data, PokemonRBLocation
from .map_shuffle import warp_data, mandatory_connections, safe_rooms, safari_zone_houses, pokemon_centers,\
    pokemon_center_entrances, entrance_only, map_ids, insanity_safe_rooms, connecting_interiors
import worlds.pokemon_rb.poke_data as poke_data
from copy import deepcopy

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


def outdoor_map(name):
    i = map_ids[name.split("-")[0]]
    if i <= 0x24 or 0xD9 <= i <= 0xDC:
        return True
    return False

def create_regions(self):
    multiworld = self.multiworld
    player = self.player
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
                     state.pokemon_rb_has_badges(state.multiworld.viridian_gym_condition[player].value, player))
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
    connect(multiworld, player, "Pewter City", "Pewter City-E")
    connect(multiworld, player, "Pewter City-M", "Pewter City", one_way=True)
    connect(multiworld, player, "Pewter City", "Pewter City-M", lambda state: state.pokemon_rb_can_cut(player), one_way=True)
    connect(multiworld, player, "Pewter City-E", "Route 3", lambda state: state.has("Defeat Brock", player), one_way=True)
    connect(multiworld, player, "Route 3", "Pewter City-E", one_way=True)
    connect(multiworld, player, "Route 4-W", "Route 3")
    connect(multiworld, player, "Route 24", "Cerulean City-Water", one_way=True)
    connect(multiworld, player, "Cerulean City-Water", "Route 4-Lass", lambda state: state.pokemon_rb_can_surf(player), one_way=True)
    # connect(multiworld, player, "Mt Moon 1F", "Mt Moon B1F")
    # connect(multiworld, player, "Mt Moon B1F", "Mt Moon B2F")
    # connect(multiworld, player, "Mt Moon B2F", "Mt Moon B1F-Exit", one_way=True)
    # connect(multiworld, player, "Mt Moon B1F", "Route 4", one_way=True)
    connect(multiworld, player, "Mt Moon B2F", "Mt Moon B2F-Wild")
    connect(multiworld, player, "Mt Moon B2F-NE", "Mt Moon B2F-Wild")
    connect(multiworld, player, "Mt Moon B2F-C", "Mt Moon B2F-Wild")
    connect(multiworld, player, "Route 4-Lass", "Route 4-E", one_way=True)
    connect(multiworld, player, "Route 4-C", "Route 4-E", one_way=True)
    connect(multiworld, player, "Route 4-E", "Route 4-Grass", one_way=True)
    connect(multiworld, player, "Route 4-Grass", "Cerulean City", one_way=True)
    # connect(multiworld, player, "Cerulean City", "Cerulean Gym", one_way=True)
    connect(multiworld, player, "Cerulean City", "Route 24", one_way=True)
    connect(multiworld, player, "Cerulean City", "Cerulean City-T", lambda state: state.has("Visit Bill", player))
    connect(multiworld, player, "Cerulean City-Outskirts", "Cerulean City", one_way=True)
    connect(multiworld, player, "Cerulean City-Outskirts", "Cerulean City", lambda state: state.pokemon_rb_can_cut(player))
    connect(multiworld, player, "Cerulean City-Outskirts", "Route 9", lambda state: state.pokemon_rb_can_cut(player))
    connect(multiworld, player, "Cerulean City-Outskirts", "Route 5")
    connect(multiworld, player, "Cerulean Cave B1F", "Cerulean Cave B1F-E", lambda state: state.pokemon_rb_can_surf(player), one_way=True)
    connect(multiworld, player, "Route 24", "Route 25", one_way=True)
    connect(multiworld, player, "Route 9", "Route 10-N")
    connect(multiworld, player, "Route 10-N", "Route 10-C", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Route 10-C", "Route 10-P", lambda state: state.has("Plant Key", player) or not state.multiworld.extra_key_items[player].value)
    # connect(multiworld, player, "Route 10-P", "Route 10-C", one_way=True)
    connect(multiworld, player, "Pallet Town", "Pallet/Viridian Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Viridian City", "Pallet/Viridian Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 22", "Route 22 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 24", "Route 24/25/Cerulean/Cerulean Gym Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 25", "Route 24/25/Cerulean/Cerulean Gym Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean City", "Route 24/25/Cerulean/Cerulean Gym Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean Gym", "Route 24/25/Cerulean/Cerulean Gym Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 6", "Route 6/11/Vermilion/Dock Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 11", "Route 6/11/Vermilion/Dock Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Vermilion City", "Route 6/11/Vermilion/Dock Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Vermilion Dock", "Route 6/11/Vermilion/Dock Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 10-N", "Route 10/Celadon Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 10-C", "Route 10/Celadon Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Celadon City", "Route 10/Celadon Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone Center-NW", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone Center-NE", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone Center-S", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone West", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone West-NW", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone East", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Safari Zone North", "Safari Zone Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 12-N", "Route 12/13/17/18 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 12-S", "Route 12/13/17/18 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 13", "Route 12/13/17/18 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 13-E", "Route 12/13/17/18 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 17", "Route 12/13/17/18 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 18-W", "Route 12/13/17/18 Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 21", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cinnabar Island", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 20-IW", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 20-IE", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 19-N", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Seafoam Islands B3F", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Seafoam Islands B4F", "Sea Routes/Cinnabar/Seafoam Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 23-S", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Route 23-C", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-SE", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-NE", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-N", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-SW", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Cerulean Cave B1F", "Route 23/Cerulean Cave Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Fuchsia City", "Fuchsia Fishing", lambda state: state.has("Super Rod", player), one_way=True)
    connect(multiworld, player, "Pallet Town", "Old Rod Fishing", lambda state: state.has("Old Rod", player), one_way=True)
    connect(multiworld, player, "Pallet Town", "Good Rod Fishing", lambda state: state.has("Good Rod", player), one_way=True)
    connect(multiworld, player, "Cinnabar Lab Fossil Room", "Good Rod Fishing", one_way=True)
    connect(multiworld, player, "Cinnabar Lab Fossil Room", "Fossil Level", lambda state: state.pokemon_rb_fossil_checks(1, player), one_way=True)
    connect(multiworld, player, "Route 5 Gate-N", "Route 5 Gate-S", lambda state: state.pokemon_rb_can_pass_guards(player))
    connect(multiworld, player, "Route 6 Gate-N", "Route 6 Gate-S", lambda state: state.pokemon_rb_can_pass_guards(player))
    connect(multiworld, player, "Route 7 Gate-W", "Route 7 Gate-E", lambda state: state.pokemon_rb_can_pass_guards(player))
    connect(multiworld, player, "Route 8 Gate-W", "Route 8 Gate-E", lambda state: state.pokemon_rb_can_pass_guards(player))
    connect(multiworld, player, "Saffron City", "Route 5-S")
    connect(multiworld, player, "Saffron City", "Route 6-N")
    connect(multiworld, player, "Saffron City", "Route 7-E")
    connect(multiworld, player, "Saffron City", "Route 8-W")
    connect(multiworld, player, "Saffron City", "Saffron City-Copycat", lambda state: state.has("Silph Co Liberated", player))
    connect(multiworld, player, "Saffron City", "Saffron City-Pidgey", lambda state: state.has("Silph Co Liberated", player))
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
    connect(multiworld, player, "Route 18 Gate 1F-W", "Route 18 Gate 1F-E", lambda state: state.has("Bicycle", player))
    connect(multiworld, player, "Route 16 Gate 1F-W", "Route 16 Gate 1F-E", lambda state: state.has("Bicycle", player))
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
    connect(multiworld, player, "Route 14", "Route 15-N", lambda state: state.pokemon_rb_can_cut(player), one_way=True)
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
    connect(multiworld, player, "Safari Zone West-NW", "Safari Zone West", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Safari Zone West", "Safari Zone West-Wild", one_way=True)
    connect(multiworld, player, "Safari Zone West-NW", "Safari Zone West-Wild", one_way=True)
    connect(multiworld, player, "Safari Zone Center-NW", "Safari Zone Center-C", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Safari Zone Center-NE", "Safari Zone Center-C", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Safari Zone Center-S", "Safari Zone Center-C", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Safari Zone Center-S", "Safari Zone Center-Wild", one_way=True)
    connect(multiworld, player, "Safari Zone Center-NW", "Safari Zone Center-Wild", one_way=True)
    connect(multiworld, player, "Safari Zone Center-NE", "Safari Zone Center-Wild", one_way=True)

    connect(multiworld, player, "Victory Road 3F-S", "Victory Road 3F", lambda state: state.pokemon_rb_can_strength(player))
    connect(multiworld, player, "Victory Road 3F-SE", "Victory Road 3F-S", lambda state: state.pokemon_rb_can_strength(player), one_way=True)
    connect(multiworld, player, "Victory Road 3F", "Victory Road 3F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 3F-SE", "Victory Road 3F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 3F-S", "Victory Road 3F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 2F-W", "Victory Road 2F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 2F-NW", "Victory Road 2F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 2F-C", "Victory Road 2F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 2F-W", "Victory Road 2F-C", lambda state: state.pokemon_rb_can_strength(player), one_way=True)
    connect(multiworld, player, "Victory Road 2F-NW", "Victory Road 2F-W", lambda state: state.pokemon_rb_can_strength(player), one_way=True)
    connect(multiworld, player, "Victory Road 2F-C", "Victory Road 2F-SE", lambda state: state.pokemon_rb_can_strength(player) and state.has("Victory Road Boulder", player), one_way=True)
    connect(multiworld, player, "Victory Road 1F-S", "Victory Road 1F", lambda state: state.pokemon_rb_can_strength(player))
    connect(multiworld, player, "Victory Road 1F", "Victory Road 1F-Wild", one_way=True)
    connect(multiworld, player, "Victory Road 1F-S", "Victory Road 1F-Wild", one_way=True)
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
    connect(multiworld, player, "Seafoam Islands B2F-SE", "Seafoam Islands B2F-Wild", one_way=True)
    connect(multiworld, player, "Seafoam Islands B3F-SE", "Seafoam Islands B3F", lambda state: state.pokemon_rb_can_surf(player) and state.pokemon_rb_can_strength(player), one_way=True)

    connect(multiworld, player, "Viridian City", "Viridian City-N", lambda state: state.has("Oak's Parcel", player) or state.multiworld.old_man[player].value == 2 or state.pokemon_rb_can_cut(player))

    connect(multiworld, player, "Route 11", "Route 11-C", lambda state: state.pokemon_rb_can_strength(player) or not state.multiworld.extra_strength_boulders[player])
    connect(multiworld, player, "Cinnabar Island", "Cinnabar Island-G", lambda state: state.has("Secret Key", player) and state.pokemon_rb_cinnabar_gym(player))
    connect(multiworld, player, "Cinnabar Island", "Cinnabar Island-M", lambda state: state.has("Mansion Key", player) or not state.multiworld.extra_key_items[player].value)

    connect(multiworld, player, "Route 21", "Cinnabar Island", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Pallet Town", "Route 21", lambda state: state.pokemon_rb_can_surf(player))

    connect(multiworld, player, "Celadon Gym", "Celadon Gym-C", lambda state: state.pokemon_rb_can_cut(player), one_way=True)
    connect(multiworld, player, "Rocket Hideout B1F-SE", "Rocket Hideout B1F", one_way=True)

    connect(multiworld, player, "Indigo Plateau Lobby", "Indigo Plateau Lobby-N", lambda state: state.pokemon_rb_has_badges(state.multiworld.elite_four_condition[player], player))

    connect(multiworld, player, "Rock Tunnel 1F-S", "Rock Tunnel 1F-Wild", lambda state: state.pokemon_rb_rock_tunnel(player), one_way=True)
    connect(multiworld, player, "Rock Tunnel 1F-NW", "Rock Tunnel 1F-Wild", lambda state: state.pokemon_rb_rock_tunnel(player), one_way=True)
    connect(multiworld, player, "Rock Tunnel 1F-NE", "Rock Tunnel 1F-Wild", lambda state: state.pokemon_rb_rock_tunnel(player), one_way=True)
    connect(multiworld, player, "Rock Tunnel B1F-W", "Rock Tunnel B1F-Wild", lambda state: state.pokemon_rb_rock_tunnel(player), one_way=True)
    connect(multiworld, player, "Rock Tunnel B1F-E", "Rock Tunnel B1F-Wild", lambda state: state.pokemon_rb_rock_tunnel(player), one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-SE", "Cerulean Cave 1F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-SW", "Cerulean Cave 1F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-NE", "Cerulean Cave 1F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-N", "Cerulean Cave 1F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-NW", "Cerulean Cave 1F-Wild", one_way=True)
    connect(multiworld, player, "Cerulean Cave 1F-SE", "Cerulean Cave 1F-Water", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Cerulean Cave 1F-SW", "Cerulean Cave 1F-Water", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Cerulean Cave 1F-N", "Cerulean Cave 1F-Water", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Cerulean Cave 1F-NW", "Cerulean Cave 1F-Water", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Cerulean Cave 1F-NE", "Cerulean Cave 1F-Water", lambda state: state.pokemon_rb_can_surf(player))
    connect(multiworld, player, "Pokemon Mansion 3F", "Pokemon Mansion 3F-SE", one_way=True)
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
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-1F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-2F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-3F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-4F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-5F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-6F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-7F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-8F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-9F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-10F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Silph Co Elevator", "Silph Co Elevator-11F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Rocket Hideout Elevator", "Rocket Hideout Elevator-B1F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Rocket Hideout Elevator", "Rocket Hideout Elevator-B2F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Rocket Hideout Elevator", "Rocket Hideout Elevator-B4F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Celadon Pokemart Elevator", "Celadon Pokemart Elevator-1F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Celadon Pokemart Elevator", "Celadon Pokemart Elevator-2F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Celadon Pokemart Elevator", "Celadon Pokemart Elevator-3F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Celadon Pokemart Elevator", "Celadon Pokemart Elevator-4F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Celadon Pokemart Elevator", "Celadon Pokemart Elevator-5F", lambda state: state.has("Lift Key", player))
    connect(multiworld, player, "Route 23-N", "Indigo Plateau")
    connect(multiworld, player, "Cerulean City-Water", "Cerulean City-Cave", lambda state:
            state.pokemon_rb_cerulean_cave(state.multiworld.cerulean_cave_condition[player].value + (state.multiworld.extra_key_items[player].value * 4), player) and
            state.pokemon_rb_can_surf(player), one_way=True)

    # access to any part of a city will enable flying to the Pokemon Center!
    connect(multiworld, player, "Cerulean City-Cave", "Cerulean City", lambda state: state.pokemon_rb_can_fly(player), one_way=True)
    connect(multiworld, player, "Cerulean City-Badge House Backyard", "Cerulean City", lambda state: state.pokemon_rb_can_fly(player), one_way=True)
    connect(multiworld, player, "Fuchsia City-Good Rod House Backyard", "Fuchsia City", lambda state: state.pokemon_rb_can_fly(player), one_way=True)
    connect(multiworld, player, "Saffron City-G", "Saffron City", lambda state: state.pokemon_rb_can_fly(player), one_way=True)
    connect(multiworld, player, "Saffron City-Pidgey", "Saffron City", lambda state: state.pokemon_rb_can_fly(player), one_way=True)
    connect(multiworld, player, "Saffron City-Silph", "Saffron City", lambda state: state.pokemon_rb_can_fly(player), one_way=True)
    connect(multiworld, player, "Saffron City-Copycat", "Saffron City", lambda state: state.pokemon_rb_can_fly(player), one_way=True)
    connect(multiworld, player, "Celadon City-G", "Celadon City", lambda state: state.pokemon_rb_can_fly(player), one_way=True)
    connect(multiworld, player, "Vermilion City-G", "Vermilion City", lambda state: state.pokemon_rb_can_fly(player), one_way=True)
    connect(multiworld, player, "Vermilion City-Dock", "Vermilion City", lambda state: state.pokemon_rb_can_fly(player), one_way=True)


    # Drops
    connect(multiworld, player, "Seafoam Islands 1F", "Seafoam Islands B1F", one_way=True)
    connect(multiworld, player, "Seafoam Islands 1F", "Seafoam Islands B1F-NE", one_way=True)
    connect(multiworld, player, "Seafoam Islands B1F", "Seafoam Islands B2F-NW", one_way=True)
    connect(multiworld, player, "Seafoam Islands B1F-NE", "Seafoam Islands B2F-NE", one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-NW", "Seafoam Islands B2F-NW", one_way=True)
    connect(multiworld, player, "Seafoam Islands B2F-NE", "Seafoam Islands B2F-NE", one_way=True)
    connect(multiworld, player, "Seafoam Islands B3F", "Seafoam Islands B4F", one_way=True)
    connect(multiworld, player, "Pokemon Mansion 3F-SE", "Pokemon Mansion 2F", one_way=True)
    connect(multiworld, player, "Pokemon Mansion 3F-SE", "Pokemon Mansion 1F-SE", one_way=True)
    connect(multiworld, player, "Victory Road 3F-S", "Victory Road 2F-C", one_way=True)


    # connect(multiworld, player, "Cerulean Cave 1F", "Cerulean Cave 2F", one_way=True)
    # connect(multiworld, player, "Cerulean Cave 1F", "Cerulean Cave B1F", lambda state: state.pokemon_rb_can_surf(player), one_way=True)
    if multiworld.worlds[player].fly_map != "Pallet Town":
        connect(multiworld, player, "Menu", multiworld.worlds[player].fly_map, lambda state: state.pokemon_rb_can_fly(player), one_way=True,
                name="Fly to " + multiworld.worlds[player].fly_map)

    # for connection in connecting_interior_warps:
    #     connect(multiworld, player, connection[0], connection[1])
    entrances = []
    self.warp_data = deepcopy(warp_data)
    for region_name, region_entrances in warp_data.items():
        for entrance_data in region_entrances:
            region = self.multiworld.get_region(region_name, player)
            if not outdoor_map(region.name) and not outdoor_map(entrance_data['to']['map']) and True:
                connect(multiworld, player, region.name, entrance_data['to']['map'], one_way=True)
            else:
                entrance = PokemonRBWarp(player, f"{region.name} to {entrance_data['to']['map']}" if "name" not in
                                         entrance_data else entrance_data["name"], region, entrance_data["id"],
                                         entrance_data["address"], entrance_data["flags"] if "flags" in entrance_data
                                         else "")
                if "Rock Tunnel" in region:
                    entrance.access_rule = lambda state: state.pokemon_rb_rock_tunnel(player)
                entrances.append(entrance)
                region.exits.append(entrance)

    def dead_end(e):
        region = e.parent_region
        check_warps = set()
        checked_regions = {region}
        check_warps.update(region.exits)
        check_warps.remove(e)
        while check_warps:
            warp = list(check_warps)[0]
            check_warps.remove(warp)
            if warp.connected_region is None and warp.access_rule(state):
                if warp.connected_region is None:
                    return False
            elif not isinstance(warp, PokemonRBWarp) and warp.access_rule(state):
                if warp.connected_region not in checked_regions:
                    checked_regions.add(warp.connected_region)
                    check_warps.update(warp.connected_region.exits)
        return True

    # for entrance in entrances:
    #     if "m" in entrance.flags:
    #         entrance.connected_region = self.multiworld.get_region()
    if False:
        for region, region_entrances in warp_data.items():
            for entrance in region_entrances:
                if "Rock Tunnel" in region:
                    connect(multiworld, player, region, entrance["to"]["map"], lambda state: state.pokemon_rb_rock_tunnel(player))
                else:
                    connect(multiworld, player, region, entrance["to"]["map"])
    else:
        if True:
            loop_out_interiors = [[multiworld.get_entrance(e[0], player), multiworld.get_entrance(e[1], player)] for e
                                  in multiworld.random.sample(connecting_interiors, 2)]
            entrances.remove(loop_out_interiors[0][1])
            entrances.remove(loop_out_interiors[1][1])
        if not multiworld.badgesanity[player]:
            badges = []
            placed_locs = []
            for badge in ["Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Soul Badge",
                          "Marsh Badge", "Volcano Badge", "Earth Badge"]:
                badges.append(self.create_item(badge))
            for loc in ["Pewter Gym - Brock 1", "Cerulean Gym - Misty 1", "Vermilion Gym - Lt. Surge 1",
                        "Celadon Gym - Erika 1", "Fuchsia Gym - Koga 1", "Saffron Gym - Sabrina 1",
                        "Cinnabar Gym - Blaine 1", "Viridian Gym - Giovanni 1"]:
                placed_locs.append(self.multiworld.get_location(loc, self.player))
            multiworld.random.shuffle(badges)
            for badge, loc in zip(badges, placed_locs):
                loc.item = badge
                loc.event = True
        else:
            placed_locs = []

        for location in location_data:
            if location.event and location.type == "Item":
                loc = self.multiworld.get_location(location.name, player)
                loc.item = self.create_item(location.original_item)
                loc.event = True
                placed_locs.append(loc)

        state = multiworld.state.copy()
        for item, data in item_table.items():
            if (data.id or item in poke_data.pokemon_data) and data.classification == ItemClassification.progression \
                    and ("Badge" not in item or multiworld.badgesanity[player]):
                state.collect(self.create_item(item))

        forced_connections = mandatory_connections.copy()
        if False: #insanity
            forced_connections.extend(insanity_mandatory_connections)
        # # if True:
        # #     for region, region_entrances in warp_data.items():
        # #         if region in map_ids and map_ids[region.split("-")[0]] > 0x25:
        # #             for entrance in region_entrances:
        # #                 if map_ids[entrance["to"]["map"].split("-")[0]] > 0x25:
        # #                     l = [region + " to " + entrance["to"]["map"], entrance["to"]["map"] + " to " + region]
        # #                     l.sort()
        # #                     forced_connections.add(tuple(l))
        # for entrance in entrances:
        #     if map_ids[entrance.parent_region.name.split("-")[0]] >= 0x25:
        #

        usable_safe_rooms = safe_rooms.copy()
        if False:
            usable_safe_rooms += insanity_safe_rooms
        safe_rooms_sample = multiworld.random.sample(usable_safe_rooms, 6)
        for a, b in zip(multiworld.random.sample(["Pallet Town to Player's House 1F", "Pallet Town to Oak's Lab",
                                                  "Pallet Town to Rival's House"], 3), ["Oak's Lab to Pallet Town",
                                                  "Player's House 1F to Pallet Town", safe_rooms_sample.pop()]):
            forced_connections.add((a, b))
        for a, b in zip(safari_zone_houses, safe_rooms_sample):
            forced_connections.add((a, b))
        for a, b in zip(multiworld.random.sample(pokemon_center_entrances, 11), pokemon_centers):
            forced_connections.add((a, b))
        for pair in forced_connections:
            entrance_a = multiworld.get_entrance(pair[0], player)
            entrance_b = multiworld.get_entrance(pair[1], player)
            entrance_a.connect(entrance_b)
            entrance_b.connect(entrance_a)
            entrances.remove(entrance_a)
            entrances.remove(entrance_b)

        multiworld.random.shuffle(entrances)
        reachable_entrances = []
        while True:
            state.sweep_for_events()
            state.update_reachable_regions(player)
            reachable_entrances += [entrance for entrance in entrances if entrance.can_reach(state)]
            if not reachable_entrances:
                assert not entrances
                break
            reachable_entrances.sort(key=lambda e: e.name in entrance_only)
            entrances = [entrance for entrance in entrances if entrance not in reachable_entrances]
            entrance_a = reachable_entrances.pop()
            multiworld.random.shuffle(entrances)
            print(len(reachable_entrances))
            if entrances:
                entrances.sort(key=lambda e: e.name not in entrance_only)
                if len(reachable_entrances) < 2:  # this number seemed to create the best sphere distribution
                    entrances.sort(key=lambda e: not dead_end(e))
                else:
                    entrances.sort(key=lambda e: dead_end(e))
                if True:
                    if outdoor_map(entrance_a.parent_region.name):
                        entrances.sort(key=lambda e: not outdoor_map(e.parent_region.name))
                    else:
                        entrances.sort(key=lambda e: outdoor_map(e.parent_region.name))

                entrance_b = entrances.pop()
            else:
                entrance_b = multiworld.random.choice(reachable_entrances)
                reachable_entrances.remove(entrance_b)

            entrance_a.connect(entrance_b)
            entrance_b.connect(entrance_a)
            print(f"Connected {entrance_a.parent_region.name} to {entrance_b.parent_region.name}")

        for loc in placed_locs:
            loc.item = None
            loc.event = False

        for pair in loop_out_interiors:
            pair[1].connected_region = pair[0].connected_region
            pair[1].parent_region.entrances.append(pair[0])
            pair[1].target = pair[0].target



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


class PokemonRBWarp(Entrance):
    def __init__(self, player, name, parent, warp_id, address, flags):
        super().__init__(player, name, parent)
        self.warp_id = warp_id
        self.address = address
        self.flags = flags

    def connect(self, entrance):
        super().connect(entrance.parent_region, None, target=entrance.warp_id)