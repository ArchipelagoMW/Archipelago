from ..data.npc import NPC

class NPCs():
    NPC_COUNT = 2192
    DATA_START_ADDR = 0x041d52
    DATA_END_ADDR = 0x046abf

    def __init__(self, rom):
        self.rom = rom
        self.read()

    def read(self):
        self.npcs = []

        for npc_index in range(self.NPC_COUNT):
            npc_data_start = self.DATA_START_ADDR + npc_index * NPC.DATA_SIZE
            npc_data = self.rom.get_bytes(npc_data_start, NPC.DATA_SIZE)

            new_npc = NPC()
            new_npc.from_data(npc_data)
            self.npcs.append(new_npc)

    def mod(self, characters):
        for npc in self.npcs:
            if npc.sprite < characters.CHARACTER_COUNT or (npc.sprite <= characters.KEFKA and npc.palette == characters.character_palettes.DEFAULTS[npc.sprite]):
                # fix palettes of npcs with character sprites and customizable npc palettes
                npc.palette = characters.get_palette(npc.sprite)

    def get_npc(self, index):
        return self.npcs[index]

    def add_npc(self, index, new_npc):
       # some sprites are broken up
        if new_npc.sprite == 109:
            new_npc.split_sprite = 1

        self.npcs.insert(index, new_npc)
        self.NPC_COUNT += 1

    def remove_npc(self, index):
        del self.npcs[index]
        self.NPC_COUNT -= 1

    def set_palette(self, npc, palette):
        self.npcs[npc].palette = palette

    def print(self):
        for npc in self.npcs:
            npc.print()

    def write(self):
        for npc_index, npc in enumerate(self.npcs):
            npc_data = npc.to_data()
            npc_data_start = self.DATA_START_ADDR + npc_index * NPC.DATA_SIZE
            # Assert that the address being written doesn't go beyond the expected end point
            # If it does, then the npc_index is too high -- you've added more NPCs than the ROM can handle
            assert(npc_data_start < self.DATA_END_ADDR)
            self.rom.set_bytes(npc_data_start, npc_data)
