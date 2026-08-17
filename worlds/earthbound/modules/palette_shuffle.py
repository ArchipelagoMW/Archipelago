from ..game_data.palettes_organized import map_palettes, nice_palettes, ugly_palettes, nonsense_palettes
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import EarthBoundWorld
    from .Rom import LocalRom


event_palettes = {
    "Happy-Happy Village": 0x8367,
    "Threed": 0x85A7,
    "Deep Darkness": 0x8F67
    }


def randomize_psi_palettes(world: "EarthBoundWorld", rom: "LocalRom") -> None:
    spell_palettes = []
    for i in range(34):
        spell_palettes.append(0x0CF47F + (i * 8))
    
    for i in range(7):
        spell_palettes.append(0x360710 + (i * 8))
        
    shuffled_palettes = spell_palettes.copy()

    if world.options.randomize_psi_palettes == 1:
        world.random.shuffle(shuffled_palettes)

    elif world.options.randomize_psi_palettes == 2:
        for i in range(0x010E):
            rom.write_bytes(0x0CF47F + i, bytearray([world.random.randint(0x00, 0xFF)]))

        for i in range(0x50):
            rom.write_bytes(0x36F710 + i, bytearray([world.random.randint(0x00, 0xFF)]))

    for index, pointer in enumerate(spell_palettes):
        rom.copy_bytes(pointer, 8, shuffled_palettes[index])


def map_palette_shuffle(world: "EarthBoundWorld", rom: "LocalRom") -> None:
    for i in range(168):
        rom.copy_bytes(0x1A7CA7 + (i * 192), 191, 0x381000 + (i * 192))
    
    for item in map_palettes:
        choosable_palettes = nice_palettes[item]
        if world.options.map_palette_shuffle > 1:
            choosable_palettes += ugly_palettes[item]
        if world.options.map_palette_shuffle > 2:
            choosable_palettes += nonsense_palettes[item]
        
        chosen_palette = world.random.choice(choosable_palettes)
        rom.copy_bytes(0x381002 + (chosen_palette * 192), 29, 0x1A7CA9 + (map_palettes[item] * 192))
        rom.copy_bytes(0x381022 + (chosen_palette * 192), 157, 0x1A7CC9 + (map_palettes[item] * 192))  # The event palette pointer is between these 2 blocks
