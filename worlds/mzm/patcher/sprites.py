from enum import StrEnum
from typing import Mapping

from .local_rom import LocalRom, get_rom_address
from .symbols import get_symbol


class Sprite(StrEnum):
    EnergyTank = "Energy Tank"
    MissileTank = "Missile Tank"
    SuperMissileTank = "Super Missile Tank"
    PowerBombTank = "Power Bomb Tank"
    LongBeam = "Long Beam"
    ChargeBeam = "Charge Beam"
    IceBeam = "Ice Beam"
    WaveBeam = "Wave Beam"
    UnknownPlasmaBeam = "Unknown Plasma Beam"
    PlasmaBeam = "Plasma Beam"
    Bomb = "Bomb"
    VariaSuit = "Varia Suit"
    UnknownGravitySuit = "Unknown Gravity Suit"
    GravitySuit = "Gravity Suit"
    MorphBall = "Morph Ball"
    SpeedBooster = "Speed Booster"
    HiJump = "Hi-Jump"
    ScrewAttack = "Screw Attack"
    UnknownSpaceJump = "Unknown Space Jump"
    SpaceJump = "Space Jump"
    PowerGrip = "Power Grip"
    Nothing = "Nothing"
    FullyPoweredSuit = "Fully Powered Suit"
    MetroidDNA = "Metroid DNA"
    ItemSphere = "Item Sphere"
    APLogo = "AP Logo"
    APLogoProgression = "AP Progression"
    APLogoUseful = "AP Useful"
    SpazerBeam = "Spazer"
    GrappleBeam = "Grapple Beam"
    SpringBall = "Spring Ball"
    XRayScope = "X-Ray Scope"
    ReserveTank = "Reserve Tank"
    WallJump = "Wall Jump"
    PowerBeam = "Power Beam"
    SpiderBall = "Spider Ball"


builtin_sprite_pointers: Mapping[Sprite, int] = {
    Sprite.EnergyTank: get_symbol("sRandoEnergyTankSprite"),
    Sprite.MissileTank: get_symbol("sRandoMissileTankSprite"),
    Sprite.SuperMissileTank: get_symbol("sRandoSuperMissileTankSprite"),
    Sprite.PowerBombTank: get_symbol("sRandoPowerBombTankSprite"),
    Sprite.LongBeam: get_symbol("sRandoLongBeamSprite"),
    Sprite.ChargeBeam: get_symbol("sRandoChargeBeamSprite"),
    Sprite.IceBeam: get_symbol("sRandoIceBeamSprite"),
    Sprite.WaveBeam: get_symbol("sRandoWaveBeamSprite"),
    Sprite.UnknownPlasmaBeam: get_symbol("sRandoUnknownPlasmaBeamSprite"),
    Sprite.Bomb: get_symbol("sRandoBombSprite"),
    Sprite.VariaSuit: get_symbol("sRandoVariaSuitSprite"),
    Sprite.UnknownGravitySuit: get_symbol("sRandoUnknownGravitySuitSprite"),
    Sprite.MorphBall: get_symbol("sRandoMorphBallSprite"),
    Sprite.SpeedBooster: get_symbol("sRandoSpeedBoosterSprite"),
    Sprite.HiJump: get_symbol("sRandoHiJumpSprite"),
    Sprite.ScrewAttack: get_symbol("sRandoScrewAttackSprite"),
    Sprite.UnknownSpaceJump: get_symbol("sRandoUnknownSpaceJumpSprite"),
    Sprite.PowerGrip: get_symbol("sRandoPowerGripSprite"),
}


# TODO: Edited vanilla sprites could/should be diffed, segmented, or something
# Plasma Beam also
sprite_imports: Mapping[Sprite, tuple[str | int, str | int]] = {
    Sprite.PlasmaBeam: ("plasma_beam.gfx", "plasma_beam.pal"),
    Sprite.GravitySuit: ("gravity_suit.gfx", "gravity_suit.pal"),
    Sprite.SpaceJump: ("space_jump.gfx", "space_jump.pal"),
    Sprite.Nothing: ("nothing.gfx", "nothing.pal"),
    Sprite.ItemSphere: ("item_sphere.gfx", "item_sphere.pal"),
    Sprite.FullyPoweredSuit: ("fully_powered_suit.gfx", "fully_powered_suit.pal"),
    Sprite.MetroidDNA: ("metroid_dna.gfx", get_symbol("sCommonTilesPal")),
    Sprite.APLogo: ("ap_logo.gfx", "ap_logo.pal"),
    Sprite.APLogoProgression: ("ap_logo_progression.gfx", "ap_logo.pal"),
    Sprite.APLogoUseful: ("ap_logo_useful.gfx", "ap_logo.pal"),
    Sprite.SpazerBeam: ("spazer_beam.gfx", "spazer_beam.pal"),
    Sprite.GrappleBeam: ("grapple_beam.gfx", "grapple_beam.pal"),
    Sprite.SpringBall: ("spring_ball.gfx", "spring_ball.pal"),
    Sprite.XRayScope: ("xray_scope.gfx", "xray_scope.pal"),
    Sprite.ReserveTank: ("reserve_tank.gfx", get_symbol("sCommonTilesPal")),
    Sprite.WallJump: (get_symbol("sRandoHiJumpGfx"), "wall_jump.pal"),
    Sprite.PowerBeam: ("power_beam.gfx", "power_beam.pal"),
    Sprite.SpiderBall: ("spider_ball.gfx", "spider_ball.pal"),
}


def get_tile(tiledata: bytes, x: int, y: int) -> bytes:
    offset = 0x20 * x + 0x400 * y
    return tiledata[offset:offset+0x20]


def get_sprites(tileset: bytes, start_x: int, start_y: int, sprites: int, rows: int = 2):
    return b"".join(get_tile(tileset, 2 * t + x, y)
                    for t in range(sprites)
                    for y in range(start_y, start_y + rows)
                    for x in range(start_x, start_x + 2))


def make_4_frame_animation(data: bytes):
    middle_frame = data[0x80:0x100]
    return data + middle_frame


# Symbol for statue, symbol for rando gfx
CHOZO_STATUES = [
    ("LongBeam", "LongBeam"),
    ("IceBeam", "IceBeam"),
    ("WaveBeam", "WaveBeam"),
    ("Bombs", "Bomb"),
    ("Varia", "VariaSuit"),
    ("Speedbooster", "SpeedBooster"),
    ("HighJump", "HiJump"),
    ("ScrewAttack", "ScrewAttack"),
]


# Symbol, gfx offset in pixels downward
UNKNOWN_STATUES = [
    ("PlasmaBeam", 4),
    ("GravitySuit", 2),
    ("SpaceJump", 2),
]


def write_decompressed_item_sprites(rom: LocalRom):
    # This extracts the sprites for the vanilla items and writes them into some reserved space in uncompressed format
    # using the same tile layout as the tank graphics.

    for statue_name, item_name in CHOZO_STATUES:
        statue_gfx = rom.decompress_lzss(get_rom_address(f"sChozoStatue{statue_name}Gfx"))
        item_gfx = get_sprites(statue_gfx, 4, 4, 3)
        item_gfx = make_4_frame_animation(item_gfx)
        rom.write(get_rom_address(f"sRando{item_name}Gfx"), item_gfx)

    for item_name, y_offset in UNKNOWN_STATUES:
        statue_gfx = rom.decompress_lzss(get_rom_address(f"sChozoStatue{item_name}Gfx"))
        tiles = get_sprites(statue_gfx, 4, 4, 2)
        byte_offset = y_offset * 4
        # Move the graphics down by `y_offset` pixels
        shifted = (tiles[byte_offset:0x20] + tiles[0x40:0x40 + byte_offset]
                 + tiles[0x20 + byte_offset:0x40] + tiles[0x60:0x60 + byte_offset]
                 + tiles[0x40 + byte_offset:0x60] + tiles[0x80:0x80 + byte_offset]
                 + tiles[0x60 + byte_offset:0x80] + tiles[0xA0:0xA0 + byte_offset])
        item_gfx = 4 * shifted
        rom.write(get_rom_address(f"sRandoUnknown{item_name}Gfx"), item_gfx)

    # Charge Beam
    charge = rom.decompress_lzss(get_rom_address("sChargeBeamGfx"))
    charge1 = get_sprites(charge, 18, 0, 1)
    charge2 = get_sprites(charge, 20, 0, 1)
    charge3 = bytearray(charge1)
    charge3[0x20:0x40] = get_tile(charge, 22, 0)
    rom.write(get_rom_address("sRandoChargeBeamGfx"), charge1 + charge2 + charge3 + charge2)

    # Morph Ball
    morph = rom.decompress_lzss(get_rom_address("sMorphBallGfx"))
    morph_core = get_sprites(morph, 0, 0, 3)
    morph_glass = get_sprites(morph, 6, 0, 1)
    morph_composited = bytearray(len(morph_core))
    for t in range(3):
        for y in range(2):
            for i in range(0x40):
                glass_pair = morph_glass[i + 0x40 * y]
                glass_left, glass_right = glass_pair & 0xF, glass_pair >> 4
                ball_pair = morph_core[i + 0x40 * y + 0x80 * t]
                ball_left, ball_right = ball_pair & 0xF, ball_pair >> 4
                if glass_left != 0:
                    ball_left = glass_left
                if glass_right != 0:
                    ball_right = glass_right
                combined = ball_right << 4 | ball_left
                morph_composited[i + 0x40 * y + 0x80 * t] = combined
    rom.write(get_rom_address("sRandoMorphBallGfx"), make_4_frame_animation(morph_composited))

    # Power Grip
    powergrip = rom.decompress_lzss(get_rom_address("sPowerGripGfx"))
    powergrip = get_sprites(powergrip, 0, 0, 3)
    rom.write(get_rom_address("sRandoPowerGripGfx"), make_4_frame_animation(powergrip))
