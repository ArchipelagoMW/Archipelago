"""Hard Mode information."""


class HardModeItem:
    """Hard Mode multiselector information."""

    def __init__(self, name, shift, tooltip=""):
        """Initialize with given data."""
        self.name = name
        self.shift = shift
        self.tooltip = tooltip


HardSelector = []
HardBossSelector = []
# If you make changes to this list, make sure to change the corresponding
# MiscChangesSelected enum in randomizer.Enums.Settings.
HardItems = [
    HardModeItem("Hard Enemies", 3, "Enemies fight back a little harder."),
    HardModeItem("Water is Lava", 1, "All water surfaces are lava water instead, damaging you."),
    HardModeItem("Reduced Fall Damage Threshold", 0, "The amount of distance required to fall too far has been reduced by 70%."),
    HardModeItem("Shuffled Jetpac Enemies", -1, "Jetpac enemies are shuffled within Jetpac."),
    HardModeItem("Lower Max Refill Amounts", -1, "Refills will have lower caps."),
    HardModeItem("Strict Helm Timer", -1, "Helm Timer starts a base time of 0 minutes instead of 10, requiring Blueprints to be turned in to Snides in order to access the level."),
    HardModeItem("Angry Caves", -1, "Rockfall in Caves is constant, and more deadly than ever."),
    HardModeItem("Fast Balloons", -1, "Balloons are 4x faster than normal."),
    HardModeItem(
        "Donk in the Dark World",
        -1,
        "All maps are pitch black, with only a light to help you path your way to the end of the game. Mixing this with 'Donk in the Sky' will convert the challenge into 'Memory Challenge' instead.",
    ),
    HardModeItem(
        "Donk in the Sky",
        -1,
        "Level geometry is invisible. Mixing this with 'Donk in the Dark World' will convert the challenge into 'Memory Challenge' instead.",
    ),
]
HardBossItems = [
    HardModeItem("Fast Mad Jack", -1, "Mad Jack is faster."),
    HardModeItem("Alternative Mad Jack Kongs", -1, "Mad Jack can now be beaten with DK, Chunky and twirlless Tiny."),
    HardModeItem("Pufftoss Star Rando", -1, "Star locations in Pufftoss are randomized."),
    HardModeItem("Pufftoss Star Raised", -1, "Star locations in Pufftoss are raised slightly, requiring that they are jumped into."),
    HardModeItem("Kut Out Phase Rando", -1, "Kut Out Phases have been randomized in order, including the unused 4th phase."),
    HardModeItem("K Rool Toes Rando", -1, "The toe sequence in Tiny Phase is randomized."),
    HardModeItem("Beta Lanky Phase", -1, "K. Rool is distracted by shooting a balloon rather than playing an instrument."),
]
for item in HardItems:
    if item.name != "No Group":
        HardSelector.append(
            {
                "name": item.name,
                "value": item.name.lower().replace(" ", "_"),
                "tooltip": item.tooltip,
                "shift": item.shift,
            }
        )
for item in HardBossItems:
    if item.name != "No Group":
        HardBossSelector.append(
            {
                "name": item.name,
                "value": item.name.lower().replace(" ", "_"),
                "tooltip": item.tooltip,
                "shift": item.shift,
            }
        )
