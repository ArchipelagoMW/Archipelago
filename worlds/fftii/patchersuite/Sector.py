class Sector:
    header_size = 0x18
    data_size = 0x800
    error_size = 0x118
    sector_size = header_size + data_size + error_size
    header: bytearray
    data: bytearray
    error: bytearray
    all_data: bytearray

    def __init__(self, new_data):
        self.header = new_data[:self.header_size]
        self.data = bytearray(new_data[self.header_size:self.header_size + self.data_size])
        self.error = new_data[self.header_size + self.data_size:]
        self.all_data = new_data
        assert len(self.header) == self.header_size
        assert len(self.data) == self.data_size
        assert len(self.error) == self.error_size





iso_filename = "Final Fantasy Tactics (USA).bin"
entd_size = 80 * 1024
entd_sector_count = 40
event_count = 128
entd_start = 0x0875FD30

# if False:
#     iso_data = file.read()
#     total_entd_length = entd_sector_count * Sector.sector_size
#     entd_list: list[bytearray] = []
#     all_entd_sectors: list[Sector] = list()
#     for i in range(4):
#         start = entd_start + (i * total_entd_length)
#         entd = iso_data[start:start + total_entd_length]
#         entd_sectors = []
#         for j in range(entd_sector_count):
#             new_sector = Sector(entd[j * Sector.sector_size:(j + 1) * Sector.sector_size])
#             entd_sectors.append(new_sector)
#             all_entd_sectors.append(new_sector)
#         entd_data = bytearray()
#         for sector in entd_sectors:
#             entd_data.extend(sector.data)
#         entd_list.append(entd_data)
#     full_entd = bytearray()
#     for entd in entd_list:
#         full_entd.extend(entd)
#     print(hex(len(full_entd)))
#     used_units = []
#     entd_entries: list[ENTDEntry] = list()
#     for i in range(0x1D5):
#         if i in events.keys():
#             entd_data = full_entd[i * ENTDEntry.total_length:(i + 1) * ENTDEntry.total_length]
#             new_entd_entry = ENTDEntry(entd_data, events[i], i * ENTDEntry.total_length)
#             new_entd_entry.index = i
#             for unit in new_entd_entry.units:
#                 if unit[0] > 0 and unit[1] > 0:
#                     new_unit = Unit(unit)
#                     if new_unit.job != 0:
#                         used_units.append(new_unit.job)
#                 else:
#                     new_unit = Unit(unit)
#                 new_entd_entry.unit_datas.append(new_unit)
#             used_sprite_sheets = set()
#             used_source_units = set()
#             for unit in new_entd_entry.unit_datas:
#                 if unit.sprite_set > 0 and unit.team == UnitTeam.RED:
#                     source_unit = SourceUnit(SpriteSet(unit.sprite_set), Job(unit.job), unit.gender)
#                     if source_unit in valid_shuffle_source_units:
#                         used_source_units.add(source_unit)
#                     included = False
#                     if source_unit not in used_sprite_sheets:
#                         used_sprite_sheets.add(source_unit)
#             for source in used_source_units:
#                 print(source)
#             #print(f"#Used sprite sheets: {len(used_sprite_sheets)}")
#             new_entd_entry.apply_data()
#             entd_entries.append(new_entd_entry)
#     exit()
#     new_full_entd: bytearray = full_entd.copy()
#     for entd_entry in entd_entries:
#         start_location: int = entd_entry.location
#         end_location: int = entd_entry.location + ENTDEntry.total_length
#         new_full_entd[start_location:end_location] = entd_entry.all_data
#     new_all_entd_sectors: list[Sector] = list()
#     for sector in all_entd_sectors:
#         new_all_entd_sectors.append(Sector(sector.all_data))
#     for i in range(len(new_full_entd)):
#         #assert new_full_entd[i] == full_entd[i], (i, new_full_entd[i], full_entd[i])
#         sector_number: int = i // 2048
#         new_all_entd_sectors[sector_number].data[i % 2048] = new_full_entd[i]
#     for i in range(len(all_entd_sectors)):
#         for j in range(len(all_entd_sectors[i].data)):
#             pass
#             #assert all_entd_sectors[i].data[j] == new_all_entd_sectors[i].data[j]
#         new_all_data: bytearray = bytearray()
#         new_all_data.extend(new_all_entd_sectors[i].header)
#         new_all_data.extend(new_all_entd_sectors[i].data)
#         new_all_data.extend(new_all_entd_sectors[i].error)
#         new_all_entd_sectors[i].all_data = new_all_data
#     new_iso_data = bytearray(iso_data)
#     new_sector_data: bytearray = bytearray()
#     for sector in new_all_entd_sectors:
#         new_sector_data.extend(sector.all_data)
#     new_iso_data[entd_start:entd_start + len(new_sector_data)] = new_sector_data
#     for i in range(len(new_iso_data)):
#         assert iso_data[i] == new_iso_data[i]