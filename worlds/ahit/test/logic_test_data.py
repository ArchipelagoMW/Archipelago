from typing import Dict, Tuple, List, Hashable, TypeVar

from .. import Items
from ..Types import ChapterIndex

from .logic_test_helpers import TestConditions, TestData, SpotType, hashable_vanilla_act_plando

"""
All the different logic tests to check.

Tests try to avoid testing the logic of the internal structure of the world, focusing on a starting point (region) and
what items should be required to reach specific locations from that starting point. For that reason, there are few tests
for individual entrances and no tests specifically checking event items used for logic, such as `TOD Access` and
`AFR Access`.
"""

BASE_WORLD_OPTIONS = {
    # Disable entrance randomization for simplicity.
    "ActRandomizer": "false",
    # With no act randomization, starts other than Chapter 1 can put items into start inventory.
    # The time piece costs for each chapter are overwritten in world_setup() to fixed values.
    "StartingChapter": 1,
    # DLCs and Death Wish are disabled by default to reduce world setup times.
    "EnableDLC1": False,
    "EnableDLC2": False,
    "EnableDeathWish": False,
    # Default to no painting skips.
    "NoPaintingSkips": True,
    # Default to no ticket skips.
    "NoTicketSkips": True,
    # Force the maximum number of thug shop locations.
    "NyakuzaThugMinShopItems": 5,
    "NyakuzaThugMaxShopItems": 5,
    # Enable so that "Progressive Painting Unlock" items are in the pool by default.
    "ShuffleSubconPaintings": True,
    # Enable so that zipline unlock items are in the pool by default.
    "ShuffleAlpineZiplines": True,
    "LogicDifficulty": "normal",
    # Enable so that Umbrella is more logically relevant by default.
    "UmbrellaLogic": True,
    # Due to randomized Hat stitching order, Yarn is difficult to add tests for, so HatItems are enabled by default.
    "HatItems": True,
}

# Each chapter is specifically set to a non-zero time piece requirement so that the first act in a chapter without a
# timepiece requirement does not become accessible with nothing when there is access to Spaceship.
TEST_CHAPTER_TIMEPIECE_COSTS: Dict[ChapterIndex, int] = {
    ChapterIndex.MAFIA: 1,
    ChapterIndex.BIRDS: 2,
    ChapterIndex.SUBCON: 3,
    ChapterIndex.ALPINE: 4,
    ChapterIndex.FINALE: 5,
    ChapterIndex.CRUISE: 6,
    ChapterIndex.METRO: 7,
}

TEST_CHAPTER_TIMEPIECES: Dict[ChapterIndex, Tuple[str, ...]] = {
    chapter_index: ("Time Piece",) * cost for chapter_index, cost in TEST_CHAPTER_TIMEPIECE_COSTS.items()
}


MAIN_SUBCON_ACTS = {
    "Contractual Obligations",
    "The Subcon Well",
    "Toilet of Doom",
    "Queen Vanessa's Manor",
    "Mail Delivery Service",
}

ALL_SUBCON_ACTS = {
    *MAIN_SUBCON_ACTS,
    "Your Contract has Expired",
}

MAFIA_TOWN_ACTS = {
    "Welcome to Mafia Town",
    "Barrel Battle",
    "She Came from Outer Space",
    "Down with the Mafia!",
    "Cheating the Race",
    "Heating Up Mafia Town",
    "The Golden Vault",
}

RUSH_HOUR_TICKETS = {
    "Metro Ticket - Yellow",
    "Metro Ticket - Blue",
    "Metro Ticket - Pink"
}

# Shorten test code by putting the TestConditions classmethods into the module globals.
always = TestConditions.always
always_on_difficulties = TestConditions.always_on_difficulties
never = TestConditions.never
never_on_difficulties = TestConditions.never_on_difficulties

T = TypeVar("T", TestData, List[TestConditions])


def add_options(to: T, **options: Hashable) -> T:
    """Helper to add options to a group of Conditions or an entire TestData dict."""
    if isinstance(to, dict):
        for conditions_list in to.values():
            for conditions in conditions_list:
                conditions.options.update(options)
    elif isinstance(to, list):
        for conditions in to:
            conditions.options.update(options)
    else:
        raise TypeError(f"Could not add options to: {to}")
    return to


LOCATION_TEST_DATA: TestData = {
    # Spaceship
    "Act Completion (Time Rift - Gallery)": [
        always("Time Rift - Gallery", "Brewing Hat"),
        *always_on_difficulties("Time Rift - Gallery", min_difficulty="moderate"),
    ],

    # Chapter 1 - Mafia Town
    # The Mafia HQ platform is only reachable in acts that are chronologically after the start of Down with the Mafia!.
    "Mafia Town - Behind HQ Chest": [
        # todo: Expert logic could probably bucket hover up to the Mafia HQ platform.
        *always_on_difficulties(["Down with the Mafia!", "Cheating the Race", "The Golden Vault"]),
        # The cannon to the platform is only activated once all the faucets have been turned off.
        *always_on_difficulties("Heating Up Mafia Town", "Umbrella"),
        *always_on_difficulties("Heating Up Mafia Town", UmbrellaLogic=False),
        *never_on_difficulties(["Welcome to Mafia Town", "Barrel Battle", "She Came from Outer Space"]),
    ],
    # The Old Men are not present in She Came from Outer Space or Heating Up Mafia Town.
    ("Mafia Town - Old Man (Steel Beams)",
     "Mafia Town - Old Man (Seaside Spaghetti)"): [
        *always_on_difficulties(MAFIA_TOWN_ACTS - {"She Came from Outer Space", "Heating Up Mafia Town"}),
        *never_on_difficulties(["She Came from Outer Space", "Heating Up Mafia Town"]),
    ],
    # This location is not present in She Came from Outer Space because the Time Piece is there instead.
    "Mafia Town - Mafia Geek Platform": [
        *always_on_difficulties(MAFIA_TOWN_ACTS - {"She Came from Outer Space"}),
        *never_on_difficulties("She Came from Outer Space"),
    ],
    # This location is not present in Down with the Mafia! for some unknown reason.
    "Mafia Town - On Scaffolding": [
        *always_on_difficulties(MAFIA_TOWN_ACTS - {"Down with the Mafia!"}),
        *never_on_difficulties("Down with the Mafia!"),
    ],
    # The brewing crate in the way is removed in Heating Up Mafia Town.
    "Mafia Town - Secret Cave": [
        *always_on_difficulties(MAFIA_TOWN_ACTS - {"Heating Up Mafia Town"}, "Brewing Hat"),
        *always_on_difficulties("Heating Up Mafia Town"),
    ],
    # The lava is above sea level, so the player can bounce across the lava (and die) to reach this in Heating Up Mafia
    # Town.
    "Mafia Town - Above Boats": [
        always(MAFIA_TOWN_ACTS - {"Heating Up Mafia Town"}, "Hookshot Badge"),
        # Moderate logic can Ice Hat slide.
        *always_on_difficulties(MAFIA_TOWN_ACTS - {"Heating Up Mafia Town"}, ["Hookshot Badge", "Ice Hat"], min_difficulty="moderate", max_difficulty="hard"),
        # Expert can dive boost off a descending sloped roof to gain incredible speed, launching themselves to this
        # location from far away.
        always(MAFIA_TOWN_ACTS - {"Heating Up Mafia Town"}, LogicDifficulty="expert"),
        *always_on_difficulties("Heating Up Mafia Town"),
    ],
    # This location was previously mistakenly not possible to access with Sprint Hat + Scooter Badge on Normal logic
    # difficulty with CTRLogic: scooter because the Scooter Badge was not being set to ItemClassification.progression.
    "Act Completion (Cheating the Race)": [
        *always_on_difficulties("Cheating the Race", "Time Stop Hat"),
        *always_on_difficulties("Cheating the Race", ["Time Stop Hat", ("Sprint Hat", "Scooter Badge")], CTRLogic="scooter"),
        *always_on_difficulties("Cheating the Race", ["Time Stop Hat", "Sprint Hat"], CTRLogic="sprint"),
        *always_on_difficulties("Cheating the Race", CTRLogic="nothing"),
    ],
    # This location was previously mistakenly not having its moderate logic set.
    "Mafia Town - Clock Tower Chest": [
        always(MAFIA_TOWN_ACTS, "Hookshot Badge"),
        *always_on_difficulties(MAFIA_TOWN_ACTS, min_difficulty="moderate"),
    ],
    # This location was previously mistakenly not having its moderate logic set.
    "Mafia Town - Top of Ruined Tower": [
        always(MAFIA_TOWN_ACTS, "Ice Hat"),
        *always_on_difficulties(MAFIA_TOWN_ACTS, min_difficulty="moderate"),
    ],
    "Mafia Town - Top of Lighthouse": [
        *always_on_difficulties(MAFIA_TOWN_ACTS, "Hookshot Badge", max_difficulty="hard"),
        always(MAFIA_TOWN_ACTS, LogicDifficulty="expert"),
    ],
    "Mafia Town - Hot Air Balloon": [
        *always_on_difficulties(MAFIA_TOWN_ACTS, "Ice Hat", max_difficulty="hard"),
        always(MAFIA_TOWN_ACTS - {"Heating Up Mafia Town"}, LogicDifficulty="expert"),
        always("Heating Up Mafia Town", "Ice Hat", LogicDifficulty="expert"),
    ],

    # Chapter 2 - Battle of the Birds
    # Reaching the Post Elevator Area has a mix of requirements depending on UmbrellaLogic and LogicDifficulty.
    "Dead Bird Studio - Tightrope Chest": [
        *always_on_difficulties("Dead Bird Studio", UmbrellaLogic=False),
        *always_on_difficulties("Dead Bird Studio", ["Umbrella", "Brewing Hat"], max_difficulty="hard"),
        always("Dead Bird Studio Basement", LogicDifficulty="expert", UmbrellaLogic=False),
        always(["Dead Bird Studio", "Dead Bird Studio Basement"], LogicDifficulty="expert"),
        # Access from Dead Bird Studio Basement is expert-only.
        *never_on_difficulties("Dead Bird Studio Basement", max_difficulty="hard"),
    ],
    # These locations are in the Post Elevator Area, but are after a fast moving platform controlled by a lever, which
    # results in slightly different requirements.
    ("Dead Bird Studio - DJ Grooves Sign Chest",
     "Dead Bird Studio - Tepee Chest",
     "Dead Bird Studio - Conductor Chest"): [
        *add_options(UmbrellaLogic=False, to=[
            # Umbrella/Brewing Hat is still required on Normal logic even with UmbrellaLogic=False because the platform
            # starts moving away before Hat Kid is finished recoiling in pain from punching the lever.
            always("Dead Bird Studio", ["Umbrella", "Brewing Hat"]),
            *always_on_difficulties("Dead Bird Studio", min_difficulty="moderate"),
            always("Dead Bird Studio Basement", LogicDifficulty="expert"),
            # Access from Dead Bird Studio Basement is expert-only.
            *never_on_difficulties("Dead Bird Studio Basement", max_difficulty="hard"),
        ]),
        *always_on_difficulties("Dead Bird Studio", ["Umbrella", "Brewing Hat"], max_difficulty="hard"),
        # Expert can climb on top of the walls of the level to get past the gaps with moving platforms.
        always(["Dead Bird Studio", "Dead Bird Studio Basement"], LogicDifficulty="expert"),
        # Access from Dead Bird Studio Basement is expert-only.
        *never_on_difficulties("Dead Bird Studio Basement", max_difficulty="hard"),
    ],
    # This location is in the same area as above, but is only accessible in Dead Bird Studio, so must be tested
    # separately.
    "Act Completion (Dead Bird Studio)": [
        always("Dead Bird Studio", ["Umbrella", "Brewing Hat"], UmbrellaLogic=False),
        *always_on_difficulties("Dead Bird Studio", min_difficulty="moderate", UmbrellaLogic=False),
        always("Dead Bird Studio", ["Umbrella", "Brewing Hat"]),
        *always_on_difficulties("Dead Bird Studio", ["Umbrella", "Brewing Hat"], min_difficulty="moderate", max_difficulty="hard"),
        always("Dead Bird Studio", LogicDifficulty="expert"),
        *never_on_difficulties("Dead Bird Studio Basement"),
    ],
    # Expert logic can clear Dead Bird Studio Basement without hookshot.
    ("Dead Bird Studio Basement - Window Platform",
     "Dead Bird Studio Basement - Cardboard Conductor",
     "Dead Bird Studio Basement - Above Conductor Sign",
     "Dead Bird Studio Basement - Disco Room",
     "Dead Bird Studio Basement - Tightrope",
     "Dead Bird Studio Basement - Cameras",
     "Dead Bird Studio Basement - Locked Room",
     "Act Completion (Dead Bird Studio Basement)"): [
        *always_on_difficulties("Dead Bird Studio Basement", "Hookshot Badge", max_difficulty="hard"),
        always("Dead Bird Studio Basement", LogicDifficulty="expert"),
    ],

    # Chapter 3 - Subcon Forest
    # This location was previously missing accessibility from Your Contract has Expired with no items.
    "Subcon Forest - Boss Arena Chest": [
        # Accessible with nothing from YCHE.
        *always_on_difficulties("Your Contract has Expired"),
        # Normal logic can only access from YCHE and TOD.
        *always_on_difficulties("Toilet of Doom", [("Hookshot Badge", "Progressive Painting Unlock")], max_difficulty="moderate"),
        # Moderate logic and below can only access from YCHE and TOD.
        *never_on_difficulties(MAIN_SUBCON_ACTS - {"Toilet of Doom"}, max_difficulty="moderate"),

        # Cherry bridge across the boss arena gap instead of needing to use Hookshot Badge in Toilet of Doom.
        *always_on_difficulties(MAIN_SUBCON_ACTS, "Progressive Painting Unlock", min_difficulty="hard"),
        # Hard logic cannot skip the boss firewall.
        always(MAIN_SUBCON_ACTS, "Progressive Painting Unlock", LogicDifficulty="hard", NoPaintingSkips=False),

        # Only expert can skip the boss firewall, so the painting unlock is still required.
        always(MAIN_SUBCON_ACTS, "Progressive Painting Unlock", LogicDifficulty="expert"),
        always(MAIN_SUBCON_ACTS, LogicDifficulty="expert", NoPaintingSkips=False),
        # Expert can Snatcher Hover to reach the act completion of YCHE, but this does not grant access to the boss
        # arena itself if logic does not allow painting skips.
        *never_on_difficulties(MAIN_SUBCON_ACTS, "Progressive Painting Unlock"),
    ],
    "Act Completion (Your Contract has Expired)": [
        *always_on_difficulties("Your Contract has Expired", UmbrellaLogic=False),
        *always_on_difficulties("Your Contract has Expired", "Umbrella", max_difficulty="hard"),
        # Expert can 'Snatcher Hover', skipping directly to the post-fight cutscene area.
        always("Your Contract has Expired", LogicDifficulty="expert"),
        # 'Snatcher Hover' also works from other Subcon Forest acts.
        always(MAIN_SUBCON_ACTS, LogicDifficulty="expert")
    ],
    "Act Completion (Toilet of Doom)": [
        *always_on_difficulties("Toilet of Doom", [
            ("Hookshot Badge", "Umbrella", "Progressive Painting Unlock"),
            ("Hookshot Badge", "Brewing Hat", "Progressive Painting Unlock")
        ]),
        always("Toilet of Doom", [
            ("Hookshot Badge", "Umbrella"),
            ("Hookshot Badge", "Brewing Hat")
        ], LogicDifficulty="expert", NoPaintingSkips=False),
        # Expert logic is required to skip the boss firewall.
        *never_on_difficulties("Toilet of Doom", "Progressive Painting Unlock", max_difficulty="hard", NoPaintingSkips=False)
    ],
    # This location was previously missing the requirement to get past the boss firewall.
    "Subcon Village - Snatcher Statue Chest": [
        *always_on_difficulties(MAIN_SUBCON_ACTS, "Progressive Painting Unlock"),
        # Only expert logic can skip the boss firewall.
        *always_on_difficulties(MAIN_SUBCON_ACTS, "Progressive Painting Unlock", max_difficulty="hard", NoPaintingSkips=False),
        always(MAIN_SUBCON_ACTS, LogicDifficulty="expert", NoPaintingSkips=False),
        # Expert can cherry hover across the boss arena gap in reverse. No paintings are needed because YCHE enters from
        # the boss arena, which is already behind the boss firewall.
        always("Your Contract has Expired", LogicDifficulty="expert"),
        # todo: Hard could probably cherry bridge across the boss arena gap in reverse.
        *never_on_difficulties("Your Contract has Expired", max_difficulty="hard")
    ],
    # Paintings can never be skipped for Contractual Obligations.
    "Act Completion (Contractual Obligations)": [
        *never_on_difficulties("Contractual Obligations", "Progressive Painting Unlock", NoPaintingSkips=False),
    ],
    # Moderate logic can reach all locations within Subcon Well with nothing.
    ("Subcon Well - Hookshot Badge Chest",
     "Subcon Well - Above Chest",
     "Subcon Well - Mushroom"): [
        always("The Subcon Well", [
            ("Progressive Painting Unlock", "Umbrella"),
            ("Progressive Painting Unlock", "Brewing Hat"),
        ]),
        always("The Subcon Well", [
            ("Progressive Painting Unlock", "Umbrella"),
            ("Progressive Painting Unlock", "Brewing Hat"),
        ], NoPaintingSkips=False),
        *always_on_difficulties("The Subcon Well", "Progressive Painting Unlock", UmbrellaLogic=False),
        *always_on_difficulties("The Subcon Well", "Progressive Painting Unlock", min_difficulty="moderate"),
        *always_on_difficulties("The Subcon Well", min_difficulty="moderate", NoPaintingSkips=False),
    ],
    ("Subcon Well - On Pipe",
     "Act Completion (The Subcon Well)"): [
        always("The Subcon Well", [
            ("Progressive Painting Unlock", "Hookshot Badge", "Umbrella"),
            ("Progressive Painting Unlock", "Hookshot Badge", "Brewing Hat"),
        ]),
        always("The Subcon Well", [
            ("Progressive Painting Unlock", "Hookshot Badge", "Umbrella"),
            ("Progressive Painting Unlock", "Hookshot Badge", "Brewing Hat"),
        ], NoPaintingSkips=False),
        always("The Subcon Well", [
            ("Progressive Painting Unlock", "Hookshot Badge"),
        ], UmbrellaLogic=False),
        *always_on_difficulties("The Subcon Well", "Progressive Painting Unlock", min_difficulty="moderate"),
        *always_on_difficulties("The Subcon Well", min_difficulty="moderate", NoPaintingSkips=False),
    ],
    # Moderate logic can reach all locations within Queen Vanessa's Manor with nothing.
    ("Queen Vanessa's Manor - Cellar",
     "Queen Vanessa's Manor - Bedroom Chest",
     "Queen Vanessa's Manor - Hall Chest",
     "Queen Vanessa's Manor - Chandelier",
     "Act Completion (Queen Vanessa's Manor)"): [
        # Normal logic needs to be able to hit a Dweller Bell or use their Dweller Mask.
        always("Queen Vanessa's Manor", "Progressive Painting Unlock", UmbrellaLogic=False),
        # Painting skips require at least Moderate logic.
        always("Queen Vanessa's Manor", "Progressive Painting Unlock", UmbrellaLogic=False, NoPaintingSkips=False),
        always("Queen Vanessa's Manor", [
            ("Umbrella", "Progressive Painting Unlock"),
            ("Brewing Hat", "Progressive Painting Unlock"),
            ("Dweller Mask", "Progressive Painting Unlock")
        ], UmbrellaLogic=True),
        *always_on_difficulties("Queen Vanessa's Manor", min_difficulty="moderate", UmbrellaLogic=True, NoPaintingSkips=False),
        *always_on_difficulties("Queen Vanessa's Manor", "Progressive Painting Unlock", min_difficulty="moderate", UmbrellaLogic=True),
    ],
    # Like the locations within Queen Vanessa's Manor, moderate logic can reach this location with nothing.
    "Subcon Forest - Manor Rooftop": [
        always(MAIN_SUBCON_ACTS, "Progressive Painting Unlock", UmbrellaLogic=False),
        # Painting skips require at least Moderate logic.
        always(MAIN_SUBCON_ACTS, "Progressive Painting Unlock", UmbrellaLogic=False, NoPaintingSkips=False),
        always(MAIN_SUBCON_ACTS, [
            ("Umbrella", "Progressive Painting Unlock"),
            ("Brewing Hat", "Progressive Painting Unlock"),
            ("Dweller Mask", "Progressive Painting Unlock")
        ], UmbrellaLogic=True),
        *always_on_difficulties(MAIN_SUBCON_ACTS, min_difficulty="moderate", UmbrellaLogic=False, NoPaintingSkips=False),
        *always_on_difficulties(MAIN_SUBCON_ACTS, "Progressive Painting Unlock", min_difficulty="moderate", UmbrellaLogic=True),
        # Expert can Cherry Hover over the boss arena gap from YCHE to reach the main Subcon Forest area.
        always("Your Contract has Expired", LogicDifficulty="expert", UmbrellaLogic=False, NoPaintingSkips=False),
        *never_on_difficulties("Your Contract has Expired", max_difficulty="hard"),
    ],
    "Act Completion (Time Rift - Village)": [
        *always_on_difficulties("Time Rift - Village", ["Brewing Hat", "Umbrella", "Dweller Mask"], max_difficulty="hard"),
        always("Time Rift - Village", ["Brewing Hat", "Umbrella", "Dweller Mask"], UmbrellaLogic=False),
        # Moderate logic can punch the first dweller bell in the time rift and then, at the final area, jump from the
        # top of the first dweller bell in that area, to the Time Piece.
        *always_on_difficulties("Time Rift - Village", UmbrellaLogic=False, min_difficulty="moderate", max_difficulty="hard"),
        # Expert logic can skip needing to hit the first dweller bell in the time rift with a slingshot.
        always("Time Rift - Village", LogicDifficulty="expert"),
        always("Time Rift - Village", UmbrellaLogic=False, LogicDifficulty="expert"),
    ],
    ("Subcon Forest - Dweller Floating Rocks",
     "Subcon Forest - Dweller Platforming Tree B"): [
        *always_on_difficulties(MAIN_SUBCON_ACTS, [("Dweller Mask",) + (("Progressive Painting Unlock",) * 3)], max_difficulty="moderate"),
        # No Dweller Mask needed for Hard.
        *always_on_difficulties(MAIN_SUBCON_ACTS, [("Progressive Painting Unlock",) * 3], min_difficulty="hard"),
        *never_on_difficulties("Your Contract has Expired"),
        *add_options(NoPaintingSkips=False, to=[
            always(MAIN_SUBCON_ACTS, [("Dweller Mask",) + (("Progressive Painting Unlock",) * 3)]),
            # Moderate can skip paintings.
            always(MAIN_SUBCON_ACTS, "Dweller Mask", LogicDifficulty="moderate"),
            # No Dweller Mask needed for Hard.
            *always_on_difficulties(MAIN_SUBCON_ACTS, min_difficulty="hard"),
            # Only Expert can access from YCHE.
            always("Your Contract has Expired", LogicDifficulty="expert"),
            *never_on_difficulties("Your Contract has Expired", max_difficulty="hard"),
        ]),
    ],
    "Subcon Forest - Noose Treehouse": [
        *always_on_difficulties(MAIN_SUBCON_ACTS, [("Hookshot Badge",) + (("Progressive Painting Unlock",) * 2)], max_difficulty="moderate"),
        *always_on_difficulties(MAIN_SUBCON_ACTS, [("Progressive Painting Unlock",) * 2], min_difficulty="hard"),
        *never_on_difficulties("Your Contract has Expired"),
        *add_options(NoPaintingSkips=False, to=[
            always(MAIN_SUBCON_ACTS, [("Hookshot Badge",) + (("Progressive Painting Unlock",) * 2)]),
            always(MAIN_SUBCON_ACTS, "Hookshot Badge", LogicDifficulty="moderate"),
            *always_on_difficulties(MAIN_SUBCON_ACTS, min_difficulty="hard"),
            always("Your Contract has Expired", LogicDifficulty="expert"),
            *never_on_difficulties("Your Contract has Expired", max_difficulty="hard"),
        ]),
    ],
    "Subcon Forest - Tall Tree Hookshot Swing": [
        *always_on_difficulties(MAIN_SUBCON_ACTS, [("Hookshot Badge",) + (("Progressive Painting Unlock",) * 3)], max_difficulty="moderate"),
        *always_on_difficulties(MAIN_SUBCON_ACTS, [("Progressive Painting Unlock",) * 3], min_difficulty="hard"),
        *never_on_difficulties("Your Contract has Expired"),
        *add_options(NoPaintingSkips=False, to=[
            always(MAIN_SUBCON_ACTS, [("Hookshot Badge",) + (("Progressive Painting Unlock",) * 3)]),
            always(MAIN_SUBCON_ACTS, "Hookshot Badge", LogicDifficulty="moderate"),
            *always_on_difficulties(MAIN_SUBCON_ACTS, min_difficulty="hard"),
            always("Your Contract has Expired", LogicDifficulty="expert"),
            *never_on_difficulties("Your Contract has Expired", max_difficulty="hard"),
        ]),
    ],
    "Subcon Forest - Long Tree Climb Chest": [
        *always_on_difficulties(MAIN_SUBCON_ACTS, [("Dweller Mask",) + (("Progressive Painting Unlock",) * 2)], max_difficulty="moderate"),
        *always_on_difficulties(MAIN_SUBCON_ACTS, [("Progressive Painting Unlock",) * 2], min_difficulty="hard"),
        *never_on_difficulties("Your Contract has Expired"),
        *add_options(NoPaintingSkips=False, to=[
            always(MAIN_SUBCON_ACTS, [("Dweller Mask",) + (("Progressive Painting Unlock",) * 2)]),
            always(MAIN_SUBCON_ACTS, "Dweller Mask", LogicDifficulty="moderate"),
            *always_on_difficulties(MAIN_SUBCON_ACTS, min_difficulty="hard"),
            always("Your Contract has Expired", LogicDifficulty="expert"),
            *never_on_difficulties("Your Contract has Expired", max_difficulty="hard"),
        ]),
    ],
    "Subcon Forest - Magnet Badge Bush": [
        *always_on_difficulties(MAIN_SUBCON_ACTS, [("Brewing Hat",) + (("Progressive Painting Unlock",) * 3)], max_difficulty="hard"),
        always(MAIN_SUBCON_ACTS, [("Progressive Painting Unlock",) * 3], LogicDifficulty="expert"),
        *never_on_difficulties("Your Contract has Expired"),
        *add_options(NoPaintingSkips=False, to=[
            always(MAIN_SUBCON_ACTS, [("Brewing Hat",) + (("Progressive Painting Unlock",) * 3)]),
            *always_on_difficulties(MAIN_SUBCON_ACTS, "Brewing Hat", max_difficulty="hard"),
            always(MAIN_SUBCON_ACTS, LogicDifficulty="expert"),
            always("Your Contract has Expired", LogicDifficulty="expert"),
            *never_on_difficulties("Your Contract has Expired", max_difficulty="hard"),
        ])
    ],
    # These locations were previous missing the requirement to get past the first firewall. The locations can be
    # collected in any order, but only two are accessible without a Progressive Painting Unlock, so all three must
    # logically require a painting unlock.
    ("Snatcher's Contract - Toilet of Doom",
     "Snatcher's Contract - Queen Vanessa's Manor",
     "Snatcher's Contract - Mail Delivery Service"): [
        *always_on_difficulties("Subcon Forest Area", "Progressive Painting Unlock"),
        *always_on_difficulties("Subcon Forest Area", min_difficulty="moderate", NoPaintingSkips=False),
    ],
    # This location looks similar to the above Contract locations, but should have separate rules.
    "Snatcher's Contract - The Subcon Well": [
        *always_on_difficulties("Contractual Obligations"),
        # This contract is only reachable from Contractual Obligations.
        *never_on_difficulties(MAIN_SUBCON_ACTS - {"Contractual Obligations"}),
    ],

    # Chapter 4 - Alpine Skyline
    # No Brewing Hat needed for Moderate logic.
    "Alpine Skyline - Yellow Band Hills": [
        always("Alpine Free Roam", [("Umbrella", "Hookshot Badge", "Zipline Unlock - The Birdhouse Path", "Brewing Hat")]),
        *always_on_difficulties("Alpine Free Roam", [("Umbrella", "Hookshot Badge", "Zipline Unlock - The Birdhouse Path")], min_difficulty="moderate"),
        always("The Illness has Spread", [("Hookshot Badge", "Zipline Unlock - The Birdhouse Path", "Brewing Hat")]),
        *always_on_difficulties("The Illness has Spread", [("Hookshot Badge", "Zipline Unlock - The Birdhouse Path")], min_difficulty="moderate"),
        *add_options(UmbrellaLogic=False, to=[
            always(["Alpine Free Roam", "The Illness has Spread"], [("Hookshot Badge", "Zipline Unlock - The Birdhouse Path", "Brewing Hat")]),
            *always_on_difficulties(["Alpine Free Roam", "The Illness has Spread"], [("Hookshot Badge", "Zipline Unlock - The Birdhouse Path")], min_difficulty="moderate"),
        ]),
        *add_options(ShuffleAlpineZiplines=False, to=[
            always("Alpine Free Roam", [("Umbrella", "Hookshot Badge", "Brewing Hat")]),
            *always_on_difficulties("Alpine Free Roam", [("Umbrella", "Hookshot Badge")], min_difficulty="moderate"),
            always("The Illness has Spread", [("Hookshot Badge", "Brewing Hat")]),
            *always_on_difficulties("The Illness has Spread", "Hookshot Badge", min_difficulty="moderate"),
            *add_options(UmbrellaLogic=False, to=[
                always(["Alpine Free Roam", "The Illness has Spread"], [("Hookshot Badge", "Brewing Hat")]),
                *always_on_difficulties(["Alpine Free Roam", "The Illness has Spread"], "Hookshot Badge", min_difficulty="moderate"),
            ]),
        ]),
    ],
    "Alpine Skyline - The Birdhouse: Dweller Platforms Relic": [
        always("The Birdhouse", "Dweller Mask"),
        *always_on_difficulties("The Birdhouse", min_difficulty="moderate"),
    ],
    # Moderate and above can void out to warp past the section that would otherwise require the Dweller Mask.
    "Alpine Skyline - The Twilight Path": [
        always("Alpine Free Roam", [("Umbrella", "Hookshot Badge", "Dweller Mask", "Zipline Unlock - The Twilight Bell Path")]),
        *always_on_difficulties("Alpine Free Roam", [("Umbrella", "Hookshot Badge", "Zipline Unlock - The Twilight Bell Path")], min_difficulty="moderate"),
        *add_options(UmbrellaLogic=False, to=[
            always("Alpine Free Roam", [("Hookshot Badge", "Dweller Mask", "Zipline Unlock - The Twilight Bell Path")]),
            *always_on_difficulties("Alpine Free Roam", [("Hookshot Badge", "Zipline Unlock - The Twilight Bell Path")], min_difficulty="moderate"),
        ]),
        *never_on_difficulties("The Illness has Spread"),
        *add_options(ShuffleAlpineZiplines=False, to=[
            always("Alpine Free Roam", [("Umbrella", "Hookshot Badge", "Dweller Mask")]),
            *always_on_difficulties("Alpine Free Roam", [("Umbrella", "Hookshot Badge")], min_difficulty="moderate"),
            *add_options(UmbrellaLogic=False, to=[
                always("Alpine Free Roam", [("Hookshot Badge", "Dweller Mask")]),
                *always_on_difficulties("Alpine Free Roam", "Hookshot Badge", min_difficulty="moderate"),
            ]),
        ]),
    ],
    # Moderate can reach without Sprint Hat or Time Stop Hat.
    "Alpine Skyline - Mystifying Time Mesa: Zipline": [
        always("Alpine Free Roam", [
            ("Umbrella", "Hookshot Badge", "Sprint Hat", "Zipline Unlock - The Lava Cake Path"),
            ("Umbrella", "Hookshot Badge", "Time Stop Hat", "Zipline Unlock - The Lava Cake Path")]),
        # No hats needed for moderate logic.
        *always_on_difficulties("Alpine Free Roam", [("Umbrella", "Hookshot Badge", "Zipline Unlock - The Lava Cake Path")], min_difficulty="moderate"),
        *add_options(UmbrellaLogic=False, to=[
            always("Alpine Free Roam", [
                ("Hookshot Badge", "Sprint Hat", "Zipline Unlock - The Lava Cake Path"),
                ("Hookshot Badge", "Time Stop Hat", "Zipline Unlock - The Lava Cake Path")
            ]),
            *always_on_difficulties("Alpine Free Roam", [("Hookshot Badge", "Zipline Unlock - The Lava Cake Path")], min_difficulty="moderate"),
        ]),
        # The Zipline is blocked off in TIHS.
        *never_on_difficulties("The Illness has Spread"),
    ],
    "Alpine Skyline - Goat Refinery": [
        # There is no way to get past the Alpine Free Roam intro without these items, which provides enough to reach
        # the location once past the intro.
        *always_on_difficulties("Alpine Free Roam", [("Hookshot Badge", "Umbrella")]),
        *always_on_difficulties("Alpine Free Roam", "Hookshot Badge", UmbrellaLogic=False),
        # Normal logic cannot get this item from The Illness has Spread because the hookpoint is blocked and Normal
        # logic has no trick to reach the location without using the hookpoint.
        never("The Illness has Spread"),
        # Moderate logic can use Sprint Hat to cross the gap to Goat Refinery.
        always("The Illness has Spread", "Sprint Hat", LogicDifficulty="moderate"),
        # Hard logic can cross the gap with nothing.
        *always_on_difficulties("The Illness has Spread", min_difficulty="hard"),
    ],
    "Act Completion (Time Rift - The Twilight Bell)": [
        *always_on_difficulties("Time Rift - The Twilight Bell", "Dweller Mask", max_difficulty="moderate"),
        # Hard can jump around the Dweller wall with the Scooter.
        always("Time Rift - The Twilight Bell", ["Dweller Mask", ("Sprint Hat", "Scooter Badge")], LogicDifficulty="hard"),
        # Expert can jump around the Dweller wall with nothing.
        always("Time Rift - The Twilight Bell", LogicDifficulty="expert"),
    ],
    "Act Completion (Time Rift - Curly Tail Trail)": [
        *always_on_difficulties("Time Rift - Curly Tail Trail", "Ice Hat", max_difficulty="moderate"),
        # SDJ.
        always("Time Rift - Curly Tail Trail", ["Ice Hat", "Sprint Hat"], LogicDifficulty="hard"),
        # Slingshot.
        always("Time Rift - Curly Tail Trail", LogicDifficulty="expert"),
    ],
    # Goat Outpost Horn was previously missing accessibility from The Illness has Spread.
    ("Alpine Skyline - Goat Outpost Horn",
     "Alpine Skyline - Windy Passage"): [
        *add_options(UmbrellaLogic=False, ShuffleAlpineZiplines=False, to=[
            *always_on_difficulties("Alpine Free Roam", "Hookshot Badge"),
            *always_on_difficulties("The Illness has Spread", "Hookshot Badge"),
        ]),
        *never_on_difficulties("Alpine Free Roam", ["Zipline Unlock - The Windmill Path", "Umbrella"]),
        *never_on_difficulties("The Illness has Spread", "Zipline Unlock - The Windmill Path"),
        *never_on_difficulties(["Alpine Free Roam", "The Illness has Spread"], "Zipline Unlock - The Windmill Path", UmbrellaLogic=False),
        *never_on_difficulties("Alpine Free Roam", "Umbrella", ShuffleAlpineZiplines=False),
    ],
    "Act Completion (The Twilight Bell)": [
        *add_options(UmbrellaLogic=False, ShuffleAlpineZiplines=False, to=[
            *always_on_difficulties("Alpine Free Roam", [("Hookshot Badge", "Dweller Mask")], max_difficulty="moderate"),
            always("Alpine Free Roam", [("Hookshot Badge", "Dweller Mask")], LogicDifficulty="hard"),
            always("Alpine Free Roam", [
                ("Hookshot Badge", "Brewing Hat"),
                ("Hookshot Badge", "Dweller Mask"),
                ("Hookshot Badge", "Sprint Hat"),
                # The Time Stop Hat + Umbrella option still requires Umbrella with Umbrella logic not enabled.
                ("Hookshot Badge", "Umbrella", "Time Stop Hat"),
            ], LogicDifficulty="expert"),
        ]),
        *never_on_difficulties("Alpine Free Roam", ["Zipline Unlock - The Twilight Bell Path", "Umbrella"]),
        *never_on_difficulties("Alpine Free Roam", "Zipline Unlock - The Twilight Bell Path", UmbrellaLogic=False),
        *never_on_difficulties("Alpine Free Roam", "Umbrella", ShuffleAlpineZiplines=False),
        *never_on_difficulties("The Illness has Spread"),
    ],

    # Chapter 5 - The Finale
    "Act Completion (The Finale)": [
        # No difficulties need Ice Hat.
        always("The Finale", [("Hookshot Badge", "Dweller Mask")]),
        # Moderate does not need Hookshot Badge.
        *always_on_difficulties("The Finale", "Dweller Mask", min_difficulty="moderate"),
    ],
}


DLC1_LOCATION_TEST_DATA: TestData = add_options(EnableDLC1=True, to={
    # Chapter 6 - The Arctic Cruise
    # This location does not exist in Rock the Boat, so can only be accessed from Bon Voyage! or Ship Shape.
    # This location was previously missing the Hookshot Badge requirement to reach the Cruise Ship region from
    # Bon Voyage!.
    # Rock the Boat gives access to the Cruise Ship region with no items required, but this location is not present in
    # Rock the Boat, so access to either Ship Shape or Bon Voyage! is required.
    "The Arctic Cruise - Toilet": [
        *always_on_difficulties("Ship Shape"),
        *always_on_difficulties("Bon Voyage!", "Hookshot Badge"),
        # Neither of these combinations of accessible regions can give access to the location without Hookshot Badge.
        *never_on_difficulties([("Cruise Ship", "Bon Voyage!"), ("Rock the Boat", "Bon Voyage!")], "Hookshot Badge"),
        # With all items, neither of these regions are enough to reach the location.
        *never_on_difficulties(["Cruise Ship", "Rock the Boat"]),
    ],
    # These locations were previously mistakenly not having their moderate logic set, due to using the wrong rule
    # function.
    ("Rock the Boat - Post Captain Rescue",
     "Act Completion (Rock the Boat)"): [
        always("Rock the Boat", "Ice Hat"),
        # Moderate can jump across the freezing water while taking damage.
        *always_on_difficulties("Rock the Boat", min_difficulty="moderate"),
    ],
    "Act Completion (Time Rift - Deep Sea)": [
        always("Time Rift - Deep Sea", [("Hookshot Badge", "Dweller Mask", "Ice Hat")]),
        # Moderate can reach enough Rift Pons without Ice Hat.
        always("Time Rift - Deep Sea", [("Hookshot Badge", "Dweller Mask")], LogicDifficulty="moderate"),
        # Hard can reach enough Rift Pons without either Ice Hat or Dweller Mask.
        *always_on_difficulties("Time Rift - Deep Sea", "Hookshot Badge", min_difficulty="hard"),
    ],
})


DLC2_LOCATION_TEST_DATA: TestData = add_options(EnableDLC2=True, to={
    # Chapter 7 - Nyakuza Metro
    "Act Completion (Yellow Overpass Station)": [
        always(["Nyakuza Free Roam", "Yellow Overpass Station"], "Hookshot Badge"),
        *always_on_difficulties(["Nyakuza Free Roam", "Yellow Overpass Station"], min_difficulty="moderate"),
    ],
    "Pink Paw Station - Behind Fan": [
        # Tickets are always required with NoTicketSkips=True
        always("Nyakuza Free Roam", [
            ("Metro Ticket - Blue", "Metro Ticket - Yellow", "Hookshot Badge", "Time Stop Hat", "Dweller Mask"),
            ("Metro Ticket - Pink", "Hookshot Badge", "Time Stop Hat", "Dweller Mask")]),
        # Only tickets required on moderate logic.
        *always_on_difficulties("Nyakuza Free Roam", [
            ("Metro Ticket - Blue", "Metro Ticket - Yellow"),
            "Metro Ticket - Pink"
        ], min_difficulty="moderate"),
        # Rush Hour ticket skips only allows ticket skips in Rush Hour, and not in Nyakuza Free Roam.
        *add_options(NoTicketSkips="rush_hour", to=[
            always("Nyakuza Free Roam", [
                ("Metro Ticket - Blue", "Metro Ticket - Yellow", "Hookshot Badge", "Time Stop Hat", "Dweller Mask"),
                ("Metro Ticket - Pink", "Hookshot Badge", "Time Stop Hat", "Dweller Mask")]),
            # Only tickets required on moderate logic.
            *always_on_difficulties("Nyakuza Free Roam", [
                ("Metro Ticket - Blue", "Metro Ticket - Yellow"),
                "Metro Ticket - Pink"
            ], min_difficulty="moderate"),
        ]),
        *add_options(NoTicketSkips=False, to=[
            # Normal logic cannot perform ticket skips, so still needs the tickets.
            always("Nyakuza Free Roam", [
                ("Metro Ticket - Blue", "Metro Ticket - Yellow", "Hookshot Badge", "Time Stop Hat", "Dweller Mask"),
                ("Metro Ticket - Pink", "Hookshot Badge", "Time Stop Hat", "Dweller Mask")]),
            # Moderate can wrongwarp into Pink Paw Station from Yellow Overpass Station, so requires nothing.
            *always_on_difficulties("Nyakuza Free Roam", min_difficulty="moderate"),
        ]),
    ],
    # This location was previously mistakenly not setting its ticket skips logic in Hard logic, so was acting as if
    # ticket skips were always disabled.
    # This location was previously mistakenly not setting its Rush Hour-only ticket skips logic in Expert logic.
    "Act Completion (Rush Hour)": [
        # Rush Hour ticket skips are only in logic on Hard LogicDifficulty and above.
        always("Rush Hour", [("Brewing Hat", "Dweller Mask", "Ice Hat", "Hookshot Badge", *RUSH_HOUR_TICKETS)]),
        always("Rush Hour", [("Brewing Hat", "Dweller Mask", "Ice Hat", "Hookshot Badge", *RUSH_HOUR_TICKETS)], NoTicketSkips=False),
        always("Rush Hour", [("Brewing Hat", "Dweller Mask", "Ice Hat", "Hookshot Badge", *RUSH_HOUR_TICKETS)], NoTicketSkips="rush_hour"),
        # Moderate logic can do wall jumps to skip needing Hookshot Badge and can make precise jumps and go under
        # Dweller signs to skip needing Dweller Mask.
        *add_options(LogicDifficulty="moderate", to=[
            always("Rush Hour", [("Brewing Hat", "Ice Hat", *RUSH_HOUR_TICKETS)]),
            always("Rush Hour", [("Brewing Hat", "Ice Hat", *RUSH_HOUR_TICKETS)], NoTicketSkips=False),
            always("Rush Hour", [("Brewing Hat", "Ice Hat", *RUSH_HOUR_TICKETS)], NoTicketSkips="rush_hour"),
        ]),
        # Hard logic can perform the ticket skip when ticket skips are in logic and can skip Ice Hat by jumping directly
        # from Green Clean Station to Yellow Overpass Station while avoiding the kill plane under most of Green Clean.
        *add_options(LogicDifficulty="hard", to=[
            always("Rush Hour", [("Brewing Hat", *RUSH_HOUR_TICKETS)]),
            always("Rush Hour", "Brewing Hat", NoTicketSkips=False),
            always("Rush Hour", "Brewing Hat", NoTicketSkips="rush_hour"),
        ]),
        # Expert logic can go out-of-bounds to bypass the brewing obstacle.
        *add_options(LogicDifficulty="expert", to=[
            always("Rush Hour", [tuple(RUSH_HOUR_TICKETS)]),
            always("Rush Hour", NoTicketSkips=False),
            always("Rush Hour", NoTicketSkips="rush_hour"),
        ]),
    ],
    # This thug shop has unique logical requirements.
    ("Green Clean Station Thug B - Item 1",
     "Green Clean Station Thug B - Item 2",
     "Green Clean Station Thug B - Item 3",
     "Green Clean Station Thug B - Item 4",
     "Green Clean Station Thug B - Item 5"): [
        *always_on_difficulties("Nyakuza Free Roam", ["Ice Hat", "Metro Ticket - Yellow"])
    ],
    # In the upper section of Pink Paw Station, so additionally requires Hookshot Badge + Dweller Mask.
    "Act Completion (Pink Paw Station)": [
        always("Nyakuza Free Roam", [
            ("Metro Ticket - Pink", "Hookshot Badge", "Dweller Mask"),
            ("Metro Ticket - Yellow", "Metro Ticket - Blue", "Hookshot Badge", "Dweller Mask"),
        ]),
        # Hookshot Badge + Dweller Mask can be skipped using either wall jumps or the wrongwarp from Yellow Overpass.
        *always_on_difficulties("Nyakuza Free Roam", [
            "Metro Ticket - Pink",
            ("Metro Ticket - Yellow", "Metro Ticket - Blue"),
        ], min_difficulty="moderate"),
        *always_on_difficulties("Nyakuza Free Roam", min_difficulty="moderate", NoTicketSkips=False),
    ],
    "Act Completion (Green Clean Manhole)": [
        *always_on_difficulties("Nyakuza Free Roam", [("Ice Hat", "Dweller Mask")], max_difficulty="moderate"),
        # Hard can jump from the sign below the Dweller roof and wall jump to get on top of the Dweller roof.
        always("Nyakuza Free Roam", "Ice Hat", LogicDifficulty="hard"),
        # Boop Clip to get into the manhole area without entering the manhole.
        always("Nyakuza Free Roam", LogicDifficulty="expert"),
    ],
    "Act Completion (Yellow Overpass Manhole)": [
        *always_on_difficulties("Nyakuza Free Roam", "Ice Hat", max_difficulty="hard"),
        # Boop Clip to get into the manhole area without entering the manhole.
        always("Nyakuza Free Roam", LogicDifficulty="expert"),
    ],
})


DEATH_WISH_OPTIONS: Dict[str, Hashable] = dict(
    # Fully enable Death Wish locations.
    EnableDeathWish=True,
    DWEnableBonus=True,
    DWAutoCompleteBonuses=False,
    DWExcludeAnnoyingContracts=False,
    DWExcludeAnnoyingBonuses=False,
    DWExcludeCandles=False,
)


DEATH_WISH_LOCATION_TEST_DATA: TestData = add_options(**DEATH_WISH_OPTIONS, to={
    # Death Wish
    # Auto-completed Bonus Stamp locations were previously missing the requirement to complete the contract's Main
    # Objective, which would incorrectly grant Bonus Stamps as soon as the Death Wish contract was unlocked.
    "Bonus Stamps - Beat the Heat": [
        # With Umbrella logic enabled, Umbrella is required to complete the Main Objective of Beat the Heat.
        *always_on_difficulties("Beat the Heat", "Umbrella"),
        *always_on_difficulties("Beat the Heat", "Umbrella", DWAutoCompleteBonuses=True),
        *always_on_difficulties("Beat the Heat", "Umbrella", DWEnableBonus=False),
        *always_on_difficulties("Beat the Heat", "Umbrella", DWEnableBonus=False, DWAutoCompleteBonuses=True),
        # With Umbrella logic disabled, no items are required to complete the Main Objective of Beat the Heat.
        *add_options(UmbrellaLogic=False, to=[
            *always_on_difficulties("Beat the Heat"),
            *always_on_difficulties("Beat the Heat", DWAutoCompleteBonuses=True),
            *always_on_difficulties("Beat the Heat", DWEnableBonus=False),
            *always_on_difficulties("Beat the Heat", DWEnableBonus=False, DWAutoCompleteBonuses=True),
        ]),
    ],
    # Camera Tourist
    # There was previously a mismatch between the locations and logic, where one used the name "Director" and the other
    # used the name "Conductor", so the Hookshot Badge logic requirement for this location was not being set.
    "Director - Dead Bird Studio Basement": [
        always("Dead Bird Studio Basement", "Hookshot Badge"),
        # todo: There is currently no expert logic set for reaching this location without Hookshot Badge.
        # always("Dead Bird Studio Basement", LogicDifficulty="expert"),
    ],
    # This location was previously missing all item requirements.
    "Toilet - Toilet of Doom": [
        # The boss is behind the boss firewall, so Expert is the only difficulty that does not need the Progressive
        # Painting Unlock with NoPaitningSkips=False.
        *always_on_difficulties("Toilet of Doom", [("Progressive Painting Unlock", "Hookshot Badge")], max_difficulty="moderate"),
        # Hard logic can cherry bridge across the boss arena gap.
        *always_on_difficulties("Toilet of Doom", "Progressive Painting Unlock", min_difficulty="hard"),
        always("Toilet of Doom", "Progressive Painting Unlock", LogicDifficulty="hard", NoPaintingSkips=False),
        always("Toilet of Doom", LogicDifficulty="expert", NoPaintingSkips=False),
    ],
    # Snatcher Coins
    # This location was previously missing the requirement to be able to complete Beat the Heat. The cannon to the HQ
    # platform only opens once all faucets have been turned off.
    "Snatcher Coin - Top of HQ (DW: BTH)": [
        *always_on_difficulties("Beat the Heat", "Umbrella"),
        *always_on_difficulties("Beat the Heat", UmbrellaLogic=False),
    ],
    # todo: Snatcher Coin - Swamp Tree and Snatcher Coin - Swamp Tree (Speedrun Well) should not need Hookshot on higher
    #  logic difficulties.
    # todo: Snatcher Coin - Manor Roof is missing moderate logic
})


ENTRANCE_TEST_DATA: TestData = {
    # Chapter 3 - Subcon Forest
    # "Subcon Forest" is the name for the Chapter 3 telescope Region, it is not related to "Subcon Forest Area".
    "Subcon Forest - Act 2": [
        *always_on_difficulties("Spaceship", [("Snatcher's Contract - The Subcon Well", *TEST_CHAPTER_TIMEPIECES[ChapterIndex.SUBCON])]),
        *always_on_difficulties("Subcon Forest", "Snatcher's Contract - The Subcon Well"),
    ],
    "Subcon Forest - Act 3": [
        *always_on_difficulties("Spaceship", [("Snatcher's Contract - Toilet of Doom", *TEST_CHAPTER_TIMEPIECES[ChapterIndex.SUBCON])]),
        *always_on_difficulties("Subcon Forest", "Snatcher's Contract - Toilet of Doom"),
    ],
    "Subcon Forest - Act 4": [
        *always_on_difficulties("Spaceship", [("Snatcher's Contract - Queen Vanessa's Manor", *TEST_CHAPTER_TIMEPIECES[ChapterIndex.SUBCON])]),
        *always_on_difficulties("Subcon Forest", "Snatcher's Contract - Queen Vanessa's Manor"),
    ],
    "Subcon Forest - Act 5": [
        *always_on_difficulties("Spaceship", [("Snatcher's Contract - Mail Delivery Service", *TEST_CHAPTER_TIMEPIECES[ChapterIndex.SUBCON])]),
        *always_on_difficulties("Subcon Forest", "Snatcher's Contract - Mail Delivery Service"),
    ],

    # Chapter 4 - Alpine Skyline
    "Alpine Skyline - Finale": [
        *never_on_difficulties("Alpine Skyline", [
            "Zipline Unlock - The Birdhouse Path",
            "Zipline Unlock - The Lava Cake Path",
            "Zipline Unlock - The Windmill Path",
            "Zipline Unlock - The Twilight Bell Path",
            "Umbrella",
            "Hookshot Badge",
        ]),
        *never_on_difficulties("Alpine Skyline", [
            "Zipline Unlock - The Birdhouse Path",
            "Zipline Unlock - The Lava Cake Path",
            "Zipline Unlock - The Windmill Path",
            "Zipline Unlock - The Twilight Bell Path",
            "Hookshot Badge",
        ], UmbrellaLogic=False),
        *add_options(ShuffleAlpineZiplines=False, UmbrellaLogic=False, to=[
            always("Alpine Skyline", [
                ("Hookshot Badge", "Brewing Hat", "Dweller Mask")
            ]),
            # Moderate does not need Brewing Hat for completing The Birdhouse.
            *always_on_difficulties("Alpine Skyline", [
                ("Hookshot Badge", "Dweller Mask")
            ], min_difficulty="moderate", max_difficulty="hard"),
            # Expert has alternatives to Dweller Mask for completing The Twilight Bell.
            # See also: Act Completion (The Twilight Bell).
            always("Alpine Skyline", [
                ("Hookshot Badge", "Brewing Hat"),
                ("Hookshot Badge", "Dweller Mask"),
                ("Hookshot Badge", "Sprint Hat"),
                ("Hookshot Badge", "Umbrella", "Time Stop Hat"),
            ], LogicDifficulty="expert"),
        ]),
    ],
}

REGION_TEST_DATA: TestData = {
    # Spaceship
    "Mafia Town": [
        *always_on_difficulties("Spaceship", [tuple(TEST_CHAPTER_TIMEPIECES[ChapterIndex.MAFIA])]),
    ],
    "Battle of the Birds": [
        *always_on_difficulties("Spaceship", [tuple(TEST_CHAPTER_TIMEPIECES[ChapterIndex.BIRDS])]),
    ],
    "Subcon Forest": [
        *always_on_difficulties("Spaceship", [tuple(TEST_CHAPTER_TIMEPIECES[ChapterIndex.SUBCON])]),
    ],
    "Alpine Skyline": [
        *always_on_difficulties("Spaceship", [tuple(TEST_CHAPTER_TIMEPIECES[ChapterIndex.ALPINE])]),
    ],
    "Time's End": [
        # No difficulties need Ice Hat because the ceiling button can be reached by jumping from the top of the Dweller
        # block.
        always("Spaceship", [("Dweller Mask", "Brewing Hat", *TEST_CHAPTER_TIMEPIECES[ChapterIndex.FINALE])]),
        # Moderate can alternatively bounce on a beach ball with the Ice Hat to get over the iron bars blocking access
        # to the telescope.
        *always_on_difficulties("Spaceship", [
            ("Dweller Mask", "Brewing Hat", *TEST_CHAPTER_TIMEPIECES[ChapterIndex.FINALE]),
            ("Ice Hat", *TEST_CHAPTER_TIMEPIECES[ChapterIndex.FINALE])
        ], min_difficulty="moderate", max_difficulty="hard"),
        always("Spaceship", [tuple(TEST_CHAPTER_TIMEPIECES[ChapterIndex.FINALE])], LogicDifficulty="expert"),
    ],
    # The Chapter 6 and 7 doors are behind the Chapter 4 door.
    "The Arctic Cruise": [
        *always_on_difficulties("Spaceship", [
            ("Time Piece",) * max(TEST_CHAPTER_TIMEPIECE_COSTS[ChapterIndex.ALPINE], TEST_CHAPTER_TIMEPIECE_COSTS[ChapterIndex.CRUISE]),
        ], EnableDLC1=True),
    ],
    "Nyakuza Metro": [
        *always_on_difficulties("Spaceship", [
            (
                "Dweller Mask",
                "Ice Hat",
                *(["Time Piece"] * max(TEST_CHAPTER_TIMEPIECE_COSTS[ChapterIndex.ALPINE], TEST_CHAPTER_TIMEPIECE_COSTS[ChapterIndex.METRO]))
             )
        ], EnableDLC2=True),
    ],

    # Chapter 3 - Subcon Forest
    "Subcon Forest Area": [
        *always_on_difficulties(MAIN_SUBCON_ACTS),
        # Expert can cherry hover from YCHE to the Subcon Forest Area.
        always("Your Contract has Expired", LogicDifficulty="expert", NoPaintingSkips=False),
        # Without painting skips, it is not possible to go from the Boss Arena to the Subcon Forest Area because the
        # paintings are on the other side of the boss firewall.
        *never_on_difficulties("Your Contract has Expired"),
    ],
    "Your Contract has Expired - Post Fight": [
        # The entrance from YCHE must never have any requirements because its logic is not inherited by act connections.
        *always_on_difficulties("Your Contract has Expired"),
        # Snatcher Hover.
        always(MAIN_SUBCON_ACTS, LogicDifficulty="expert"),
    ],

    "Alpine Skyline Area (TIHS)": [
        *always_on_difficulties("Alpine Free Roam", [("Umbrella", "Hookshot Badge")]),
        *always_on_difficulties("Alpine Free Roam", "Hookshot Badge", UmbrellaLogic=False),
        *always_on_difficulties("The Illness has Spread"),
    ],
    "The Birdhouse": [
        always("Alpine Skyline Area", [("Hookshot Badge", "Brewing Hat", "Zipline Unlock - The Birdhouse Path")]),
        *always_on_difficulties("Alpine Skyline Area", [("Hookshot Badge", "Zipline Unlock - The Birdhouse Path")], min_difficulty="moderate"),
        always("Alpine Skyline Area", [("Hookshot Badge", "Brewing Hat")], ShuffleAlpineZiplines=False),
        *always_on_difficulties("Alpine Skyline Area", "Hookshot Badge", min_difficulty="moderate", ShuffleAlpineZiplines=False),
        *never_on_difficulties("The Illness has Spread"),
    ],
    "The Lava Cake": [
        *always_on_difficulties("Alpine Skyline Area", [("Hookshot Badge", "Zipline Unlock - The Lava Cake Path")]),
        *always_on_difficulties("Alpine Skyline Area", "Hookshot Badge", ShuffleAlpineZiplines=False),
        *never_on_difficulties("The Illness has Spread"),
    ],
    "The Windmill": [
        *always_on_difficulties("Alpine Skyline Area", [("Hookshot Badge", "Zipline Unlock - The Windmill Path")]),
        *always_on_difficulties("Alpine Skyline Area", "Hookshot Badge", ShuffleAlpineZiplines=False),
        *never_on_difficulties("The Illness has Spread"),
    ],
    "The Twilight Bell": [
        *always_on_difficulties("Alpine Skyline Area", [("Hookshot Badge", "Dweller Mask", "Zipline Unlock - The Twilight Bell Path")], max_difficulty="hard"),
        *always_on_difficulties("Alpine Skyline Area", [("Hookshot Badge", "Dweller Mask")], max_difficulty="hard", ShuffleAlpineZiplines=False),
        always("Alpine Skyline Area", [("Hookshot Badge", "Zipline Unlock - The Twilight Bell Path")], LogicDifficulty="expert"),
        always("Alpine Skyline Area", "Hookshot Badge", LogicDifficulty="expert", ShuffleAlpineZiplines=False),
        *never_on_difficulties("The Illness has Spread"),
    ],

    # Chapter 6 - The Arctic Cruise
    "Cruise Ship": add_options(EnableDLC1=True, to=[
        *always_on_difficulties("Bon Voyage!", "Hookshot Badge"),
        *always_on_difficulties(["Ship Shape", "Rock the Boat"]),
    ]),

    # Other
    "Badge Seller": [
        # todo: Also accessible from some Death Wish contracts, e.g. Collect-a-thon, though this is rather obscure
        #  knowledge.
        *always_on_difficulties([
            *MAFIA_TOWN_ACTS,
            "Dead Bird Studio",
            "Picture Perfect",
            "Train Rush",
            *MAIN_SUBCON_ACTS,
            "The Illness has Spread",
            "Ship Shape",
            "Rock the Boat",
        ], EnableDLC1=True),
        *always_on_difficulties("Bon Voyage!", "Hookshot Badge", EnableDLC1=True),
        *always_on_difficulties("Alpine Free Roam", [("Hookshot Badge", "Umbrella")]),
        *always_on_difficulties("Alpine Free Roam", "Hookshot Badge", UmbrellaLogic=False),
        # Needs painting skips because the boss firewall cannot be removed from the YCHE side.
        always("Your Contract has Expired", LogicDifficulty="expert", NoPaintingSkips=False),
        *never_on_difficulties("Your Contract has Expired", NoPaintingSkips=True),
    ],
}

DLC2_REGION_TEST_DATA: TestData = add_options(EnableDLC2=True, to={
    # Chapter 7 - Nyakuza Metro
    "Yellow Overpass Station": [
        *always_on_difficulties("Nyakuza Free Roam")
    ],
    "Green Clean Station": [
        *always_on_difficulties("Nyakuza Free Roam")
    ],
    "Pink Paw Station": [
        *always_on_difficulties("Nyakuza Free Roam", [
            "Metro Ticket - Pink",
            ("Metro Ticket - Yellow", "Metro Ticket - Blue"),
        ]),
        # Wrongwarp from Yellow Overpass Station into Pink Paw Station.
        *always_on_difficulties("Nyakuza Free Roam", min_difficulty="moderate", NoTicketSkips=False),
    ],
    "Bluefin Tunnel": [
        *always_on_difficulties("Nyakuza Free Roam", ["Metro Ticket - Green", "Metro Ticket - Blue"]),
        # Ticket skips require Moderate logic, so tickets are still required with Normal logic.
        always("Nyakuza Free Roam", ["Metro Ticket - Green", "Metro Ticket - Blue"], NoTicketSkips=False),
        # Dive under the kill plane/box from the entrance to Yellow Overpass Station.
        *always_on_difficulties("Nyakuza Free Roam", min_difficulty="moderate", NoTicketSkips=False),
    ],
})

# Separated from region tests because these regions can be shuffled when act randomization is enabled.
RANDOMIZED_REGION_TEST_DATA: TestData = {
    "Time Rift - Gallery": [
        *always_on_difficulties("Spaceship", [("Brewing Hat", *TEST_CHAPTER_TIMEPIECES[ChapterIndex.BIRDS])]),
    ],
    "Time Rift - The Lab": [
        *always_on_difficulties("Spaceship", [("Dweller Mask", *TEST_CHAPTER_TIMEPIECES[ChapterIndex.ALPINE])]),
    ],
    "Time Rift - Sewers": [
        *always_on_difficulties(MAFIA_TOWN_ACTS, None, "Mafia Town - Act 4"),
    ],
    "Time Rift - Bazaar": [
        *always_on_difficulties(MAFIA_TOWN_ACTS, None, "Mafia Town - Act 6"),
    ],
    "Time Rift - Mafia of Cooks": [
        *always_on_difficulties(MAFIA_TOWN_ACTS - {"Heating Up Mafia Town"}, [Items.relic_groups["Burger"]]),
        *never_on_difficulties("Heating Up Mafia Town"),
    ],
    "Time Rift - The Owl Express": [
        *always_on_difficulties("Murder on the Owl Express", None, ["Battle of the Birds - Act 2", "Battle of the Birds - Act 3"]),
    ],
    "Time Rift - The Moon": [
        *always_on_difficulties(["Picture Perfect", "The Big Parade"], None, ["Battle of the Birds - Act 4", "Battle of the Birds - Act 5"]),
    ],
    "Time Rift - Dead Bird Studio": [
        *always_on_difficulties(["Dead Bird Studio", "Dead Bird Studio Basement"], [Items.relic_groups["Train"]]),
    ],
    "Time Rift - Pipe": [
        *always_on_difficulties(MAIN_SUBCON_ACTS, [("Progressive Painting Unlock", "Progressive Painting Unlock")], "Subcon Forest - Act 2"),
        *always_on_difficulties(MAIN_SUBCON_ACTS, None, "Subcon Forest - Act 2", min_difficulty="moderate", NoPaintingSkips=False),
        always("Your Contract has Expired", None, "Subcon Forest - Act 2", LogicDifficulty="expert", NoPaintingSkips=False),
    ],
    "Time Rift - Village": [
        *always_on_difficulties(MAIN_SUBCON_ACTS, [("Progressive Painting Unlock", "Progressive Painting Unlock")], "Subcon Forest - Act 4"),
        *always_on_difficulties(MAIN_SUBCON_ACTS, None, "Subcon Forest - Act 4", min_difficulty="moderate", NoPaintingSkips=False),
        always("Your Contract has Expired", None, "Subcon Forest - Act 4", LogicDifficulty="expert", NoPaintingSkips=False),
    ],
    "Time Rift - Sleepy Subcon": [
        *always_on_difficulties(MAIN_SUBCON_ACTS, [(
            "Progressive Painting Unlock",
            "Progressive Painting Unlock",
            "Progressive Painting Unlock",
            *Items.relic_groups["UFO"],
        )]),
        *always_on_difficulties(MAIN_SUBCON_ACTS, [Items.relic_groups["UFO"]], min_difficulty="moderate", NoPaintingSkips=False),
        always("Your Contract has Expired", [Items.relic_groups["UFO"]], LogicDifficulty="expert", NoPaintingSkips=False),
    ],
    # Access to the time rift is unlocked by completing The Windmill.
    "Time Rift - Curly Tail Trail": [
        *always_on_difficulties("Alpine Free Roam", [("Hookshot Badge", "Umbrella", "Zipline Unlock - The Windmill Path")]),
        *always_on_difficulties("Alpine Free Roam", [("Hookshot Badge", "Zipline Unlock - The Windmill Path")], UmbrellaLogic=False),
        *always_on_difficulties("Alpine Free Roam", [("Hookshot Badge", "Umbrella")], ShuffleAlpineZiplines=False),
        *always_on_difficulties("Alpine Free Roam", "Hookshot Badge", UmbrellaLogic=False, ShuffleAlpineZiplines=False),
        # The Time Rift - Alpine Skyline entrance could lead to Alpine Free Roam in insanity act randomizer and would be
        # accessible if all items were collected, so ensure it is not accessible by not collecting the Crayon Relics.
        # An alternative would be using the ActPlando option to make Time Rift - Alpine Skyline vanilla or some other
        # dead-end act that is not Alpine Free Roam, but this is slower for testing purposes because each unique
        # combination of options requires a new test world to be created.
        *never_on_difficulties("The Illness has Spread", collect_all_but_items=[Items.relic_groups["Crayon"]]),
    ],
    # Access to the time rift is unlocked by completing The Twilight Bell.
    # The tests for "-> The Twilight Bell" and "Act Completion (The Twilight Bell)" go over more of the combinations of
    # conditions that can reach the Act Completion.
    "Time Rift - The Twilight Bell": [
        # Copied from the "Act Completion (The Twilight Bell)" test:
        *add_options(UmbrellaLogic=False, ShuffleAlpineZiplines=False, to=[
            *always_on_difficulties("Alpine Free Roam", [("Hookshot Badge", "Dweller Mask")], max_difficulty="moderate"),
            always("Alpine Free Roam", [("Hookshot Badge", "Dweller Mask")], LogicDifficulty="hard"),
            always("Alpine Free Roam", [
                ("Hookshot Badge", "Brewing Hat"),
                ("Hookshot Badge", "Dweller Mask"),
                ("Hookshot Badge", "Sprint Hat"),
                # The Time Stop Hat + Umbrella option still requires Umbrella with Umbrella logic not enabled.
                ("Hookshot Badge", "Umbrella", "Time Stop Hat"),
            ], LogicDifficulty="expert"),
        ]),
        *never_on_difficulties("Alpine Free Roam", ["Zipline Unlock - The Twilight Bell Path", "Umbrella"]),
        *never_on_difficulties("Alpine Free Roam", "Zipline Unlock - The Twilight Bell Path", UmbrellaLogic=False),
        *never_on_difficulties("Alpine Free Roam", "Umbrella", ShuffleAlpineZiplines=False),
        # Prevent access to the Time Rift - Alpine Skyline entrance like the test for Time Rift - Curly Tail Trail.
        *never_on_difficulties("The Illness has Spread", collect_all_but_items=[Items.relic_groups["Crayon"]]),
    ],
    # The entrance to this Purple Time Rift was previously missing the Hookshot Badge and Umbrella (with umbrella logic)
    # requirements when accessed from Alpine Free Roam.
    "Time Rift - Alpine Skyline": [
        *always_on_difficulties("Alpine Free Roam", [("Umbrella", "Hookshot Badge", *Items.relic_groups["Crayon"])]),
        *always_on_difficulties("Alpine Free Roam", [("Hookshot Badge", *Items.relic_groups["Crayon"])], UmbrellaLogic=False),
        *always_on_difficulties("The Illness has Spread", [Items.relic_groups["Crayon"]]),
    ],
    "Time Rift - Balcony": add_options(EnableDLC1=True, to=[
        *always_on_difficulties("Cruise Ship", None, "The Arctic Cruise - Finale"),
        # The Time Rift - Deep Sea entrance could lead to Ship Shape or Rock the Boat in insanity act randomizer.
        # Because this test is an 'always' test, its items are expected to always be required, so the test would fail if
        # it was made to always require the Cake relics, so Time Rift - Deep Sea is ActPlando-ed to be vanilla instead.
        *always_on_difficulties("Bon Voyage!", "Hookshot Badge", "The Arctic Cruise - Finale",
                                _InsanityActPlando=hashable_vanilla_act_plando("Time Rift - Deep Sea")),
        *always_on_difficulties(["Ship Shape", "Rock the Boat"], None, "The Arctic Cruise - Finale"),
    ]),
    "Time Rift - Deep Sea": add_options(EnableDLC1=True, to=[
        *always_on_difficulties("Bon Voyage!", [Items.relic_groups["Cake"]]),
        *never_on_difficulties(["Ship Shape", "Rock the Boat"]),
    ]),
    "Time Rift - Rumbi Factory": add_options(EnableDLC2=True, to=[
        *always_on_difficulties("Nyakuza Free Roam", [Items.relic_groups["Necklace"]]),
        *never_on_difficulties("Rush Hour"),
    ]),
}

ALL_TESTS: List[Tuple[SpotType, TestData]] = [
    ("Location", LOCATION_TEST_DATA),
    ("Location", DLC1_LOCATION_TEST_DATA),
    ("Location", DLC2_LOCATION_TEST_DATA),
    ("Location", DEATH_WISH_LOCATION_TEST_DATA),
    ("Entrance", ENTRANCE_TEST_DATA),
    ("Region", REGION_TEST_DATA),
    ("Region", DLC2_REGION_TEST_DATA),
    ("RandomizedRegion", RANDOMIZED_REGION_TEST_DATA),
]
