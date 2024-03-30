import os
import typing
import settings
import base64
import logging

from BaseClasses import Item, Region, Tutorial, ItemClassification
from .items import CVCotMItem, filler_item_names, action_cards, attribute_cards, get_item_info, get_item_names_to_ids,\
    get_item_counts
from .locations import CVCotMLocation, get_location_info, get_location_names_to_ids, base_id, get_named_locations_data,\
    get_locations_by_area
from .options import CVCotMOptions, SubWeaponShuffle
from .regions import get_region_info, get_all_region_names, get_named_entrances_data
from .rules import CVCotMRules
from .data import iname
from ..AutoWorld import WebWorld, World

from .aesthetics import shuffle_sub_weapons, get_start_inventory_data, get_location_data, get_countdown_numbers, \
    populate_enemy_drops
from .rom import RomData, patch_rom, get_base_rom_path, CVCotMProcedurePatch, CVCOTM_CT_US_HASH, CVCOTM_AC_US_HASH
from .client import CastlevaniaCotMClient


class CVCotMSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Castlevania CotM US rom"""
        copy_to = "Castlevania - Circle of the Moon (USA).gba"
        description = "Castlevania CotM (US) ROM File"
        md5s = [CVCOTM_CT_US_HASH, CVCOTM_AC_US_HASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class CVCotMWeb(WebWorld):
    theme = "stone"

    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipleago Castlevania: Circle of the Moon randomizer on your computer and "
        "connecting it to a multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Liquid Cat"]
    )]


class CVCotMWorld(World):
    """
    Castlevania: Circle of the Moon is the first of three Castlevania games released on the GameBoy Advance.
    As Nathan Graves, utilizing the Dual Set-Up System in conjunction with the Hunter Whip, you must battle your way
    through Camilla's castle and rescue your master.
    """
    game = "Castlevania - Circle of the Moon"
    item_name_groups = {
        "DSS": action_cards.union(attribute_cards),
        "Card": action_cards.union(attribute_cards),
        "Action": action_cards,
        "Action Card": action_cards,
        "Attribute": attribute_cards,
        "Attribute Card": attribute_cards,
        "Freeze": {iname.serpent, iname.cockatrice, iname.mercury, iname.mars},
        "Freeze Action": {iname.mercury, iname.mars},
        "Freeze Attribute": {iname.serpent, iname.cockatrice}
    }
    location_name_groups = get_locations_by_area()
    options_dataclass = CVCotMOptions
    options: CVCotMOptions
    settings: typing.ClassVar[CVCotMSettings]
    topology_present = True

    item_name_to_id = get_item_names_to_ids()
    location_name_to_id = get_location_names_to_ids()

    # Default values to possibly be updated in generate_early
    total_last_keys: int = 0
    required_last_keys: int = 0

    auth: bytearray

    web = CVCotMWeb()

    def generate_early(self) -> None:
        # Generate the player's unique authentication
        self.auth = bytearray(self.multiworld.random.getrandbits(8) for _ in range(16))

        # If Require All Bosses is on, force Required and Available Last Keys to 8.
        if self.options.require_all_bosses:
            self.options.required_last_keys.value = 8
            self.options.available_last_keys.value = 8

        self.total_last_keys = self.options.available_last_keys.value
        self.required_last_keys = self.options.required_last_keys.value

        # If there are more Last Keys required than there are Last Keys in total, drop the required Last Keys to
        # something valid.
        if self.required_last_keys > self.total_last_keys:
            self.required_last_keys = self.total_last_keys
            logging.warning(f"[{self.multiworld.player_name[self.player]}] The Required Last Keys "
                            f"({self.options.required_last_keys.value}) is higher than the Available Last Keys "
                            f"({self.options.available_last_keys.value}). Lowering the required number to: "
                            f"{self.required_last_keys}")
            self.options.required_last_keys.value = self.required_last_keys

    def create_regions(self) -> None:
        # Create every Region object.
        created_regions = [Region(name, self.player, self.multiworld) for name in get_all_region_names()]

        # Attach the Regions to the Multiworld.
        self.multiworld.regions.extend(created_regions)

        for reg in created_regions:

            # Add the Entrances to all the Regions.
            ent_names = get_region_info(reg.name, "entrances")
            if ent_names is not None:
                reg.add_exits(get_named_entrances_data(ent_names))

            # Add the Locations to all the Regions.
            loc_names = get_region_info(reg.name, "locations")
            if loc_names is None:
                continue
            locations_with_ids, events = get_named_locations_data(loc_names, self.options)
            reg.add_locations(locations_with_ids, CVCotMLocation)

            # Place event Items on all of their associated Locations.
            for event_loc, event_item in events.items():
                self.get_location(event_loc).place_locked_item(self.create_item(event_item, "progression"))

    def create_item(self, name: str, force_classification: typing.Optional[str] = None) -> Item:
        if force_classification is not None:
            classification = getattr(ItemClassification, force_classification)
        else:
            classification = getattr(ItemClassification, get_item_info(name, "default classification"))

        code = get_item_info(name, "code")
        if code is not None:
            code += base_id

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
        active_locations = self.multiworld.get_locations(self.player)

    # Location data
        offset_data = get_location_data(self, active_locations)
    # Sub-weapons
        if self.options.sub_weapon_shuffle:
            offset_data.update(shuffle_sub_weapons(self))
    # Item drop randomization
        if self.options.item_drop_randomization:
            offset_data.update(populate_enemy_drops(self))
    # Countdown
        #if self.options.countdown:
        #    offset_data.update(get_countdown_numbers(self.options, active_locations))
    # Start Inventory
        #offset_data.update(get_start_inventory_data(self.player, self.options,
        #                                            self.multiworld.precollected_items[self.player]))

        patch = CVCotMProcedurePatch()
        patch_rom(self, patch, offset_data)

        rom_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
                                                  f"{patch.patch_file_ending}")

        patch.write(rom_path)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_item_names)

    def modify_multidata(self, multidata: typing.Dict[str, typing.Any]):
        # Put the player's unique authentication in connect_names.
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] = \
            multidata["connect_names"][self.multiworld.player_name[self.player]]
