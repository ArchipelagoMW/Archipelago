from .. import LocationData
from ..progress_type import *

locations: dict[str, LocationData] = {
    f"Task #{x}-{y}": LocationData(10000 + x * 10 + y, always_default)
    for x in range(1, 201)
    for y in range(1, 6)
}
