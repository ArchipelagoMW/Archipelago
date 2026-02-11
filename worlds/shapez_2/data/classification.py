from BaseClasses import ItemClassification
from . import ClassificationMethod

always_progression: ClassificationMethod = lambda world: ItemClassification.progression
always_progression_deprioritized: ClassificationMethod = lambda world: ItemClassification.progression_deprioritized
always_progression_skip_balancing: ClassificationMethod = lambda world: ItemClassification.progression_skip_balancing
always_useful: ClassificationMethod = lambda world: ItemClassification.useful
always_filler: ClassificationMethod = lambda world: ItemClassification.filler
