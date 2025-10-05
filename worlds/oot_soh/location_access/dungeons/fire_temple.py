from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


def set_region_rules(world: "SohWorld") -> None:
    player = world.player
    
