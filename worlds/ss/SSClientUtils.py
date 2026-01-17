# dAcPy_c::LINK
LINK_PTR = 0x8057578C

# This address is used to check/set the player's health for DeathLink.
CURR_HEALTH_ADDR = 0x8095A76A  # HALFWORD

# Link's state- make sure he is not in a loading zone
# fBase_c::actor_list.mpLast
CURR_STATE_OFFSET = 0x59

# Link's action - make sure he is in a "normal" action (i.e. idle, moving on the ground, etc.)
# dAcPy_c::mCurrentAction
LINK_ACTION_OFFSET = 0x36F

MAX_SAFE_ACTION = 0xD
ITEM_GET_ACTION = 0x78
SWIM_ACTIONS = [0x4F, 0x50, 0x51, 0x52]

DEMISE_STAGE = "B400"
BEEDLE_STAGE = "F002r"

# Location indices for Beedle checks (used for scouting their items)
BEEDLE_LEFTMOST_CHECKS = [41, 42, 43]
BEEDLE_LEFT_MIDDLE_CHECKS = [44, 45]
BEEDLE_RIGHT_MIDDLE_CHECKS = [46, 47, 48]
BEEDLE_RIGHTMOST_CHECKS = [49, 50]
BEEDLE_CHECKS = (
    BEEDLE_LEFTMOST_CHECKS,
    BEEDLE_LEFT_MIDDLE_CHECKS,
    BEEDLE_RIGHT_MIDDLE_CHECKS,
    BEEDLE_RIGHTMOST_CHECKS
)

MINIGAME_STATE_ADDR = 0x80572250

# The byte at this address stores which save file is currently selected (0 indexed)
SELECTED_FILE_ADDR = 0x8095FC98

# The expected index for the following item that should be received. Array of 2 bytes right after the give item array
# Uses an unused scene index which is 16 bytes wide
EXPECTED_INDEX_ADDR = 0x80956F28 # HALFWORD
# WILL BE UPDATED WHEN THE BUILD IS RELEASED

# This address contains the current stage ID.
CURR_STAGE_ADDR = 0x805B388C  # STRING[16]

# This is an array of length 0x10 where each element is a byte and contains item IDs for items to give the player.
# 0xFF represents no item. The array is read and cleared every frame.
ARCHIPELAGO_ARRAY_ADDR = 0x80678770 # ARRAY[16]
# WILL BE UPDATED WHEN THE BUILD IS RELEASED

# This is the address that holds the player's file name.
FILE_NAME_ADDR = 0x80955D38  # ARRAY[16]

# A bit at this address is set if on the title screen
GLOBAL_TITLE_LOADER_ADDR = 0x80575780

# An array at the address pointed to here holds text to be displayed by the game
CLIENT_TEXT_BUFFER_PTR = 0x8005526C # Pointer to STRING[512]
CLIENT_TEXT_BUFFER_SIZE = 512

# Time for a client message to disappear in-game (in seconds, not including stagger time for multiple lines in the queue)
CLIENT_TEXT_TIMEOUT = 6

# Max number of characters in a line for in-game client text
INGAME_LINE_LENGTH = 64

AP_VISITED_STAGE_NAMES_KEY_FORMAT = "ss_visited_stages_%i"

LINK_INVALID_STATES = [
    b'\x00\x00\x00',
    b'\x5A\x2C\x88', # Loading zone
    b'\x5A\x32\x8C', # Door / talking to Bird Statue
    # b'\x5A\x27\x20', # Calling Fi
    b'\xB4\xF4\x50', # Bird picking up link
    # b'\xB7\xA6\x7C', # Bed dialogue option
    b'\x5A\x31\xAC', # Sleeping
    b'\x5A\x33\x6C', # Waking up
    b'\x97\x96\xBC', # Load transition maybe?
]

# Valid addresses for storyflags (ending in zero - final bit is added to this address)
VALID_STORYFLAG_ADDR = [
    0x805A9AD0,
    0x805A9AE0,
    0x805A9AF0,
    0x805A9B00,
    0x805A9B10,
    0x805A9B20,
    0x805A9B30,
]

# Address for the sceneflags for the current stage
CURR_STAGE_SCENEFLAG_ADDR = 0x805A78D0

# Addresses to the sceneflags saved on the current save file
STAGE_TO_SCENEFLAG_ADDR = {
    "Skyloft": 0x80956EC8,
    "Faron Woods": 0x80956ED8,
    "Lake Floria": 0x80956EE8,
    "Flooded Faron Woods": 0x80956EF8,
    "Eldin Volcano": 0x80956F08,
    "Boko Base/Volcano Summit": 0x80956F18,
    "Lanayru Desert": 0x80956F38,
    "Lanayru Sand Sea": 0x80956F48,
    "Lanayru Gorge": 0x80956F58,
    "Sealed Grounds": 0x80956F68,
    "Skyview": 0x80956F78,
    "Ancient Cistern": 0x80956F88,
    "Earth Temple": 0x80956FA8,
    "Fire Sanctuary": 0x80956FB8,
    "Lanayru Mining Facility": 0x80956FD8,
    "Sandship": 0x80956FE8,
    "Sky Keep": 0x80957008,
    "Sky": 0x80957018,
    "Faron Silent Realm": 0x80957028,
    "Eldin Silent Realm": 0x80957038,
    "Lanayru Silent Realm": 0x80957048,
    "Skyloft Silent Realm": 0x80957058,
}

# Used for batch lookup
STORYFLAG_START_ADDR = 0x805A9AD8
SCENEFLAG_START_ADDR = 0x80956EC8

# Boolean used by the patched game to determine whether to use networking & display network info
NETWORK_USAGE_BOOL = 0x80686871 # Be sure to update if the patcher ever changes something in the assembly!

# DME Connection Messages for the client
CONNECTION_REFUSED_GAME_STATUS = "Dolphin failed to connect. Please load a randomized ROM for Skyward Sword. Trying again in 5 seconds..."
CONNECTION_REFUSED_SAVE_STATUS = "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
CONNECTION_LOST_STATUS = "Dolphin connection was lost. Please restart your emulator and make sure Skyward Sword is running."
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."

CONSOLE_CONNECTED_STATUS = "Wii connected successfully."
