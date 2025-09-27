from typing import List, Dict, Any
import math

from BaseClasses import CollectionState, Item, Region, Tutorial
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World
from .Items import SohItem, item_data_table, item_table, filler_items, filler_bottles
from .Locations import SohLocation, SohLocationData, base_location_table, \
    gold_skulltula_overworld_location_table, \
    gold_skulltula_dungeon_location_table, \
    shops_location_table, \
    scrubs_location_table, \
    trade_items_location_table, \
    merchants_items_location_table, \
    cows_location_table, \
    frogs_location_table, \
    beehives_location_table, \
    pots_overworld_location_table, \
    pots_dungeon_location_table, \
    crates_overworld_location_table, \
    crates_dungeon_location_table, \
    freestanding_overworld_location_table, \
    freestanding_dungeon_location_table, \
    fairies_location_table, \
    grass_overworld_location_table, \
    grass_dungeon_location_table, \
    fish_pond_location_table, \
    fish_overworld_location_table, \
    child_zelda_location_table, \
    carpenters_location_table, \
    location_table
from .Options import SohOptions
from .RegionAgeAccess import reset_age_access, update_age_access
from .Regions import region_data_table
from .Enums import *
from ...location_access import root
from ...location_access.overworld import \
    castle_grounds, \
    death_mountain_crater, \
    death_mountain_trail, \
    desert_colossus, \
    gerudo_fortress, \
    gerudo_valley, \
    goron_city, \
    graveyard, \
    haunted_wasteland, \
    hyrule_field, \
    kakariko, \
    kokiri_forest, \
    lake_hylia, \
    lon_lon_ranch
from ...location_access.dungeons import \
    bottom_of_the_well, \
    deku_tree, \
    dodongos_cavern, \
    fire_temple, \
    forest_temple, \
    ganons_castle, \
    gerudo_training_ground, \
    ice_cavern, \
    jabujabus_belly, \
    shadow_temple, \
    spirit_temple, \
    water_temple

import logging
logger = logging.getLogger("SOH_OOT")

class SohWebWorld(WebWorld):
    theme = "ice"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Ship of Harkinian.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["aMannus"]
    )
    
    tutorials = [setup_en]
    game_info_languages = ["en"]


class SohWorld(World):
    """A PC Port of Ocarina of Time"""

    game = "Ship of Harkinian"
    web = SohWebWorld()
    options: SohOptions
    options_dataclass = SohOptions
    location_name_to_id = location_table
    item_name_to_id = item_table

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.included_locations = dict[str: int]()

    def generate_early(self) -> None:
        #input("\033[33m WARNING: Ship of Harkinian currently only supports SOME LOGIC! There may still be impossible generations. If you're OK with this, press Enter to continue. \033[0m")
        pass

    def create_item(self, name: str) -> SohItem:
        return SohItem(name, item_data_table[name].classification, item_data_table[name].item_id, self.player)

    def create_items(self) -> None:
        item_pool: List[SohItem] = []

        items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_data_table.items()}

        filler_bottle_amount: int = 2

        # King Zora
        if self.options.zoras_fountain == "open":
            items_to_create[Items.BOTTLE_WITH_RUTOS_LETTER.value] = 0
            filler_bottle_amount += 1

        # Overworld door keys
        if self.options.lock_overworld_doors:
            items_to_create[Items.GUARD_HOUSE_KEY.value] = 1
            items_to_create[Items.MARKET_BAZAAR_KEY.value] = 1
            items_to_create[Items.MARKET_POTION_SHOP_KEY.value] = 1
            items_to_create[Items.MASK_SHOP_KEY.value] = 1
            items_to_create[Items.MARKET_SHOOTING_GALLERY_KEY.value] = 1
            items_to_create[Items.BOMBCHU_BOWLING_KEY.value] = 1
            items_to_create[Items.TREASURE_CHEST_GAME_BUILDING_KEY.value] = 1
            items_to_create[Items.BOMBCHU_SHOP_KEY.value] = 1
            items_to_create[Items.RICHARDS_HOUSE_KEY.value] = 1
            items_to_create[Items.ALLEY_HOUSE_KEY.value] = 1
            items_to_create[Items.KAK_BAZAAR_KEY.value] = 1
            items_to_create[Items.KAK_POTION_SHOP_KEY.value] = 1
            items_to_create[Items.BOSS_HOUSE_KEY.value] = 1
            items_to_create[Items.GRANNYS_POTION_SHOP_KEY.value] = 1
            items_to_create[Items.SKULLTULA_HOUSE_KEY.value] = 1
            items_to_create[Items.IMPAS_HOUSE_KEY.value] = 1
            items_to_create[Items.WINDMILL_KEY.value] = 1
            items_to_create[Items.KAK_SHOOTING_GALLERY_KEY.value] = 1
            items_to_create[Items.DAMPES_HUT_KEY.value] = 1
            items_to_create[Items.TALONS_HOUSE_KEY.value] = 1
            items_to_create[Items.STABLES_KEY.value] = 1
            items_to_create[Items.BACK_TOWER_KEY.value] = 1
            items_to_create[Items.HYLIA_LAB_KEY.value] = 1
            items_to_create[Items.FISHING_HOLE_KEY.value] = 1

        # Gerudo Fortress Keys
        if self.options.fortress_carpenters == "fast":
                items_to_create[Items.GERUDO_FORTRESS_SMALL_KEY.value] = 1

        if self.options.fortress_carpenters == "free":
            items_to_create[Items.GERUDO_FORTRESS_SMALL_KEY.value] = 0
        
        # Triforce pieces
        if self.options.triforce_hunt:
            total_triforce_pieces = math.floor(self.options.triforce_hunt_required_pieces * (1 + (self.options.triforce_hunt_extra_pieces_percentage / 100)))
            if total_triforce_pieces > 100:
                total_triforce_pieces = 100
            items_to_create[Items.TRIFORCE_PIECE.value] = total_triforce_pieces

        # Overworld Skull Tokens
        if self.options.shuffle_skull_tokens == "overworld" or self.options.shuffle_skull_tokens == "all":
            items_to_create[Items.GOLD_SKULLTULA_TOKEN.value] += 56

        # Dungeon Skull Tokens
        if self.options.shuffle_skull_tokens == "dungeon" or self.options.shuffle_skull_tokens == "all":
            items_to_create[Items.GOLD_SKULLTULA_TOKEN.value] += 44

        # Master Sword
        if self.options.shuffle_master_sword:
            items_to_create[Items.MASTER_SWORD.value] = 1

        # Child's Wallet
        if self.options.shuffle_childs_wallet:
            items_to_create[Items.PROGRESSIVE_WALLET.value] += 1

        # Ocarina Buttons
        if self.options.shuffle_ocarina_buttons:
            items_to_create[Items.OCARINA_ABUTTON.value] = 1
            items_to_create[Items.OCARINA_CDOWN_BUTTON.value] = 1
            items_to_create[Items.OCARINA_CLEFT_BUTTON.value] = 1
            items_to_create[Items.OCARINA_CRIGHT_BUTTON.value] = 1
            items_to_create[Items.OCARINA_CUP_BUTTON.value] = 1

        # Swim
        if self.options.shuffle_swim:
            items_to_create[Items.PROGRESSIVE_SCALE.value] += 1

        # Weird Egg
        if not self.options.skip_child_zelda and self.options.shuffle_weird_egg:
            items_to_create[Items.WEIRD_EGG.value] = 1

        # Fishing Pole
        if self.options.shuffle_fishing_pole:
            items_to_create[Items.FISHING_POLE.value] = 1

        # Deku Stick Bag
        if self.options.shuffle_deku_stick_bag:
            items_to_create[Items.PROGRESSIVE_STICK_CAPACITY.value] += 1

        # Deku Nut Bag
        if self.options.shuffle_deku_nut_bag:
            items_to_create[Items.PROGRESSIVE_NUT_CAPACITY.value] += 1

        # Merchants
        if self.options.shuffle_merchants == "bean_merchant_only" or self.options.shuffle_merchants == "all":
            items_to_create[Items.MAGIC_BEAN_PACK.value] = 1

        if self.options.shuffle_merchants == "all_but_beans" or self.options.shuffle_merchants == "all":
            items_to_create[Items.GIANTS_KNIFE.value] = 1

        # Adult Trade Items
        if self.options.shuffle_adult_trade_items:
            items_to_create[Items.POCKET_EGG.value] = 1
            items_to_create[Items.COJIRO.value] = 1
            items_to_create[Items.ODD_MUSHROOM.value] = 1
            items_to_create[Items.ODD_POTION.value] = 1
            items_to_create[Items.POACHERS_SAW.value] = 1
            items_to_create[Items.BROKEN_GORONS_SWORD.value] = 1
            items_to_create[Items.PRESCRIPTION.value] = 1
            items_to_create[Items.EYEBALL_FROG.value] = 1
            items_to_create[Items.WORLDS_FINEST_EYEDROPS.value] = 1

        # Boss Souls
        if self.options.shuffle_boss_souls:
            items_to_create[Items.GOHMAS_SOUL.value] = 1
            items_to_create[Items.KING_DODONGOS_SOUL.value] = 1
            items_to_create[Items.BARINADES_SOUL.value] = 1
            items_to_create[Items.PHANTOM_GANONS_SOUL.value] = 1
            items_to_create[Items.VOLVAGIAS_SOUL.value] = 1
            items_to_create[Items.MORPHAS_SOUL.value] = 1
            items_to_create[Items.BONGO_BONGOS_SOUL.value] = 1
            items_to_create[Items.TWINROVAS_SOUL.value] = 1
        
        if self.options.shuffle_boss_souls == "on_plus_ganons":
            items_to_create[Items.GANONS_SOUL.value] = 1

        # Dungeon Rewards
        if self.options.shuffle_dungeon_rewards == "anywhere":
            items_to_create[Items.KOKIRIS_EMERALD.value] = 1
            items_to_create[Items.GORONS_RUBY.value] = 1
            items_to_create[Items.ZORAS_SAPPHIRE.value] = 1
            items_to_create[Items.FOREST_MEDALLION.value] = 1
            items_to_create[Items.FIRE_MEDALLION.value] = 1
            items_to_create[Items.WATER_MEDALLION.value] = 1
            items_to_create[Items.SPIRIT_MEDALLION.value] = 1
            items_to_create[Items.SHADOW_MEDALLION.value] = 1
            items_to_create[Items.LIGHT_MEDALLION.value] = 1

        # Maps and Compasses
        if self.options.maps_and_compasses:
            items_to_create[Items.GREAT_DEKU_TREE_MAP.value] = 1
            items_to_create[Items.DODONGOS_CAVERN_MAP.value] = 1
            items_to_create[Items.JABU_JABUS_BELLY_MAP.value] = 1
            items_to_create[Items.FOREST_TEMPLE_MAP.value] = 1
            items_to_create[Items.FIRE_TEMPLE_MAP.value] = 1
            items_to_create[Items.WATER_TEMPLE_MAP.value] = 1
            items_to_create[Items.SPIRIT_TEMPLE_MAP.value] = 1
            items_to_create[Items.SHADOW_TEMPLE_MAP.value] = 1
            items_to_create[Items.BOTTOM_OF_THE_WELL_MAP.value] = 1
            items_to_create[Items.ICE_CAVERN_MAP.value] = 1
            items_to_create[Items.GREAT_DEKU_TREE_COMPASS.value] = 1
            items_to_create[Items.DODONGOS_CAVERN_COMPASS.value] = 1
            items_to_create[Items.JABU_JABUS_BELLY_COMPASS.value] = 1
            items_to_create[Items.FOREST_TEMPLE_COMPASS.value] = 1
            items_to_create[Items.FIRE_TEMPLE_COMPASS.value] = 1
            items_to_create[Items.WATER_TEMPLE_COMPASS.value] = 1
            items_to_create[Items.SPIRIT_TEMPLE_COMPASS.value] = 1
            items_to_create[Items.SHADOW_TEMPLE_COMPASS.value] = 1
            items_to_create[Items.BOTTOM_OF_THE_WELL_COMPASS.value] = 1
            items_to_create[Items.ICE_CAVERN_COMPASS.value] = 1

        # Ganon's Castle Boss Key
        if self.options.ganons_castle_boss_key == "anywhere" and not self.options.triforce_hunt:
            items_to_create[Items.GANONS_CASTLE_BOSS_KEY.value] = 1

        # Key Rings
        if self.options.key_rings:
            items_to_create[Items.FOREST_TEMPLE_SMALL_KEY.value] = 0
            items_to_create[Items.FIRE_TEMPLE_SMALL_KEY.value] = 0
            items_to_create[Items.WATER_TEMPLE_SMALL_KEY.value] = 0
            items_to_create[Items.SPIRIT_TEMPLE_SMALL_KEY.value] = 0
            items_to_create[Items.SHADOW_TEMPLE_SMALL_KEY.value] = 0
            items_to_create[Items.BOTTOM_OF_THE_WELL_SMALL_KEY.value] = 0
            items_to_create[Items.TRAINING_GROUND_SMALL_KEY.value] = 0
            items_to_create[Items.GANONS_CASTLE_SMALL_KEY.value] = 0
            items_to_create[Items.FOREST_TEMPLE_KEY_RING.value] = 1
            items_to_create[Items.FIRE_TEMPLE_KEY_RING.value] = 1
            items_to_create[Items.WATER_TEMPLE_KEY_RING.value] = 1
            items_to_create[Items.SPIRIT_TEMPLE_KEY_RING.value] = 1
            items_to_create[Items.SHADOW_TEMPLE_KEY_RING.value] = 1
            items_to_create[Items.BOTTOM_OF_THE_WELL_KEY_RING.value] = 1
            items_to_create[Items.TRAINING_GROUND_KEY_RING.value] = 1
            items_to_create[Items.GANONS_CASTLE_KEY_RING.value] = 1
            if self.options.fortress_carpenters == "normal":
                items_to_create[Items.GERUDO_FORTRESS_SMALL_KEY.value] = 0
                items_to_create[Items.GERUDO_FORTRESS_KEY_RING.value] = 1

        # Big Poe Bottle
        if self.options.big_poe_target_count == 0:
            items_to_create[Items.BOTTLE_WITH_BIG_POE.value] = 0
            filler_bottle_amount += 1

        # Bombchu bag
        if self.options.bombchu_bag:
            items_to_create[Items.BOMBCHUS_5.value] = 0
            items_to_create[Items.BOMBCHUS_10.value] = 0
            items_to_create[Items.BOMBCHUS_20.value] = 0
            items_to_create[Items.PROGRESSIVE_BOMBCHU.value] = 5

        # Infinite Upgrades
        if self.options.infinite_upgrades == "progressive":
            items_to_create[Items.PROGRESSIVE_BOMB_BAG.value] += 1
            items_to_create[Items.PROGRESSIVE_BOW.value] += 1
            items_to_create[Items.PROGRESSIVE_NUT_CAPACITY.value] += 1
            items_to_create[Items.PROGRESSIVE_SLINGSHOT.value] += 1
            items_to_create[Items.PROGRESSIVE_STICK_CAPACITY.value] += 1
            items_to_create[Items.PROGRESSIVE_MAGIC_METER.value] += 1
            items_to_create[Items.PROGRESSIVE_WALLET.value] += 1

        # Skeleton Key
        if self.options.skeleton_key:
            items_to_create[Items.SKELETON_KEY.value] = 1

        # Add regular item pool
        for item, quantity in items_to_create.items():
            for _ in range(quantity):
                item_pool.append(self.create_item(item))

        # Add random filler bottles
        item_pool += [self.create_item(self.get_filler_bottle_name()) for _ in range(filler_bottle_amount)]

        # Add junk items to fill remaining locations
        open_location_count = sum(1 for loc in self.get_locations() if not loc.locked)
        filler_item_count: int = open_location_count - len(item_pool)
        item_pool += [self.create_item(self.get_filler_item_name()) for _ in range(filler_item_count)]

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None: 

        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)
            region.add_exits(region_data_table[region_name].connecting_regions)

        # Create locations.

            # Base locations
            self.included_locations.update({
                location_name: location_data.address for location_name, location_data in base_location_table.items()
            })

            # Gold Skulltulas (Overworld)
            self.included_locations.update({
                location_name: location_data.address for location_name, location_data in gold_skulltula_overworld_location_table.items()
            })

            # Gold Skulltulas (Dungeon)
            self.included_locations.update({
                location_name: location_data.address for location_name, location_data in gold_skulltula_dungeon_location_table.items()
            })

            # Shops
            if self.options.shuffle_shops:
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in shops_location_table.items()
                })

            # Scrubs
            if self.options.shuffle_scrubs:
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in scrubs_location_table.items()
                })

            # Adult Trade Items
            if self.options.shuffle_adult_trade_items:
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in trade_items_location_table.items()
                })

            # Merchants
            if self.options.shuffle_merchants == "bean_merchant_only" or self.options.shuffle_merchants == "all":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in merchants_items_location_table.items()
                    #if location_data.region == region_name and location_name == "ZR Magic Bean Salesman"
                })

            if self.options.shuffle_merchants == "all_but_beans" or self.options.shuffle_merchants == "all":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in merchants_items_location_table.items()
                    #if location_data.region == region_name and (location_name == "Kak Granny's Shop" or location_name == "GC Medigoron" or location_name == "Wasteland Carpet Salesman")
                })

            # Cows
            if self.options.shuffle_cows:
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in cows_location_table.items()
                })

            # Frogs
            if self.options.shuffle_frog_song_rupees:
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in frogs_location_table.items()
                })

            # Beehives
            if self.options.shuffle_beehives:
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in beehives_location_table.items()
                })

            # Pots (Overworld)
            if self.options.shuffle_pots == "overworld" or self.options.shuffle_pots == "all":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in pots_overworld_location_table.items()
                })

            # Pots (Dungeon)
            if self.options.shuffle_pots == "dungeon" or self.options.shuffle_pots == "all":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in pots_dungeon_location_table.items()
                })

            # Crates (Overworld)
            if self.options.shuffle_crates == "overworld" or self.options.shuffle_crates == "all":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in crates_overworld_location_table.items()
                })

            # Crates (Dungeon)
            if self.options.shuffle_crates == "dungeon" or self.options.shuffle_crates == "all":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in crates_dungeon_location_table.items()
                })

            # Freestanding (Overworld)
            if self.options.shuffle_freestanding_items == "overworld" or self.options.shuffle_freestanding_items == "all":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in freestanding_overworld_location_table.items()
                })

            # Freestanding (Dungeon)
            if self.options.shuffle_freestanding_items == "dungeon" or self.options.shuffle_freestanding_items == "all":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in freestanding_dungeon_location_table.items()
                })

            # Fairies
            if self.options.shuffle_fairies:
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in fairies_location_table.items()
                })

            # Grass (Overworld)
            if self.options.shuffle_grass == "overworld" or self.options.shuffle_grass == "all":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in grass_overworld_location_table.items()
                })

            # Grass (Dungeon)
            if self.options.shuffle_grass == "dungeon" or self.options.shuffle_grass == "all":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in grass_dungeon_location_table.items()
                })

            # Fish (Pond)
            if self.options.shuffle_fish == "pond" or self.options.shuffle_fish == "all":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in fish_pond_location_table.items()
                })

            # Fish (Overworld)
            if self.options.shuffle_fish == "overworld" or self.options.shuffle_fish == "all":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in fish_overworld_location_table.items()
                })

            # Child Zelda
            if not self.options.skip_child_zelda:
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in child_zelda_location_table.items()
                })

            # Carpenters
            if self.options.fortress_carpenters == "normal":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in carpenters_location_table.items()
                })

            if self.options.fortress_carpenters == "fast":
                self.included_locations.update({
                    location_name: location_data.address for location_name, location_data in carpenters_location_table.items()
                    #if location_data.region == region_name and (location_name == "GF Freed All Carpenters" or location_name == "GF 1 Torch Carpenter")
                })
            
        # Set region rules and location rules after all locations are created
        # Root
        root.create_regions_and_rules(self)

        # Overworld
        castle_grounds.create_regions_and_rules(self)
        death_mountain_crater.create_regions_and_rules(self)
        death_mountain_trail.create_regions_and_rules(self)
        desert_colossus.create_regions_and_rules(self)
        gerudo_fortress.create_regions_and_rules(self)
        gerudo_valley.create_regions_and_rules(self)
        goron_city.create_regions_and_rules(self)
        graveyard.create_regions_and_rules(self)
        haunted_wasteland.create_regions_and_rules(self)
        hyrule_field.create_regions_and_rules(self)
        kakariko.create_regions_and_rules(self)
        kokiri_forest.create_regions_and_rules(self)
        lake_hylia.create_regions_and_rules(self)
        lon_lon_ranch.create_regions_and_rules(self)
        
        # Dungeons
        bottom_of_the_well.create_regions_and_rules(self)
        deku_tree.create_regions_and_rules(self)
        dodongos_cavern.create_regions_and_rules(self)
        fire_temple.create_regions_and_rules(self)
        forest_temple.create_regions_and_rules(self)
        ganons_castle.create_regions_and_rules(self)
        gerudo_training_ground.create_regions_and_rules(self)
        ice_cavern.create_regions_and_rules(self)
        jabujabus_belly.create_regions_and_rules(self)
        shadow_temple.create_regions_and_rules(self)
        spirit_temple.create_regions_and_rules(self)
        water_temple.create_regions_and_rules(self)

        # Place any locations that were missed
        # TODO should be removed when logic is done
        for location_name, location_address in self.included_locations.items():
            self.get_region(Regions.ROOT.value).add_locations({location_name: location_address}, SohLocation)

        # Add Weird Egg and Zelda's Letter to their vanilla locations when not shuffled
        if not self.options.skip_child_zelda and not self.options.shuffle_weird_egg:
            self.get_location(Locations.HC_MALON_EGG.value).place_locked_item(self.create_item(Items.WEIRD_EGG.value))

        if not self.options.skip_child_zelda:
            self.get_location(Locations.HC_ZELDAS_LETTER.value).place_locked_item(self.create_item(Items.ZELDAS_LETTER.value))

        # Place Master Sword on vanilla location if not shuffled
        if not self.options.shuffle_master_sword:
            self.get_location(Locations.MARKET_TOT_MASTER_SWORD.value).place_locked_item(self.create_item(Items.MASTER_SWORD.value))

        # Handle vanilla goron tunic in shop
        # TODO: Proper implementation of vanilla shop items and shuffle them amongst all shops
        if self.options.shuffle_shops:
            self.get_location(Locations.GC_SHOP_ITEM1.value).place_locked_item(self.create_item(Items.BUY_GORON_TUNIC.value))

        # Create a dictionary mapping blue warp rewards to their vanilla items
        dungeon_reward_item_mapping = {
            Locations.QUEEN_GOHMA.value: Items.KOKIRIS_EMERALD.value,
            Locations.KING_DODONGO.value: Items.GORONS_RUBY.value,
            Locations.BARINADE.value: Items.ZORAS_SAPPHIRE.value,
            Locations.PHANTOM_GANON.value: Items.FOREST_MEDALLION.value,
            Locations.VOLVAGIA.value: Items.FIRE_MEDALLION.value,
            Locations.MORPHA.value: Items.WATER_MEDALLION.value,
            Locations.BONGO_BONGO.value: Items.SHADOW_MEDALLION.value,
            Locations.TWINROVA.value: Items.SPIRIT_MEDALLION.value,
            Locations.LINKS_POCKET.value: Items.LIGHT_MEDALLION.value
        }

        # Preplace dungeon rewards in vanilla locations when not shuffled
        if self.options.shuffle_dungeon_rewards == "off":      
            # Loop through dungeons rewards and set their items to the vanilla reward.      
            for location_name, reward_name in zip(dungeon_reward_item_mapping.keys(), dungeon_reward_item_mapping.values()):
                self.get_location(location_name).place_locked_item(self.create_item(reward_name))

        if self.options.shuffle_dungeon_rewards == "dungeons": 
            # Extract and shuffle just the item names from location_item_mapping
            reward_names = list(dungeon_reward_item_mapping.values())
            self.random.shuffle(reward_names)
            
            # Pair each location with a unique shuffled dungeon reward
            for location_name, reward_name in zip(dungeon_reward_item_mapping.keys(), reward_names):
                self.get_location(location_name).place_locked_item(self.create_item(reward_name))

        # Place Ganons Boss Key
        if not self.options.ganons_castle_boss_key == "vanilla" and not self.options.ganons_castle_boss_key == "anywhere" and not self.options.triforce_hunt:
            self.get_location(Locations.MARKET_TOT_LIGHT_ARROW_CUTSCENE.value).place_locked_item(self.create_item(Items.GANONS_CASTLE_BOSS_KEY.value))

        if self.options.ganons_castle_boss_key == "vanilla" and not self.options.triforce_hunt:
            self.get_location(Locations.GANONS_CASTLE_TOWER_BOSS_KEY_CHEST.value).place_locked_item(self.create_item(Items.GANONS_CASTLE_BOSS_KEY.value))

        # Preplace tokens based on settings.
        if self.options.shuffle_skull_tokens == "off" or self.options.shuffle_skull_tokens == "dungeon":
            token_item = self.create_item(Items.GOLD_SKULLTULA_TOKEN.value)
            for location_name, location_data in gold_skulltula_overworld_location_table.items():
                self.get_location(location_name).place_locked_item(token_item)

        if self.options.shuffle_skull_tokens == "off" or self.options.shuffle_skull_tokens == "overworld":
            token_item = self.create_item(Items.GOLD_SKULLTULA_TOKEN.value)
            for location_name, location_data in gold_skulltula_dungeon_location_table.items():
                self.get_location(location_name).place_locked_item(token_item)
        

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)
    
    def get_filler_bottle_name(self) -> str:
        return self.random.choice(filler_bottles)

    def set_rules(self) -> None:
        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: True

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "closed_forest": self.options.closed_forest.value,
            "kakariko_gate": self.options.kakariko_gate.value,
            "door_of_time": self.options.door_of_time.value,
            "zoras_fountain": self.options.zoras_fountain.value,
            "sleeping_waterfall": self.options.sleeping_waterfall.value,
            "jabu_jabu": self.options.jabu_jabu.value,
            "lock_overworld_doors": self.options.lock_overworld_doors.value,
            "fortress_carpenters": self.options.fortress_carpenters.value,
            "rainbow_bridge": self.options.rainbow_bridge.value,
            "rainbow_bridge_stones_required": self.options.rainbow_bridge_stones_required.value,
            "rainbow_bridge_medallions_required": self.options.rainbow_bridge_medallions_required.value,
            "rainbow_bridge_dungeon_rewards_required": self.options.rainbow_bridge_dungeon_rewards_required.value,
            "rainbow_bridge_dungeons_required": self.options.rainbow_bridge_dungeons_required.value,
            "rainbow_bridge_skull_tokens_required": self.options.rainbow_bridge_skull_tokens_required.value,
            "ganons_trials_required": self.options.ganons_trials_required.value,
            "triforce_hunt": self.options.triforce_hunt.value,
            "triforce_hunt_required_pieces": self.options.triforce_hunt_required_pieces.value,
            "triforce_hunt_extra_pieces_percentage": self.options.triforce_hunt_extra_pieces_percentage.value,
            "shuffle_skull_tokens": self.options.shuffle_skull_tokens.value,
            "shuffle_master_sword": self.options.shuffle_master_sword.value,
            "shuffle_childs_wallet": self.options.shuffle_childs_wallet.value,
            "shuffle_ocarina_buttons": self.options.shuffle_ocarina_buttons.value,
            "shuffle_swim": self.options.shuffle_swim.value,
            "shuffle_weird_egg": self.options.shuffle_weird_egg.value,
            "shuffle_fishing_pole": self.options.shuffle_fishing_pole.value,
            "shuffle_deku_stick_bag": self.options.shuffle_deku_stick_bag.value,
            "shuffle_deku_nut_bag": self.options.shuffle_deku_nut_bag.value,
            "shuffle_freestanding_items": self.options.shuffle_freestanding_items.value,
            "shuffle_shops": self.options.shuffle_shops.value,
            "shuffle_fish": self.options.shuffle_fish.value,
            "shuffle_scrubs": self.options.shuffle_scrubs.value,
            "shuffle_beehives": self.options.shuffle_beehives.value,
            "shuffle_cows": self.options.shuffle_cows.value,
            "shuffle_pots": self.options.shuffle_pots.value,
            "shuffle_crates": self.options.shuffle_crates.value,
            "shuffle_merchants": self.options.shuffle_merchants.value,
            "shuffle_frog_song_rupees": self.options.shuffle_frog_song_rupees.value,
            "shuffle_adult_trade_items": self.options.shuffle_adult_trade_items.value,
            "shuffle_boss_souls": self.options.shuffle_boss_souls.value,
            "shuffle_fairies": self.options.shuffle_fairies.value,
            "shuffle_grass": self.options.shuffle_grass.value,
            "shuffle_dungeon_rewards": self.options.shuffle_dungeon_rewards.value,
            "maps_and_compasses": self.options.maps_and_compasses.value,
            "ganons_castle_boss_key": self.options.ganons_castle_boss_key.value,
            "ganons_castle_boss_key_stones_required": self.options.ganons_castle_boss_key_stones_required.value,
            "ganons_castle_boss_key_medallions_required": self.options.ganons_castle_boss_key_medallions_required.value,
            "ganons_castle_boss_key_dungeon_rewards_required": self.options.ganons_castle_boss_key_dungeon_rewards_required.value,
            "ganons_castle_boss_key_dungeons_required": self.options.ganons_castle_boss_key_dungeons_required.value,
            "ganons_castle_boss_key_skull_tokens_required": self.options.ganons_castle_boss_key_skull_tokens_required.value,
            "key_rings": self.options.key_rings.value,
            "big_poe_target_count": self.options.big_poe_target_count.value,
            "skip_child_zelda": self.options.skip_child_zelda.value,
            "skip_epona_race": self.options.skip_epona_race.value,
            "complete_mask_quest": self.options.complete_mask_quest.value,
            "skip_scarecrows_song": self.options.skip_scarecrows_song.value,
            "full_wallets": self.options.full_wallets.value,
            "bombchu_bag": self.options.bombchu_bag.value,
            "bombchu_drops": self.options.bombchu_drops.value,
            "blue_fire_arrows": self.options.blue_fire_arrows.value,
            "sunlight_arrows": self.options.sunlight_arrows.value,
            "infinite_upgrades": self.options.infinite_upgrades.value,
            "skeleton_key": self.options.skeleton_key.value,
        }
    
    def collect(self, state: CollectionState, item: Item) -> bool:
        # Temporarily disabled because logic is in progress
        #update_age_access(self, state)
        return super().collect(state, item)
    
    def remove(self, state: CollectionState, item: Item) -> bool:
        # Temporarily disabled because logic is in progress
        #reset_age_access() #TODO pass the starting age option 
        #update_age_access(self, state)
        return super().remove(state, item)

    def generate_output(self, output_directory: str):
    
        visualize_regions(self.multiworld.get_region(self.origin_region_name, self.player), f"SOH-Player{self.player}.puml",
                        show_entrance_names=True,
                        regions_to_highlight=self.multiworld.get_all_state().reachable_regions[
                            self.player])