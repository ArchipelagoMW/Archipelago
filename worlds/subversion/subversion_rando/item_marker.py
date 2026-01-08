from enum import Enum
from typing import Iterable, Mapping

from .item_data import unique_items
from .location_data import Location, get_location_ids
from .map_icon_data import data as map_icon_data
from .romWriter import RomWriter


class ItemMarker(Enum):
    big_dot = b"\x01"
    circle = b"\x00"
    small_dot = b"\x02"


class ItemMarkersOption(Enum):
    Simple = "Simple"
    ThreeTiered = "3-Tiered"


LocationToMarker = Mapping[int, ItemMarker]
""" `{` location id (plmparamlo) `: ItemMarker }` """


def write_item_markers(romWriter: RomWriter, markers: LocationToMarker) -> None:
    """ set the icons displayed on in-game maps for items """

    for loc_id, item_marker in markers.items():
        table_entry = map_icon_data[loc_id]
        major_item_addr = table_entry + 6
        # if item_marker.value != b"\x00":
        #     print(f"marked {loc_id=} as {item_marker.value!r} at {major_item_addr}")
        romWriter.writeBytes(major_item_addr, item_marker.value)


def make_item_markers(item_markers_option: ItemMarkersOption, locations: Iterable[Location]) -> LocationToMarker:
    item_markers: dict[int, ItemMarker] = {}

    for loc in locations:
        loc_ids = get_location_ids(loc)
        item = loc["item"]
        assert item
        if item_markers_option != ItemMarkersOption.Simple and item in unique_items:
            for loc_id in loc_ids:
                item_markers[loc_id] = ItemMarker.big_dot
        elif item_markers_option == ItemMarkersOption.ThreeTiered and item.ammo_qty != b"\x00":
            # ammo is small dot
            # print(f"{item.name} is ammo?")  # testing
            for loc_id in loc_ids:
                item_markers[loc_id] = ItemMarker.small_dot
        else:
            assert item_markers_option == ItemMarkersOption.Simple or (
                item not in unique_items and item.ammo_qty == b"\x00"
            ), f"{item_markers_option=} {item=}"
            for loc_id in loc_ids:
                item_markers[loc_id] = ItemMarker.circle

    return item_markers


def markers_to_jsonable(markers: LocationToMarker) -> dict[int, str]:
    return {
        loc_id: marker.name
        for loc_id, marker in markers.items()
    }


def markers_from_jsonable(markers: Mapping[str, str]) -> LocationToMarker:
    return {
        int(loc_id): getattr(ItemMarker, marker_name)
        for loc_id, marker_name in markers.items()
    }
