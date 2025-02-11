from typing import Any, Dict, TextIO

from BaseClasses import Tutorial
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from .coordinates import coordinate_description, generate_random_coordinates
from .db_layout import generate_random_db_layout
from .items import OuterWildsItem, all_non_event_items_table, item_name_groups, create_item, create_items
from .locations_and_regions import all_non_event_locations_table, location_name_groups, create_regions
from .options import OuterWildsGameOptions, RandomizeDarkBrambleLayout, Spawn, Goal, EnableEchoesOfTheEyeDLC
from .orbits import generate_random_orbits, generate_random_rotations
from .warp_platforms import generate_random_warp_platform_mapping


class OuterWildsWebWorld(WebWorld):
    theme = "dirt"
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to playing Outer Wilds.",
            language="English",
            file_name="guide_en.md",
            link="guide/en",
            authors=["Ixrec"]
        )
    ]


class OuterWildsWorld(World):
    game = "Outer Wilds"
    web = OuterWildsWebWorld()

    eotu_coordinates = 'vanilla'
    db_layout = 'vanilla'
    planet_order = 'vanilla'
    orbit_angles = 'vanilla'
    rotation_axes = 'vanilla'
    warps = 'vanilla'
    spawn = Spawn.option_vanilla

    # this is how we tell the Universal Tracker we want to use re_gen_passthrough
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data

    def generate_early(self) -> None:
        # apply options that edit other options or themselves
        if self.options.dlc_only:
            self.options.enable_eote_dlc = EnableEchoesOfTheEyeDLC(1)
            self.options.spawn = Spawn(Spawn.option_stranger)
            self.options.goal = Goal(Goal.option_echoes_of_the_eye)

        if self.options.spawn == Spawn.option_random_non_vanilla:
            max_spawn = Spawn.option_stranger if self.options.enable_eote_dlc else Spawn.option_giants_deep
            self.options.spawn = Spawn(self.random.choice(range(Spawn.option_hourglass_twins, max_spawn + 1)))

        # validate options
        if not self.options.enable_eote_dlc:
            if self.options.spawn == Spawn.option_stranger:
                raise OptionError('Incompatible options: stranger spawn requires enable_eote_dlc to be true')
            if self.options.goal in [
                Goal.option_song_of_the_stranger,
                Goal.option_song_of_six,
                Goal.option_song_of_seven,
                Goal.option_echoes_of_the_eye
            ]:
                raise OptionError('Incompatible options: goal %s requires enable_eote_dlc to be true', self.options.goal)

        if self.options.shuffle_spacesuit and self.options.spawn != Spawn.option_vanilla:
            raise OptionError('Incompatible options: shuffle_spacesuit is true and spawn is non-vanilla (%s)', self.options.spawn)

        # When Universal Tracker is not involved, spawn is just a normal option.
        # But we also run this before the UT check because if we're in UT's 1st pass, we won't have slot_data's spawn
        # yet, and we still need to set this to avoid a DLC-only slot from thinking it has vanilla spawn and crashing
        # when items.py tries to lock Launch Codes on a location that doesn't exist.
        self.spawn = self.options.spawn

        # implement Universal Tracker support
        if hasattr(self.multiworld, "generation_is_fake"):
            if hasattr(self.multiworld, "re_gen_passthrough"):
                if "Outer Wilds" in self.multiworld.re_gen_passthrough:
                    slot_data = self.multiworld.re_gen_passthrough["Outer Wilds"]
                    self.warps = slot_data["warps"]
                    self.spawn = slot_data["spawn"]
            return

        # generate game-specific randomizations separate from AP items/locations
        self.eotu_coordinates = generate_random_coordinates(self.random) \
            if self.options.randomize_coordinates else "vanilla"
        self.warps = generate_random_warp_platform_mapping(self.random, self.options) \
            if self.options.randomize_warp_platforms else "vanilla"
        (self.planet_order, self.orbit_angles) = generate_random_orbits(self.random, self.options) \
            if self.options.randomize_orbits else ("vanilla", "vanilla")
        self.rotation_axes = generate_random_rotations(self.random) \
            if self.options.randomize_rotations else "vanilla"

        db_option = self.options.randomize_dark_bramble_layout
        self.db_layout = generate_random_db_layout(self.random, db_option) \
            if db_option != RandomizeDarkBrambleLayout.option_false else "vanilla"

    # members and methods implemented by locations_and_regions.py, locations.jsonc and connections.jsonc

    location_name_to_id = all_non_event_locations_table
    location_name_groups = location_name_groups

    def create_regions(self) -> None:
        create_regions(self)

    # members and methods implemented by items.py and items.jsonc

    item_name_to_id = all_non_event_items_table
    item_name_groups = item_name_groups

    def create_item(self, name: str) -> OuterWildsItem:
        return create_item(self.player, name)

    def create_items(self) -> None:
        create_items(self)

    def get_filler_item_name(self) -> str:
        # Used in corner cases (e.g. plando, item_links, start_inventory_from_pool)
        # where even a well-behaved world may end up "missing" items.
        # Technically this "should" be a random choice among all filler/trap items
        # the world is configured to have, but it's not worth that much effort.
        return "Marshmallow"

    # members and methods related to options.py

    options_dataclass = OuterWildsGameOptions
    options: OuterWildsGameOptions

    # miscellaneous smaller methods

    def set_rules(self) -> None:
        # here we only set the completion condition; all the location/region rules were set in create_regions()
        option_key_to_item_name = {
            'song_of_five':         "Victory - Song of Five",
            'song_of_the_nomai':    "Victory - Song of the Nomai",
            'song_of_the_stranger': "Victory - Song of the Stranger",
            'song_of_six':          "Victory - Song of Six",
            'song_of_seven':        "Victory - Song of Seven",
            'echoes_of_the_eye':    "Victory - Echoes of the Eye",
        }

        goal_item = option_key_to_item_name[self.options.goal.current_key]
        self.multiworld.completion_condition[self.player] = lambda state: state.has(goal_item, self.player)

    def fill_slot_data(self):
        slot_data = self.options.as_dict(
            "death_link",                   # a client/mod feature
            "goal", "spawn",                             # affects tons of stuff, but also a client/mod faeture
            "logsanity", "enable_eote_dlc", "dlc_only",  # changes AP locations, needed by in-game tracker
            "enable_hn1_mod", "enable_hn2_mod",
            "enable_outsider_mod", "enable_ac_mod", "enable_fq_mod",
            "split_translator"                           # changes AP items, and how client/mod implements Translator
        )
        # more client/mod features, these are only in the apworld because we want them fixed per-slot/at gen time
        slot_data["eotu_coordinates"] = self.eotu_coordinates
        slot_data["db_layout"] = self.db_layout
        slot_data["planet_order"] = self.planet_order
        slot_data["orbit_angles"] = self.orbit_angles
        slot_data["rotation_axes"] = self.rotation_axes
        slot_data["warps"] = self.warps
        # Archipelago does not yet have apworld versions (data_version is deprecated),
        # so we have to roll our own with slot_data for the time being
        slot_data["apworld_version"] = "0.3.11"
        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.eotu_coordinates != 'vanilla':
            spoiler_handle.write('\nRandomized Coordinates for %s:'
                                 '\n\n%s\n%s\n%s\n' % (self.multiworld.player_name[self.player],
                                                       coordinate_description(self.eotu_coordinates[0]),
                                                       coordinate_description(self.eotu_coordinates[1]),
                                                       coordinate_description(self.eotu_coordinates[2])))
        if self.db_layout != 'vanilla':
            spoiler_handle.write('\nRandomized Dark Bramble Layout for %s:'
                                 '\nRoom names are (H)ub, (E)scapePod, (A)nglerNest, '
                                 '(P)ioneer, E(X)itOnly, (V)essel, (C)luster, (S)mallNest'
                                 '\n\n%s\n' % (self.multiworld.player_name[self.player],
                                               self.db_layout.replace('|', '\n')))
        if self.planet_order != 'vanilla':
            spoiler_handle.write('\nRandomized Orbits for %s:'
                                 '\n\nPlanet Order: %s\nOrbit Angles: %s\nRotation Axes: %s\n' %
                                 (self.multiworld.player_name[self.player],
                                  self.planet_order, self.orbit_angles, self.rotation_axes))
        if self.warps != 'vanilla':
            spoiler_handle.write('\nRandomized Warp Platforms for %s:'
                                 '\n\n%s\n' %
                                 (self.multiworld.player_name[self.player],
                                  self.warps))
