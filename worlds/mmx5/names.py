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

# The two secret armors from the Zero Space capsule (id 8). Unlike the eight
# Falcon/Gaea parts these are NOT collected in pieces - one flag each, and
# each is tied to a character: Ultimate is X's, Black Zero is Zero's.
ULTIMATE_ARMOR = "Ultimate Armor"
BLACK_ZERO = "Black Zero"

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

# ---- DNA Parts ----------------------------------------------------------
# The 16 equippable Parts, stored as bits 2..17 of the u32 0x800D1C84. Bit
# numbers were read from the game itself (Parts screen with every bit forced
# on, 2026-08-06) rather than from the web, which returns Mega Man X6 Part
# facts for X5 queries constantly. Full provenance: ghidra-findings §9.15.
#
# Each Maverick offers TWO Parts and you get exactly one, decided by whether
# you pick Life+ or Energy+ at Alia's prompt - so vanilla yields 8 of the 16
# per playthrough. PART_PAIRS keeps that pairing; the shuffle picks one from
# each pair so a seed's Part economy matches the base game's.
SHOCK_BUFFER = "Shock Buffer"
HYPER_DASH = "Hyper Dash"
SUPER_RECOVER = "Super Recover"
W_ENERGY_SAVER = "W-Energy Saver"
QUICK_CHARGE = "Quick Charge"
Z_SABER_EXTEND = "Z-Saber Extend"
BURST_SHOTS = "Burst Shots"
SHOT_ERASER = "Shot Eraser"
ANTI_VIRUS_GUARD = "Anti-Virus Guard"
VIRUS_BUSTER = "Virus Buster"
JUMPER = "Jumper"
SPEEDSTER = "Speedster"
SPEED_SHOT = "Speed Shot"
BUSTER_PLUS = "Buster Plus"
ULTIMATE_BUSTER = "Ultimate Buster"
Z_SABER_PLUS = "Z-Saber Plus"

# boss -> (Life+ Part, Energy+ Part)
PART_PAIRS = {
    GRIZZLY:  (SHOCK_BUFFER, HYPER_DASH),
    WHALE:    (SUPER_RECOVER, W_ENERGY_SAVER),
    KRAKEN:   (QUICK_CHARGE, Z_SABER_EXTEND),
    FIREFLY:  (BURST_SHOTS, SHOT_ERASER),
    NECROBAT: (ANTI_VIRUS_GUARD, VIRUS_BUSTER),
    PEGASUS:  (JUMPER, SPEEDSTER),
    DINOREX:  (SPEED_SHOT, BUSTER_PLUS),
    ROSERED:  (ULTIMATE_BUSTER, Z_SABER_PLUS),
}
DNA_PARTS = [p for pair in PART_PAIRS.values() for p in pair]

# Six Parts only do anything for one character. Never progression: a run
# played entirely as the other character must not be stranded behind one.
# Note bits 11-16 are exactly these six - Capcom grouped them, which is what
# corroborates the name/bit mapping in §9.15.
X_ONLY_PARTS = {BURST_SHOTS, ULTIMATE_BUSTER, QUICK_CHARGE}
ZERO_ONLY_PARTS = {Z_SABER_PLUS, Z_SABER_EXTEND, SHOT_ERASER}

# Stage access items (option-gated). The lock is client-side: the hub's
# slot -> stage-id table at 0x800F5050 gets a 0 written over any stage you do
# not hold the codes for, and the game's own `stage id == 0 -> do nothing`
# branch at 0x800EFCA4 swallows the confirm. See ghidra-findings §9.14.
def access_item(stage: str) -> str:
    return f"{stage} Access Codes"


ACCESS_ITEMS = [access_item(s) for s in STAGES]

# Launcher parts (spec item 4 / overlay-findings §11): no vanilla storage
# exists (parts are the kill bits) - these are AP-only items the client
# turns into launch-score sourcing. 4 + 4; generic names on purpose.
ENIGMA_PART = "Enigma Part"
SHUTTLE_PART = "Shuttle Part"

# Locations
INTRO_CLEAR = "Intro Stage - Clear"

# Endgame stage clears. The hub's stage-select confirm handler picks the Zero
# Space destination straight off the story ACT byte (0x800D1C79):
#
#   ACT == 5 -> stage 0x10 (Zero Space 1)
#   ACT == 6 -> stage 0x11 (Zero Space 2)
#   ACT == 7 -> stage 0x12 (X vs Zero)
#   else     -> stage 0x0C (Sigma)
#
# so ACT doubles as the endgame progress counter and each clear is detectable
# from a byte the client already reads. Before these, the entire endgame held
# no checks at all outside pickupsanity capsules.
#
# Confirmed live 2026-08-06: clearing Zero Space 1 stepped ACT 5 -> 6.
ZERO_SPACE_1 = "Zero Space 1"
ZERO_SPACE_2 = "Zero Space 2"
ZERO_SPACE_X_VS_ZERO = "X vs Zero"
ENDGAME_STAGES = [ZERO_SPACE_1, ZERO_SPACE_2, ZERO_SPACE_X_VS_ZERO]


def endgame_clear_location(stage: str) -> str:
    return f"{stage} - Clear"


def boss_location(stage: str) -> str:
    return f"{stage} - Boss Defeated"


def heart_location(stage: str) -> str:
    return f"{stage} - Heart Tank"


def capsule_location(stage: str) -> str:
    return f"{stage} - Armor Capsule"


def tank_location(stage: str) -> str:
    return f"{stage} - {STAGE_TANK[stage]}"


def dna_part_location(stage: str) -> str:
    """The equippable Part granted alongside the level-8+ DNA reward tier.

    A Maverick at boss level 8+ gives THREE things: the weapon, the
    Life+/Energy+ boost, and an equippable Part (DNA parts bitfield u32
    0x800D1C84). Checked on the BOSS KILL like dna_location, deliberately NOT
    on the Part actually dropping - Parts only appear at level 8+, so on
    `relaxed` boss_difficulty (base 1) early bosses grant none and a
    grant-based check would be permanently MISSABLE.

    Not to be confused with the Enigma/Shuttle launcher part ITEMS."""
    return f"{stage} - DNA Part"


def rematch_location(stage: str) -> str:
    """Boss Rush rematch kill (Zero Space, stage 0x0C).

    Detection is a pure client-side watcher: the rematch runs in the standard
    boss-HP slot and the portal streams that Maverick's own boss module into
    RAM, which is what identifies the fight (16-byte fingerprint - see
    ram-notes §Boss fights). Nothing persists in the rush, so a missed check
    is always refightable by re-entering the stage."""
    return f"{stage} - Rematch"


def dna_location(stage: str) -> str:
    """The post-boss DNA reward choice (Alia's "Weapon + Life" / "Weapon +
    Energy" prompt). This REPLACED an earlier `energy_up_location`, which
    modelled Energy Ups as stage pickups - they are not. MMX5 has no
    Energy Up items lying in stages; the DNA choice is the only source, one
    per Maverick. See ai-docs/plans/2026-08-02_mmx5-reachability-rules.md."""
    return f"{stage} - DNA Reward"


VICTORY = "Sigma Defeated"
