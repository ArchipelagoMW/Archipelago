""" Constants for Ratchet & Clank 3 player action states. States without a character name defaults to Ratchet."""


class RAC3PLAYERACTION:
    """Ratchet's (or the current player character's) Action states."""
    IDLE = 0x00
    WRENCH_FIRST_PERSON = 0x01
    WALKING = 0x02
    SKIDDING = 0x03
    CROUCHING = 0x04
    QUICK_TURN = 0x05
    FALLING = 0x06
    JUMP_FEET_APART = 0x07
    GLIDING = 0x08
    JUMP_FEET_TOGETHER = 0x09
    HELI_LONG_JUMP = 0x0A
    JUMP_FLIP = 0x0B
    JUMP_JINK = 0x0C
    THRUSTER_HIGH_JUMP = 0x0D
    DOUBLE_JUMP = 0x0E
    HELI_HIGH_JUMP = 0x0F
    THRUSTER_LONG_JUMP = 0x10
    WALL_JUMP = 0x11
    JUMP_OUT_OF_WATER = 0x12
    MELEE_SWING = 0x13
    HYPER_STRIKE = 0x14
    MELEE_THROW = 0x15
    HURT = 0x16
    LEDGE_GRAB = 0x17
    LEDGE_HANG = 0x18
    LEDGE_TRAVERSAL_LEFT = 0x19
    LEDGE_TRAVERSAL_RIGHT = 0x1A
    LEDGE_JUMP = 0x1B
    VISIBOMB = 0x1C
    WEAPON_FIRST_PERSON = 0x1D
    GUN_WAITING = 0x1E
    WALLOPER_ATTACK = 0x1F
    ATTACK_BOUNCE = 0x20
    THRUSTER_GROUND_POUND = 0x21
    GLOVE_THROW = 0x22
    HYPERSHOT_EXTEND = 0x23
    HYPERSHOT_PULL = 0x24
    HYPERSHOT_PULL_VEHICLE = 0x25
    SUCK_CANNON = 0x26
    GRIND = 0x27
    GRIND_JUMP = 0x28
    GRIND_SWITCH_JUMP = 0x29
    GRIND_ATTACK = 0x2A
    HYPERSHOT_SWING = 0x2B
    HYPERSHOT_LAUNCH = 0x2C
    RECOIL = 0x2D
    ICE_SKATING = 0x2E
    DEVASTATOR = 0x2F
    SLIDING = 0x30
    EATEN = 0x31
    UNDERWATER_SWIM = 0x32
    UNDERWATER_IDLE = 0x33
    HYDRO_PACK = 0x34
    SURFACE_SWIM = 0x35
    WATER_SURFACE_IDLE = 0x36
    WRENCH_CRANK = 0x37
    LAVA_ELECTRIC_BOUNCE = 0x38
    DEATH = 0x39
    BOARDING = 0x3A
    GRAVITY_WALK = 0x3B
    GRIND_HIT = 0x3C
    GRIND_JUMP_TURN = 0x3D
    CLANK_IDLE = 0x3F
    CLANK_WALK = 0x40
    CLANK_HURT = 0x42
    CLANK_DIE = 0x43
    CLANK_JUMP = 0x45
    CLANK_GLIDE = 0x4B
    CLANK_PUNCH = 0x4D
    CLANK_FROZEN = 0x50
    TYHRRANOID_IDLE = 0x51
    TYHRRANOID_WALK = 0x52
    TYHRRANOID_FALLING = 0x53
    TYHRRANOID_JUMP = 0x54
    TYHRRANOID_HURT = 0x55
    TYHRRANOID_DEATH = 0x56
    TYHRRANOID_MINIGAME = 0x58
    TYHRRANOID_WAVE = 0x59
    GIANT_CLANK_IDLE = 0x5B
    GIANT_CLANK_WALK = 0x5C
    GIANT_CLANK_HURT = 0x5D
    GIANT_CLANK_JUMP = 0x5F
    GIANT_CLANK_PUNCH = 0x61
    GIANT_CLANK_BOMB = 0x62
    GIANT_CLANK_DIE = 0x63
    IN_CUTSCENE = 0x65
    PATHING = 0x66
    HACKER = 0x68
    AREA_LOAD_SEWERS = 0x69
    UNDERWATER_DEATH = 0x6C
    GRAVITY_BOOTS_JUMP = 0x73
    SQUASHED = 0x74
    SHALLOW_WATER = 0x75
    ZIPLINE = 0x76
    UNDERWATER_DAMAGE = 0x78
    FALLING_DEATH = 0x79
    WALL_BONK = 0x7C
    DROWNING_IN_LAVA_MUD_INSTANT = 0x7D
    DROWNING_IN_LAVA_BOUNCE = 0x7E
    CHARGE_BOOTS = 0x80
    FROZEN_ICECUBE = 0x81
    PANCAKED = 0x91
    QWARK_IDLE = 0x9A
    QWARK_WALK = 0x9B
    QWARK_WALL_SLIDE = 0x9C
    QWARK_PUNCH = 0x9D
    QWARK_HURT = 0x9E
    QWARK_DEATH = 0x9F
    QWARK_JUMP = 0xA2
    QWARK_CROUCH = 0xA3
    QWARK_WALL_JUMP = 0xA7
    QWARK_LEDGE_GRAB = 0xA9
    HALO_DIVE = 0xB0


PERMITTED_DEATHLINK_SHIP_TELEPORT_ACTIONS = [
    RAC3PLAYERACTION.IDLE,
    RAC3PLAYERACTION.WRENCH_FIRST_PERSON,
    RAC3PLAYERACTION.WALKING,
    RAC3PLAYERACTION.SKIDDING,
    RAC3PLAYERACTION.CROUCHING,
    RAC3PLAYERACTION.MELEE_SWING,
    RAC3PLAYERACTION.WEAPON_FIRST_PERSON,
    RAC3PLAYERACTION.ICE_SKATING,
    RAC3PLAYERACTION.UNDERWATER_SWIM,
    RAC3PLAYERACTION.UNDERWATER_IDLE,
    RAC3PLAYERACTION.HYDRO_PACK,
    RAC3PLAYERACTION.WRENCH_CRANK,
    RAC3PLAYERACTION.CLANK_IDLE,
    RAC3PLAYERACTION.CLANK_WALK,
    RAC3PLAYERACTION.CLANK_PUNCH,
    RAC3PLAYERACTION.TYHRRANOID_IDLE,
    RAC3PLAYERACTION.TYHRRANOID_WALK,
    RAC3PLAYERACTION.TYHRRANOID_WAVE,
    RAC3PLAYERACTION.GIANT_CLANK_IDLE,
    RAC3PLAYERACTION.GIANT_CLANK_WALK,
    RAC3PLAYERACTION.GIANT_CLANK_PUNCH,
    RAC3PLAYERACTION.GIANT_CLANK_BOMB,
    RAC3PLAYERACTION.SHALLOW_WATER,
    RAC3PLAYERACTION.ZIPLINE,
    RAC3PLAYERACTION.WALL_BONK,
    RAC3PLAYERACTION.CHARGE_BOOTS,
    RAC3PLAYERACTION.QWARK_IDLE,
    RAC3PLAYERACTION.QWARK_WALK,
    RAC3PLAYERACTION.QWARK_PUNCH,
    RAC3PLAYERACTION.QWARK_CROUCH,
]

PLAYER_ACTION_NAMES: dict[int, str] = {
    0x00: "Idle",
    0x01: "Wrench First Person",
    0x02: "Walking",
    0x03: "Skidding",
    0x04: "Crouching",
    0x05: "Quick Turn",
    0x06: "Falling",
    0x07: "Jump (Feet Apart)",
    0x08: "Gliding",
    0x09: "Jump (Feet Together)",
    0x0A: "Heli Long Jump",
    0x0B: "Jump Flip",
    0x0C: "Jump Jink",
    0x0D: "Thruster High Jump",
    0x0E: "Double Jump",
    0x0F: "Heli High Jump",
    0x10: "Thruster Long Jump",
    0x11: "Wall Jump",
    0x12: "Jump Out of Water",
    0x13: "Melee Swing",
    0x14: "Hyper Strike",
    0x15: "Melee Throw",
    0x16: "Hurt",
    0x17: "Ledge Grab",
    0x18: "Ledge Hang",
    0x19: "Ledge Traverse Left",
    0x1A: "Ledge Traverse Right",
    0x1B: "Ledge Jump",
    0x1C: "Visibomb",
    0x1D: "Weapon First Person",
    0x1E: "Gun Waiting",
    0x1F: "Walloper Attack",
    0x20: "Attack Bounce",
    0x21: "Thruster Ground Pound",
    0x22: "Glove Throw",
    0x23: "Hypershot Extend",
    0x24: "Hypershot Pull",
    0x25: "Hypershot Pull (Vehicle)",
    0x26: "Suck Cannon",
    0x27: "Grind",
    0x28: "Grind Jump",
    0x29: "Grind Switch Jump",
    0x2A: "Grind Attack",
    0x2B: "Hypershot Swing",
    0x2C: "Hypershot Launch",
    0x2D: "Recoil",
    0x2E: "Ice Skating",
    0x2F: "Devastator",
    0x30: "Sliding",
    0x31: "Eaten",
    0x32: "Underwater Swim",
    0x33: "Underwater Idle",
    0x34: "Hydro Pack",
    0x35: "Surface Swim",
    0x36: "Water Surface Idle",
    0x37: "Wrench Crank",
    0x38: "Lava/Electric Bounce",
    0x39: "Death",
    0x3A: "Boarding",
    0x3B: "Gravity Walk",
    0x3C: "Grind Hit",
    0x3D: "Grind Jump Turn",
    0x3F: "Clank Idle",
    0x40: "Clank Walk",
    0x42: "Clank Hurt",
    0x43: "Clank Death",
    0x45: "Clank Jump",
    0x4B: "Clank Glide",
    0x4D: "Clank Punch",
    0x50: "Clank Frozen",
    0x51: "Tyhrranoid Idle",
    0x52: "Tyhrranoid Walk",
    0x53: "Tyhrranoid Falling",
    0x54: "Tyhrranoid Jump",
    0x55: "Tyhrranoid Hurt",
    0x56: "Tyhrranoid Death",
    0x58: "Tyhrranoid Minigame",
    0x59: "Tyhrranoid Wave",
    0x5B: "Giant Clank Idle",
    0x5C: "Giant Clank Walk",
    0x5D: "Giant Clank Hurt",
    0x5F: "Giant Clank Jump",
    0x61: "Giant Clank Punch",
    0x62: "Giant Clank Bomb",
    0x63: "Giant Clank Death",
    0x65: "In Cutscene",
    0x66: "Pathing",
    0x68: "Hacker",
    0x69: "Area Load (Sewers)",
    0x6C: "Underwater Death",
    0x73: "Gravity Boots Jump",
    0x74: "Squashed",
    0x75: "Shallow Water",
    0x76: "Zipline",
    0x78: "Underwater Damage",
    0x79: "Falling Death",
    0x7C: "Wall Bonk",
    0x7D: "Instant Lava/Mud Death",
    0x7E: "Lava Bounce",
    0x80: "Charge Boots",
    0x81: "Frozen (Ice Cube)",
    0x91: "Pancaked",
    0x9A: "Qwark Idle",
    0x9B: "Qwark Walk",
    0x9C: "Qwark Wall Slide",
    0x9D: "Qwark Punch",
    0x9E: "Qwark Hurt",
    0x9F: "Qwark Death",
    0xA2: "Qwark Jump",
    0xA3: "Qwark Crouch",
    0xA7: "Qwark Wall Jump",
    0xA9: "Qwark Ledge Grab",
    0xB0: "Halo Dive",
}
