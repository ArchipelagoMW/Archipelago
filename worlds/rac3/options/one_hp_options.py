from Options import OptionDict
from worlds.rac3 import RAC3OPTION
from worlds.rac3.constants.player_type import ONE_HP_CHALLENGE_CHARACTERS


class OneHpChallenge(OptionDict):
    """
    Game is too easy? Try this challenge mode where the player has only 1 HP!
    Each option toggles 1 HP for a specific character or vehicle.
    Ratchet: Ratchet has only 1 HP.
    Clank: Clank has only 1 HP.
    Vehicle: Vehicles have only 1 HP.
    Qwark: Qwark has only 1 HP.
    Giant Clank: Giant Clank has only 1 HP. This one is impossible as terror of talos will one hit you immediately
    If you feel like this is too hard for you, you can always toggle the challenge for a character using /one_hp [character name]
    """
    display_name = RAC3OPTION.ONE_HP_CHALLENGE
    default = {name: False for name in ONE_HP_CHALLENGE_CHARACTERS}
    valid_keys = ONE_HP_CHALLENGE_CHARACTERS


