from ..data.world_map_event_modification import WorldMapEventModification

class WorldMapEventModifications:
    WOB_MODIFICATIONS_COUNT = 15
    WOR_MODIFICATIONS_COUNT = 3
    MODIFICATION_COUNT = WOB_MODIFICATIONS_COUNT + WOR_MODIFICATIONS_COUNT

    WOB_FIGARO_CASTLE_EAST, WOB_FIGARO_CASTLE_WEST, WOB_NIKEAH_ROCKSLIDE, WOB_ESPER_MOUNTAIN_ENTRANCE,\
    WOB_SEALED_GATE1, WOB_SEALED_GATE2, WOB_SEALED_GATE3, WOB_SEALED_GATE4, WOB_SEALED_GATE5,\
    WOB_SEALED_GATE6, WOB_SEALED_GATE7, WOB_SEALED_GATE8, WOB_SEALED_GATE9, WOB_SEALED_GATE10,\
    WOB_UNKNOWN_CAVE, WOR_FIGARO_CASTLE_EAST, WOR_FIGARO_CASTLE_WEST, WOR_EBOTS_ROCK = range(MODIFICATION_COUNT)

    def __init__(self, rom):
        self.rom = rom
        self.read()

    def set_event_bit(self, id, event_bit):
        self.event_modifications[id].event_bit = event_bit

    def set_sealed_gate_event_bit(self, event_bit):
        for id in range(self.WOB_SEALED_GATE1, self.WOB_SEALED_GATE10 + 1):
            self.set_event_bit(id, event_bit)

    def read(self):
        self.event_modifications = []
        for em_index in range(self.MODIFICATION_COUNT):
            event_modification = WorldMapEventModification(self.rom, em_index)
            self.event_modifications.append(event_modification)

    def write(self):
        for event_modification in self.event_modifications:
            event_modification.write()

    def print(self):
        for event_modification in self.event_modifications:
            event_modification.print()
