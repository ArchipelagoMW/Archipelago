import json
import pkgutil

from worlds.AutoWorld import World

tileset_names = [
    "grass_hills",
    "grass_forest",
    "grass_rocks",
    "grass_clouds",
    "grass_mountains",
    "cave",
    "cave_rocks",
    "water",
    "mushroom_rocks",
    "mushroom_clouds",
    "mushroom_forest",
    "mushroom_hills",
    "mushroom_stars",
    "mushroom_cave",
    "forest",
    "logs",
    "clouds",
    "castle_pillars",
    "castle_windows",
    "castle_wall",
    "castle_small_windows",
    "ghost_house",
    "ghost_house_exit",
    "ship_exterior",
    "ship_interior",
    "switch_palace",
    "yoshi_house"
]

map_names = [
    "main",
    "yoshi",
    "vanilla",
    "forest",
    "valley",
    "special",
    "star"
]

level_palette_index = [
    0xFF,0x03,0x09,0x01,0x15,0x0A,0x04,0x12,0x19,0x06,0x07,0x12,0x09,0x0F,0x13,0x09,  # Levels 000-00F
    0x03,0x07,0xFF,0x15,0x19,0x04,0x04,0xFF,0x17,0xFF,0x14,0x12,0x02,0x05,0xFF,0x11,  # Levels 010-01F
    0x12,0x15,0x04,0x02,0x02,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 020-02F
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 030-03F
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 040-04F
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 050-05F
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 060-06F
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 070-07F
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 080-08F
    0xFF,0xFF,0xFF,0x12,0x12,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 090-09F
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 0A0-0AF
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x19,0x08,0x09,  # Levels 0B0-0BF
    0x02,0x08,0x05,0x04,0x16,0x1A,0x04,0x02,0x0C,0x19,0x19,0x09,0xFF,0x02,0x02,0x02,  # Levels 0C0-0CF
    0x04,0x04,0x05,0x12,0x14,0xFF,0x12,0x10,0x05,0xFF,0x19,0x12,0x14,0x0F,0x15,0xFF,  # Levels 0D0-0DF
    0x12,0x12,0xFF,0x04,0x15,0xFF,0x19,0x14,0x12,0x05,0x05,0x16,0x15,0x15,0x15,0x12,  # Levels 0E0-0EF
    0x16,0x15,0x15,0x09,0x19,0x04,0x04,0x13,0x18,0x15,0x15,0x16,0x15,0x19,0x15,0x04,  # Levels 0F0-0FF
    0xFF,0x11,0x08,0x02,0x1A,0x00,0x01,0x15,0xFF,0x05,0x05,0x05,0xFF,0x11,0x12,0x05,  # Levels 100-10F
    0x12,0x14,0xFF,0x0D,0x15,0x06,0x05,0x05,0x05,0x0C,0x05,0x19,0x12,0x15,0x0E,0x01,  # Levels 110-11F
    0x07,0x19,0x0E,0x0E,0xFF,0x04,0x0E,0x02,0x02,0xFF,0x09,0x04,0x0B,0x02,0xFF,0xFF,  # Levels 120-12F
    0x07,0xFF,0x0C,0xFF,0x05,0x0C,0x0C,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 130-13F
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 140-14F
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 150-15F
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 160-16F
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 170-17F
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 180-18F
    0xFF,0xFF,0xFF,0x12,0x12,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 190-19F
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,  # Levels 1A0-1AF
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x19,0x19,0x12,0x02,0x05,  # Levels 1B0-1BF
    0x02,0x07,0x05,0x05,0x03,0x03,0x00,0xFF,0x0F,0x10,0x05,0x05,0x12,0x11,0x14,0x14,  # Levels 1C0-1CF
    0x11,0x12,0x12,0x12,0x11,0x03,0x03,0x19,0x19,0x15,0x16,0x15,0x15,0x15,0xFF,0x05,  # Levels 1D0-1DF
    0x10,0x02,0x06,0x06,0x19,0x05,0x16,0x16,0x15,0x15,0x15,0xFF,0x06,0x05,0x05,0x06,  # Levels 1E0-1EF
    0x05,0x05,0x12,0x14,0x12,0x05,0xFF,0x19,0x05,0x16,0x15,0x15,0x11,0x05,0x12,0x09   # Levels 1F0-1FF
]

mario_palettes = [
    [0x5F, 0x63, 0x1D, 0x58, 0x0A, 0x00, 0x1F, 0x39, 0xC4, 0x44, 0x08, 0x4E, 0x70, 0x67, 0xB6, 0x30, 0xDF, 0x35, 0xFF, 0x03], # Mario
    [0x3F, 0x4F, 0x1D, 0x58, 0x40, 0x11, 0xE0, 0x3F, 0x07, 0x3C, 0xAE, 0x7C, 0xB3, 0x7D, 0x00, 0x2F, 0x5F, 0x16, 0xFF, 0x03], # Luigi
    [0x5F, 0x63, 0x1D, 0x58, 0x0A, 0x00, 0x1F, 0x03, 0xC4, 0x44, 0x08, 0x4E, 0x70, 0x67, 0x16, 0x02, 0xDF, 0x35, 0xFF, 0x03], # Wario
    [0x5F, 0x63, 0x1D, 0x58, 0x0A, 0x00, 0x12, 0x7C, 0xC4, 0x44, 0x08, 0x4E, 0x70, 0x67, 0x0D, 0x58, 0xDF, 0x35, 0xFF, 0x03], # Waluigi
    [0x5F, 0x63, 0x1D, 0x58, 0x0A, 0x00, 0x00, 0x7C, 0xC4, 0x44, 0x08, 0x4E, 0x70, 0x67, 0x00, 0x58, 0xDF, 0x35, 0xFF, 0x03], # Geno
    [0x5F, 0x63, 0x1D, 0x58, 0x0A, 0x00, 0x1F, 0x7C, 0xC4, 0x44, 0x08, 0x4E, 0x70, 0x67, 0x16, 0x58, 0xDF, 0x35, 0xFF, 0x03], # Princess
    [0x5F, 0x63, 0x1D, 0x58, 0x0A, 0x00, 0xE0, 0x00, 0xC4, 0x44, 0x08, 0x4E, 0x70, 0x67, 0x80, 0x00, 0xDF, 0x35, 0xFF, 0x03], # Dark
    [0x5F, 0x63, 0x1D, 0x58, 0x0A, 0x00, 0xFF, 0x01, 0xC4, 0x44, 0x08, 0x4E, 0x70, 0x67, 0x5F, 0x01, 0xDF, 0x35, 0xFF, 0x03], # Sponge
]

fire_mario_palettes = [
    [0x5F, 0x63, 0x1D, 0x58, 0x29, 0x25, 0xFF, 0x7F, 0x08, 0x00, 0x17, 0x00, 0x1F, 0x00, 0x7B, 0x57, 0xDF, 0x0D, 0xFF, 0x03], # Mario
    [0x1F, 0x3B, 0x1D, 0x58, 0x29, 0x25, 0xFF, 0x7F, 0x40, 0x11, 0xE0, 0x01, 0xE0, 0x02, 0x7B, 0x57, 0xDF, 0x0D, 0xFF, 0x03], # Luigi
    [0x5F, 0x63, 0x1D, 0x58, 0x29, 0x25, 0xFF, 0x7F, 0x08, 0x00, 0x16, 0x02, 0x1F, 0x03, 0x7B, 0x57, 0xDF, 0x0D, 0xFF, 0x03], # Wario
    [0x5F, 0x63, 0x1D, 0x58, 0x29, 0x25, 0xFF, 0x7F, 0x08, 0x00, 0x0D, 0x58, 0x12, 0x7C, 0x7B, 0x57, 0xDF, 0x0D, 0xFF, 0x03], # Waluigi
    [0x5F, 0x63, 0x1D, 0x58, 0x29, 0x25, 0xFF, 0x7F, 0x08, 0x00, 0x00, 0x58, 0x00, 0x7C, 0x7B, 0x57, 0xDF, 0x0D, 0xFF, 0x03], # Geno
    [0x5F, 0x63, 0x1D, 0x58, 0x29, 0x25, 0xFF, 0x7F, 0x08, 0x00, 0x16, 0x58, 0x1F, 0x7C, 0x7B, 0x57, 0xDF, 0x0D, 0xFF, 0x03], # Princess
    [0x5F, 0x63, 0x1D, 0x58, 0x29, 0x25, 0xFF, 0x7F, 0x08, 0x00, 0x80, 0x00, 0xE0, 0x00, 0x7B, 0x57, 0xDF, 0x0D, 0xFF, 0x03], # Dark
    [0x5F, 0x63, 0x1D, 0x58, 0x29, 0x25, 0xFF, 0x7F, 0x08, 0x00, 0x5F, 0x01, 0xFF, 0x01, 0x7B, 0x57, 0xDF, 0x0D, 0xFF, 0x03], # Sponge
]

ow_mario_palettes = [
    [0x16, 0x00, 0x1F, 0x00], # Mario
    [0x80, 0x02, 0xE0, 0x03], # Luigi
    [0x16, 0x02, 0x1F, 0x03], # Wario
    [0x0D, 0x58, 0x12, 0x7C], # Waluigi
    [0x00, 0x58, 0x00, 0x7C], # Geno
    [0x16, 0x58, 0x1F, 0x7C], # Princess
    [0x80, 0x00, 0xE0, 0x00], # Dark
    [0x5F, 0x01, 0xFF, 0x01], # Sponge
]

level_music_address_data = [
    0x284DB,
    0x284DC,
    0x284DD,
    0x284DE,
    0x284DF,
    0x284E0,
    0x284E1,
    0x284E2,
]

level_music_value_data = [
    0x02,
    0x06,
    0x01,
    0x08,
    0x07,
    0x03,
    0x05,
    0x12,
]

ow_music_address_data = [
    [0x25BC8, 0x20D8A],
    [0x25BC9, 0x20D8B],
    [0x25BCA, 0x20D8C],
    [0x25BCB, 0x20D8D],
    [0x25BCC, 0x20D8E],
    [0x25BCD, 0x20D8F],
    [0x25BCE, 0x20D90],
    [0x16C7]
]

ow_music_value_data = [
    0x02,
    0x03,
    0x04,
    0x06,
    0x07,
    0x09,
    0x05,
    0x01,
]

valid_foreground_palettes = {
    0x00: [0x00, 0x01, 0x03, 0x04, 0x05, 0x07], # Normal 1
    0x01: [0x03, 0x04, 0x05, 0x07],             # Castle 1
    0x02: [0x01, 0x02, 0x03, 0x04, 0x05, 0x07], # Rope 1
    0x03: [0x02, 0x03, 0x04, 0x05, 0x07],       # Underground 1
    0x04: [0x01, 0x02, 0x03, 0x04, 0x05, 0x07], # Switch Palace 1
    0x05: [0x04, 0x05],                         # Ghost House 1
    0x06: [0x01, 0x02, 0x03, 0x04, 0x05, 0x07], # Rope 2
    0x07: [0x00, 0x01, 0x03, 0x04, 0x05, 0x07], # Normal 2
    0x08: [0x01, 0x02, 0x03, 0x04, 0x05, 0x07], # Rope 3
    0x09: [0x01, 0x02, 0x03, 0x04, 0x05, 0x07], # Underground 2
    0x0A: [0x01, 0x02, 0x03, 0x04, 0x05, 0x07], # Switch Palace 2
    0x0B: [0x03, 0x04, 0x05, 0x07],             # Castle 2
    #0x0C: [],                                  # Cloud/Forest
    0x0D: [0x04, 0x05],                         # Ghost House 2
    0x0E: [0x02, 0x03, 0x04, 0x05, 0x07],       # Underground 3
}

valid_background_palettes = {
    0x06861B: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Ghost House Exit
    0xFFD900: [0x01],                                           # P. Hills
    0xFFDAB9: [0x04],                                           # Water
    0xFFDC71: [0x00, 0x01, 0x02, 0x03, 0x05, 0x06, 0x07],       # Hills & Clouds
    0xFFDD44: [0x00, 0x01, 0x02, 0x03, 0x05, 0x06, 0x07],       # Clouds
    0xFFDE54: [0x00, 0x01, 0x02, 0x03, 0x05, 0x06, 0x07],       # Small Hills
    0xFFDF59: [0x00, 0x01, 0x02, 0x03, 0x05, 0x06, 0x07],       # Mountains & Clouds
    0xFFE103: [0x00, 0x01, 0x02, 0x03, 0x05, 0x06, 0x07],       # Castle Pillars
    0xFFE472: [0x00, 0x01, 0x02, 0x03, 0x05, 0x06, 0x07],       # Big Hills
    0xFFE674: [0x00, 0x01, 0x02, 0x03, 0x05, 0x06, 0x07],       # Bonus
    0xFFE684: [0x01, 0x03, 0x05, 0x06],                         # Stars
    0xFFE7C0: [0x00, 0x01, 0x02, 0x03, 0x05, 0x06, 0x07],       # Mountains
    0xFFE8EE: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Empty/Layer 2
    0xFFE8FE: [0x01, 0x06],                                     # Cave
    0xFFEC82: [0x00, 0x02, 0x03, 0x05, 0x06, 0x07],             # Bushes
    0xFFEF80: [0x01, 0x03, 0x05, 0x06],                         # Ghost House
    0xFFF175: [0x00, 0x01, 0x02, 0x03, 0x05, 0x06],             # Ghost Ship
    0xFFF45A: [0x01, 0x03, 0x06],                               # Castle
}

valid_background_colors = {
    0x06861B: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Ghost House Exit
    0xFFD900: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # P. Hills
    0xFFDAB9: [0x02, 0x03, 0x05],                               # Water
    0xFFDC71: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Hills & Clouds
    0xFFDD44: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Clouds
    0xFFDE54: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Small Hills
    0xFFDF59: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Mountains & Clouds
    0xFFE103: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Castle Pillars
    0xFFE472: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Big Hills
    0xFFE674: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Bonus
    0xFFE684: [0x02, 0x03, 0x04, 0x05],                         # Stars
    0xFFE7C0: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Mountains
    0xFFE8EE: [0x03, 0x05],                                     # Empty/Layer 2
    0xFFE8FE: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Cave
    0xFFEC82: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Bushes
    0xFFEF80: [0x03, 0x04],                                     # Ghost House
    0xFFF175: [0x02, 0x03, 0x04, 0x05],                         # Ghost Ship
    0xFFF45A: [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07], # Castle
}

valid_ow_palettes = {
    0x2D1E: [0x00, 0x01, 0x03],       # Main OW
    0x2D1F: [0x00, 0x03, 0x04],       # Yoshi's Island
    0x2D20: [0x00, 0x01, 0x03, 0x04], # Vanilla Dome
    0x2D21: [0x00, 0x02, 0x03, 0x04], # Forest of Illusion
    0x2D22: [0x00, 0x01, 0x03, 0x04], # Valley of Bowser
    0x2D24: [0x00, 0x02, 0x03],       # Star Road
}

valid_sfxs = [
    [0x01, 1],      # Jump
    [0x01, 0],      # Hit head
    [0x02, 0],      # Contact/Spinjump on an enemy
    [0x03, 0],      # Kick item
    [0x04, 0],      # Go in pipe, get hurt
    [0x05, 0],      # Midway point
    [0x06, 0],      # Yoshi gulp
    [0x07, 0],      # Dry bones collapse
    [0x08, 0],      # Kill enemy with a spin jump
    [0x09, 0],      # Fly with cape
    [0x0A, 0],      # Get powerup
    [0x0B, 0],      # ON/OFF switch
    [0x0C, 0],      # Carry item past the goal
    [0x0D, 0],      # Get cape
    [0x0E, 0],      # Swim 
    [0x0F, 0],      # Hurt while flying
    [0x10, 0],      # Magikoopa shoot magic
    [0x13, 0],      # Enemy stomp #1
    [0x14, 0],      # Enemy stomp #2
    [0x15, 0],      # Enemy stomp #3
    [0x16, 0],      # Enemy stomp #4
    [0x17, 0],      # Enemy stomp #5
    [0x18, 0],      # Enemy stomp #6
    [0x19, 0],      # Enemy stomp #7
    [0x1C, 0],      # Yoshi Coin
    [0x1E, 0],      # P-Balloon
    [0x1F, 0],      # Koopaling defeated
    [0x20, 0],      # Yoshi spit
    [0x23, 0],      # Lemmy/Wendy falling
    [0x25, 0],      # Blargg roar
    [0x26, 0],      # Firework whistle
    [0x27, 0],      # Firework bang
    [0x2A, 0],      # Peach pops up from the Clown Car
    [0x04, 1],      # Grinder
    [0x01, 3],      # Coin
    [0x02, 3],      # Hit a ? block
    [0x03, 3],      # Hit a block with a vine inside
    [0x04, 3],      # Spin jump
    [0x05, 3],      # 1up
    [0x06, 3],      # Shatter block
    [0x07, 3],      # Shoot fireball
    [0x08, 3],      # Springboard
    [0x09, 3],      # Bullet bill
    [0x0A, 3],      # Egg hatch
    [0x0B, 3],      # Item going into item box
    [0x0C, 3],      # Item falls from item box
    [0x0E, 3],      # L/R scroll
    [0x0F, 3],      # Door
    [0x13, 3],      # Lose Yoshi
    [0x14, 3],      # SMW2: New level available
    [0x15, 3],      # OW tile reveal
    [0x16, 3],      # OW castle collapse
    [0x17, 3],      # Fire spit
    [0x18, 3],      # Thunder
    [0x19, 3],      # Clap
    [0x1A, 3],      # Castle bomb
    [0x1C, 3],      # OW switch palace block ejection
    [0x1E, 3],      # Whistle
    [0x1F, 3],      # Yoshi mount
    [0x20, 3],      # Lemmy/Wendy going in lava
    [0x21, 3],      # Yoshi's tongue
    [0x22, 3],      # Message box hit
    [0x23, 3],      # Landing in a level tile
    [0x24, 3],      # P-Switch running out
    [0x25, 3],      # Yoshi defeats an enemy
    [0x26, 3],      # Swooper
    [0x27, 3],      # Podoboo
    [0x28, 3],      # Enemy hurt
    [0x29, 3],      # Correct
    [0x2A, 3],      # Wrong
    [0x2B, 3],      # Firework whistle
    [0x2C, 3]       # Firework bang
]

game_sfx_calls = [
    0x0565E,       # Jump
    0x1BABD,       # Spin jump
    0x06D41,       # Hit head on ceiling
    0x0B4F2,       # Hit head on sprite
    0x07EB5,       # Shooting a fireball
    0x0507B,       # Cape spin
    0x058A8,       # Cape smash
    0x075F3,       # Taking damage
    0x075E2,       # Taking damage while flying
    0x07919,       # Something during a boss fight
    0x05AA9,       # Swim
    0x1BC04,       # Spin jump off water
    0x05BA5,       # Jump off a net
    0x05BB2,       # Punching a net
    0x06C10,       # Entering a door
    0x05254,       # Entering a pipe #1
    0x07439,       # Entering a pipe #2
    0x052A5,       # Shot from a diagonal pipe
    0x072E8,       # Hit a midway point
    0x07236,       # Hit a wrong block
    0x07B7D,       # Spawn a powerup during the goal tape
    0x1C342,       # Invisible mushroom spawn
    0x04E3F,       # Scrolling the screen with L/R
    0x0AAFD,       # Pressing a P-Switch
    0x04557,       # P-Switch running out
    0x0BAD7,       # Climbing door turning
    0x0C109,       # Break goal tape
    0x0C548,       # Putting item in item box
    0x10012,       # Trigger item box
    0x2B34D,       # Collecting a coin
    0x07358,       # Collecting a Yoshi Coin
    0x0C57A,       # Collecting a powerup (generic)
    0x0C59C,       # Collecting a feather
    0x0C309,       # Collecting a P-Balloon
    0x0E6A9,       # Bouncing off a springboard
    0x1117D,       # Bouncing off a note block
    0x14DEC,       # Bouncing off a wall springboard
    0x1067F,       # Block shattering
    0x1081E,       # Activate ON/OFF switch #1
    0x1118C,       # Activate ON/OFF switch #2
    0x12045,       # Fireballs hitting a block/sprite
    0x12124,       # Fireballs converting an enemy into a coin
    0x12106,       # Fireballs defeating a Chuck
    0x18D7D,       # Activating a message box
    0x1C209,       # Activating a red question block
    0x0A290,       # Baby Yoshi swallowing an item #1
    0x1C037,       # Baby Yoshi swallowing an item #2
    0x0F756,       # Yoshi egg hatching
    0x0A2C5,       # Yoshi growing #1
    0x1C06C,       # Yoshi growing #2
    0x0ED5F,       # Mounting Yoshi
    0x0F71D,       # Yoshi hurt
    0x12481,       # Yoshi hurt (projectiles)
    0x0EF0E,       # Yoshi flying
    0x06F90,       # Yoshi stomping an enemy
    0x06FB6,       # Yoshi ground pound (yellow shell)
    0x07024,       # Yoshi bounces off a triangle
    0x11BE9,       # Yoshi stomping the ground
    0x0F0D3,       # Yoshi swallowing a sprite
    0x0F0FD,       # Yoshi eating a green berry
    0x1BA7D,       # Yoshi sticking out tongue
    0x0F5A1,       # Yoshi unable to eat
    0x0F2DF,       # Yoshi spitting out an item
    0x0F28F,       # Yoshi spitting out flames
    0x0F3EC,       # Collecting Yoshi's wings (eaten)
    0x0F6C8,       # Collecting Yoshi's wings (touched)
    0x7FE04,       # Defeated sprite combo #1 (using Y index)
    0x7FE0E,       # Defeated sprite combo #2 (using Y index)
    0x7FE18,       # Defeated sprite combo #3 (using Y index)
    0x7FE22,       # Defeated sprite combo #4 (using Y index)
    0x7FE2C,       # Defeated sprite combo #5 (using Y index)
    0x7FE36,       # Defeated sprite combo #6 (using Y index)
    0x7FE40,       # Defeated sprite combo #7 (using Y index)
    0x7FE4B,       # Defeated sprite combo #1 (using X index)
    0x7FE55,       # Defeated sprite combo #2 (using X index)
    0x7FE5F,       # Defeated sprite combo #3 (using X index)
    0x7FE69,       # Defeated sprite combo #4 (using X index)
    0x7FE73,       # Defeated sprite combo #5 (using X index)
    0x7FE7D,       # Defeated sprite combo #6 (using X index)
    0x7FE87,       # Defeated sprite combo #7 (using X index)
    0x0A728,       # Kicking a carryable item
    0x0B12F,       # Kicking a stunned and vulnerable enemy
    0x0A8D8,       # Performing a spinjump on a immune enemy
    0x0A93F,       # Defeating an enemy via spinjump
    0x0999E,       # Thrown sprite hitting the ground from the side
    0x192B8,       # Creating/Eating block moving
    0x195EC,       # Rex stomped
    0x134A7,       # Bullet bill blaster shooting
    0x13088,       # Bullet bill generator #1
    0x130DF,       # Bullet bill generator #2
    0x09631,       # Bob-omb explosion
    0x15918,       # Popping a bubble
    0x15D64,       # Sumo bro stomping the ground
    0x15ECC,       # Sumo bro lightning spawning flames
    0x1726B,       # Bouncing off wiggler
    0x08390,       # Banzai bill spawn
    0x0AF17,       # Thwomp hitting the ground
    0x0AFFC,       # Thwimp hitting the ground
    0x14707,       # Chuck running
    0x14381,       # Chuck whistling
    0x144F8,       # Chuck clapping
    0x14536,       # Chuck jumping
    0x145AE,       # Chuck splitting
    0x147D2,       # Chuck bounce
    0x147F6,       # Chuck hurt
    0x147B8,       # Chuck defeated
    0x19D55,       # Dino torch shooting fire
    0x19FFA,       # Blargg attacking
    0x188FF,       # Swooper bat swooping
    0x08584,       # Bowser statue flame spawn
    0x18ADA,       # Bowser statue shooting a flame
    0x13043,       # Bowser statue flame from generator
    0x0BF28,       # Magikoopa shooting a magic spell
    0x0BC5F,       # Magikoopa's magic spell hitting the ground
    0x0D745,       # Line guided sprites' motor
    0x0DB70,       # Grinder sound
    0x0E0A1,       # Podoboo jumping
    0x0E5F2,       # Dry bones/Bony beetle collapsing
    0x15474,       # Giant wooden pillar hitting the ground
    0x2C9C1,       # Spiked columns hitting the ground
    0x19B03,       # Reznor shooting a fireball
    0x19A66,       # Reznor: Hitting a platform
    0x1D752,       # Reznor: Bridge collapsing
    0x19ABB,       # Reznor: Defeated
    0x180E9,       # Big Boo: Reappearing
    0x18233,       # Big Boo: Hurt
    0x181DE,       # Big Boo: Defeated
    0x1CEC1,       # Wendy/Lemmy: Hitting a dummy
    0x1CECB,       # Wendy/Lemmy: Hurt
    0x1CE33,       # Wendy/Lemmy: Hurt (correct)
    0x1CE46,       # Wendy/Lemmy: Hurt (incorrect)
    0x1CE24,       # Wendy/Lemmy: Defeated
    0x1CE7E,       # Wendy/Lemmy: Falling into lava
    0x0CF0A,       # Ludwig: Jumping
    0x0D059,       # Ludwig: Shooting a fireball
    0x10414,       # Morton/Roy: Pillar drop
    0x0D299,       # Morton/Roy: Ground smash
    0x0D3AB,       # Morton/Roy/Ludwig: Hit by a fireball
    0x0D2FD,       # Morton/Roy/Ludwig: Bouncing off
    0x0D31E,       # Morton/Roy/Ludwig: Bouncing off (immune)
    0x0D334,       # Morton/Roy/Ludwig: Bouncing off (immune, going up a wall)
    0x0CFD0,       # Morton/Roy/Ludwig: Defeated
    0x0FCCE,       # Iggy/Larry: Being hit
    0x0FD40,       # Iggy/Larry: Being hit by a fireball
    0x0FB60,       # Iggy/Larry: Falling in lava
    0x1A8B2,       # Peach emerging from Clown Car
    0x1A8E3,       # Peach throwing an item
    0x1B0B8,       # Bumping into Clown Car
    0x1B129,       # Bowser: Hurt
    0x1AB8C,       # Bowser: Slamming the ground (third phase)
    0x1A5D0,       # Bowser: Throwing a Mechakoopa
    0x1A603,       # Bowser: Dropping a ball
    0x1A7F6,       # Bowser: Spawning a flame
    0x1B1A3,       # Bowser's ball slam #1
    0x1B1B1,       # Bowser's ball slam #2
    0x1E016,       # Bowser's arena lightning effect
    0x26CAA,       # Map: Level tile reveal
    0x26763,       # Map: Terrain reveal
    0x21170,       # Map: Using a star
    0x2666F,       # Map: Castle destruction
    0x272A4,       # Map: Switch palace blocks spawning
    0x203CC,       # Map: Earthquake
    0x27A78,       # Map: Fish jumping
    0x27736,       # Map: Valley of bowser thunder
    0x013C0,       # Menu: Nintendo presents
    0x01AE3,       # Menu: File menu option select
    0x01AF9,       # Menu: File menu option change
    0x01BBB,       # Menu: Saving game
    0x273FF,       # Menu: Map misc menu appearing
    0x27567,       # Menu: Something during the map
    0x1767A,       # Cutscene: Castle door opening
    0x17683,       # Cutscene: Castle door closing
    0x17765,       # Cutscene: Ghost house door opening
    0x1776E,       # Cutscene: Ghost house door closing
    0x04720,       # Cutscene: Detonator fuse
    0x04732,       # Cutscene: Bouncing off something
    0x0475F,       # Cutscene: Tossing the castle
    0x04798,       # Cutscene: Picking up the castle
    0x047AC,       # Cutscene: Huff
    0x047D1,       # Cutscene: Hitting a castle
    0x1C830,       # Cutscene: Shooting a firework
    0x625AF,       # Cutscene: Egg shattering
    0x64F2C,       # Cutscene: Hitting a hill
    0x6512A,       # Cutscene: Castle crashing
    0x65295,       # Cutscene: Explosion
    0x652B2,       # Cutscene: Castle sinking
    0x652BD,       # Cutscene: Castle flying
    0x652D8,       # Cutscene: Fake explosion
    0x653E7,       # Cutscene: Castle being hit by a hammer
    0x657D8        # Cutscene: Castle being mopped away
]

def generate_shuffled_sfx(rom, world: World):
    # Adjust "hitting sprites in succession" codes
    rom.write_bytes(0x0A60B, bytearray([0x22, 0x00, 0xFE, 0x0F, 0xEA, 0xEA]))    # jsl $0FFE00 : nop #2     # Thrown sprites combo #1
    rom.write_bytes(0x0A659, bytearray([0x22, 0x47, 0xFE, 0x0F, 0xEA, 0xEA]))    # jsl $0FFE47 : nop #2     # Thrown sprites combo #2
    rom.write_bytes(0x0A865, bytearray([0x22, 0x47, 0xFE, 0x0F, 0xEA, 0xEA]))    # jsl $0FFE47 : nop #2     # Star combo
    rom.write_bytes(0x0AB57, bytearray([0x22, 0x00, 0xFE, 0x0F, 0xEA, 0xEA]))    # jsl $0FFE00 : nop #2     # Bouncing off enemies
    rom.write_bytes(0x172C0, bytearray([0x22, 0x00, 0xFE, 0x0F, 0xEA, 0xEA]))    # jsl $0FFE00 : nop #2     # Star combo (wigglers)
    rom.write_bytes(0x1961D, bytearray([0x22, 0x00, 0xFE, 0x0F, 0xEA, 0xEA]))    # jsl $0FFE00 : nop #2     # Star combo (rexes)
    rom.write_bytes(0x19639, bytearray([0x22, 0x00, 0xFE, 0x0F, 0xEA, 0xEA]))    # jsl $0FFE00 : nop #2     # Bouncing off rexes

    COMBO_SFX_ADDR = 0x7FE00
    rom.write_bytes(COMBO_SFX_ADDR + 0x0000, bytearray([0xC0, 0x01]))                         # COMBO_Y:                    CPY #$01
    rom.write_bytes(COMBO_SFX_ADDR + 0x0002, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE0A
    rom.write_bytes(COMBO_SFX_ADDR + 0x0004, bytearray([0xA9, 0x13]))                         #                             LDA #$13
    rom.write_bytes(COMBO_SFX_ADDR + 0x0006, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x0009, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x000A, bytearray([0xC0, 0x02]))                         # label_0FFE0A:               CPY #$02
    rom.write_bytes(COMBO_SFX_ADDR + 0x000C, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE14
    rom.write_bytes(COMBO_SFX_ADDR + 0x000E, bytearray([0xA9, 0x14]))                         #                             LDA #$14
    rom.write_bytes(COMBO_SFX_ADDR + 0x0010, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x0013, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x0014, bytearray([0xC0, 0x03]))                         # label_0FFE14:               CPY #$03
    rom.write_bytes(COMBO_SFX_ADDR + 0x0016, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE1E
    rom.write_bytes(COMBO_SFX_ADDR + 0x0018, bytearray([0xA9, 0x15]))                         #                             LDA #$15
    rom.write_bytes(COMBO_SFX_ADDR + 0x001A, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x001D, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x001E, bytearray([0xC0, 0x04]))                         # label_0FFE1E:               CPY #$04
    rom.write_bytes(COMBO_SFX_ADDR + 0x0020, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE28
    rom.write_bytes(COMBO_SFX_ADDR + 0x0022, bytearray([0xA9, 0x16]))                         #                             LDA #$16
    rom.write_bytes(COMBO_SFX_ADDR + 0x0024, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x0027, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x0028, bytearray([0xC0, 0x05]))                         # label_0FFE28:               CPY #$05
    rom.write_bytes(COMBO_SFX_ADDR + 0x002A, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE32
    rom.write_bytes(COMBO_SFX_ADDR + 0x002C, bytearray([0xA9, 0x17]))                         #                             LDA #$17
    rom.write_bytes(COMBO_SFX_ADDR + 0x002E, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x0031, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x0032, bytearray([0xC0, 0x06]))                         # label_0FFE32:               CPY #$06
    rom.write_bytes(COMBO_SFX_ADDR + 0x0034, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE3C
    rom.write_bytes(COMBO_SFX_ADDR + 0x0036, bytearray([0xA9, 0x18]))                         #                             LDA #$18
    rom.write_bytes(COMBO_SFX_ADDR + 0x0038, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x003B, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x003C, bytearray([0xC0, 0x07]))                         # label_0FFE3C:               CPY #$07
    rom.write_bytes(COMBO_SFX_ADDR + 0x003E, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE46
    rom.write_bytes(COMBO_SFX_ADDR + 0x0040, bytearray([0xA9, 0x19]))                         #                             LDA #$19
    rom.write_bytes(COMBO_SFX_ADDR + 0x0042, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x0045, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x0046, bytearray([0x6B]))                               # label_0FFE46:               RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x0047, bytearray([0xE0, 0x01]))                         # COMBO_X:                    CPX #$01
    rom.write_bytes(COMBO_SFX_ADDR + 0x0049, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE51
    rom.write_bytes(COMBO_SFX_ADDR + 0x004B, bytearray([0xA9, 0x13]))                         #                             LDA #$13
    rom.write_bytes(COMBO_SFX_ADDR + 0x004D, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x0050, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x0051, bytearray([0xE0, 0x02]))                         # label_0FFE51:               CPX #$02
    rom.write_bytes(COMBO_SFX_ADDR + 0x0053, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE5B
    rom.write_bytes(COMBO_SFX_ADDR + 0x0055, bytearray([0xA9, 0x14]))                         #                             LDA #$14
    rom.write_bytes(COMBO_SFX_ADDR + 0x0057, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x005A, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x005B, bytearray([0xE0, 0x03]))                         # label_0FFE5B:               CPX #$03
    rom.write_bytes(COMBO_SFX_ADDR + 0x005D, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE65
    rom.write_bytes(COMBO_SFX_ADDR + 0x005F, bytearray([0xA9, 0x15]))                         #                             LDA #$15
    rom.write_bytes(COMBO_SFX_ADDR + 0x0061, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x0064, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x0065, bytearray([0xE0, 0x04]))                         # label_0FFE65:               CPX #$04
    rom.write_bytes(COMBO_SFX_ADDR + 0x0067, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE6F
    rom.write_bytes(COMBO_SFX_ADDR + 0x0069, bytearray([0xA9, 0x16]))                         #                             LDA #$16
    rom.write_bytes(COMBO_SFX_ADDR + 0x006B, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x006E, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x006F, bytearray([0xE0, 0x05]))                         # label_0FFE6F:               CPX #$05
    rom.write_bytes(COMBO_SFX_ADDR + 0x0071, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE79
    rom.write_bytes(COMBO_SFX_ADDR + 0x0073, bytearray([0xA9, 0x17]))                         #                             LDA #$17
    rom.write_bytes(COMBO_SFX_ADDR + 0x0075, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x0078, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x0079, bytearray([0xE0, 0x06]))                         # label_0FFE79:               CPX #$06
    rom.write_bytes(COMBO_SFX_ADDR + 0x007B, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE83
    rom.write_bytes(COMBO_SFX_ADDR + 0x007D, bytearray([0xA9, 0x18]))                         #                             LDA #$18
    rom.write_bytes(COMBO_SFX_ADDR + 0x007F, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x0082, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x0083, bytearray([0xE0, 0x07]))                         # label_0FFE83:               CPX #$07
    rom.write_bytes(COMBO_SFX_ADDR + 0x0085, bytearray([0xD0, 0x06]))                         #                             BNE label_0FFE8D
    rom.write_bytes(COMBO_SFX_ADDR + 0x0087, bytearray([0xA9, 0x19]))                         #                             LDA #$19
    rom.write_bytes(COMBO_SFX_ADDR + 0x0089, bytearray([0x8D, 0xF9, 0x1D]))                   #                             STA $1DF9
    rom.write_bytes(COMBO_SFX_ADDR + 0x008C, bytearray([0x6B]))                               #                             RTL
    rom.write_bytes(COMBO_SFX_ADDR + 0x008D, bytearray([0x6B]))                               # label_0FFE8D:               RTL

    # Adjust "Hit head on ceiling" code
    rom.write_bytes(0x06D41 + 0x00, bytearray([0xA9, 0x01]))                # lda #$01
    rom.write_bytes(0x06D41 + 0x02, bytearray([0x8D, 0xF9, 0x1D]))          # sta $1DF9
    rom.write_bytes(0x06D41 + 0x05, bytearray([0xEA, 0xEA, 0xEA, 0xEA]))    # nop #4

    # Manually add "Map: Stepping onto a level tile" random SFX
    selected_sfx = world.random.choice(valid_sfxs)
    rom.write_byte(0x2169F + 0x01, selected_sfx[0])
    rom.write_byte(0x2169F + 0x04, selected_sfx[1] + 0xF9)

    # Disable panning on Bowser's flames
    rom.write_bytes(0x1A83D, bytearray([0xEA, 0xEA, 0xEA]))    # nop #3

    # Randomize SFX calls
    for address in game_sfx_calls:
        # Get random SFX
        if world.options.sfx_shuffle != "singularity":
            selected_sfx = world.random.choice(valid_sfxs)
        # Write randomized SFX num
        rom.write_byte(address + 0x01, selected_sfx[0])
        # Write randomized SFX port
        rom.write_byte(address + 0x03, selected_sfx[1] + 0xF9)

def generate_shuffled_level_music(world: World):
    shuffled_level_music = level_music_value_data.copy()

    if world.options.music_shuffle == "consistent":
        world.random.shuffle(shuffled_level_music)
    elif world.options.music_shuffle == "singularity":
        single_song = world.random.choice(shuffled_level_music)
        shuffled_level_music = [single_song for i in range(len(shuffled_level_music))]

    return shuffled_level_music

def generate_shuffled_ow_music(world: World):
    shuffled_ow_music = ow_music_value_data.copy()

    if world.options.music_shuffle == "consistent" or world.options.music_shuffle == "full":
        world.random.shuffle(shuffled_ow_music)
    elif world.options.music_shuffle == "singularity":
        single_song = world.random.choice(shuffled_ow_music)
        shuffled_ow_music = [single_song for i in range(len(shuffled_ow_music))]

    return shuffled_ow_music

def generate_shuffled_ow_palettes(rom, world: World):
    if world.options.overworld_palette_shuffle != "on_legacy":
        return

    for address, valid_palettes in valid_ow_palettes.items():
        chosen_palette = world.random.choice(valid_palettes)
        rom.write_byte(address, chosen_palette)

def generate_shuffled_header_data(rom, world: World):
    if world.options.music_shuffle != "full" and world.options.level_palette_shuffle != "on_legacy":
        return

    for level_id in range(0, 0x200):
        layer1_ptr_list = list(rom.read_bytes(0x2E000 + level_id * 3, 3))
        layer1_ptr = (layer1_ptr_list[2] << 16 | layer1_ptr_list[1] << 8 | layer1_ptr_list[0])

        if layer1_ptr == 0x68000:
            # Unused Levels
            continue

        if layer1_ptr >= 0x70000:
            layer1_ptr -= 0x8000

        layer1_ptr -= 0x38000

        level_header = list(rom.read_bytes(layer1_ptr, 5))

        tileset = level_header[4] & 0x0F

        if world.options.music_shuffle == "full":
            level_header[2] &= 0x8F
            level_header[2] |= (world.random.randint(0, 7) << 5)

        if world.options.level_palette_shuffle == "on_legacy":
            if tileset in valid_foreground_palettes:
                level_header[3] &= 0xF8
                level_header[3] |= world.random.choice(valid_foreground_palettes[tileset])

            layer2_ptr_list = list(rom.read_bytes(0x2E600 + level_id * 3, 3))
            layer2_ptr = (layer2_ptr_list[2] << 16 | layer2_ptr_list[1] << 8 | layer2_ptr_list[0])

            if layer2_ptr in valid_background_palettes:
                level_header[0] &= 0x1F
                level_header[0] |= (world.random.choice(valid_background_palettes[layer2_ptr]) << 5)

            if layer2_ptr in valid_background_colors:
                level_header[1] &= 0x1F
                level_header[1] |= (world.random.choice(valid_background_colors[layer2_ptr]) << 5)

        rom.write_bytes(layer1_ptr, bytes(level_header))

def generate_curated_level_palette_data(rom, world: World):
    PALETTE_LEVEL_CODE_ADDR = 0x88000
    PALETTE_INDEX_ADDR = 0x8F000
    PALETTE_LEVEL_TILESET_ADDR = 0x8F200
    PALETTE_LEVEL_PTR_ADDR = 0x92000
    PALETTE_LEVEL_DATA_ADDR = 0xA8000

    addr = pc_to_snes(PALETTE_LEVEL_PTR_ADDR)
    snes_level_palette_pointers_1 = bytearray([0xBF, (addr)&0xFF, (addr>>8)&0xFF, (addr>>16)&0xFF])
    snes_level_palette_pointers_2 = bytearray([0xBF, (addr+2)&0xFF, (addr>>8)&0xFF, (addr>>16)&0xFF])

    # Enable curated palette loader
    rom.write_bytes(0x02BED, bytearray([0x5C, 0x00, 0x80, 0x11])) # org $00ABED : jml custom_palettes
    rom.write_bytes(0x02330, bytearray([0x5C, 0x02, 0x80, 0x11])) # org $00A318 : jml custom_palettes_original
    rom.write_bytes(0x013D7, bytearray([0x20, 0x30, 0xA3]))       # org $0093D7 : jmp $A330
    rom.write_bytes(0x014DA, bytearray([0x20, 0x30, 0xA3]))       # org $0094DA : jmp $A330
    rom.write_bytes(0x015EC, bytearray([0x20, 0x30, 0xA3]))       # org $0095EC : jmp $A330
    rom.write_bytes(0x0165B, bytearray([0x20, 0x30, 0xA3]))       # org $00965B : jmp $A330
    rom.write_bytes(0x02DD9, bytearray([0x20, 0x30, 0xA3]))       # org $00ADD9 : jmp $A330
    rom.write_bytes(0x02E1F, bytearray([0x20, 0x30, 0xA3]))       # org $00AE1F : jmp $A330
    
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0000, bytearray([0x80, 0x09]))                #                     bra custom_palettes
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0002, bytearray([0xC2, 0x30]))                # .original           rep #$30
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0004, bytearray([0xA9, 0xDD, 0x7F]))          #                     lda #$7FDD
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0007, bytearray([0x5C, 0xF2, 0xAB, 0x00]))    #                     jml $00ABF2
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x000B, bytearray([0xC2, 0x30]))                # custom_palettes:    rep #$30
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x000D, bytearray([0xA9, 0x70, 0xB1]))          #                     lda #$B170
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0010, bytearray([0x85, 0x0A]))                #                     sta !_ptr
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0012, bytearray([0x64, 0x0C]))                #                     stz !_ptr+$02
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0014, bytearray([0xA9, 0x10, 0x00]))          #                     lda.w #$0010
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0017, bytearray([0x85, 0x04]))                #                     sta !_index
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0019, bytearray([0xA9, 0x07, 0x00]))          #                     lda #$0007
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x001C, bytearray([0x85, 0x06]))                #                     sta !_x_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x001E, bytearray([0xA9, 0x01, 0x00]))          #                     lda #$0001
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0021, bytearray([0x85, 0x08]))                #                     sta !_y_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0023, bytearray([0x20, 0xE4, 0x80]))          #                     jsr load_colors
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0026, bytearray([0xAE, 0x0B, 0x01]))          # .get_index          ldx $010B
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0029, bytearray([0xBF, 0x00, 0xF2, 0x11]))    #                     lda.l level_tilesets,x
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x002D, bytearray([0x29, 0xFF, 0x00]))          #                     and #$00FF
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0030, bytearray([0xEB]))                      #                     xba 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0031, bytearray([0x85, 0x00]))                #                     sta !_tileset
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0033, bytearray([0xBF, 0x00, 0xF0, 0x11]))    #                     lda.l level_index,x
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0037, bytearray([0x29, 0xFF, 0x00]))          #                     and #$00FF
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x003A, bytearray([0x05, 0x00]))                #                     ora !_tileset
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x003C, bytearray([0x85, 0x0A]))                #                     sta !_ptr
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x003E, bytearray([0x0A]))                      #                     asl 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x003F, bytearray([0x18]))                      #                     clc 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0040, bytearray([0x65, 0x0A]))                #                     adc !_ptr
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0042, bytearray([0x85, 0x0E]))                #                     sta !_num
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0044, bytearray([0xAA]))                      #                     tax 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0045, snes_level_palette_pointers_1)          # .back_color         lda.l palette_pointers,x
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0049, bytearray([0x85, 0x0A]))                #                     sta !_ptr
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x004B, snes_level_palette_pointers_2)          #                     lda.l palette_pointers+$02,x
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x004F, bytearray([0x85, 0x0C]))                #                     sta !_ptr+$02
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0051, bytearray([0xA7, 0x0A]))                #                     lda [!_ptr]
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0053, bytearray([0x8D, 0x01, 0x07]))          #                     sta $0701
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0056, bytearray([0xE6, 0x0A]))                #                     inc !_ptr
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0058, bytearray([0xE6, 0x0A]))                #                     inc !_ptr
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x005A, bytearray([0xA9, 0x02, 0x00]))          # .background         lda.w #$0001*$02
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x005D, bytearray([0x85, 0x04]))                #                     sta !_index
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x005F, bytearray([0xA9, 0x06, 0x00]))          #                     lda #$0006
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0062, bytearray([0x85, 0x06]))                #                     sta !_x_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0064, bytearray([0xA9, 0x01, 0x00]))          #                     lda #$0001
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0067, bytearray([0x85, 0x08]))                #                     sta !_y_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0069, bytearray([0x20, 0xE4, 0x80]))          #                     jsr load_colors
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x006C, bytearray([0xA9, 0x42, 0x00]))          # .foreground         lda.w #$0021*$02
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x006F, bytearray([0x85, 0x04]))                #                     sta !_index
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0071, bytearray([0xA9, 0x06, 0x00]))          #                     lda #$0006
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0074, bytearray([0x85, 0x06]))                #                     sta !_x_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0076, bytearray([0xA9, 0x01, 0x00]))          #                     lda #$0001
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0079, bytearray([0x85, 0x08]))                #                     sta !_y_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x007B, bytearray([0x20, 0xE4, 0x80]))          #                     jsr load_colors
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x007E, bytearray([0xA9, 0x52, 0x00]))          # .berries            lda.w #$0029*$02
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0081, bytearray([0x85, 0x04]))                #                     sta !_index
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0083, bytearray([0xA9, 0x06, 0x00]))          #                     lda #$0006
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0086, bytearray([0x85, 0x06]))                #                     sta !_x_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0088, bytearray([0xA9, 0x02, 0x00]))          #                     lda #$0002
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x008B, bytearray([0x85, 0x08]))                #                     sta !_y_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x008D, bytearray([0xA5, 0x0A]))                #                     lda !_ptr
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x008F, bytearray([0x48]))                      #                     pha 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0090, bytearray([0x20, 0xE4, 0x80]))          #                     jsr load_colors
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0093, bytearray([0x68]))                      #                     pla 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0094, bytearray([0x85, 0x0A]))                #                     sta !_ptr
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0096, bytearray([0xA9, 0x32, 0x01]))          #                     lda.w #$0099*$02
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0099, bytearray([0x85, 0x04]))                #                     sta !_index
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x009B, bytearray([0xA9, 0x06, 0x00]))          #                     lda #$0006
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x009E, bytearray([0x85, 0x06]))                #                     sta !_x_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00A0, bytearray([0xA9, 0x02, 0x00]))          #                     lda #$0002
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00A3, bytearray([0x85, 0x08]))                #                     sta !_y_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00A5, bytearray([0x20, 0xE4, 0x80]))          #                     jsr load_colors
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00A8, bytearray([0xA9, 0x82, 0x00]))          # .global             lda.w #$0041*$02
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00AB, bytearray([0x85, 0x04]))                #                     sta !_index
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00AD, bytearray([0xA9, 0x06, 0x00]))          #                     lda #$0006
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00B0, bytearray([0x85, 0x06]))                #                     sta !_x_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00B2, bytearray([0xA9, 0x0B, 0x00]))          #                     lda #$000B
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00B5, bytearray([0x85, 0x08]))                #                     sta !_y_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00B7, bytearray([0x20, 0xE4, 0x80]))          #                     jsr load_colors
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00BA, bytearray([0xA5, 0x00]))                # .sprite_specific    lda !_tileset
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00BC, bytearray([0xC9, 0x00, 0x05]))          #                     cmp #$0500
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00BF, bytearray([0xD0, 0x1D]))                #                     bne .end 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00C1, bytearray([0xAD, 0x2E, 0x19]))          #                     lda $192E
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00C4, bytearray([0x29, 0x0F, 0x00]))          #                     and #$000F
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00C7, bytearray([0xC9, 0x02, 0x00]))          #                     cmp #$0002
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00CA, bytearray([0xD0, 0x12]))                #                     bne .end
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00CC, bytearray([0xA9, 0xC2, 0x01]))          #                     lda.w #$00E1*$02
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00CF, bytearray([0x85, 0x04]))                #                     sta !_index
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00D1, bytearray([0xA9, 0x06, 0x00]))          #                     lda #$0006
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00D4, bytearray([0x85, 0x06]))                #                     sta !_x_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00D6, bytearray([0xA9, 0x01, 0x00]))          #                     lda #$0001
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00D9, bytearray([0x85, 0x08]))                #                     sta !_y_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00DB, bytearray([0x20, 0xE4, 0x80]))          #                     jsr load_colors
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00DE, bytearray([0xE2, 0x30]))                # .end                sep #$30
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00E0, bytearray([0x5C, 0xEC, 0xAC, 0x00]))    #                     jml $00ACEC
    
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00E4, bytearray([0xA6, 0x04]))                # load_colors:        ldx !_index
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00E6, bytearray([0xA4, 0x06]))                #                     ldy !_x_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00E8, bytearray([0xA7, 0x0A]))                # .x_loop             lda [!_ptr]
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00EA, bytearray([0x9D, 0x03, 0x07]))          #                     sta $0703,x
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00ED, bytearray([0xE6, 0x0A]))                #                     inc !_ptr
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00EF, bytearray([0xE6, 0x0A]))                #                     inc !_ptr
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F1, bytearray([0xE8]))                      #                     inx 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F2, bytearray([0xE8]))                      #                     inx 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F3, bytearray([0x88]))                      #                     dey 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F4, bytearray([0x10, 0xF2]))                #                     bpl .x_loop
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F6, bytearray([0xA5, 0x04]))                #                     lda !_index
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F8, bytearray([0x18]))                      #                     clc 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F9, bytearray([0x69, 0x20, 0x00]))          #                     adc #$0020
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00FC, bytearray([0x85, 0x04]))                #                     sta !_index
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00FE, bytearray([0xC6, 0x08]))                #                     dec !_y_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0100, bytearray([0x10, 0xE2]))                #                     bpl load_colors
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0102, bytearray([0x60]))                      #                     rts 

    # Load palette paths
    data = pkgutil.get_data(__name__, f"data/palettes/level/palettes.json").decode("utf-8")
    tilesets = json.loads(data)

    # Writes the level tileset index to ROM
    rom.write_bytes(PALETTE_LEVEL_TILESET_ADDR, bytearray(level_palette_index))

    # Builds the table in ROM that holds the palette index for each level, including sublevels
    for level_id in range(0x200):
        tileset_num = level_palette_index[level_id]
        if tileset_num != 0xFF:
            tileset = tileset_names[tileset_num]
        else:
            tileset = tileset_names[0x19]
        palette = world.random.randint(0, len(tilesets[tileset])-1)
        rom.write_bytes(PALETTE_INDEX_ADDR + level_id, bytearray([palette]))
        
    # Writes the actual level palette data and pointer to said data to the ROM
    pal_offset = 0x0000
    tileset_num = 0
    bank_palette_count = 0
    for tileset in tilesets.keys():
        for palette in range(len(tilesets[tileset])):
            # Handle bank crossing
            if bank_palette_count == 110:
                pal_offset = (pal_offset & 0xF8000) + 0x8000
                bank_palette_count = 0
            # Write pointer
            data_ptr = pc_to_snes(PALETTE_LEVEL_DATA_ADDR + pal_offset)
            rom.write_bytes(PALETTE_LEVEL_PTR_ADDR + ((tileset_num*3)<<8) + (palette*3), bytearray([data_ptr & 0xFF, (data_ptr>>8)&0xFF, (data_ptr>>16)&0xFF]))
            # Write data
            rom.write_bytes(PALETTE_LEVEL_DATA_ADDR + pal_offset, read_palette_file(tileset, tilesets[tileset][palette], "level"))
            pal_offset += 0x128
            bank_palette_count += 1
        tileset_num += 1

    # Fix eaten berry tiles
    EATEN_BERRY_ADDR = 0x68248
    rom.write_byte(EATEN_BERRY_ADDR + 0x01, 0x04)
    rom.write_byte(EATEN_BERRY_ADDR + 0x03, 0x04)
    rom.write_byte(EATEN_BERRY_ADDR + 0x05, 0x04)
    rom.write_byte(EATEN_BERRY_ADDR + 0x07, 0x04)

    # Fix title screen changing background colors
    rom.write_bytes(0x1D30, bytearray([0xEA, 0xEA, 0xEA]))

    # Skips level intros automatically
    rom.write_byte(0x4896, 0x80)

def generate_curated_map_palette_data(rom, world: World):
    PALETTE_MAP_CODE_ADDR = 0x88200
    PALETTE_UPLOADER_EDIT = 0x88400
    PALETTE_MAP_INDEX_ADDR = 0x8F400
    PALETTE_MAP_PTR_ADDR = 0x90000
    PALETTE_MAP_DATA_ADDR = 0x98000

    addr = pc_to_snes(PALETTE_MAP_PTR_ADDR)
    snes_map_palette_pointers_1 = bytearray([0xBF, (addr)&0xFF, (addr>>8)&0xFF, (addr>>16)&0xFF])
    snes_map_palette_pointers_2 = bytearray([0xBF, (addr+2)&0xFF, (addr>>8)&0xFF, (addr>>16)&0xFF])

    rom.write_bytes(0x02D25, bytearray([0x5C, 0x09, 0x82, 0x11])) # org $00AD25 : jml map_palettes

    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0000, bytearray([0xC2, 0x30]))                  # map_og_palettes:    rep #$30
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0002, bytearray([0xA0, 0xD8, 0xB3]))            #                     ldy #$B3D8
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0005, bytearray([0x5C, 0x2A, 0xAD, 0x00]))      #                     jml $00AD2A
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0009, bytearray([0xC2, 0x30]))                  # map_palettes:       rep #$30
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x000B, bytearray([0xAD, 0x31, 0x19]))            # .prepare_index      lda $1931
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x000E, bytearray([0x29, 0x0F, 0x00]))            #                     and #$000F
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0011, bytearray([0x3A]))                        #                     dec 
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0012, bytearray([0xAA]))                        #                     tax 
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0013, bytearray([0xEB]))                        #                     xba 
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0014, bytearray([0x85, 0x0E]))                  #                     sta !_num
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0016, bytearray([0xBF, 0x00, 0xF4, 0x11]))      #                     lda.l map_index,x
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x001A, bytearray([0x29, 0xFF, 0x00]))            #                     and #$00FF
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x001D, bytearray([0x05, 0x0E]))                  #                     ora !_num
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x001F, bytearray([0x85, 0x0A]))                  #                     sta !_ptr
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0021, bytearray([0x0A]))                        #                     asl 
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0022, bytearray([0x18]))                        #                     clc 
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0023, bytearray([0x65, 0x0A]))                  #                     adc !_ptr
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0025, bytearray([0xAA]))                        #                     tax 
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0026, snes_map_palette_pointers_1)              #                     lda.l map_palette_pointers,x
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x002A, bytearray([0x85, 0x0A]))                  #                     sta !_ptr
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x002C, snes_map_palette_pointers_2)              #                     lda.l map_palette_pointers+$02,x
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0030, bytearray([0x85, 0x0C]))                  #                     sta !_ptr+$02
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0032, bytearray([0xA7, 0x0A]))                  # .load_back_color    lda [!_ptr]
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0034, bytearray([0x8D, 0x01, 0x07]))            #                     sta $0701
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0037, bytearray([0xE6, 0x0A]))                  #                     inc !_ptr
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0039, bytearray([0xE6, 0x0A]))                  #                     inc !_ptr
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x003B, bytearray([0xA9, 0x82, 0x00]))            # .load_layer_2       lda.w #$0041*$02
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x003E, bytearray([0x85, 0x04]))                  #                     sta !_index
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0040, bytearray([0xA9, 0x06, 0x00]))            #                     lda #$0006
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0043, bytearray([0x85, 0x06]))                  #                     sta !_x_span
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0045, bytearray([0xA9, 0x03, 0x00]))            #                     lda #$0003
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0048, bytearray([0x85, 0x08]))                  #                     sta !_y_span
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x004A, bytearray([0x20, 0xE4, 0x80]))            #                     jsr load_colors
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x004D, bytearray([0xA9, 0x52, 0x00]))            # .load_layer_1       lda.w #$0029*$02
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0050, bytearray([0x85, 0x04]))                  #                     sta !_index
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0052, bytearray([0xA9, 0x06, 0x00]))            #                     lda #$0006
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0055, bytearray([0x85, 0x06]))                  #                     sta !_x_span
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0057, bytearray([0xA9, 0x05, 0x00]))            #                     lda #$0005
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x005A, bytearray([0x85, 0x08]))                  #                     sta !_y_span
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x005C, bytearray([0x20, 0xE4, 0x80]))            #                     jsr load_colors
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x005F, bytearray([0xA9, 0x10, 0x00]))            # .load_layer_3       lda.w #$0008*$02
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0062, bytearray([0x85, 0x04]))                  #                     sta !_index
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0064, bytearray([0xA9, 0x07, 0x00]))            #                     lda #$0007
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0067, bytearray([0x85, 0x06]))                  #                     sta !_x_span
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0069, bytearray([0xA9, 0x01, 0x00]))            #                     lda #$0001
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x006C, bytearray([0x85, 0x08]))                  #                     sta !_y_span
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x006E, bytearray([0x20, 0xE4, 0x80]))            #                     jsr load_colors
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0071, bytearray([0xA9, 0x02, 0x01]))            # .load_sprites       lda.w #$0081*$02
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0074, bytearray([0x85, 0x04]))                  #                     sta !_index
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0076, bytearray([0xA9, 0x06, 0x00]))            #                     lda #$0006
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0079, bytearray([0x85, 0x06]))                  #                     sta !_x_span
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x007B, bytearray([0xA9, 0x07, 0x00]))            #                     lda #$0007
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x007E, bytearray([0x85, 0x08]))                  #                     sta !_y_span
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0080, bytearray([0x20, 0xE4, 0x80]))            #                     jsr load_colors
    rom.write_bytes(PALETTE_MAP_CODE_ADDR + 0x0083, bytearray([0x5C, 0xA3, 0xAD, 0x00]))      # .return             jml $00ADA3

    rom.write_bytes(0x2488, bytearray([0x5C, 0x00, 0x84, 0x11])) # org $00A488 : jml palette_upload

    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0000, bytearray([0xAD, 0x00, 0x01]))            # palette_upload:     lda $0100
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0003, bytearray([0xC9, 0x0E]))                  #                     cmp #$0E
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0005, bytearray([0xF0, 0x0A]))                  #                     beq .map
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0007, bytearray([0xAC, 0x80, 0x06]))            # .regular            ldy $0680
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x000A, bytearray([0xBE, 0x81, 0xA4]))            #                     ldx.w $A47F+2,y
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x000D, bytearray([0x5C, 0x8E, 0xA4, 0x00]))      #                     jml $00A48E
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0011, bytearray([0xAD, 0xD9, 0x13]))            # .map                lda $13D9
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0014, bytearray([0xC9, 0x0A]))                  #                     cmp #$0A
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0016, bytearray([0xD0, 0xEF]))                  #                     bne .regular
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0018, bytearray([0xAD, 0xE8, 0x1D]))            #                     lda $1DE8
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x001B, bytearray([0xC9, 0x06]))                  #                     cmp #$06
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x001D, bytearray([0xD0, 0xE8]))                  #                     bne .regular
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x001F, bytearray([0x9C, 0x03, 0x07]))            #                     stz $0703
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0022, bytearray([0x9C, 0x04, 0x07]))            #                     stz $0704
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0025, bytearray([0x9C, 0x21, 0x21]))            #                     stz $2121
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0028, bytearray([0xA2, 0x06]))                  #                     ldx #$06
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x002A, bytearray([0xBD, 0x49, 0x92]))            # .loop               lda.w $9249,x
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x002D, bytearray([0x9D, 0x20, 0x43]))            #                     sta $4320,x
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0030, bytearray([0xCA]))                        #                     dex 
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0031, bytearray([0x10, 0xF7]))                  #                     bpl .loop
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0033, bytearray([0xA9, 0x04]))                  #                     lda #$04
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0035, bytearray([0x8D, 0x0B, 0x42]))            #                     sta $420B
    rom.write_bytes(PALETTE_UPLOADER_EDIT + 0x0038, bytearray([0x5C, 0xCF, 0xA4, 0x00]))      #                     jml $00A4CF

    # Insert this piece of ASM again in case levels are disabled
    PALETTE_LEVEL_CODE_ADDR = 0x88000
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00E4, bytearray([0xA6, 0x04]))                # load_colors:        ldx !_index
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00E6, bytearray([0xA4, 0x06]))                #                     ldy !_x_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00E8, bytearray([0xA7, 0x0A]))                # .x_loop             lda [!_ptr]
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00EA, bytearray([0x9D, 0x03, 0x07]))          #                     sta $0703,x
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00ED, bytearray([0xE6, 0x0A]))                #                     inc !_ptr
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00EF, bytearray([0xE6, 0x0A]))                #                     inc !_ptr
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F1, bytearray([0xE8]))                      #                     inx 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F2, bytearray([0xE8]))                      #                     inx 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F3, bytearray([0x88]))                      #                     dey 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F4, bytearray([0x10, 0xF2]))                #                     bpl .x_loop
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F6, bytearray([0xA5, 0x04]))                #                     lda !_index
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F8, bytearray([0x18]))                      #                     clc 
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00F9, bytearray([0x69, 0x20, 0x00]))          #                     adc #$0020
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00FC, bytearray([0x85, 0x04]))                #                     sta !_index
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x00FE, bytearray([0xC6, 0x08]))                #                     dec !_y_span
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0100, bytearray([0x10, 0xE2]))                #                     bpl load_colors
    rom.write_bytes(PALETTE_LEVEL_CODE_ADDR + 0x0102, bytearray([0x60]))                      #                     rts 

    # Load palette paths
    data = pkgutil.get_data(__name__, f"data/palettes/map/palettes.json").decode("utf-8")
    maps = json.loads(data)

    for map_id in range(0x07):
        current_map_name = map_names[map_id]
        palette = world.random.randint(0, len(maps[current_map_name])-1)
        rom.write_bytes(PALETTE_MAP_INDEX_ADDR + map_id, bytearray([palette]))

    # Writes the actual map palette data and pointer to said data to the ROM
    pal_offset = 0x0000
    map_num = 0
    bank_palette_count = 0
    for current_map in maps.keys():
        for palette in range(len(maps[current_map])):
            # Handle bank crossing
            if bank_palette_count == 113:
                pal_offset = (pal_offset & 0xF8000) + 0x8000
                bank_palette_count = 0
            # Write pointer
            data_ptr = pc_to_snes(PALETTE_MAP_DATA_ADDR + pal_offset)
            rom.write_bytes(PALETTE_MAP_PTR_ADDR + ((map_num*3)<<8) + (palette*3), bytearray([data_ptr & 0xFF, (data_ptr>>8)&0xFF, (data_ptr>>16)&0xFF]))
            # Write data
            rom.write_bytes(PALETTE_MAP_DATA_ADDR + pal_offset, read_palette_file(current_map, maps[current_map][palette], "map"))
            # Update map mario palette
            chosen_palette = world.options.mario_palette.value
            rom.write_bytes(PALETTE_MAP_DATA_ADDR + pal_offset + 206, bytes(ow_mario_palettes[chosen_palette]))
            pal_offset += 0x11C
            bank_palette_count += 1
        map_num += 1


def pc_to_snes(address):
    return ((address << 1) & 0x7F0000) | (address & 0x7FFF) | 0x8000

def read_palette_file(tileset, filename, type_):
    palette_file = pkgutil.get_data(__name__, f"data/palettes/{type_}/{tileset}/{filename}")
    colors = bytearray([])

    # Copy back colors
    colors += bytearray([palette_file[0x200], palette_file[0x201]])

    if type_ == "level":
        # Copy background colors
        colors += bytearray([palette_file[(0x01*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x11*2)+(i)] for i in range(14)])

        # Copy foreground colors
        colors += bytearray([palette_file[(0x21*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x31*2)+(i)] for i in range(14)])

        # Copy berry colors
        colors += bytearray([palette_file[(0x29*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x39*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x49*2)+(i)] for i in range(14)])

        # Copy global colors
        colors += bytearray([palette_file[(0x41*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x51*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x61*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x71*2)+(i)] for i in range(14)])

        # Copy sprite colors
        colors += bytearray([palette_file[(0x81*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x91*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xA1*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xB1*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xC1*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xD1*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xE1*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xF1*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xE9*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xF9*2)+(i)] for i in range(14)])
    
    elif type_ == "map":
        # Copy layer 2 colors
        colors += bytearray([palette_file[(0x41*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x51*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x61*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x71*2)+(i)] for i in range(14)])

        # Copy layer 1 colors
        colors += bytearray([palette_file[(0x29*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x39*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x49*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x59*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x69*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x79*2)+(i)] for i in range(14)])

        # Copy layer 3 colors
        colors += bytearray([palette_file[(0x08*2)+(i)] for i in range(16)])
        colors += bytearray([palette_file[(0x18*2)+(i)] for i in range(16)])

        # Copy sprite colors
        colors += bytearray([palette_file[(0x81*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0x91*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xA1*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xB1*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xC1*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xD1*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xE1*2)+(i)] for i in range(14)])
        colors += bytearray([palette_file[(0xF1*2)+(i)] for i in range(14)])

    return colors
