"""String constants for Mega Man X5 items and locations.

Boss/weapon names use the US (NTSC-U) localization. Boss->weapon mapping is
series knowledge; marked TODO until each is confirmed in-game during testing.
"""

# Stages / bosses (US names)
GRIZZLY = "Grizzly Slash"
WHALE = "Duff McWhalen"
KRAKEN = "Squid Adler"
FIREFLY = "Izzy Glow"
NECROBAT = "Dark Dizzy"
PEGASUS = "The Skiver"
DINOREX = "Mattrex"
ROSERED = "Axle the Red"

STAGES = [GRIZZLY, WHALE, KRAKEN, FIREFLY, NECROBAT, PEGASUS, DINOREX, ROSERED]

# Weapons (X's versions; ammo-slot bit order per verified RAM map:
# 0x800D1C4C bit0=C-Shot, bit1=Dark Hold; bits 2-7 inferred - TODO confirm)
CSHOT = "C-Shot"
DARK_HOLD = "Dark Hold"
GOO_SHAVER = "Goo Shaver"
GROUND_FIRE = "Ground Fire"
TRI_THUNDER = "Tri-Thunder"
F_LASER = "F-Laser"
SPIKE_BALL = "Spike Ball"
WING_SPIRAL = "Wing Spiral"

# boss -> weapon awarded (TODO: verify each during testing)
BOSS_WEAPON = {
    GRIZZLY: CSHOT,
    WHALE: GOO_SHAVER,
    KRAKEN: TRI_THUNDER,
    FIREFLY: F_LASER,
    NECROBAT: DARK_HOLD,
    PEGASUS: WING_SPIRAL,
    DINOREX: GROUND_FIRE,
    ROSERED: SPIKE_BALL,
}

# Other items
HEART_TANK = "Heart Tank"
FALCON_HEAD = "Falcon Armor Head"
FALCON_BODY = "Falcon Armor Body"
FALCON_ARM = "Falcon Armor Arm"
FALCON_LEG = "Falcon Armor Leg"
GAEA_HEAD = "Gaea Armor Head"
GAEA_BODY = "Gaea Armor Body"
GAEA_ARM = "Gaea Armor Arm"
GAEA_LEG = "Gaea Armor Leg"
ARMOR_PARTS = [FALCON_HEAD, FALCON_BODY, FALCON_ARM, FALCON_LEG,
               GAEA_HEAD, GAEA_BODY, GAEA_ARM, GAEA_LEG]

SMALL_ENERGY = "Small Energy"

# Tanks (vanilla stage homes from the placement-record harvest 2026-07-31:
# Sub-Tank #1 = Grizzly Slash, Sub-Tank #2 = Dark Dizzy, W-Tank = The Skiver,
# EX-Tank = Izzy Glow)
SUB_TANK = "Sub-Tank"
W_TANK = "W-Tank"
EX_TANK = "EX-Tank"
STAGE_TANK = {
    GRIZZLY: SUB_TANK,
    NECROBAT: SUB_TANK,
    PEGASUS: W_TANK,
    FIREFLY: EX_TANK,
}

# Locations
INTRO_CLEAR = "Intro Stage - Clear"


def boss_location(stage: str) -> str:
    return f"{stage} - Boss Defeated"


def heart_location(stage: str) -> str:
    return f"{stage} - Heart Tank"


def capsule_location(stage: str) -> str:
    return f"{stage} - Armor Capsule"


def tank_location(stage: str) -> str:
    return f"{stage} - {STAGE_TANK[stage]}"


VICTORY = "Sigma Defeated"
