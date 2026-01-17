import json
import os.path
import pkgutil
from typing import Any, Literal, NamedTuple
from inspect import stack

from .Data.Events import all_events, EventData, EventFlags
from .Data.Locations import all_locations
from .Data.Regions import RegionEnum, all_areas, Nexus

IsFrozen = '.apworld' in os.path.abspath(__file__)


class UTStuff:
    ut_can_gen_without_yaml = True
    found_entrances_datastorage_key = "Slot:{player}:EventMap"

    tracker_world: dict
    tracked_events: EventFlags

    player_map: type[RegionEnum]
    last_map: type[RegionEnum]
    variant: 'MapVariant'
    offsets: dict[str,tuple[int,int]]

    def __init__(self, *args, **kwargs):
        super(UTStuff, self).__init__(*args, **kwargs)
        self.maps = (
        "Maps", [(area.area_name(), all_mapdata[area].get_variant_name(variant)) for area, variant in all_variants])
        self.tracker_world = {
            "map_page_folder": "tracker",
            "map_page_maps": "maps.json",
            "map_page_locations": "locations.json",
            "map_page_setting_key": "Slot:{player}:MapLocation",
            "map_page_index": self.map_page_index,
            "location_setting_key": "Slot:{player}:MapLocation",
            "location_icon_coords": self.location_icon_coords,
            "map_page_groups": [self.maps, (
            "Settings", [("Toggle Split View", "Toggle Split View"), ("Toggle Swap View", "Toggle Swap View")])]
        }
        self.tracked_events = EventFlags(0)
        self.player_map = Nexus
        self.last_map = Nexus
        self.variant = MapVariant(False, self.swap_level)
        if IsFrozen:
            self.tracker_world.update({
                "external_pack_key": "ut_tracker_path",
                "ut_dialog_name": "Select Anodyne's Universal Tracker Pack"
            })
        self.offsets = json.loads(pkgutil.get_data(__name__,"Data/offsets.json"))

    def ut_event_check(self, event: EventData):
        return lambda _: event.flag in self.tracked_events

    def reconnect_found_entrances(self, key: str, value: Any):
        if key.endswith("EventMap") and isinstance(value, int):
            self.tracked_events = EventFlags(value)
            if self.variant.swap_level == 1 and self.swap_level == 2:
                self.variant = MapVariant(self.variant.is_split, 2)
                self.set_maps()

                if len(self.last_map.swap_areas()[1]) > 0:
                    #Reload the map if
                    s = stack()
                    parent_frame = s[1][0]
                    if 'self' in parent_frame.f_locals:
                        tracker = parent_frame.f_locals['self']
                        tracker.load_map(self.map_index(self.last_map))  # re-entrant hack

    def map_index(self, region: type[RegionEnum]):
        return mapname_to_mapid[all_mapdata[region].get_variant_name(self.variant)]

    def map_page_index(self, coords: dict[str, int] | Literal[""] | None):
        print("map page:",coords)
        if not isinstance(coords, dict):
            return 0
        self.player_map = all_areas[coords.get("Map", 0)]
        return self.map_index(self.player_map)

    @property
    def swap_level(self):
        return 2 if EventFlags.SwapExtended in self.tracked_events else 1

    def set_maps(self):
        self.maps[1].clear()
        self.maps[1].extend((region.area_name(), mapdata.get_variant_name(self.variant)) for region, mapdata in
                            all_mapdata.items())

    def location_icon_coords(self, index: int, coords: dict[str, int] | Literal[""] | None) -> tuple[
                                                                                                   int, int, str] | None:
        """Converts player coordinates provided by the game mod into image coordinates for the map page."""
        print("location coords:",index,coords)
        if len(self.maps[1]) == len(all_variants):
            #Set maps when the maps are still the full list used to initialize the UI list.
            self.set_maps()

        if index >= len(all_variants):
            index -= len(all_variants)
            if index == 0:
                self.variant = MapVariant(not self.variant.is_split, self.variant.swap_level)
            elif index == 1:
                self.variant = MapVariant(self.variant.is_split, 0 if self.variant.swap_level > 0 else self.swap_level)
            self.set_maps()

            s = stack()
            parent_frame = s[1][0]
            if 'self' in parent_frame.f_locals:
                tracker = parent_frame.f_locals['self']
                tracker.load_map(self.map_index(self.last_map))  #re-entrant hack

            return None

        self.last_map = all_variants[index][0]

        if not isinstance(coords, dict):
            # Initial call with empty string or no player yet
            return None

        game_region = all_areas[coords.get("Map", 0)]
        self.player_map = game_region
        ut_map = all_variants[index][0]

        if ut_map is Nexus and game_region is not Nexus:
            # Nexus
            return game_region.nexus_ut_loc()[0], game_region.nexus_ut_loc()[1], f"images/icons/young_player.png"

        if ut_map != game_region:
            return None

        res = coords.get("X",0) * 160 + 80, coords.get("Y",0)*160 + 80

        ut_offset = game_region.ut_map_offset()

        res = res[0]+ut_offset[0], res[1]+ut_offset[1]

        if all_variants[index][1].is_split:
            split_offset = self.offsets[game_region.area_name()]
            res = res[0]+split_offset[0], res[1]+split_offset[1]

        return res[0], res[1], f"images/icons/young_player.png"


class MapVariant(NamedTuple):
    is_split: bool
    swap_level: int

    @property
    def is_generated(self):
        return self.is_split or self.swap_level > 0


class MapData:
    region: type[RegionEnum]
    has_split: bool

    def __init__(self, region: type[RegionEnum]):
        self.region = region
        self.has_split = region is not Nexus

    @property
    def has_swap(self):
        return any(len(l) > 0 for l in self.region.swap_areas())

    def swap_mapping(self):
        # noinspection PyListCreation
        ret = [0, 0 if len(self.region.swap_areas()[0]) == 0 else 1]  #self-reference makes literal impossible
        ret.append(ret[1] if len(self.region.swap_areas()[1]) == 0 else 2)
        return ret

    def variants(self) -> list[MapVariant]:
        ret = [MapVariant(False, swap) for swap in sorted(set(self.swap_mapping()))]
        if self.has_split:
            ret.extend([MapVariant(True, variant.swap_level) for variant in ret])
        return ret

    def _match_variant(self, variant: MapVariant):
        """
        Returns a new map variant that matches the request to what this map actually has
        """
        return MapVariant(variant.is_split if self.has_split else False, self.swap_mapping()[variant.swap_level])

    def get_variant_name(self, variant: MapVariant):
        variant = self._match_variant(variant)
        return f"{self.region.area_name()}{':Split' if variant.is_split else ''}{f':Swap{variant.swap_level}' if variant.swap_level > 0 else ''}"

    def get_variant_path(self, variant: MapVariant):
        variant = self._match_variant(variant)
        return f"images/maps/{'generated/' if variant.is_generated else ''}{self.region.__name__.upper()}{'_Split' if variant.is_split else ''}{f'_Swap{variant.swap_level}' if variant.swap_level > 0 else ''}.png"


def map_images():
    ret: dict[type[RegionEnum], MapData] = {}
    for region in all_areas:
        ret[region] = MapData(region)
    return ret


all_mapdata = map_images()

all_variants = [(region, variant) for region, mapdata in all_mapdata.items() for variant in mapdata.variants()]
all_variants.sort(key=lambda d: 0 if d[0] is Nexus else 1)  #Put Nexus first

mapname_to_mapid = {
    all_mapdata[variant[0]].get_variant_name(variant[1]): i for i, variant in enumerate(all_variants)
}


def make_map():
    return [{
        "name": all_mapdata[area].get_variant_name(variant),
        "img": all_mapdata[area].get_variant_path(variant),
        "location_size": 20,
        "location_border_thickness": 1
    } for area, variant in all_variants] + [{
        "name": "Toggle Split View",
        "img": "images/maps/generated/split_view.png"
    }, {
        "name": "Toggle Swap View",
        "img": "images/maps/generated/swap_view.png"
    }]


#####
# Source distribution only functions
#####

class ImageOffsetData(NamedTuple):
    map_offset: tuple[int, int]
    nexus_offset: tuple[int, int]

    @classmethod
    def from_sizes(cls, image_size: tuple[int, int], nexus_size: tuple[int, int]):
        image_width, image_height = image_size
        nexus_width, nexus_height = nexus_size
        if image_height > nexus_height:
            image_offset = 0
            nexus_offset = (image_height - nexus_height) // 2
        else:
            image_offset = (nexus_height - image_height) // 2
            nexus_offset = 0
        return cls((0, image_offset), (image_width, nexus_offset))


def gen_images(img_dir: str) -> dict[type[RegionEnum], ImageOffsetData]:
    from PIL import Image, ImageDraw, ImageColor

    def make_partial_transparent(im: Image):
        im2 = im.copy()
        im2.putalpha(100)
        im.paste(im2, mask=im)

    nexus = Image.open(os.path.join(img_dir, 'images/maps/NEXUS.png'))

    ret = {}
    for area, mapdata in all_mapdata.items():
        if area is Nexus:
            continue
        swap_level_images = [Image.open(os.path.join(img_dir, mapdata.get_variant_path(MapVariant(False, 0)))), None,
                             None]
        offset = ImageOffsetData.from_sizes(swap_level_images[0].size, nexus.size)
        ret[area] = offset

        for variant in mapdata.variants():
            if not variant.is_generated:
                continue
            image = swap_level_images[variant.swap_level]
            if image is None:
                base_image = swap_level_images[0]
                overlay = Image.new('RGBA', base_image.size)
                draw = ImageDraw.Draw(overlay)
                for swap in range(variant.swap_level):
                    color = [ImageColor.getrgb('#00FF00'), ImageColor.getrgb('#FFFF00')][swap]
                    rects = mapdata.region.swap_areas()[swap]
                    for r in rects:
                        draw.rectangle([r[0], r[1], r[0] + r[2], r[1] + r[3]], color)
                make_partial_transparent(overlay)
                image = base_image.copy()
                image = image.convert("RGBA")
                image.alpha_composite(overlay)
                swap_level_images[variant.swap_level] = image

            if variant.is_split:
                combined = Image.new('RGBA', (image.width + nexus.width, max(image.height, nexus.height)))
                combined.paste(image, offset.map_offset)
                combined.paste(nexus, offset.nexus_offset)
                image = combined

            image.save(os.path.join(img_dir, mapdata.get_variant_path(variant)))
    return ret


def location_data(offset_data: dict[type[RegionEnum], ImageOffsetData]):
    all_locs: dict[type[RegionEnum], dict[tuple[int, int], list[str]]] = {}

    for location in all_locations:
        all_locs.setdefault(location.region.__class__, {}).setdefault(location.tracker_loc, []).append(location.name)
        if location.region.__class__ is not Nexus:
            all_locs.setdefault(Nexus, {}).setdefault(location.region.nexus_ut_loc(), []).append(location.name)

    for event in all_events:
        all_locs.setdefault(event.region.__class__, {}).setdefault(event.tracker_loc, []).append(event.name)
        if event.region.__class__ is not Nexus:
            # Move event overviews a bit to the left in the nexus overview so they don't overlap
            loc = event.region.nexus_ut_loc()
            loc = (loc[0] - 25, loc[1])
            all_locs.setdefault(Nexus, {}).setdefault(loc, []).append(event.name)

    def variant_loc(map_loc: tuple[int, int], variant: MapVariant, map_name: str, offset: ImageOffsetData):
        if variant.is_split:
            return {"map": map_name, "x": offset.map_offset[0] + map_loc[0], "y": offset.map_offset[1] + map_loc[1]}
        return {"map": map_name, "x": map_loc[0], "y": map_loc[1]}

    base = [{
        "name": region.area_name(),
        "children": [
            {
                "name": region.area_name(),
                "map_locations": [variant_loc(map_loc, variant, all_mapdata[region].get_variant_name(variant),
                                              offset_data[region] if region is not Nexus else None) for variant in
                                  all_mapdata[region].variants()],
                "sections": [{"name": name} for name in names]
            }
            for map_loc, names in map_locs.items()
        ]
    } for region, map_locs in all_locs.items()]

    for region, mapdata in all_mapdata.items():
        if region is Nexus:
            continue
        nexus_offset = offset_data[region].nexus_offset
        for variant in mapdata.variants():
            if not variant.is_split:
                continue
            base.append({
                "name": f"Nexus-{region.area_name()} split",
                "children": [
                    {
                        "name": region.area_name(),
                        "map_locations": [{"map": mapdata.get_variant_name(variant), "x": map_loc[0] + nexus_offset[0],
                                           "y": map_loc[1] + nexus_offset[1]}],
                        "sections": [{"name": name} for name in names]
                    }
                    for map_loc, names in all_locs[Nexus].items()
                ]
            })
    return base


if not IsFrozen:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(base_dir, "tracker")):
        with open(os.path.join(base_dir, 'tracker/maps.json'), 'w', encoding='utf-8') as f:
            json.dump(make_map(), f, ensure_ascii=True, indent=4)
        offsets = gen_images(os.path.join(base_dir, 'tracker'))
        with open(os.path.join(base_dir, 'Data/offsets.json'), 'w', encoding='utf-8') as f:
            json.dump({region.area_name(): offset.map_offset for region,offset in offsets.items()},f)
        with open(os.path.join(base_dir, 'tracker/locations.json'), 'w', encoding='utf-8') as f:
            json.dump(location_data(offsets), f, ensure_ascii=True, indent=4)
