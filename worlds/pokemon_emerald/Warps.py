from typing import Dict, List, Optional
from .Data import get_extracted_data, get_warp_to_region_map


_warp_map = None
special_warp_id_map = {
    "WARP_ID_SECRET_BASE": -1,
    "WARP_ID_DYNAMIC": -2
}


class Warp:
    source_map: str
    source_ids: List[int]
    dest_map: str
    dest_id: int

    def __init__(self, encoded_string: str) -> None:
        source_map, source_ids, dest_map, dest_id = Warp.decode(encoded_string)
        self.source_map = source_map
        self.source_ids = source_ids
        self.dest_map = dest_map
        self.dest_id = dest_id

    def encode(self):
        source_ids_string = ""
        for id in self.source_ids:
            source_ids_string += str(id) + ","
        source_ids_string = source_ids_string[:-1] # Remove last ","
    
        if (self.dest_id < 0):
            dest_id = {key for key in special_warp_id_map if special_warp_id_map[key] == self.dest_id}

        return f"{self.source_map}:{source_ids_string}/{self.dest_map}:{self.dest_id}"
    
    @staticmethod
    def decode(encoded_string: str):
        warp_source, warp_dest = encoded_string.split("/")
        warp_source_map, warp_source_indices = warp_source.split(":")
        warp_dest_map, warp_dest_index = warp_dest.split(":")

        warp_source_indices = [int(index) for index in warp_source_indices.split(",")]
        warp_dest_index = int(warp_dest_index) if (not warp_dest_index in special_warp_id_map) else special_warp_id_map[warp_dest_index]

        return (warp_source_map, warp_source_indices, warp_dest_map, warp_dest_index)


def warps_connect_ltr(warp_1, warp_2) -> bool:
    warp_1_source, warp_1_dest = warp_1.split("/")
    warp_2_source, warp_2_dest = warp_2.split("/")
    warp_1_source_map, warp_1_source_indices = warp_1_source.split(":")
    warp_2_source_map, warp_2_source_indices = warp_2_source.split(":")
    warp_1_dest_map, warp_1_dest_index = warp_1_dest.split(":")
    warp_2_dest_map, warp_2_dest_index = warp_2_dest.split(":")

    return warp_1_dest_map == warp_2_source_map and \
           warp_1_dest_index in warp_2_source_indices.split(",")


def get_warp_map() -> Dict[str, Optional[str]]:
    global _warp_map
    if (_warp_map == None):
        _warp_map = {}
        warps_json = get_extracted_data()["warps"]
        for warp in warps_json:
            for other_warp in warps_json:
                if (warp in _warp_map): continue
                if (warps_connect_ltr(warp, other_warp)):
                    _warp_map[warp] = other_warp
            
            if (not warp in _warp_map):
                _warp_map[warp] = None
    
    return _warp_map


def get_warp_destination(warp: str) -> Optional[str]:
    warp_map = get_warp_map()
    return warp_map[warp]


def get_warp_region_name(warp: str) -> Optional[str]:
    warp_to_region_map = get_warp_to_region_map()
    if (not warp in warp_to_region_map):
        return None
    return warp_to_region_map[warp]
