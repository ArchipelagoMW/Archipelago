import sys
module = sys.modules[__name__]

from ..objectives.objectives import Objectives
sys.modules[__name__] = Objectives()
