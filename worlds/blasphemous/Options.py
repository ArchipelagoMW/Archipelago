from Options import Choice, Toggle, DefaultOnToggle, DeathLink

class StrictMiasma(DefaultOnToggle):
    """Items obscured by miasma will logically require the Silvered Lung of Dolphos to obtain, rather than taking damage to get the item."""
    display_name = "Strict Miasma Rules"

blasphemous_options = {
    "strict_miasma" : StrictMiasma
}