import typing
from Options import  DefaultOnToggle, Option


class EnablePurpleCoinStars(DefaultOnToggle):
    """tuning this off we allow purple coin stars to count as checks *note all purple coin stars are postgame only but one."""
    display_name = "Disable Purple Coin Stars"

smg_options= {
    "EnablePurpleCoinStars": EnablePurpleCoinStars
}
