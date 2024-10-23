
class DropTable:
    def __init__(self):
        self.common = None
        self.uncommon = None
        self.rare = None
        self.mythic = None

    def encode(self):
        return [(0 if i is None else i) for i in [self.common, self.uncommon, self.rare, self.mythic]]

def decode(byte_list):
    dt = DropTable()
    dt.common = (None if byte_list[0] == 0 else byte_list[0])
    dt.uncommon = (None if byte_list[1] == 0 else byte_list[1])
    dt.rare = (None if byte_list[2] == 0 else byte_list[2])
    dt.mythic = (None if byte_list[3] == 0 else byte_list[3])

    return dt
