from typing import TYPE_CHECKING
from copy import deepcopy

from Options import OptionError
from Fill import FillError

from ..Locations import LOCATION_TABLE
from ..Items import ITEM_TABLE
from ..Options import SSOptions
from ..Constants import *

from ..logic.Logic import ALL_REQUIREMENTS

if TYPE_CHECKING:
    from .. import SSWorld

def shuffle_batreaux_counts(world: "SSWorld") -> dict[str, int]:
    """
    
    """
    batreaux_setting = world.options.batreaux_counts
    if batreaux_setting == "vanilla":
        batreaux_counts = [5, 10, 30, 40, 50, 70, 80]
    elif batreaux_setting == "half":
        batreaux_counts = [2, 5, 15, 20, 25, 35, 40]
    elif batreaux_setting == "shuffled":
        batreaux_counts = world.random.sample(range(1, 81), 7)
        batreaux_counts.sort()
    elif batreaux_setting == "shuffled_high":
        batreaux_counts = world.random.sample(range(30, 81), 7)
        batreaux_counts.sort()
    elif batreaux_setting == "shuffled_low":
        batreaux_counts = world.random.sample(range(1, 51), 7)
        batreaux_counts.sort()
    else:
        raise OptionError(f"Unknown value for option batreaux_counts: {batreaux_setting.value}")
    
    batreaux_rewards = {
        "First Reward": 0,
        "Second Reward": 0,
        "Third Reward": 0, # Also counts for chest check
        "Fourth Reward": 0,
        "Fifth Reward": 0,
        "Sixth Reward": 0, # Also counts for seventh reward check
        "Final Reward": 0,
    }

    for reward, count in zip(batreaux_rewards.keys(), batreaux_counts):
        batreaux_rewards[reward] = count

    return batreaux_rewards
