# Words that are auto-unlocked when using the "start with default words" option
DEFAULT_WORDS = ("Baba", "Is", "You", "Flag", "Win", "Wall", "Stop", "Rock", "Push")

# List of progression words prior to ???
EARLY_PROG_WORDS = ("Sink", "Skull", "Defeat", "Lava", "And",
                    "Star", "Crab", "Keke", "Love", "Move",
                    "Pillar", "Jelly", "Key", "Open", "Door",
                    "Shut", "Belt", "Shift", "End", "Rose",
                    "Red", "Violet", "Blue", "Water", "Float",
                    "Text", "Robot", "Bolt", "Hot", "Cog",
                    "Weak", "Has", "Box", "Melt", "Ghost",
                    "Tele", "Pull", "Ice", "Leaf", "Fence",
                    "Not", "Me", "Tree", "Up", "Right",
                    "Bug", "Fungus", "Swap", "Empty", "Cloud",
                    "Rocket", "UFO", "Moon", "Fall", "Dust",
                    "On", "Grass", "Make", "Hand", "Fruit",
                    "All", "More", "Word", "Sleep", "Bat",
                    "Group", "Fire", "Facing", "Lonely", "Bird",
                    "Sun", "Tile")

# List of progression words past the top gate and prior to ???
TOP_GATE_PROG_WORDS = ("Level", "Orb", "Hide", "Bonus")

# List of progression words in ??? + ABC
FLOWER_PROG_WORDS = ("Write", "A", "AB", "B", "BA", "C", "E", "G", "H", "L", "M", "N", "O", "R", "S", "T", "V", "W")

# List of progression words in Depths
DEPTHS_PROG_WORDS = ("Hedge",)

# List of progression words in Meta
META_PROG_WORDS = ("Near", "Cursor", "I")

# List of progression words in Center (The End and Gallery only)
CENTER_PROG_WORDS = ("Cake", "Done", "Image")

# All filler words
ALL_FILLER_WORDS = ("Anni", "Best", "Down", "Left", "Cliff", "Line", "F", "U", "X")

# All progression words
ALL_PROG_WORDS = DEFAULT_WORDS + EARLY_PROG_WORDS + TOP_GATE_PROG_WORDS + FLOWER_PROG_WORDS + DEPTHS_PROG_WORDS + META_PROG_WORDS + CENTER_PROG_WORDS

# Every single word, including both progression and filler
ALL_WORDS = ALL_PROG_WORDS + ALL_FILLER_WORDS

# Function to get the current progression words given the area access
def get_curr_prog_words(area_access):
    curr_prog_words = DEFAULT_WORDS + EARLY_PROG_WORDS
    if area_access <= 1:
        curr_prog_words += TOP_GATE_PROG_WORDS
    if area_access <= 2:
        curr_prog_words += FLOWER_PROG_WORDS
    if area_access <= 3:
        curr_prog_words += DEPTHS_PROG_WORDS
    if area_access <= 4:
        curr_prog_words += META_PROG_WORDS
    return curr_prog_words