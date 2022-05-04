import logging
import threading

from ...worlds.alttp.Items import LttpItem
from ..AutoWorld import World, LogicMixin
from ...worlds.alttp.Options import alttp_options, smallkey_shuffle
from ...worlds.alttp.Items import item_table, item_name_groups, LttpItem
from ...worlds.alttp.Regions import lookup_name_to_id, create_regions, mark_light_world_regions
from ...worlds.alttp.Rules import set_rules
from ...worlds.alttp.ItemPool import generate_itempool, difficulties
from ...worlds.alttp.Shops import create_shops, ShopSlotFill
from ...worlds.alttp.Dungeons import create_dungeons
from ...worlds.alttp.Rom import LocalRom, patch_rom, patch_race_rom, patch_enemizer, apply_rom_settings, \
    get_hash_string, get_base_rom_path, LttPDeltaPatch
from ...worlds.alttp.InvertedRegions import create_inverted_regions, mark_dark_world_regions
from ...worlds.alttp.EntranceShuffle import link_entrances, link_inverted_entrances, plando_connect

lttp_logger = logging.getLogger("A Link to the Past")


class ALTTPWorld(World):
    """
    The Legend of Zelda: A Link to the Past is an action/adventure game where you take on the role of Link, a boy
    destined to save the land of Hyrule. Delve through three palaces and nine dungeons in your quest to rescue the
    descendants of the seven wise men and defeat the evil Ganon!
    """
    game: str = 'A Link to the Past'
    options = alttp_options
    topology_present = True
    item_name_groups = item_name_groups
    hint_blacklist = {'Triforce'}

    item_name_to_id = {name: data.item_code for name, data in item_table.items() if type(data.item_code) == int}
    location_name_to_id = lookup_name_to_id

    data_version = 9
    remote_items = False
    remote_start_inventory = False
    required_client_version = (0, 3, 2)

    set_rules = set_rules

    create_items = generate_itempool

    def __init__(self, *args, **kwargs):
        self.dungeon_local_item_names = set()
        self.dungeon_specific_item_names = set()
        self.rom_name_available_event = threading.Event()
        self.has_progressive_bows = False
        super(ALTTPWorld, self).__init__(*args, **kwargs)


