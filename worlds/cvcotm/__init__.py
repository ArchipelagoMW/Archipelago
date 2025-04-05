import os
import typing
import settings
import base64
import logging

from BaseClasses import Item, Region, Tutorial, ItemClassification
from .items import CVCotMItem, FILLER_ITEM_NAMES, ACTION_CARDS, ATTRIBUTE_CARDS, cvcotm_item_info, \
    get_item_names_to_ids, get_item_counts
from .locations import CVCotMLocation, get_location_names_to_ids, BASE_ID, get_named_locations_data, \
    get_location_name_groups
from .options import cvcotm_option_groups, CVCotMOptions, SubWeaponShuffle, IronMaidenBehavior, RequiredSkirmishes, \
    CompletionGoal, EarlyEscapeItem
from .regions import get_region_info, get_all_region_names
from .rules import CVCotMRules
from .data import iname, lname
from .presets import cvcotm_options_presets
from worlds.AutoWorld import WebWorld, World

from .aesthetics import shuffle_sub_weapons, get_location_data, get_countdown_flags, populate_enemy_drops, \
    get_start_inventory_data
from .rom import RomData, patch_rom, get_base_rom_path, CVCotMProcedurePatch, CVCOTM_CT_US_HASH, CVCOTM_AC_US_HASH
    # CVCOTM_VC_US_HASH
from .client import CastlevaniaCotMClient


class CVCotMSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Castlevania CotM US rom"""
        copy_to = "Castlevania - Circle of the Moon (USA).gba"
        description = "Castlevania CotM (US) ROM File"
        # md5s = [CVCOTM_CT_US_HASH, CVCOTM_AC_US_HASH, CVCOTM_VC_US_HASH]
        md5s = [CVCOTM_CT_US_HASH, CVCOTM_AC_US_HASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class CVCotMWeb(WebWorld):
    theme = "stone"
    options_presets = cvcotm_options_presets

    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipleago Castlevania: Circle of the Moon randomizer on your computer and "
        "connecting it to a multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Liquid Cat"]
    )]

    option_groups = cvcotm_option_groups


class CVCotMWorld(World):
    """
    Castlevania: Circle of the Moon is a launch title for the Game Boy Advance and the first of three Castlevania games
    released for the handheld in the "Metroidvania" format. As Nathan Graves, wielding the Hunter Whip and utilizing the
    Dual Set-Up System for new possibilities, you must battle your way through Camilla's castle and rescue your master
    from a demonic ritual to restore the Count's power...
    """
    game = "Castlevania - Circle of the Moon"
    item_name_groups = {
        "DSS": ACTION_CARDS.union(ATTRIBUTE_CARDS),
        "Card": ACTION_CARDS.union(ATTRIBUTE_CARDS),
        "Action": ACTION_CARDS,
        "Action Card": ACTION_CARDS,
        "Attribute": ATTRIBUTE_CARDS,
        "Attribute Card": ATTRIBUTE_CARDS,
        "Freeze": {iname.serpent, iname.cockatrice, iname.mercury, iname.mars},
        "Freeze Action": {iname.mercury, iname.mars},
        "Freeze Attribute": {iname.serpent, iname.cockatrice}
    }
    location_name_groups = get_location_name_groups()
    options_dataclass = CVCotMOptions
    options: CVCotMOptions
    settings: typing.ClassVar[CVCotMSettings]
    origin_region_name = "Catacomb"
    hint_blacklist = frozenset({lname.ba24})  # The Battle Arena reward, if it's put in, will always be a Last Key.

    item_name_to_id = {name: cvcotm_item_info[name].code + BASE_ID for name in cvcotm_item_info
                       if cvcotm_item_info[name].code is not None}
    location_name_to_id = get_location_names_to_ids()

    # Default values to possibly be updated in generate_early
    total_last_keys: int = 0
    required_last_keys: int = 0

    auth: bytearray

    web = CVCotMWeb()

    def generate_early(self) -> None:
        # Generate the player's unique authentication
        self.auth = bytearray(self.random.getrandbits(8) for _ in range(16))

        # If Required Skirmishes are on, force the Required and Available Last Keys to 8 or 9 depending on which option
        # was chosen.
        if self.options.required_skirmishes == RequiredSkirmishes.option_all_bosses:
            self.options.required_last_keys.value = 8
            self.options.available_last_keys.value = 8
        elif self.options.required_skirmishes == RequiredSkirmishes.option_all_bosses_and_arena:
            self.options.required_last_keys.value = 9
            self.options.available_last_keys.value = 9

        self.total_last_keys = self.options.available_last_keys.value
        self.required_last_keys = self.options.required_last_keys.value

        # If there are more Last Keys required than there are Last Keys in total, drop the required Last Keys to
        # the total Last Keys.
        if self.required_last_keys > self.total_last_keys:
            self.required_last_keys = self.total_last_keys
            logging.warning(f"[{self.player_name}] The Required Last Keys "
                            f"({self.options.required_last_keys.value}) is higher than the Available Last Keys "
                            f"({self.options.available_last_keys.value}). Lowering the required number to: "
                            f"{self.required_last_keys}")
            self.options.required_last_keys.value = self.required_last_keys

        # Place the Double or Roc Wing in local_early_items if the Early Escape option is being used.
        if self.options.early_escape_item == EarlyEscapeItem.option_double:
            self.multiworld.local_early_items[self.player][iname.double] = 1
        elif self.options.early_escape_item == EarlyEscapeItem.option_roc_wing:
            self.multiworld.local_early_items[self.player][iname.roc_wing] = 1
        elif self.options.early_escape_item == EarlyEscapeItem.option_double_or_roc_wing:
            self.multiworld.local_early_items[self.player][self.random.choice([iname.double, iname.roc_wing])] = 1

    def create_regions(self) -> None:
        # Create every Region object.
        created_regions = [Region(name, self.player, self.multiworld) for name in get_all_region_names()]

        # Attach the Regions to the Multiworld.
        self.multiworld.regions.extend(created_regions)

        for reg in created_regions:

            # Add the Entrances to all the Regions.
            ent_destinations_and_names = get_region_info(reg.name, "entrances")
            if ent_destinations_and_names is not None:
                reg.add_exits(ent_destinations_and_names)

            # Add the Locations to all the Regions.
            loc_names = get_region_info(reg.name, "locations")
            if loc_names is None:
                continue
            locations_with_ids, locked_pairs = get_named_locations_data(loc_names, self.options)
            reg.add_locations(locations_with_ids, CVCotMLocation)

            # Place locked Items on all of their associated Locations.
            for locked_loc, locked_item in locked_pairs.items():
                self.get_location(locked_loc).place_locked_item(self.create_item(locked_item,
                                                                                 ItemClassification.progression))

    def create_item(self, name: str, force_classification: typing.Optional[ItemClassification] = None) -> Item:
        if force_classification is not None:
            classification = force_classification
        else:
            classification = cvcotm_item_info[name].default_classification

        code = cvcotm_item_info[name].code
        if code is not None:
            code += BASE_ID

        created_item = CVCotMItem(name, classification, code, self.player)

        return created_item

    def create_items(self) -> None:
        item_counts = get_item_counts(self)

        # Set up the items correctly
        self.multiworld.itempool += [self.create_item(item, classification) for classification in item_counts for item
                                     in item_counts[classification] for _ in range(item_counts[classification][item])]

    def set_rules(self) -> None:
        # Set all the Entrance and Location rules properly.
        CVCotMRules(self).set_cvcotm_rules()

    def generate_output(self, output_directory: str) -> None:
        # Get out all the Locations that are not Events. Only take the Iron Maiden switch if the Maiden Detonator is in
        # the item pool.
        active_locations = [loc for loc in self.multiworld.get_locations(self.player) if loc.address is not None and
                            (loc.name != lname.ct21 or self.options.iron_maiden_behavior ==
                             IronMaidenBehavior.option_detonator_in_pool)]

        # Location data
        offset_data = get_location_data(self, active_locations)
        # Sub-weapons
        if self.options.sub_weapon_shuffle:
            offset_data.update(shuffle_sub_weapons(self))
        # Item drop randomization
        if self.options.item_drop_randomization:
            offset_data.update(populate_enemy_drops(self))
        # Countdown
        if self.options.countdown:
            offset_data.update(get_countdown_flags(self, active_locations))
        # Start Inventory
        start_inventory_data = get_start_inventory_data(self)
        offset_data.update(start_inventory_data[0])

        patch = CVCotMProcedurePatch(player=self.player, player_name=self.player_name)
        patch_rom(self, patch, offset_data, start_inventory_data[1])

        rom_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
                                                  f"{patch.patch_file_ending}")

        patch.write(rom_path)

    def fill_slot_data(self) -> dict:
        return {"death_link": self.options.death_link.value,
                "iron_maiden_behavior": self.options.iron_maiden_behavior.value,
                "ignore_cleansing": self.options.ignore_cleansing.value,
                "skip_tutorials": self.options.skip_tutorials.value,
                "required_last_keys": self.required_last_keys,
                "completion_goal": self.options.completion_goal.value}

    def get_filler_item_name(self) -> str:
        return self.random.choice(FILLER_ITEM_NAMES)

    def modify_multidata(self, multidata: typing.Dict[str, typing.Any]):
        # Put the player's unique authentication in connect_names.
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] = \
            multidata["connect_names"][self.player_name]
