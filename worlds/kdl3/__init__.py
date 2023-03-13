from BaseClasses import Tutorial, ItemClassification, Entrance, Region, MultiWorld
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule
from .Items import item_table, item_names, copy_ability_table, animal_friend_table, filler_item_weights, KDL3Item
from .Locations import location_table, KDL3Location, stage_locations
from .Options import kdl3_options
from .Names import LocationName
from .Rom import KDL3DeltaPatch, get_base_rom_path, RomData, patch_rom
from .Client import KDL3SNIClient

import os
import math
import threading
import base64


class KDL3WebWorld(WebWorld):
    theme = "party"
    tutorials = [
        """
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Kirby's Dream Land 3 randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Silvris"]
        )"""
    ]


class KDL3World(World):
    """
    Join Kirby and his Animal Friends on an adventure to collect Heart Stars and drive Dark Matter away from Dream Land!
    """

    game: str = "Kirby's Dream Land 3"
    option_definitions = kdl3_options
    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = {location_table[location]: location for location in location_table}
    data_version = 0
    web = KDL3WebWorld()
    boss_requirements = dict()

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        rom_file: str = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(f"Could not find base ROM for {cls.game}: {rom_file}")

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        start = Entrance(self.player, "Start Game", menu)
        menu.exits.append(start)
        level1 = Region("Grass Land", self.player, self.multiworld)
        level2 = Region("Ripple Field", self.player, self.multiworld)
        level3 = Region("Sand Canyon", self.player, self.multiworld)
        level4 = Region("Cloudy Park", self.player, self.multiworld)
        level5 = Region("Iceberg", self.player, self.multiworld)
        level6 = Region("Hyper Zone", self.player, self.multiworld)
        start.connect(level1)
        if False:  # self.multiworld.level_shuffle[self.player].value != 0:
            return
        else:
            for location in location_table:
                if (location & 0x000200) == 0:
                    idx = location & 0x0000FF
                    if idx <= 6:
                        level1.locations.append(KDL3Location(self.player, location_table[location], location, level1))
                    elif idx <= 12:
                        level2.locations.append(KDL3Location(self.player, location_table[location], location, level2))
                    elif idx <= 18:
                        level3.locations.append(KDL3Location(self.player, location_table[location], location, level3))
                    elif idx <= 24:
                        level4.locations.append(KDL3Location(self.player, location_table[location], location, level4))
                    elif idx <= 30:
                        level5.locations.append(KDL3Location(self.player, location_table[location], location, level5))
        level1.locations.append(KDL3Location(self.player, LocationName.grass_land_whispy, 0x770200, level1))
        level2.locations.append(KDL3Location(self.player, LocationName.ripple_field_acro, 0x770201, level2))
        level3.locations.append(KDL3Location(self.player, LocationName.sand_canyon_poncon, 0x770202, level3))
        level4.locations.append(KDL3Location(self.player, LocationName.cloudy_park_ado, 0x770203, level4))
        level5.locations.append(KDL3Location(self.player, LocationName.iceberg_dedede, 0x770204, level5))
        level1.locations.append(KDL3Location(self.player, "Level 1 Boss", None, level1))
        level2.locations.append(KDL3Location(self.player, "Level 2 Boss", None, level2))
        level3.locations.append(KDL3Location(self.player, "Level 3 Boss", None, level3))
        level4.locations.append(KDL3Location(self.player, "Level 4 Boss", None, level4))
        level5.locations.append(KDL3Location(self.player, "Level 5 Boss", None, level5))
        if self.multiworld.goal[self.player] == 1:
            level6.locations.append(KDL3Location(self.player, LocationName.boss_butch, None, level6))
        else:
            level6.locations.append(KDL3Location(self.player, LocationName.hyper_zone, None, level6))
        tlv2 = Entrance(self.player, "To Level 2", level1)
        level1.exits.append(tlv2)
        tlv2.connect(level2)
        tlv3 = Entrance(self.player, "To Level 3", level1)
        level2.exits.append(tlv3)
        tlv3.connect(level3)
        tlv4 = Entrance(self.player, "To Level 4", level1)
        level3.exits.append(tlv4)
        tlv4.connect(level4)
        tlv5 = Entrance(self.player, "To Level 5", level1)
        level4.exits.append(tlv5)
        tlv5.connect(level5)
        tlv6 = Entrance(self.player, "To Level 6", level1)
        level5.exits.append(tlv6)
        tlv6.connect(level6)
        self.multiworld.regions += [menu, level1, level2, level3, level4, level5, level6]

    def create_item(self, name: str, force_non_progression=False) -> KDL3Item:
        item = item_table[name]
        classification = ItemClassification.filler
        if item.progression and not force_non_progression:
            classification = ItemClassification.progression_skip_balancing \
                if item.skip_balancing else ItemClassification.progression
        return KDL3Item(name, classification, item.code, self.player)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choices(list(filler_item_weights.keys()),
                                              weights=list(filler_item_weights.values()))[0]

    def create_items(self) -> None:
        itempool = []
        itempool.extend([self.create_item(name) for name in copy_ability_table])
        itempool.extend([self.create_item(name) for name in animal_friend_table])
        required_percentage = self.multiworld.heart_stars_required[self.player].value / 100.0
        remaining_items = len(location_table) - len(itempool)
        total_heart_stars = self.multiworld.total_heart_stars[self.player].value
        required_heart_stars = math.floor(total_heart_stars * required_percentage)
        filler_items = total_heart_stars - required_heart_stars
        filler_amount = math.floor(filler_items * (self.multiworld.filler_percentage[self.player].value / 100.0))
        nonrequired_heart_stars = filler_items - filler_amount
        # handle boss requirements here
        requirements = [required_heart_stars]
        for i in range(4):
            requirements.append(self.multiworld.per_slot_randoms[self.player].randint(
                min(3, required_heart_stars), required_heart_stars))
        self.boss_requirements[self.player] = requirements
        itempool.extend([self.create_item("Heart Star") for _ in range(required_heart_stars)])
        itempool.extend([self.create_item(self.get_filler_item_name())
                         for _ in range(filler_amount + (remaining_items - total_heart_stars))])
        itempool.extend([self.create_item("Heart Star", True) for _ in range(nonrequired_heart_stars)])
        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        for stage in stage_locations:
            set_rule(self.multiworld.get_location(stage_locations[stage], self.player),
                     lambda state, prev=stage - 1: True if prev == 0x770000
                     else state.can_reach(stage_locations[prev], "Location", self.player))

        # Level 1
        set_rule(self.multiworld.get_location(LocationName.grass_land_muchi, self.player),
                 lambda state: state.has("ChuChu", self.player))
        set_rule(self.multiworld.get_location(LocationName.grass_land_chao, self.player),
                 lambda state: state.has("Stone", self.player))
        set_rule(self.multiworld.get_location(LocationName.grass_land_mine, self.player),
                 lambda state: state.has("Kine", self.player))
        set_rule(self.multiworld.get_entrance("To Level 2", self.player),
                 lambda state: state.can_reach(LocationName.grass_land_6, "Location", self.player))
        # Level 2
        add_rule(self.multiworld.get_location(LocationName.ripple_field_5, self.player),
                 lambda state: state.has("Kine", self.player))
        set_rule(self.multiworld.get_location(LocationName.ripple_field_kamuribana, self.player),
                 lambda state: state.has("Pitch", self.player) and state.has("Clean", self.player))
        set_rule(self.multiworld.get_location(LocationName.ripple_field_bakasa, self.player),
                 lambda state: state.has("Kine", self.player) and state.has("Parasol", self.player))
        set_rule(self.multiworld.get_location(LocationName.ripple_field_toad, self.player),
                 lambda state: state.has("Needle", self.player))
        set_rule(self.multiworld.get_location(LocationName.ripple_field_mama_pitch, self.player),
                 lambda state: state.has("Pitch", self.player) and state.has("Kine", self.player))
        set_rule(self.multiworld.get_entrance("To Level 3", self.player),
                 lambda state: state.can_reach(LocationName.ripple_field_6, "Location", self.player))

        # Level 3
        set_rule(self.multiworld.get_location(LocationName.sand_canyon_auntie, self.player),
                 lambda state: state.has("Clean", self.player))
        set_rule(self.multiworld.get_location(LocationName.sand_canyon_nyupun, self.player),
                 lambda state: state.has("ChuChu", self.player))
        set_rule(self.multiworld.get_location(LocationName.sand_canyon_rob, self.player),
                 lambda state: (state.has("Kine", self.player) or state.has("Coo", self.player))
                               and state.has("Parasol", self.player)
                               and state.has("Stone", self.player)
                 )
        set_rule(self.multiworld.get_entrance("To Level 4", self.player),
                 lambda state: state.can_reach(LocationName.sand_canyon_6, "Location", self.player))

        # Level 4
        set_rule(self.multiworld.get_location(LocationName.cloudy_park_hibanamodoki, self.player),
                 lambda state: state.has("Coo", self.player) and state.has("Clean", self.player))
        set_rule(self.multiworld.get_location(LocationName.cloudy_park_piyokeko, self.player),
                 lambda state: state.has("Needle", self.player))
        set_rule(self.multiworld.get_location(LocationName.cloudy_park_mikarin, self.player),
                 lambda state: state.has("Coo", self.player))
        set_rule(self.multiworld.get_location(LocationName.cloudy_park_pick, self.player),
                 lambda state: state.has("Rick", self.player))
        set_rule(self.multiworld.get_entrance("To Level 5", self.player),
                 lambda state: state.can_reach(LocationName.cloudy_park_6, "Location", self.player))

        # Level 5
        set_rule(self.multiworld.get_location(LocationName.iceberg_kogoesou, self.player),
                 lambda state: state.has("Burning", self.player))
        set_rule(self.multiworld.get_location(LocationName.iceberg_samus, self.player),
                 lambda state: state.has("Ice", self.player))
        set_rule(self.multiworld.get_location(LocationName.iceberg_name, self.player),
                 lambda state: state.has("Coo", self.player) and state.has("Burning", self.player))
        set_rule(self.multiworld.get_location(LocationName.iceberg_shiro, self.player),
                 lambda state: state.has("Nago", self.player))
        set_rule(self.multiworld.get_location(LocationName.iceberg_angel, self.player),
                 lambda state: state.has("Copy Ability", self.player, 8))  # easier than writing out 8 ands

        set_rule(self.multiworld.get_location("Level 1 Boss", self.player),
                 lambda state: state.has("Heart Star", self.player, self.boss_requirements[self.player][0]))
        set_rule(self.multiworld.get_location(LocationName.grass_land_whispy, self.player),
                 lambda state: state.has("Heart Star", self.player, self.boss_requirements[self.player][0]))
        set_rule(self.multiworld.get_location("Level 2 Boss", self.player),
                 lambda state: state.has("Heart Star", self.player, self.boss_requirements[self.player][1]))
        set_rule(self.multiworld.get_location(LocationName.ripple_field_acro, self.player),
                 lambda state: state.has("Heart Star", self.player, self.boss_requirements[self.player][1]))
        set_rule(self.multiworld.get_location("Level 3 Boss", self.player),
                 lambda state: state.has("Heart Star", self.player, self.boss_requirements[self.player][2]))
        set_rule(self.multiworld.get_location(LocationName.sand_canyon_poncon, self.player),
                 lambda state: state.has("Heart Star", self.player, self.boss_requirements[self.player][2]))
        set_rule(self.multiworld.get_location("Level 4 Boss", self.player),
                 lambda state: state.has("Heart Star", self.player, self.boss_requirements[self.player][3]))
        set_rule(self.multiworld.get_location(LocationName.cloudy_park_ado, self.player),
                 lambda state: state.has("Heart Star", self.player, self.boss_requirements[self.player][3]))
        set_rule(self.multiworld.get_location("Level 5 Boss", self.player),
                 lambda state: state.has("Heart Star", self.player, self.boss_requirements[self.player][4]))
        set_rule(self.multiworld.get_location(LocationName.iceberg_dedede, self.player),
                 lambda state: state.has("Heart Star", self.player, self.boss_requirements[self.player][4]))

        set_rule(self.multiworld.get_entrance("To Level 6", self.player),
                 lambda state: state.has("Level 1 Boss Purified", self.player)
                               and state.has("Level 2 Boss Purified", self.player)
                               and state.has("Level 3 Boss Purified", self.player)
                               and state.has("Level 4 Boss Purified", self.player)
                               and state.has("Level 5 Boss Purified", self.player))

    def generate_basic(self) -> None:
        goal = self.multiworld.goal[self.player].value
        goal_location = self.multiworld.get_location(LocationName.boss_butch, self.player) \
            if goal == 1 else self.multiworld.get_location(LocationName.hyper_zone, self.player)
        goal_location.place_locked_item(KDL3Item("Love-Love Rod", ItemClassification.progression, None, self.player))
        self.multiworld.get_location("Level 1 Boss", self.player) \
            .place_locked_item(KDL3Item("Level 1 Boss Purified", ItemClassification.progression, None, self.player))
        self.multiworld.get_location("Level 2 Boss", self.player) \
            .place_locked_item(KDL3Item("Level 2 Boss Purified", ItemClassification.progression, None, self.player))
        self.multiworld.get_location("Level 3 Boss", self.player) \
            .place_locked_item(KDL3Item("Level 3 Boss Purified", ItemClassification.progression, None, self.player))
        self.multiworld.get_location("Level 4 Boss", self.player) \
            .place_locked_item(KDL3Item("Level 4 Boss Purified", ItemClassification.progression, None, self.player))
        self.multiworld.get_location("Level 5 Boss", self.player) \
            .place_locked_item(KDL3Item("Level 5 Boss Purified", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Love-Love Rod", self.player)

    def generate_output(self, output_directory: str):
        rompath = ""
        try:
            world = self.multiworld
            player = self.player

            rom = RomData(get_base_rom_path())
            patch_rom(self.multiworld, self.player, rom, self.boss_requirements[self.player])

            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = KDL3DeltaPatch(os.path.splitext(rompath)[0]+KDL3DeltaPatch.patch_file_ending, player=player,
                                  player_name=world.player_name[player], patched_path=rompath)
            patch.write()
        except:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected
            if os.path.exists(rompath):
                os.unlink(rompath)

    def modify_multidata(self, multidata: dict):
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
