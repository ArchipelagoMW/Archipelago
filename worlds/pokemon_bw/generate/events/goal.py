from typing import TYPE_CHECKING

from ...locations import PokemonBWLocation
from BaseClasses import ItemClassification
from ...items import PokemonBWItem

if TYPE_CHECKING:
    from ... import PokemonBWWorld


def create(world: "PokemonBWWorld") -> None:

    location: PokemonBWLocation
    regions = world.regions
    match world.options.goal.current_key:
        case "ghetsis":
            location = PokemonBWLocation(world.player, "Defeat Ghetsis", None, regions["N's Castle"])
            regions["N's Castle"].locations.append(location)
        case "champion":
            location = PokemonBWLocation(world.player, "Defeat Alder", None, regions["Pokémon League"])
            regions["Pokémon League"].locations.append(location)
        case "cynthia":
            location = PokemonBWLocation(world.player, "Defeat Cynthia", None, regions["Undella Town"])
            regions["Undella Town"].locations.append(location)
        case "cobalion":
            location = PokemonBWLocation(world.player, "Defeat or catch Cobalion", None, regions["Mistralton Cave Inner"])
            regions["Mistralton Cave Inner"].locations.append(location)
        # case "regional_pokedex":
        # case "national_pokedex":
        # case "custom_pokedex":
        case "tmhm_hunt":
            from ...data.items.tm_hm import tm as tm_items, hm as hm_items
            location = PokemonBWLocation(world.player, "Verify TMs/HMs", None, regions["Castelia City"])
            regions["Castelia City"].locations.append(location)
            location.access_rule = lambda state: state.has_all(tm_items, world.player) and state.has_all(hm_items, world.player)
        case "seven_sages_hunt":
            location = PokemonBWLocation(world.player, "Find all seven sages", None, regions["N's Castle"])
            regions["N's Castle"].locations.append(location)
            location.access_rule = lambda state: (
                # Finding Ghetsis is checked by setting N's Castle as the region
                state.can_reach_location("Route 18 - TM from sage Rood", world.player) and
                state.can_reach_location("Dreamyard - TM from sage Gorm", world.player) and
                state.can_reach_location("Relic Castle - TM from sage Ryoku", world.player) and
                state.can_reach_location("Cold Storage - TM from sage Zinzolin", world.player) and
                state.can_reach_location("Chargestone Cave - TM from sage Bronius", world.player) and
                state.can_reach_location("Route 14 - TM from sage Giallo", world.player)
            )
        case "legendary_hunt":
            location = PokemonBWLocation(world.player, "Defeat or catch all legendaries", None, regions["N's Castle"])
            regions["N's Castle"].locations.append(location)
            location.access_rule = lambda state: (
                state.can_reach_region("Mistralton Cave Inner", world.player) and
                state.can_reach_region("Trial Chamber", world.player) and
                state.can_reach_region("Giant Chasm Inner Cave", world.player) and
                state.can_reach_region("Liberty Garden", world.player) and
                state.can_reach_region("Relic Castle Basement", world.player)
            )
        case "pokemon_master":
            from ...data.items.tm_hm import tm, hm
            # N's Castle includes Ghetsis and Champion
            location = PokemonBWLocation(world.player, "Become the very best like no one ever was", None, regions["N's Castle"])
            regions["N's Castle"].locations.append(location)
            location.access_rule = lambda state: (
                # Legendary hunt, including Cobalion
                state.can_reach_region("Mistralton Cave Inner", world.player) and
                state.can_reach_region("Trial Chamber", world.player) and
                state.can_reach_region("Giant Chasm Inner Cave", world.player) and
                state.can_reach_region("Liberty Garden", world.player) and
                state.can_reach_region("Relic Castle Basement", world.player) and
                # Cynthia
                state.can_reach_region("Undella Town", world.player) and
                # TM/HM hunt
                state.has_all(tm, world.player) and
                state.has_all(hm, world.player) and
                # Seven sages hunt
                state.can_reach_location("Route 18 - TM from sage Rood", world.player) and
                state.can_reach_location("Dreamyard - TM from sage Gorm", world.player) and
                state.can_reach_location("Relic Castle - TM from sage Ryoku", world.player) and
                state.can_reach_location("Cold Storage - TM from sage Zinzolin", world.player) and
                state.can_reach_location("Chargestone Cave - TM from sage Bronius", world.player) and
                state.can_reach_location("Route 14 - TM from sage Giallo", world.player)
            )
        case _:
            raise Exception(f"Bad goal option: {world.options.goal.current_key}")
    item: PokemonBWItem = PokemonBWItem("Goal", ItemClassification.progression, None, world.player)
    location.place_locked_item(item)
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Goal", world.player)
