from Overcooked2Levels import Overcooked2Level

overcooked_regions = [
    ("Menu", ["New Game"]),
    ("World Map", [level.level_name() for level in Overcooked2Level()]),
]

for level in Overcooked2Level():
    if (level.level_name() == "6-6"):
        overcooked_regions.append(
            (
                level.level_name(),
                ["Level Exit", "Credits"]
            )
        )
    else:
        overcooked_regions.append(
            (
                level.level_name(),
                ["Level Exit"]
            )
        )

mandatory_connections = [
    ("New Game", "World Map"),
    ("Level Exit", "World Map"),
]

default_connections = [

]

illegal_connections = {
    
}