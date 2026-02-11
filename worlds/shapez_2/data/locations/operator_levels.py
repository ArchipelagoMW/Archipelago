from .. import LocationData
from ..progress_type import *

locations: dict[str, LocationData] = {
    f"Operator level {x}": LocationData(20000 + x, always_default)
    for x in range(1, 201)
}
