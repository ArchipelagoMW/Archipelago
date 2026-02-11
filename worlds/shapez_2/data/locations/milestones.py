from .. import LocationData
from ..progress_type import *

locations: dict[str, LocationData] = {
    f"Milestone {x} reward #{y}": LocationData(x * 100 + y, always_default)
    for x in range(1, 21)
    for y in range(1, 13)
}
