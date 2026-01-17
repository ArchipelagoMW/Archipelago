import logging
from collections.abc import Iterable
from typing import TYPE_CHECKING

from Options import Toggle
from .data import data, StartingTown, FlyRegion, RegionData
from .mart_data import CUSTOM_MART_SLOT_NAMES
from .options import FreeFlyLocation, Route32Condition, JohtoOnly, RandomizeBadges, UndergroundsRequirePower, \
    Route3Access, EliteFourRequirement, Goal, Route44AccessRequirement, BlackthornDarkCaveAccess, RedRequirement, \
    MtSilverRequirement, HMBadgeRequirements, RedGyaradosAccess, EarlyFly, RadioTowerRequirement, \
    BreedingMethodsRequired, Shopsanity, KantoTrainersanity, JohtoTrainersanity, RandomizePokemonRequests, \
    EnhancedOptionSet, RandomizeTypes, RandomizeEvolution, RandomizeTrades, TradesRequired, MagnetTrainAccess
from ..Files import APTokenTypes

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


def adjust_options(world: "PokemonCrystalWorld"):
    __adjust_meta_options(world)
    __adjust_option_problems(world)


def __adjust_meta_options(world: "PokemonCrystalWorld"):
    for option_name in dir(world.options):
        option = getattr(world.options, option_name)
        if isinstance(option, EnhancedOptionSet):
            if "_Random" in option.value:
                option.value.remove("_Random")
                for value in [opt for opt in option.valid_keys if not opt.startswith("_")]:
                    if value not in option.value and world.random.randint(0, 1):
                        option.value.add(value)


def __adjust_option_problems(world: "PokemonCrystalWorld"):
    __adjust_options_radio_tower_and_route_44(world)
    __adjust_options_victory_road_badges(world)
    __adjust_options_johto_only(world)
    __adjust_options_restrictive_region_travel(world)
    __adjust_options_gyarados(world)
    __adjust_options_early_fly(world)
    __adjust_options_encounters_and_breeding(world)
    __adjust_options_race_mode(world)
    __adjust_options_pokemon_requests(world)
    __adjust_options_trades(world)
    __adjust_options_dark_areas(world)
    __adjust_options_randomize_types(world)
    __adjust_options_tm_plando(world)
    __adjust_options_traps(world)
    __adjust_options_mischief_bounds(world)


def __adjust_options_radio_tower_and_route_44(world: "PokemonCrystalWorld"):
    if (world.options.randomize_badges.value != RandomizeBadges.option_completely_random
            and world.options.radio_tower_count.value > (7 if world.options.johto_only else 15)):
        world.options.radio_tower_count.value = 7 if world.options.johto_only else 15
        logging.warning(
            "Pokemon Crystal: Radio Tower Count >%d incompatible with vanilla or shuffled badges. "
            "Changing Radio Tower Count to %d for player %s.",
            world.options.radio_tower_count.value,
            world.options.radio_tower_count.value,
            world.player_name)

    if (world.options.route_44_access_count.value > (7 if world.options.johto_only else 15)
            and world.options.randomize_badges.value != RandomizeBadges.option_completely_random):
        world.options.route_44_access_count.value = 7 if world.options.johto_only else 15
        logging.warning(
            "Pokemon Crystal: Route 44 Access Count >%d incompatible with vanilla or shuffled badges. "
            "Changing Route 44 Access Count to %d for player %s.",
            world.options.route_44_access_count.value,
            world.options.route_44_access_count.value,
            world.player_name)

    if (world.options.route_44_access_requirement.value == Route44AccessRequirement.option_gyms
            and world.options.blackthorn_dark_cave_access.value == BlackthornDarkCaveAccess.option_vanilla
            and world.options.route_44_access_count.value > (7 if world.options.johto_only else 15)):
        world.options.route_44_access_count.value = 7 if world.options.johto_only else 15
        logging.warning(
            "Pokemon Crystal: Route 44 Access Gyms >%d incompatible with vanilla Dark Cave. "
            "Changing Route 44 Access Gyms to %d for player %s.",
            world.options.route_44_access_count.value,
            world.options.route_44_access_count.value,
            world.player_name)

    if (world.options.radio_tower_requirement.value == RadioTowerRequirement.option_gyms
            and world.options.radio_tower_count.value > (7 if world.options.johto_only else 15)):
        world.options.radio_tower_count.value = 7 if world.options.johto_only else 15
        logging.warning(
            "Pokemon Crystal: Radio Tower Gyms >%d is impossible. "
            "Changing Radio Tower Gyms to %d for player %s.",
            world.options.radio_tower_count.value,
            world.options.radio_tower_count.value,
            world.player_name)


def __adjust_options_victory_road_badges(world: "PokemonCrystalWorld"):
    if (world.options.elite_four_requirement == EliteFourRequirement.option_johto_badges
            and world.options.elite_four_count > 8):
        world.options.elite_four_count.value = 8
        logging.warning(
            "Pokemon Crystal: Elite Four count cannot be greater than 8 if Elite Four requirement is Johto Badges. "
            "Changing Elite Four Count to 8 for player %s.",
            world.player_name)


def __adjust_options_johto_only(world: "PokemonCrystalWorld"):
    if world.options.johto_only:

        if world.options.goal == Goal.option_red and world.options.johto_only == JohtoOnly.option_on:
            world.options.goal.value = Goal.option_elite_four
            logging.warning(
                "Pokemon Crystal: Red goal is incompatible with Johto Only "
                "without Silver Cave. Changing goal to Elite Four for player %s.",
                world.player_name)

        if world.options.goal == Goal.option_diploma and world.options.johto_only != JohtoOnly.option_off:
            world.options.goal.value = Goal.option_elite_four
            logging.warning(
                "Pokemon Crystal: Diploma goal is incompatible with Johto Only. "
                "Changing goal to Elite Four for player %s.",
                world.player_name)

        if (world.options.elite_four_requirement.value == EliteFourRequirement.option_gyms
                and world.options.elite_four_count.value > 8):
            world.options.elite_four_count.value = 8
            logging.warning(
                "Pokemon Crystal: Elite Four Gyms >8 incompatible with Johto Only. "
                "Changing Elite Four Gyms to 8 for player %s.",
                world.player_name)

        if (world.options.red_requirement.value == RedRequirement.option_gyms
                and world.options.red_count.value > 8):
            world.options.red_count.value = 8
            logging.warning(
                "Pokemon Crystal: Red Gyms >8 incompatible with Johto Only. "
                "Changing Red Gyms to 8 for player %s.",
                world.player_name)

        if (world.options.mt_silver_requirement.value == MtSilverRequirement.option_gyms
                and world.options.mt_silver_count.value > 8):
            world.options.mt_silver_count.value = 8
            logging.warning(
                "Pokemon Crystal: Mt. Silver Gyms >8 incompatible with Johto Only. "
                "Changing Mt. Silver Gyms to 8 for player %s.",
                world.player_name)

        if (world.options.route_44_access_requirement.value == Route44AccessRequirement.option_gyms
                and world.options.route_44_access_count.value > 8):
            world.options.route_44_access_count.value = 8
            logging.warning(
                "Pokemon Crystal: Route 44 Access Gyms >8 incompatible with Johto Only. "
                "Changing Route 44 Access Gyms to 8 for player %s.",
                world.player_name)

        if (world.options.radio_tower_requirement.value == RadioTowerRequirement.option_gyms
                and world.options.radio_tower_count.value > 7):
            world.options.radio_tower_count.value = 7
            logging.warning(
                "Pokemon Crystal: Radio Tower Gyms >7 incompatible with Johto Only. "
                "Changing Radio Tower Gyms to 7 for player %s.",
                world.player_name)

        if world.options.evolution_gym_levels.value < 8:
            world.options.evolution_gym_levels.value = 8
            logging.warning(
                "Pokemon Crystal: Evolution Gym Levels <8 incompatible with Johto Only. "
                "Changing Evolution Gym Levels to 8 for player %s.",
                world.player_name)

        if world.options.randomize_badges != RandomizeBadges.option_completely_random:
            if world.options.red_count.value > 8 and world.options.red_requirement == RedRequirement.option_badges:
                world.options.red_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Red Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Red Badges to 8 for player %s.",
                    world.player_name)

            if (world.options.elite_four_count.value > 8 and
                    world.options.elite_four_requirement.value == EliteFourRequirement.option_badges):
                world.options.elite_four_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Elite Four Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Elite Four Badges to 8 for player %s.",
                    world.player_name)

            if (world.options.radio_tower_count.value > 8
                    and world.options.radio_tower_requirement.value == RadioTowerRequirement.option_badges):
                world.options.radio_tower_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Radio Tower Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Radio Tower Badges to 8 for player %s.",
                    world.player_name)

            if (world.options.mt_silver_count.value > 8 and
                    world.options.mt_silver_requirement.value == MtSilverRequirement.option_badges):
                world.options.mt_silver_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Mt. Silver Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Mt. Silver Badges to 8 for player %s.",
                    world.player_name)

            if (world.options.route_44_access_count.value > 8 and
                    world.options.route_44_access_requirement.value == Route44AccessRequirement.option_badges):
                world.options.route_44_access_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Route 44 Access Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Route 44 Access Badges to 8 for player %s.",
                    world.player_name)


def __adjust_options_restrictive_region_travel(world: "PokemonCrystalWorld") -> None:
    if world.options.randomize_badges != RandomizeBadges.option_completely_random:
        if world.options.magnet_train_access == MagnetTrainAccess.option_pass_and_power:
            world.options.magnet_train_access.value = MagnetTrainAccess.option_pass
            logging.warning("Pokemon Crystal: Magnet Train requires power not compatible with badges in gyms. "
                            "Changing Magnet Train Access to Pass for player %s.",
                            world.player_name)


def __adjust_options_gyarados(world: "PokemonCrystalWorld"):
    if (world.options.red_gyarados_access
            and world.options.randomize_badges.value == RandomizeBadges.option_vanilla
            and "Whirlpool" and not world.options.hm_badge_requirements == HMBadgeRequirements.option_no_badges
            and "Whirlpool" not in world.options.remove_badge_requirement):
        world.options.red_gyarados_access.value = RedGyaradosAccess.option_vanilla
        logging.warning("Pokemon Crystal: Red Gyarados access requires Whirlpool and Vanilla Badges are not "
                        "compatible, setting Red Gyarados access to vanilla for player %s.",
                        world.player_name)


def __adjust_options_early_fly(world: "PokemonCrystalWorld"):
    if (world.options.early_fly
            and world.options.randomize_starting_town
            and world.options.randomize_badges.value != RandomizeBadges.option_completely_random
            and "Fly" not in world.options.remove_badge_requirement
            and world.options.hm_badge_requirements != HMBadgeRequirements.option_no_badges):
        world.options.early_fly.value = EarlyFly.option_false
        logging.warning("Pokemon Crystal: Early fly is not compatible with Random Starting Town if Badges are "
                        "not completely random. Disabling Early Fly for player %s",
                        world.player_name)


def __adjust_options_encounters_and_breeding(world: "PokemonCrystalWorld"):
    if (world.options.breeding_methods_required == BreedingMethodsRequired.option_with_ditto
            and "Ditto" in world.options.wild_encounter_blocklist):
        world.options.breeding_methods_required.value = BreedingMethodsRequired.option_none
        logging.warning(
            "Pokemon Crystal: Ditto cannot be blocklisted while Ditto only breeding is enabled. "
            "Disabling breeding logic for player %s.",
            world.player_name)

    if "Land" not in world.options.wild_encounter_methods_required and "Fishing" not in world.options.wild_encounter_methods_required:
        world.options.wild_encounter_methods_required.value.add(world.random.choice(("Land", "Fishing")))
        logging.warning(
            "Pokemon Crystal: At least one of Land or Fishing must be enabled in wild encounter methods required. "
            "Adding one at random for player %s.",
            world.player_name)

    if (not world.options.randomize_wilds and
            world.options.breeding_methods_required == BreedingMethodsRequired.option_with_ditto
            and "Land" not in world.options.wild_encounter_methods_required):
        world.options.breeding_methods_required.value = BreedingMethodsRequired.option_none
        logging.warning(
            "Pokemon Crystal: Ditto only breeding is not available for vanilla wilds with no Land encounters. "
            "Disabling breeding logic for player %s.",
            world.player_name)


def __adjust_options_race_mode(world: "PokemonCrystalWorld"):
    # In race mode we don't patch any item location information into the ROM
    if world.multiworld.is_race and not world.options.remote_items:
        logging.warning("Pokemon Crystal: Forcing Player %s (%s) to use remote items due to race mode.",
                        world.player, world.player_name)
        world.options.remote_items.value = Toggle.option_true


def __adjust_options_pokemon_requests(world: "PokemonCrystalWorld"):
    if world.options.randomize_pokemon_requests == RandomizePokemonRequests.option_items and not world.options.randomize_wilds:
        logging.warning("Pokemon Crystal: Randomize Pokemon Requests items only is not compatible with vanilla wilds. "
                        "Disabling Randomize Pokemon Requests for player %s (%s).", world.player, world.player_name)
        world.options.randomize_pokemon_requests.value = RandomizePokemonRequests.option_off


def __adjust_options_trades(world: "PokemonCrystalWorld"):
    if (world.options.trades_required and world.options.randomize_trades.value in (RandomizeTrades.option_vanilla,
                                                                                   RandomizeTrades.option_received)
            and not world.options.randomize_wilds):
        logging.warning("Pokemon Crystal: Requested trade Pokemon must be randomized for vanilla wilds. "
                        "Disabling Trades Required for player %s (%s).", world.player, world.player_name)
        world.options.trades_required.value = TradesRequired.option_false


def __adjust_options_dark_areas(world: "PokemonCrystalWorld"):
    if (world.options.dark_areas != world.options.dark_areas.default
            and world.options.randomize_badges != RandomizeBadges.option_completely_random):
        logging.warning(
            "Pokemon Crystal: Non-vanilla dark areas are not compatible with badges that are not completely random. "
            "Resetting dark areas to vanilla for %s (%s).", world.player, world.player_name)
        world.options.dark_areas.value = world.options.dark_areas.default


def __adjust_options_randomize_types(world: "PokemonCrystalWorld"):
    if (world.options.randomize_types == RandomizeTypes.option_follow_evolutions and
            world.options.randomize_evolution == RandomizeEvolution.option_match_a_type):
        logging.warning(
            "Pokemon Crystal: Types follow evolutions and evolutions follow types are incompatible. "
            "Setting Randomize Types to completely random for %s (%s).", world.player, world.player_name)
        world.options.randomize_types.value = RandomizeTypes.option_completely_random


def __adjust_options_tm_plando(world: "PokemonCrystalWorld"):
    if 12 in world.options.tm_plando.value and "Sweet Scent" not in world.options.tm_plando.value.values() \
            and (world.options.dexsanity or world.options.dexcountsanity):
        logging.warning(
            "Pokemon Crystal: A Sweet Scent TM must exist if Dexsanity or Dexcountsanity are enabled. "
            "Resetting TM12 to vanilla for Player %s (%s).", world.player, world.player_name)
        world.options.tm_plando.value.pop(12)


def __adjust_options_traps(world: "PokemonCrystalWorld"):
    if world.options.filler_trap_percentage > world.settings.maximum_filler_trap_percentage:
        maximum_trap_weight = world.settings.maximum_filler_trap_percentage
        logging.warning(
            "Pokemon Crystal: Trap Weight is greater than allowed maximum. "
            f"Reducing filler trap percentage to {maximum_trap_weight} for Player %s (%s).",
            world.player,
            world.player_name
        )
        world.options.filler_trap_percentage.value = maximum_trap_weight


def __adjust_options_mischief_bounds(world: "PokemonCrystalWorld"):
    if world.options.enable_mischief and \
            world.options.mischief_lower_bound.value > world.options.mischief_upper_bound.value:
        world.options.mischief_upper_bound.value = world.options.mischief_lower_bound.value
        logging.warning("Pokemon Crystal: Adjusted mischief bounds for player %s (%s) :3",
                        world.player,
                        world.player_name
                        )


def should_include_region(region: RegionData, world: "PokemonCrystalWorld"):
    # check if region should be included
    return (region.johto
            or world.options.johto_only.value == JohtoOnly.option_off
            or (region.silver_cave and world.options.johto_only == JohtoOnly.option_include_silver_cave)) and (
            not world.options.skip_elite_four or not region.elite_4
    )


def pokemon_convert_friendly_to_ids(world: "PokemonCrystalWorld", pokemon: Iterable[str]) -> set[str]:
    if not pokemon: return set()

    pokemon = set(pokemon)
    if "_Legendaries" in pokemon:
        pokemon.discard("_Legendaries")
        pokemon.update({"Articuno", "Zapdos", "Moltres", "Mewtwo", "Mew", "Entei", "Raikou", "Suicune", "Celebi",
                        "Lugia", "Ho-Oh"})

    pokemon_ids = {pokemon_id for pokemon_id, pokemon_data in world.generated_pokemon.items() if
                   pokemon_data.friendly_name in pokemon}

    return pokemon_ids


def randomize_starting_town(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker or not world.options.randomize_starting_town: return

    location_pool = data.starting_towns[:]
    location_pool = [loc for loc in location_pool if _starting_town_valid(world, loc)]

    blocklist = set(world.options.starting_town_blocklist.value)
    if "_Johto" in blocklist:
        blocklist.remove("_Johto")
        blocklist.update(town.name for town in data.starting_towns if town.johto)
    if "_Kanto" in blocklist:
        blocklist.remove("_Kanto")
        blocklist.update(town.name for town in data.starting_towns if not town.johto)

    filtered_pool = [loc for loc in location_pool if loc.name not in blocklist]
    if not filtered_pool:
        logging.warning("Pokemon Crystal: All valid starting town locations blocked for player %s (%s). "
                        "Using global list instead.", world.player, world.player_name)
        filtered_pool = location_pool

    world.random.shuffle(filtered_pool)
    world.starting_town = filtered_pool.pop()
    logging.debug(f"Starting town({world.player_name}): {world.starting_town.name}")

    if world.starting_town.name == "Cianwood City":
        world.multiworld.early_items[world.player]["HM03 Surf"] = 1


def _starting_town_valid(world: "PokemonCrystalWorld", starting_town: StartingTown):
    if world.options.johto_only and not starting_town.johto: return False
    if world.options.randomize_badges != RandomizeBadges.option_completely_random and starting_town.restrictive_start:
        return False

    immediate_hiddens = world.options.randomize_hidden_items and not world.options.require_itemfinder
    full_johto_trainersanity = world.options.johto_trainersanity == JohtoTrainersanity.range_end
    full_kanto_trainersanity = world.options.kanto_trainersanity == KantoTrainersanity.range_end
    johto_shopsanity = Shopsanity.johto_marts in world.options.shopsanity.value
    kanto_shopsanity = Shopsanity.kanto_marts in world.options.shopsanity.value

    if starting_town.name == "Cianwood City":
        return world.options.static_pokemon_required and (
                (full_johto_trainersanity and immediate_hiddens) or johto_shopsanity)
    if starting_town.name in ("Lake of Rage", "Mahogany Town"):
        return ((not world.options.mount_mortar_access and "Mount Mortar" not in world.options.dark_areas)
                or johto_shopsanity or full_johto_trainersanity)
    if starting_town.name == "Azalea Town":
        return ("Slowpoke Well" not in world.options.dark_areas
                or "Union Cave" not in world.options.dark_areas)

    if starting_town.name in ("Pallet Town", "Viridian City", "Pewter City"):
        return (immediate_hiddens or world.options.route_3_access == Route3Access.option_vanilla or kanto_shopsanity
                or world.options.randomize_berry_trees)
    if starting_town.name == "Rock Tunnel":
        return full_kanto_trainersanity
    if starting_town.name == "Vermilion City":
        return "South" not in world.options.saffron_gatehouse_tea or world.options.undergrounds_require_power not in (
            UndergroundsRequirePower.option_both, UndergroundsRequirePower.option_north_south) or kanto_shopsanity
    if starting_town.name == "Cerulean City":
        return ("North" not in world.options.saffron_gatehouse_tea or immediate_hiddens or kanto_shopsanity
                or full_kanto_trainersanity)
    if starting_town.name == "Celadon City":
        return "West" not in world.options.saffron_gatehouse_tea or immediate_hiddens or kanto_shopsanity
    if starting_town.name == "Lavender Town":
        return "East" not in world.options.saffron_gatehouse_tea or full_kanto_trainersanity or kanto_shopsanity or (
                not world.options.route_12_access and immediate_hiddens and world.options.randomize_berry_trees)
    if starting_town.name == "Fuchsia City":
        return ("East" not in world.options.saffron_gatehouse_tea and not world.options.route_12_access) or (
                immediate_hiddens and world.options.randomize_berry_trees) or (
                not world.options.route_12_access and kanto_shopsanity) or full_kanto_trainersanity

    return True


def get_fly_regions(world: "PokemonCrystalWorld") -> list[FlyRegion]:
    fly_regions = list(data.fly_regions)

    if world.options.johto_only == JohtoOnly.option_on:
        fly_regions = [region for region in fly_regions if region.name != "Silver Cave"]

    if world.options.johto_only:
        fly_regions = [region for region in fly_regions if region.johto]

    return fly_regions


def get_free_fly_locations(world: "PokemonCrystalWorld"):
    location_pool = data.fly_regions[:]

    if not world.options.randomize_starting_town:
        location_pool = \
            [region for region in location_pool if not region.exclude_vanilla_start]
        if world.options.route_32_condition.value != Route32Condition.option_any_badge:
            # Azalea, Goldenrod
            location_pool = [region for region in location_pool if region.name not in ("Azalea Town", "Goldenrod City")]
        if not world.options.remove_ilex_cut_tree and world.options.route_32_condition.value != Route32Condition.option_any_badge:
            # Goldenrod
            location_pool = [region for region in location_pool if region.name != "Goldenrod City"]
    if world.options.johto_only:
        location_pool = [region for region in location_pool if region.johto]
    if world.options.johto_only.value == JohtoOnly.option_on:
        # Mt. Silver
        location_pool = [region for region in location_pool if region.name != "Silver Cave"]

    if world.options.randomize_starting_town:
        world.options.free_fly_blocklist.value.add(world.starting_town.name)

    blocklist = set(world.options.free_fly_blocklist.value)
    if "_Johto" in blocklist:
        blocklist.remove("_Johto")
        blocklist.update(town.name for town in data.fly_regions if town.johto)
    if "_Kanto" in blocklist:
        blocklist.remove("_Kanto")
        blocklist.update(town.name for town in data.fly_regions if not town.johto)

    # only do any of this if there even is a fly location blocklist
    if blocklist:

        # figure out how many fly locations are needed
        locations_required = 1
        if world.options.free_fly_location.value == FreeFlyLocation.option_free_fly_and_map_card:
            locations_required = 2

        # calculate what the list of locations would be after the blocklist
        location_pool_after_blocklist = [item for item in location_pool if
                                         item.name not in blocklist]

        # if the list after the blocked locations are removed is long enough to satisfy all the requested fly locations, set the location pool to it
        if len(location_pool_after_blocklist) >= locations_required:
            location_pool = location_pool_after_blocklist
        else:
            logging.warning("Pokemon Crystal: All valid free fly locations blocked for player %s (%s). "
                            "Using global list instead.", world.player, world.player_name)

    world.random.shuffle(location_pool)
    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                 FreeFlyLocation.option_free_fly_and_map_card):
        world.free_fly_location = location_pool.pop()
    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card):
        world.map_card_fly_location = location_pool.pop()


def get_mart_slot_location_name(mart: str, index: int):
    if mart in CUSTOM_MART_SLOT_NAMES:
        return CUSTOM_MART_SLOT_NAMES[mart][index]
    else:
        return f"Shop Item {index + 1}"


def convert_to_ingame_text(text: str, string_terminator: bool = False) -> list[int]:
    charmap = {
        "…": 0x75, " ": 0x7f, "A": 0x80, "B": 0x81, "C": 0x82, "D": 0x83, "E": 0x84, "F": 0x85, "G": 0x86, "H": 0x87,
        "I": 0x88, "J": 0x89, "K": 0x8a, "L": 0x8b, "M": 0x8c, "N": 0x8d, "O": 0x8e, "P": 0x8f, "Q": 0x90, "R": 0x91,
        "S": 0x92, "T": 0x93, "U": 0x94, "V": 0x95, "W": 0x96, "X": 0x97, "Y": 0x98, "Z": 0x99, "(": 0x9a, ")": 0x9b,
        ":": 0x9c, ";": 0x9d, "[": 0x9e, "]": 0x9f, "a": 0xa0, "b": 0xa1, "c": 0xa2, "d": 0xa3, "e": 0xa4, "f": 0xa5,
        "g": 0xa6, "h": 0xa7, "i": 0xa8, "j": 0xa9, "k": 0xaa, "l": 0xab, "m": 0xac, "n": 0xad, "o": 0xae, "p": 0xaf,
        "q": 0xb0, "r": 0xb1, "s": 0xb2, "t": 0xb3, "u": 0xb4, "v": 0xb5, "w": 0xb6, "x": 0xb7, "y": 0xb8, "z": 0xb9,
        "Ä": 0xc0, "Ö": 0xc1, "Ü": 0xc2, "ä": 0xc3, "ö": 0xc4, "ü": 0xc5, "'": 0xe0, "-": 0xe3, "?": 0xe6, "!": 0xe7,
        ".": 0xe8, "&": 0xe9, "é": 0xea, "→": 0xeb, "▷": 0xec, "▶": 0xed, "▼": 0xee, "♂": 0xef, "¥": 0xf0, "/": 0xf3,
        ",": 0xf4, "0": 0xf6, "1": 0xf7, "2": 0xf8, "3": 0xf9, "4": 0xfa, "5": 0xfb, "6": 0xfc, "7": 0xfd, "8": 0xfe,
        "9": 0xff, "_": 0xe3, "♀": 0xf5
    }
    ingame_string = [charmap.get(char, charmap["?"]) for char in text]
    if string_terminator:
        ingame_string.append(0x50)
    return ingame_string


def bound(value: int, lower_bound: int, upper_bound: int) -> int:
    return max(min(value, upper_bound), lower_bound)


def replace_map_tiles(patch, map_name: str, x: int, y: int, tiles):
    # x and y are 0 indexed
    tile_index = (y * data.maps[map_name].width) + x
    base_address = data.rom_addresses[f"{map_name}_Blocks"]

    logging.debug(f"Writing {len(tiles)} new tile(s) to map {map_name} at {x},{y}")
    write_appp_tokens(patch, tiles, base_address + tile_index)


def write_appp_tokens(patch, byte_array, address):
    patch.write_token(
        APTokenTypes.WRITE,
        address,
        bytes(byte_array)
    )


def write_rom_bytes(rom, byte_array, address):
    rom[address:address + len(byte_array)] = bytes(byte_array)
