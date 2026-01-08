from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions


class DoYouLikeWaffles(Choice):
    """Placeholder option for now."""
    display_name = "Do you like waffles?"
    rich_text_doc = True
    option_yeah_we_like_waffles = 0
    option_just_give_me_my_new_ap_game = 1
    default = 1


@dataclass
class Shapez2Options(PerGameCommonOptions):
    do_you_like_waffles: DoYouLikeWaffles
