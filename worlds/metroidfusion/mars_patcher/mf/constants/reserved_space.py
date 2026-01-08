class ReservedConstantsMF:
    """
    These are constants that are in the patches 'Reserved Space';
    things that are intended to be modified by this patcher.
    """

    # These need to be kept in sync with the base patch
    # found somewhere around https://github.com/MetroidAdvRandomizerSystem/MARS-Fusion/blob/main/src/main.s#L45

    # Pointers, offset by language value, that store the message table location
    MESSAGE_TABLE_LOOKUP_ADDR = 0x79CDF4
    FIRST_CUSTOM_MESSAGE_ID = 0x39  # The first 0x38 messages are reserved for standard messages

    PATCHER_FREE_SPACE_ADDR = 0x7D0000
    PATCHER_FREE_SPACE_END = PATCHER_FREE_SPACE_ADDR + 0x20000
    MINOR_LOCS_TABLE_ADDR = 0x7FF000
    MINOR_LOCS_ARRAY_ADDR = 0x7FF004
    MAJOR_LOCS_POINTER_ADDR = 0x7FF008
    TANK_INC_ADDR = 0x7FF00C
    TOTAL_METROID_COUNT_ADDR = 0x7FF010
    REQUIRED_METROID_COUNT_ADDR = 0x7FF010
    STARTING_LOCATION_ADDR = 0x7FF014
    CREDITS_END_DELAY_ADDR = 0x7FF018  # TODO: Is this meant to be changed?
    CREDITS_SCROLL_SPEED_ADDR = 0x7FF018  # + 2 TODO: Ditto
    HINT_SECURITY_LEVELS_ADDR = 0x7FF01C
    ENVIRONMENTAL_HARZARD_DAMAGE_ADDR = 0x7FF020  # TODO: Implement this
    MISSILE_LIMIT_ADDR = 0x7FF024
    ROOM_NAMES_TABLE_ADDR = 0x7FF028
    REVEAL_HIDDEN_TILES_ADDR = 0x7FF02C
    TITLESCREEN_TEXT_POINTERS_POINTER_ADDR = 0x7FF030
    DEFAULT_STEREO_FLAG_POINTER_ADDR = 0x7FF034
