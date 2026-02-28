"""Logic information for glitch logic."""

from __future__ import annotations

from typing import TYPE_CHECKING


class GlitchLogicItem:
    """Glitch Logic multiselector information."""

    def __init__(self, name: str, tooltip: str = "") -> None:
        """Initialize with given data."""
        self.name = name
        self.shorthand = name.lower().replace(" ", "_")
        self.tooltip = tooltip


GlitchSelector = []
# If you make changes to this list, make sure to change the corresponding
# GlitchesSelected enum in randomizer.Enums.Settings.
GlitchLogicItems = [
    GlitchLogicItem("B Locker Skips", "Any skip that allows you to bypass the B. Locker's requirements."),
    GlitchLogicItem(
        "General Clips",
        "Any trick that doesn't fall into a general category. Includes object clips, bush push, terminal 2 clip and Crypt jump clip.",
    ),
    GlitchLogicItem("Ledge Clips", "A trick that allows the player to fall through gaps between walls and floors."),
    GlitchLogicItem("Moonkicks", "A trick that allows Donkey to ascend by interrupting his aerial attack with a kick."),
    GlitchLogicItem("Moontail", "A trick that allows the player to gain extra height with Diddy"),
    GlitchLogicItem(
        "Phase Swimming",
        "Formerly known as STVW, a trick to go through a significant amount of walls in the game whilst underwater.",
    ),
    GlitchLogicItem(
        "Phase Walking",
        "A triple-frame perfect technique to go through a significant amount of walls in the game. This option also includes Phase Falling",
    ),
    GlitchLogicItem(
        "Skew",
        "A trick that enables you to rotate the kong's collision and model, enabling the player to go through most walls in the game.",
    ),
    GlitchLogicItem(
        "Spawn Snags",
        "A trick that allows you to collect items earlier than intended by keeping them unloaded. Only accounts for spawn snags that have been done by humans.",
    ),
    GlitchLogicItem("Swim through Shores", "A trick that allows you to swim into a sloped shoreline to get out of bounds."),
    GlitchLogicItem("Tag Barrel Storage", "A trick that allows you to store a tag barrel being entered and abuse that storage. Includes telegrabs and Orangstand TBS Noclips."),
    GlitchLogicItem("Troff n Scoff Skips", "Any skip that allows you to bypass the kong and small banana requirement in order to fight a boss."),
    GlitchLogicItem("PhaseFall", "An alternative to Phase walking that allows you to use fairy camera and Chunky to go through walls"),
    # GlitchLogicItem("Boulder Clips"),
]
for item in GlitchLogicItems:
    if item.name != "No Group":
        GlitchSelector.append({"name": item.name, "value": item.shorthand, "tooltip": item.tooltip})

TrickSelector = []
TrickItems = [
    GlitchLogicItem("Advanced Grenading", "Advanced techniques using oranges."),
    GlitchLogicItem("Monkey Maneuvers", "Advanced platforming techniques that aren't considered beginner friendly will be considered as part of logic."),
    GlitchLogicItem("Hard Shooting", "Doing gun shooting tasks without items that make the task easy will be considered in logic."),
    GlitchLogicItem("Slope Resets", "Can use the Kong's techniques to climb a slippery slope without Orangstand."),
]
for item in TrickItems:
    if item.name != "No Group":
        TrickSelector.append({"name": item.name, "value": item.shorthand, "tooltip": item.tooltip})
