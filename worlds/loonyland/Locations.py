from enum import Enum
from typing import NamedTuple, Dict

from BaseClasses import Location


loonyland_base_id: int = 2876900


class LoonylandLocation(Location):
    game = "Loonyland"
    
class LocationCategory(Enum):
    PICKUP = 0
    QUEST = 1
    BADGE = 2
    EVENT = 4
    
class LoonylandLocationData(NamedTuple):
    id: int
    category: LocationCategory
    region: str
    
loonyland_location_table: Dict[str, LoonylandLocationData] = {
    "Swamp: Mud Path": LoonylandLocationData(0, LocationCategory.PICKUP, "Slurpy Swamp Mud"),
    "Swamp: Bog Beast": LoonylandLocationData(1, LocationCategory.PICKUP, "Halloween Hill"),
    "Rocky Cliffs: Upper Ledge":     LoonylandLocationData(2, LocationCategory.PICKUP, "Rocky Cliffs"),
    "Swamp: Sapling Shrine":     LoonylandLocationData(3, LocationCategory.PICKUP, "Slurpy Swamp Mud"),
    "Terror Glade: South Trees":     LoonylandLocationData(4, LocationCategory.PICKUP, "Halloween Hill"),
    "Rocky Cliffs: Vine":     LoonylandLocationData(5, LocationCategory.PICKUP, "Rocky Cliffs"),
    "Rocky Cliffs: Grand Pharoh":     LoonylandLocationData(6, LocationCategory.PICKUP, "Rocky Cliffs"),
    "Rocky Cliffs: Rock Corner":     LoonylandLocationData(7, LocationCategory.PICKUP, "Rocky Cliffs"),
    "Swamp: Outside Luniton":     LoonylandLocationData(8, LocationCategory.PICKUP, "Halloween Hill"),
    "Swamp: East 1":     LoonylandLocationData(9, LocationCategory.PICKUP, "Halloween Hill"),
    "Swamp: Top Left dry":   LoonylandLocationData(10, LocationCategory.PICKUP, "Halloween Hill"),
    "Swamp: East 2":     LoonylandLocationData(11, LocationCategory.PICKUP, "Halloween Hill"),
    "Woods: Above Castle":     LoonylandLocationData(12, LocationCategory.PICKUP, "Halloween Hill"),
    "Rocky Cliffs: Entrance Ledge":     LoonylandLocationData(13, LocationCategory.PICKUP, "Rocky Cliffs"),
    "Rocky Cliffs: Peak":     LoonylandLocationData(14, LocationCategory.PICKUP, "Rocky Cliffs"),
    "Woods: SW of Cabin":     LoonylandLocationData(15, LocationCategory.PICKUP, "Halloween Hill"),
    "Witch's Cabin: Bedroom":     LoonylandLocationData(16, LocationCategory.PICKUP, "The Witch's Cabin Front"),
    "Witch's Cabin: Backroom":     LoonylandLocationData(17, LocationCategory.PICKUP, "The Witch's Cabin Back"),
    "Bonita's Cabin: Barrel Maze":     LoonylandLocationData(18, LocationCategory.PICKUP, "Bonita's Cabin"),
    "Bog Pit: Top Door":     LoonylandLocationData(19, LocationCategory.PICKUP, "The Bog Pit"),
    "Bog Pit: Posts Room":     LoonylandLocationData(20, LocationCategory.PICKUP, "The Bog Pit"),
    "Bog Pit: Drippy Window":     LoonylandLocationData(21, LocationCategory.PICKUP, "The Bog Pit"),
    "Bog Pit: Green room":     LoonylandLocationData(22, LocationCategory.PICKUP, "The Bog Pit"),
    "Bog Pit: Arena":     LoonylandLocationData(23, LocationCategory.PICKUP, "The Bog Pit"),
    "Bog Pit: Sw Switch":     LoonylandLocationData(24, LocationCategory.PICKUP, "The Bog Pit"),
    "Tunnel: Swampdog Pumpkin Door":     LoonylandLocationData(25, LocationCategory.PICKUP, "Underground Tunnel Top"),
    "Tunnel: Scratch Wall":     LoonylandLocationData(26, LocationCategory.PICKUP, "Underground Tunnel Top"),
    "Tunnel: Narrow Passage":     LoonylandLocationData(27, LocationCategory.PICKUP, "Underground Tunnel Top"),
    "Tunnel: Top Frogs":     LoonylandLocationData(28, LocationCategory.PICKUP, "Underground Tunnel Top"),
    "Tunnel: Torch Island":     LoonylandLocationData(29, LocationCategory.PICKUP, "Underground Tunnel Mud"),
    "Tunnel: Small Room":     LoonylandLocationData(30, LocationCategory.PICKUP, "Underground Tunnel Top"),
    "Swamp Gas: Scratch Wall":     LoonylandLocationData(31, LocationCategory.PICKUP, "Swamp Gas Cavern Front"),
    "Swamp Gas: Bat Door":     LoonylandLocationData(32, LocationCategory.PICKUP, "Swamp Gas Cavern Front"),
    "Swamp Gas: Stair room":     LoonylandLocationData(33, LocationCategory.PICKUP, "Swamp Gas Cavern Back"),
    "Swamp Gas: Rock Prison":     LoonylandLocationData(34, LocationCategory.PICKUP, "Swamp Gas Cavern Front"),
    "A Tiny Cabin":     LoonylandLocationData(35, LocationCategory.PICKUP, "A Tiny Cabin"),
    "Seer: Bedside":     LoonylandLocationData(36, LocationCategory.PICKUP, "A Cabin Seer"),
    "Dusty Crypt: Pumpkin Door":     LoonylandLocationData(37, LocationCategory.PICKUP, "Dusty Crypt"),
    "Dusty Crypt: Maze":     LoonylandLocationData(38, LocationCategory.PICKUP, "Dusty Crypt"),
    "Musty Crypt: Maze Room":     LoonylandLocationData(39, LocationCategory.PICKUP, "Musty Crypt"),
    "Rusty Crypt: Vine":     LoonylandLocationData(40, LocationCategory.PICKUP, "Rusty Crypt"),
    "Rusty Crypt: Boulders":     LoonylandLocationData(41, LocationCategory.PICKUP, "Rusty Crypt"),
    "A Messy Cabin":     LoonylandLocationData(42, LocationCategory.PICKUP, "A Messy Cabin"),
    "Under The Lake: Behind Lightning Rod":     LoonylandLocationData(43, LocationCategory.PICKUP, "Under The Lake"),
    "Under The Lake: Bat Door":     LoonylandLocationData(44, LocationCategory.PICKUP, "Under The Lake"),
    "Deeper Lake: Corner":     LoonylandLocationData(45, LocationCategory.PICKUP, "Deeper Under The Lake"),
    "Deeper Lake: Rhombus":     LoonylandLocationData(46, LocationCategory.PICKUP, "Deeper Under The Lake"),
    "Frankenjulie's Reward":     LoonylandLocationData(47, LocationCategory.PICKUP, "Frankenjulie's Laboratory"),
    "Tower: Barracks":     LoonylandLocationData(48, LocationCategory.PICKUP, "Haunted Tower"),
    "Tower F2: Skull Puzzle":     LoonylandLocationData(49, LocationCategory.PICKUP, "Haunted Tower, Floor 2"),
    "PolterGuy's Reward":     LoonylandLocationData(50, LocationCategory.PICKUP, "Haunted Tower Roof"),
    "Tower Basement: DoorDoorDoorDoorDoorDoor":     LoonylandLocationData(51, LocationCategory.PICKUP, "Haunted Basement"),
    "Abandoned Mine: Shaft":     LoonylandLocationData(52, LocationCategory.PICKUP, "Abandoned Mines"),
    "Shrine of Bombulus: Prize":     LoonylandLocationData(53, LocationCategory.PICKUP, "The Shrine Of Bombulus"),
    "Gloomy Cavern: Lockpick":     LoonylandLocationData(54, LocationCategory.PICKUP, "A Gloomy Cavern"),
    "Happy Stick: Hidden":     LoonylandLocationData(55, LocationCategory.PICKUP, "Happy Stick Woods"),
    "Happy Stick: Reward":     LoonylandLocationData(56, LocationCategory.PICKUP, "Happy Stick Woods"),
    "Wolf Den: Top Left":     LoonylandLocationData(57, LocationCategory.PICKUP, "The Wolf Den"),
    "Wolf Den: Pumpkin Door":     LoonylandLocationData(58, LocationCategory.PICKUP, "The Wolf Den"),
    "Wolf Den: Vine":     LoonylandLocationData(59, LocationCategory.PICKUP, "The Wolf Den"),
    "Upper Cavern: Three Gold Skeletons":     LoonylandLocationData(60, LocationCategory.PICKUP, "Upper Creepy Caverns"),
    "Under The Ravine: Left Vine":     LoonylandLocationData(61, LocationCategory.PICKUP, "Under The Ravine"),
    "Under The Ravine: Right Vine":     LoonylandLocationData(62, LocationCategory.PICKUP, "Under The Ravine"),
    "Creepy Caverns M: Pharaoh Bat Door":     LoonylandLocationData(63, LocationCategory.PICKUP, "Creepy Caverns Middle"),
    "Creepy Caverns E: Top Pharaohs":     LoonylandLocationData(64, LocationCategory.PICKUP, "Creepy Caverns Right"),
    "Creepy Caverns M: Gargoyles":     LoonylandLocationData(65, LocationCategory.PICKUP, "Creepy Caverns Middle"),
    "Castle Vampy: Top Room":     LoonylandLocationData(66, LocationCategory.PICKUP, "Castle Vampy"),
    "Castle Vampy: Maze":     LoonylandLocationData(67, LocationCategory.PICKUP, "Castle Vampy"),
    "Castle Vampy: Gauntlet":     LoonylandLocationData(68, LocationCategory.PICKUP, "Castle Vampy"),
    "Castle Vampy: Bat Closet":     LoonylandLocationData(69, LocationCategory.PICKUP, "Castle Vampy"),
    "Castle Vampy II: Candle Room":     LoonylandLocationData(70, LocationCategory.PICKUP, "Castle Vampy II Main"),
    "Castle Vampy II: Bloodsucker Room":     LoonylandLocationData(71, LocationCategory.PICKUP, "Castle Vampy II Main"),
    "Castle Vampy II: Vampire Lord":     LoonylandLocationData(72, LocationCategory.PICKUP, "Castle Vampy II Main"),
    "Castle Vampy II: Bat Room":     LoonylandLocationData(73, LocationCategory.PICKUP, "Castle Vampy II Main"),
    "Cabin in the Woods: Gold Skull":     LoonylandLocationData(74, LocationCategory.PICKUP, "Cabin In The Woods"),
    "Castle Vampy III: Center":     LoonylandLocationData(75, LocationCategory.PICKUP, "Castle Vampy III Main"),
    "Castle Vampy III: Behind the Pews":     LoonylandLocationData(76, LocationCategory.PICKUP, "Castle Vampy III Main"),
    "Castle Vampy III: AMBUSH!":     LoonylandLocationData(77, LocationCategory.PICKUP, "Castle Vampy III Main"),
    "Castle Vampy III: Halloween":     LoonylandLocationData(78, LocationCategory.PICKUP, "Castle Vampy III Main"),
    "Castle Vampy III: Bat room":     LoonylandLocationData(79, LocationCategory.PICKUP, "Castle Vampy III Main"),
    "Castle Vampy IV: Right Path":     LoonylandLocationData(80, LocationCategory.PICKUP, "Castle Vampy IV Main"),
    "Castle Vampy IV: Left Path":     LoonylandLocationData(81, LocationCategory.PICKUP, "Castle Vampy IV Main"),
    "Castle Vampy IV: Ballroom Right":     LoonylandLocationData(82, LocationCategory.PICKUP, "Castle Vampy IV Main"),
    "Castle Vampy IV: Right Secret Wall":     LoonylandLocationData(83, LocationCategory.PICKUP, "Castle Vampy IV Main"),
    "Castle Vampy IV: Ballroom Left":     LoonylandLocationData(84, LocationCategory.PICKUP, "Castle Vampy IV Main"),
    "Roof NW: Gutsy the Elder":     LoonylandLocationData(85, LocationCategory.PICKUP, "Castle Vampy Roof NW"),
    "Roof NE: Stoney the Elder":     LoonylandLocationData(86, LocationCategory.PICKUP, "Castle Vampy Roof NE"),
    "Roof SW: Drippy the Elder":     LoonylandLocationData(87, LocationCategory.PICKUP, "Castle Vampy Roof SW"),
    "Roof SE: Toasty the Elder":     LoonylandLocationData(88, LocationCategory.PICKUP, "Castle Vampy Roof SE"),
    "Bonkula":     LoonylandLocationData(89, LocationCategory.PICKUP, "The Heart Of Terror"),
    "Hidey-Hole: Bat Door":     LoonylandLocationData(90, LocationCategory.PICKUP, "A Hidey-Hole"),
    "Hidey-Hole: Pebbles":     LoonylandLocationData(91, LocationCategory.PICKUP, "A Hidey-Hole"),
    "Swampdog Lair: Entrance":     LoonylandLocationData(92, LocationCategory.PICKUP, "Swampdog Lair"),
    "Swampdog Lair: End":     LoonylandLocationData(93, LocationCategory.PICKUP, "Swampdog Lair"),
    "Q: Save Halloween Hill":     LoonylandLocationData(94, LocationCategory.QUEST, "The Evilizer"),
    "Q: Ghostbusting":     LoonylandLocationData(95, LocationCategory.QUEST, "The Witch's Cabin Front"),
    "Q: Hairy Larry":     LoonylandLocationData(96, LocationCategory.QUEST, "A Cabin Larry"),
    "Q: Scaredy Cat":     LoonylandLocationData(97, LocationCategory.QUEST, "Halloween Hill"),
    "Q: Silver Bullet":     LoonylandLocationData(98, LocationCategory.QUEST, "Halloween Hill"),
    "Q: Smashing Pumpkins":     LoonylandLocationData(99, LocationCategory.QUEST, "Halloween Hill"),
    "Q: Sticky Shoes":     LoonylandLocationData(100, LocationCategory.QUEST, "Halloween Hill"),
    "Q: The Collection":     LoonylandLocationData(101, LocationCategory.QUEST, "A Cabin Collector"),
    "Q: The Rescue":     LoonylandLocationData(102, LocationCategory.QUEST, "A Gloomy Cavern"),
    "Q: Tree Trimming":     LoonylandLocationData(103, LocationCategory.QUEST, "A Cabin Trees"),
    "Q: Witch Mushrooms":     LoonylandLocationData(104, LocationCategory.QUEST, "The Witch's Cabin Front"),
    "Q: Zombie Stomp":     LoonylandLocationData(105, LocationCategory.QUEST, "Zombiton")
    #todo the 40 badge locations
    }