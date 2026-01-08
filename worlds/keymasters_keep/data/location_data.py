from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Union

from ..enums import (
    KeymastersKeepLocations,
    KeymastersKeepRegions,
    KeymastersKeepTags,
    KeymastersKeepTrials,
)


class KeymastersKeepLocationData(NamedTuple):
    name: str
    archipelago_id: Optional[int]
    region: KeymastersKeepRegions
    tags: Optional[Tuple[KeymastersKeepTags, ...]] = None


location_data: Dict[
    KeymastersKeepLocations,
    Union[KeymastersKeepLocationData, List[KeymastersKeepLocationData]],
] = {
    # Door Unlocks
    KeymastersKeepLocations.THE_ARCANE_DOOR_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_ARCANE_DOOR_UNLOCK.value,
        archipelago_id=201,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_ARCANE_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_ARCANE_PASSAGE_UNLOCK.value,
        archipelago_id=1,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_ARCANE_THRESHOLD_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_ARCANE_THRESHOLD_UNLOCK.value,
        archipelago_id=2,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_CLANDESTINE_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_CLANDESTINE_PASSAGE_UNLOCK.value,
        archipelago_id=3,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_CLOAKED_ENTRANCE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_CLOAKED_ENTRANCE_UNLOCK.value,
        archipelago_id=4,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_CLOAKED_THRESHOLD_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_CLOAKED_THRESHOLD_UNLOCK.value,
        archipelago_id=5,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_CLOAKED_VAULT_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_CLOAKED_VAULT_UNLOCK.value,
        archipelago_id=6,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_CONCEALED_THRESHOLD_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_CONCEALED_THRESHOLD_UNLOCK.value,
        archipelago_id=7,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_CONCEALED_VAULT_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_CONCEALED_VAULT_UNLOCK.value,
        archipelago_id=8,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_CRYPTIC_CHAMBER_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_CRYPTIC_CHAMBER_UNLOCK.value,
        archipelago_id=9,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_CRYPTIC_GATEWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_CRYPTIC_GATEWAY_UNLOCK.value,
        archipelago_id=10,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_CRYPTIC_VAULT_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_CRYPTIC_VAULT_UNLOCK.value,
        archipelago_id=11,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_DISGUISED_GATEWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_DISGUISED_GATEWAY_UNLOCK.value,
        archipelago_id=12,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_ECHOING_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_ECHOING_PASSAGE_UNLOCK.value,
        archipelago_id=13,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_ELUSIVE_DOOR_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_ELUSIVE_DOOR_UNLOCK.value,
        archipelago_id=14,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_ENCHANTED_GATEWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_ENCHANTED_GATEWAY_UNLOCK.value,
        archipelago_id=15,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_ENCHANTED_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_ENCHANTED_PASSAGE_UNLOCK.value,
        archipelago_id=16,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_ENIGMATIC_PORTAL_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_ENIGMATIC_PORTAL_UNLOCK.value,
        archipelago_id=17,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_ENIGMATIC_THRESHOLD_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_ENIGMATIC_THRESHOLD_UNLOCK.value,
        archipelago_id=18,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_FADED_GATEWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_FADED_GATEWAY_UNLOCK.value,
        archipelago_id=19,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_FAINT_DOORWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_FAINT_DOORWAY_UNLOCK.value,
        archipelago_id=20,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_FAINT_PATH_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_FAINT_PATH_UNLOCK.value,
        archipelago_id=21,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_FAINT_THRESHOLD_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_FAINT_THRESHOLD_UNLOCK.value,
        archipelago_id=22,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_FORBIDDEN_ENTRANCE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_FORBIDDEN_ENTRANCE_UNLOCK.value,
        archipelago_id=23,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_FORGOTTEN_DOOR_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_FORGOTTEN_DOOR_UNLOCK.value,
        archipelago_id=24,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_FORGOTTEN_GATEWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_FORGOTTEN_GATEWAY_UNLOCK.value,
        archipelago_id=25,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_FORGOTTEN_PORTAL_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_FORGOTTEN_PORTAL_UNLOCK.value,
        archipelago_id=26,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_FORGOTTEN_THRESHOLD_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_FORGOTTEN_THRESHOLD_UNLOCK.value,
        archipelago_id=27,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_GHOSTED_PASSAGEWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_GHOSTED_PASSAGEWAY_UNLOCK.value,
        archipelago_id=28,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_GHOSTLY_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_GHOSTLY_PASSAGE_UNLOCK.value,
        archipelago_id=29,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_HIDDEN_ARCHWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_HIDDEN_ARCHWAY_UNLOCK.value,
        archipelago_id=30,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_HIDDEN_CHAMBER_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_HIDDEN_CHAMBER_UNLOCK.value,
        archipelago_id=31,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_HIDDEN_DOORWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_HIDDEN_DOORWAY_UNLOCK.value,
        archipelago_id=32,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_HIDDEN_ENTRANCE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_HIDDEN_ENTRANCE_UNLOCK.value,
        archipelago_id=33,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_HIDDEN_KEYHOLE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_HIDDEN_KEYHOLE_UNLOCK.value,
        archipelago_id=34,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_HIDDEN_PASSAGEWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_HIDDEN_PASSAGEWAY_UNLOCK.value,
        archipelago_id=35,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_HIDDEN_PATH_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_HIDDEN_PATH_UNLOCK.value,
        archipelago_id=36,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_HIDDEN_REACH_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_HIDDEN_REACH_UNLOCK.value,
        archipelago_id=37,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_HIDDEN_VAULT_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_HIDDEN_VAULT_UNLOCK.value,
        archipelago_id=38,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_INCONSPICUOUS_DOOR_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_INCONSPICUOUS_DOOR_UNLOCK.value,
        archipelago_id=39,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_INVISIBLE_DOORWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_INVISIBLE_DOORWAY_UNLOCK.value,
        archipelago_id=40,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_KEYMASTERS_CHALLENGE_CHAMBER_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_KEYMASTERS_CHALLENGE_CHAMBER_UNLOCK.value,
        archipelago_id=41,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_LOCKED_DOORWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_LOCKED_DOORWAY_UNLOCK.value,
        archipelago_id=42,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_LOCKED_GATEWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_LOCKED_GATEWAY_UNLOCK.value,
        archipelago_id=43,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_LOST_ARCHWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_LOST_ARCHWAY_UNLOCK.value,
        archipelago_id=44,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_LOST_PORTAL_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_LOST_PORTAL_UNLOCK.value,
        archipelago_id=45,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_LOST_THRESHOLD_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_LOST_THRESHOLD_UNLOCK.value,
        archipelago_id=46,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_MYSTERIOUS_ARCH_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_MYSTERIOUS_ARCH_UNLOCK.value,
        archipelago_id=47,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_MYSTERIOUS_DOORWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_MYSTERIOUS_DOORWAY_UNLOCK.value,
        archipelago_id=48,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_MYSTERIOUS_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_MYSTERIOUS_PASSAGE_UNLOCK.value,
        archipelago_id=49,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_MYSTERIOUS_VAULT_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_MYSTERIOUS_VAULT_UNLOCK.value,
        archipelago_id=50,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_MYSTICAL_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_MYSTICAL_PASSAGE_UNLOCK.value,
        archipelago_id=51,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_OBSCURED_ARCH_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_OBSCURED_ARCH_UNLOCK.value,
        archipelago_id=52,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_OBSCURED_DOORWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_OBSCURED_DOORWAY_UNLOCK.value,
        archipelago_id=53,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_OBSCURED_PORTAL_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_OBSCURED_PORTAL_UNLOCK.value,
        archipelago_id=54,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_OBSCURED_VAULT_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_OBSCURED_VAULT_UNLOCK.value,
        archipelago_id=55,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_OBSCURE_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_OBSCURE_PASSAGE_UNLOCK.value,
        archipelago_id=56,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_PHANTOM_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_PHANTOM_PASSAGE_UNLOCK.value,
        archipelago_id=57,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_PHANTOM_VAULT_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_PHANTOM_VAULT_UNLOCK.value,
        archipelago_id=58,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_QUIET_ARCHWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_QUIET_ARCHWAY_UNLOCK.value,
        archipelago_id=59,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_QUIET_THRESHOLD_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_QUIET_THRESHOLD_UNLOCK.value,
        archipelago_id=60,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SEALED_CHAMBER_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SEALED_CHAMBER_UNLOCK.value,
        archipelago_id=61,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SEALED_GATEWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SEALED_GATEWAY_UNLOCK.value,
        archipelago_id=62,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SEALED_THRESHOLD_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SEALED_THRESHOLD_UNLOCK.value,
        archipelago_id=63,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SECRETED_DOOR_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SECRETED_DOOR_UNLOCK.value,
        archipelago_id=64,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SECRETIVE_DOOR_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SECRETIVE_DOOR_UNLOCK.value,
        archipelago_id=65,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SECRET_ARCHWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SECRET_ARCHWAY_UNLOCK.value,
        archipelago_id=66,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SECRET_PASSAGEWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SECRET_PASSAGEWAY_UNLOCK.value,
        archipelago_id=67,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SECRET_THRESHOLD_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SECRET_THRESHOLD_UNLOCK.value,
        archipelago_id=68,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SECRET_VAULT_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SECRET_VAULT_UNLOCK.value,
        archipelago_id=69,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SHADOWED_PORTAL_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SHADOWED_PORTAL_UNLOCK.value,
        archipelago_id=70,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SHADOWED_THRESHOLD_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SHADOWED_THRESHOLD_UNLOCK.value,
        archipelago_id=71,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SHADOWY_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SHADOWY_PASSAGE_UNLOCK.value,
        archipelago_id=72,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SHIMMERING_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SHIMMERING_PASSAGE_UNLOCK.value,
        archipelago_id=73,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SHROUDED_GATEWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SHROUDED_GATEWAY_UNLOCK.value,
        archipelago_id=74,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SHROUDED_PORTAL_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SHROUDED_PORTAL_UNLOCK.value,
        archipelago_id=75,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SILENT_ARCHWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SILENT_ARCHWAY_UNLOCK.value,
        archipelago_id=76,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SILENT_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SILENT_PASSAGE_UNLOCK.value,
        archipelago_id=77,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SILENT_THRESHOLD_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SILENT_THRESHOLD_UNLOCK.value,
        archipelago_id=78,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_SILENT_VAULT_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_SILENT_VAULT_UNLOCK.value,
        archipelago_id=79,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_UNFATHOMABLE_DOOR_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_UNFATHOMABLE_DOOR_UNLOCK.value,
        archipelago_id=80,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_UNKNOWN_ARCH_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_UNKNOWN_ARCH_UNLOCK.value,
        archipelago_id=81,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_UNKNOWN_GATEWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_UNKNOWN_GATEWAY_UNLOCK.value,
        archipelago_id=82,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_UNMARKED_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_UNMARKED_PASSAGE_UNLOCK.value,
        archipelago_id=83,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_UNMARKED_VAULT_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_UNMARKED_VAULT_UNLOCK.value,
        archipelago_id=84,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_UNRAVELED_DOOR_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_UNRAVELED_DOOR_UNLOCK.value,
        archipelago_id=85,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_UNSEEN_ARCHWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_UNSEEN_ARCHWAY_UNLOCK.value,
        archipelago_id=86,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_UNSEEN_DOOR_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_UNSEEN_DOOR_UNLOCK.value,
        archipelago_id=87,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_UNSEEN_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_UNSEEN_PASSAGE_UNLOCK.value,
        archipelago_id=88,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_UNSEEN_PORTAL_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_UNSEEN_PORTAL_UNLOCK.value,
        archipelago_id=89,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_UNSPOKEN_GATE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_UNSPOKEN_GATE_UNLOCK.value,
        archipelago_id=90,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_UNTOLD_GATEWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_UNTOLD_GATEWAY_UNLOCK.value,
        archipelago_id=91,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_UNTRACEABLE_PATH_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_UNTRACEABLE_PATH_UNLOCK.value,
        archipelago_id=92,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_VANISHING_ARCHWAY_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_VANISHING_ARCHWAY_UNLOCK.value,
        archipelago_id=93,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_VANISHING_DOOR_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_VANISHING_DOOR_UNLOCK.value,
        archipelago_id=94,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_VAULT_OF_WHISPERS_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_VAULT_OF_WHISPERS_UNLOCK.value,
        archipelago_id=95,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_VEILED_PASSAGE_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_VEILED_PASSAGE_UNLOCK.value,
        archipelago_id=96,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_VEILED_PATH_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_VEILED_PATH_UNLOCK.value,
        archipelago_id=97,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_WHISPERED_PORTAL_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_WHISPERED_PORTAL_UNLOCK.value,
        archipelago_id=98,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_WHISPERED_THRESHOLD_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_WHISPERED_THRESHOLD_UNLOCK.value,
        archipelago_id=99,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
    KeymastersKeepLocations.THE_WHISPERING_DOOR_UNLOCK: KeymastersKeepLocationData(
        name=KeymastersKeepLocations.THE_WHISPERING_DOOR_UNLOCK.value,
        archipelago_id=100,
        region=KeymastersKeepRegions.KEYMASTERS_KEEP,
        tags=(KeymastersKeepTags.DOOR_UNLOCKS,),
    ),
}

# Trials
trials: List[Any] = sorted([trial.value for trial in KeymastersKeepTrials])
trial_count: int = len(trials)

location_data[KeymastersKeepLocations.THE_ARCANE_DOOR_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_ARCANE_DOOR_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_ARCANE_DOOR_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=1000 + i,
            region=KeymastersKeepRegions.THE_ARCANE_DOOR,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_ARCANE_DOOR),
        )
    )

location_data[KeymastersKeepLocations.THE_ARCANE_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_ARCANE_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_ARCANE_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=1100 + i,
            region=KeymastersKeepRegions.THE_ARCANE_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_ARCANE_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_ARCANE_THRESHOLD_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_ARCANE_THRESHOLD_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_ARCANE_THRESHOLD_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=1200 + i,
            region=KeymastersKeepRegions.THE_ARCANE_THRESHOLD,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_ARCANE_THRESHOLD),
        )
    )

location_data[KeymastersKeepLocations.THE_CLANDESTINE_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_CLANDESTINE_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_CLANDESTINE_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=1300 + i,
            region=KeymastersKeepRegions.THE_CLANDESTINE_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_CLANDESTINE_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_CLOAKED_ENTRANCE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_CLOAKED_ENTRANCE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_CLOAKED_ENTRANCE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=1400 + i,
            region=KeymastersKeepRegions.THE_CLOAKED_ENTRANCE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_CLOAKED_ENTRANCE),
        )
    )

location_data[KeymastersKeepLocations.THE_CLOAKED_THRESHOLD_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_CLOAKED_THRESHOLD_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_CLOAKED_THRESHOLD_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=1500 + i,
            region=KeymastersKeepRegions.THE_CLOAKED_THRESHOLD,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_CLOAKED_THRESHOLD),
        )
    )

location_data[KeymastersKeepLocations.THE_CLOAKED_VAULT_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_CLOAKED_VAULT_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_CLOAKED_VAULT_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=1600 + i,
            region=KeymastersKeepRegions.THE_CLOAKED_VAULT,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_CLOAKED_VAULT),
        )
    )

location_data[KeymastersKeepLocations.THE_CONCEALED_THRESHOLD_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_CONCEALED_THRESHOLD_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_CONCEALED_THRESHOLD_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=1700 + i,
            region=KeymastersKeepRegions.THE_CONCEALED_THRESHOLD,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_CONCEALED_THRESHOLD),
        )
    )

location_data[KeymastersKeepLocations.THE_CONCEALED_VAULT_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_CONCEALED_VAULT_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_CONCEALED_VAULT_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=1800 + i,
            region=KeymastersKeepRegions.THE_CONCEALED_VAULT,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_CONCEALED_VAULT),
        )
    )

location_data[KeymastersKeepLocations.THE_CRYPTIC_CHAMBER_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_CRYPTIC_CHAMBER_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_CRYPTIC_CHAMBER_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=1900 + i,
            region=KeymastersKeepRegions.THE_CRYPTIC_CHAMBER,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_CRYPTIC_CHAMBER),
        )
    )

location_data[KeymastersKeepLocations.THE_CRYPTIC_GATEWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_CRYPTIC_GATEWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_CRYPTIC_GATEWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=2000 + i,
            region=KeymastersKeepRegions.THE_CRYPTIC_GATEWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_CRYPTIC_GATEWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_CRYPTIC_VAULT_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_CRYPTIC_VAULT_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_CRYPTIC_VAULT_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=2100 + i,
            region=KeymastersKeepRegions.THE_CRYPTIC_VAULT,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_CRYPTIC_VAULT),
        )
    )

location_data[KeymastersKeepLocations.THE_DISGUISED_GATEWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_DISGUISED_GATEWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_DISGUISED_GATEWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=2200 + i,
            region=KeymastersKeepRegions.THE_DISGUISED_GATEWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_DISGUISED_GATEWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_ECHOING_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_ECHOING_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_ECHOING_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=2300 + i,
            region=KeymastersKeepRegions.THE_ECHOING_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_ECHOING_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_ELUSIVE_DOOR_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_ELUSIVE_DOOR_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_ELUSIVE_DOOR_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=2400 + i,
            region=KeymastersKeepRegions.THE_ELUSIVE_DOOR,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_ELUSIVE_DOOR),
        )
    )

location_data[KeymastersKeepLocations.THE_ENCHANTED_GATEWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_ENCHANTED_GATEWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_ENCHANTED_GATEWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=2500 + i,
            region=KeymastersKeepRegions.THE_ENCHANTED_GATEWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_ENCHANTED_GATEWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_ENCHANTED_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_ENCHANTED_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_ENCHANTED_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=2600 + i,
            region=KeymastersKeepRegions.THE_ENCHANTED_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_ENCHANTED_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_ENIGMATIC_PORTAL_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_ENIGMATIC_PORTAL_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_ENIGMATIC_PORTAL_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=2700 + i,
            region=KeymastersKeepRegions.THE_ENIGMATIC_PORTAL,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_ENIGMATIC_PORTAL),
        )
    )

location_data[KeymastersKeepLocations.THE_ENIGMATIC_THRESHOLD_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_ENIGMATIC_THRESHOLD_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_ENIGMATIC_THRESHOLD_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=2800 + i,
            region=KeymastersKeepRegions.THE_ENIGMATIC_THRESHOLD,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_ENIGMATIC_THRESHOLD),
        )
    )

location_data[KeymastersKeepLocations.THE_FADED_GATEWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_FADED_GATEWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_FADED_GATEWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=2900 + i,
            region=KeymastersKeepRegions.THE_FADED_GATEWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_FADED_GATEWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_FAINT_DOORWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_FAINT_DOORWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_FAINT_DOORWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=3000 + i,
            region=KeymastersKeepRegions.THE_FAINT_DOORWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_FAINT_DOORWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_FAINT_PATH_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_FAINT_PATH_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_FAINT_PATH_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=3100 + i,
            region=KeymastersKeepRegions.THE_FAINT_PATH,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_FAINT_PATH),
        )
    )

location_data[KeymastersKeepLocations.THE_FAINT_THRESHOLD_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_FAINT_THRESHOLD_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_FAINT_THRESHOLD_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=3200 + i,
            region=KeymastersKeepRegions.THE_FAINT_THRESHOLD,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_FAINT_THRESHOLD),
        )
    )

location_data[KeymastersKeepLocations.THE_FORBIDDEN_ENTRANCE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_FORBIDDEN_ENTRANCE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_FORBIDDEN_ENTRANCE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=3300 + i,
            region=KeymastersKeepRegions.THE_FORBIDDEN_ENTRANCE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_FORBIDDEN_ENTRANCE),
        )
    )

location_data[KeymastersKeepLocations.THE_FORGOTTEN_DOOR_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_FORGOTTEN_DOOR_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_FORGOTTEN_DOOR_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=3400 + i,
            region=KeymastersKeepRegions.THE_FORGOTTEN_DOOR,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_FORGOTTEN_DOOR),
        )
    )

location_data[KeymastersKeepLocations.THE_FORGOTTEN_GATEWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_FORGOTTEN_GATEWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_FORGOTTEN_GATEWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=3500 + i,
            region=KeymastersKeepRegions.THE_FORGOTTEN_GATEWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_FORGOTTEN_GATEWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_FORGOTTEN_PORTAL_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_FORGOTTEN_PORTAL_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_FORGOTTEN_PORTAL_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=3600 + i,
            region=KeymastersKeepRegions.THE_FORGOTTEN_PORTAL,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_FORGOTTEN_PORTAL),
        )
    )

location_data[KeymastersKeepLocations.THE_FORGOTTEN_THRESHOLD_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_FORGOTTEN_THRESHOLD_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_FORGOTTEN_THRESHOLD_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=3700 + i,
            region=KeymastersKeepRegions.THE_FORGOTTEN_THRESHOLD,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_FORGOTTEN_THRESHOLD),
        )
    )

location_data[KeymastersKeepLocations.THE_GHOSTED_PASSAGEWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_GHOSTED_PASSAGEWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_GHOSTED_PASSAGEWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=3800 + i,
            region=KeymastersKeepRegions.THE_GHOSTED_PASSAGEWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_GHOSTED_PASSAGEWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_GHOSTLY_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_GHOSTLY_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_GHOSTLY_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=3900 + i,
            region=KeymastersKeepRegions.THE_GHOSTLY_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_GHOSTLY_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_HIDDEN_ARCHWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_HIDDEN_ARCHWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_HIDDEN_ARCHWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=4000 + i,
            region=KeymastersKeepRegions.THE_HIDDEN_ARCHWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_HIDDEN_ARCHWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_HIDDEN_CHAMBER_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_HIDDEN_CHAMBER_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_HIDDEN_CHAMBER_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=4100 + i,
            region=KeymastersKeepRegions.THE_HIDDEN_CHAMBER,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_HIDDEN_CHAMBER),
        )
    )

location_data[KeymastersKeepLocations.THE_HIDDEN_DOORWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_HIDDEN_DOORWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_HIDDEN_DOORWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=4200 + i,
            region=KeymastersKeepRegions.THE_HIDDEN_DOORWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_HIDDEN_DOORWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_HIDDEN_ENTRANCE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_HIDDEN_ENTRANCE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_HIDDEN_ENTRANCE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=4300 + i,
            region=KeymastersKeepRegions.THE_HIDDEN_ENTRANCE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_HIDDEN_ENTRANCE),
        )
    )

location_data[KeymastersKeepLocations.THE_HIDDEN_KEYHOLE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_HIDDEN_KEYHOLE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_HIDDEN_KEYHOLE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=4400 + i,
            region=KeymastersKeepRegions.THE_HIDDEN_KEYHOLE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_HIDDEN_KEYHOLE),
        )
    )

location_data[KeymastersKeepLocations.THE_HIDDEN_PASSAGEWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_HIDDEN_PASSAGEWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_HIDDEN_PASSAGEWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=4500 + i,
            region=KeymastersKeepRegions.THE_HIDDEN_PASSAGEWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_HIDDEN_PASSAGEWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_HIDDEN_PATH_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_HIDDEN_PATH_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_HIDDEN_PATH_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=4600 + i,
            region=KeymastersKeepRegions.THE_HIDDEN_PATH,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_HIDDEN_PATH),
        )
    )

location_data[KeymastersKeepLocations.THE_HIDDEN_REACH_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_HIDDEN_REACH_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_HIDDEN_REACH_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=4700 + i,
            region=KeymastersKeepRegions.THE_HIDDEN_REACH,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_HIDDEN_REACH),
        )
    )

location_data[KeymastersKeepLocations.THE_HIDDEN_VAULT_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_HIDDEN_VAULT_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_HIDDEN_VAULT_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=4800 + i,
            region=KeymastersKeepRegions.THE_HIDDEN_VAULT,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_HIDDEN_VAULT),
        )
    )

location_data[KeymastersKeepLocations.THE_INCONSPICUOUS_DOOR_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_INCONSPICUOUS_DOOR_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_INCONSPICUOUS_DOOR_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=4900 + i,
            region=KeymastersKeepRegions.THE_INCONSPICUOUS_DOOR,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_INCONSPICUOUS_DOOR),
        )
    )

location_data[KeymastersKeepLocations.THE_INVISIBLE_DOORWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_INVISIBLE_DOORWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_INVISIBLE_DOORWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=5000 + i,
            region=KeymastersKeepRegions.THE_INVISIBLE_DOORWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_INVISIBLE_DOORWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_KEYMASTERS_CHALLENGE_CHAMBER_VICTORY] = KeymastersKeepLocationData(
    name=KeymastersKeepLocations.THE_KEYMASTERS_CHALLENGE_CHAMBER_VICTORY.value,
    archipelago_id=999,
    region=KeymastersKeepRegions.THE_KEYMASTERS_CHALLENGE_CHAMBER,
    tags=(KeymastersKeepTags.TRIALS,),
)

location_data[KeymastersKeepLocations.THE_LOCKED_DOORWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_LOCKED_DOORWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_LOCKED_DOORWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=5100 + i,
            region=KeymastersKeepRegions.THE_LOCKED_DOORWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_LOCKED_DOORWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_LOCKED_GATEWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_LOCKED_GATEWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_LOCKED_GATEWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=5200 + i,
            region=KeymastersKeepRegions.THE_LOCKED_GATEWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_LOCKED_GATEWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_LOST_ARCHWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_LOST_ARCHWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_LOST_ARCHWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=5300 + i,
            region=KeymastersKeepRegions.THE_LOST_ARCHWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_LOST_ARCHWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_LOST_PORTAL_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_LOST_PORTAL_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_LOST_PORTAL_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=5400 + i,
            region=KeymastersKeepRegions.THE_LOST_PORTAL,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_LOST_PORTAL),
        )
    )

location_data[KeymastersKeepLocations.THE_LOST_THRESHOLD_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_LOST_THRESHOLD_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_LOST_THRESHOLD_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=5500 + i,
            region=KeymastersKeepRegions.THE_LOST_THRESHOLD,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_LOST_THRESHOLD),
        )
    )

location_data[KeymastersKeepLocations.THE_MYSTERIOUS_ARCH_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_MYSTERIOUS_ARCH_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_MYSTERIOUS_ARCH_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=5600 + i,
            region=KeymastersKeepRegions.THE_MYSTERIOUS_ARCH,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_MYSTERIOUS_ARCH),
        )
    )

location_data[KeymastersKeepLocations.THE_MYSTERIOUS_DOORWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_MYSTERIOUS_DOORWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_MYSTERIOUS_DOORWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=5700 + i,
            region=KeymastersKeepRegions.THE_MYSTERIOUS_DOORWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_MYSTERIOUS_DOORWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_MYSTERIOUS_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_MYSTERIOUS_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_MYSTERIOUS_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=5800 + i,
            region=KeymastersKeepRegions.THE_MYSTERIOUS_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_MYSTERIOUS_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_MYSTERIOUS_VAULT_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_MYSTERIOUS_VAULT_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_MYSTERIOUS_VAULT_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=5900 + i,
            region=KeymastersKeepRegions.THE_MYSTERIOUS_VAULT,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_MYSTERIOUS_VAULT),
        )
    )

location_data[KeymastersKeepLocations.THE_MYSTICAL_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_MYSTICAL_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_MYSTICAL_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=6000 + i,
            region=KeymastersKeepRegions.THE_MYSTICAL_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_MYSTICAL_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_OBSCURED_ARCH_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_OBSCURED_ARCH_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_OBSCURED_ARCH_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=6100 + i,
            region=KeymastersKeepRegions.THE_OBSCURED_ARCH,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_OBSCURED_ARCH),
        )
    )

location_data[KeymastersKeepLocations.THE_OBSCURED_DOORWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_OBSCURED_DOORWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_OBSCURED_DOORWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=6200 + i,
            region=KeymastersKeepRegions.THE_OBSCURED_DOORWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_OBSCURED_DOORWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_OBSCURED_PORTAL_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_OBSCURED_PORTAL_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_OBSCURED_PORTAL_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=6300 + i,
            region=KeymastersKeepRegions.THE_OBSCURED_PORTAL,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_OBSCURED_PORTAL),
        )
    )

location_data[KeymastersKeepLocations.THE_OBSCURED_VAULT_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_OBSCURED_VAULT_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_OBSCURED_VAULT_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=6400 + i,
            region=KeymastersKeepRegions.THE_OBSCURED_VAULT,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_OBSCURED_VAULT),
        )
    )

location_data[KeymastersKeepLocations.THE_OBSCURE_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_OBSCURE_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_OBSCURE_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=6500 + i,
            region=KeymastersKeepRegions.THE_OBSCURE_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_OBSCURE_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_PHANTOM_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_PHANTOM_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_PHANTOM_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=6600 + i,
            region=KeymastersKeepRegions.THE_PHANTOM_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_PHANTOM_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_PHANTOM_VAULT_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_PHANTOM_VAULT_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_PHANTOM_VAULT_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=6700 + i,
            region=KeymastersKeepRegions.THE_PHANTOM_VAULT,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_PHANTOM_VAULT),
        )
    )

location_data[KeymastersKeepLocations.THE_QUIET_ARCHWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_QUIET_ARCHWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_QUIET_ARCHWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=6800 + i,
            region=KeymastersKeepRegions.THE_QUIET_ARCHWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_QUIET_ARCHWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_QUIET_THRESHOLD_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_QUIET_THRESHOLD_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_QUIET_THRESHOLD_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=6900 + i,
            region=KeymastersKeepRegions.THE_QUIET_THRESHOLD,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_QUIET_THRESHOLD),
        )
    )

location_data[KeymastersKeepLocations.THE_SEALED_CHAMBER_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SEALED_CHAMBER_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SEALED_CHAMBER_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=7000 + i,
            region=KeymastersKeepRegions.THE_SEALED_CHAMBER,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SEALED_CHAMBER),
        )
    )

location_data[KeymastersKeepLocations.THE_SEALED_GATEWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SEALED_GATEWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SEALED_GATEWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=7100 + i,
            region=KeymastersKeepRegions.THE_SEALED_GATEWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SEALED_GATEWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_SEALED_THRESHOLD_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SEALED_THRESHOLD_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SEALED_THRESHOLD_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=7200 + i,
            region=KeymastersKeepRegions.THE_SEALED_THRESHOLD,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SEALED_THRESHOLD),
        )
    )

location_data[KeymastersKeepLocations.THE_SECRETED_DOOR_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SECRETED_DOOR_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SECRETED_DOOR_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=7300 + i,
            region=KeymastersKeepRegions.THE_SECRETED_DOOR,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SECRETED_DOOR),
        )
    )

location_data[KeymastersKeepLocations.THE_SECRETIVE_DOOR_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SECRETIVE_DOOR_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SECRETIVE_DOOR_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=7400 + i,
            region=KeymastersKeepRegions.THE_SECRETIVE_DOOR,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SECRETIVE_DOOR),
        )
    )

location_data[KeymastersKeepLocations.THE_SECRET_ARCHWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SECRET_ARCHWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SECRET_ARCHWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=7500 + i,
            region=KeymastersKeepRegions.THE_SECRET_ARCHWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SECRET_ARCHWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_SECRET_PASSAGEWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SECRET_PASSAGEWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SECRET_PASSAGEWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=7600 + i,
            region=KeymastersKeepRegions.THE_SECRET_PASSAGEWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SECRET_PASSAGEWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_SECRET_THRESHOLD_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SECRET_THRESHOLD_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SECRET_THRESHOLD_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=7700 + i,
            region=KeymastersKeepRegions.THE_SECRET_THRESHOLD,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SECRET_THRESHOLD),
        )
    )

location_data[KeymastersKeepLocations.THE_SECRET_VAULT_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SECRET_VAULT_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SECRET_VAULT_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=7800 + i,
            region=KeymastersKeepRegions.THE_SECRET_VAULT,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SECRET_VAULT),
        )
    )

location_data[KeymastersKeepLocations.THE_SHADOWED_PORTAL_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SHADOWED_PORTAL_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SHADOWED_PORTAL_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=7900 + i,
            region=KeymastersKeepRegions.THE_SHADOWED_PORTAL,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SHADOWED_PORTAL),
        )
    )

location_data[KeymastersKeepLocations.THE_SHADOWED_THRESHOLD_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SHADOWED_THRESHOLD_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SHADOWED_THRESHOLD_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=8000 + i,
            region=KeymastersKeepRegions.THE_SHADOWED_THRESHOLD,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SHADOWED_THRESHOLD),
        )
    )

location_data[KeymastersKeepLocations.THE_SHADOWY_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SHADOWY_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SHADOWY_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=8100 + i,
            region=KeymastersKeepRegions.THE_SHADOWY_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SHADOWY_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_SHIMMERING_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SHIMMERING_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SHIMMERING_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=8200 + i,
            region=KeymastersKeepRegions.THE_SHIMMERING_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SHIMMERING_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_SHROUDED_GATEWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SHROUDED_GATEWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SHROUDED_GATEWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=8300 + i,
            region=KeymastersKeepRegions.THE_SHROUDED_GATEWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SHROUDED_GATEWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_SHROUDED_PORTAL_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SHROUDED_PORTAL_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SHROUDED_PORTAL_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=8400 + i,
            region=KeymastersKeepRegions.THE_SHROUDED_PORTAL,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SHROUDED_PORTAL),
        )
    )

location_data[KeymastersKeepLocations.THE_SILENT_ARCHWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SILENT_ARCHWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SILENT_ARCHWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=8500 + i,
            region=KeymastersKeepRegions.THE_SILENT_ARCHWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SILENT_ARCHWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_SILENT_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SILENT_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SILENT_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=8600 + i,
            region=KeymastersKeepRegions.THE_SILENT_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SILENT_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_SILENT_THRESHOLD_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SILENT_THRESHOLD_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SILENT_THRESHOLD_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=8700 + i,
            region=KeymastersKeepRegions.THE_SILENT_THRESHOLD,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SILENT_THRESHOLD),
        )
    )

location_data[KeymastersKeepLocations.THE_SILENT_VAULT_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_SILENT_VAULT_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_SILENT_VAULT_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=8800 + i,
            region=KeymastersKeepRegions.THE_SILENT_VAULT,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_SILENT_VAULT),
        )
    )

location_data[KeymastersKeepLocations.THE_UNFATHOMABLE_DOOR_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_UNFATHOMABLE_DOOR_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_UNFATHOMABLE_DOOR_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=8900 + i,
            region=KeymastersKeepRegions.THE_UNFATHOMABLE_DOOR,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_UNFATHOMABLE_DOOR),
        )
    )

location_data[KeymastersKeepLocations.THE_UNKNOWN_ARCH_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_UNKNOWN_ARCH_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_UNKNOWN_ARCH_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=9000 + i,
            region=KeymastersKeepRegions.THE_UNKNOWN_ARCH,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_UNKNOWN_ARCH),
        )
    )

location_data[KeymastersKeepLocations.THE_UNKNOWN_GATEWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_UNKNOWN_GATEWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_UNKNOWN_GATEWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=9100 + i,
            region=KeymastersKeepRegions.THE_UNKNOWN_GATEWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_UNKNOWN_GATEWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_UNMARKED_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_UNMARKED_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_UNMARKED_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=9200 + i,
            region=KeymastersKeepRegions.THE_UNMARKED_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_UNMARKED_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_UNMARKED_VAULT_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_UNMARKED_VAULT_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_UNMARKED_VAULT_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=9300 + i,
            region=KeymastersKeepRegions.THE_UNMARKED_VAULT,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_UNMARKED_VAULT),
        )
    )

location_data[KeymastersKeepLocations.THE_UNRAVELED_DOOR_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_UNRAVELED_DOOR_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_UNRAVELED_DOOR_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=9400 + i,
            region=KeymastersKeepRegions.THE_UNRAVELED_DOOR,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_UNRAVELED_DOOR),
        )
    )

location_data[KeymastersKeepLocations.THE_UNSEEN_ARCHWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_UNSEEN_ARCHWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_UNSEEN_ARCHWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=9500 + i,
            region=KeymastersKeepRegions.THE_UNSEEN_ARCHWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_UNSEEN_ARCHWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_UNSEEN_DOOR_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_UNSEEN_DOOR_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_UNSEEN_DOOR_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=9600 + i,
            region=KeymastersKeepRegions.THE_UNSEEN_DOOR,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_UNSEEN_DOOR),
        )
    )

location_data[KeymastersKeepLocations.THE_UNSEEN_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_UNSEEN_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_UNSEEN_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=9700 + i,
            region=KeymastersKeepRegions.THE_UNSEEN_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_UNSEEN_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_UNSEEN_PORTAL_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_UNSEEN_PORTAL_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_UNSEEN_PORTAL_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=9800 + i,
            region=KeymastersKeepRegions.THE_UNSEEN_PORTAL,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_UNSEEN_PORTAL),
        )
    )

location_data[KeymastersKeepLocations.THE_UNSPOKEN_GATE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_UNSPOKEN_GATE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_UNSPOKEN_GATE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=9900 + i,
            region=KeymastersKeepRegions.THE_UNSPOKEN_GATE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_UNSPOKEN_GATE),
        )
    )

location_data[KeymastersKeepLocations.THE_UNTOLD_GATEWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_UNTOLD_GATEWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_UNTOLD_GATEWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=10000 + i,
            region=KeymastersKeepRegions.THE_UNTOLD_GATEWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_UNTOLD_GATEWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_UNTRACEABLE_PATH_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_UNTRACEABLE_PATH_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_UNTRACEABLE_PATH_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=10100 + i,
            region=KeymastersKeepRegions.THE_UNTRACEABLE_PATH,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_UNTRACEABLE_PATH),
        )
    )

location_data[KeymastersKeepLocations.THE_VANISHING_ARCHWAY_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_VANISHING_ARCHWAY_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_VANISHING_ARCHWAY_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=10200 + i,
            region=KeymastersKeepRegions.THE_VANISHING_ARCHWAY,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_VANISHING_ARCHWAY),
        )
    )

location_data[KeymastersKeepLocations.THE_VANISHING_DOOR_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_VANISHING_DOOR_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_VANISHING_DOOR_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=10300 + i,
            region=KeymastersKeepRegions.THE_VANISHING_DOOR,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_VANISHING_DOOR),
        )
    )

location_data[KeymastersKeepLocations.THE_VAULT_OF_WHISPERS_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_VAULT_OF_WHISPERS_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_VAULT_OF_WHISPERS_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=10400 + i,
            region=KeymastersKeepRegions.THE_VAULT_OF_WHISPERS,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_VAULT_OF_WHISPERS),
        )
    )

location_data[KeymastersKeepLocations.THE_VEILED_PASSAGE_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_VEILED_PASSAGE_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_VEILED_PASSAGE_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=10500 + i,
            region=KeymastersKeepRegions.THE_VEILED_PASSAGE,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_VEILED_PASSAGE),
        )
    )

location_data[KeymastersKeepLocations.THE_VEILED_PATH_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_VEILED_PATH_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_VEILED_PATH_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=10600 + i,
            region=KeymastersKeepRegions.THE_VEILED_PATH,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_VEILED_PATH),
        )
    )

location_data[KeymastersKeepLocations.THE_WHISPERED_PORTAL_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_WHISPERED_PORTAL_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_WHISPERED_PORTAL_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=10700 + i,
            region=KeymastersKeepRegions.THE_WHISPERED_PORTAL,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_WHISPERED_PORTAL),
        )
    )

location_data[KeymastersKeepLocations.THE_WHISPERED_THRESHOLD_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_WHISPERED_THRESHOLD_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_WHISPERED_THRESHOLD_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=10800 + i,
            region=KeymastersKeepRegions.THE_WHISPERED_THRESHOLD,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_WHISPERED_THRESHOLD),
        )
    )

location_data[KeymastersKeepLocations.THE_WHISPERING_DOOR_TRIAL] = list()

i: int
for i in range(trial_count):
    location_data[KeymastersKeepLocations.THE_WHISPERING_DOOR_TRIAL].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.THE_WHISPERING_DOOR_TRIAL.value.replace("TRIAL_NAME", trials[i]),
            archipelago_id=10900 + i,
            region=KeymastersKeepRegions.THE_WHISPERING_DOOR,
            tags=(KeymastersKeepTags.TRIALS, KeymastersKeepTags.TRIALS_THE_WHISPERING_DOOR),
        )
    )

# Shop Items
location_data[KeymastersKeepLocations.SHOP_ABYSSFORGE_CURIOS_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_ABYSSFORGE_CURIOS_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_ABYSSFORGE_CURIOS_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=20000 + i,
            region=KeymastersKeepRegions.SHOP_ABYSSFORGE_CURIOS,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_ABYSSFORGE_CURIOS),
        )
    )

location_data[KeymastersKeepLocations.SHOP_ARCANE_LANTERN_WORKSHOP_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_ARCANE_LANTERN_WORKSHOP_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_ARCANE_LANTERN_WORKSHOP_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=20100 + i,
            region=KeymastersKeepRegions.SHOP_ARCANE_LANTERN_WORKSHOP,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_ARCANE_LANTERN_WORKSHOP),
        )
    )

location_data[KeymastersKeepLocations.SHOP_ASTRAL_ECHO_ATELIER_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_ASTRAL_ECHO_ATELIER_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_ASTRAL_ECHO_ATELIER_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=20200 + i,
            region=KeymastersKeepRegions.SHOP_ASTRAL_ECHO_ATELIER,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_ASTRAL_ECHO_ATELIER),
        )
    )

location_data[KeymastersKeepLocations.SHOP_ASTRALGLOW_COLLECTION_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_ASTRALGLOW_COLLECTION_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_ASTRALGLOW_COLLECTION_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=20300 + i,
            region=KeymastersKeepRegions.SHOP_ASTRALGLOW_COLLECTION,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_ASTRALGLOW_COLLECTION),
        )
    )

location_data[KeymastersKeepLocations.SHOP_ASTRALHELM_ARMORY_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_ASTRALHELM_ARMORY_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_ASTRALHELM_ARMORY_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=20400 + i,
            region=KeymastersKeepRegions.SHOP_ASTRALHELM_ARMORY,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_ASTRALHELM_ARMORY),
        )
    )

location_data[KeymastersKeepLocations.SHOP_BLOODROSE_ATELIER_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_BLOODROSE_ATELIER_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_BLOODROSE_ATELIER_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=20500 + i,
            region=KeymastersKeepRegions.SHOP_BLOODROSE_ATELIER,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_BLOODROSE_ATELIER),
        )
    )

location_data[KeymastersKeepLocations.SHOP_CELESTIAL_CODEX_CURIOS_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_CELESTIAL_CODEX_CURIOS_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_CELESTIAL_CODEX_CURIOS_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=20600 + i,
            region=KeymastersKeepRegions.SHOP_CELESTIAL_CODEX_CURIOS,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_CELESTIAL_CODEX_CURIOS),
        )
    )

location_data[KeymastersKeepLocations.SHOP_DAWNSHARD_DEPOT_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_DAWNSHARD_DEPOT_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_DAWNSHARD_DEPOT_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=20700 + i,
            region=KeymastersKeepRegions.SHOP_DAWNSHARD_DEPOT,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_DAWNSHARD_DEPOT),
        )
    )

location_data[KeymastersKeepLocations.SHOP_DRAGONBONE_BAZAAR_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_DRAGONBONE_BAZAAR_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_DRAGONBONE_BAZAAR_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=20800 + i,
            region=KeymastersKeepRegions.SHOP_DRAGONBONE_BAZAAR,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_DRAGONBONE_BAZAAR),
        )
    )

location_data[KeymastersKeepLocations.SHOP_DREAMSHARD_COLLECTION_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_DREAMSHARD_COLLECTION_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_DREAMSHARD_COLLECTION_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=20900 + i,
            region=KeymastersKeepRegions.SHOP_DREAMSHARD_COLLECTION,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_DREAMSHARD_COLLECTION),
        )
    )

location_data[KeymastersKeepLocations.SHOP_DREAMLIGHT_DEPOT_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_DREAMLIGHT_DEPOT_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_DREAMLIGHT_DEPOT_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=21000 + i,
            region=KeymastersKeepRegions.SHOP_DREAMLIGHT_DEPOT,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_DREAMLIGHT_DEPOT),
        )
    )

location_data[KeymastersKeepLocations.SHOP_ECHOCHIME_PARLOR_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_ECHOCHIME_PARLOR_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_ECHOCHIME_PARLOR_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=21100 + i,
            region=KeymastersKeepRegions.SHOP_ECHOCHIME_PARLOR,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_ECHOCHIME_PARLOR),
        )
    )

location_data[KeymastersKeepLocations.SHOP_ECLIPSEGEAR_EMPORIUM_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_ECLIPSEGEAR_EMPORIUM_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_ECLIPSEGEAR_EMPORIUM_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=21200 + i,
            region=KeymastersKeepRegions.SHOP_ECLIPSEGEAR_EMPORIUM,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_ECLIPSEGEAR_EMPORIUM),
        )
    )

location_data[KeymastersKeepLocations.SHOP_EMBERHEART_FORGE_AND_FINDS_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_EMBERHEART_FORGE_AND_FINDS_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_EMBERHEART_FORGE_AND_FINDS_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=21300 + i,
            region=KeymastersKeepRegions.SHOP_EMBERHEART_FORGE_AND_FINDS,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_EMBERHEART_FORGE_AND_FINDS),
        )
    )

location_data[KeymastersKeepLocations.SHOP_EMBERWING_EMPORIUM_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_EMBERWING_EMPORIUM_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_EMBERWING_EMPORIUM_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=21400 + i,
            region=KeymastersKeepRegions.SHOP_EMBERWING_EMPORIUM,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_EMBERWING_EMPORIUM),
        )
    )

location_data[KeymastersKeepLocations.SHOP_ETHERHOLLOW_COLLECTION_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_ETHERHOLLOW_COLLECTION_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_ETHERHOLLOW_COLLECTION_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=21500 + i,
            region=KeymastersKeepRegions.SHOP_ETHERHOLLOW_COLLECTION,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_ETHERHOLLOW_COLLECTION),
        )
    )

location_data[KeymastersKeepLocations.SHOP_FIRESONG_FORGE_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_FIRESONG_FORGE_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_FIRESONG_FORGE_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=21600 + i,
            region=KeymastersKeepRegions.SHOP_FIRESONG_FORGE,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_FIRESONG_FORGE),
        )
    )

location_data[KeymastersKeepLocations.SHOP_FROSTLIGHT_CABINET_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_FROSTLIGHT_CABINET_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_FROSTLIGHT_CABINET_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=21700 + i,
            region=KeymastersKeepRegions.SHOP_FROSTLIGHT_CABINET,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_FROSTLIGHT_CABINET),
        )
    )

location_data[KeymastersKeepLocations.SHOP_FROSTWIND_FRONTIER_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_FROSTWIND_FRONTIER_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_FROSTWIND_FRONTIER_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=21800 + i,
            region=KeymastersKeepRegions.SHOP_FROSTWIND_FRONTIER,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_FROSTWIND_FRONTIER),
        )
    )

location_data[KeymastersKeepLocations.SHOP_IRONBLOOM_BAZAAR_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_IRONBLOOM_BAZAAR_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_IRONBLOOM_BAZAAR_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=21900 + i,
            region=KeymastersKeepRegions.SHOP_IRONBLOOM_BAZAAR,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_IRONBLOOM_BAZAAR),
        )
    )

location_data[KeymastersKeepLocations.SHOP_IRONSHARD_ARMORY_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_IRONSHARD_ARMORY_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_IRONSHARD_ARMORY_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=22000 + i,
            region=KeymastersKeepRegions.SHOP_IRONSHARD_ARMORY,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_IRONSHARD_ARMORY),
        )
    )

location_data[KeymastersKeepLocations.SHOP_LUMINSPIRE_WORKSHOP_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_LUMINSPIRE_WORKSHOP_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_LUMINSPIRE_WORKSHOP_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=22100 + i,
            region=KeymastersKeepRegions.SHOP_LUMINSPIRE_WORKSHOP,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_LUMINSPIRE_WORKSHOP),
        )
    )

location_data[KeymastersKeepLocations.SHOP_MOONLIT_RELIQUARY_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_MOONLIT_RELIQUARY_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_MOONLIT_RELIQUARY_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=22200 + i,
            region=KeymastersKeepRegions.SHOP_MOONLIT_RELIQUARY,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_MOONLIT_RELIQUARY),
        )
    )

location_data[KeymastersKeepLocations.SHOP_MOONREIGN_PARLOR_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_MOONREIGN_PARLOR_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_MOONREIGN_PARLOR_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=22300 + i,
            region=KeymastersKeepRegions.SHOP_MOONREIGN_PARLOR,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_MOONREIGN_PARLOR),
        )
    )

location_data[KeymastersKeepLocations.SHOP_MOONSTONE_MARKET_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_MOONSTONE_MARKET_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_MOONSTONE_MARKET_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=22400 + i,
            region=KeymastersKeepRegions.SHOP_MOONSTONE_MARKET,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_MOONSTONE_MARKET),
        )
    )

location_data[KeymastersKeepLocations.SHOP_MYTHRIL_MIRROR_MARKET_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_MYTHRIL_MIRROR_MARKET_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_MYTHRIL_MIRROR_MARKET_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=22500 + i,
            region=KeymastersKeepRegions.SHOP_MYTHRIL_MIRROR_MARKET,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_MYTHRIL_MIRROR_MARKET),
        )
    )

location_data[KeymastersKeepLocations.SHOP_NETHERGLOW_WORKSHOP_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_NETHERGLOW_WORKSHOP_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_NETHERGLOW_WORKSHOP_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=22600 + i,
            region=KeymastersKeepRegions.SHOP_NETHERGLOW_WORKSHOP,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_NETHERGLOW_WORKSHOP),
        )
    )

location_data[KeymastersKeepLocations.SHOP_NIGHTSPIRE_NOOK_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_NIGHTSPIRE_NOOK_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_NIGHTSPIRE_NOOK_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=22700 + i,
            region=KeymastersKeepRegions.SHOP_NIGHTSPIRE_NOOK,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_NIGHTSPIRE_NOOK),
        )
    )

location_data[KeymastersKeepLocations.SHOP_OBSIDIANFLARE_OUTPOST_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_OBSIDIANFLARE_OUTPOST_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_OBSIDIANFLARE_OUTPOST_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=22800 + i,
            region=KeymastersKeepRegions.SHOP_OBSIDIANFLARE_OUTPOST,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_OBSIDIANFLARE_OUTPOST),
        )
    )

location_data[KeymastersKeepLocations.SHOP_OPALINE_RELIQUARY_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_OPALINE_RELIQUARY_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_OPALINE_RELIQUARY_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=22900 + i,
            region=KeymastersKeepRegions.SHOP_OPALINE_RELIQUARY,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_OPALINE_RELIQUARY),
        )
    )

location_data[KeymastersKeepLocations.SHOP_RADIANTCORE_GALLERY_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_RADIANTCORE_GALLERY_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_RADIANTCORE_GALLERY_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=23000 + i,
            region=KeymastersKeepRegions.SHOP_RADIANTCORE_GALLERY,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_RADIANTCORE_GALLERY),
        )
    )

location_data[KeymastersKeepLocations.SHOP_RUNEBOUND_REPOSITORY_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_RUNEBOUND_REPOSITORY_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_RUNEBOUND_REPOSITORY_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=23100 + i,
            region=KeymastersKeepRegions.SHOP_RUNEBOUND_REPOSITORY,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_RUNEBOUND_REPOSITORY),
        )
    )

location_data[KeymastersKeepLocations.SHOP_RUNEBROOK_EXCHANGE_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_RUNEBROOK_EXCHANGE_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_RUNEBROOK_EXCHANGE_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=23200 + i,
            region=KeymastersKeepRegions.SHOP_RUNEBROOK_EXCHANGE,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_RUNEBROOK_EXCHANGE),
        )
    )

location_data[KeymastersKeepLocations.SHOP_RUNECROWN_BOUTIQUE_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_RUNECROWN_BOUTIQUE_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_RUNECROWN_BOUTIQUE_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=23300 + i,
            region=KeymastersKeepRegions.SHOP_RUNECROWN_BOUTIQUE,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_RUNECROWN_BOUTIQUE),
        )
    )

location_data[KeymastersKeepLocations.SHOP_SHADEWOOD_TROVE_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_SHADEWOOD_TROVE_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_SHADEWOOD_TROVE_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=23400 + i,
            region=KeymastersKeepRegions.SHOP_SHADEWOOD_TROVE,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_SHADEWOOD_TROVE),
        )
    )

location_data[KeymastersKeepLocations.SHOP_SHADOWMANTLE_MARKET_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_SHADOWMANTLE_MARKET_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_SHADOWMANTLE_MARKET_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=23500 + i,
            region=KeymastersKeepRegions.SHOP_SHADOWMANTLE_MARKET,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_SHADOWMANTLE_MARKET),
        )
    )

location_data[KeymastersKeepLocations.SHOP_SHATTERSTONE_TROVE_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_SHATTERSTONE_TROVE_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_SHATTERSTONE_TROVE_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=23600 + i,
            region=KeymastersKeepRegions.SHOP_SHATTERSTONE_TROVE,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_SHATTERSTONE_TROVE),
        )
    )

location_data[KeymastersKeepLocations.SHOP_SILVERDAWN_SUNDRIES_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_SILVERDAWN_SUNDRIES_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_SILVERDAWN_SUNDRIES_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=23700 + i,
            region=KeymastersKeepRegions.SHOP_SILVERDAWN_SUNDRIES,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_SILVERDAWN_SUNDRIES),
        )
    )

location_data[KeymastersKeepLocations.SHOP_SILVERQUARTZ_EXCHANGE_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_SILVERQUARTZ_EXCHANGE_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_SILVERQUARTZ_EXCHANGE_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=23800 + i,
            region=KeymastersKeepRegions.SHOP_SILVERQUARTZ_EXCHANGE,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_SILVERQUARTZ_EXCHANGE),
        )
    )

location_data[KeymastersKeepLocations.SHOP_SPIRITCHIME_BOUTIQUE_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_SPIRITCHIME_BOUTIQUE_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_SPIRITCHIME_BOUTIQUE_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=23900 + i,
            region=KeymastersKeepRegions.SHOP_SPIRITCHIME_BOUTIQUE,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_SPIRITCHIME_BOUTIQUE),
        )
    )

location_data[KeymastersKeepLocations.SHOP_STARBOUND_STUDIO_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_STARBOUND_STUDIO_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_STARBOUND_STUDIO_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=24000 + i,
            region=KeymastersKeepRegions.SHOP_STARBOUND_STUDIO,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_STARBOUND_STUDIO),
        )
    )

location_data[KeymastersKeepLocations.SHOP_STARROOT_REPOSITORY_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_STARROOT_REPOSITORY_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_STARROOT_REPOSITORY_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=24100 + i,
            region=KeymastersKeepRegions.SHOP_STARROOT_REPOSITORY,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_STARROOT_REPOSITORY),
        )
    )

location_data[KeymastersKeepLocations.SHOP_STARWEAVE_ARMORY_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_STARWEAVE_ARMORY_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_STARWEAVE_ARMORY_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=24200 + i,
            region=KeymastersKeepRegions.SHOP_STARWEAVE_ARMORY,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_STARWEAVE_ARMORY),
        )
    )

location_data[KeymastersKeepLocations.SHOP_STORMHOLLOW_GEARWORKS_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_STORMHOLLOW_GEARWORKS_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_STORMHOLLOW_GEARWORKS_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=24300 + i,
            region=KeymastersKeepRegions.SHOP_STORMHOLLOW_GEARWORKS,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_STORMHOLLOW_GEARWORKS),
        )
    )

location_data[KeymastersKeepLocations.SHOP_SUNFORGE_SUNDRIES_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_SUNFORGE_SUNDRIES_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_SUNFORGE_SUNDRIES_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=24400 + i,
            region=KeymastersKeepRegions.SHOP_SUNFORGE_SUNDRIES,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_SUNFORGE_SUNDRIES),
        )
    )

location_data[KeymastersKeepLocations.SHOP_THORNBLOOM_CRAFTWORKS_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_THORNBLOOM_CRAFTWORKS_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_THORNBLOOM_CRAFTWORKS_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=24500 + i,
            region=KeymastersKeepRegions.SHOP_THORNBLOOM_CRAFTWORKS,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_THORNBLOOM_CRAFTWORKS),
        )
    )

location_data[KeymastersKeepLocations.SHOP_THORNVALE_WORKSHOP_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_THORNVALE_WORKSHOP_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_THORNVALE_WORKSHOP_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=24600 + i,
            region=KeymastersKeepRegions.SHOP_THORNVALE_WORKSHOP,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_THORNVALE_WORKSHOP),
        )
    )

location_data[KeymastersKeepLocations.SHOP_THUNDERSHARD_TROVE_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_THUNDERSHARD_TROVE_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_THUNDERSHARD_TROVE_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=24700 + i,
            region=KeymastersKeepRegions.SHOP_THUNDERSHARD_TROVE,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_THUNDERSHARD_TROVE),
        )
    )

location_data[KeymastersKeepLocations.SHOP_VINEWHISPER_VAULT_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_VINEWHISPER_VAULT_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_VINEWHISPER_VAULT_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=24800 + i,
            region=KeymastersKeepRegions.SHOP_VINEWHISPER_VAULT,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_VINEWHISPER_VAULT),
        )
    )

location_data[KeymastersKeepLocations.SHOP_VOIDSPIRE_VAULT_ITEM] = list()

i: int
for i in range(5):
    location_data[KeymastersKeepLocations.SHOP_VOIDSPIRE_VAULT_ITEM].append(
        KeymastersKeepLocationData(
            name=KeymastersKeepLocations.SHOP_VOIDSPIRE_VAULT_ITEM.value.replace("ITEM_NUMBER", str(i + 1)),
            archipelago_id=24900 + i,
            region=KeymastersKeepRegions.SHOP_VOIDSPIRE_VAULT,
            tags=(KeymastersKeepTags.SHOP_ITEM, KeymastersKeepTags.SHOP_VOIDSPIRE_VAULT),
        )
    )
