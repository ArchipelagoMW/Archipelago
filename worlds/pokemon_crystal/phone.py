import random
from typing import TYPE_CHECKING

from BaseClasses import ItemClassification
from .data import data
from .phone_data import get_shuffled_basic_calls, template_call_bike_shop, template_call_psychic, template_call_remote

if TYPE_CHECKING:
    from . import PokemonCrystalWorld
else:
    PokemonCrystalWorld = object


def generate_phone_traps(world: PokemonCrystalWorld):
    bike_shop_location = None
    psychic_location = None
    remote_progression_locs = []
    for location in world.multiworld.get_locations(world.player):
        if location.name == data.locations["BICYCLE"].label:
            # world.multiworld.worlds[world.player].game
            bike_shop_location = location
        elif location.name == data.locations["TM29_PSYCHIC"].label:
            psychic_location = location
        elif location.address is not None and location.item and location.item.player != world.player and location.item.classification == ItemClassification.progression:
            remote_progression_locs.append(location)

    remote_progression_spheres = []
    sphere_i = 0
    for sphere in world.multiworld.get_spheres():
        sphere_locations = []
        for location in remote_progression_locs:
            if location in sphere:
                sphere_locations += [location]
        remote_progression_spheres.append(sphere_locations)
        sphere_i += 1
    if not len(remote_progression_spheres[-2]):  # remove unplaced
        remote_progression_spheres = remote_progression_spheres[:-2]
    sphere_cutoff = int(len(remote_progression_spheres) * 0.66)

    remote_locs = []
    for sphere in remote_progression_spheres[sphere_cutoff:]:
        remote_locs += sphere
    world.random.shuffle(remote_locs)

    phone_traps_list = []
    if psychic_location is not None and world.random.random() < 0.75:
        phone_traps_list.append("psychic")
    if bike_shop_location is not None and world.random.random() < 0.75:
        phone_traps_list.append("bike_shop")
    remote_count = 3 if len(remote_locs) > 2 else len(remote_locs)
    phone_traps_list += ["remote"] * remote_count
    phone_traps_list += ["basic"] * (16 - len(phone_traps_list))
    random.shuffle(phone_traps_list)

    basic_calls = get_shuffled_basic_calls(world.random)

    location_call_indices = [0] * 16
    phone_traps = []
    for i, trap in enumerate(phone_traps_list):
        if trap == "basic":
            phone_traps += [basic_calls.pop()]
            continue
        if trap == "bike_shop":
            trap = template_call_bike_shop(bike_shop_location)
            phone_traps += [trap]
            location_call_indices[i] = bike_shop_location.address
            continue
        if trap == "psychic":
            trap = template_call_psychic()
            phone_traps += [trap]
            location_call_indices[i] = psychic_location.address
            continue
        if trap == "remote":
            remote_loc = remote_locs.pop()
            trap = template_call_remote(remote_loc, world)
            phone_traps += [trap]
            location_call_indices[i] = remote_loc.address

    return phone_traps, location_call_indices
