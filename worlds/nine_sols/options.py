from dataclasses import dataclass

from Options import DefaultOnToggle, PerGameCommonOptions, StartInventoryPool, Toggle


class ShuffleSolSeals(DefaultOnToggle):
    """Allows the Sol Seal items to be placed on any location in the multiworld, instead of their vanilla locations."""
    display_name = "Shuffle Sol Seals"


class SkipSoulscapePlatforming(Toggle):
    """When you unlock Lady Ethereal by collecting 4 Sol Seals, if this option is enabled, Cortex Center will skip ahead
    to the state where you can enter her boss fight, instead of the long platforming sequence you normally do first.

    This is a .yaml/generation option because it has a small effect on logic: The platforming sequence logically
    requires Tai-Chi Kick, so skipping it allows the Lady Ethereal fight to be in-logic without Tai-Chi Kick."""
    display_name = "Skip Soulscape Platforming"


@dataclass
class NineSolsGameOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    shuffle_sol_seals: ShuffleSolSeals
    skip_soulscape_platforming: SkipSoulscapePlatforming

