from typing import NamedTuple


class RAC3VENDORSLOT(NamedTuple):
    item_id: int
    is_ammo: bool
    model_oclass: int = 0xCDB
    ammo_model_oclass: int = 0xCDB
    is_upgrade: bool = False