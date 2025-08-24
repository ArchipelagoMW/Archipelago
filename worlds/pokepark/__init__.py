"""
Archipelago init file for Pokepark
"""
import os
import zipfile
from base64 import b64encode
from typing import Any, ClassVar, Callable

import yaml

from BaseClasses import Tutorial, Region
from BaseClasses import ItemClassification as IC

from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, Type, launch as launch_component
from .items import item_name_groups, PokeparkItem, ITEM_TABLE
from .locations import LOCATION_TABLE, MultiZoneFlag, PokeparkLocation, PokeparkFlag
from .options import PokeparkOptions, pokepark_option_groups
from .regions import REGION_TO_ENTRANCES, get_entrance_rules, get_entrances_to_exits, get_region_to_entrances
from .rules import set_rules
from ..Files import APPlayerContainer


class PokeparkWebWorld(WebWorld):
    theme = "jungle"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Pokepark Randomizer software on your computer."
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        [""]
    )]
    options_presets = {
        "Default": {
            "power_randomizer": 3,
            "starting_zone": 0,
            "goal": 0
        }
    }
    option_groups = pokepark_option_groups


class PokeparkContainer(APPlayerContainer):
    """
    This class defines the container file for The Wind Waker.
    """

    game: str = "PokePark"
    patch_file_ending: str = ".appkprk"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if "data" in kwargs:
            self.data = kwargs["data"]
            del kwargs["data"]

        super().__init__(*args, **kwargs)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        """
        Write the contents of the container file.
        """
        super().write_contents(opened_zipfile)

        # Record the data for the game under the key `plando`.
        opened_zipfile.writestr("plando", b64encode(bytes(yaml.safe_dump(self.data, sort_keys=False), "utf-8")))


class PokeparkWorld(World):
    """
    The first Pokepark game featuring 3D Gameplay controlling Pokemon.
    Lot of Minigames in the mission to save the Pokepark through the collection of Prism Shards.
    """
    game = "PokePark"

    options_dataclass = PokeparkOptions
    options: PokeparkOptions

    web = PokeparkWebWorld()

    item_name_to_id: ClassVar[dict[str, int]] = {
        name: PokeparkItem.get_apid(data.code) for name, data in ITEM_TABLE.items() if data.code is not None
    }
    location_name_to_id = {
        name: PokeparkItem.get_apid(data.code) for name, data in LOCATION_TABLE.items() if data.code is not None
    }
    origin_region_name: str = "Treehouse"

    item_name_groups: ClassVar[dict[str, set[str]]] = item_name_groups

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.locations: set[str] = set()
        self.nonprogress_locations: set[str] = set()
        self.item_classification_overrides: dict[str, IC] = {}

    def _determine_locations(self) -> set[str]:
        """
        Determine which locations included in the world based on the player's options.

        :return: A set containing the names of the locations
        """
        each_zone_filter = MultiZoneFlag.SINGLE if self.options.each_zone == self.options.each_zone.option_true else MultiZoneFlag.MULTI
        removable_location_flags = set()

        flag_options = [
            (PokeparkFlag.BATTLE, self.options.remove_battle_power_comp_locations),
            (PokeparkFlag.CHASE, self.options.remove_chase_power_comp_locations),
            (PokeparkFlag.QUIZ, self.options.remove_quiz_power_comp_locations),
            (PokeparkFlag.HIDEANDSEEK, self.options.remove_hide_and_seek_power_comp_locations),
            (PokeparkFlag.ERRAND, self.options.remove_errand_power_comp_locations),
            (PokeparkFlag.FRIENDSHIP, self.options.remove_misc_power_comp_locations),
            (PokeparkFlag.POWER_UP, self.options.remove_power_training_locations),
            (PokeparkFlag.QUEST, self.options.remove_quest_locations),
            (PokeparkFlag.ATTRACTION, self.options.remove_attraction_locations),
        ]

        for flag, option in flag_options:
            if option == option.option_true:
                removable_location_flags.add(flag)

        if self.options.goal == self.options.goal.option_mew:
            removable_location_flags.add(PokeparkFlag.POSTGAME)

        locations: set[str] = set()
        for location, data in LOCATION_TABLE.items():
            if (data.each_zone == each_zone_filter or
                    data.flags in removable_location_flags):
                pass
            else:
                locations.add(location)

        return locations

    def generate_early(self) -> None:
        options = self.options
        if options.goal == options.goal.option_postgame:
            self.options.remove_attraction_locations.value = self.options.remove_attraction_locations.option_true
        if not options.remove_attraction_locations:
            self.options.remove_chase_power_comp_locations.value = self.options.remove_chase_power_comp_locations.option_true
            self.options.remove_battle_power_comp_locations.value = self.options.remove_battle_power_comp_locations.option_true
            self.options.remove_hide_and_seek_power_comp_locations.value = self.options.remove_hide_and_seek_power_comp_locations.option_true
            self.options.remove_errand_power_comp_locations.value = self.options.remove_errand_power_comp_locations.option_true
            self.options.remove_misc_power_comp_locations.value = self.options.remove_misc_power_comp_locations.option_true
            self.options.remove_quest_locations.value = self.options.remove_quest_locations.option_true

        self.locations = self._determine_locations()

    def generate_output(self, output_directory: str) -> None:
        """
        Create the output Pokeprk file that is used to randomize the ISO.

        :param output_directory: The output directory for the Pokeprk file.
        """
        multiworld = self.multiworld
        player = self.player

        # Output seed name and slot number to seed RNG in randomizer client.
        output_data = {
            "Seed": multiworld.seed_name,
            "Slot": player,
            "Name": self.player_name,
            "Options": self.options.get_output_dict(),
            "Locations": {},
            "Entrances": {},
        }

        # Output the plando details to file.
        aptww = PokeparkContainer(
            path=os.path.join(
                output_directory, f"{multiworld.get_out_file_name_base(player)}{PokeparkContainer.patch_file_ending}"
            ),
            player=player,
            player_name=self.player_name,
            data=output_data,
        )
        aptww.write()

    def create_regions(self):
        multiworld = self.multiworld
        player = self.player
        options = self.options

        ENTRANCES_TO_EXITS = get_entrances_to_exits(options)
        REGION_TO_ENTRANCES = get_region_to_entrances(options)
        ENTRANCE_RULES = get_entrance_rules(player, options)

        treehouse = Region("Treehouse", player, multiworld)
        multiworld.regions.append(treehouse)
        unique_region_names = set(ENTRANCES_TO_EXITS.values())
        for _region_name in unique_region_names:
            multiworld.regions.append(Region(_region_name, player, multiworld))
        for region_map, entrances in REGION_TO_ENTRANCES.items():
            for entrance in entrances:
                target_region_name = ENTRANCES_TO_EXITS.get(entrance)
                target_region = multiworld.get_region(target_region_name, player)
                print(f"{region_map} -> {target_region}")
                multiworld.get_region(region_map, player).connect(
                    target_region
                    , f"{entrance} ->"
                      f" {target_region_name}", ENTRANCE_RULES[entrance]
                )
        for location_name in sorted(self.locations):
            data = LOCATION_TABLE[location_name]

            region = self.get_region(data.region)
            location = PokeparkLocation(player, location_name, region, data)

            region.locations.append(location)

    def set_rules(self) -> None:
        set_rules(self)

    def create_item(self, name: str) -> PokeparkItem:
        if name in ITEM_TABLE:
            if self.item_classification_overrides.__contains__(name):
                classification = self.item_classification_overrides.get(name)
            else:
                classification = ITEM_TABLE[name].classification
            return PokeparkItem(name, self.player, ITEM_TABLE[name], classification)
        raise KeyError(f"Invalid item name: {name}")

    def update_pool_with_precollected_items(self) -> tuple[list[str], list[str]]:
        options = self.options
        progressive_pool = []
        precollected_pool = []

        for item_name, data in ITEM_TABLE.items():
            if data.type == "Item":
                progressive_pool.extend([item_name] * data.quantity)

        if options.power_randomizer == options.power_randomizer.option_dash:
            precollected_pool.append("Progressive Dash")
            progressive_pool.remove("Progressive Dash")
        if options.power_randomizer == options.power_randomizer.option_thunderbolt:
            precollected_pool.append("Progressive Thunderbolt")
            progressive_pool.remove("Progressive Thunderbolt")
        if options.power_randomizer == options.power_randomizer.option_thunderbolt_dash:
            precollected_pool.append("Progressive Thunderbolt")
            progressive_pool.remove("Progressive Thunderbolt")
            precollected_pool.append("Progressive Dash")
            progressive_pool.remove("Progressive Dash")
        if options.power_randomizer == options.power_randomizer.option_full:
            for i in range(4):
                precollected_pool.append("Progressive Thunderbolt")
                progressive_pool.remove("Progressive Thunderbolt")
                precollected_pool.append("Progressive Dash")
                progressive_pool.remove("Progressive Dash")
            for i in range(3):
                precollected_pool.append("Progressive Iron Tail")
                progressive_pool.remove("Progressive Iron Tail")
                precollected_pool.append("Progressive Health")
                progressive_pool.remove("Progressive Health")
            precollected_pool.append("Double Dash")
            progressive_pool.remove("Double Dash")

        if options.starting_zone == options.starting_zone.option_one:
            fast_travel_items = [
                "Meadow Zone Fast Travel",
                "Beach Zone Fast Travel",
                "Ice Zone Fast Travel",
                "Cavern Zone Fast Travel",
                "Magma Zone Fast Travel",
                "Haunted Zone Fast Travel",
                "Granite Zone Fast Travel",
                "Flower Zone Fast Travel",
            ]
            self.random.shuffle(fast_travel_items)
            precollected_fast_travel = self.random.choice(fast_travel_items)
            precollected_pool.append(precollected_fast_travel)
            progressive_pool.remove(precollected_fast_travel)

        if options.starting_zone == options.starting_zone.option_all:
            fast_travel_items = [
                "Meadow Zone Fast Travel",
                "Beach Zone Fast Travel",
                "Ice Zone Fast Travel",
                "Cavern Zone Fast Travel",
                "Magma Zone Fast Travel",
                "Haunted Zone Fast Travel",
                "Granite Zone Fast Travel",
                "Flower Zone Fast Travel",
            ]
            for item in fast_travel_items:
                precollected_pool.append(item)
                progressive_pool.remove(item)

        if not options.in_zone_road_blocks:
            road_block_items = [
                "Beach Bridge 1 Unlock",
                "Beach Bridge 2 Unlock",
                "Magma Zone Fire Wall Unlock",
                "Haunted Zone Mansion Doors Unlock"
            ]
            for item in road_block_items:
                precollected_pool.append(item)
                progressive_pool.remove(item)

        return progressive_pool, precollected_pool

    def update_classification(self):
        # mostly documentation items -> options for now
        options = self.options
        min_required_friendship_count = 0
        progressive_items = [
            "Bulbasaur Prisma",
            "Venusaur Prisma",
            "Pelipper Prisma",
            "Gyarados Prisma",
            "Empoleon Prisma",
            "Bastiodon Prisma",
            "Rhyperior Prisma",
            "Blaziken Prisma",
            "Tangrowth Prisma",
            "Dusknoir Prisma",
            "Rotom Prisma",
            "Absol Prisma",
            "Salamence Prisma",
            "Rayquaza Prisma",

            "Prinplup Friendship",  # Lower Lift Area

            "Beach Zone Fast Travel",
            "Ice Zone Fast Travel",
            "Cavern Zone Fast Travel",
            "Magma Zone Fast Travel",
            "Haunted Zone Fast Travel",
            "Granite Zone Fast Travel",
            "Flower Zone Fast Travel",

            "Beach Bridge 1 Unlock",
            "Beach Bridge 2 Unlock",
            "Magma Zone Fire Wall Unlock",
            "Haunted Zone Mansion Doors Unlock",

            "Progressive Dash",
            "Progressive Thunderbolt",

            "Victory"
        ]

        if not options.remove_attraction_locations:
            min_required_friendship_count = max(min_required_friendship_count, 80)

            progressive = [
                # Attraction stuff
                "Shaymin Friendship",
                "Lopunny Friendship",
                "Lucario Friendship",
                "Infernape Friendship",
                "Espeon Friendship",
                "Absol Friendship",
                "Ponyta Friendship",
                "Ninetales Friendship",
                "Breloom Friendship",
                "Riolu Friendship",
                "Furret Friendship",
                "Mareep Friendship",
                "Eevee Friendship",
                "Vulpix Friendship",
                "Chikorita Friendship",
                "Deoxys Friendship",
                "Floatzel Friendship",
                "Glaceon Friendship",
                "Luxray Friendship",
                "Rhyperior Friendship",
                "Mamoswine Friendship",
                "Totodile Friendship",
                "Cyndaquil Friendship",
                "Mime Jr. Friendship",
                "Jirachi Friendship",
                "Blaziken Friendship",
                "Tangrowth Friendship",
                "Primeape Friendship",
                "Ambipom Friendship",
                "Mankey Friendship",
                "Aipom Friendship",
                "Chimchar Friendship",
                "Treecko Friendship",
                "Croagunk Friendship",
                "Pachirisu Friendship",
                "Munchlax Friendship",
                "Magikarp Friendship",
                "Celebi Friendship",
                "Sneasel Friendship",
                "Electabuzz Friendship",
                "Raichu Friendship",
                "Meowth Friendship",
                "Pichu Friendship",
                "Darkrai Friendship",
                "Gengar Friendship",
                "Mismagius Friendship",
                "Scizor Friendship",
                "Dusknoir Friendship",
                "Umbreon Friendship",
                "Krabby Friendship",
                "Electrode Friendship",
                "Cranidos Friendship",
                "Skuntank Friendship",
                "Misdreavus Friendship",
                "Gastly Friendship",
                "Stunky Friendship",
                "Duskull Friendship",
                "Manaphy Friendship",
                "Empoleon Friendship",
                "Feraligatr Friendship",
                "Golduck Friendship",
                "Vaporeon Friendship",
                "Prinplup Friendship",
                "Bibarel Friendship",
                "Corsola Friendship",
                "Buizel Friendship",
                "Piplup Friendship",
                "Lotad Friendship",
                "Psyduck Friendship",
                "Azurill Friendship",
                "Slowpoke Friendship",
                "Latias Friendship",
                "Staraptor Friendship",
                "Togekiss Friendship",
                "Honchkrow Friendship",
                "Staravia Friendship",
                "Pidgeotto Friendship",
                "Gliscor Friendship",
                "Taillow Friendship",
                "Spearow Friendship",
                "Pelipper Friendship",
                "Starly Friendship",
                "Murkrow Friendship",
                "Wingull Friendship",
                "Tropius Friendship",
                "Butterfree Friendship",
                "Suicune Friendship",
                "Blastoise Friendship",
                "Glalie Friendship",
                "Lapras Friendship",
                "Delibird Friendship",
                "Quagsire Friendship",
                "Squirtle Friendship",
                "Spheal Friendship",
                "Piloswine Friendship",
                "Teddiursa Friendship",
                "Metagross Friendship",
                "Hitmonlee Friendship",
                "Electivire Friendship",
                "Magmortar Friendship",
                "Ursaring Friendship",
                "Sableye Friendship",
                "Mr. Mime Friendship",
                "Sudowoodo Friendship",
                "Charmander Friendship",
                "Gible Friendship",
                "Torchic Friendship",
                "Magby Friendship",
                "Heatran Friendship",
                "Tyranitar Friendship",
                "Hitmontop Friendship",
                "Flareon Friendship",
                "Venusaur Friendship",
                "Snorlax Friendship",
                "Torterra Friendship",
                "Magnezone Friendship",
                "Claydol Friendship",
                "Quilava Friendship",
                "Torkoal Friendship",
                "Baltoy Friendship",
                "Bonsly Friendship",
                "Magnemite Friendship",
                "Groudon Friendship",
                "Garchomp Friendship",
                "Hitmonchan Friendship",
                "Machamp Friendship",
                "Bastiodon Friendship",
                "Marowak Friendship",
                "Camerupt Friendship",
                "Mawile Friendship",
                "Farfetch'd Friendship",
                "Geodude Friendship",
                "Phanpy Friendship",
                "Rotom Friendship",
                "Porygon-Z Friendship",
                "Haunter Friendship",
                "Abra Friendship",
                "Elekid Friendship",
                "Latios Friendship",
                "Salamence Friendship",
                "Charizard Friendship",
                "Dragonite Friendship",
                "Flygon Friendship",
                "Aerodactyl Friendship",
                "Golbat Friendship",
                "Zubat Friendship",
                "Mew Friendship",
                "Arcanine Friendship",
                "Jolteon Friendship",
                "Leafeon Friendship",
                "Scyther Friendship",
                "Shinx Friendship",
                "Buneary Friendship",
                "Turtwig Friendship",
                "Bulbasaur Friendship",
                "Bidoof Friendship",
                "Oddish Friendship",
                "Shroomish Friendship",
                "Weedle Friendship",
                "Caterpie Friendship",
                "Dusknoir Unlock",
                "Rayquaza Unlock",
                "Pikachu Surfboard",
                "Pikachu Snowboard",
                "Pikachu Balloon",
            ]
            progressive_items.extend(progressive)

        if not options.remove_battle_power_comp_locations:
            min_required_friendship_count = max(min_required_friendship_count, 60)
            progressive = [
                "Lotad Unlock",
                "Weedle Unlock",
                "Bibarel Unlock",
                "Torterra Unlock",
                "Scyther Unlock",
                "Chimchar Unlock",
                "Ambipom Unlock",
                "Totodile Unlock",
                "Golduck Unlock",
                "Blastoise Unlock",
                "Floatzel Unlock",
                "Krabby Unlock",
                "Corphish Unlock",
                "Smoochum Unlock",
                "Squirtle Unlock",
                "Primeape Unlock",
                "Ursaring Unlock",
                "Mamoswine Unlock",
                "Magnezone Unlock",
                "Scizor Unlock",
                "Phanpy Unlock",
                "Hitmonlee Unlock",
                "Electivire Unlock",
                "Infernape Unlock",
                "Torkoal Unlock",
                "Hitmonchan Unlock",
                "Magmortar Unlock",
                "Baltoy Unlock",
                "Honchkrow Unlock",
                "Elekid Unlock",
                "Electabuzz Unlock",
                "Skuntank Unlock",
                "Breloom Unlock",
                "Mismagius Unlock",
                "Gengar Unlock",
                "Aerodactyl Unlock",
                "Tyranitar Unlock",
                "Garchomp Unlock",

                "Progressive Iron Tail",
                "Progressive Health"
            ]
            progressive_items.extend(progressive)

        if not options.remove_chase_power_comp_locations:
            min_required_friendship_count = max(min_required_friendship_count, 100)

            progressive = [
                "Pachirisu Unlock",
                "Shinx Unlock",
                "Caterpie Unlock",
                "Shroomish Unlock",
                "Leafeon Unlock",
                "Starly Unlock",
                "Starly 2 Unlock",
                "Sneasel Unlock",
                "Raichu Unlock",
                "Ninetales Unlock",
                "Ponyta Unlock",
                "Espeon Unlock",
                "Voltorb Unlock",
                "Luxray Unlock",
                "Stunky Unlock",
                "Electrode Unlock",
                "Haunter Unlock",
                "Gastly Unlock",
                "Gastly 2 Unlock",
                "Jolteon Unlock",
            ]
            progressive_items.extend(progressive)

        if not options.remove_quiz_power_comp_locations:
            min_required_friendship_count = max(min_required_friendship_count, 0)

        if not options.remove_hide_and_seek_power_comp_locations:
            min_required_friendship_count = max(min_required_friendship_count, 0)
            progressive = [
                "Bonsly Unlock",
                "Sudowoodo Unlock",
                "Mudkip Unlock",
            ]
            progressive_items.extend(progressive)

        if not options.remove_errand_power_comp_locations:
            min_required_friendship_count = max(min_required_friendship_count, 0)
            progressive = [
                "Tropius Unlock",
            ]
            progressive_items.extend(progressive)

        if not options.remove_misc_power_comp_locations:
            min_required_friendship_count = max(min_required_friendship_count, 0)

            progressive = [
                "Magnemite Unlock",
                "Magnemite 2 Unlock",
                "Magnemite 3 Unlock",
                "Golem Unlock",
                "Metapod Unlock",
                "Kakuna Unlock",
            ]
            progressive_items.extend(progressive)

        if not options.remove_quest_locations:
            min_required_friendship_count = max(min_required_friendship_count, 0)

            progressive = [
                "Mankey Friendship",
                "Delibird Unlock",
                "Spheal Friendship",
                "Teddiursa Friendship",
                "Squirtle Unlock",
                "Squirtle Friendship",
                "Smoochum Friendship",
                "Smoochum Unlock",
                "Glalie Unlock"
            ]
            progressive_items.extend(progressive)

        if options.goal == options.goal.option_postgame:
            min_required_friendship_count = max(min_required_friendship_count, 193)

        progressive_set = set(progressive_items)

        friendship_items = {
            name: data for name, data in ITEM_TABLE.items()
            if "Friendship" in name
        }
        max_removable_friendship_items = 193 - min_required_friendship_count
        removable_friendship_items = [name for name in friendship_items.keys()
                                      if name not in progressive_set
                                      ][:max_removable_friendship_items]
        for name in removable_friendship_items:
            self.item_classification_overrides[name] = IC.filler

        removable_items = {
            name: data for name, data in ITEM_TABLE.items()
            if "Friendship" not in name and name not in progressive_set
        }
        for name in removable_items:
            self.item_classification_overrides[name] = IC.filler

    def create_items(self):

        progressive_pool, precollected_pool = self.update_pool_with_precollected_items()

        for item in precollected_pool:
            self.multiworld.push_precollected(self.create_item(item))

        if self.options.goal == self.options.goal.option_mew:
            location = self.get_location("Skygarden - Mew Power Competition -- Friendship")
            location.place_locked_item(
                self.create_item(
                    "Victory"
                )
            )
            location.address = None
        elif self.options.goal == self.options.goal.option_postgame:
            location = self.get_location("Skygarden - Prisma Completion -- Completed")
            location.place_locked_item(
                self.create_item(
                    "Victory"
                )
            )
            location.address = None

        print(f"progressive pool len: {len(progressive_pool)}")
        remaining_slots = len(self.multiworld.get_unfilled_locations(self.player)) - len(progressive_pool)
        for i in range(remaining_slots):
            if i % 20 == 0:
                progressive_pool.append("100 Berries")
            elif i % 8 == 0:
                progressive_pool.append("50 Berries")
            elif i % 4 == 0:
                progressive_pool.append("20 Berries")
            else:
                progressive_pool.append("10 Berries")

        self.random.shuffle(progressive_pool)

        self.update_classification()

        for item in progressive_pool:
            self.multiworld.itempool.append(self.create_item(item))



def launch_client():
    from .PokeparkClient import main
    launch_component(main, name="Pokepark client")


components.append(Component("Pokepark Client", "PokeparkClient",
                            func=launch_client, component_type=Type.CLIENT))
