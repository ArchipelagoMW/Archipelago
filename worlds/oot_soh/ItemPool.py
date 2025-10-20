from typing import TYPE_CHECKING

from .Enums import *
from .Items import item_data_table, filler_items, filler_bottles

if TYPE_CHECKING:
    from . import SohWorld


def create_item_pool(world: "SohWorld") -> None:
    items_to_create: dict[str, int] = {
        item: data.quantity_in_item_pool for item, data in item_data_table.items()}

    # King Zora
    if world.options.zoras_fountain == "open":
        items_to_create[Items.BOTTLE_WITH_RUTOS_LETTER] = 0

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
        new_items = [world.create_item(item) for _ in range(quantity)]
        world.multiworld.itempool += new_items
        world.item_pool += [world.create_item(item) for _ in range(quantity)]

    filler_bottle_amount: int = 2
    if world.options.zoras_fountain == "open":
        filler_bottle_amount += 1
    if world.options.big_poe_target_count == 0:
        filler_bottle_amount += 1

    # Add random filler bottles
    filler_bottle_items = [world.create_item(
        get_filler_bottle(world)) for _ in range(filler_bottle_amount)]
    world.multiworld.itempool += filler_bottle_items
    world.item_pool += filler_bottle_items


def create_triforce_pieces(world: "SohWorld") -> None:
    total_triforce_pieces: int = min(
        get_open_location_count(world), world.options.triforce_hunt_pieces_total.value)

    triforce_pieces_made = [world.create_item(
        Items.TRIFORCE_PIECE) for _ in range(total_triforce_pieces)]
    world.item_pool += triforce_pieces_made
    world.multiworld.itempool += triforce_pieces_made

    triforce_pieces_to_win: int = max(1, round(
        total_triforce_pieces * (world.options.triforce_hunt_pieces_required_percentage.value * .01)))

    world.options.triforce_hunt_pieces_total.value = total_triforce_pieces
    world.triforce_pieces_required = triforce_pieces_to_win

    if world.using_ut:
        world.triforce_pieces_required = world.passthrough["triforce_hunt_pieces_required"]


def create_filler_item_pool(world: "SohWorld") -> None:
    filler_item_count = get_open_location_count(world)

    # Ice Trap Count
    ice_trap_count = min(filler_item_count, world.options.ice_trap_count.value)
    world.multiworld.itempool += [world.create_item(
        Items.ICE_TRAP) for _ in range(ice_trap_count)]

    filler_item_count -= ice_trap_count

    # Ice Trap Filler Replacement
    ice_traps_to_place: int = int(
        filler_item_count * (world.options.ice_trap_filler_replacement.value * .01))
    world.multiworld.itempool += [world.create_item(
        Items.ICE_TRAP) for _ in range(ice_traps_to_place)]

    filler_item_count -= ice_traps_to_place

    # Add junk items to fill remaining locations
    world.multiworld.itempool += [world.create_item(
        get_filler_item(world)) for _ in range(filler_item_count)]


def get_open_location_count(world: "SohWorld") -> int:
    open_location_count = len(world.multiworld.get_unfilled_locations(
        world.player)) - len(world.item_pool)
    # Subtract vanilla shop items because they're prefilled later.
    if world.options.shuffle_shops:
        open_location_count -= (64 -
                                (8 * world.options.shuffle_shops_item_amount))
    else:
        open_location_count -= 64
    # Subtract dungeon rewards when set to dungeons as they're prefilled later.
    if world.options.shuffle_dungeon_rewards == "dungeons":
        open_location_count -= 9
    return open_location_count


def get_filler_item(world: "SohWorld") -> str:
    return world.random.choice(filler_items)


def get_filler_bottle(world: "SohWorld") -> str:
    return world.random.choice(filler_bottles)
