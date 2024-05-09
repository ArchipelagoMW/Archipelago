from Options import Choice, StartInventoryPool, PerGameCommonOptions
from dataclasses import dataclass


class ScalingType(Choice):
    """
        This will determine how stage difficulty is scaled.
        An item appearing in a stage is directly tied to the difficulty they appear in.
        Difficulty maxes out at 4, either through active player count, or player level by default.
        Levels: Stages will increase in difficulty every 5 player levels. Base level increases every domain.
        Clear Count: Stage difficulty will increase by 1 every time you clear it.
        """
    display_name = "Scaling Type"
    option_levels = 0
    option_clear_count = 1
    default = 0

@dataclass
class GLOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    scaling_type: ScalingType
