from BaseClasses import Location


class DWLocation(Location):
    game: str = "Dragon Warrior"

    progress_byte: int = 0x000000
    progress_bit:  int = 0
    inverted_bit: bool = False

    def __init__(self, player: int, name: str = '', address: int = None, parent=None, prog_byte: int = None, prog_bit: int = None, invert: bool = False):
        super().__init__(player, name, address, parent)
        self.progress_byte = prog_byte
        self.progress_bit  = prog_bit
        self.inverted_bit  = invert
