from enum import Enum, IntEnum

GAME = "Tomba!"

INVENTORY_STACK_SIZE = 0xFF

# See 8002959c for the check
MAX_LIVES = 99

VICTORY = "Victory"
VILLAGE_OF_ALL_BEGINNINGS_FOG_DISSIPATED = "Village Of All Beginnings Fog Dissipated"


class Locations(str):
    AP_150_000 = "150,000 AP"
    MAILBOX = "Mailbox"


class Regions(str):
    BACCUS_LAKE = "Baccus Lake"
    BACCUS_VILLAGE = "Baccus Village"
    CENTRAL_PARK = "Central Park"
    CHARITY_SQUARE = "Charity Square"
    CLOCK_TOWER = "Clock Tower"
    # DWARF_FOREST = "Dwarf Forest" # Rather a group of regions
    DWARF_JAIL = "Dwarf Jail"
    DWARF_VILLAGE = "Dwarf Village"
    FOREST_OF_100_FLOWERS = "Forest Of 100 Flowers"
    FOREST_OF_ALL_BEGINNINGS = "Forest Of All Beginnings"
    HAUNTED_MANSION = "Haunted Mansion"
    HIDDEN_VILLAGE = "Hidden Village"
    IRON_CASTLE = "Iron Castle"
    LAVA_CAVES = "Lava Caves"
    LUMBERJACK_FACTORY = "Lumberjack Factory"
    MANSION = "Mansion"
    MASAKARI_JUNGLE = "Masakari Jungle"
    MUSHROOM_FOREST = "Mushroom Forest"
    OL_POND = "Ol' Pond"
    OLD_TREE_HILL = "Old Tree Hill"
    PHOENIX_MOUNTAIN = "Phoenix Mountain"
    PHOENIXS_NEST = "Phoenix's Nest"
    STORMY_MOUNTAIN = "Stormy Mountain"
    THE_MERMAIDS_SINGING_ROCK = "The Mermaid's Singing Rock"
    THE_STRANGE_SMALL_ROOM = "The Strange Small Room"
    TRICK_VILLAGE = "Trick Village"
    UNDERGROUND_MAZE = "Underground Maze"
    UNDERGROUND_PRISON = "Underground Prison"
    VILLAGE_OF_ALL_BEGINNINGS = "Village Of All Beginnings"
    VILLAGE_OF_CIVILIZATION = "Village Of Civilization"
    WATCH_TOWER = "Watch Tower"
    WOBBLY_WHARF = "Whobbly Warf"
    Y_CROSSING = "Y-crossing"


class Areas(str):
    BACCUS_LAKE = "Baccus Lake"
    BACCUS_VILLAGE = "Baccus Village"
    DIRT_MOTOCROSS = "Dirt Motocross"
    DEEP_JUNGLE = "Deep Jungle"
    DWARF_FOREST = "Dwarf Forest"
    DWARF_FOREST_PURIFIED = "Dward Forest (Purified)"
    DWARF_VILLAGE = "Dwarf Village"
    EVIL_PIGS = "Evil Pigs"
    HAUNTED_MANSION = "Haunted Mansion"
    HAUNTED_MANSION_PURIFIED = "Haunted Mansion (Purified)"
    MUSHROOM_VILLAGE = "Mushroom Village"
    PHOENIX_MOUNTAIN = "Phoenix Mountain"
    PIG_ISLAND = "Pig Island"
    UNKNOWN = "Unknown"
    VILLAGE_OF_ALL_BEGINNINGS = "Village Of All Beginnings"
    VILLAGE_OF_CIVILIZATION = "Village Of Civilization"
    VILLAGE_OF_CIVILIZATION_PURIFIED = "Village Of Civilization (Purified)"
    CLOCK_TOWER = "Clock Tower"
    IRON_TOWER = "Iron Tower"
    Y_CROSSING = "Y-crossing"


class Sections(str):
    CENTRAL_PARK = "Central Park"
    CHARITY_SQUARE = "Charity Square"
    CLOCK_TOWER = "Clock Tower"
    DWARF_JAIL = "Dwarf Jail"
    FOREST_OF_100_FLOWERS = "Forest Of 100 Flowers"
    FOREST_OF_ALL_BEGINNINGS = "Forest Of All Beginnings"
    HIDDEN_VILLAGE = "Hidden Village"
    HUNDRED_YEAR_OLD_MANS_HUT = "100 Year Old Man's Hut"
    IRON_CASTLE = "Iron Castle"
    LAVA_CAVES = "Lava Caves"
    LUMBERJACK_FACTORY = "Lumberjack Factory"
    MANSION = "Mansion"
    MASAKARI_JUNGLE = "Masakari Jungle"
    MUSHROOM_FOREST = "Mushroom Forest"
    OL_POND = "Ol' Pond"
    OLD_TREE_HILL = "Old Tree Hill"
    PHOENIXS_NEST = "Phoenix's Nest"
    STORMY_MOUNTAIN = "Stormy Mountain"
    THE_MERMAIDS_SINGING_ROCK = "The Mermaid's Singing Rock"
    THE_STRANGE_SMALL_ROOM = "The Strange Small Room"
    TRICK_VILLAGE = "Trick Village"
    UNDERGROUND_MAZE = "Underground Maze"
    UNDERGROUND_PRISON = "Underground Prison"
    VILLAGE_OF_ALL_BEGINNINGS = "Village Of All Beginnings"
    WATCH_TOWER = "Watch Tower"
    WOBBLY_WHARF = "Whobbly Warf"


class Items(str):
    BABY_PIG = "Baby Pig"
    BAKED_YAM = "Baked Yam"
    BANANA_JUICE = "Banana Juice"
    BANANAS = "Bananas"
    BARON = "Baron"
    BIG_KEY = "Big Key"
    BITTING_PLANT_FLOWER = "Bitting Plant Flower"
    BLACK_CANDY = "Black Candy"
    BLACK_WATER = "Black Water"
    BLACKJACK = "Blackjack"
    BLUE_CANDY = "Blue Candy"
    BLUE_EVIL_PIG_BAG = "Blue Evil Pig Bag"
    BLUE_POWDER = "Blue Powder"
    BOMB = "Bomb"
    BOSS_JEWEL = "Boss' Jewel"
    BROKEN_VASE = "Broken Vase"
    BRONZE_MEDAL = "Bronze Medal"
    BUCKET = "Bucket"
    BUCKET_OF_WATER = "Bucket Of Water"
    BUNK_FLOWER = "Bunk Flower"
    BUTAMUSHI_THORN = "Butamushi Thorn"
    CHARITY_WINGS = "Charity Wings"
    CHARLES_PANTS = "Charle's Pants"
    CHEESE = "Cheese"
    CHICK = "Chick"
    CHUCKLING_MUSHROOM = "Chuckling Mushroom"
    COCONUTS = "Coconuts"
    COLD_MEDECINE = "Cold Medecine"
    DASHING_PANTS = "Dashing Pants"
    DIRTY_MIRROR = "Dirty Mirror"
    ELECTRIC_EEL = "Electric Eel"
    FLASH_PANTS = "Flash Pants"
    FLOWER_SEEDS = "Flower Seeds"
    FLOWER_TEARS = "Flower Tears"
    FORBIDDEN_MUSHROOM = "Forbidden Mushroom"
    FROG = "Frog"
    FUEL_BAR = "Fuel Bar"
    FUNGA_DRUM = "Funga Drum"
    FUNGA_LEATHER = "Funga Leather"
    FUNGA_SAP = "Funga Sap"
    FUNGA_TREE = "Funga Tree"
    FUNKY_PARASOL = "Funky Parasol"
    FURIOUS_TORNADO = "Furious Tornado"
    GOLD_CANDY = "Gold Candy"
    GOLD_FLOWER = "Gold Flower"
    GOLD_MEDAL = "Gold Medal"
    GOLDEN_BOWL = "Golden Bowl"
    GOLDEN_FRUIT = "Golden Fruit"
    GOLDEN_LEAF_BUTTERFLY = "Golden Leaf Butterfly"
    GRANDPAS_BRACELET = "Grandpa's Bracelet"
    GRAPPLE = "Grapple"
    GRAPPLEJACK = "GrappleJack"
    GREEN_CANDY = "Green Candy"
    GREEN_EVIL_PIG_BAG = "Green Evil Pig Bag"
    HEALING_HERBS = "Healing Herbs"
    HEALING_MUSHROOM = "Healing Mushroom"
    HUNDRED_YEAR_OLD_BELL = "100 Year Old Bell"
    HUNDRED_YEAR_OLD_KEY = "100 Year Old Key"
    IRON = "Iron"
    IRON_BOOMERANG = "Iron Boomerang"
    IRON_WHEEL = "Iron Wheel"
    ITEM = "Item"
    JEWEL_OF_FIRE = "Jewel Of Fire"
    JEWEL_OF_WATER = "Jewel Of Water"
    JEWEL_OF_WIND = "Jewel Of Wind"
    JUMPING_PANTS = "Jumping Pants"
    KEY_TO_OL_POND = "Key To Ol' Pond"
    KNOWLEDGE_FRUIT = "Knowledge Fruit"
    KOKKA_CLAW = "Kokka Claw"
    LARGE_LUNCH_BOX = "Large Lunch Box"
    LARGE_KEY_PANEL_1 = "Large Key Panel 1"
    LARGE_KEY_PANEL_2 = "Large Key Panel 2"
    LARGE_KEY_PANEL_3 = "Large Key Panel 3"
    LARGE_KEY_PANEL_4 = "Large Key Panel 4"
    LARGE_KEY_PANEL_5 = "Large Key Panel 5"
    LEAF_BUTTERFLY = "Leaf Butterfly"
    LETTER = "Letter"
    LOST_DWARF = "Lost Dwarf"
    LUNCH_BOX = "Lunch Box"
    MAGIC_MIRROR = "Magic Mirror"
    MAP = "Map"
    MATH_BEAD_1 = "Math Bead 1"
    MATH_BEAD_2 = "Math Bead 2"
    MATH_BEAD_3 = "Math Bead 3"
    MATH_BEAD_4 = "Math Bead 4"
    MATH_BEAD_5 = "Math Bead 5"
    MATH_BEAD_6 = "Math Bead 6"
    MATH_BEAD_7 = "Math Bead 7"
    MATH_BEAD_8 = "Math Bead 8"
    MATH_BEAD_9 = "Math Bead 9"
    MATH_BEAD_10 = "Math Bead 10"
    MIGHTY_FISH = "Mighty Fish"
    MIGHTY_FISH_FOOD = "Mighty Fish Food"
    MILLION_YEAR_OLD_BELL = "Million Year Old Bell"
    MILLION_YEAR_OLD_KEY = "Million Year Old Key"
    MINERS_HAT = "Miner's Hat"
    MOLASSES = "Molasses"
    MYSTERIOUS_MUSHROOM = "Mysterious Mushroom"
    NAVY_EVIL_PIG_BAG = "Navy Evil Pig Bag"
    NEEDLEGATOR_TEETH = "Needlegathor Teeth"
    NORMAL_PANTS = "Normal Pants"
    ORANGE_EVIL_PIG_BAG = "Orange Evil Pig Bag"
    ORDINARY_MUSHROOM = "Ordinary Mushroom"
    PINK_EVIL_PIG_BAG = "Pink Evil Pig Bag"
    PIPE = "Pipe"
    PSYCHIC_FISH = "Psychic Fish"
    RAFT = "Raft"
    RAIN_ESSENCE = "Rain Essence"
    RED_CANDY = "Red Candy"
    RED_EVIL_PIG_BAG = "Red Evil Pig Bag"
    RISE_AND_SHINE_POWDER = "Rise And Shine Powder"
    RUBBER_GLOVES = "Rubber Gloves"
    SACRED_FISH = "Sacred Fish"
    SEASHELL_NECKLACE = "Seashell Necklace"
    SEAWEED = "Seaweed"
    SHOVEL = "Shovel"
    SILVER_CANDY = "Silver Candy"
    SILVER_MEDAL = "Silver Medal"
    SILVER_POWDER = "Silver Powder"
    SMALL_KEY = "Small Key"
    STONE_BOOMERANG = "Stone Boomerang"
    STRONG_WIRE = "Strong Wire"
    TEAR_JAR = "Tear Jar"
    TELESCOPE = "Telescope"
    TEN_THOUSAND_YEAR_OLD_BELL = "10,000 Year Old Bell"
    TEN_THOUSAND_YEAR_OLD_KEY = "10,000 Year Old Key"
    THIEFS_WIRE = "Thief's Wire"
    THOUSAND_YEAR_OLD_BELL = "1,000 Year Old Bell"
    THOUSAND_YEAR_OLD_KEY = "1,000 Year Old Key"
    THREE_CRYSTAL_BALLS = "Three Crystal Balls"
    TORCH = "TORCH"
    TORN_MAP_1 = "Torn Map 1"
    TORN_MAP_2 = "Torn Map 2"
    UNUSUAL_KEY = "Unusual Key"
    WEED_KILLER = "Weed Killer"
    WEEPING_MUSHROOM = "Weeping Mushroom"
    WHAT_THE_THIEF_FORGOT = "What The Thief Forgot"
    WHAT_THE_THIEF_LOST = "What The Thief Lost"
    WINE = "Wine"
    WOOD = "Wood"
    WOOD_BOOMERANG = "Wood Boomerang"
    YANS_LUNCH_BOX = "Yan's Lunch Box"
    YELLOW_EVIL_PIG_BAG = "Yellow Evil Pig Bag"


class Events(str):
    A_DRINK_FOR_GROWNUPS = "A Drink for Grownups"
    A_FAMILIAR_LOOKING_MANSION = "A Familiar Looking Mansion"
    A_HUNGRY_MONKEY = "A Hungry Monkey"
    A_LARGE_KEY_HOLE = "A Large Key Hole!"
    A_LOST_CHILD = "A Lost Child"
    A_MAGIC_MIRROR = "A Magic Mirror?"
    A_MANS_BEST_FRIEND = "A Man's Best Friend"
    A_PRECIOUS_TREASURE_CHEST = "A Precious Treasure Chest?"
    A_REAL_EVIL_PIG = "A Real Evil Pig"
    A_REFRESHING_DRING = "A Refreshing Drink"
    A_SAFE_MUSHROOM = "A Safe Mushroom?"
    A_SMALL_KEY_HOLE = "A Small Key Hole!"
    A_STORMY_PIG_BAG = "A Stormy Pig Bag"
    BACCUS_VILLAGE = "Baccus Village"
    BARONS_STRENGTH = "Baron's Strength"
    BEGINNERS_DWARF_LANGUAGE = "Beginner's Dwarf Language"
    BITTING_PLANT_FLOWER = "Bitting Plant Flower"
    BLUE_HIDDEN_POWERS = "Blue Hidden Powers"
    BREAK_THE_MAGIC_EGG = "Break the Magic Egg!"
    BREAK_THE_RUSTY_DOOR = "Break the Rusty Door!"
    CANT_STOP_CRYING = "Can't Stop Crying"
    CHARLES_PANTS = "Charles' Pants"
    CLEAR_THE_FOG = "Clear the Fog"
    CRY_BABY = "Cry Baby"
    DEATH_FRUIT_JUICE = "Death Fruit Juice"
    DELICIOUS_KNOWLEDGE_FRUIT = "Delicious Knowledge Fruit"
    DIG_LIKE_A_MOLE = "Dig Like a Mole"
    DWARF_ELDER = "Dwarf Elder"
    GRANDPAS_BRACELET = "Grandpa's Bracelet"
    FIND_CHARLES = "Find Charles!"
    FLOWER_SEEDS = "Flower Seeds"
    FOOD_FOR_FUEL = "Food for Fuel?"
    GREEN_HIDDEN_POWERS = "Green Hidden Powers"
    HEALING_HERBS_FOR_BARON = "Healing Herbs for Baron"
    HIDE_AND_GO_SEEK = "Hide and Go Seek"
    I_CANT_SWIM = "I Can't Swim..."
    I_NEED_A_BOMB = "I Need a Bomb"
    I_NEED_A_TEAR_BOTTLE = "I Need a Tear Bottle"
    I_WANT_A_BRONZE_MEDAL = "I Want a Bronze Medal"
    I_WANT_A_SILVER_MEDAL = "I Want a Silver Medal"
    I_WANT_A_GOLD_MEDAL = "I Want a Gold Medal"
    IM_SO_HUNGRY = "I'm So Hungry"
    INSIDE_THE_KOKKA_EGGS = "Inside the Kokka Eggs"
    LAVA_CAVES = "Lava Caves"
    LEAF_BUTTERFLIES = "Leaf Butterflies"
    LEAF_SLIDER = "Leaf Slider"
    LETS_MAKE_CANDY = "Let's Make Candy!"
    LETS_RIDE_THE_RAFT = "Let's Ride the Raft!"
    LOOK_AND_SEE = "Look and See?!"
    LOST_AND_FOUND = "Lost and Found"
    MIGHTY_FISH_FOOD = "Mighty Fish Food"
    MILLION_YEAR_OLD_WISH = "Million Year Old Wish"
    MONSTER_HUNT = "Monster Hunt"
    MOTOCROSS_COURSE = "Motocross Course"
    PAINTING_OF_A_BIG_KEY = "Painting of a Big Key?"
    PEACH_FLOWER_GAS = "Peach Flower Gas"
    PHOENIX_MOUNTAIN = "Phoenix Mountain"
    PLANT_A_FLOWER_GARDEN = "Plant a Flower Garden"
    POWER_UP_FOR_TOOLS = "Power Up for Tools!?"
    READY_SET_GO = "Ready, Set, Go!"
    RED_BLUE = "Red + Blue = ?"
    RED_HIDDEN_POWERS = "Red Hidden Powers"
    ROAD_TO_BACCUS_LAKE = "Road to Baccus Lake"
    SAVE_THE_DWARVES = "Save the Dwarves"
    SEAWEED_FOR_YOUR_HEALTH = "Seaweed for Your Health"
    SEVEN_FRIENDS = "Seven Friends"
    SMILE = "Smile!"
    SOME_CHEESE_PLEASE = "Some Cheese Please"
    SOMETHINGS_COOKIN = "Something's Cookin'?"
    SOURCE_OF_EVIL_MAGIC = "Source of Evil Magic"
    STOP_THE_FIGHT = "Stop the Fight!"
    TAKE_ME_HOME = "Take Me Home"
    TAKE_OUT = "Take Out"
    TAKE_TWO_OF_THESE = "Take Two of These"
    TALE_OF_THE_EVIL_PIGS = "Tale of the Evil Pigs"
    TEARS_FROM_A_FLOWER = "Tears from a Flower"
    THE_AP_BOX = "The AP Box"
    THE_BLUE_FORTUNE_TELLER = "The Blue Fortune Teller"
    THE_BOSS_TREASURE = "The Boss' Trasure"
    THE_BROKEN_FOUNTAIN = "The Broken Fountain"
    THE_CIVILIZATION_MACHINE = "The Civilization Machine"
    THE_CUTE_WITCH = "The Cute Witch"
    THE_DEEP_JUNGLE_PIG = "The Deep Jungle Pig"
    THE_EVIL_PIG_BAG = "The Evil Pig Bag"
    THE_FAMOUS_DIGGER = "The Famous Digger"
    THE_FIRE_PIG_BAG = "The Fire Pig Bag"
    THE_FLOWER_TOWER = "The Flower Tower"
    THE_GREAT_ESCAPE = "The Great Escape"
    THE_HAUNTED_MANSION = "The Haunted Mansion"
    THE_HAUNTED_PIG_BAG = "The Haunted Pig Bag"
    THE_JUNGLE_PIG_BAG = "The Jungle Pig Bag"
    THE_MASTER_OF_THE_SKIES = "The Master of the Skies"
    THE_MERMAIDS_NECKLACE = "The Mermaid's Necklace"
    THE_MERMAIDS_SINGING_ROCK = "The Mermaid's Singing Rock"
    THE_MOUSE_PIG_BAG = "The Mouse Pig Bag"
    THE_MYSTERIOUS_MUSHROOM = "The Mysterious Mushroom"
    THE_PHOENIXS_FAVORITE = "The Phoenix's Favorite"
    THE_PUMPS_ROCKS = "The Pump Rocks"
    THE_RED_FORTUNE_TELLER = "The Red Fortune Teller"
    THE_THIEFS_DOOR = "The Thief's Door"
    THE_TROUBLED_THIEF = "The Troubled Thief"
    THE_UNDERWATER_PIG_BAG = "The Underwater Pig Bag"
    THE_WORLDS_GREATEST_POUT = "The World's Greatest Pout?"
    THE_WORLDS_GREATEST_SMILE = "The World's Greatest Smile!"
    THE_5_GOLDEN_ITEMS = "The 5 Golden Items"
    THE_8TH_EVIL_PIG_BAG = "The 8th Evil Pig Bag?"
    THE_10_MATH_BEADS = "The 10 Math Beads"
    THE_100_FLOWER_FOREST = "The 100 Flower Forest"
    THE_100_YEAR_OLD_WISE_MAN = "The 100 Year Old Wise Man"
    THE_1000_YEAR_OLD_MAN = "The 1,000 Year Old Man?"
    THE_10000_YEAR_OLD_MAN = "The 10,000 Year Old Man"
    TO_PHOENIX_MOUNTAIN = "To Phoenix Mountain..."
    TREASURES_FROM_THE_MANSION = "Treasures from the Mansion?"
    TREE_OF_KNOWLEDGE_KNOWS = "Tree of Knowledge Knows"
    TRICK_VILLAGE = "Trick Village"
    UNBREAKABLE_WIRE = "Unbreakable Wire"
    UNDERGROUND_TREASURE = "Underground Treasure"
    WE_NEED_POWER = "We Need Power..."
    WHAT_IS_THIS = "What is this?"
    WHAT_THE_THIEF_FORGOT = "What the Thief Forgot"
    WHAT_THE_WITCH_LOST = "What the Witch Lost..."
    WHATS_A_FUNGA = "What's a Funga?"
    WHATS_UNDER_THE_FOREST = "What's Under the Forest?"
    WHATS_UNDERWATER = "What's Underwater?"
    WHEN_THE_WIND_DIES_DOWN = "When the Wind Dies Down..."
    WHERE_DID_I_COME_FROM = "Where did I come from?"
    WHERE_THE_BARREL_ROLLS = "Where The Barrel Rolls..."
    WHERED_THE_LIGHTS_GO = "Where'd the Lights Go?"
    WHERES_THE_BABY_MOUSE = "Where's the Baby Mouse?"
    WHO_ARE_YOU = "Who are You?"


class EventStatus(IntEnum):
    """Status of in-game events"""

    UNDISCOVERED = 0x00
    STARTED = 0x01
    CLEARED = 0xFF


class MenuState(IntEnum):
    OPEN = 0x01
    CLOSED = 0x00


class GameState(Enum):
    UNKNOWN = 0
    IN_MENU = 1
    NO_HUD = 2
    PLAYING = 3
    CUTSCENE = 4


class HudState(IntEnum):
    HIDDEN = 0x00
    VISIBLE = 0x01


class SFX(IntEnum):
    """RAM code associated with each SFX"""

    ACQUIRED = 0x0A
    LAUGH = 0x20
    CRY = 0x25
    EVENT_STARTED = 0x2A
    FART = 0x32


class Addresses(IntEnum):
    """List of usefull ROM addresses"""

    GAME_ID = 0x009244

    # ??? = 0x09BC98

    AP_SCORE = 0x09BCD4

    LIVES = 0x09BCE8  # Shown amount = Stored - 1

    CREDITS_VISIBILITY = 0x09BCC8
    SHOW_FOG = 0x09BCCE  # Also determines if can use FURIOUS TORNADO OR NOT

    MAILBOX_STATE = 0x09BCEC

    EVENT_FLAGS = 0x09C10C

    # Items count are given in order: base address + item ID is item count for that item
    INVENTORY_ITEM_AMOUNT = 0x09C40C
    INVENTORY_STACK = 0x09C50C

    # Memorize which is the last received index from Archipelago that was dispatched to player (2 bytes)
    ARCHIPELAGO_RECEIVED_INDEX = 0x09C50A

    INVENTORY_COUNTER = 0x09C60C
    UI_REFRESH_FLAG = 0x09C60E

    EQUIPED_WEAPON_ID = 0x09C61A
    EQUIPED_PANTS_ID = 0x09C61B

    HUD_VISIBILITY = 0x0B0770
    HUD_VISIBILITY_TIMER = 0x0B0774

    PV_MAX = 0x09BCD9
    PV_CURRENT = 0x09BCD8

    MENU_STATE = 0x1F8001C6

    I_STAT = 0x1F801070
    I_MASK = 0x1F801074

    # Addresses for items found in game stack
    FOUND_ITEMS_STACK_SIZE = 0xB400
    FOUND_ITEMS_STACK = 0xB401

    # Where we put the sound to be played
    IS_PATCHED = 0xB13F
    PLAY_SFX = 0xB140
    MESSAGE = 0xB142

    # Send command to the custom handler
    CUSTOM_COMMAND = 0xB141

    PATCH_INTERFACE_HANDLER = 0xB150
    PATCH_INTERFACE_HOOK = 0x01E110
    PATCH_ADD_ITEM = 0x0297B0

    CAMERA_HORIZONTAL_OFFSET = 0x1F8000EC  # 2bytes, Left: 0xA0
    CAMERA_VERTICAL_OFFSET = 0x1F8000F0  # 2bytes, Bottom: 0xFF88

    PIPE_STATE = 0x09C269
    GOLD_FLOWER_STATE = 0x09C34C
    GOLDEN_BOWL_STATE = 0x09C3E7
    BITTING_PLANT_FLOWER_STATE = 0x09C3E3

    VILLAGE_OF_ALL_BEGINNING_EVENT_CONTROL = 0x09BCEC

    SELECTED_AREA = 0x09BCC8
    SELECTED_SECTION = 0x9BCCA

    SECTION_STATE = 0x09BCFC  # Bit flag for each item/object taken/broken


class SectionEventMask(IntEnum):
    SECTION_1_BITTING_FLOWER_BLUE_APPLE = 0x20  # Byte 0


class EventControlState(IntEnum):
    NOT_DONE = 0x00
    DONE = 0x01


class EventControlMask(IntEnum):
    ANIMAL_DASH = 0x40
    MAILBOX_OPENNED = 0x01


class BittingPlantFlowerState(IntEnum):
    NORMAL = 0x00
    BLOOM = 0x01
    GRABBED = 0x02


class MailboxState(IntEnum):
    CLOSED = 0x00
    OPENNED = 0x01  # Tornado no longer there


class CustomCommand(IntEnum):
    """Masks for custom commands"""

    CLEAR_STACK = 0x00000001  # Bit 0 R/W = 1: Clear stack, stack is being cleared
    SHOW_MESSAGE = 0x00000010  # Bit 1 R/W = 1: Display info message (B142 and B143)
