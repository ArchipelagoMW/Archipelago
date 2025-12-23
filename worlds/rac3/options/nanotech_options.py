from Options import Choice
from worlds.rac3 import RAC3OPTION


class NanotechMilestones(Choice):
    """
    Determines whether nanotech milestones are locations in the world.
    None: No nanotech milestones are locations.
    Every 20: Makes every 20 nanotech milestones locations starting from nanotech level 20.
    Every 10: Makes every 10 nanotech milestones locations starting from nanotech level 20.
    Every 5: Makes every 5 nanotech milestones locations starting from nanotech level 15.
    All: All nanotech milestones are locations.
    """
    display_name = RAC3OPTION.NANOTECH_MILESTONES
    option_none = 0
    option_every_20 = 1
    option_every_10 = 2
    option_every_5 = 3
    option_all = 4
    default = 0
