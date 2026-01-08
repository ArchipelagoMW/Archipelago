from ....memory.space import Bank, Allocate, Reserve, Write, Read
from .... import args as args

from ....instruction.field import instructions as field
from ....instruction.field.y_npc.instructions import SetYNPCGraphics, YEffect, YNPCEffect

DEFAULT_SOUND = 0x4f # lagomorph

def _graphics_group(possibilities):
    from ....instruction.field.custom import BranchChance
    space = Allocate(Bank.CC, 200, "field y npc graphics group", field.NOP())

    addresses = []
    for option in possibilities:
        sprite = option[0]
        palette = option[1]
        vehicle = option[2]
        sound = option[3]

        addresses.append(space.next_address)
        space.write(
            field.PlaySoundEffect(sound),
            SetYNPCGraphics(sprite, palette, vehicle),
            field.Return(),
        )

    count = len(addresses)
    pick_random = space.next_address
    for i in range(count - 1):
        probability = (count / (count - i)) / count
        space.write(
            BranchChance(probability, addresses[i]),
        )
    space.write(
        field.Branch(addresses[-1]),
    )
    return pick_random

def mascot():
    wark_sound = 0xd9
    kupo_sound = 0xf9
    imp_sound = 0xce # splash sound

    mog_sprite = 0x0a
    mog_palette = 0x05
    imp_sprite = 0x0f
    imp_palette = 0x00

    no_vehicle = field.Vehicle.NONE
    chocobo = field.Vehicle.CHOCOBO
    chocobo_and_rider = field.Vehicle.CHOCOBO_AND_RIDER

    possibilities = [
        (0xff, 0xff, chocobo, wark_sound),
        (mog_sprite, mog_palette, chocobo_and_rider, kupo_sound),
        (mog_sprite, mog_palette, no_vehicle, kupo_sound),
        (imp_sprite, imp_palette, chocobo_and_rider, imp_sound),
        (imp_sprite, imp_palette, no_vehicle, imp_sound),
    ]

    return _graphics_group(possibilities)

def creature():
    dog_sprite = 0x19
    octopus_sprite = 0x1f
    bird_sprite = 0x28
    behemoth_sprite = 0x33
    fairy_sprite = 0x37
    wolf_sprite = 0x38
    dragon_sprite = 0x39
    fish_sprite = 0x3a

    bark_sound = 0x97
    chirp_sound = 0xc0

    no_vehicle = field.Vehicle.NONE

    possibilities = [
        (dog_sprite, 4, no_vehicle, bark_sound),
        (octopus_sprite, 5, no_vehicle, DEFAULT_SOUND),
        (bird_sprite, 4, no_vehicle, chirp_sound),
        (fish_sprite, 4, no_vehicle, DEFAULT_SOUND),
        (behemoth_sprite, 2, no_vehicle, DEFAULT_SOUND),
        (behemoth_sprite, 4, no_vehicle, DEFAULT_SOUND),
        (fairy_sprite, 1, no_vehicle, DEFAULT_SOUND),
        (fairy_sprite, 2, no_vehicle, DEFAULT_SOUND),
        (wolf_sprite, 2, no_vehicle, DEFAULT_SOUND),
        (wolf_sprite, 4, no_vehicle, DEFAULT_SOUND),
        (dragon_sprite, 0, no_vehicle, DEFAULT_SOUND),
        (dragon_sprite, 1, no_vehicle, DEFAULT_SOUND),
        (dragon_sprite, 2, no_vehicle, DEFAULT_SOUND),
        (dragon_sprite, 3, no_vehicle, DEFAULT_SOUND),
        (dragon_sprite, 4, no_vehicle, DEFAULT_SOUND),
        (dragon_sprite, 5, no_vehicle, DEFAULT_SOUND),
    ]

    return _graphics_group(possibilities)

def imperial():
    celes_sprite = 0x06
    soldier_sprite = 0x0e
    leo_sprite = 0x10
    kefka_sprite = 0x15
    gestahl_sprite = 0x16

    no_vehicle = field.Vehicle.NONE
    magitek = field.Vehicle.MAGITEK_AND_RIDER

    possibilities = [
        (celes_sprite, 0, no_vehicle, DEFAULT_SOUND),
        (celes_sprite, 0, magitek, DEFAULT_SOUND),
        (soldier_sprite, 0, no_vehicle, DEFAULT_SOUND),
        (soldier_sprite, 0, magitek, DEFAULT_SOUND),
        (soldier_sprite, 1, no_vehicle, DEFAULT_SOUND),
        (soldier_sprite, 1, magitek, DEFAULT_SOUND),
        (soldier_sprite, 4, no_vehicle, DEFAULT_SOUND),
        (soldier_sprite, 4, magitek, DEFAULT_SOUND),
        (leo_sprite, 0, no_vehicle, DEFAULT_SOUND),
        (kefka_sprite, 3, no_vehicle, DEFAULT_SOUND),
        (gestahl_sprite, 3, no_vehicle, DEFAULT_SOUND),
    ]

    return _graphics_group(possibilities)

def main_character():
    from ....data.characters import Characters
    from ....data.character_sprites import DEFAULT_CHARACTER_SPRITES
    from ....data.character_palettes import DEFAULT_CHARACTER_SPRITE_PALETTES

    sprites = DEFAULT_CHARACTER_SPRITES[:Characters.CHARACTER_COUNT]
    palettes = args.sprite_palettes

    possibilities = []
    for x in range(Characters.CHARACTER_COUNT):
        possibilities.append((sprites[x], palettes[x], field.Vehicle.NONE, DEFAULT_SOUND))

    return _graphics_group(possibilities)

def reflect():
    sound_effect = 0x5c # repeat 3 times for reflect
    tint_color = field.Tint.WHITE
    tint_palette = 6 # palette to change tint during animation

    src = [
        SetYNPCGraphics(0xff, tint_palette, 0xff),
        field.Repeat(3,
            field.PlaySoundEffect(sound_effect),
            field.Repeat(10,
                field.TintSpritePalette(tint_color, tint_palette),
            ),
            field.PauseUnits(2),
        ),
        YNPCEffect(YEffect.REFLECT),
        field.Repeat(30,
            field.TintSpritePalette(tint_color, tint_palette, invert = True),
        ),
        field.Return(),
    ]
    space = Write(Bank.CC, src, "field y npc reflect")
    return space.start_address

def stone():
    break_sound_effect = 0x53
    end_sound_effect = 0x47

    src = [
        field.PlaySoundEffect(break_sound_effect),
        YNPCEffect(YEffect.STOP),
        field.Pause(1),
        field.FlashScreen(field.Flash.WHITE),
        SetYNPCGraphics(0xff, 7, 0xff),
        field.PlaySoundEffect(end_sound_effect),

        Read(0xc19fd, 0xc1a03), # set palette 7 to gray
        field.Return(),
    ]
    space = Write(Bank.CC, src, "field y npc stone")
    return space.start_address

def vanish_xzone():
    vanish_sound_effect = 0x59
    xzone_sound_effect = 0x24

    src = [
        field.PlaySoundEffect(vanish_sound_effect),
        field.FadeSongVolume(0x00, 0x40),
        field.Repeat(26,
            field.TintBackground(field.Tint.BLACK),
        ),
        field.PauseUnits(34),
        field.PlaySoundEffect(0x47),

        field.Pause(1),
        field.PlaySoundEffect(xzone_sound_effect),

        field.Repeat(2,
            YNPCEffect(YEffect.HIDE),
            field.PauseUnits(10),
            YNPCEffect(YEffect.SHOW),
            field.PauseUnits(10),
        ),
        field.Repeat(2,
            YNPCEffect(YEffect.HIDE),
            field.PauseUnits(8),
            YNPCEffect(YEffect.SHOW),
            field.PauseUnits(8),
        ),
        field.Repeat(2,
            YNPCEffect(YEffect.HIDE),
            field.PauseUnits(6),
            YNPCEffect(YEffect.SHOW),
            field.PauseUnits(5),
        ),
        field.Repeat(2,
            YNPCEffect(YEffect.HIDE),
            field.PauseUnits(3),
            YNPCEffect(YEffect.SHOW),
            field.PauseUnits(1),
        ),

        YNPCEffect(YEffect.DELETE),
        field.FadeSongVolume(0x20, 0xdf),

        # restore background color
        field.Repeat(26,
            field.TintBackground(field.Tint.BLACK, invert = True),
        ),
        field.Return(),
    ]
    space = Write(Bank.CC, src, "field y npc vanish xzone")
    return space.start_address

def sketch():
    sketch_sound = 0x61

    src = [
        field.PlaySoundEffect(sketch_sound),
        field.PauseUnits(32),
        YNPCEffect(YEffect.ANY_RANDOM_GRAPHIC),
        field.Return(),
    ]
    space = Write(Bank.CC, src, "field y npc sketch")
    return space.start_address

def remove():
    sound_effect = 0x2d

    src = [
        field.PlaySoundEffect(sound_effect),
        YNPCEffect(YEffect.DELETE),
        field.Return(),
    ]
    space = Write(Bank.CC, src, "field y npc remove")
    return space.start_address

def random_graphics():
    sound_effect = 0x4f # lagomorph

    src = [
        field.PlaySoundEffect(sound_effect),
        YNPCEffect(YEffect.RANDOM_GRAPHIC),
        field.Return(),
    ]
    space = Write(Bank.CC, src, "field y npc random graphics")
    return space.start_address

def _y_npc():
    from ....instruction.field.functions import RETURN
    address = RETURN
    if args.y_npc_mascot:
        address = mascot()
    elif args.y_npc_creature:
        address = creature()
    elif args.y_npc_imperial:
        address = imperial()
    elif args.y_npc_main:
        address = main_character()
    elif args.y_npc_reflect:
        address = reflect()
    elif args.y_npc_stone:
        address = stone()
    elif args.y_npc_vanish_xzone:
        address = vanish_xzone()
    elif args.y_npc_sketch:
        address = sketch()
    elif args.y_npc_random:
        address = random_graphics()
    elif args.y_npc_remove:
        address = remove()
    return address

# called when player interacts with npc using y button
Y_NPC = _y_npc()
