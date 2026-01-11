from BaseClasses import ItemClassification
from .. import ClassificationMethod


always_progression: ClassificationMethod = lambda world: ItemClassification.progression

always_useful: ClassificationMethod = lambda world: ItemClassification.useful

always_filler: ClassificationMethod = lambda world: ItemClassification.filler

always_trap: ClassificationMethod = lambda world: ItemClassification.trap

tm_hm_hunt: ClassificationMethod = lambda world: (
    ItemClassification.progression_deprioritized
    if world.options.goal in ("tmhm_hunt", "pokemon_master") else ItemClassification.useful
)

dowsing_machine_logic: ClassificationMethod = lambda world: (
    ItemClassification.progression
    if "Require Dowsing Machine" in world.options.modify_logic else ItemClassification.useful
)
