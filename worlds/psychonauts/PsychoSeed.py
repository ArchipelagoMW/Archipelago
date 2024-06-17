import os
import zipfile
from typing import List, Tuple, Iterable, Union, Dict, TYPE_CHECKING

import Utils
from worlds.Files import APContainer
from .Items import ITEM_DICTIONARY, AP_ITEM_OFFSET
from .Locations import ALL_LOCATIONS, PSYCHOSEED_LOCATION_IDS
from .Options import Goal
from .PsychoRandoItems import PSYCHORANDO_BASE_ITEM_IDS, PSYCHORANDO_ITEM_TABLE, MAX_PSY_ITEM_ID

if TYPE_CHECKING:
    from . import PSYWorld

PSY_NON_LOCAL_ID_START = MAX_PSY_ITEM_ID + 1


class PSYContainer(APContainer):
    game: str = 'Psychonauts'

    def __init__(self, patch_data: str, base_path: str, output_directory: str,
                 player=None, player_name: str = "", server: str = ""):
        self.patch_data = patch_data
        self.file_path = base_path
        container_path = os.path.join(output_directory, base_path + ".zip")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("RandoSeed.lua", self.patch_data)
        super().write_contents(opened_zipfile)


def gen_psy_ids(location_tuples_in: Iterable[Tuple[bool, Union[str, None], int]]
                ) -> Tuple[List[Tuple[int, int]], Dict[int, int]]:
    """
    Generic Psychonauts ID generator. The input location tuples may come from scouted locations or from generated
    locations.
    """
    # append the item values, need to be in exact order
    # locations are handled by index in table
    # items from other games need to be converted to a new value
    # Starting at PSY_NON_LOCAL_ID_START, +1 each time
    non_local_id = PSY_NON_LOCAL_ID_START

    # Initialize a list to store tuples of location ID and item code
    location_tuples = []

    # If we run out of Psychonauts IDs to place an item locally because a yaml plando-ed more than can exist by default,
    # or in the very unlikely case that more filler PsiCards were placed locally than can exist locally, place the item
    # as an AP item placeholder instead and send the item as if it were non-local. This dict stores the mapping from AP
    # items placed like this to the item ID to send to Psychonauts when the placeholder item is collected.
    # Since receiving the correct item relies on a connection to the AP server, these items won't be received when
    # disconnected.
    local_items_placed_as_ap_items = {}

    placed_item_counts = {}

    # Pre-sort the tuples based on location ID to ensure the generated IDs are consistent even if the input is in a
    # different order.
    for is_local_item, local_item_name, location_id in sorted(location_tuples_in, key=lambda t: t[2]):
        # Skip any locations not part of PsychoSeed generation.
        if location_id not in PSYCHOSEED_LOCATION_IDS:
            continue

        if is_local_item:
            # When there are multiple copies of an item, locally placed items start from the first id for that item
            # and count upwards for each item placed.
            count_placed = placed_item_counts.setdefault(local_item_name, 0)
            # Maximum number of times this item can be placed into the Psychonauts game world.
            max_count = PSYCHORANDO_ITEM_TABLE[local_item_name]
            if count_placed < max_count:
                base_item_code = PSYCHORANDO_BASE_ITEM_IDS[local_item_name]
                item_code = base_item_code + count_placed
                placed_item_counts[local_item_name] = count_placed + 1
            else:
                # There aren't any Psychonauts IDs left to place this item into the Psychonauts game world, so place
                # it as an AP placeholder item and receive the item as if it were placed non-locally.
                item_code = non_local_id
                ap_item_id = ITEM_DICTIONARY[local_item_name] + AP_ITEM_OFFSET
                local_items_placed_as_ap_items[item_code] = ap_item_id
                non_local_id += 1
        else:
            # item from another game
            item_code = non_local_id
            non_local_id += 1

        # Append the location ID and item code tuple to the list

        location_tuples.append((location_id, item_code))

    return location_tuples, local_items_placed_as_ap_items


def gen_psy_ids_from_filled_locations(self) -> List[Tuple[int, int]]:
    location_tuples = []

    for location in self.multiworld.get_filled_locations(self.player):
        location_id = ALL_LOCATIONS[location.name]

        is_local = location.item and location.item.player == self.player
        local_item_name = location.item.name if is_local else None

        location_tuples.append((is_local, local_item_name, location_id))

    psy_ids, local_items_placed_as_ap_items = gen_psy_ids(location_tuples)
    if local_items_placed_as_ap_items:
        print("Warning: There were not enough Psychonauts IDs to place all local items. Some local items have been"
              " placed as AP placeholder items instead.")
    return psy_ids


def _lua_bool(option):
    """
    Psychonauts' sandboxed lua environment uses `TRUE` (`1`) for boolean true and `FALSE` (`nil`) for boolean false.
    """
    return "TRUE" if option else "FALSE"


def gen_psy_seed(self: "PSYWorld", output_directory):
    # Mod name for Zip Folder
    mod_name = f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.get_file_safe_player_name(self.player)}"
    # Folder name for Client and Game to Read/Write to
    seed_folder_name = f"AP-{self.multiworld.seed_name}-P{self.player}"
    # Need to clip off the seed name for Display Version to fit in Randomizer
    rando_display_name = f"AP-P{self.player}-{self.multiworld.get_file_safe_player_name(self.player)}"

    randoseed_parts = []

    # First part of lua code structure
    formatted_text1 = '''function RandoSeed(Ob)
        if ( not Ob ) then
            Ob = CreateObject('ScriptBase')
            Ob.seed = {}
        '''
    randoseed_parts.append(formatted_text1)

    # append seed_folder_name for APfoldername
    randoseed_parts.append(f"       Ob.APfoldername = '{seed_folder_name}'\n")

    # append rando_display_name 
    randoseed_parts.append(f"       Ob.seedname = '{rando_display_name}'\n")

    # append startlevitation setting
    randoseed_parts.append(f"           Ob.startlevitation = {_lua_bool(self.options.StartingLevitation)}\n")

    # append mentalmagnet setting
    randoseed_parts.append(f"           Ob.mentalmagnet = {_lua_bool(self.options.StartingMentalMagnet)}\n")

    # append lootboxvaults setting
    randoseed_parts.append(f"           Ob.lootboxvaults = {_lua_bool(self.options.LootboxVaults)}\n")

    # append enemydamagemultiplier setting
    enemy_damage_multiplier = self.options.EnemyDamageMultiplier.value
    randoseed_parts.append(f"           Ob.enemydamagemultiplier = {enemy_damage_multiplier}\n")

    # append instantdeath setting
    randoseed_parts.append(f"           Ob.instantdeath = {_lua_bool(self.options.InstantDeathMode)}\n")

    # append easymillarace setting
    randoseed_parts.append(f"           Ob.easymillarace = {_lua_bool(self.options.EasyMillaRace)}\n")

    # append easyflight setting
    randoseed_parts.append(f"           Ob.easyflight = {_lua_bool(self.options.EasyFlightMode)}\n")

    # append requireMC setting
    randoseed_parts.append(f"           Ob.requireMC = {_lua_bool(self.options.RequireMeatCircus)}\n")

    # append deepArrowheadShuffle and randomizeDowsingRod depending on DeepArrowheadShuffle setting
    randoseed_parts.append(f"           Ob.deepArrowheadShuffle = {_lua_bool(self.options.DeepArrowheadShuffle)}\n")
    randoseed_parts.append(f"           Ob.randomizeDowsingRod = {_lua_bool(self.options.DeepArrowheadShuffle)}\n")

    # append cobwebShuffle setting
    randoseed_parts.append(f"           Ob.cobwebShuffle = {_lua_bool(self.options.MentalCobwebShuffle)}\n")

    # append Goal settings
    beat_oleander = _lua_bool(self.options.Goal == Goal.option_braintank
                              or self.options.Goal == Goal.option_braintank_and_brainhunt)
    require_brain_hunt = _lua_bool(self.options.Goal == Goal.option_brainhunt
                                   or self.options.Goal == Goal.option_braintank_and_brainhunt)
    randoseed_parts.append(f"           Ob.beatoleander = {beat_oleander}\n")
    randoseed_parts.append(f"           Ob.brainhunt = {require_brain_hunt}\n")

    # append Brain Jar Requirement
    brains_required = self.options.BrainsRequired.value
    randoseed_parts.append(f"           Ob.brainsrequired = {brains_required}\n")

    # Section where default settings booleans are written to RandoSeed.lua
    # adding new settings will remove from this list
    default_seed_settings = '''
        Ob.isAP = TRUE
        Ob.startcobweb = FALSE
        Ob.startbutton = FALSE
        Ob.randomizecobwebduster = TRUE
        Ob.everylocationpossible = FALSE
        Ob.harderbutton = FALSE
        Ob.beatalllevels = FALSE
        Ob.rank101 = FALSE
        Ob.scavengerhunt = FALSE
        Ob.fasterLO = TRUE
        Ob.earlyelevator = FALSE
        Ob.removetutorials = TRUE
        Ob.createhints = FALSE
        Ob.spoilerlog = FALSE
    '''
    randoseed_parts.append(default_seed_settings)

    location_tuples = gen_psy_ids_from_filled_locations(self)

    # attach more lua code structure first
    formatted_text2 = '''
    end
    
    function Ob:fillTable()
    local SEED_GOES_HERE = {
    
    
    '''
    randoseed_parts.append(formatted_text2)

    # Iterate through the sorted list of tuples and append item codes to randoseed_parts
    for index, (location_id, itemcode) in enumerate(location_tuples):
        randoseed_parts.append(str(itemcode))
        # Format so that each line has 10 values, for readability
        if index % 10 == 9:
            randoseed_parts.append(",\n")
        else:
            randoseed_parts.append(", ")

    formatted_text3 = ''' }
        self.seed = SEED_GOES_HERE
        end
        return Ob
    end

    '''

    randoseed_parts.append(formatted_text3)

    # Combine all the parts into one long piece of text
    randoseed = ''.join(randoseed_parts)

    mod_dir = os.path.join(output_directory, mod_name + "_" + Utils.__version__)

    mod = PSYContainer(randoseed, mod_dir, output_directory, self.player,
                       self.multiworld.get_file_safe_player_name(self.player))
    mod.write()
