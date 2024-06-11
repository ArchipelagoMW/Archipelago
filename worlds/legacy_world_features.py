# This file triggers various "legacy modes" for worlds, so that breaking changes
# can be made without needing to simultaneously update or break every exisitng
# world. Authors of worlds listed here should remove their worlds when they have
# time to update them to the new behavior.

from Options import PerGameCommonOptions
from worlds.AutoWorld import AutoWorldRegister

# # Option docstring format
#
# These worlds still use the old-style plain text Option docstrings. All other
# worlds' Option docstrings are parsed as reStructuredText (the standard Python
# docstring format) and rendered as HTML in the WebHost.
for world_name in [
    "Adventure", "A Hat in Time", "A Link to the Past", "Aquaria", "ArchipIDLE", "A Short Hike",
    "Blasphemous", "Bomb Rush Cyberfunk", "Bumper Stickers", "Castlevania 64", "Celeste 64",
    "ChecksFinder", "Clique", "Dark Souls III", "DLCQuest", "Donkey Kong Country 3", "DOOM 1993",
    "DOOM II", "Factorio", "Final Fantasy", "Final Fantasy Mystic Quest", "Heretic",
    "Hollow Knight", "Hylics 2", "Kingdom Hearts 2", "Kirby's Dream Land 3",
    "Landstalker - The Treasures of King Nole", "Lufia II Ancient Cave",
    "Mario & Luigi Superstar Saga", "MegaMan Battle Network 3", "Meritous", "Minecraft",
    "Muse Dash", "Noita", "Ocarina of Time", "Overcooked! 2", "Pokemon Emerald",
    "Pokemon Red and Blue", "Raft", "Risk of Rain 2", "Rogue Legacy", "Secret of Evermore",
    "Shivers", "Slay the Spire", "SMZ3", "Sonic Adventure 2 Battle", "Starcraft 2",
    "Stardew Valley", "Subnautica", "Sudoku", "Super Mario 64", "Super Mario World",
    "Super Metroid", "Terraria", "The Legend of Zelda", "The Messenger", "The Witness",
    "Timespinner", "TUNIC", "Undertale", "VVVVVV", "Wargroove", "Yoshi's Island", "Yu-Gi-Oh! 2006",
    "Zillion"
]:
    common_options = set(option for option in PerGameCommonOptions.type_hints.values())
    world = AutoWorldRegister.world_types[world_name]
    for option in world.options_dataclass.type_hints.values():
        if option not in common_options:
            option.plain_text_doc = True
