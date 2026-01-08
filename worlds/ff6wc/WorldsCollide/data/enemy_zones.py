from ..data.enemy_zone import WOBZone, WORZone, MapZone

class EnemyZones():
    # world of balance is split into 64 zones
    # world of ruin is split into 64 zones
    # maps are 1 zone each
    WOB_COUNT = 64
    WOR_COUNT = 64
    MAP_COUNT = 512
    ZONE_COUNT = WOB_COUNT + WOR_COUNT + MAP_COUNT

    def __init__(self, rom, args):
        self.rom = rom
        self.args = args
        self.read()

    def read(self):
        self.zones = []
        for zone_index in range(self.WOB_COUNT):
            zone = WOBZone(self.rom, zone_index)
            self.zones.append(zone)

        for zone_index in range(self.WOR_COUNT):
            zone = WORZone(self.rom, zone_index)
            self.zones.append(zone)

        for zone_index in range(self.MAP_COUNT):
            zone = MapZone(self.rom, zone_index)
            self.zones.append(zone)

    def mod(self):
        pass

    def write(self):
        for zone in self.zones:
            zone.write()

    def print(self):
        for zone in self.zones:
            zone.print()
