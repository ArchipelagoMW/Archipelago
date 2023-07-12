from Options import Choice, Toggle


class StartingArea(Choice):
    """
    Which chunks are available at the start. The player may need to move through locked chunks to reach the starting
    area, but any areas that require quests, skills, or coins are not available as starting location.

    Any Bank rolls a random region that contains a bank.
    Chunksanity can start you in any chunk. Hope you like woodcutting!
    """
    display_name = "Starting Region"
    option_lumbridge = 0
    option_al_kharid = 1
    option_varrock_east = 2
    option_varrock_west = 3
    option_edgeville = 4
    option_falador = 5
    option_draynor = 6
    option_wilderness = 7
    option_any_bank = 8
    option_chunksanity = 9
    default = 0


class BrutalGrinds(Toggle):
    """
    Whether to allow skill tasks without having reasonable access to the usual skill training path.
    For example, if enabled, you could be forced to train smithing without an anvil purely by smelting bars,
    or training fishing to high levels entirely on shrimp.
    """
    display_name = "Allow Brutal Grinds"


OSRSOptions = {
    "starting_area": StartingArea,
    "brutal_grinds": BrutalGrinds
}
