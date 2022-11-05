
from .Names import LocationName


class CV64Level:
    startzoneSceneOffset: int
    startzoneSpawnOffset: int
    startSceneID: int
    startSpawnID: int

    midSceneID: int
    midSpawnID: int

    endzoneSceneOffset: int
    endzoneSpawnOffset: int
    endSceneID: int
    endSpawnID: int
    
    def __init__(self, startzoneSceneOffset: int, startzoneSpawnOffset: int, startSceneID: int, startSpawnID: int,
                 midSceneID: int, midSpawnID: int, endzoneSceneOffset: int, endzoneSpawnOffset: int, endSceneID: int,
                 endSpawnID: int, stageNumberOffsetList: list):
        self.startzoneSceneOffset = startzoneSceneOffset
        self.startzoneSpawnOffset = startzoneSpawnOffset
        self.startSceneID = startSceneID
        self.startSpawnID = startSpawnID

        self.midSceneID = midSceneID
        self.midSpawnID = midSpawnID

        self.endzoneSceneOffset = endzoneSceneOffset
        self.endzoneSpawnOffset = endzoneSpawnOffset
        self.endSceneID = endSceneID
        self.endSpawnID = endSpawnID

        self.stageNumberOffsetList = stageNumberOffsetList


level_dict = {
    LocationName.forest_of_silence:    CV64Level(0xFFFFFF, 0xFFFFFF, 0x00, 0x00, 0x00, 0x04,
                                                 0xB6302F, 0xB6302B, 0x00, 0x01, [0x1049C5, 0x1049CD, 0x1049D5]),
    LocationName.castle_wall:          CV64Level(0xFFFFFF, 0xFFFFFF, 0x02, 0x00, 0x02, 0x07,
                                                 0x109A5F, 0x109A61, 0x02, 0x10, [0x1049DD, 0x1049E5, 0x1049ED]),
    LocationName.villa:                CV64Level(0xFFFFFF, 0xFFFFFF, 0x03, 0x00, 0x05, 0x04,
                                                 0x0D9DA3, 0x109E81, 0x1A, 0x03, [0x1049F5, 0x1049FD, 0x104A05,
                                                                                  0x104A0D]),
    LocationName.tunnel:               CV64Level(0xFFFFFF, 0xFFFFFF, 0x07, 0x00, 0x07, 0x03,
                                                 0x109B4F, 0x109B51, 0x07, 0x11, [0x104A15, 0x104A1D, 0x104A25,
                                                                                  0x104A2D]),
    LocationName.underground_waterway: CV64Level(0xFFFFFF, 0xFFFFFF, 0x08, 0x00, 0x08, 0x03,
                                                 0x109B67, 0x109B69, 0x08, 0x01,
                                                 [0x104A35, 0x104A3D]),
    LocationName.castle_center:        CV64Level(0xFFFFFF, 0xFFFFFF, 0x19, 0x00, 0x0E, 0x03,
                                                 0x109CB7, 0x109CB9, 0x0F, 0x02, [0x104A45, 0x104A4D, 0x104A55,
                                                                                  0x104A5D, 0x104A65, 0x104A6D,
                                                                                  0x104A75]),
    LocationName.duel_tower:           CV64Level(0x109DA7, 0x109DA9, 0x13, 0x00, 0x13, 0x01,
                                                 0x109D8F, 0x109D91, 0x13, 0x01, [0x104ACD]),
    LocationName.tower_of_execution:   CV64Level(0x109D17, 0x109D19, 0x10, 0x00, 0x10, 0x02,
                                                 0x109CFF, 0x109D01, 0x10, 0x12, [0x104A7D, 0x104A85]),
    LocationName.tower_of_science:     CV64Level(0x109D77, 0x109D79, 0x12, 0x00, 0x12, 0x01,
                                                 0x109D5F, 0x109D61, 0x12, 0x04, [0x104A95, 0x104A9D, 0x104AA5]),
    LocationName.tower_of_sorcery:     CV64Level(0x109D47, 0x109D49, 0x11, 0x00, 0x11, 0x01,
                                                 0x109D2F, 0x109D31, 0x11, 0x13, [0x104A8D]),
    LocationName.room_of_clocks:       CV64Level(0xFFFFFF, 0xFFFFFF, 0x1B, 0x00, 0x1B, 0x02,
                                                 0x109EAF, 0x109EB1, 0x1B, 0x14, [0x104AC5]),
    LocationName.clock_tower:          CV64Level(0xFFFFFF, 0xFFFFFF, 0x17, 0x00, 0x17, 0x02,
                                                 0x109E37, 0x109E39, 0x17, 0x03, [0x104AB5, 0x104ABD]),
    LocationName.castle_keep:          CV64Level(0xFFFFFF, 0xFFFFFF, 0x14, 0x02, 0x14, 0x02,
                                                 0xFFFFFF, 0xFFFFFF, 0xFF, 0xFF, [0x104AAD]),
}

mid_regions_dict = {
    LocationName.forest_of_silence: LocationName.forest_mid,
    LocationName.castle_wall: LocationName.cw_descent,
    LocationName.villa: LocationName.villa_storeroom,
    LocationName.tunnel: LocationName.tunnel_end,
    LocationName.underground_waterway: LocationName.underground_waterway,
    LocationName.castle_center: LocationName.cc_invention_lizard_exit,
    LocationName.duel_tower: LocationName.duel_tower,
    LocationName.tower_of_execution: LocationName.tower_of_execution,
    LocationName.tower_of_science: LocationName.tosci_conveyors,
    LocationName.tower_of_sorcery: LocationName.tower_of_sorcery,
    LocationName.room_of_clocks: LocationName.room_of_clocks,
    LocationName.clock_tower: LocationName.ct_middle,
    LocationName.castle_keep: LocationName.castle_keep
}

end_regions_dict = {
    LocationName.forest_of_silence:    LocationName.forest_end,
    LocationName.castle_wall:          LocationName.cw_exit,
    LocationName.villa:                LocationName.villa_crypt,
    LocationName.tunnel:               LocationName.tunnel_end,
    LocationName.underground_waterway: LocationName.uw_end,
    LocationName.castle_center:        LocationName.cc_elev_top,
    LocationName.duel_tower:           LocationName.duel_tower,
    LocationName.tower_of_execution:   LocationName.tower_of_execution,
    LocationName.tower_of_science:     LocationName.tosci_conveyors,
    LocationName.tower_of_sorcery:     LocationName.tower_of_sorcery,
    LocationName.room_of_clocks:       LocationName.room_of_clocks,
    LocationName.clock_tower:          LocationName.ct_end,
}

level_list = [
    LocationName.forest_of_silence,
    LocationName.castle_wall,
    LocationName.villa,
    LocationName.tunnel,
    LocationName.underground_waterway,
    LocationName.castle_center,
    LocationName.duel_tower,
    LocationName.tower_of_execution,
    LocationName.tower_of_science,
    LocationName.tower_of_sorcery,
    LocationName.room_of_clocks,
    LocationName.clock_tower,
    LocationName.castle_keep
]
