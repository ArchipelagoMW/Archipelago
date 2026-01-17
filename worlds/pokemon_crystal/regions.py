import logging
from typing import TYPE_CHECKING

from BaseClasses import Region, ItemClassification
from .data import data, RegionData, EncounterMon, StaticPokemon, LogicalAccess, EncounterKey, FishingRodType, \
    TreeRarity, EncounterType
from .items import PokemonCrystalItem
from .locations import PokemonCrystalLocation
from .options import FreeFlyLocation, JohtoOnly, BlackthornDarkCaveAccess, Goal, FlyCheese, Route42Access
from .utils import get_fly_regions, should_include_region

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld

# Rematches
MAP_LOCKED = [
    "BUG_CATCHER_ARNIE_BLACKTHORN", "BUG_CATCHER_ARNIE_LAKE",
    "BUG_CATCHER_WADE_GOLDENROD", "BUG_CATCHER_WADE_MAHOGANY",
    "CAMPER_TODD_BLACKTHORN", "CAMPER_TODD_CIANWOOD",
    "HIKER_ANTHONY_OLIVINE", "LASS_DANA_CIANWOOD",
    "PICNICKER_GINA_MAHOGANY", "SCHOOLBOY_ALAN_BLACKTHORN",
    "SCHOOLBOY_ALAN_OLIVINE", "SCHOOLBOY_CHAD_MAHOGANY",
    "SCHOOLBOY_JACK_OLIVINE", "YOUNGSTER_JOEY_GOLDENROD",
    "YOUNGSTER_JOEY_OLIVINE"
]

ROCKETHQ_LOCKED = [
    "FISHER_TULLY_ROCKETHQ", "POKEMANIAC_BRENT_ROCKETHQ"
]

RADIO_LOCKED = [
    "BUG_CATCHER_WADE_RADIO", "HIKER_ANTHONY_RADIO",
    "LASS_DANA_RADIO", "PICNICKER_GINA_RADIO",
    "PICNICKER_TIFFANY_RADIO", "SAILOR_HUEY_RADIO",
    "SCHOOLBOY_CHAD_RADIO", "SCHOOLBOY_JACK_RADIO",
    "YOUNGSTER_JOEY_RADIO"
]

CHAMPION_LOCKED = [
    "BIRD_KEEPER_JOSE_CHAMPION", "BIRD_KEEPER_VANCE_CHAMPION",
    "BUG_CATCHER_ARNIE_CHAMPION", "BUG_CATCHER_WADE_CHAMPION",
    "CAMPER_TODD_CHAMPION", "COOLTRAINERF_BETH_CHAMPION",
    "COOLTRAINERF_REENA_CHAMPION", "COOLTRAINERM_GAVEN_CHAMPION",
    "FISHER_TULLY_CHAMPION", "FISHER_WILTON_CHAMPION",
    "HIKER_ANTHONY_CHAMPION", "HIKER_PARRY_CHAMPION",
    "LASS_DANA_CHAMPION", "PICNICKER_ERIN_CHAMPION",
    "PICNICKER_GINA_CHAMPION", "PICNICKER_TIFFANY_CHAMPION",
    "POKEMANIAC_BRENT_CHAMPION", "SAILOR_HUEY_CHAMPION",
    "SCHOOLBOY_ALAN_CHAMPION", "SCHOOLBOY_CHAD_CHAMPION",
    "SCHOOLBOY_JACK_CHAMPION", "YOUNGSTER_JOEY_CHAMPION",
    "PICNICKER_LIZ_CHAMPION"
]

KANTO_LOCKED = [
    "BIRD_KEEPER_JOSE_POWER", "BIRD_KEEPER_VANCE_POWER",
    "BUG_CATCHER_ARNIE_POWER", "CAMPER_TODD_POWER",
    "COOLTRAINERF_BETH_POWER", "COOLTRAINERF_REENA_POWER",
    "COOLTRAINERM_GAVEN_POWER", "FISHER_TULLY_POWER",
    "FISHER_WILTON_POWER", "HIKER_ANTHONY_POWER",
    "HIKER_PARRY_POWER", "LASS_DANA_POWER",
    "PICNICKER_ERIN_POWER", "PICNICKER_GINA_POWER",
    "PICNICKER_TIFFANY_POWER", "POKEMANIAC_BRENT_POWER",
    "SAILOR_HUEY_POWER", "SCHOOLBOY_ALAN_POWER",
    "SCHOOLBOY_CHAD_POWER", "SCHOOLBOY_JACK_POWER"
]

LOGIC_EXCLUDE_STATICS = [
    "Raikou", "Entei", "CatchTutorial1", "CatchTutorial2", "CatchTutorial3"
]

E4_LOCKED = list(set(CHAMPION_LOCKED + KANTO_LOCKED))
REMATCHES = list(set(MAP_LOCKED + ROCKETHQ_LOCKED + RADIO_LOCKED + E4_LOCKED + KANTO_LOCKED))


def create_regions(world: "PokemonCrystalWorld") -> dict[str, Region]:
    regions: dict[str, Region] = {}
    connections: list[tuple[str, str, str]] = []
    johto_only = world.options.johto_only.value
    rematches = world.options.rematchsanity or world.options.randomize_phone_call_items

    wild_name_level_list: list[tuple[str, list[int]]] = []
    trainer_name_level_list: list[tuple[str, int]] = []
    static_name_level_list: list[tuple[str, int]] = []

    wild_scaling_locations = set()

    def exclude_scaling(trainer: str):
        if not rematches and (trainer in REMATCHES):
            return True
        elif johto_only != JohtoOnly.option_off and trainer in KANTO_LOCKED:
            return True
        elif world.options.goal.value == Goal.option_elite_four and trainer in E4_LOCKED:
            return True
        else:
            return False

    def create_scaling_location(parent_region: Region, wild_key: EncounterKey):
        if wild_key.region_name() in wild_scaling_locations: return
        if world.options.level_scaling and wild_key.encounter_type in [EncounterType.Grass,
                                                                       EncounterType.Water]:
            wild_name_level_list.append((
                wild_key.region_name(),
                [slot.level for slot in world.generated_wild[wild_key]]
            ))

            scaling_event = PokemonCrystalLocation(
                world.player, wild_key.region_name(), parent_region, None, None, None,
                frozenset({"wilds scaling"}))
            scaling_event.show_in_spoiler = False
            scaling_event.place_locked_item(PokemonCrystalItem(
                "Wild Pokemon", ItemClassification.filler, None, world.player))
            scaling_event.encounter_key = wild_key
            parent_region.locations.append(scaling_event)
            wild_scaling_locations.add(scaling_event.name)

    def create_wild_region(parent_region: Region, wild_key: EncounterKey, wilds: list[EncounterMon | StaticPokemon],
                           tags: set[str] | None = None):
        region_name = wild_key.region_name()
        if region_name not in regions:
            wild_region = Region(region_name, world.player, world.multiworld)
            wild_region.key = wild_key
            regions[region_name] = wild_region

            # We place a slot for each encounter here, but we don't care about what they are yet
            for i in range(len(wilds)):
                location = PokemonCrystalLocation(
                    world.player,
                    f"{region_name}_{i + 1}",
                    wild_region,
                    tags=frozenset(tags | {"wild encounter"} if tags else {"wild encounter"})
                )
                location.show_in_spoiler = False
                wild_region.locations.append(location)
        else:
            wild_region = regions[region_name]
        parent_region.connect(wild_region)

    def setup_wild_regions(parent_region: Region, wild_region_data: RegionData):

        if wild_region_data.wild_encounters:
            if wild_region_data.wild_encounters.grass:
                encounter_key = EncounterKey.grass(wild_region_data.wild_encounters.grass)
                create_scaling_location(parent_region, encounter_key)
                if "Land" in world.options.wild_encounter_methods_required:
                    world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                    create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                else:
                    if not world.options.enforce_wild_encounter_methods_logic:
                        world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                    if world.is_universal_tracker:
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

            if wild_region_data.wild_encounters.surfing:
                encounter_key = EncounterKey.water(wild_region_data.wild_encounters.surfing)
                create_scaling_location(parent_region, encounter_key)
                if "Surfing" in world.options.wild_encounter_methods_required:
                    world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                    create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                else:
                    if not world.options.enforce_wild_encounter_methods_logic:
                        world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                    if world.is_universal_tracker:
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

            if wild_region_data.wild_encounters.fishing:
                if "Fishing" in world.options.wild_encounter_methods_required:
                    for fishing_rod in (FishingRodType.Old, FishingRodType.Good, FishingRodType.Super):
                        encounter_key = EncounterKey.fish(wild_region_data.wild_encounters.fishing, fishing_rod)
                        world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                else:
                    for fishing_rod in (FishingRodType.Old, FishingRodType.Good, FishingRodType.Super):
                        encounter_key = EncounterKey.fish(wild_region_data.wild_encounters.fishing, fishing_rod)
                        if not world.options.enforce_wild_encounter_methods_logic:
                            world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                        if world.is_universal_tracker:
                            create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

            if wild_region_data.wild_encounters.headbutt:
                if "Headbutt" in world.options.wild_encounter_methods_required:
                    for rarity in (TreeRarity.Common, TreeRarity.Rare):
                        encounter_key = EncounterKey.tree(wild_region_data.wild_encounters.headbutt, rarity)
                        world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                else:
                    for rarity in (TreeRarity.Common, TreeRarity.Rare):
                        encounter_key = EncounterKey.tree(wild_region_data.wild_encounters.headbutt, rarity)
                        if not world.options.enforce_wild_encounter_methods_logic:
                            world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                        if world.is_universal_tracker:
                            create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

            if wild_region_data.wild_encounters.rock_smash:
                encounter_key = EncounterKey.rock_smash()
                if "Rock Smash" in world.options.wild_encounter_methods_required:
                    world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                    create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                else:
                    if not world.options.enforce_wild_encounter_methods_logic:
                        world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                    if world.is_universal_tracker:
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

        for static_id in wild_region_data.statics:
            static_encounter = world.generated_static[static_id]
            encounter_key = EncounterKey.static(static_encounter.name)
            if (world.options.static_pokemon_required
                    and static_encounter.name not in LOGIC_EXCLUDE_STATICS):
                world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                create_wild_region(parent_region, encounter_key, [static_encounter])
            else:
                world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                if world.is_universal_tracker:
                    create_wild_region(parent_region, encounter_key, [static_encounter])

    def setup_mart_regions(parent_region: Region, region_data: RegionData):
        for mart in region_data.marts:
            mart_data = data.marts[mart]
            if mart_data.category in world.options.shopsanity.value:
                region_name = f"REGION_{mart}"
                new_region = Region(region_name, world.player, world.multiworld)
                regions[region_name] = new_region
                parent_region.connect(new_region)

    for region_name, region_data in data.regions.items():
        if should_include_region(region_data, world):
            new_region = Region(region_name, world.player, world.multiworld)

            regions[region_name] = new_region

            for event_data in region_data.events:
                event_location = PokemonCrystalLocation(world.player, event_data.name, new_region)
                event_location.show_in_spoiler = False
                event_location.place_locked_item(world.create_event(event_data.name))
                new_region.locations.append(event_location)

            setup_wild_regions(new_region, region_data)
            if world.options.shopsanity:
                setup_mart_regions(new_region, region_data)

            # Level Scaling
            if world.options.level_scaling and not world.is_universal_tracker:
                # Create plando locations for the trainers in their regions.
                for trainer in region_data.trainers:
                    if exclude_scaling(trainer.name):
                        logging.debug(
                            f"Excluding %s from level scaling for %s", trainer.name, world.player_name)
                        continue
                    scaling_event = PokemonCrystalLocation(
                        world.player, trainer.name, new_region, None, None, None, frozenset({"trainer scaling"}))
                    scaling_event.show_in_spoiler = False
                    scaling_event.place_locked_item(PokemonCrystalItem(
                        "Trainer Party", ItemClassification.filler, None, world.player))
                    new_region.locations.append(scaling_event)

                # Create plando locations for the statics in their regions.
                for static in region_data.statics:
                    scaling_event = PokemonCrystalLocation(
                        world.player, world.generated_static[static].name, new_region, None, None, None,
                        frozenset({"static scaling"}))
                    scaling_event.show_in_spoiler = False
                    scaling_event.place_locked_item(PokemonCrystalItem(
                        "Static Pokemon", ItemClassification.filler, None, world.player))
                    new_region.locations.append(scaling_event)

                min_level = 100
                # Create a new list of all the Trainer Pokemon and their levels
                for trainer in region_data.trainers:
                    if exclude_scaling(trainer.name):
                        continue
                    for pokemon in trainer.pokemon:
                        min_level = min(min_level, pokemon.level)
                    # We grab the level and add it to our custom list.
                    trainer_name_level_list.append((trainer.name, min_level))
                    world.trainer_name_level_dict[trainer.name] = min_level

                min_level = 100
                # Now we do the same for statics.
                for static_id in region_data.statics:
                    static = world.generated_static[static_id]
                    min_level = min(min_level, static.level)
                    static_name_level_list.append((static.name, min_level))

            if world.options.grasssanity and region_name in data.grass_tiles:
                grass_region = Region(f"{region_name}:GRASS", world.player, world.multiworld)
                regions[grass_region.name] = grass_region
                new_region.connect(grass_region)

            for region_exit in region_data.exits:
                connections.append((f"{region_name} -> {region_exit}", region_name, region_exit))

    for name, source, dest in connections:
        if should_include_region(data.regions[source], world) and should_include_region(data.regions[dest], world):
            regions[source].connect(regions[dest], name)

    if world.options.skip_elite_four:
        regions["REGION_INDIGO_PLATEAU_POKECENTER_1F"].connect(regions["REGION_LANCES_ROOM"])

    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    if world.options.randomize_starting_town:
        regions["Menu"].connect(regions[world.starting_town.region_id])
    else:
        regions["Menu"].connect(regions["REGION_PLAYERS_HOUSE_2F"], "Start Game")

    regions["Menu"].connect(regions["REGION_FLY"], "Fly")

    if world.options.randomize_fly_unlocks:
        fly_region = regions["REGION_FLY"]
        for region in get_fly_regions(world):
            fly_region.connect(regions[region.exit_region])

    if world.options.fly_cheese == FlyCheese.option_in_logic:
        regions["REGION_ROUTE_44"].connect(regions["REGION_MAHOGANY_TOWN:FLY"])

        if not world.options.johto_only:
            regions["REGION_DIGLETTS_CAVE"].connect(regions["REGION_VERMILION_CITY:FLY"])
            regions["REGION_ROUTE_11"].connect(regions["REGION_VERMILION_CITY:FLY"])

    if world.options.johto_only == JohtoOnly.option_off and world.options.east_west_underground:
        regions["REGION_ROUTE_7"].connect(regions["REGION_ROUTE_8"])
        regions["REGION_ROUTE_8"].connect(regions["REGION_ROUTE_7"])

    if world.options.blackthorn_dark_cave_access == BlackthornDarkCaveAccess.option_waterfall:
        regions["REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTH_WEST"].connect(
            regions["REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTH_WEST"])

    if world.options.route_42_access != Route42Access.option_blocked:
        regions["REGION_ROUTE_42:WEST"].connect(regions["REGION_ROUTE_42:CENTER"])
        regions["REGION_ROUTE_42:CENTER"].connect(regions["REGION_ROUTE_42:WEST"])
        regions["REGION_ROUTE_42:EAST"].connect(regions["REGION_ROUTE_42:CENTER"])
        regions["REGION_ROUTE_42:CENTER"].connect(regions["REGION_ROUTE_42:EAST"])

    if world.options.route_42_access in \
            (Route42Access.option_blocked, Route42Access.option_whirlpool_open_mortar):
        regions["REGION_MOUNT_MORTAR_1F_OUTSIDE:BELOW_WATERFALL"].connect(
            regions["REGION_MOUNT_MORTAR_1F_INSIDE:FRONT"])
        regions["REGION_MOUNT_MORTAR_1F_INSIDE:FRONT"].connect(
            regions["REGION_MOUNT_MORTAR_1F_OUTSIDE:BELOW_WATERFALL"])

    if world.options.dexsanity or world.options.dexcountsanity:
        pokedex_region = Region("Pokedex", world.player, world.multiworld)
        regions["Pokedex"] = pokedex_region
        regions["Menu"].connect(regions["Pokedex"])
    if world.options.evolution_methods_required or world.is_universal_tracker:
        evolution_region = Region("Evolutions", world.player, world.multiworld)
        regions["Evolutions"] = evolution_region
        regions["Menu"].connect(regions["Evolutions"])
    if world.options.breeding_methods_required or world.is_universal_tracker:
        breeding_region = Region("Breeding", world.player, world.multiworld)
        regions["Breeding"] = breeding_region
        regions["Menu"].connect(regions["Breeding"])

    if world.options.level_scaling and not world.is_universal_tracker:
        trainer_name_level_list.sort(key=lambda i: i[1])
        world.trainer_name_list = [i[0] for i in trainer_name_level_list]
        world.trainer_level_list = [i[1] for i in trainer_name_level_list]
        static_name_level_list.sort(key=lambda i: i[1])
        world.static_name_list = [i[0] for i in static_name_level_list]
        world.static_level_list = [i[1] for i in static_name_level_list]
        wild_name_level_list.sort(key=lambda i: max(i[1]))
        world.encounter_region_name_list = [i[0] for i in wild_name_level_list]
        world.encounter_region_levels_list = [j for i in wild_name_level_list for j in i[1]]
        world.encounter_region_levels_list.sort()
    return regions


def setup_free_fly_regions(world: "PokemonCrystalWorld"):
    fly = world.get_region("REGION_FLY")
    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                 FreeFlyLocation.option_free_fly_and_map_card):
        free_fly_location = world.free_fly_location
        fly_region = world.get_region(free_fly_location.exit_region)
        fly.connect(fly_region, f"Free Fly {free_fly_location.exit_region}")

    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card):
        map_card_fly_location = world.map_card_fly_location
        map_card_region = world.get_region(map_card_fly_location.exit_region)
        fly.connect(map_card_region, f"Free Fly {map_card_fly_location.exit_region}")
