from typing import TYPE_CHECKING, Callable

from BaseClasses import LocationProgressType, CollectionState

from ...locations import PokemonBWLocation

if TYPE_CHECKING:
    from ... import PokemonBWWorld
    from BaseClasses import Region
    from ...data import SpeciesData


def lookup(domain: int) -> dict[str, int]:
    from ...data.locations.dexsanity import location_table

    return {name: data.dex_number + domain for name, data in location_table.items()}


def create(world: "PokemonBWWorld", catchable_species_data: dict[str, "SpeciesData"]) -> None:
    from ...data.locations.dexsanity import location_table

    # These lambdas have to be created from functions, because else they would all use the same 'name' variable
    def get_standard_rule(x: str) -> Callable[[CollectionState], bool]:
        return lambda state: state.has(x.split(" - ")[-1], world.player)

    def get_special_rule(x: str) -> Callable[[CollectionState], bool]:
        return lambda state: location_table[x].special_rule(state, world)

    catchable_dex: dict[str, None] = {data.dex_name: None for data in catchable_species_data.values()}
    dexsanity_numbers: list[int] = []
    count = min(world.options.dexsanity.value, len(catchable_dex))
    possible = [f"Pokédex - {species}" for species in catchable_dex]
    world.random.shuffle(possible)

    for _ in range(count):
        name = possible.pop()  # location name
        data = location_table[name]
        dexsanity_numbers.append(data.dex_number)
        r: "Region" = world.regions["Pokédex"]
        l: PokemonBWLocation = PokemonBWLocation(world.player, name, world.location_name_to_id[name], r)
        l.progress_type = LocationProgressType.DEFAULT
        if data.special_rule is not None:
            l.access_rule = get_special_rule(name)
        else:
            l.access_rule = get_standard_rule(name)
        if data.ut_alias is not None:
            world.location_id_to_alias[world.location_name_to_id[name]] = data.ut_alias
        r.locations.append(l)

    world.dexsanity_numbers.extend(dexsanity_numbers)
