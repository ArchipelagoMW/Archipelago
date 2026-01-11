from typing import TYPE_CHECKING, Callable

from ...locations import PokemonBWLocation
from BaseClasses import ItemClassification, CollectionState
from ...items import PokemonBWItem

if TYPE_CHECKING:
    from ... import PokemonBWWorld
    from BaseClasses import Region
    from ...data import SpeciesData


def create(world: "PokemonBWWorld", catchable_species_data: dict[str, "SpeciesData"]) -> None:

    # Only some certain Pokémon because it's complicated and I didn't want to make this
    # Reasons for not doing...
    #   Castform and Cherrim: Having a reliable way to change weather is too complex
    #   Burmy: Checking for access to needed maps will become too complex for door shuffling
    #   Giratina: Requires Griseous Orb to be repeatedly obtainable, maybe I'll add that later
    #   Shaymin: Gracidea only works on fateful encounters
    #   Darmanitan: Requires repeatable access to Darmanitans with hidden ability
    #   Meloetta: Not possible in BW according to PokéWiki

    seasons = ("Spring", "Summer", "Autumn", "Winter")
    for pokemon in ("Deerling", "Sawsbuck"):
        forms = [f"{pokemon} ({season})" for season in seasons]
        if (
            any(form in catchable_species_data for form in forms) and
            world.options.season_control != "vanilla"
        ):
            region = world.regions["Nimbasa City"]
            for season in seasons:
                location = PokemonBWLocation(world.player, pokemon+" in "+season, None, region)
                item = PokemonBWItem(f"{pokemon} ({season})", ItemClassification.progression, None, world.player)
                location.place_locked_item(item)
                if world.options.season_control == "randomized":
                    location.access_rule = lambda state: (
                        state.has_any(forms, world.player) and
                        state.has(season, world.player)
                    )
                else:
                    location.access_rule = lambda state: state.has_any(forms, world.player)
                region.locations.append(location)

    rotom_machines = ("Heat", "Wash", "Frost", "Fan", "Mow", "Default")
    rotom_forms = (*(f"Rotom ({machine})" for machine in rotom_machines[:5]), "Rotom")
    if any(form in catchable_species_data for form in rotom_forms):
        region = world.regions["Route 9"]
        for form_num in range(6):
            location = PokemonBWLocation(world.player, "Change Rotom to "+rotom_machines[form_num], None, region)
            item = PokemonBWItem(rotom_forms[form_num], ItemClassification.progression, None, world.player)
            location.place_locked_item(item)
            location.access_rule = lambda state: state.has_any(rotom_forms, world.player)
            region.locations.append(location)

    deoxys_appends = ("Attack", "Defense", "Speed", "Default")
    deoxys_forms = (*(f"Deoxys ({append})" for append in deoxys_appends[:3]), "Deoxys")
    if any(form in catchable_species_data for form in deoxys_forms):
        region = world.regions["Nacrene City"]
        for form_num in range(4):
            location = PokemonBWLocation(world.player, "Change Deoxys to "+deoxys_appends[form_num], None, region)
            item = PokemonBWItem(deoxys_forms[form_num], ItemClassification.progression, None, world.player)
            location.place_locked_item(item)
            location.access_rule = lambda state: state.has_any(deoxys_forms, world.player)
            region.locations.append(location)

    # if "Shaymin" in catchable_species_data or "Shaymin (Sky)" in catchable_species_data:
    #     region = world.regions["Form Change"]
    #     location = PokemonBWLocation(world.player, "Change Shaymin to Sky", None, region)
    #     item = PokemonBWItem("Shaymin (Sky)", ItemClassification.progression, None, world.player)
    #     location.place_locked_item(item)
    #     location.access_rule = lambda state: state.has_all(("Shaymin", "Gracidea"), world.player)
    #     region.locations.append(location)
    #     location = PokemonBWLocation(world.player, "Change Shaymin to Land", None, region)
    #     item = PokemonBWItem("Shaymin", ItemClassification.progression, None, world.player)
    #     location.place_locked_item(item)
    #     location.access_rule = lambda state: state.has_all(("Shaymin (Sky)", "Gracidea"), world.player)
    #     region.locations.append(location)
