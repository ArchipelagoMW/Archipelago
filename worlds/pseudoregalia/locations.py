from BaseClasses import Location
from typing import NamedTuple, Callable
from .constants.versions import MAP_PATCH, FULL_GOLD
from .options import PseudoregaliaOptions


class PseudoregaliaLocation(Location):
    game = "Pseudoregalia"


class PseudoregaliaLocationData(NamedTuple):
    region: str
    code: int | None = None
    can_create: Callable[[PseudoregaliaOptions], bool] = lambda options: True
    locked_item: str | None = None


zones = (
    "Dilapidated Dungeon",
    "Castle Sansa",
    "Sansa Keep",
    "Listless Library",
    "Twilight Theatre",
    "Empty Bailey",
    "The Underbelly",
    "Tower Remains",
    "D S T RT ED M M O   Y",
)

location_table = {
    # Sorted by greater region, then subregion
    # Then abilities first
    # Then alphabetically
    # Anything optional goes below the 50 base locations

    "Dilapidated Dungeon - Dream Breaker": PseudoregaliaLocationData(
        code=2365810001,
        region="Dungeon Mirror"),
    "Dilapidated Dungeon - Slide": PseudoregaliaLocationData(
        code=2365810002,
        region="Dungeon Slide"),
    "Dilapidated Dungeon - Alcove Near Mirror": PseudoregaliaLocationData(
        code=2365810003,
        region="Dungeon => Castle",),
    "Dilapidated Dungeon - Dark Orbs": PseudoregaliaLocationData(
        code=2365810004,
        region="Dungeon Escape Upper",),
    "Dilapidated Dungeon - Past Poles": PseudoregaliaLocationData(
        code=2365810005,
        region="Dungeon Strong Eyes",),
    "Dilapidated Dungeon - Rafters": PseudoregaliaLocationData(
        code=2365810006,
        region="Dungeon Strong Eyes",),
    "Dilapidated Dungeon - Strong Eyes": PseudoregaliaLocationData(
        code=2365810007,
        region="Dungeon Strong Eyes",),

    "Castle Sansa - Indignation": PseudoregaliaLocationData(
        code=2365810008,
        region="Castle Main"),
    "Castle Sansa - Alcove Near Dungeon": PseudoregaliaLocationData(
        code=2365810009,
        region="Castle => Theatre Pillar",),
    "Castle Sansa - Balcony": PseudoregaliaLocationData(
        code=2365810010,
        region="Castle Main",),
    "Castle Sansa - Corner Corridor": PseudoregaliaLocationData(
        code=2365810011,
        region="Castle Main",),
    "Castle Sansa - Floater In Courtyard": PseudoregaliaLocationData(
        code=2365810012,
        region="Castle Main",),
    "Castle Sansa - Locked Door": PseudoregaliaLocationData(
        code=2365810013,
        region="Castle Main",
        can_create=lambda options: options.game_version == FULL_GOLD),
    "Castle Sansa - Platform In Main Halls": PseudoregaliaLocationData(
        code=2365810014,
        region="Castle Main",),
    "Castle Sansa - Tall Room Near Wheel Crawlers": PseudoregaliaLocationData(
        code=2365810015,
        region="Castle Main",),
    "Castle Sansa - Wheel Crawlers": PseudoregaliaLocationData(
        code=2365810016,
        region="Castle Main",),
    "Castle Sansa - High Climb From Courtyard": PseudoregaliaLocationData(
        code=2365810017,
        region="Castle High Climb",),
    "Castle Sansa - Alcove Near Scythe Corridor": PseudoregaliaLocationData(
        code=2365810018,
        region="Castle By Scythe Corridor",),
    "Castle Sansa - Near Theatre Front": PseudoregaliaLocationData(
        code=2365810019,
        region="Castle Moon Room",),

    "Sansa Keep - Strikebreak": PseudoregaliaLocationData(
        code=2365810020,
        region="Keep Main"),
    "Sansa Keep - Alcove Near Locked Door": PseudoregaliaLocationData(
        code=2365810021,
        region="Keep Locked Room",),
    "Sansa Keep - Levers Room": PseudoregaliaLocationData(
        code=2365810022,
        region="Keep Main",),
    "Sansa Keep - Lonely Throne": PseudoregaliaLocationData(
        code=2365810023,
        region="Keep Throne Room",),
    "Sansa Keep - Near Theatre": PseudoregaliaLocationData(
        code=2365810024,
        region="Keep Main",),
    "Sansa Keep - Sunsetter": PseudoregaliaLocationData(
        code=2365810025,
        region="Keep Sunsetter"),

    "Listless Library - Sun Greaves": PseudoregaliaLocationData(
        code=2365810026,
        region="Library Greaves",
        can_create=lambda options: not bool(options.split_sun_greaves)),
    "Listless Library - Upper Back": PseudoregaliaLocationData(
        code=2365810027,
        region="Library Top",),
    "Listless Library - Locked Door Across": PseudoregaliaLocationData(
        code=2365810028,
        region="Library Locked",),
    "Listless Library - Locked Door Left": PseudoregaliaLocationData(
        code=2365810029,
        region="Library Locked",),

    "Twilight Theatre - Soul Cutter": PseudoregaliaLocationData(
        code=2365810030,
        region="Theatre Main"),
    "Twilight Theatre - Back Of Auditorium": PseudoregaliaLocationData(
        code=2365810031,
        region="Theatre Main",),
    "Twilight Theatre - Center Stage": PseudoregaliaLocationData(
        code=2365810032,
        region="Theatre Main",),
    "Twilight Theatre - Locked Door": PseudoregaliaLocationData(
        code=2365810033,
        region="Theatre Main",),
    "Twilight Theatre - Tucked Behind Boxes": PseudoregaliaLocationData(
        code=2365810034,
        region="Theatre Main",),
    "Twilight Theatre - Corner Beam": PseudoregaliaLocationData(
        code=2365810035,
        region="Theatre Pillar",),

    "Empty Bailey - Solar Wind": PseudoregaliaLocationData(
        code=2365810036,
        region="Bailey Lower",),
    "Empty Bailey - Center Steeple": PseudoregaliaLocationData(
        code=2365810037,
        region="Bailey Upper",),
    "Empty Bailey - Cheese Bell": PseudoregaliaLocationData(
        code=2365810038,
        region="Bailey Upper",),
    "Empty Bailey - Guarded Hand": PseudoregaliaLocationData(
        code=2365810039,
        region="Bailey Lower",),
    "Empty Bailey - Inside Building": PseudoregaliaLocationData(
        code=2365810040,
        region="Bailey Lower",),

    "The Underbelly - Ascendant Light": PseudoregaliaLocationData(
        code=2365810041,
        region="Underbelly Ascendant Light"),
    "The Underbelly - Alcove Near Light": PseudoregaliaLocationData(
        code=2365810042,
        region="Underbelly Light Pillar",),
    "The Underbelly - Building Near Little Guy": PseudoregaliaLocationData(
        code=2365810043,
        region="Underbelly => Bailey",),
    "The Underbelly - Locked Door": PseudoregaliaLocationData(
        code=2365810044,
        region="Underbelly By Heliacal",),
    "The Underbelly - Main Room": PseudoregaliaLocationData(
        code=2365810045,
        region="Underbelly Main Upper",),
    "The Underbelly - Rafters Near Keep": PseudoregaliaLocationData(
        code=2365810046,
        region="Underbelly => Keep",),
    "The Underbelly - Strikebreak Wall": PseudoregaliaLocationData(
        code=2365810047,
        region="Underbelly Main Upper",),
    "The Underbelly - Surrounded By Holes": PseudoregaliaLocationData(
        code=2365810048,
        region="Underbelly Hole",),

    "Tower Remains - Cling Gem": PseudoregaliaLocationData(
        code=2365810049,
        region="Tower Remains",
        can_create=lambda options: not options.split_cling_gem),
    "Tower Remains - Atop The Tower": PseudoregaliaLocationData(
        code=2365810050,
        region="The Great Door",),

    "Listless Library - Sun Greaves 1": PseudoregaliaLocationData(
        code=2365810051,
        region="Library Greaves",
        can_create=lambda options: bool(options.split_sun_greaves)),
    "Listless Library - Sun Greaves 2": PseudoregaliaLocationData(
        code=2365810052,
        region="Library Greaves",
        can_create=lambda options: bool(options.split_sun_greaves)),
    "Listless Library - Sun Greaves 3": PseudoregaliaLocationData(
        code=2365810053,
        region="Library Greaves",
        can_create=lambda options: bool(options.split_sun_greaves)),
    
    "Dilapidated Dungeon - Time Trial": PseudoregaliaLocationData(
        code=2365810054,
        region="Dungeon Mirror",
        can_create=lambda options: options.game_version == MAP_PATCH and options.randomize_time_trials),
    "Castle Sansa - Time Trial": PseudoregaliaLocationData(
        code=2365810055,
        region="Castle Main",
        can_create=lambda options: options.game_version == MAP_PATCH and options.randomize_time_trials),
    "Sansa Keep - Time Trial": PseudoregaliaLocationData(
        code=2365810056,
        region="Keep Throne Room",
        can_create=lambda options: options.game_version == MAP_PATCH and options.randomize_time_trials),
    "Listless Library - Time Trial": PseudoregaliaLocationData(
        code=2365810057,
        region="Library Main",
        can_create=lambda options: options.game_version == MAP_PATCH and options.randomize_time_trials),
    "Twilight Theatre - Time Trial": PseudoregaliaLocationData(
        code=2365810058,
        region="Theatre Pillar",
        can_create=lambda options: options.game_version == MAP_PATCH and options.randomize_time_trials),
    "Empty Bailey - Time Trial": PseudoregaliaLocationData(
        code=2365810059,
        region="Bailey Upper",
        can_create=lambda options: options.game_version == MAP_PATCH and options.randomize_time_trials),
    "The Underbelly - Time Trial": PseudoregaliaLocationData(
        code=2365810060,
        region="Underbelly Main Upper",
        can_create=lambda options: options.game_version == MAP_PATCH and options.randomize_time_trials),
    "Tower Remains - Time Trial": PseudoregaliaLocationData(
        code=2365810061,
        region="The Great Door",
        can_create=lambda options: options.game_version == MAP_PATCH and options.randomize_time_trials),

    "Castle Sansa - Memento": PseudoregaliaLocationData(
        code=2365810062,
        region="Castle Main",
        can_create=lambda options: options.game_version == MAP_PATCH),

    "Tower Remains - Cling Gem 1": PseudoregaliaLocationData(
        code=2365810063,
        region="Tower Remains",
        can_create=lambda options: bool(options.split_cling_gem),
    ),
    "Tower Remains - Cling Gem 2": PseudoregaliaLocationData(
        code=2365810064,
        region="Tower Remains",
        can_create=lambda options: bool(options.split_cling_gem),
    ),
    "Tower Remains - Cling Gem 3": PseudoregaliaLocationData(
        code=2365810065,
        region="Tower Remains",
        can_create=lambda options: bool(options.split_cling_gem),
    ),

    "Dilapidated Dungeon - Mirror Room Goatling": PseudoregaliaLocationData(
        code=2365810066,
        region="Dungeon Mirror",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Dilapidated Dungeon - Rambling Goatling": PseudoregaliaLocationData(
        code=2365810067,
        region="Dungeon Mirror",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Dilapidated Dungeon - Unwelcoming Goatling": PseudoregaliaLocationData(
        code=2365810068,
        region="Dungeon Strong Eyes",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Dilapidated Dungeon - Repentant Goatling": PseudoregaliaLocationData(
        code=2365810069,
        region="Dungeon Strong Eyes",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Dilapidated Dungeon - Defeatist Goatling": PseudoregaliaLocationData(
        code=2365810070,
        region="Dungeon Strong Eyes",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Castle Sansa - Crystal Licker Goatling": PseudoregaliaLocationData(
        code=2365810071,
        region="Castle Main",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Castle Sansa - Gazebo Goatling": PseudoregaliaLocationData(
        code=2365810072,
        region="Castle Main",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Castle Sansa - Bubblephobic Goatling": PseudoregaliaLocationData(
        code=2365810073,
        region="Castle Main",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Castle Sansa - Trapped Goatling": PseudoregaliaLocationData(
        code=2365810074,
        region="Castle By Scythe Corridor",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Castle Sansa - Memento Goatling": PseudoregaliaLocationData(
        code=2365810075,
        region="Castle Main",
        can_create=lambda options: options.randomize_goats and options.game_version == MAP_PATCH,
    ),
    "Castle Sansa - Goatling Near Library": PseudoregaliaLocationData(
        code=2365810076,
        region="Castle Main",
        can_create=lambda options: options.randomize_goats and options.game_version == MAP_PATCH,
    ),
    "Sansa Keep - Furniture-less Goatling": PseudoregaliaLocationData(
        code=2365810077,
        region="Keep Main",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Sansa Keep - Distorted Goatling": PseudoregaliaLocationData(
        code=2365810078,
        region="Keep (Northeast) => Castle",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Twilight Theatre - 20 Bean Casserole Goatling": PseudoregaliaLocationData(
        code=2365810079,
        region="Castle => Theatre (Front)",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Twilight Theatre - Theatre Goer Goatling 1": PseudoregaliaLocationData(
        code=2365810080,
        region="Castle => Theatre (Front)",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Twilight Theatre - Theatre Goer Goatling 2": PseudoregaliaLocationData(
        code=2365810081,
        region="Castle => Theatre (Front)",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Twilight Theatre - Theatre Manager Goatling": PseudoregaliaLocationData(
        code=2365810082,
        region="Castle => Theatre (Front)",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Twilight Theatre - Murderous Goatling": PseudoregaliaLocationData(
        code=2365810083,
        region="Theatre Main",
        can_create=lambda options: bool(options.randomize_goats),
    ),
    "Empty Bailey - Alley Goatling": PseudoregaliaLocationData(
        code=2365810084,
        region="Bailey Lower",
        can_create=lambda options: bool(options.randomize_goats),
    ),

    "Castle Sansa - Stool Near Crystal 1": PseudoregaliaLocationData(
        code=2365810085,
        region="Castle Main",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Castle Sansa - Stool Near Crystal 2": PseudoregaliaLocationData(
        code=2365810086,
        region="Castle Main",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Castle Sansa - Stool Near Crystal 3": PseudoregaliaLocationData(
        code=2365810087,
        region="Castle Main",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Castle Sansa - Gazebo Stool": PseudoregaliaLocationData(
        code=2365810088,
        region="Castle Main",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Sansa Keep - Distorted Stool": PseudoregaliaLocationData(
        code=2365810089,
        region="Keep (Northeast) => Castle",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Sansa Keep - Path to Throne Stool": PseudoregaliaLocationData(
        code=2365810090,
        region="Keep Throne Room",  # TODO: could define some real logic here, but this mostly works
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Sansa Keep - The Throne": PseudoregaliaLocationData(
        code=2365810091,
        region="Keep Throne Room",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Listless Library - Hay Bale Near Entrance": PseudoregaliaLocationData(
        code=2365810092,
        region="Library Main",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Listless Library - Hay Bale Near Eggs": PseudoregaliaLocationData(
        code=2365810093,
        region="Library Top",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Listless Library - Hay Bale in the Back": PseudoregaliaLocationData(
        code=2365810094,
        region="Library Back",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Twilight Theatre - Stool Near Bookcase": PseudoregaliaLocationData(
        code=2365810095,
        region="Theatre Outside Scythe Corridor",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Twilight Theatre - Stool Around a Table 1": PseudoregaliaLocationData(
        code=2365810096,
        region="Theatre Outside Scythe Corridor",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Twilight Theatre - Stool Around a Table 2": PseudoregaliaLocationData(
        code=2365810097,
        region="Theatre Outside Scythe Corridor",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Twilight Theatre - Stool Around a Table 3": PseudoregaliaLocationData(
        code=2365810098,
        region="Theatre Outside Scythe Corridor",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Twilight Theatre - Stage Left Stool": PseudoregaliaLocationData(
        code=2365810099,
        region="Theatre Main",
        can_create=lambda options: bool(options.randomize_chairs),
    ),
    "Twilight Theatre - Stage Right Stool": PseudoregaliaLocationData(
        code=2365810100,
        region="Theatre Main",
        can_create=lambda options: bool(options.randomize_chairs),
    ),

    "Listless Library - A Book About a Princess": PseudoregaliaLocationData(
        code=2365810101,
        region="Library Main",
        can_create=lambda options: bool(options.randomize_books),
    ),
    "Listless Library - A Book About Cooking": PseudoregaliaLocationData(
        code=2365810102,
        region="Library Main",
        can_create=lambda options: bool(options.randomize_books),
    ),
    "Listless Library - A Book Full of Plays": PseudoregaliaLocationData(
        code=2365810103,
        region="Library Main",
        can_create=lambda options: bool(options.randomize_books),
    ),
    "Listless Library - A Book About Reading": PseudoregaliaLocationData(
        code=2365810104,
        region="Library Main",
        can_create=lambda options: bool(options.randomize_books),
    ),
    "Listless Library - A Book About Aquatic Life": PseudoregaliaLocationData(
        code=2365810105,
        region="Library Main",
        can_create=lambda options: bool(options.randomize_books),
    ),
    "Listless Library - A Book About a Jester": PseudoregaliaLocationData(
        code=2365810106,
        region="Library Main",
        can_create=lambda options: bool(options.randomize_books),
    ),
    "Listless Library - A Book About Loss": PseudoregaliaLocationData(
        code=2365810107,
        region="Library Main",
        can_create=lambda options: bool(options.randomize_books),
    ),
    "Listless Library - A Book on Musical Theory": PseudoregaliaLocationData(
        code=2365810108,
        region="Library Main",
        can_create=lambda options: bool(options.randomize_books),
    ),
    "Listless Library - A Book About a Girl": PseudoregaliaLocationData(
        code=2365810109,
        region="Library Main",
        can_create=lambda options: bool(options.randomize_books),
    ),
    "Listless Library - A Book About a Thimble": PseudoregaliaLocationData(
        code=2365810110,
        region="Library Main",
        can_create=lambda options: bool(options.randomize_books),
    ),
    "Listless Library - A Book About a Monster": PseudoregaliaLocationData(
        code=2365810111,
        region="Library Greaves",
        can_create=lambda options: bool(options.randomize_books),
    ),
    "Listless Library - A Book About Revenge": PseudoregaliaLocationData(
        code=2365810112,
        region="Library Greaves",
        can_create=lambda options: bool(options.randomize_books),
    ),
    "Listless Library - A Book About a Restaurant": PseudoregaliaLocationData(
        code=2365810113,
        region="Library Top",
        can_create=lambda options: bool(options.randomize_books),
    ),

    "Listless Library - Note Near Eggs": PseudoregaliaLocationData(
        code=2365810114,
        region="Library Top",
        can_create=lambda options: bool(options.randomize_notes),
    ),
    "The Underbelly - Note on a Ledge": PseudoregaliaLocationData(
        code=2365810115,
        region="Underbelly => Bailey",
        can_create=lambda options: bool(options.randomize_notes),
    ),
    "The Underbelly - Note in the Big Room": PseudoregaliaLocationData(
        code=2365810116,
        region="Underbelly Main Lower",
        can_create=lambda options: bool(options.randomize_notes),
    ),
    "The Underbelly - Note Behind a Locked Door": PseudoregaliaLocationData(
        code=2365810117,
        region="Underbelly By Heliacal",
        can_create=lambda options: bool(options.randomize_notes),
    ),    

    "D S T RT ED M M O   Y": PseudoregaliaLocationData(
        region="The Great Door",
        locked_item="Something Worth Being Awake For"),
}
