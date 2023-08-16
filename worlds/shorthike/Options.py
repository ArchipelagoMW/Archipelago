from typing import Dict
from Options import AssembleOptions, Choice, Toggle

class Goal(Choice):
    """Choose the end goal.
    Complete the climb to the top of Hawk Peak and take a nap"""
    display_name = "Goal"
    option_nap = 0
    default = 0

class ShowGoldenChests(Toggle):
    """Turns chests that contain items required for progression into golden chests."""
    display_name = "Progression Items in Golden Chests"

class SkipCutscenes(Toggle):
    """Skip major cutscenes."""
    display_name = "Skip Cutscenes"

short_hike_options: Dict[str, AssembleOptions] = {
    "goal": Goal,
    "show_golden_chests": ShowGoldenChests,
    "skip_cutscenes": SkipCutscenes,
}