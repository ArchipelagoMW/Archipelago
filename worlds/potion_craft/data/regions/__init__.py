from .. import RegionTypeEnum, ConnectionTypeEnum
from .chapters import ChapterRegions, ChapterConnections

all_regions: list[RegionTypeEnum] = [
    *ChapterRegions
]

all_connections: list[ConnectionTypeEnum] = [
 *ChapterConnections
]