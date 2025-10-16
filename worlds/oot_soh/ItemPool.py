from typing import Dict, TYPE_CHECKING
import math

from .Enums import *
from .Items import item_data_table, filler_items, filler_bottles

if TYPE_CHECKING:
    from . import SohWorld


def create_item_pool(world: "SohWorld") -> None:
    items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_data_table.items()}

    filler_bottle_amount: int = 2

    # King Zora
    if world.options.zoras_fountain == "open":
        items_to_create[Items.BOTTLE_WITH_RUTOS_LETTER] = 0
        filler_bottle_amount += 1

    # Overworld door keys
    if world.options.lock_overworld_doors:
        items_to_create[Items.GUARD_HOUSE_KEY] = 1
        items_to_create[Items.MARKET_BAZAAR_KEY] = 1
        items_to_create[Items.MARKET_POTION_SHOP_KEY] = 1
        items_to_create[Items.MASK_SHOP_KEY] = 1
        items_to_create[Items.MARKET_SHOOTING_GALLERY_KEY] = 1
        items_to_create[Items.BOMBCHU_BOWLING_KEY] = 1
        items_to_create[Items.TREASURE_CHEST_GAME_BUILDING_KEY] = 1
        items_to_create[Items.BOMBCHU_SHOP_KEY] = 1
        items_to_create[Items.RICHARDS_HOUSE_KEY] = 1
        items_to_create[Items.ALLEY_HOUSE_KEY] = 1
        items_to_create[Items.KAK_BAZAAR_KEY] = 1
        items_to_create[Items.KAK_POTION_SHOP_KEY] = 1
        items_to_create[Items.BOSS_HOUSE_KEY] = 1
        items_to_create[Items.GRANNYS_POTION_SHOP_KEY] = 1
        items_to_create[Items.SKULLTULA_HOUSE_KEY] = 1
        items_to_create[Items.IMPAS_HOUSE_KEY] = 1
        items_to_create[Items.WINDMILL_KEY] = 1
        items_to_create[Items.KAK_SHOOTING_GALLERY_KEY] = 1
        items_to_create[Items.DAMPES_HUT_KEY] = 1
        items_to_create[Items.TALONS_HOUSE_KEY] = 1
        items_to_create[Items.STABLES_KEY] = 1
        items_to_create[Items.BACK_TOWER_KEY] = 1
        items_to_create[Items.HYLIA_LAB_KEY] = 1
        items_to_create[Items.FISHING_HOLE_KEY] = 1

    # Gerudo Fortress Keys
    if world.options.fortress_carpenters == "fast":
            items_to_create[Items.GERUDO_FORTRESS_SMALL_KEY] = 1

    if world.options.fortress_carpenters == "free":
        items_to_create[Items.GERUDO_FORTRESS_SMALL_KEY] = 0
    
    # Triforce pieces
    if world.options.triforce_hunt:
        total_triforce_pieces = math.floor(world.options.triforce_hunt_required_pieces * (1 + (world.options.triforce_hunt_extra_pieces_percentage / 100)))
        if total_triforce_pieces > 100:
            total_triforce_pieces = 100
        items_to_create[Items.TRIFORCE_PIECE] = total_triforce_pieces

    # Overworld Skull Tokens
    if world.options.shuffle_skull_tokens == "overworld" or world.options.shuffle_skull_tokens == "all":
        items_to_create[Items.GOLD_SKULLTULA_TOKEN] += 56

    # Dungeon Skull Tokens
    if world.options.shuffle_skull_tokens == "dungeon" or world.options.shuffle_skull_tokens == "all":
        items_to_create[Items.GOLD_SKULLTULA_TOKEN] += 44

    # Master Sword
    if world.options.shuffle_master_sword:
        items_to_create[Items.MASTER_SWORD] = 1

    # Child's Wallet
    if world.options.shuffle_childs_wallet:
        items_to_create[Items.PROGRESSIVE_WALLET] += 1

    # Ocarina Buttons
    if world.options.shuffle_ocarina_buttons:
        items_to_create[Items.OCARINA_A_BUTTON] = 1
        items_to_create[Items.OCARINA_CDOWN_BUTTON] = 1
        items_to_create[Items.OCARINA_CLEFT_BUTTON] = 1
        items_to_create[Items.OCARINA_CRIGHT_BUTTON] = 1
        items_to_create[Items.OCARINA_CUP_BUTTON] = 1

    # Swim
    if world.options.shuffle_swim:
        items_to_create[Items.PROGRESSIVE_SCALE] += 1

    # Weird Egg
    if not world.options.skip_child_zelda and world.options.shuffle_weird_egg:
        items_to_create[Items.WEIRD_EGG] = 1

    # Fishing Pole
    if world.options.shuffle_fishing_pole:
        items_to_create[Items.FISHING_POLE] = 1

    # Deku Stick Bag
    if world.options.shuffle_deku_stick_bag:
        items_to_create[Items.PROGRESSIVE_STICK_CAPACITY] += 1

    # Deku Nut Bag
    if world.options.shuffle_deku_nut_bag:
        items_to_create[Items.PROGRESSIVE_NUT_CAPACITY] += 1

    # Merchants
    if world.options.shuffle_merchants == "bean_merchant_only" or world.options.shuffle_merchants == "all":
        items_to_create[Items.MAGIC_BEAN_PACK] = 1

    if world.options.shuffle_merchants == "all_but_beans" or world.options.shuffle_merchants == "all":
        items_to_create[Items.GIANTS_KNIFE] = 1

    # Adult Trade Items
    if world.options.shuffle_adult_trade_items:
        items_to_create[Items.POCKET_EGG] = 1
        items_to_create[Items.COJIRO] = 1
        items_to_create[Items.ODD_MUSHROOM] = 1
        items_to_create[Items.ODD_POTION] = 1
        items_to_create[Items.POACHERS_SAW] = 1
        items_to_create[Items.BROKEN_GORONS_SWORD] = 1
        items_to_create[Items.PRESCRIPTION] = 1
        items_to_create[Items.EYEBALL_FROG] = 1
        items_to_create[Items.WORLDS_FINEST_EYEDROPS] = 1

    # Boss Souls
    if world.options.shuffle_boss_souls:
        items_to_create[Items.GOHMAS_SOUL] = 1
        items_to_create[Items.KING_DODONGOS_SOUL] = 1
        items_to_create[Items.BARINADES_SOUL] = 1
        items_to_create[Items.PHANTOM_GANONS_SOUL] = 1
        items_to_create[Items.VOLVAGIAS_SOUL] = 1
        items_to_create[Items.MORPHAS_SOUL] = 1
        items_to_create[Items.BONGO_BONGOS_SOUL] = 1
        items_to_create[Items.TWINROVAS_SOUL] = 1
    
    if world.options.shuffle_boss_souls == "on_plus_ganons":
        items_to_create[Items.GANONS_SOUL] = 1

    # Dungeon Rewards
    if world.options.shuffle_dungeon_rewards == "anywhere":
        items_to_create[Items.KOKIRIS_EMERALD] = 1
        items_to_create[Items.GORONS_RUBY] = 1
        items_to_create[Items.ZORAS_SAPPHIRE] = 1
        items_to_create[Items.FOREST_MEDALLION] = 1
        items_to_create[Items.FIRE_MEDALLION] = 1
        items_to_create[Items.WATER_MEDALLION] = 1
        items_to_create[Items.SPIRIT_MEDALLION] = 1
        items_to_create[Items.SHADOW_MEDALLION] = 1
        items_to_create[Items.LIGHT_MEDALLION] = 1

    # Maps and Compasses
    if world.options.maps_and_compasses:
        items_to_create[Items.GREAT_DEKU_TREE_MAP] = 1
        items_to_create[Items.DODONGOS_CAVERN_MAP] = 1
        items_to_create[Items.JABU_JABUS_BELLY_MAP] = 1
        items_to_create[Items.FOREST_TEMPLE_MAP] = 1
        items_to_create[Items.FIRE_TEMPLE_MAP] = 1
        items_to_create[Items.WATER_TEMPLE_MAP] = 1
        items_to_create[Items.SPIRIT_TEMPLE_MAP] = 1
        items_to_create[Items.SHADOW_TEMPLE_MAP] = 1
        items_to_create[Items.BOTTOM_OF_THE_WELL_MAP] = 1
        items_to_create[Items.ICE_CAVERN_MAP] = 1
        items_to_create[Items.GREAT_DEKU_TREE_COMPASS] = 1
        items_to_create[Items.DODONGOS_CAVERN_COMPASS] = 1
        items_to_create[Items.JABU_JABUS_BELLY_COMPASS] = 1
        items_to_create[Items.FOREST_TEMPLE_COMPASS] = 1
        items_to_create[Items.FIRE_TEMPLE_COMPASS] = 1
        items_to_create[Items.WATER_TEMPLE_COMPASS] = 1
        items_to_create[Items.SPIRIT_TEMPLE_COMPASS] = 1
        items_to_create[Items.SHADOW_TEMPLE_COMPASS] = 1
        items_to_create[Items.BOTTOM_OF_THE_WELL_COMPASS] = 1
        items_to_create[Items.ICE_CAVERN_COMPASS] = 1

    # Ganon's Castle Boss Key
    if world.options.ganons_castle_boss_key == "anywhere" and not world.options.triforce_hunt:
        items_to_create[Items.GANONS_CASTLE_BOSS_KEY] = 1

    # Key Rings
    if world.options.key_rings:
        items_to_create[Items.FOREST_TEMPLE_SMALL_KEY] = 0
        items_to_create[Items.FIRE_TEMPLE_SMALL_KEY] = 0
        items_to_create[Items.WATER_TEMPLE_SMALL_KEY] = 0
        items_to_create[Items.SPIRIT_TEMPLE_SMALL_KEY] = 0
        items_to_create[Items.SHADOW_TEMPLE_SMALL_KEY] = 0
        items_to_create[Items.BOTTOM_OF_THE_WELL_SMALL_KEY] = 0
        items_to_create[Items.TRAINING_GROUND_SMALL_KEY] = 0
        items_to_create[Items.GANONS_CASTLE_SMALL_KEY] = 0
        items_to_create[Items.FOREST_TEMPLE_KEY_RING] = 1
        items_to_create[Items.FIRE_TEMPLE_KEY_RING] = 1
        items_to_create[Items.WATER_TEMPLE_KEY_RING] = 1
        items_to_create[Items.SPIRIT_TEMPLE_KEY_RING] = 1
        items_to_create[Items.SHADOW_TEMPLE_KEY_RING] = 1
        items_to_create[Items.BOTTOM_OF_THE_WELL_KEY_RING] = 1
        items_to_create[Items.TRAINING_GROUND_KEY_RING] = 1
        items_to_create[Items.GANONS_CASTLE_KEY_RING] = 1
        if world.options.fortress_carpenters == "normal":
            items_to_create[Items.GERUDO_FORTRESS_SMALL_KEY] = 0
            items_to_create[Items.GERUDO_FORTRESS_KEY_RING] = 1

    # Big Poe Bottle
    if world.options.big_poe_target_count == 0:
        items_to_create[Items.BOTTLE_WITH_BIG_POE] = 0
        filler_bottle_amount += 1

    # Bombchu bag
    if world.options.bombchu_bag:
        items_to_create[Items.BOMBCHUS_5] = 0
        items_to_create[Items.BOMBCHUS_10] = 0
        items_to_create[Items.BOMBCHUS_20] = 0
        items_to_create[Items.PROGRESSIVE_BOMBCHU] = 5

    # Infinite Upgrades
    if world.options.infinite_upgrades == "progressive":
        items_to_create[Items.PROGRESSIVE_BOMB_BAG] += 1
        items_to_create[Items.PROGRESSIVE_BOW] += 1
        items_to_create[Items.PROGRESSIVE_NUT_CAPACITY] += 1
        items_to_create[Items.PROGRESSIVE_SLINGSHOT] += 1
        items_to_create[Items.PROGRESSIVE_STICK_CAPACITY] += 1
        items_to_create[Items.PROGRESSIVE_MAGIC_METER] += 1
        items_to_create[Items.PROGRESSIVE_WALLET] += 1

    # Skeleton Key
    if world.options.skeleton_key:
        items_to_create[Items.SKELETON_KEY] = 1

    # Add regular item pool
    for item, quantity in items_to_create.items():
        for _ in range(quantity):
            world.item_pool.append(world.create_item(item))

    # Add random filler bottles
    world.item_pool += [world.create_item(get_filler_bottle(world)) for _ in range(filler_bottle_amount)]

def get_filler_item(world: "SohWorld") -> str:
    return world.random.choice(filler_items)

def get_filler_bottle(world: "SohWorld") -> str:
    return world.random.choice(filler_bottles)
