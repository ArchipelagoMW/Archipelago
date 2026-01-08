from typing import TYPE_CHECKING

from .data import data
from .phone_data import get_shuffled_basic_calls, template_call_bike_shop, template_call_psychic, template_call_remote, \
    template_call_filler_hint

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld

PHONE_TRAP_COUNT = 32


def generate_phone_traps(world: "PokemonCrystalWorld"):
    bike_shop_location = world.multiworld.get_location(data.locations["BICYCLE"].label, world.player)
    if world.options.johto_only:
        psychic_location = None
    else:
        psychic_location = world.multiworld.get_location(data.locations["TM29_PSYCHIC"].label, world.player)
    remote_locs = []
    filler_location = None

    world_locations = list(world.multiworld.get_locations(world.player))
    world.random.shuffle(world_locations)

    for location in world_locations:
        if len(remote_locs) > 3 and filler_location is not None:
            break
        if (len(remote_locs) < 3 and location.address is not None and location.item
                and location.item.player != world.player):
            if location.item.advancement:
                remote_locs.append(location)
            if filler_location is None and not (location.item.advancement or location.item.useful):
                filler_location = location

    phone_traps_list = []
    if psychic_location is not None and world.random.random() < 0.75:
        phone_traps_list.append("psychic")
    if world.random.random() < 0.75:
        phone_traps_list.append("bike_shop")
    if filler_location and world.random.random() < 0.75:
        phone_traps_list.append("filler_hint")
    remote_count = min(len(remote_locs), 3)
    phone_traps_list.extend(["remote"] * remote_count)
    phone_traps_list.extend(["basic"] * (PHONE_TRAP_COUNT - len(phone_traps_list)))
    world.random.shuffle(phone_traps_list)

    basic_calls = get_shuffled_basic_calls(world.random, data.phone_scripts)

    location_call_indices = [0] * PHONE_TRAP_COUNT
    phone_traps = []
    for i, trap in enumerate(phone_traps_list):
        if trap == "basic":
            phone_traps.append(basic_calls.pop())
            continue
        if trap == "bike_shop":
            phone_traps.append(template_call_bike_shop(bike_shop_location))
            location_call_indices[i] = bike_shop_location.address
            continue
        if trap == "psychic":
            phone_traps.append(template_call_psychic())
            location_call_indices[i] = psychic_location.address
            continue
        if trap == "remote":
            remote_loc = remote_locs.pop()
            phone_traps.append(template_call_remote(remote_loc, world))
            location_call_indices[i] = remote_loc.address
            continue
        if trap == "filler_hint":
            phone_traps.append(template_call_filler_hint(filler_location, world))
            location_call_indices[i] = filler_location.address

    world.generated_phone_traps = phone_traps
    world.generated_phone_indices = location_call_indices
