from .. import JakAndDaxterWorld
from ..GameID import jak1_name
from test.bases import WorldTestBase


class JakAndDaxterTestBase(WorldTestBase):
    game = jak1_name
    world: JakAndDaxterWorld

    level_info = {
        "Geyser Rock": {
            "cells": 4,
            "flies": 7,
            "orbs": 50,
        },
        "Sandover Village": {
            "cells": 6,
            "flies": 7,
            "orbs": 50,
        },
        "Forbidden Jungle": {
            "cells": 8,
            "flies": 7,
            "orbs": 150,
        },
        "Sentinel Beach": {
            "cells": 8,
            "flies": 7,
            "orbs": 150,
        },
        "Misty Island": {
            "cells": 8,
            "flies": 7,
            "orbs": 150,
        },
        "Fire Canyon": {
            "cells": 2,
            "flies": 7,
            "orbs": 50,
        },
        "Rock Village": {
            "cells": 6,
            "flies": 7,
            "orbs": 50,
        },
        "Precursor Basin": {
            "cells": 8,
            "flies": 7,
            "orbs": 200,
        },
        "Lost Precursor City": {
            "cells": 8,
            "flies": 7,
            "orbs": 200,
        },
        "Boggy Swamp": {
            "cells": 8,
            "flies": 7,
            "orbs": 200,
        },
        "Mountain Pass": {
            "cells": 4,
            "flies": 7,
            "orbs": 50,
        },
        "Volcanic Crater": {
            "cells": 8,
            "flies": 7,
            "orbs": 50,
        },
        "Spider Cave": {
            "cells": 8,
            "flies": 7,
            "orbs": 200,
        },
        "Snowy Mountain": {
            "cells": 8,
            "flies": 7,
            "orbs": 200,
        },
        "Lava Tube": {
            "cells": 2,
            "flies": 7,
            "orbs": 50,
        },
        "Gol and Maia's Citadel": {
            "cells": 5,
            "flies": 7,
            "orbs": 200,
        },
    }
