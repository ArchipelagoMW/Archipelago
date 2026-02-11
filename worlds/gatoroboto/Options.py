from dataclasses import dataclass

from Options import ItemsAccessibility

## Add deathlink later!!!
from Options import Toggle, OptionGroup, PerGameCommonOptions

class RocketJumps(Toggle):
    """
    Enable logic for accessing locations using rocket jumps.
    This also includes logic for requiring the coolant module for some jumps.
    """
    display_name = "Rocket Jumps"

class PreciseTricks(Toggle):
    """
    Enable logic for accessing locations that are mechanically difficult.
    """
    display_name = "Precise Tricks"
        
class WaterMech(Toggle):
    """
    Enable logic for accessing locations with the Water Mech glitch.
    """
    display_name = "Water Mech"
            
class SmallMech(Toggle):
    """
    Enable logic for accessing locations with the Small Mech glitch.
    """
    display_name = "Small Mech"
    
gatoroboto_option_groups = [
    OptionGroup("Logic Options", [
        RocketJumps,
        PreciseTricks,
        WaterMech,
        SmallMech
    ])
]

@dataclass
class GatoRobotoOptions(PerGameCommonOptions):
    accessibility: ItemsAccessibility
    rocket_jumps: RocketJumps
    precise_tricks: PreciseTricks
    water_mech: WaterMech
    small_mech: SmallMech