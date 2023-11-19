from typing import Dict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

class PrioritizeBosses(Toggle):
    """
    Should boss location prioritize holding friend cards?
    """
    display_name = "Friend Cards Prioritized to Bosses"


khcom_options: Dict[str, type(Option)] = {
    "prioritize_bosses": PrioritizeBosses,
}
