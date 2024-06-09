import copy
import logging
import pkgutil
from typing import List, Union, ClassVar, Dict, Any, Tuple

import settings
from BaseClasses import Tutorial, ItemClassification
from Fill import fill_restrictive
from worlds.AutoWorld import World, WebWorld
from .client import PokemonCrystalClient
from .data import PokemonData, TrainerData, BASE_OFFSET, MiscData, TMHMData, BankAddress, data as crystal_data, \
    WildData, StaticPokemon
from .items import PokemonCrystalItem, create_item_label_to_code_map, get_item_classification, \
    reverse_offset_item_value, ITEM_GROUPS, item_const_name_to_id, item_const_name_to_label
from .locations import create_locations, PokemonCrystalLocation, create_location_label_to_id_map
from .misc import misc_activities, get_misc_spoiler_log
from .moves import randomize_tms
from .options import PokemonCrystalOptions, JohtoOnly, RandomizeBadges, Goal, HMBadgeRequirements
from .phone import generate_phone_traps
from .phone_data import PhoneScript
from .pokemon import randomize_pokemon, randomize_starters
from .regions import create_regions, setup_free_fly
from .rom import generate_output, PokemonCrystalProcedurePatch
from .rules import set_rules
from .trainers import randomize_trainers, vanilla_trainer_movesets
from .utils import get_random_filler_item, get_free_fly_location
from .wild import randomize_wild_pokemon, randomize_static_pokemon


class PokemonCrystalSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        description = "Pokemon Crystal (UE) (V1.0) ROM File"
        copy_to = "Pokemon - Crystal Version (UE) (V1.0) [C][!].gbc"
        md5s = ["9f2922b235a5eeb78d65594e82ef5dde"]

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching)
        True for operating system default program
        Alternatively, a path to a program to open the .gb file with
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: Union[RomStart, bool] = True


class PokemonCrystalWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokemon Crystal with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["AliceMousie"]
    )]


class PokemonCrystalWorld(World):
    """Pokémon Crystal is the culmination of the Generation I and II Pokémon games.
    Explore the Johto and Kanto regions, become the Pokémon League Champion, and
    defeat the elusive Red at the peak of Mt. Silver!"""
    game = "Pokemon Crystal"

    topology_present = True
    web = PokemonCrystalWebWorld()

    settings_key = "pokemon_crystal_settings"
    settings: ClassVar[PokemonCrystalSettings]

    options_dataclass = PokemonCrystalOptions
    options: PokemonCrystalOptions

    data_version = 0
    required_client_version = (0, 4, 4)

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_label_to_id_map()
    item_name_groups = ITEM_GROUPS  # item_groups

    free_fly_location: int
    map_card_fly_location: int
    generated_pokemon: Dict[str, PokemonData]
    generated_starters: Tuple[List[str], List[str], List[str]]
    generated_starter_helditems: Tuple[str, str, str]
    generated_trainers: Dict[str, TrainerData]
    generated_palettes: Dict[str, List[int]]
    generated_phone_traps: List[PhoneScript]
    generated_phone_indices: List[int]
    generated_misc: MiscData
    generated_tms: Dict[str, TMHMData]
    generated_wild: WildData
    # generated_sfx: List[BankAddress]
    generated_music: List[int]
    generated_wooper: str
    generated_static: Dict[str, StaticPokemon]

    def generate_early(self) -> None:
        if self.options.early_fly:
            self.multiworld.local_early_items[self.player]["HM02 Fly"] = 1
            if (self.options.hm_badge_requirements.value != HMBadgeRequirements.option_no_badges
                    and self.options.randomize_badges == RandomizeBadges.option_completely_random):
                self.multiworld.local_early_items[self.player]["Storm Badge"] = 1

        if self.options.johto_only:
            if self.options.goal == Goal.option_red and self.options.johto_only == JohtoOnly.option_on:
                self.options.goal.value = Goal.option_elite_four
                logging.warning(
                    "Pokemon Crystal: Red goal is incompatible with Johto Only "
                    "without Silver Cave. Changing goal to Elite Four for player %s.",
                    self.multiworld.get_player_name(self.player))
            if self.options.randomize_badges != RandomizeBadges.option_completely_random:
                if self.options.red_badges.value > 8:
                    self.options.red_badges.value = 8
                    logging.warning(
                        "Pokemon Crystal: Red Badges >8 incompatible with Johto Only "
                        "if badges are not completely random. Changing Red Badges to 8 for player %s.",
                        self.multiworld.get_player_name(self.player))
                if self.options.elite_four_badges.value > 8:
                    self.options.elite_four_badges.value = 8
                    logging.warning(
                        "Pokemon Crystal: Elite Four Badges >8 incompatible with Johto Only "
                        "if badges are not completely random. Changing Elite Four Badges to 8 for player %s.",
                        self.multiworld.get_player_name(self.player))

    def create_regions(self) -> None:
        regions = create_regions(self)
        create_locations(self, regions)
        self.multiworld.regions.extend(regions.values())
        if self.options.free_fly_location:
            get_free_fly_location(self)
            setup_free_fly(self)

    def create_items(self) -> None:
        item_locations = [
            location
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ]

        if self.options.randomize_badges.value == RandomizeBadges.option_shuffle:
            item_locations = [location for location in item_locations if "Badge" not in location.tags]

        total_badges = max(self.options.elite_four_badges.value, self.options.red_badges.value)
        add_badges = []
        # Extra badges to add to the pool in johto only
        if self.options.johto_only and total_badges > 8:
            kanto_badges = [item_id + BASE_OFFSET for item_id, item_data in crystal_data.items.items() if
                            "KantoBadge" in item_data.tags]
            self.random.shuffle(kanto_badges)
            add_badges = kanto_badges[:total_badges - 8]

        traps_pool = []
        traps_pool += ["Phone Trap"] * self.options.phone_trap_weight.value
        traps_pool += ["Sleep Trap"] * self.options.sleep_trap_weight.value
        traps_pool += ["Poison Trap"] * self.options.poison_trap_weight.value
        traps_pool += ["Burn Trap"] * self.options.burn_trap_weight.value
        traps_pool += ["Freeze Trap"] * self.options.freeze_trap_weight.value
        traps_pool += ["Paralysis Trap"] * self.options.paralysis_trap_weight.value

        total_trap_weight = len(traps_pool)

        def get_random_trap():
            return self.create_item(self.random.choice(traps_pool))

        default_itempool = []

        for location in item_locations:
            item_code = location.default_item_code
            if item_code > BASE_OFFSET and get_item_classification(item_code) != ItemClassification.filler:
                if item_code in crystal_data.tm_replace_map and self.options.randomize_tm_moves:
                    default_itempool += [self.create_item_by_code(item_code + 256)]
                else:
                    default_itempool += [self.create_item_by_code(item_code)]
            elif len(add_badges):
                default_itempool += [self.create_item_by_code(add_badges.pop())]
            elif self.random.randint(0, 100) < total_trap_weight:
                default_itempool += [get_random_trap()]
            elif item_code == BASE_OFFSET:  # item is NO_ITEM, trainersanity checks
                default_itempool += [self.create_item_by_const_name(get_random_filler_item(self.random))]
            else:
                default_itempool += [self.create_item_by_code(item_code)]

        self.multiworld.itempool += default_itempool

    def set_rules(self) -> None:
        set_rules(self)

    def pre_fill(self) -> None:
        if self.options.randomize_badges.value == RandomizeBadges.option_shuffle:
            badge_locs = [loc for loc in self.multiworld.get_locations(self.player) if "Badge" in loc.tags]
            badge_items = [self.create_item_by_code(loc.default_item_code) for loc in badge_locs]
            if self.options.early_fly:
                # take one of the 3 early badge locations, set it to storm badge
                storm_loc = self.random.choice([loc for loc in badge_locs if "EarlyBadge" in loc.tags])
                storm_badge = [item for item in badge_items if item.name == "Storm Badge"][0]
                storm_loc.place_locked_item(storm_badge)
                badge_locs.remove(storm_loc)
                badge_items.remove(storm_badge)

            # 5/8 badge locations in each region do not require a HM to access, so only trying once should be okay.
            # I generated 1000 seeds with shuffled badges and none of them broke here, so it's fine probably
            self.random.shuffle(badge_locs)
            collection_state = self.multiworld.get_all_state(False)
            fill_restrictive(self.multiworld, collection_state, badge_locs, badge_items,
                             single_player_placement=True, lock=True, allow_excluded=True)

    def generate_output(self, output_directory: str) -> None:

        self.generated_pokemon = copy.deepcopy(crystal_data.pokemon)
        self.generated_starters = (["CYNDAQUIL", "QUILAVA", "TYPHLOSION"],
                                   ["TOTODILE", "CROCONAW", "FERALIGATR"],
                                   ["CHIKORITA", "BAYLEEF", "MEGANIUM"])
        self.generated_starter_helditems = ("BERRY", "BERRY", "BERRY")
        self.generated_trainers = copy.deepcopy(crystal_data.trainers)
        self.generated_misc = copy.deepcopy(crystal_data.misc)
        self.generated_tms = copy.deepcopy(crystal_data.tmhm)
        self.generated_wild = copy.deepcopy(crystal_data.wild)
        self.generated_static = copy.deepcopy(crystal_data.static)
        self.generated_palettes = {}
        self.generated_phone_traps = []
        self.generated_phone_indices = []
        self.generated_music = []
        self.generated_wooper = "WOOPER"
        # self.generated_sfx = copy.deepcopy(crystal_data.sfx.pointers)

        randomize_pokemon(self)

        if self.options.randomize_starters.value:
            randomize_starters(self)

        if self.options.randomize_tm_moves.value:
            randomize_tms(self)

        if self.options.randomize_trainer_parties.value:
            randomize_trainers(self)
        elif self.options.randomize_learnsets.value:
            vanilla_trainer_movesets(self)

        if self.options.randomize_wilds.value:
            randomize_wild_pokemon(self)

        if self.options.randomize_static_pokemon.value:
            randomize_static_pokemon(self)

        if self.options.randomize_music.value:
            music_pool = [music_id for music_name, music_id in crystal_data.music.consts.items() if
                          music_name != "MUSIC_NONE"]
            for _music in crystal_data.music.maps:
                new_music = self.random.choice(music_pool)
                self.generated_music.append(new_music)

        # if self.options.randomize_sfx:
        #     self.random.shuffle(self.generated_sfx)

        if self.options.enable_mischief.value:
            misc_activities(self)

        generate_phone_traps(self)

        player_name = self.multiworld.get_player_name(self.player)
        patch = PokemonCrystalProcedurePatch(player=self.player, player_name=player_name)
        patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "data/basepatch.bsdiff4"))
        generate_output(self, output_directory, patch)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict(
            "goal",
            "johto_only",
            "elite_four_badges",
            "red_badges",
            "randomize_badges",
            "randomize_hidden_items",
            "require_itemfinder",
            "trainersanity",
            "randomize_pokegear",
            "hm_badge_requirements",
            "randomize_berry_trees"
        )
        slot_data["free_fly_location"] = 0
        slot_data["map_card_fly_location"] = 0
        if self.options.free_fly_location:
            slot_data["free_fly_location"] = self.free_fly_location
            if self.options.free_fly_location > 1:
                slot_data["map_card_fly_location"] = self.map_card_fly_location

        return slot_data

    def write_spoiler(self, spoiler_handle) -> None:
        if self.options.randomize_starters:
            spoiler_handle.write(f"\n\nStarter Pokemon ({self.multiworld.player_name[self.player]}):\n\n")
            for evo in self.generated_starters:
                types_0 = ", ".join(self.generated_pokemon[evo[0]].types)
                types_1 = ", ".join(self.generated_pokemon[evo[1]].types)
                types_2 = ", ".join(self.generated_pokemon[evo[2]].types)
                spoiler_handle.write(f"{evo[0]} ({types_0}) -> {evo[1]} ({types_1}) -> {evo[2]} ({types_2})\n")

        if self.options.free_fly_location:
            free_fly_locations = {22: "Ecruteak City",
                                  21: "Olivine City",
                                  19: "Cianwood City",
                                  23: "Mahogany Town",
                                  25: "Blackthorn City",
                                  3: "Viridian City",
                                  4: "Pewter City",
                                  5: "Cerulean City",
                                  7: "Vermilion City",
                                  8: "Lavender Town",
                                  10: "Celadon City",
                                  9: "Saffron City",
                                  11: "Fuchsia City"}
            spoiler_handle.write(f"\n\nFree Fly Location ({self.multiworld.player_name[self.player]}): "
                                 f"{free_fly_locations[self.free_fly_location]}\n")
            if self.options.free_fly_location > 1:
                spoiler_handle.write(f"\n\nMap Card Fly Location ({self.multiworld.player_name[self.player]}): "
                                     f"{free_fly_locations[self.map_card_fly_location]}\n")

        if self.options.enable_mischief:
            spoiler_handle.write(f"\n\nMischief ({self.multiworld.player_name[self.player]}):\n\n")
            get_misc_spoiler_log(self, spoiler_handle.write)

    def create_item(self, name: str) -> PokemonCrystalItem:
        return self.create_item_by_code(self.item_name_to_id[name])

    def get_filler_item_name(self) -> str:
        item = get_random_filler_item(self.random)
        return item_const_name_to_label(item)

    def create_item_by_const_name(self, item_const: str) -> PokemonCrystalItem:
        item_code = item_const_name_to_id(item_const) + BASE_OFFSET
        return self.create_item_by_code(item_code)

    def create_item_by_code(self, item_code: int) -> PokemonCrystalItem:
        return PokemonCrystalItem(
            self.item_id_to_name[item_code],
            get_item_classification(item_code),
            item_code,
            self.player
        )
