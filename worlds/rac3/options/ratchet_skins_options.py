from Options import Choice
from worlds.rac3 import RAC3OPTION


class RatchetSkin(Choice):
    """
    Cosmetic:
    What Skin should Ratchet have?
    Remember to reload your save file after starting a new game to apply the skin!
    """
    display_name = RAC3OPTION.SKIN
    option_default = 0
    option_old_school = 5
    option_snowman = 6
    option_tuxedo = 7
    option_buginoid = 8
    option_brainius = 9
    option_unused_robot = 10
    option_robo_rooster = 11
    option_trooper = 12
    option_robo = 13
    default = 0
