from pathlib import Path
from typing import Dict, Iterator, Union

OW_SETTINGS_KEY_BOY_CLASS: str
OW_SETTINGS_KEY_GIRL_CLASS: str
OW_SETTINGS_KEY_SPRITE_CLASS: str
WORKING_DATA_KEY_BOY_CLASS: str
WORKING_DATA_KEY_BOY_EXISTS: str
WORKING_DATA_KEY_BOY_IN_LOGIC: str
WORKING_DATA_KEY_BOY_START_WEAPON_INDEX: str
WORKING_DATA_KEY_GIRL_CLASS: str
WORKING_DATA_KEY_GIRL_EXISTS: str
WORKING_DATA_KEY_GIRL_IN_LOGIC: str
WORKING_DATA_KEY_GIRL_START_WEAPON_INDEX: str
WORKING_DATA_KEY_SPRITE_CLASS: str
WORKING_DATA_KEY_SPRITE_EXISTS: str
WORKING_DATA_KEY_SPRITE_IN_LOGIC: str
WORKING_DATA_KEY_SPRITE_START_WEAPON_INDEX: str

class Context:
    error: Union[str, None]
    working_data: WorkingData

class Item:
    event_flag: int
    id: int
    name: str
    type: str

class ItemList:
    def __iter__(self) -> Iterator[Item]: ...
    def __len__(self) -> int: ...

class Location:
    event_index: int
    event_num: int
    id: int
    map_num: int
    name: str
    obj_num: int
    requirements: StrList

class LocationList:
    def __iter__(self) -> Iterator[Location]: ...
    def __len__(self) -> int: ...

class OW:
    context: Context
    generator: OWGenerator
    seed: str
    settings: OWSettings

    def __init__(self, src: Union[str, Path], seed: str, settings: Dict[str, str]) -> None: ...
    @staticmethod
    def get_all_items() -> ItemList: ...
    @staticmethod
    def get_all_locations() -> LocationList: ...
    def run(self, src: Union[str, Path]) -> None: ...

class OWGenerator:
    def get_items(self) -> ItemList: ...
    def get_locations(self) -> LocationList: ...

class OWSettings:
    def __setitem__(self, key: str, value: str) -> None: ...

class StrList:
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...

class WorkingData:
    def get_bool(self, key: str) -> bool: ...
    def get_int(self, key: str) -> int: ...
    def __getitem__(self, key: str) -> str: ...
    def __setitem__(self, key: str, value: str) -> None: ...
