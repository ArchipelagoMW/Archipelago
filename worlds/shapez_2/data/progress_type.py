from BaseClasses import LocationProgressType
from . import ProgressTypeMethod

always_default: ProgressTypeMethod = lambda world: LocationProgressType.DEFAULT
always_priority: ProgressTypeMethod = lambda world: LocationProgressType.PRIORITY
always_excluded: ProgressTypeMethod = lambda world: LocationProgressType.EXCLUDED
