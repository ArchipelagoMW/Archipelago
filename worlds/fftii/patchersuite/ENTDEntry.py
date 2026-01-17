from worlds.fftii.patchersuite.Unit import Unit


class ENTDEntry:
    name: str
    location: int
    index: int
    unit_count = 16
    unit_length = 40
    total_length = unit_count * unit_length
    units: list[bytearray] = []
    unit_datas: list[Unit] = []
    all_data: bytearray

    def __init__(self, entd_data: bytearray, name: str, location: int):
        self.units = []
        self.unit_datas = []
        self.all_data = bytearray()
        self.name = name
        self.location = location
        for i in range(self.unit_count):
            self.units.append(entd_data[i * self.unit_length:(i + 1) * self.unit_length])
        assert len(self.units) == 16, len(self.units)

    def __repr__(self):
        return self.name

    def apply_data(self):
        for unit_data in self.unit_datas:
            self.all_data.extend(unit_data.unit_data)