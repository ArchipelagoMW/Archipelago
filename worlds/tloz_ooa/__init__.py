import logging
import os
import yaml
import settings

from BaseClasses import Tutorial, Region, Location, LocationProgressType
from Fill import fill_restrictive, FillError
from Options import Accessibility, OptionError
from worlds.AutoWorld import WebWorld, World
from typing import Any, Set, List, Dict, Optional, Tuple, ClassVar, TextIO, Union
from .Data import *
from .data.Items import *
from .Logic import create_connections, apply_self_locking_rules
from .Options import *
from .PatchWriter import ooa_create_appp_patch
from .data import LOCATIONS_DATA
from .data.Constants import *
from .data.Regions import REGIONS
from .Client import OracleOfAgesClient  # Unused, but required to register with BizHawkClient
from .patching.ProcedurePatch import ROM_HASH

class OOASettings(settings.Group):
    class OOARomFile(settings.UserFilePath):
        """File path of the OOA US rom"""
        description = "Oracle of Ages (USA) ROM File"
        copy_to = "Legend of Zelda, The - Oracle of Ages (USA).gbc"
        md5s = [ROM_HASH]

    class OoACharacterSprite(str):
        """
        The name of the sprite file to use (from "data/sprites/oos_ooa/").
        Putting "link" as a value uses the default game sprite.
        Putting "random" as a value randomly picks a sprite from your sprites directory for each generated ROM.
        """
    class OoACharacterPalette(str):
        """
        The color palette used for character sprite throughout the game.
        Valid values are: "green", "red", "blue", "orange", and "random"
        """
    class OoAHeartBeepInterval(str):
        """
        A factor applied to the infamous heart beep sound interval.
        Valid values are: "vanilla", "half", "quarter", "disabled"
        """
    
    class OoAQolMermaidSuit(str):
        """
        Defines if you don't want to spam the buttons to swim with the mermaid suit.
        """
        
    class OoAQuickFlute(str):
        """
        When enabled, playing the flute and the harp will immobilize you during a very small amount of time compared to vanilla game.
        """

    class OoASkipTokkeyDance(str):
        """
        Defines if you want to skip the small dance that tokkay does
        """

    class OoASkipSadBoiJoke(str):
        """
        Defines if you want to skip the joke you tell to the sad boi
        """

    rom_file: OOARomFile = OOARomFile(OOARomFile.copy_to)
    heart_beep_interval: Union[OoAHeartBeepInterval, str] = "vanilla"
    character_sprite: Union[OoACharacterSprite, str] = "link"
    character_palette: Union[OoACharacterPalette, str] = "green"
    qol_mermaid_suit: Union[OoAQolMermaidSuit, bool] = True
    qol_quick_flute: Union[OoAQuickFlute, bool] = True
    skip_tokkey_dance: Union[OoASkipTokkeyDance, bool] = False
    skip_boi_joke: Union[OoASkipSadBoiJoke, bool] = False

class OracleOfAgesWeb(WebWorld):
    theme = "grass"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Oracle of Ages for Archipelago on your computer.",
        "English",
        "ooa_setup_en.md",
        "ooa_setup/en",
        ["Dinopony"]
    )]

class OracleOfAgesWorld(World):
    """
    The Legend of Zelda: Oracles of Ages is one of the rare Capcom entries to the series.
    Nayru, the oracle of ages, has been possessed by Veran, and she is now making a mess in Labrynna
    Gather the Essences of Times, exorcice Nayru and defeat Veran to save the timeline of Labrynna
    """
    game = "The Legend of Zelda - Oracle of Ages"
    options_dataclass = OracleOfAgesOptions
    options: OracleOfAgesOptions
    required_client_version = (0, 5, 1)
    web = OracleOfAgesWeb()
    topology_present = True

    location_name_to_id = build_location_name_to_id_dict()
    item_name_to_id = build_item_name_to_id_dict()
    item_name_groups = ITEM_GROUPS
    location_name_groups = LOCATION_GROUPS

    pre_fill_items: List[Item]
    dungeon_items: List[Item]
    dungeon_entrances: Dict[str, str]
    shop_prices: Dict[str, int]

    settings: ClassVar[OOASettings]
    settings_key = "tloz_ooa_options"

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.pre_fill_items = []
        self.dungeon_items = []
        self.dungeon_entrances = DUNGEON_ENTRANCES.copy()
        self.shop_prices = SHOP_PRICES_DIVIDERS.copy()

    def fill_slot_data(self) -> dict:
        # Put options that are useful to the tracker inside slot data
        # TODO MOAR DATA ?
        options = ["goal", "death_link",
                   # Logic-impacting options
                   "logic_difficulty",
                   "shuffle_dungeons",
                   "default_seed",
                   # Locations
                   "advance_shop",
                   # Requirements
                   "required_essences", "required_slates",
                   # keysanity
                   "keysanity_small_keys", "keysanity_boss_keys", "keysanity_slates"
                   ]

        slot_data = self.options.as_dict(*options)
        slot_data["animal_companion"] = COMPANIONS[self.options.animal_companion.value]
        slot_data["default_seed"] = SEED_ITEMS[self.options.default_seed.value]

        slot_data["dungeon_entrances"] = self.dungeon_entrances

        return slot_data

    def generate_early(self):
        conflicting_rings = self.options.required_rings.value & self.options.excluded_rings.value
        if len(conflicting_rings) > 0:
            raise OptionError("Required Rings and Excluded Rings contain the same element(s)", conflicting_rings)
        
        self.restrict_non_local_items()

        if self.options.shuffle_dungeons == "shuffle":
            self.shuffle_dungeons()

        self.randomize_shop_prices()

    def restrict_non_local_items(self):
        # Restrict non_local_items option in cases where it's incompatible with other options that enforce items
        # to be placed locally (e.g. dungeon items with keysanity off)
        if not self.options.keysanity_small_keys:
            self.options.non_local_items.value -= self.item_name_groups["Small Keys"]
        if not self.options.keysanity_boss_keys:
            self.options.non_local_items.value -= self.item_name_groups["Boss Keys"]
        if not self.options.keysanity_maps_compasses:
            self.options.non_local_items.value -= self.item_name_groups["Dungeon Maps"]
            self.options.non_local_items.value -= self.item_name_groups["Compasses"]
        if not self.options.keysanity_slates:
            self.options.non_local_items.value -= set(["Slate"])

    
    def shuffle_dungeons(self):
        shuffled_dungeons = list(self.dungeon_entrances.values())
        while True:
            self.random.shuffle(shuffled_dungeons)
            if shuffled_dungeons[4] != "enter d0": # Ensure D4 entrance doesn't lead to d0
                break
        
        self.dungeon_entrances = dict(zip(self.dungeon_entrances, shuffled_dungeons))

    def randomize_shop_prices(self):
        prices_pool = get_prices_pool()
        self.random.shuffle(prices_pool)
        global_prices_factor = self.options.shop_prices_factor.value / 100.0
        for key, divider in self.shop_prices.items():
            floating_price = prices_pool.pop() * global_prices_factor / divider
            for i, value in enumerate(VALID_RUPEE_VALUES):
                if value > floating_price:
                    self.shop_prices[key] = VALID_RUPEE_VALUES[i-1]
                    break

    def location_is_active(self, location_name, location_data):
        if "conditional" not in location_data or location_data["conditional"] is False:
            return True

        region_id = location_data["region_id"]
        if region_id == "advance shop":
            return self.options.advance_shop.value

        # TODO FUNNY LOCATION ?

        return False

    def create_location(self, region_name: str, location_name: str, local: bool):
        region = self.multiworld.get_region(region_name, self.player)
        location = Location(self.player, location_name, self.location_name_to_id[location_name], region)
        region.locations.append(location)
        if local:
            location.item_rule = lambda item: item.player == self.player

    def create_regions(self):
        # Create regions
        for region_name in REGIONS:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations
        for location_name, location_data in LOCATIONS_DATA.items():
            if not self.location_is_active(location_name, location_data):
                continue

            is_local = "local" in location_data and location_data["local"] is True
            self.create_location(location_data['region_id'], location_name, is_local)

        self.create_events()
        self.exclude_problematic_locations()

    def create_event(self, region_name, event_item_name):
        region = self.multiworld.get_region(region_name, self.player)
        location = Location(self.player, region_name + ".event", None, region)
        region.locations.append(location)
        location.place_locked_item(Item(event_item_name, ItemClassification.progression, None, self.player))

    def create_events(self):
        self.create_event("maku seed", "Maku Seed")

        if self.options.goal == OracleOfAgesGoal.option_beat_veran:
            self.create_event("veran beaten", "_beaten_game")
        elif self.options.goal == OracleOfAgesGoal.option_beat_ganon:
            self.create_event("ganon beaten", "_beaten_game")

        self.create_event("ridge move vine seed", "_access_cart")

        self.create_event("d3 S crystal", "_d3_S_crystal")
        self.create_event("d3 E crystal", "_d3_E_crystal")
        self.create_event("d3 W crystal", "_d3_W_crystal")
        self.create_event("d3 N crystal", "_d3_N_crystal")
        self.create_event("d3 B1F spinner", "_d3_B1F_spinner")

        self.create_event("d6 wall B bombed", "_d6_wall_B_bombed")
        self.create_event("d6 canal expanded", "_d6_canal_expanded")

        self.create_event("d7 boss", "_finished_d7")

    def exclude_problematic_locations(self):
        locations_to_exclude = []
        # If goal essence requirement is set to a specific value, prevent essence-bound checks which require more
        # essences than this goal to hold anything of value
        #if self.options.required_essences < 7:
        #    locations_to_exclude.append("Horon Village: Item Inside Maku Tree (7+ Essences)")
        #    if self.options.required_essences < 5:
        #        locations_to_exclude.append("Horon Village: Item Inside Maku Tree (5+ Essences)")
        #        if self.options.required_essences < 3:
        #            locations_to_exclude.append("Horon Village: Item Inside Maku Tree (3+ Essences)")

        # TODO PROBLEMATIC LOCATIONS

        for name in locations_to_exclude:
            self.multiworld.get_location(name, self.player).progress_type = LocationProgressType.EXCLUDED

    def set_rules(self):
        create_connections(self.multiworld, self.player)
        apply_self_locking_rules(self.multiworld, self.player)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("_beaten_game", self.player)

    def create_item(self, name: str) -> Item:
        if name.endswith("!PROG"):
            # If item name has a "!PROG" suffix, force it to be progression. This is typically used to create the right
            # amount of progression rupees while keeping them a filler item as default
            name = name.removesuffix("!PROG")
            classification = ItemClassification.progression_skip_balancing
        elif name.endswith("!USEFUL"):
            # Same for above but with useful. This is typically used for Required Rings,
            # as we don't want those locked in a barren dungeon
            name = name.removesuffix("!USEFUL")
            classification = ITEMS_DATA[name]["classification"]
            if classification == ItemClassification.filler:
                classification = ItemClassification.useful
        else:
            classification = ITEMS_DATA[name]["classification"]
        ap_code = self.item_name_to_id[name]

        # A few items become progression only in hard logic
        progression_items_in_medium_logic = ["Expert's Ring", "Fist Ring", "Toss Ring", "Energy Ring"]
        if self.options.logic_difficulty == "medium" and name in progression_items_in_medium_logic:
            classification = ItemClassification.progression

        return Item(name, classification, ap_code, self.player)

    def build_item_pool_dict(self):
        item_pool_dict = {}
        filler_item_count = 0
        remaining_rings = len({name for name, idata in ITEMS_DATA.items() if "ring" in idata}) - len(self.options.excluded_rings.value)
        for loc_name, loc_data in LOCATIONS_DATA.items():

            if "vanilla_item" not in loc_data:
                #print("Can't create item from location '",loc_name ,"' because it doesn't have one")
                continue

            item_name = loc_data['vanilla_item']
            if "randomized" in loc_data and loc_data["randomized"] is False:
                item = self.create_item(item_name)
                location = self.multiworld.get_location(loc_name, self.player)
                location.place_locked_item(item)
                #print("placing locked item '",loc_data['vanilla_item'] ,"' in '",loc_name ,"'")
                continue
            if not self.location_is_active(loc_name, loc_data):
                #print("Can't create item '",loc_data['vanilla_item'] ,"' because '",loc_name ,"' is not active")
                continue


            if self.options.master_keys != OracleOfAgesMasterKeys.option_disabled and "Small Key" in item_name:
                # Small Keys don't exist if Master Keys are set to replace them
                filler_item_count += 1
                continue
            if self.options.master_keys == OracleOfAgesMasterKeys.option_all_dungeon_keys and "Boss Key" in item_name:
                # Boss keys don't exist if Master Keys are set to replace them
                filler_item_count += 1
                continue

            item_name = loc_data['vanilla_item']
            if "Ring" in item_name:
                if remaining_rings > 0:
                    item_name = "Random Ring"
                    remaining_rings -= 1
                else:
                    filler_item_count += 1
                    continue

            item_pool_dict[item_name] = item_pool_dict.get(item_name, 0) + 1

        # If Master Keys are enabled, put one for every dungeon
        if self.options.master_keys != OracleOfAgesMasterKeys.option_disabled:
            for small_key_name in ITEM_GROUPS["Master Keys"]:
                item_pool_dict[small_key_name] = 1
                filler_item_count -= 1

        # Add the required rings
        ring_copy = sorted(self.options.required_rings.value.copy())
        for _ in range(len(ring_copy)):
            ring_name = f"{ring_copy.pop()}!USEFUL"
            item_pool_dict[ring_name] = item_pool_dict.get(ring_name, 0) + 1

            if item_pool_dict["Random Ring"] > 0:
                # Take from set ring pool first
                item_pool_dict["Random Ring"] -= 1
            else:
                # Take from filler after
                filler_item_count -= 1

        # Add as many filler items as required
        for _ in range(filler_item_count):
            random_filler_item = self.get_filler_item_name()
            item_pool_dict[random_filler_item] = item_pool_dict.get(random_filler_item, 0) + 1
        
        # Perform adjustments on the item pool
        item_pool_adjustements = [
            ["Flute", self.options.animal_companion.current_key.title() + "'s Flute"],  # Put a specific flute
            ["Gasha Seed", "Seed Satchel"],             # Add a 3rd satchel that is usually obtained in linked games (99 seeds)
            ["Gasha Seed", "Bombs (10)"],               # Add one more bomb compared to vanilla to reach 99 max bombs
            ["Gasha Seed", "Potion"],                   # Replace some Gasha Seed by 2 potions.
            ["Gasha Seed", "Potion"],                   # ^
            ["Gasha Seed", "Rupees (200)"],              # and one by rupees
            ["Gasha Seed", "Progressive Sword"],        # Need an additionnal sword to go to L3
        ]

        for i, pair in enumerate(item_pool_adjustements):
            original_name = pair[0]
            replacement_name = pair[1]
            item_pool_dict[original_name] -= 1
            item_pool_dict[replacement_name] = item_pool_dict.get(replacement_name, 0) + 1

        return item_pool_dict

    def create_items(self):
        item_pool_dict = self.build_item_pool_dict()
        
        # Create items following the dictionary that was previously constructed
        if (item_pool_dict.get("Random Ring")):
            self.create_rings(item_pool_dict["Random Ring"])
            del item_pool_dict["Random Ring"]

        for item_name, quantity in item_pool_dict.items():
            for i in range(quantity):
                if ("Small Key" in item_name or "Master Key" in item_name) and not self.options.keysanity_small_keys:
                    self.dungeon_items.append(self.create_item(item_name))
                elif "Boss Key" in item_name and not self.options.keysanity_boss_keys:
                    self.dungeon_items.append(self.create_item(item_name))
                elif ("Compass" in item_name or "Dungeon Map" in item_name) and not self.options.keysanity_maps_compasses:
                    self.dungeon_items.append(self.create_item(item_name))
                elif "Slate" in item_name and not self.options.keysanity_slates:
                    self.dungeon_items.append(self.create_item(item_name))
                else:
                    self.multiworld.itempool.append(self.create_item(item_name))        

    def create_rings(self, amount):
        # Get a subset of as many rings as needed
        ring_names = [name for name, idata in ITEMS_DATA.items() if "ring" in idata]
        # Remove excluded rings, and required rings because they'll be added later anyway
        ring_names = [name for name in ring_names if name not in self.options.required_rings.value and name not in self.options.excluded_rings.value]

        self.random.shuffle(ring_names)
        del ring_names[amount:]
        for ring_name in ring_names:
            self.multiworld.itempool.append(self.create_item(ring_name))
        self.random_rings_pool = ring_names

    def get_pre_fill_items(self):
        return self.pre_fill_items

    def pre_fill(self) -> None:
        self.pre_fill_seeds()
        self.pre_fill_dungeon_items()

        #self.debug_pre_fill("Dimitri's Flute", "Impa Gift")

    def debug_pre_fill(self, i, l):
        collection_state = self.multiworld.get_all_state(False)
        
        locations = [loc for loc in self.multiworld.get_locations(self.player)
                                 if l in loc.name]
        item = [self.create_item(i)]
        print(item)
        print(locations)
        fill_restrictive(self.multiworld, collection_state, locations, item, single_player_placement=True, lock=True, allow_excluded=True)

    def pre_fill_dungeon_items(self):
        # If keysanity is off, dungeon items can only be put inside local dungeon locations, and there are not so many
        # of those which makes them pretty crowded.
        # This usually ends up with generator not having anywhere to place a few small keys, making the seed unbeatable.
        # To circumvent this, we perform a restricted pre-fill here, placing only those dungeon items
        # before anything else.
        collection_state = self.multiworld.get_all_state(False)
        D6_remaining_location = []

        for i in range(0, 10):
            # Build a list of locations in this dungeon
            dungeon_location_names = [name for name, loc in LOCATIONS_DATA.items()
                                      if "dungeon" in loc and loc["dungeon"] == i]
            dungeon_locations = [loc for loc in self.multiworld.get_locations(self.player)
                                 if loc.name in dungeon_location_names]

            # Build a list of dungeon items that are "confined" (i.e. must be placed inside this dungeon)
            # See `create_items` to see how `self.dungeon_items` is populated depending on current options.
            confined_dungeon_items = [item for item in self.dungeon_items if item.name.endswith(f"({DUNGEON_NAMES[i]})") or (i == 8 and "Slate" in item.name)]
            if len(confined_dungeon_items) == 0:
                if i == 9 or i == 6:
                        D6_remaining_location += dungeon_locations
                continue  # This list might be empty with some keysanity options
            for item in confined_dungeon_items:
                collection_state.remove(item)

            # Perform a prefill to place confined items inside locations of this dungeon
            for attempts_remaining in range(2, -1, -1):
                self.random.shuffle(dungeon_locations)
                try:
                    fill_restrictive(self.multiworld, collection_state, dungeon_locations, confined_dungeon_items,
                                     single_player_placement=True, lock=True, allow_excluded=True)
                    if i == 9 or i == 6:
                        D6_remaining_location += dungeon_locations
                    break
                except FillError as exc:
                    if attempts_remaining == 0:
                        raise exc
                    logging.debug(f"Failed to shuffle dungeon items for player {self.player}. Retrying...")

        # D6 specific item that can appear in both dungeon (the boss key)
        d6CommonDungeon = "(Mermaid's Cave)"
        
        confined_dungeon_items = [item for item in self.dungeon_items if item.name.endswith(d6CommonDungeon) ]
        
        for item in confined_dungeon_items:
            collection_state.remove(item)

        # Preplace D6 Boss key
        for attempts_remaining in range(2, -1, -1):
            self.random.shuffle(D6_remaining_location)
            try:
                fill_restrictive(self.multiworld, collection_state, D6_remaining_location, confined_dungeon_items,
                                    single_player_placement=True, lock=True, allow_excluded=True)
                break
            except FillError as exc:
                if attempts_remaining == 0:
                    raise exc
                logging.debug(f"Failed to shuffle dungeon items for player {self.player}. Retrying...")


    def pre_fill_seeds(self) -> None:
        
        def place_seed(seed_name: str, location_name: str):
            seed_item = self.create_item(seed_name)
            self.multiworld.get_location(location_name, self.player).place_locked_item(seed_item)
            self.pre_fill_items.append(seed_item)

        seeds_to_place = set([name for name in SEED_ITEMS if name != SEED_ITEMS[self.options.default_seed.value]])

        manually_placed_trees = ["Lynna City: Seed Tree"]
        trees_to_process = [name for name in TREES_TABLE if name not in manually_placed_trees]

        # Place default seed type in Horon Village tree
        place_seed(SEED_ITEMS[self.options.default_seed.value], "Lynna City: Seed Tree")

        # Place remaining seeds on remaining trees
        self.random.shuffle(trees_to_process)
        for seed in seeds_to_place:
            place_seed(seed, trees_to_process.pop())

        while len(trees_to_process) != 0:
            place_seed(self.random.choice(SEED_ITEMS), trees_to_process.pop())
            

    def get_filler_item_name(self) -> str:
        FILLER_ITEM_NAMES = [
            "Rupees (1)", "Rupees (5)", "Rupees (5)", "Rupees (10)", "Rupees (10)",
            "Rupees (20)", "Rupees (30)",
            "Gasha Seed", "Gasha Seed",
            "Potion"
        ]

        item_name = self.random.choice(FILLER_ITEM_NAMES)
        return item_name
    
    def generate_output(self, output_directory: str):
        patch = ooa_create_appp_patch(self)
        rom_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
                                                  f"{patch.patch_file_ending}")
        patch.write(rom_path)
        return

    def write_spoiler(self, spoiler_handle):
        spoiler_handle.write(f"Apworld version : {VERSION}")
        if self.options.shuffle_dungeons != "vanilla":
            spoiler_handle.write(f"\nDungeon Entrances ({self.multiworld.player_name[self.player]}):\n")
            for entrance, dungeon in self.dungeon_entrances.items():
                spoiler_handle.write(f"\t- {entrance} --> {dungeon.replace('enter ', '')}\n")