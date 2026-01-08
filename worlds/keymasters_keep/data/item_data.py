from typing import Dict, NamedTuple, Optional, Tuple

from BaseClasses import ItemClassification

from ..enums import KeymastersKeepItems, KeymastersKeepTags


class KeymastersKeepItemData(NamedTuple):
    archipelago_id: Optional[int]
    classification: ItemClassification
    tags: Tuple[KeymastersKeepTags, ...]
    maximum_quantity: Optional[int] = 1


item_data: Dict[KeymastersKeepItems, KeymastersKeepItemData] = {
    # Keys
    KeymastersKeepItems.KEY_AMBER_INFERNO: KeymastersKeepItemData(
        archipelago_id=100,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_AMBER_STONE: KeymastersKeepItemData(
        archipelago_id=1,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_ASHEN_SPARK: KeymastersKeepItemData(
        archipelago_id=2,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_AURIC_FLASH: KeymastersKeepItemData(
        archipelago_id=3,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_AURORA_BEAM: KeymastersKeepItemData(
        archipelago_id=4,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_AZURE_TIDE: KeymastersKeepItemData(
        archipelago_id=5,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_BRONZE_ROOT: KeymastersKeepItemData(
        archipelago_id=6,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_CELESTIAL_STAR: KeymastersKeepItemData(
        archipelago_id=7,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_CERULEAN_RIPPLE: KeymastersKeepItemData(
        archipelago_id=8,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_COBALT_SKY: KeymastersKeepItemData(
        archipelago_id=9,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_COPPER_BLOOM: KeymastersKeepItemData(
        archipelago_id=10,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_CRIMSON_BLAZE: KeymastersKeepItemData(
        archipelago_id=11,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_CRYSTAL_GLACIER: KeymastersKeepItemData(
        archipelago_id=12,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_DUSKLIGHT_VEIL: KeymastersKeepItemData(
        archipelago_id=13,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_EBONY_OAK: KeymastersKeepItemData(
        archipelago_id=14,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_ELECTRIC_STORM: KeymastersKeepItemData(
        archipelago_id=15,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_EMERALD_GROVE: KeymastersKeepItemData(
        archipelago_id=16,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_FROSTBITE: KeymastersKeepItemData(
        archipelago_id=17,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_FROZEN_TWILIGHT: KeymastersKeepItemData(
        archipelago_id=18,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_GLACIAL_SHARD: KeymastersKeepItemData(
        archipelago_id=19,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_GOLDEN_BIRCH: KeymastersKeepItemData(
        archipelago_id=20,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_GOLDEN_FLAME: KeymastersKeepItemData(
        archipelago_id=21,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_GOLDEN_ZEPHYR: KeymastersKeepItemData(
        archipelago_id=22,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_HALO_FLAME: KeymastersKeepItemData(
        archipelago_id=23,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_ICY_CASCADE: KeymastersKeepItemData(
        archipelago_id=24,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_IRONCLAD: KeymastersKeepItemData(
        archipelago_id=25,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_IVORY_DRIFT: KeymastersKeepItemData(
        archipelago_id=26,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_IVORY_SPROUT: KeymastersKeepItemData(
        archipelago_id=27,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_MAHOGANY_BARK: KeymastersKeepItemData(
        archipelago_id=28,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_MIDNIGHT_ABYSS: KeymastersKeepItemData(
        archipelago_id=29,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_MIDNIGHT_SHADE: KeymastersKeepItemData(
        archipelago_id=30,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_OBSIDIAN_CORE: KeymastersKeepItemData(
        archipelago_id=31,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_OBSIDIAN_WRAITH: KeymastersKeepItemData(
        archipelago_id=32,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_ONYX_ECLIPSE: KeymastersKeepItemData(
        archipelago_id=33,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_PALE_GALE: KeymastersKeepItemData(
        archipelago_id=34,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_PEARLESCENT_GLOW: KeymastersKeepItemData(
        archipelago_id=35,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_PLASMA_SURGE: KeymastersKeepItemData(
        archipelago_id=36,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_PLATINUM_FORGE: KeymastersKeepItemData(
        archipelago_id=37,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_RADIANT_DAWN: KeymastersKeepItemData(
        archipelago_id=38,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_RUSTSTONE: KeymastersKeepItemData(
        archipelago_id=39,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_SAPPHIRE_SURGE: KeymastersKeepItemData(
        archipelago_id=40,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_SCARLET_EMBER: KeymastersKeepItemData(
        archipelago_id=41,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_SILVER_BREEZE: KeymastersKeepItemData(
        archipelago_id=42,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_SILVER_SHIELD: KeymastersKeepItemData(
        archipelago_id=43,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_SNOWDRIFT: KeymastersKeepItemData(
        archipelago_id=44,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_STORMCALL: KeymastersKeepItemData(
        archipelago_id=45,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_STORMCLOUD: KeymastersKeepItemData(
        archipelago_id=46,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_VERDANT_MOSS: KeymastersKeepItemData(
        archipelago_id=47,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_VERDANT_TIMBER: KeymastersKeepItemData(
        archipelago_id=48,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    KeymastersKeepItems.KEY_VOID_EMBER: KeymastersKeepItemData(
        archipelago_id=49,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.KEYS,),
    ),
    # Door Unlocks
    KeymastersKeepItems.UNLOCK_THE_ARCANE_DOOR: KeymastersKeepItemData(
        archipelago_id=1000 + 0,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_ARCANE_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 1,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_ARCANE_THRESHOLD: KeymastersKeepItemData(
        archipelago_id=1000 + 2,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_CLANDESTINE_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 3,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_CLOAKED_ENTRANCE: KeymastersKeepItemData(
        archipelago_id=1000 + 4,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_CLOAKED_THRESHOLD: KeymastersKeepItemData(
        archipelago_id=1000 + 5,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_CLOAKED_VAULT: KeymastersKeepItemData(
        archipelago_id=1000 + 6,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_CONCEALED_THRESHOLD: KeymastersKeepItemData(
        archipelago_id=1000 + 7,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_CONCEALED_VAULT: KeymastersKeepItemData(
        archipelago_id=1000 + 8,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_CRYPTIC_CHAMBER: KeymastersKeepItemData(
        archipelago_id=1000 + 9,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_CRYPTIC_GATEWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 10,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_CRYPTIC_VAULT: KeymastersKeepItemData(
        archipelago_id=1000 + 11,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_DISGUISED_GATEWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 12,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_ECHOING_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 13,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_ELUSIVE_DOOR: KeymastersKeepItemData(
        archipelago_id=1000 + 14,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_ENCHANTED_GATEWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 15,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_ENCHANTED_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 16,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_ENIGMATIC_PORTAL: KeymastersKeepItemData(
        archipelago_id=1000 + 17,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_ENIGMATIC_THRESHOLD: KeymastersKeepItemData(
        archipelago_id=1000 + 18,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_FADED_GATEWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 19,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_FAINT_DOORWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 20,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_FAINT_PATH: KeymastersKeepItemData(
        archipelago_id=1000 + 21,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_FAINT_THRESHOLD: KeymastersKeepItemData(
        archipelago_id=1000 + 22,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_FORBIDDEN_ENTRANCE: KeymastersKeepItemData(
        archipelago_id=1000 + 23,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_FORGOTTEN_DOOR: KeymastersKeepItemData(
        archipelago_id=1000 + 24,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_FORGOTTEN_GATEWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 25,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_FORGOTTEN_PORTAL: KeymastersKeepItemData(
        archipelago_id=1000 + 26,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_FORGOTTEN_THRESHOLD: KeymastersKeepItemData(
        archipelago_id=1000 + 27,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_GHOSTED_PASSAGEWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 28,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_GHOSTLY_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 29,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_HIDDEN_ARCHWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 30,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_HIDDEN_CHAMBER: KeymastersKeepItemData(
        archipelago_id=1000 + 31,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_HIDDEN_DOORWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 32,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_HIDDEN_ENTRANCE: KeymastersKeepItemData(
        archipelago_id=1000 + 33,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_HIDDEN_KEYHOLE: KeymastersKeepItemData(
        archipelago_id=1000 + 34,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_HIDDEN_PASSAGEWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 35,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_HIDDEN_PATH: KeymastersKeepItemData(
        archipelago_id=1000 + 36,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_HIDDEN_REACH: KeymastersKeepItemData(
        archipelago_id=1000 + 37,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_HIDDEN_VAULT: KeymastersKeepItemData(
        archipelago_id=1000 + 38,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_INCONSPICUOUS_DOOR: KeymastersKeepItemData(
        archipelago_id=1000 + 39,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_INVISIBLE_DOORWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 40,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_KEYMASTERS_CHALLENGE_CHAMBER: KeymastersKeepItemData(
        archipelago_id=1000 + 41,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_LOCKED_DOORWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 42,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_LOCKED_GATEWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 43,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_LOST_ARCHWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 44,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_LOST_PORTAL: KeymastersKeepItemData(
        archipelago_id=1000 + 45,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_LOST_THRESHOLD: KeymastersKeepItemData(
        archipelago_id=1000 + 46,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_MYSTERIOUS_ARCH: KeymastersKeepItemData(
        archipelago_id=1000 + 47,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_MYSTERIOUS_DOORWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 48,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_MYSTERIOUS_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 49,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_MYSTERIOUS_VAULT: KeymastersKeepItemData(
        archipelago_id=1000 + 50,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_MYSTICAL_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 51,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_OBSCURED_ARCH: KeymastersKeepItemData(
        archipelago_id=1000 + 52,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_OBSCURED_DOORWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 53,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_OBSCURED_PORTAL: KeymastersKeepItemData(
        archipelago_id=1000 + 54,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_OBSCURED_VAULT: KeymastersKeepItemData(
        archipelago_id=1000 + 55,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_OBSCURE_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 56,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_PHANTOM_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 57,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_PHANTOM_VAULT: KeymastersKeepItemData(
        archipelago_id=1000 + 58,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_QUIET_ARCHWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 59,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_QUIET_THRESHOLD: KeymastersKeepItemData(
        archipelago_id=1000 + 60,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SEALED_CHAMBER: KeymastersKeepItemData(
        archipelago_id=1000 + 61,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SEALED_GATEWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 62,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SEALED_THRESHOLD: KeymastersKeepItemData(
        archipelago_id=1000 + 63,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SECRETED_DOOR: KeymastersKeepItemData(
        archipelago_id=1000 + 64,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SECRETIVE_DOOR: KeymastersKeepItemData(
        archipelago_id=1000 + 65,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SECRET_ARCHWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 66,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SECRET_PASSAGEWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 67,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SECRET_THRESHOLD: KeymastersKeepItemData(
        archipelago_id=1000 + 68,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SECRET_VAULT: KeymastersKeepItemData(
        archipelago_id=1000 + 69,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SHADOWED_PORTAL: KeymastersKeepItemData(
        archipelago_id=1000 + 70,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SHADOWED_THRESHOLD: KeymastersKeepItemData(
        archipelago_id=1000 + 71,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SHADOWY_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 72,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SHIMMERING_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 73,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SHROUDED_GATEWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 74,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SHROUDED_PORTAL: KeymastersKeepItemData(
        archipelago_id=1000 + 75,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SILENT_ARCHWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 76,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SILENT_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 77,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SILENT_THRESHOLD: KeymastersKeepItemData(
        archipelago_id=1000 + 78,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_SILENT_VAULT: KeymastersKeepItemData(
        archipelago_id=1000 + 79,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_UNFATHOMABLE_DOOR: KeymastersKeepItemData(
        archipelago_id=1000 + 80,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_UNKNOWN_ARCH: KeymastersKeepItemData(
        archipelago_id=1000 + 81,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_UNKNOWN_GATEWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 82,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_UNMARKED_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 83,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_UNMARKED_VAULT: KeymastersKeepItemData(
        archipelago_id=1000 + 84,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_UNRAVELED_DOOR: KeymastersKeepItemData(
        archipelago_id=1000 + 85,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_UNSEEN_ARCHWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 86,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_UNSEEN_DOOR: KeymastersKeepItemData(
        archipelago_id=1000 + 87,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_UNSEEN_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 88,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_UNSEEN_PORTAL: KeymastersKeepItemData(
        archipelago_id=1000 + 89,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_UNSPOKEN_GATE: KeymastersKeepItemData(
        archipelago_id=1000 + 90,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_UNTOLD_GATEWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 91,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_UNTRACEABLE_PATH: KeymastersKeepItemData(
        archipelago_id=1000 + 92,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_VANISHING_ARCHWAY: KeymastersKeepItemData(
        archipelago_id=1000 + 93,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_VANISHING_DOOR: KeymastersKeepItemData(
        archipelago_id=1000 + 94,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_VAULT_OF_WHISPERS: KeymastersKeepItemData(
        archipelago_id=1000 + 95,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_VEILED_PASSAGE: KeymastersKeepItemData(
        archipelago_id=1000 + 96,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_VEILED_PATH: KeymastersKeepItemData(
        archipelago_id=1000 + 97,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_WHISPERED_PORTAL: KeymastersKeepItemData(
        archipelago_id=1000 + 98,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_WHISPERED_THRESHOLD: KeymastersKeepItemData(
        archipelago_id=1000 + 99,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepItems.UNLOCK_THE_WHISPERING_DOOR: KeymastersKeepItemData(
        archipelago_id=1000 + 100,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    # Filler
    KeymastersKeepItems.FILLER_KEY_BROKEN: KeymastersKeepItemData(
        archipelago_id=2000 + 0,
        classification=ItemClassification.filler,
        tags=(KeymastersKeepTags.FILLER,),
        maximum_quantity=None,
    ),
    KeymastersKeepItems.FILLER_KEY_CRACKED: KeymastersKeepItemData(
        archipelago_id=2000 + 1,
        classification=ItemClassification.filler,
        tags=(KeymastersKeepTags.FILLER,),
        maximum_quantity=None,
    ),
    KeymastersKeepItems.FILLER_KEY_DULL: KeymastersKeepItemData(
        archipelago_id=2000 + 2,
        classification=ItemClassification.filler,
        tags=(KeymastersKeepTags.FILLER,),
        maximum_quantity=None,
    ),
    KeymastersKeepItems.FILLER_KEY_USELESS: KeymastersKeepItemData(
        archipelago_id=2000 + 3,
        classification=ItemClassification.filler,
        tags=(KeymastersKeepTags.FILLER,),
        maximum_quantity=None,
    ),
    KeymastersKeepItems.FILLER_KEY_WORN: KeymastersKeepItemData(
        archipelago_id=2000 + 4,
        classification=ItemClassification.filler,
        tags=(KeymastersKeepTags.FILLER,),
        maximum_quantity=None,
    ),
    # Goal Items
    KeymastersKeepItems.ARTIFACT_OF_RESOLVE: KeymastersKeepItemData(
        archipelago_id=3000 + 0,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.GOAL,),
    ),
    KeymastersKeepItems.KEYMASTERS_KEEP_CHALLENGE_COMPLETE: KeymastersKeepItemData(
        archipelago_id=3000 + 1,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.GOAL,),
    ),
    # Relics
    KeymastersKeepItems.RELIC_ABYSSAL_KNOT: KeymastersKeepItemData(
        archipelago_id=4000 + 0,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_ASHVINE_RING: KeymastersKeepItemData(
        archipelago_id=4000 + 1,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_ASTRALGLEN_SPRIG: KeymastersKeepItemData(
        archipelago_id=4000 + 2,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_BLOODROOT_BULB: KeymastersKeepItemData(
        archipelago_id=4000 + 3,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_BOGMIRE_AMBER: KeymastersKeepItemData(
        archipelago_id=4000 + 4,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_CELESTINE_STRAND: KeymastersKeepItemData(
        archipelago_id=4000 + 5,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_CINDER_OF_THE_LOST: KeymastersKeepItemData(
        archipelago_id=4000 + 6,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_CORALHEART_FRAGMENT: KeymastersKeepItemData(
        archipelago_id=4000 + 7,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_DUSKWIND_FEATHER: KeymastersKeepItemData(
        archipelago_id=4000 + 8,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_ECHOIRON_NAIL: KeymastersKeepItemData(
        archipelago_id=4000 + 9,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_EMBERGLOW_PELLET: KeymastersKeepItemData(
        archipelago_id=4000 + 10,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_FOGSEED_CAPSULE: KeymastersKeepItemData(
        archipelago_id=4000 + 11,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_FROSTWREATH_SHARD: KeymastersKeepItemData(
        archipelago_id=4000 + 12,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_GALECHIME_WHISTLE: KeymastersKeepItemData(
        archipelago_id=4000 + 13,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_GLASSWING_BROOCH: KeymastersKeepItemData(
        archipelago_id=4000 + 14,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_GLIMMERCOIL_SPRING: KeymastersKeepItemData(
        archipelago_id=4000 + 15,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_GLOOMVINE_TENDRIL: KeymastersKeepItemData(
        archipelago_id=4000 + 16,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_HEARTWOOD_CHIP: KeymastersKeepItemData(
        archipelago_id=4000 + 17,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_HOURGLASS_OF_SHIFTING: KeymastersKeepItemData(
        archipelago_id=4000 + 18,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_INK_OF_FORGOTTEN_RITES: KeymastersKeepItemData(
        archipelago_id=4000 + 19,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_IRONROOT_SEED: KeymastersKeepItemData(
        archipelago_id=4000 + 20,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_LUMINWEAVE_RIBBON: KeymastersKeepItemData(
        archipelago_id=4000 + 21,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_MAELSTROM_SHARD: KeymastersKeepItemData(
        archipelago_id=4000 + 22,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_MIRROR_OF_WHISPERS: KeymastersKeepItemData(
        archipelago_id=4000 + 23,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_MISTBOUND_LANTERN: KeymastersKeepItemData(
        archipelago_id=4000 + 24,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_MORROWMIST_DEWDROP: KeymastersKeepItemData(
        archipelago_id=4000 + 25,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_NIGHTBLOOM_PETAL: KeymastersKeepItemData(
        archipelago_id=4000 + 26,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_NIGHTCROWN_CIRCLET: KeymastersKeepItemData(
        archipelago_id=4000 + 27,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_PATHFINDERS_SUNDIAL: KeymastersKeepItemData(
        archipelago_id=4000 + 28,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_PHOENIX_LAMENT_SCALE: KeymastersKeepItemData(
        archipelago_id=4000 + 29,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_QUARTZ_OF_MEMORYS_EDGE: KeymastersKeepItemData(
        archipelago_id=4000 + 30,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_RESONANT_BONE_FLUTE: KeymastersKeepItemData(
        archipelago_id=4000 + 31,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_RUNE_OF_SILENT_OATHS: KeymastersKeepItemData(
        archipelago_id=4000 + 32,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_SABLE_QUARTZ_BEAD: KeymastersKeepItemData(
        archipelago_id=4000 + 33,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_SANDS_OF_UNMAKING: KeymastersKeepItemData(
        archipelago_id=4000 + 34,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_SCALE_OF_THE_SKYBORN: KeymastersKeepItemData(
        archipelago_id=4000 + 35,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_SIGIL_OF_BROKEN_CHAINS: KeymastersKeepItemData(
        archipelago_id=4000 + 36,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_SIRENS_TEAR: KeymastersKeepItemData(
        archipelago_id=4000 + 37,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_SOUL_PRISM: KeymastersKeepItemData(
        archipelago_id=4000 + 38,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_STARMARK_LENS: KeymastersKeepItemData(
        archipelago_id=4000 + 39,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_STORMSHACKLE_CHAIN: KeymastersKeepItemData(
        archipelago_id=4000 + 40,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_TEMPESTS_HEART: KeymastersKeepItemData(
        archipelago_id=4000 + 41,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_THORNMARROW_SPIKE: KeymastersKeepItemData(
        archipelago_id=4000 + 42,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_THUNDERRIFT_SHARD: KeymastersKeepItemData(
        archipelago_id=4000 + 43,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_VEIN_OF_NIGHTFIRE: KeymastersKeepItemData(
        archipelago_id=4000 + 44,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_VEINSTONE_OF_ECHOING_LAMENT: KeymastersKeepItemData(
        archipelago_id=4000 + 45,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_VOIDECHO_SPHERE: KeymastersKeepItemData(
        archipelago_id=4000 + 46,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_VORTEX_PRISM: KeymastersKeepItemData(
        archipelago_id=4000 + 47,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_WISP_OF_THE_WEEPING_WILLOW: KeymastersKeepItemData(
        archipelago_id=4000 + 48,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
    KeymastersKeepItems.RELIC_WYRMCOIL_RING: KeymastersKeepItemData(
        archipelago_id=4000 + 49,
        classification=ItemClassification.progression,
        tags=(KeymastersKeepTags.RELICS,),
    ),
}
