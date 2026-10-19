from .levels import generate_level_locations
from .selling import ShopProduct, generate_license_locations
from .. import LocationTypeEnum, GeneratedLocationData
from .achievement_families import CardAchievementFamily
from .achievements import generate_all_achievement_locations
from .cards import generate_card_sanity_locations
from .events import EventFormat, generate_event_locations

all_Enum_locations: list[LocationTypeEnum] = []

all_Generated_locations: list[GeneratedLocationData] = (
    [
        location
        for family in CardAchievementFamily
        for location in generate_all_achievement_locations(
            family
        )
    ]
    +
    [
        location
        for event in EventFormat
        for location in generate_event_locations([event], games_per_format=999)
    ]
    +
    [
        location
        for location in generate_card_sanity_locations(True, 0, None)
    ]
    +
    [
        location
        for location in generate_level_locations()
    ]
    +
    [
        location
        for product in ShopProduct
        for location in generate_license_locations(product, 999)
    ]
)