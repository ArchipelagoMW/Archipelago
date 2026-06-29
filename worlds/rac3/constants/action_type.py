"""Constants for Ratchet & Clank 3 player action types."""


class RAC3ACTIONTYPE:
    """Ratchet's (or the current playable character's) action types."""
    STATIONARY = 0x00
    WALKING = 0x01
    FALLING = 0x02
    LEDGE_GRAB = 0x03
    IN_AIR = 0x04
    GLIDING = 0x05
    WRENCH = 0x06
    DAMAGE = 0x07
    SHOOTING = 0x08
    PLAYER_MOVEMENT_LOCKED = 0x09
    BONK = 0x0A
    STOMP = 0x0B
    CROUCHING = 0x0C
    GRAPPLE = 0x0D
    SWINGSHOT = 0x0E
    GRIND = 0x0F
    SLIDE = 0x10
    UNDERWATER = 0x11
    SURFACE_SWIMMING = 0x12
    HYDRO = 0x13
    DYING = 0x14
    BOARD = 0x15
    RACE_BOARD = 0x16
    SPIN = 0x17
    IN_CUTSCENE = 0x18
    DROWNING = 0x19
    ZIPLINE = 0x1A
    HOLO = 0x1B
    CHARGE = 0x1C
    ROCKET_HOVER = 0x1D
    JET = 0x1E
    RACEBIKE = 0x1F
    SPEEDBOAT = 0x20
    PULL = 0x21
    LATCH = 0x22
    UNKNOWN_23 = 0x23
    LADDER = 0x24
    SKYDIVE = 0x25
    CNT = 0x26

ACTION_TYPE_NAMES: dict[int, str] = {
    0x00: "Stationary",
    0x01: "Walking",
    0x02: "Falling",
    0x03: "Ledge Grab",
    0x04: "Airborne",
    0x05: "Gliding",
    0x06: "Wrench",
    0x07: "Taking Damage",
    0x08: "Shooting",
    0x09: "Player Movement Locked",
    0x0A: "Bonk",
    0x0B: "Ground Pound",
    0x0C: "Crouching",
    0x0D: "Grapple",
    0x0E: "Swingshot",
    0x0F: "Grinding",
    0x10: "Sliding",
    0x11: "Underwater",
    0x12: "Surface Swimming",
    0x13: "Hydro Pack",
    0x14: "Dying",
    0x15: "Hoverboard",
    0x16: "Hoverboard Race",
    0x17: "Spin",
    0x18: "Cutscene",
    0x19: "Drowning",
    0x1A: "Zipline",
    0x1B: "Holo-guise",
    0x1C: "Charge Boots",
    0x1D: "Rocket Hover",
    0x1E: "Jetpack",
    0x1F: "Racebike",
    0x20: "Speedboat",
    0x21: "Pulling",
    0x22: "Latched",
    0x23: "Unknown (0x23)",
    0x24: "Ladder",
    0x25: "Skydive",
}
