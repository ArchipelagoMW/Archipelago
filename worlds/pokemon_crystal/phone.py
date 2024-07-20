from typing import TYPE_CHECKING

from BaseClasses import ItemClassification
from .data import data
from .phone_data import get_shuffled_basic_calls, template_call_bike_shop, template_call_psychic, template_call_remote

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def generate_phone_traps(world: "PokemonCrystalWorld"):
    if world.options.phone_trap_weight.value:
        bike_shop_location = world.multiworld.get_location(data.locations["BICYCLE"].label, world.player)
        if world.options.johto_only:
            psychic_location = None
        else:
            psychic_location = world.multiworld.get_location(data.locations["TM29_PSYCHIC"].label, world.player)
        remote_locs = []
        for location in world.multiworld.get_locations(world.player):
            if len(remote_locs) > 3:
                break
            if (location.address is not None and location.item and location.item.player != world.player
                    and location.item.classification == ItemClassification.progression):
                remote_locs.append(location)

        phone_traps_list = []
        if psychic_location is not None and world.random.random() < 0.75:
            phone_traps_list.append("psychic")
        if world.random.random() < 0.75:
            phone_traps_list.append("bike_shop")
        remote_count = min(len(remote_locs), 3)
        phone_traps_list += ["remote"] * remote_count
        phone_traps_list += ["basic"] * (16 - len(phone_traps_list))
        world.random.shuffle(phone_traps_list)

        basic_calls = get_shuffled_basic_calls(world.random)

    location_call_indices = [0] * 16
    phone_traps = []
    for i, trap in enumerate(phone_traps_list):
        if trap == "basic":
            phone_traps += [basic_calls.pop()]
            continue
        if trap == "bike_shop":
            phone_traps += [template_call_bike_shop(bike_shop_location)]
            location_call_indices[i] = bike_shop_location.address
            continue
        if trap == "psychic":
            phone_traps += [template_call_psychic()]
            location_call_indices[i] = psychic_location.address
            continue
        if trap == "remote":
            remote_loc = remote_locs.pop()
            phone_traps += [template_call_remote(remote_loc, world)]
            location_call_indices[i] = remote_loc.address

    world.generated_phone_traps = phone_traps
    world.generated_phone_indices = location_call_indices
