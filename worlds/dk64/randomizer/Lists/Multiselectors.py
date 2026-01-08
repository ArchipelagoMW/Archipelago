"""Multiselector information."""

from __future__ import annotations

from typing import TYPE_CHECKING

from randomizer.Enums.Levels import Levels


class MultiselectorItem:
    """Quality of life multiselector information."""

    def __init__(self, name: str, shift: int, tooltip: str = "") -> None:
        """Initialize with given data."""
        self.name = name
        self.shift = shift
        self.tooltip = tooltip


QoLSelector = []
RemovedBarrierSelector = []
FasterCheckSelector = []
CBRandoSelector = []

# If you make changes to this list, make sure to change the corresponding
# MiscChangesSelected enum in randomizer.Enums.Settings.
QoLItems = [
    MultiselectorItem(
        "Auto Dance Skip",
        4,
        "Dances upon picking up some collectables, notably Golden Bananas, are removed (with some exceptions).",
    ),
    MultiselectorItem("Fast Boot", 5, "The boot sequence is dramatically sped up."),
    MultiselectorItem("Calm Caves", 12, "Crystal Caves will no longer rain rocks down periodically."),
    MultiselectorItem(
        "Animal Buddies grab Items",
        13,
        "Rambi and Enguarde will be able to pick up DK's and Lanky's Items respectively.",
    ),
    MultiselectorItem("Reduced Lag", 0, "Lag is reduced where possible without hindering gameplay."),
    MultiselectorItem("Remove Extraneous Cutscenes", 1, "A lot of cutscenes are removed, enabling a fast-paced game."),
    MultiselectorItem(
        "Hint Textbox Hold",
        11,
        "Hint Textboxes will not close automatically upon the game reaching the end of the text, requiring B to be pressed.",
    ),
    MultiselectorItem(
        "Remove Wrinkly Puzzles",
        -1,
        "Removes the Wrinkly Puzzles from the Angry Aztec, Fungi Forest and Crystal Caves lobbies",
    ),
    MultiselectorItem(
        "Fast Picture Taking",
        -1,
        "The picture taking sequence is heavily sped up, with lag being significantly reduced on BizHawk.",
    ),
    MultiselectorItem(
        "HUD Hotkey",
        14,
        "Pressing D-Pad Up will show the total amount of colored bananas acquired in the level, as well as the blueprint count for that Kong.",
    ),
    MultiselectorItem(
        "Ammo Swap",
        7,
        "Homing Ammo and Standard ammo can be swapped between (upon having Homing Ammo) by pressing D-Pad Down.",
    ),
    MultiselectorItem("Homing Balloons", 15, "Homing Ammo homes in on Banana Balloons."),
    MultiselectorItem("Fast Transform Animation", -1, "Transform barrels will not go through the morphing animation."),
    MultiselectorItem(
        "Troff n Scoff Audio Indicator",
        8,
        "A bell ding will play upon collecting enough colored bananas to unlock the level's boss.",
    ),
    MultiselectorItem("Lowered Aztec Lobby Bonus", -1, "The bonus barrel in Aztec Lobby is lowered to make it easier to reach."),
    MultiselectorItem(
        "Quicker Galleon Star",
        9,
        "The star in Gloomy Galleon now only requires Enguarde to go through it once to open the Gold Tower Gate.",
    ),
    MultiselectorItem("Vanilla Bug Fixes", 10, "Various bugs in the vanilla game have been fixed."),
    MultiselectorItem(
        "Save K Rool Progress",
        16,
        "Re-Entering K Rool after dying or pause exiting will spawn you in the latest phase you reached.",
    ),
    MultiselectorItem(
        "Small Bananas always visible",
        -1,
        "Small Bananas will always be visible regardless of whether you have the kong unlocked or not.",
    ),
    MultiselectorItem(
        "Fast Hints",
        19,
        "Wrinkly will appear faster out of her door. Additionally, pressing A during any text bubble growth will skip to it's fully grown state.",
    ),
    MultiselectorItem(
        "Brighten Mad Maze Maul Enemies",
        -1,
        "Enemies in Mad Maze Maul will be at full brightness, making them easier to see in dark areas.",
    ),
    MultiselectorItem(
        "Raise Fungi Dirt Patch",
        -1,
        "The Fungi Dirt Patch near the mill that was discovered in 2017 is slightly raised to make it visible.",
    ),
    MultiselectorItem(
        "Global Instrument",
        21,
        "Instrument Energy has been changed to be made global, to align it with the behavior of Ammo, Oranges and other consumables.",
    ),
    MultiselectorItem("Fast Pause Transitions", 22, "Pause Menu transitions are greatly sped up."),
    MultiselectorItem(
        "Cannon Game Better Control",
        23,
        "Hold A during the Galleon Cannon Game to reduce the rotation speed of the cannon.",
    ),
    MultiselectorItem(
        "Better Fairy Camera",
        -1,
        "Fairy camera range has been increased, and the wall check has been removed to improve ease of taking photos.",
    ),
    MultiselectorItem("Remove Enemy Cabin Timer", 24, "Removes the enemy 5-Door Cabin timer in Crystal Caves."),
    MultiselectorItem(
        "Remove Galleon Ship Timers",
        6,
        "The gates to the two shipwrecks in Galleon will be permanently opened after activating their respective switches.",
    ),
    MultiselectorItem(
        "Japes Bridge Permanently Extended",
        2,
        "The spiral bridge around Japes Mountain will be permanently extended as soon as you shoot the peanut switch.",
    ),
    MultiselectorItem("Move Spring Cabin Rocketbarrel", -1, "Moves the rocketbarrel in the Spring 5-Door Cabin to prevent being able to enter it earlier than intended."),
]
RemovedBarrierItems = [
    MultiselectorItem(
        "Japes Coconut Gates",
        5,
        "The gates that block the tunnels from Japes main to its various tunnels will be opened.",
    ),
    MultiselectorItem("Japes Shellhive Gate", 6, "The gate to the shellhive area in Japes is opened."),
    MultiselectorItem("Aztec Tiny Temple Ice", -1, "The ice in Tiny Temple is pre-melted."),
    MultiselectorItem("Aztec Tunnel Door", 7, "The door which blocks access to the back half of Aztec will be opened."),
    MultiselectorItem("Aztec 5DTemple Switches", 0, "The switches on the Five-Door Temple in Aztec will be pre-spawned."),
    MultiselectorItem("Aztec Llama Switches", 13, "The switches on the Llama Temple in Aztec will be pre-spawned."),
    MultiselectorItem("Factory Production Room", 1, "The production room in Factory will be turned on."),
    MultiselectorItem(
        "Factory Testing Gate",
        8,
        "The gate from the starting area of Factory to the Block Tower tunnel will be opened.",
    ),
    MultiselectorItem("Galleon Lighthouse Gate", 9, "The gate from the start of Galleon to the lighthouse portion will be opened."),
    MultiselectorItem("Galleon Shipyard Area Gate", 12, "The gate from the start of Galleon to the shipyard portion will be opened."),
    # MultiselectorItem("Galleon Shipwreck Gates", 4, "The gates to the two shipwrecks in Galleon will be permanently opened after activating their respective switches."),
    MultiselectorItem("Galleon Seasick Ship", 2, "The seasick ship in the lighthouse side of Galleon will be spawned."),
    MultiselectorItem("Galleon Treasure Room", -1, "The gate to treasure room in Galleon will be opened."),
    MultiselectorItem("Forest Green Tunnel", 10, "The green tunnel at the start of Forest will have it's gates opened."),
    MultiselectorItem("Forest Yellow Tunnel", 11, "The yellow tunnel to the owl tree area will have it's gate opened."),
    MultiselectorItem("Caves Igloo Pads", 3, "The pads to gain access to the five igloo rooms in Caves will be spawned."),
    MultiselectorItem("Caves Ice Walls", -1, "The various ice walls in Caves will be removed."),
    MultiselectorItem("Castle Crypt Doors", -1, "The various doors in the crypt area of Creepy Castle will be removed."),
]
FasterCheckItems = [
    MultiselectorItem("Factory Toy Monster Fight", -1, "The toy monster fight in Factory will remove the initial enemy killing phase."),
    MultiselectorItem(
        "Factory Piano Game",
        0,
        "The piano game in Factory will only require the 3, 5 and 7 long sequences to be recalled.",
    ),
    MultiselectorItem("Factory Diddy RnD", 1, "Only one enemy wave will need to be completed in the pincode room."),
    MultiselectorItem(
        "Factory Arcade Round 1",
        3,
        "The item for beating Round 1 will be stored inside the Baboon Blast course instead.",
    ),
    MultiselectorItem("Factory Car Race", -1, "The race will be shortened to 1 lap, instead of 2."),
    MultiselectorItem("Galleon Seal Race", -1, "The race will be shortened to 1 lap, instead of 2."),
    MultiselectorItem("Galleon Mech Fish", 2, "You will only need to shoot each target once, instead of 3 times."),
    MultiselectorItem("Forest Mill Conveyor", -1, "The lever combination will consist of only 3 numbers instead of 5."),
    MultiselectorItem("Forest Owl Race", -1, "The owl race will only require you to fly through 8 rings instead of 16."),
    MultiselectorItem(
        "Forest Rabbit Race",
        4,
        "You will only be tasked with beating the 2nd rabbit race. Beating that race will give you both the reward for the 1st and 2nd races.",
    ),
    MultiselectorItem("Caves Ice Tomato Minigame", -1, "The tile flip minigame will only have a 30 second timer, instead of 60."),
    MultiselectorItem("Castle Minecart", 5, "The Minecart ride will end once you reach the turnaround point on the track."),
    MultiselectorItem("Castle Car Race", -1, "The race will be shortened to 1 lap, instead of 2."),
    MultiselectorItem("Jetpac", -1, "Getting the rareware coin reward will only require 2500 points, instead of 5000."),
    MultiselectorItem(
        "Arcade",
        6,
        "DK Arcade will only consist of 2 screens rather than 4, with 75m being an excluded screen from appearing in the first two.",
    ),
]


def parseMultiselector(items: list[MultiselectorItem]) -> list:
    """Parse a list of multiselector items and feed them into a selector list of dictionaries."""
    lst = []
    for item in items:
        lst.append(
            {
                "name": item.name,
                "value": item.name.lower().replace(" ", "_"),
                "tooltip": item.tooltip,
                "shift": item.shift,
            }
        )
    return lst


cb_levels = {
    Levels.JungleJapes: "Jungle Japes",
    Levels.AngryAztec: "Angry Aztec",
    Levels.FranticFactory: "Frantic Factory",
    Levels.GloomyGalleon: "Gloomy Galleon",
    Levels.FungiForest: "Fungi Forest",
    Levels.CrystalCaves: "Crystal Caves",
    Levels.CreepyCastle: "Creepy Castle",
    Levels.DKIsles: "DK Isles",
}

CBRandoSelector = [
    {
        "name": name,
        "value": lvl.name,
        "tooltip": name,
        "shift": -1,
    }
    for lvl, name in cb_levels.items()
]

QoLSelector = parseMultiselector(QoLItems)
RemovedBarrierSelector = parseMultiselector(RemovedBarrierItems)
FasterCheckSelector = parseMultiselector(FasterCheckItems)
