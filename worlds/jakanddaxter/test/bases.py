from worlds.jakanddaxter import JakAndDaxterWorld
from ..game_id import jak1_name
from test.bases import WorldTestBase


class JakAndDaxterTestBase(WorldTestBase):
    game = jak1_name
    world: JakAndDaxterWorld

    level_info = {
        "Geyser Rock": {
            "cells": 4,
            "flies": 7,
            "orbs": 50,
            "caches": 0,
        },
        "Sandover Village": {
            "cells": 6,
            "flies": 7,
            "orbs": 50,
            "caches": 1,
        },
        "Forbidden Jungle": {
            "cells": 8,
            "flies": 7,
            "orbs": 150,
            "caches": 1,
        },
        "Sentinel Beach": {
            "cells": 8,
            "flies": 7,
            "orbs": 150,
            "caches": 2,
        },
        "Misty Island": {
            "cells": 8,
            "flies": 7,
            "orbs": 150,
            "caches": 1,
        },
        "Fire Canyon": {
            "cells": 2,
            "flies": 7,
            "orbs": 50,
            "caches": 0,
        },
        "Rock Village": {
            "cells": 6,
            "flies": 7,
            "orbs": 50,
            "caches": 1,
        },
        "Precursor Basin": {
            "cells": 8,
            "flies": 7,
            "orbs": 200,
            "caches": 0,
        },
        "Lost Precursor City": {
            "cells": 8,
            "flies": 7,
            "orbs": 200,
            "caches": 2,
        },
        "Boggy Swamp": {
            "cells": 8,
            "flies": 7,
            "orbs": 200,
            "caches": 0,
        },
        "Mountain Pass": {
            "cells": 4,
            "flies": 7,
            "orbs": 50,
            "caches": 0,
        },
        "Volcanic Crater": {
            "cells": 8,
            "flies": 7,
            "orbs": 50,
            "caches": 0,
        },
        "Spider Cave": {
            "cells": 8,
            "flies": 7,
            "orbs": 200,
            "caches": 0,
        },
        "Snowy Mountain": {
            "cells": 8,
            "flies": 7,
            "orbs": 200,
            "caches": 3,
        },
        "Lava Tube": {
            "cells": 2,
            "flies": 7,
            "orbs": 50,
            "caches": 0,
        },
        "Gol and Maia's Citadel": {
            "cells": 5,
            "flies": 7,
            "orbs": 200,
            "caches": 3,
        },
    }
