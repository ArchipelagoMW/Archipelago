from enum import Enum, IntEnum

class LocationType(Enum):
    CHEST = "Chest"
    """Location checked by opening a chest."""
    NPC_REWARD = "NPC Reward"
    """Location checked by talking to an NPC or stepping on an item tile."""
    LAIR = "Lair"
    """Location checked by sealing a monster lair."""

class RuleFlag(Enum):
    NONE = "NONE"
    """No special requirement preventing access."""
    CAN_CUT_METAL = "CAN_CUT_METAL"
    """Requires a way to damage metal enemies (Zantestu Sword|Soul Blade)."""
    CAN_CUT_SPIRIT = "CAN_CUT_SPIRIT"
    """Requires a way to damage metal enemies (Spirit Sword|Soul Blade)."""
    HAS_THUNDER = "HAS_THUNDER"
    """
    Requires a way to damage metal enemies in the presence of thunder pyramids
    (Thunder Ring|Zantestu Sword|Soul Blade).
    """
    HAS_MAGIC = "HAS_MAGIC"
    """Requires a way to damage enemies outside of sword range."""
    HAS_SWORD = "HAS_SWORD"
    """
    Requires any sword. Only used as a sanity check at the start of the game
    since we prefill the first chest with a sword.
    """
    HAS_STONES = "HAS_STONES"
    """Requires the necessary number of stones. Adjustable via option."""
    PHOENIX_CUTSCENE = "PHOENIX_CUTSCENE"
    """
    Requires the Phoenix cutscene:
    Access to the Mountain King
    Both Dancing Grandmas
    The 3 Red-Hot Items
    """


class IDOffset(IntEnum):
    BASE_ID: int = 374518970000
    """Base ID for items and locations"""

    LAIR_ID_OFFSET: int = 1000
    """ID offset for Lair IDs"""

    NPC_REWARD_OFFSET: int = 500
    """ID offset for NPC rewards"""

    SOUL_OFFSET: int = 300
    """ID Offset for Soul rewards."""


class WithFullName():
    full_names: dict[int,str] = {}
    @property
    def full_name (self) -> str:
        return self.full_names[self.value]
    

#TODO: Move back to Names?

class ChestID(WithFullName, IntEnum):
    TRIAL_ROOM                  = 0
    GRASS_VALLEY_SECRET_L       = 1
    GRASS_VALLEY_SECRET_R       = 2
    UNDERGROUND_CASTLE_TORCH    = 3
    UNDERGROUND_CASTLE_PILLAR   = 4
    UNDERGROUND_CASTLE_DREAM    = 5
    UNDERGROUND_CASTLE_CENTER   = 6
    LEOS_PAINTING_CENTER        = 7
    LEOS_PAINTING_METAL         = 8
    GREENWOOD_DREAM             = 9
    GREENWOOD_TUNNELS           = 10
    WATER_SHRINE_1F             = 11
    WATER_SHRINE_B1_WATERFALL   = 12
    WATER_SHRINE_B1_SPIKE       = 13
    WATER_SHRINE_B2_SW          = 14
    WATER_SHRINE_B2_SE          = 15
    FIRE_SHRINE_1F              = 16
    FIRE_SHRINE_B1_DISAPPEARING = 17
    FIRE_SHRINE_B1_METAL        = 18
    FIRE_SHRINE_B2_MID          = 19
    FIRE_SHRINE_B2_END          = 20
    LIGHT_SHRINE_1F_SPIRIT      = 21
    ST_ELLIS_COMMON_EAST        = 22
    ST_ELLIS_DOLPHIN_RIDE       = 23
    SEABED_SECRET_TL            = 24
    SEABED_SECRET_TR            = 25
    SEABED_SECRET_BL            = 26
    SEABED_SECRET_BR            = 27
    SOUTHERTA_TREE_MAZE         = 28
    ROCKBIRD_EAST_UPPER         = 29
    ROCKBIRD_EAST_LOWER         = 30
    DUREAN_LAVA_RIVER           = 31
    DUREAN_EAST_ISLAND          = 32
    GHOST_SHIP                  = 33
    SEABED_NW_SW_COVE           = 34
    MOUNTAIN_SLOPES_1_SE        = 35
    MOUNTAIN_SLOPES_2_LL        = 36
    MOUNTAIN_SLOPES_2_L         = 37
    MOUNTAIN_SLOPES_2_R         = 38
    MOUNTAIN_SLOPES_2_RR        = 39
    LAYNOLE_W_INVIS_BRIDGE      = 40
    LAYNOLE_E_INVIS_BRIDGE_1    = 41
    LAYNOLE_E_INVIS_BRIDGE_2    = 42
    LEOS_LAB_MAIN               = 43
    POWER_PLANT_START           = 44
    MODEL_TOWN_1_SE             = 45
    MODEL_TOWN_1_NL             = 46
    MODEL_TOWN_1_NR             = 47
    MODEL_TOWN_2_TOP            = 48
    MODEL_TOWN_2_BOT            = 49
    CASTLE_B1_W                 = 50
    CASTLE_B1_NE                = 51
    CASTLE_B2_INVIS_N           = 52
    CASTLE_B2_INVIS_SW          = 53
    CASTLE_B2_INVIS_DEADEND     = 54
    CASTLE_B3_INVIS_NW          = 55
    CASTLE_RIGHT_TOWER_2F_L     = 56
    CASTLE_RIGHT_TOWER_2F_R     = 57
    CASTLE_RIGHT_TOWER_3F_TL    = 58
    CASTLE_RIGHT_TOWER_3F_BR    = 59
    WOE_1_SE                    = 60
    WOE_1_SW                    = 61
    WOE_1_WARP                  = 62
    WOE_2_E                     = 63
    DAZZLING_SPACE_SE           = 64
    DAZZLING_SPACE_SW           = 65


class ItemID(WithFullName, IntEnum):
    NOTHING         = 0x00

    #Swords
    LIFESWORD       = 0x01
    PSYCHOSWORD     = 0x02
    CRITICALSWORD   = 0x03
    LUCKYBLADE      = 0x04
    ZANTETSUSWORD   = 0x05
    SPIRITSWORD     = 0x06
    RECOVERYSWORD   = 0x07
    SOULBLADE       = 0x08

    #Armor
    IRONARMOR       = 0x09
    ICEARMOR        = 0x0A
    BUBBLEARMOR     = 0x0B
    MAGICARMOR      = 0x0C
    MYSTICARMOR     = 0x0D
    LIGHTARMOR      = 0x0E
    ELEMENTALARMOR  = 0x0F
    SOULARMOR       = 0x10

    #Magic
    FLAMEBALL       = 0x11
    LIGHTARROW      = 0x12
    MAGICFLARE      = 0x13
    ROTATOR         = 0x14
    SPARKBOMB       = 0x15
    FLAMEPILLAR     = 0x16
    TORNADO         = 0x17
    PHOENIX         = 0x18

    #Items
    GOATSFOOD       = 0x19
    HARPSTRING      = 0x1A
    APASS           = 0x1B
    DREAMROD        = 0x1C
    LEOSBRUSH       = 0x1D
    TURBOSLEAVES    = 0x1E
    MOLESRIBBON     = 0x1F
    BIGPEARL        = 0x20
    MERMAIDSTEARS   = 0x21
    MUSHROOMSHOES   = 0x22
    AIRSHIPKEY      = 0x23
    THUNDERRING     = 0x24
    DELICIOUSSEEDS  = 0x25
    ACTINIDIALEAVES = 0x26
    DOORKEY         = 0x27
    PLATINUMCARD    = 0x28
    VIPCARD         = 0x29
    EMBLEMA         = 0x2A
    EMBLEMB         = 0x2B
    EMBLEMC         = 0x2C
    EMBLEMD         = 0x2D
    EMBLEME         = 0x2E
    EMBLEMF         = 0x2F
    EMBLEMG         = 0x30
    EMBLEMH         = 0x31
    REDHOTMIRROR    = 0x32
    REDHOTBALL      = 0x33
    REDHOTSTICK     = 0x34
    POWERBRACELET   = 0x35
    SHIELDBRACELET  = 0x36
    SUPERBRACELET   = 0x37
    MEDICALHERB     = 0x38
    STRANGEBOTTLE   = 0x39
    BROWNSTONE      = 0x3A
    GREENSTONE      = 0x3B
    BLUESTONE       = 0x3C
    SILVERSTONE     = 0x3D
    PURPLESTONE     = 0x3E
    BLACKSTONE      = 0x3F
    MAGICBELL       = 0x40

    # TODO: extend with more rewards (DeathLink/Traps)
    #Special
    VICTORY         = 0xFA
    SOUL            = 0xFB
    REMOTE_ITEM     = 0xFC
    LAIR_RELEASE    = 0xFD
    EXP             = 0xFE
    GEMS            = 0xFF

#TODO: redo enum names (based on NPC, or Lair location?)
class LairID(WithFullName, IntEnum):
    OLD_WOMAN_CHIEFS_HOUSE     = 2
    TOOL_SHOP_OWNER            = 6
    TULIP_CHIEFS_HOUSE         = 7
    BRIDGE_GUARD               = 8
    VILLAGE_CHIEF              = 9
    IVY_CHEST_ROOM             = 13
    WATER_MILL                 = 14
    GOAT_PEN                   = 15
    LISA                       = 16
    TULIP_ABOVE_DUNGEON        = 17
    ARCHITECT                  = 18
    IVY_SE                     = 19
    GOURMET_GOAT               = 21
    TEDDY                      = 22
    TULIP_LEOS_HOUSE           = 24
    LEOS_HOUSE                 = 26
    LONELY_GOAT                = 29
    TULIP_SLEEPING_PUSH        = 34
    BOY_CABIN                  = 35
    BOY_CAVE                   = 37
    LONELY_OLD_MAN             = 40
    OLD_MAN_CRAB_WALK          = 41
    IVY_NEAR_DUNGEON           = 42
    IVY_CLIFF_TILE             = 43
    IVY_HIDEOUT_CRYSTAL        = 44
    TULIP_GOAT_PEN             = 46
    GOAT_WIFE                  = 47
    SHY_BIRD                   = 55
    BIRD_MARSH_ENTRANCE        = 56
    DOG_WALKABLE               = 60
    DOG_SNIFFING               = 61
    DOG_WOODSTIN               = 63
    MOLE_WITH_GIFT             = 64
    SQUIRREL_NOT_HUNGRY        = 65
    SQUIRREL_HUNGRY            = 67
    BIRD_SE                    = 70
    MOLE_WITH_SOUL             = 73
    DEER_WOODSTIN              = 74
    CROCODILE_CENTER           = 78
    SQUIRREL_WEST_TREE         = 79
    GREENWOODS_GUARDIAN        = 80
    MOLE_HOLE_TO_STUMP         = 81
    DOG_WAITER                 = 86
    SQUIRREL_SLEEPING_STUMP    = 88
    SQUIRREL_CAFE              = 89
    DOG_GRAVEYARD              = 90
    CROCODILE_GRAVEYARD        = 91
    MOLE_PEEKABOO              = 92
    SQUIRREL_WOODSTIN          = 93
    BIRD_SLEEPING_TURBO        = 97
    MOLE_HOLE_FOR_BLIND_MOLE   = 98
    DEER_MASTER_CRYSTAL        = 99
    BIRD_NE                    = 100
    CROCODILE_W                = 111
    MONMO                      = 114
    DOLPHIN_NW_HOUSE           = 124
    ANGELFISH_CURIOUS          = 131
    MERMAID_NE_HOUSE           = 132
    ANGELFISH_JUMPING          = 134
    MERMAID_W_GUARD            = 138
    MERMAID_DANCER_NANNA       = 139
    DOLPHIN_SAVES_LUE          = 140
    MERMAID_STATUE_BLESTER     = 141
    MERMAID_COMMON_N_ITEM      = 142
    LUE                        = 143
    MERMAID_ATTENDANT_L        = 146
    MERMAID_NW_HOUSE           = 149
    MERMAID_TROUPE_LEADER      = 153
    DOLPHIN_NE_PLATFORM        = 155
    MERMAID_STATUE_ROCKBIRD    = 157
    MERMAID_COMMON_MAIN        = 161
    MERMAID_E_GUARD            = 164
    MERMAID_DANCER_KANNA       = 165
    MERMAID_COMMON_E           = 167
    MERMAID_STATUE_DUREAN      = 171
    ANGELFISH_CENTER_S         = 173
    ANGELFISH_WITH_SOUL        = 177
    MERMAID_COMMON_W_ITEM      = 181
    MERMAID_QUEEN              = 182
    MERMAID_STATUE_GHOST_SHIP  = 185
    DOLPHIN_SLEEPING           = 187
    MERMAID_ATTENDANT_R        = 189
    ANGELFISH_CENTER_E         = 190
    MERMAID_COMMON_SWIMMING    = 192
    DOLPHIN_RIDE_CHEST         = 193
    MERMAID_DANCER_ANNA        = 194
    GRANDPA_NW                 = 201
    GIRL_ENTRANCE              = 202
    MUSHROOM_NE_LAKE           = 203
    BOY_W_TUNNEL               = 204
    GRANDPA_HUSBAND            = 211
    SNAIL_JOCKEY_LEGEND        = 212
    NOME                       = 214
    BOY_IN_JAIL                = 215
    SLEEPING_MUSHROOM          = 221
    DANCING_GRANDMA_R          = 225
    DANCING_GRANDMA_L          = 230
    SNAIL_SECRET_ROOM          = 232
    BOY_WITH_GIFT              = 233
    GRANDMA_TELEPORT           = 234
    GIRL_GAZING                = 235
    MUSHROOM_S_TUNNEL          = 238
    SNAIL_JOCKEY_FLASH         = 239
    SNAIL_JOCKEY_UNKNOWN       = 240
    GIRL_E_TUNNEL              = 242
    MUSHROOM_SOLITARY_ROOM     = 246
    SNAIL_WITH_BOY             = 247
    GRANDPA_SW_TUNNEL          = 248
    SNAIL_WITH_GRANDPA         = 250
    GRANDPA_SE_LAKE            = 252
    GRANDPA_LUNE               = 254
    GRANDPA_JAIL               = 255
    MOUNTAIN_KING              = 259
    PLANT_MOUSEHOLE            = 265
    PLANT_W_LAB                = 267
    CHEST_OF_DRAWERS_LOCKED_RM = 268
    CAT_STALKING_1             = 269
    GREAT_DOOR_MAIN_LAB        = 274
    CAT_STALKING_2             = 276
    GREAT_DOOR_LOCKED          = 282
    CAT_LOCKED_ROOM            = 283
    MODEL_TOWN1                = 286
    GREAT_DOOR_MODEL_TOWNS     = 288
    STEPS_TO_2F                = 290
    CAT_SLEEPING               = 294
    MOUSE_OUTSIDE_HOLE         = 297
    MARIE                      = 303
    DOLL_CHAPEL                = 310
    CHEST_OF_DRAWERS_EXCERCISE = 311
    PLANT_LOCKED_ROOM          = 313
    MOUSE_CIRCLING_1           = 315
    MOUSE_WITH_GIFT            = 316
    MOUSE_BEDROOM              = 318
    GREAT_DOOR_WITH_SOUL       = 322
    MODEL_TOWN2                = 325
    MOUSE_DEVOUT               = 330
    STEPS_ATTIC                = 331
    CHEST_OF_DRAWERS_ATTIC     = 332
    PLANT_ACTINIDIA            = 333
    MOUSE_CIRCLING_2           = 338
    CAT_ATTIC                  = 339
    STAIRS_POWER_PLANT         = 341
    SOLDIER_NEAR_BASEMENT      = 345
    SOLDIER_ARCHITECT          = 346
    SOLDIER_KNOWS_SLEEPING     = 351
    SOLDIER_SLEEPING           = 353
    SOLDIER_PATROLLING         = 354
    SOLDIER_RIGHT_MOAT         = 358
    SINGER_CONCERT_HALL        = 359
    SOLDIER_CONCERT            = 360
    MAID_BASHFUL               = 363
    SOLDIER_LEFT_TOWER         = 365
    SOLDIER_DOK                = 366
    SOLDIER_CONCERT_ITEM       = 368
    SINGER_OUTSIDE             = 370
    SOLDIER_WITH_SOUL          = 377
    MAID_CONCERT_HALL          = 382
    QUEEN_MAGRIDD              = 383
    SOLDIER_WITH_LEO           = 385
    SOLDIER_RIGHT_TOWER        = 386
    DR_LEO                     = 387
    SOLDIER_BASHFUL            = 389
    SOLDIER_OBSERVANT          = 390
    MAID_HERB                  = 391
    SOLDIER_CASTLE             = 396
    SOLDIER_NE_BUILDING        = 397
    SOLDIER_BAR                = 399
    SOLDIER_UNOBSERVANT        = 402
    KING_MAGRIDD               = 405

class NPCID(WithFullName, IntEnum):
    OLD_WOMAN_CHIEFS_HOUSE     = 2
    TOOL_SHOP_OWNER            = 6
    TULIP_CHIEFS_HOUSE         = 7
    BRIDGE_GUARD               = 8
    VILLAGE_CHIEF              = 9
    IVY_CHEST_ROOM             = 13
    WATER_MILL                 = 14
    GOAT_PEN                   = 15
    LISA                       = 16
    TULIP_ABOVE_DUNGEON        = 17
    ARCHITECT                  = 18
    IVY_SE                     = 19
    GOURMET_GOAT               = 21
    TEDDY                      = 22
    TULIP_LEOS_HOUSE           = 24
    LEOS_HOUSE                 = 26
    LONELY_GOAT                = 29
    TULIP_SLEEPING_PUSH        = 34
    BOY_CABIN                  = 35
    BOY_CAVE                   = 37
    LONELY_OLD_MAN             = 40
    OLD_MAN_CRAB_WALK          = 41
    IVY_NEAR_DUNGEON           = 42
    IVY_CLIFF_TILE             = 43
    IVY_HIDEOUT_CRYSTAL        = 44
    TULIP_GOAT_PEN             = 46
    GOAT_WIFE                  = 47
    SHY_BIRD                   = 55
    BIRD_MARSH_ENTRANCE        = 56
    DOG_WALKABLE               = 60
    DOG_SNIFFING               = 61
    DOG_WOODSTIN               = 63
    MOLE_WITH_GIFT             = 64
    SQUIRREL_NOT_HUNGRY        = 65
    SQUIRREL_HUNGRY            = 67
    BIRD_SE                    = 70
    MOLE_WITH_SOUL             = 73
    DEER_WOODSTIN              = 74
    CROCODILE_CENTER           = 78
    SQUIRREL_WEST_TREE         = 79
    GREENWOODS_GUARDIAN        = 80
    MOLE_HOLE_TO_STUMP         = 81
    DOG_WAITER                 = 86
    SQUIRREL_SLEEPING_STUMP    = 88
    SQUIRREL_CAFE              = 89
    DOG_GRAVEYARD              = 90
    CROCODILE_GRAVEYARD        = 91
    MOLE_PEEKABOO              = 92
    SQUIRREL_WOODSTIN          = 93
    BIRD_SLEEPING_TURBO        = 97
    MOLE_HOLE_FOR_BLIND_MOLE   = 98
    DEER_MASTER_CRYSTAL        = 99
    BIRD_NE                    = 100
    CROCODILE_W                = 111
    MONMO                      = 114
    DOLPHIN_NW_HOUSE           = 124
    ANGELFISH_CURIOUS          = 131
    MERMAID_NE_HOUSE           = 132
    ANGELFISH_JUMPING          = 134
    MERMAID_W_GUARD            = 138
    MERMAID_DANCER_NANNA       = 139
    DOLPHIN_SAVES_LUE          = 140
    MERMAID_STATUE_BLESTER     = 141
    MERMAID_COMMON_N_ITEM      = 142
    LUE                        = 143
    MERMAID_ATTENDANT_L        = 146
    MERMAID_NW_HOUSE           = 149
    MERMAID_TROUPE_LEADER      = 153
    DOLPHIN_NE_PLATFORM        = 155
    MERMAID_STATUE_ROCKBIRD    = 157
    MERMAID_COMMON_MAIN        = 161
    MERMAID_E_GUARD            = 164
    MERMAID_DANCER_KANNA       = 165
    MERMAID_COMMON_E           = 167
    MERMAID_STATUE_DUREAN      = 171
    ANGELFISH_CENTER_S         = 173
    ANGELFISH_WITH_SOUL        = 177
    MERMAID_COMMON_W_ITEM      = 181
    MERMAID_QUEEN              = 182
    MERMAID_STATUE_GHOST_SHIP  = 185
    DOLPHIN_SLEEPING           = 187
    MERMAID_ATTENDANT_R        = 189
    ANGELFISH_CENTER_E         = 190
    MERMAID_COMMON_SWIMMING    = 192
    DOLPHIN_RIDE_CHEST         = 193
    MERMAID_DANCER_ANNA        = 194
    GRANDPA_NW                 = 201
    GIRL_ENTRANCE              = 202
    MUSHROOM_NE_LAKE           = 203
    BOY_W_TUNNEL               = 204
    GRANDPA_HUSBAND            = 211
    SNAIL_JOCKEY_LEGEND        = 212
    NOME                       = 214
    BOY_IN_JAIL                = 215
    SLEEPING_MUSHROOM          = 221
    DANCING_GRANDMA_R          = 225
    DANCING_GRANDMA_L          = 230
    SNAIL_SECRET_ROOM          = 232
    BOY_WITH_GIFT              = 233
    GRANDMA_TELEPORT           = 234
    GIRL_GAZING                = 235
    MUSHROOM_S_TUNNEL          = 238
    SNAIL_JOCKEY_FLASH         = 239
    SNAIL_JOCKEY_UNKNOWN       = 240
    GIRL_E_TUNNEL              = 242
    MUSHROOM_SOLITARY_ROOM     = 246
    SNAIL_WITH_BOY             = 247
    GRANDPA_SW_TUNNEL          = 248
    SNAIL_WITH_GRANDPA         = 250
    GRANDPA_SE_LAKE            = 252
    GRANDPA_LUNE               = 254
    GRANDPA_JAIL               = 255
    MOUNTAIN_KING              = 259
    PLANT_MOUSEHOLE            = 265
    PLANT_W_LAB                = 267
    CHEST_OF_DRAWERS_LOCKED_RM = 268
    CAT_STALKING_1             = 269
    GREAT_DOOR_MAIN_LAB        = 274
    CAT_STALKING_2             = 276
    GREAT_DOOR_LOCKED          = 282
    CAT_LOCKED_ROOM            = 283
    MODEL_TOWN1                = 286
    GREAT_DOOR_MODEL_TOWNS     = 288
    STEPS_TO_2F                = 290
    CAT_SLEEPING               = 294
    MOUSE_OUTSIDE_HOLE         = 297
    MARIE                      = 303
    DOLL_CHAPEL                = 310
    CHEST_OF_DRAWERS_EXCERCISE = 311
    PLANT_LOCKED_ROOM          = 313
    MOUSE_CIRCLING_1           = 315
    MOUSE_WITH_GIFT            = 316
    MOUSE_BEDROOM              = 318
    GREAT_DOOR_WITH_SOUL       = 322
    MODEL_TOWN2                = 325
    MOUSE_DEVOUT               = 330
    STEPS_ATTIC                = 331
    CHEST_OF_DRAWERS_ATTIC     = 332
    PLANT_ACTINIDIA            = 333
    MOUSE_CIRCLING_2           = 338
    CAT_ATTIC                  = 339
    STEPS_POWER_PLANT          = 341
    SOLDIER_NEAR_BASEMENT      = 345
    SOLDIER_ARCHITECT          = 346
    SOLDIER_KNOWS_SLEEPING     = 351
    SOLDIER_SLEEPING           = 353
    SOLDIER_PATROLLING         = 354
    SOLDIER_RIGHT_MOAT         = 358
    SINGER_CONCERT_HALL        = 359
    SOLDIER_CONCERT            = 360
    MAID_BASHFUL               = 363
    SOLDIER_LEFT_TOWER         = 365
    SOLDIER_DOK                = 366
    SOLDIER_CONCERT_ITEM       = 368
    SINGER_OUTSIDE             = 370
    SOLDIER_WITH_SOUL          = 377
    MAID_CONCERT_HALL          = 382
    QUEEN_MAGRIDD              = 383
    SOLDIER_WITH_LEO           = 385
    SOLDIER_RIGHT_TOWER        = 386
    DR_LEO                     = 387
    SOLDIER_BASHFUL            = 389
    SOLDIER_OBSERVANT          = 390
    MAID_BAR                   = 391
    SOLDIER_CASTLE             = 396
    SOLDIER_NE_BUILDING        = 397
    SOLDIER_BAR                = 399
    SOLDIER_UNOBSERVANT        = 402
    KING_MAGRIDD               = 405

class NPCRewardID(WithFullName, IntEnum):
    TOOL_SHOP_OWNER              = 0x00
    GRASS_VALLEY_SE_CLIFF_TILE   = 0x01
    GOAT_PEN_CORNER              = 0x02
    TEDDY                        = 0x03
    UNDER_TULIP_TILE             = 0x04
    HIDEOUT_CLIFF_TILE           = 0x05
    VILLAGE_CHIEF                = 0x06
    MAGICIAN                     = 0x07
    HIDEOUT_CLIFF_CRYSTAL        = 0x08
    GRASS_VALLEY_SECRET_CRYSTAL  = 0x09
    UNDERGROUND_CASTLE_CRYSTAL   = 0x0A
    SHY_BIRD                     = 0x0B
    MASTER_CRYSTAL               = 0x0C
    WOODSTIN_TRIO                = 0x0D
    GREENWOODS_GUARDIAN          = 0x0E
    TURBOS_REMAINS_TILE          = 0x0F
    MOLES_REWARD                 = 0x10
    HUNGRY_SQUIRREL              = 0x11
    NOT_HUNGRY_SQUIRREL          = 0x12
    WATER_SHRINE_B2_TILE         = 0x13
    FIRE_SHRINE_B2_CRYSTAL       = 0x14
    LOST_MARSH_CRYSTAL           = 0x15
    WATER_SHRINE_B1_CRYSTAL      = 0x16
    FIRE_SHRINE_1F_CRYSTAL       = 0x17
    MOUNTAIN_KING                = 0x18
    BOY_WITH_GIFT                = 0x19
    NOME                         = 0x1A
    SECRET_SNAIL                 = 0x1B
    MUSHROOMS_DREAM_TILE         = 0x1C
    MOUNTAIN_SUMMIT_CAVE_CRYSTAL = 0x1D
    LUNE_PASSAGE_CRYSTAL         = 0x1E
    UNDER_CHEST_OF_DRAWERS_TILE  = 0x1F
    LOCKED_ROOM_CHEST_OF_DRAWERS = 0x20
    MOUSEHOLE_PLANT              = 0x21
    SLEEPING_CAT                 = 0x22
    ACTINIDIA_PLANT              = 0x23
    ATTIC_CHEST_OF_DRAWERS       = 0x24
    MARIE                        = 0x25
    MOUSE_WITH_GIFT              = 0x26
    LEOS_LAB_B2_CRYSTAL          = 0x27
    MODEL_TOWN_1_CRYSTAL         = 0x28
    POWER_PLANT_CRYSTAL          = 0x29
    SLEEPING_SOLDIER             = 0x2A
    QUEEN_MAGRIDD_TILE           = 0x2B
    QUEEN_MAGRIDD_ITEM           = 0x2C
    UNDER_SOLDIER_TILE           = 0x2D
    MAID_AT_BAR                  = 0x2E
    CASTLE_GROUNDS_TILE          = 0x2F
    KING_MAGRIDD                 = 0x30
    LEO_ON_THE_AIRSHIP_DECK      = 0x31
    CASTLE_B1_SKELETON_TILE      = 0x32
    NORTHEAST_MERMAID            = 0x33
    COMMON_HOUSE_MAIN_MERMAID    = 0x34
    COMMON_HOUSE_W_ROOM_MERMAID  = 0x35
    MERMAID_QUEEN                = 0x36
    COMMON_HOUSE_N_MERMAID       = 0x37
    LUE                          = 0x38
    ROCKBIRD_CRYSTAL             = 0x39
    SEABED_CRYSTAL_NEAR_BLESTER  = 0x3A
    SEABED_CRYSTAL_NEAR_DUREAN   = 0x3B

    # Souls
    MAGICIAN_SOUL                = 0x3C
    MOLE_SOUL                    = 0x3D
    ANGELFISH_SOUL               = 0x3E
    GREAT_DOOR_SOUL              = 0x3F
    SOLDIER_SOUL                 = 0x40

class SoulID(WithFullName, IntEnum):
    SOUL_MAGICIAN  = 0x00
    SOUL_LIGHT     = 0x01
    SOUL_SHIELD    = 0x02
    SOUL_DETECTION = 0x03
    SOUL_REALITY   = 0x04

