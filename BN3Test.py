import worlds.mmbn3.Rom as Rom

from BaseClasses import ItemClassification
from worlds.mmbn3 import ItemData
from worlds.mmbn3.Items import ItemType, ChipCode
from worlds.mmbn3.Locations import LocationData
from worlds.mmbn3.Names import LocationName, ItemName


def main():
    rom_file = 'C:/Users/digiholic/Projects/BN3AP/Patches/combined - Copy.gba'
    Rom.read_rom(rom_file)

    Rom.ReplaceItem(
            LocationData(LocationName.ACDC_1_Southwest_BMD,         0xb31000, 0x020001d0, 0x40, 0x7643B8, 231, 1),
            ItemData(0xB3101F, ItemName.AirShot3_star, ItemClassification.useful, ItemType.Chip, 6, ChipCode('*'))
        )
    rom_file = 'C:/Users/digiholic/Projects/BN3AP/Patches/combined - Patched.gba'

    Rom.write_rom(rom_file)

if __name__ == "__main__": main()