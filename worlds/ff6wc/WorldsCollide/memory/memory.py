from ..memory.rom import ROM
from ..memory.space import Space
from ..memory.free import free
from ..data import text
from .. import args as args

class Memory:
    def __init__(self):
        self.rom = ROM(args.input_file)
        self.rom.set_bytes(0x12BEBC, bytearray(text.get_bytes(text.convert("ArchplgoItem", text.TEXT2), text.TEXT2)))
        Space.rom = self.rom
        free()

    def write(self):
        self.rom.set_bytes(0x00FFC0, bytearray(args.ap_data["RomName"], 'utf-8'))
        if not args.no_rom_output:
            self.rom.write(args.output_file)
        else:
            self.rom.write(args.output_file)
            #self.rom.write_patch(args.input_file, args.output_file)

character_texts = []
esper_texts = [1133, 1380, 1381, 1134, 1535, 1082, 1091, 1092, 1136,
               1534, 2618, 1093, 1087, 2975, 2799, 1506, 1095, 1135,
               2755, 1097, 1098, 1572, 2756, 1099, 2273, 2733, 1100]
item_texts = []