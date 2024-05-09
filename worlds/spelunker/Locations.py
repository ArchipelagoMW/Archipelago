from typing import List, Optional, NamedTuple, TYPE_CHECKING

from .Options import HiddenLocs
from worlds.generic.Rules import CollectionRule

if TYPE_CHECKING:
    from . import SpelunkerWorld


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    rule: CollectionRule = lambda state: True


def get_locations(world: Optional["SpelunkerWorld"]) -> List[LocationData]:

    location_table: List[LocationData] = [
        LocationData("Area 1", "1F - First Item", 0x696969),
        LocationData("Area 1", "1F - Pit Item", 0x69696A),
        LocationData("Area 1", "1F - Right Item 1", 0x69696B),
        LocationData("Area 1", "1F - Between Mounds", 0x69696C),
        LocationData("Area 1", "1F - Far Wall 1", 0x69696D),
        LocationData("Area 1", "1F - Far Wall 2", 0x69696E),

        LocationData("Area 1", "B1F - Elevator Item", 0x69696F),
        LocationData("Area 1", "B1F - Undulating Rocks", 0x696970),
        LocationData("Area 1", "B1F - Past Boulder", 0x696971),
        LocationData("Area 1", "B1F - Side Shaft Ledge", 0x696972),
        LocationData("Area 1", "B1F - Side Shaft Mound", 0x696973),
        LocationData("Area 1", "B1F - Side Shaft Bottom Left", 0x696974),
        LocationData("Area 1", "B1F - Side Shaft Bottom Right", 0x696975),
        LocationData("Area 1", "B1F - Side Shaft Ladder Right", 0x6969F8),

        LocationData("Area 1", "B2F - First Item", 0x696976),
        LocationData("Area 1", "B2F - Second Item", 0x696977),

        LocationData("Area 1", "B3F - Mound Item", 0x696978),
        LocationData("Area 1", "B3F - Ramp Item", 0x696979),
        LocationData("Area 1", "B3F - Ledge Item", 0x69697A),
        LocationData("Area 1", "B3F - Upper Nook 1", 0x69697B),
        LocationData("Area 1", "B3F - Upper Nook 2", 0x69697C),
        LocationData("Area 1", "B3F - Upper Nook 3", 0x69697D),
        LocationData("Area 1", "B3F - Middle Ledge", 0x69697E),
        LocationData("Area 1", "B3F - Bottom", 0x69697F),
        LocationData("Area 1", "B3F - Bat Item", 0x696980),
        LocationData("Area 1", "B3F - Ladder Left", 0x696981),
        LocationData("Area 1", "B3F - Bombable Wall", 0x696982),

        LocationData("Area 1", "B4F - Top Item", 0x696983),
        LocationData("Area 1", "B4F - Minecart 1", 0x696984),
        LocationData("Area 1", "B4F - Minecart 2", 0x696985),

        LocationData("Area 1", "B5F - Near Ramp", 0x696986),
        LocationData("Area 1", "B5F - Ladder Left", 0x696987),
        LocationData("Area 1", "B5F - Ladder Right", 0x696988),

        LocationData("Area 1", "B6F - Item", 0x696989),

        LocationData("Area 2", "B7F - Left of Elevators", 0x69698A),

        LocationData("Area 2", "B8F - Right Side 1", 0x69698B),
        LocationData("Area 2", "B8F - Right Side 2", 0x69698C),
        LocationData("Area 2", "B8F - Rope 1", 0x69698D),
        LocationData("Area 2", "B8F - Rope 2", 0x69698E),
        LocationData("Area 2", "B8F - Boulder Pit 1", 0x69698F),
        LocationData("Area 2", "B8F - Boulder Pit 2", 0x696990),

        LocationData("Area 2", "B9F - Right Item", 0x696991),
        LocationData("Area 2", "B9F - Left Top of Ramp", 0x696992),
        LocationData("Area 2", "B9F - Left Mounds", 0x696993),
        LocationData("Area 2", "B9F - Left Near Edge", 0x696994),

        LocationData("Area 2", "B10F - Far Ropes Ledge", 0x696995),
        LocationData("Area 2", "B10F - First Bridge", 0x6969F9),
        LocationData("Area 2", "B10F - Between Bridges", 0x696996),
        LocationData("Area 2", "B10F - After Bridges", 0x696997),
        LocationData("Area 2", "B10F - Ladder Item", 0x696998),
        LocationData("Area 2", "B10F - Rope Item", 0x696999),
        LocationData("Area 2", "B10F - Solo Rope", 0x69699A),
        LocationData("Area 2", "B10F - Platform Item", 0x69699B),
        LocationData("Area 2", "B10F - Left Shaft", 0x69699C),

        LocationData("Area 2", "B11F - Boulder Pit", 0x69699D),
        LocationData("Area 2", "B11F - Bombable Wall", 0x69699E),
        LocationData("Area 2", "B11F - Left Shaft", 0x69699F),

        LocationData("Area 2", "B12F - Pit Item 1", 0x6969A0),
        LocationData("Area 2", "B12F - Pit Item 2", 0x6969A1),
        LocationData("Area 2", "B12F - Pit Item 3", 0x6969A2),
        LocationData("Area 2", "B12F - Locked Item", 0x6969A3),

        LocationData("Area 2", "B13F - Item", 0x6969A4),

        LocationData("Area 3", "B14F - Near Ladder", 0x6969FA),
        LocationData("Area 3", "B14F - Disconnected Platform", 0x6969A5),
        LocationData("Area 3", "B14F - Rope Item", 0x6969A6),
        LocationData("Area 3", "B14F - Boulder Item", 0x6969A7),
        LocationData("Area 3", "B14F - Far Ledge", 0x6969A8),

        LocationData("Area 3", "B15F - Left Wall", 0x6969A9),
        LocationData("Area 3", "B15F - Past Boulder", 0x6969AA),
        LocationData("Area 3", "B15F - Upper Ledge", 0x6969AB),
        LocationData("Area 3", "B15F - Three in a Row 1", 0x6969AC),
        LocationData("Area 3", "B15F - Three in a Row 2", 0x6969AD),
        LocationData("Area 3", "B15F - Three in a Row 3", 0x6969AE),
        LocationData("Area 3", "B15F - Right Wall", 0x6969AF),

        LocationData("Area 3", "B16F - Undulating Rocks", 0x6969B0),
        LocationData("Area 3", "B16F - Top of Waterfall", 0x6969B1),
        LocationData("Area 3", "B16F - Below Waterfall", 0x6969B2),
        LocationData("Area 3", "B16F - Bat 1", 0x6969B3),
        LocationData("Area 3", "B16F - Bat 2", 0x6969B4),

        LocationData("Area 3", "B17F - Item", 0x6969b5),

        LocationData("Area 3", "B18F - Before Pit", 0x6969B6),
        LocationData("Area 3", "B18F - Trap Item", 0x6969B7),

        LocationData("Area 3", "B19F - Long Rope Bottom", 0x6969B8),
        LocationData("Area 3", "B19F - Near Ladder", 0x6969B9),
        LocationData("Area 3", "B19F - Past Boulder", 0x6969BA),

        LocationData("Area 3", "B20F - Near Ladder", 0x6969BB),
        LocationData("Area 3", "B20F - Boulder 1", 0x6969BC),
        LocationData("Area 3", "B20F - Boulder 2", 0x6969BD),
        LocationData("Area 3", "B20F - Boulder 3", 0x6969BF),
        LocationData("Area 3", "B20F - Right Side Bombable Wall", 0x6969C0),
        LocationData("Area 3", "B20F - Water Spout Upper 1", 0x6969C1),
        LocationData("Area 3", "B20F - Water Spout Upper Trap", 0x6969C2),
        LocationData("Area 3", "B20F - Water Spout Lonely Ledge", 0x6969C3),
        LocationData("Area 3", "B20F - Water Spout Middle Left Ledge", 0x6969C4),
        LocationData("Area 3", "B20F - Water Spout Middle Left Rope", 0x6969C5),
        LocationData("Area 3", "B20F - Water Spout Middle Right Ledge", 0x6969C6),
        LocationData("Area 3", "B20F - Near Right Rope", 0x6969C7),

        LocationData("Area 3", "B21F - Bat Pit 1", 0x6969C8),
        LocationData("Area 3", "B21F - Bat Pit 2", 0x6969C9),
        LocationData("Area 3", "B21F - Bat Pit 3", 0x6969CA),
        LocationData("Area 3", "B21F - Ladder Right", 0x6969CB),
        LocationData("Area 3", "B21F - Ladder Left", 0x6969CC),

        LocationData("Area 4", "B22F - Lonely Platform", 0x6969CD),
        
        LocationData("Area 4", "B23F - Pyramid Platforming", 0x6969D0),
        LocationData("Area 4", "B23F - Long Way Around", 0x6969D1),
        LocationData("Area 4", "B23F - Left Wall Near Pyramid", 0x6969FC),
        LocationData("Area 4", "B23F - Middle Pyramid Jump", 0x6969D2),
        LocationData("Area 4", "B23F - Pyramid Bombable Wall", 0x6969D3),
        LocationData("Area 4", "B23F - Offcenter T", 0x6969D4),
        LocationData("Area 4", "B23F - Lonely Platform Before Door", 0x6969FB),
        LocationData("Area 4", "B23F - Just After Door", 0x6969D5),
        LocationData("Area 4", "B23F - Ropes Right Wall", 0x6969D6),

        LocationData("Area 4", "B24F - Left Side Item", 0x6969D7),
        LocationData("Area 4", "B24F - Right Side Item", 0x6969D8),
        LocationData("Area 4", "B24F - Pit Trap", 0x6969D9),

        LocationData("Area 4", "B25F - Left 1", 0x6969DA),
        LocationData("Area 4", "B25F - Left 2", 0x6969DB),
        LocationData("Area 4", "B25F - Right 1", 0x6969DC),
        LocationData("Area 4", "B25F - Right 2", 0x6969DD),
        LocationData("Area 4", "B25F - Ropes Item", 0x6969DE),

        LocationData("Area 4", "B26F - Rope Right 1", 0x6969DF),
        LocationData("Area 4", "B26F - Rope Right 2", 0x6969E0),
        LocationData("Area 4", "B26F - So Close You Can Smell It Item", 0x6969E1),

        LocationData("Area 4", "B27F - Right of Pit 1", 0x6969E2),
        LocationData("Area 4", "B27F - Right of Pit 2", 0x6969E3),
        LocationData("Area 4", "B27F - Entry Item", 0x6969E4),

        LocationData("Area 4", "B28F - Boulder Item", 0x6969E5),
        LocationData("Area 4", "B28F - Bat Ledge", 0x6969E6),
        LocationData("Area 4", "B28F - Locked Item 1", 0x6969E7),
        LocationData("Area 4", "B28F - Locked Item 2", 0x6969E8),

        LocationData("Area 4", "B28F - Final Boulder", 0x6969E9),
        LocationData("Area 4", "B28F - Final Rope Left", 0x6969EA),
        LocationData("Area 4", "B28F - Final Rope Right", 0x6969EB),

        LocationData("Area 4", "B29F - Ladder Ledge", 0x6969EC),
        LocationData("Area 4", "B29F - Pit Trap", 0x6969ED),
        LocationData("Area 4", "B29F - Before Pit Trap", 0x6969EE),
        LocationData("Area 4", "B29F - Rope Alcove", 0x6969EF),
        LocationData("Area 4", "B29F - Left Wall Rope Ledge", 0x6969F0),
        LocationData("Area 4", "B29F - Left Pit Item", 0x6969F1),
        LocationData("Area 4", "B29F - Bombable Wall", 0x6969F2),
        LocationData("Area 4", "B29F - Left Wall Item", 0x6969F3),

        LocationData("Area 4", "B30F - Far Bottom Right", 0x6969F4),
        LocationData("Area 4", "B30F - Undulating Rocks", 0x6969F5),
        LocationData("Area 4", "B30F - Mound Item", 0x6969F6),
        LocationData("Area 4", "B30F - Far Bottom Left", 0x6969F7),

        LocationData("Area 4", "Golden Pyramid", None)
    ]

    if not world or world.options.hidden_items:
        location_table += [
            LocationData("Area 1", "B1F - Hidden Item before Boulder", 0x6969FD),
            LocationData("Area 1", "B1F - Side Shaft Hidden Item", 0x6969FE),
            LocationData("Area 2", "B8F - Boulder Pit Hidden Item", 0x6969FF),
            LocationData("Area 2", "B10F - Bridge Hidden Item", 0x696A00),
            LocationData("Area 3", "B16F - Blue Door Hidden Item", 0x696A01),
            LocationData("Area 3", "B20F - Water Spout Upper Ledge Hidden Item", 0x696A02),
            LocationData("Area 4", "B23F - Pyramid Hidden Item", 0x696A03),
            LocationData("Area 4", "B24F - Pit Trap Hidden Item", 0x696A04),
        ]

    return location_table
