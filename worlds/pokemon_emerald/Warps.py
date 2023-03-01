from typing import Dict, List, Optional
from .Data import get_extracted_data, get_warp_to_region_map


_warp_map = None


class Warp:
    is_one_way: bool
    source_map: str
    source_ids: List[int]
    dest_map: str
    dest_ids: int

    def __init__(self, encoded_string: Optional[str] = None) -> None:
        if (encoded_string != None):
            decoded_warp = Warp.decode(encoded_string)
            self.is_one_way = decoded_warp.is_one_way
            self.source_map = decoded_warp.source_map
            self.source_ids = decoded_warp.source_ids
            self.dest_map = decoded_warp.dest_map
            self.dest_ids = decoded_warp.dest_ids

    def encode(self):
        global _special_warp_id_map
        source_ids_string = ""
        for id in self.source_ids:
            source_ids_string += str(id) + ","
        source_ids_string = source_ids_string[:-1] # Remove last ","

        return f"{self.source_map}:{source_ids_string}/{self.dest_map}:{self.dest_id}"
    
    def connects_to(self, other: 'Warp'):
        return self.dest_map == other.source_map and set(self.dest_ids) <= set(other.source_ids)

    @staticmethod
    def decode(encoded_string: str) -> 'Warp':
        warp = Warp()
        warp.is_one_way = encoded_string.endswith("!")
        if (warp.is_one_way):
            encoded_string = encoded_string[:-1]

        warp_source, warp_dest = encoded_string.split("/")
        warp_source_map, warp_source_indices = warp_source.split(":")
        warp_dest_map, warp_dest_indices = warp_dest.split(":")

        warp.source_map = warp_source_map
        warp.dest_map = warp_dest_map

        warp.source_ids = [int(index) for index in warp_source_indices.split(",")]
        warp.dest_ids = [int(index) for index in warp_dest_indices.split(",")]

        return warp


def warps_connect_ltr(warp_1: str, warp_2: str) -> bool:
    return Warp(warp_1).connects_to(Warp(warp_2))


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
