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
    "Swamp Mud Path": LoonylandLocationData(0, LocationCategory.PICKUP, "Slurpy Swamp Mud"),
    "Bog Beast Home": LoonylandLocationData(1, LocationCategory.PICKUP, "Halloween Hill"),
    "Rocky Cliffs below Upper Caverns":     LoonylandLocationData(2, LocationCategory.PICKUP, "Rocky Cliffs"),
    "Sapling Shrine":     LoonylandLocationData(3, LocationCategory.PICKUP, "Slurpy Swamp Mud"),
    "Terror Glade":     LoonylandLocationData(4, LocationCategory.PICKUP, "Halloween Hill"),
    "Rocky Cliffs Vine":     LoonylandLocationData(5, LocationCategory.PICKUP, "Halloween Hill"),
    "Rocky Cliffs Grand Pharoh":     LoonylandLocationData(6, LocationCategory.PICKUP, "Rocky Cliffs"),
    "Rocky Cliffs Rock Corner":     LoonylandLocationData(7, LocationCategory.PICKUP, "Rocky Cliffs"),
    "Mushroom outside town":     LoonylandLocationData(8, LocationCategory.PICKUP, "Halloween Hill"),
    "North of UG Passage":     LoonylandLocationData(9, LocationCategory.PICKUP, "Halloween Hill"),
    "Top left mushroom spot":   LoonylandLocationData(10, LocationCategory.PICKUP, "Halloween Hill"),
    "NE of UG Passage":     LoonylandLocationData(11, LocationCategory.PICKUP, "Halloween Hill"),
    "East Woods":     LoonylandLocationData(12, LocationCategory.PICKUP, "Halloween Hill"),
    "Rocky Cliffs Ledge":     LoonylandLocationData(13, LocationCategory.PICKUP, "Rocky Cliffs"),
    "Rocky Cliffs Peak":     LoonylandLocationData(14, LocationCategory.PICKUP, "Rocky Cliffs"),
    "Cat Tree":     LoonylandLocationData(15, LocationCategory.PICKUP, "Halloween Hill"),
    "Bedroom":     LoonylandLocationData(16, LocationCategory.PICKUP, "The Witch's Cabin Front"),
    "Backroom":     LoonylandLocationData(17, LocationCategory.PICKUP, "The Witch's Cabin Back"),
    "Barrel Maze":     LoonylandLocationData(18, LocationCategory.PICKUP, "Bonita's Cabin"),
    "Top Door":     LoonylandLocationData(19, LocationCategory.PICKUP, "The Bog Pit"),
    "Post Room":     LoonylandLocationData(20, LocationCategory.PICKUP, "The Bog Pit"),
    "Window Drip":     LoonylandLocationData(21, LocationCategory.PICKUP, "The Bog Pit"),
    "Green room":     LoonylandLocationData(22, LocationCategory.PICKUP, "The Bog Pit"),
    "Arena":     LoonylandLocationData(23, LocationCategory.PICKUP, "The Bog Pit"),
    "Kill Wall":     LoonylandLocationData(24, LocationCategory.PICKUP, "The Bog Pit"),
    "Swampdog Door":     LoonylandLocationData(25, LocationCategory.PICKUP, "Underground Tunnel Top"),
    "Scribble Wall":     LoonylandLocationData(26, LocationCategory.PICKUP, "Underground Tunnel Top"),
    "Tiny Passage":     LoonylandLocationData(27, LocationCategory.PICKUP, "Underground Tunnel Top"),
    "fire frogs":     LoonylandLocationData(28, LocationCategory.PICKUP, "Underground Tunnel Top"),
    "Torch Island":     LoonylandLocationData(29, LocationCategory.PICKUP, "Underground Tunnel Mud"),
    "Small Room":     LoonylandLocationData(30, LocationCategory.PICKUP, "Underground Tunnel Top"),
    "Scratch Wall":     LoonylandLocationData(31, LocationCategory.PICKUP, "Swamp Gas Cavern Front"),
    "Bat Mound":     LoonylandLocationData(32, LocationCategory.PICKUP, "Swamp Gas Cavern Front"),
    "Stair room":     LoonylandLocationData(33, LocationCategory.PICKUP, "Swamp Gas Cavern Back"),
    "Rock Prison":     LoonylandLocationData(34, LocationCategory.PICKUP, "Swamp Gas Cavern Front"),
    "Tiny Cabin":     LoonylandLocationData(35, LocationCategory.PICKUP, "A Tiny Cabin"),
    "Bedside ":     LoonylandLocationData(36, LocationCategory.PICKUP, "A Cabin Seer"),
    "Crypt Pumpkin Door":     LoonylandLocationData(37, LocationCategory.PICKUP, "Dusty Crypt"),
    "Maze":     LoonylandLocationData(38, LocationCategory.PICKUP, "Dusty Crypt"),
    "Big Closed Room":     LoonylandLocationData(39, LocationCategory.PICKUP, "Musty Crypt"),
    "Spike Vine":     LoonylandLocationData(40, LocationCategory.PICKUP, "Rusty Crypt"),
    "Boulders":     LoonylandLocationData(41, LocationCategory.PICKUP, "Rusty Crypt"),
    "Barrel Mess":     LoonylandLocationData(42, LocationCategory.PICKUP, "A Messy Cabin"),
    "Lightning Rod Secret":     LoonylandLocationData(43, LocationCategory.PICKUP, "Under The Lake"),
    "Lake Bat Door":     LoonylandLocationData(44, LocationCategory.PICKUP, "Under The Lake"),
    "SE corner":     LoonylandLocationData(45, LocationCategory.PICKUP, "Deeper Under The Lake"),
    "Rhombus":     LoonylandLocationData(46, LocationCategory.PICKUP, "Deeper Under The Lake"),
    "Frankenjulie's Reward":     LoonylandLocationData(47, LocationCategory.PICKUP, "Frankenjulie's Laboratory"),
    "Barracks":     LoonylandLocationData(48, LocationCategory.PICKUP, "Haunted Tower"),
    "Top Left":     LoonylandLocationData(49, LocationCategory.PICKUP, "Haunted Tower, Floor 2"),
    "Boss Reward":     LoonylandLocationData(50, LocationCategory.PICKUP, "Haunted Tower Roof"),
    "DoorDoorDoorDoorDoorDoor":     LoonylandLocationData(51, LocationCategory.PICKUP, "Haunted Basement"),
    "Shaft":     LoonylandLocationData(52, LocationCategory.PICKUP, "Abandoned Mines"),
    "Bombulus":     LoonylandLocationData(53, LocationCategory.PICKUP, "The Shrine Of Bombulus"),
    "Lockpick":     LoonylandLocationData(54, LocationCategory.PICKUP, "A Gloomy Cavern"),
    "Happy Stick Hidden":     LoonylandLocationData(55, LocationCategory.PICKUP, "Happy Stick Woods"),
    "Happy Stick Reward":     LoonylandLocationData(56, LocationCategory.PICKUP, "Happy Stick Woods"),
    "Wolf Top Left":     LoonylandLocationData(57, LocationCategory.PICKUP, "The Wolf Den"),
    "Pumpkin Door":     LoonylandLocationData(58, LocationCategory.PICKUP, "The Wolf Den"),
    "Grow Room":     LoonylandLocationData(59, LocationCategory.PICKUP, "The Wolf Den"),
    "The Three ombres":     LoonylandLocationData(60, LocationCategory.PICKUP, "Upper Creepy Caverns"),
    "Left Vine":     LoonylandLocationData(61, LocationCategory.PICKUP, "Under The Ravine"),
    "Right Vine":     LoonylandLocationData(62, LocationCategory.PICKUP, "Under The Ravine"),
    "M Pharoh bat Room":     LoonylandLocationData(63, LocationCategory.PICKUP, "Creepy Caverns Middle"),
    "E 2 blue Pharos":     LoonylandLocationData(64, LocationCategory.PICKUP, "Creepy Caverns Right"),
    "M GARGOYLE ROOM":     LoonylandLocationData(65, LocationCategory.PICKUP, "Creepy Caverns Middle"),
    "Vampire Guard":     LoonylandLocationData(66, LocationCategory.PICKUP, "Castle Vampy"),
    "maze top left":     LoonylandLocationData(67, LocationCategory.PICKUP, "Castle Vampy"),
    "Top Right Gauntlet":     LoonylandLocationData(68, LocationCategory.PICKUP, "Castle Vampy"),
    "Bat Closet":     LoonylandLocationData(69, LocationCategory.PICKUP, "Castle Vampy"),
    "Candle Room":     LoonylandLocationData(70, LocationCategory.PICKUP, "Castle Vampy II Main"),
    "Top Right Top":     LoonylandLocationData(71, LocationCategory.PICKUP, "Castle Vampy II Main"),
    "Bottom Right Middle":     LoonylandLocationData(72, LocationCategory.PICKUP, "Castle Vampy II Main"),
    "Bat room":     LoonylandLocationData(73, LocationCategory.PICKUP, "Castle Vampy II Main"),
    "Gold Skull":     LoonylandLocationData(74, LocationCategory.PICKUP, "Cabin In The Woods"),
    "Middle":     LoonylandLocationData(75, LocationCategory.PICKUP, "Castle Vampy III Main"),
    "Behind the Pews":     LoonylandLocationData(76, LocationCategory.PICKUP, "Castle Vampy III Main"),
    "AMBUSH!":     LoonylandLocationData(77, LocationCategory.PICKUP, "Castle Vampy III Main"),
    "Halloween":     LoonylandLocationData(78, LocationCategory.PICKUP, "Castle Vampy III Main"),
    "So many bats":     LoonylandLocationData(79, LocationCategory.PICKUP, "Castle Vampy III Main"),
    "Right Path":     LoonylandLocationData(80, LocationCategory.PICKUP, "Castle Vampy IV Main"),
    "Left Path":     LoonylandLocationData(81, LocationCategory.PICKUP, "Castle Vampy IV Main"),
    "Ballroom Right":     LoonylandLocationData(82, LocationCategory.PICKUP, "Castle Vampy IV Main"),
    "Right Secret Wall":     LoonylandLocationData(83, LocationCategory.PICKUP, "Castle Vampy IV Main"),
    "Ballroom Left":     LoonylandLocationData(84, LocationCategory.PICKUP, "Castle Vampy IV Main"),
    "Gutsy the Elder":     LoonylandLocationData(85, LocationCategory.PICKUP, "Castle Vampy Roof NW"),
    "Stoney the Elder":     LoonylandLocationData(86, LocationCategory.PICKUP, "Castle Vampy Roof NE"),
    "Drippy the Elder":     LoonylandLocationData(87, LocationCategory.PICKUP, "Castle Vampy Roof SW"),
    "Toasty the Elder":     LoonylandLocationData(88, LocationCategory.PICKUP, "Castle Vampy Roof SE"),
    "Bonkula":     LoonylandLocationData(89, LocationCategory.PICKUP, "The Heart Of Terror"),
    "Bat Door":     LoonylandLocationData(90, LocationCategory.PICKUP, "A Hidey-Hole"),
    "Pebbles":     LoonylandLocationData(91, LocationCategory.PICKUP, "A Hidey-Hole"),
    "Entrance":     LoonylandLocationData(92, LocationCategory.PICKUP, "Swampdog Lair"),
    "End":     LoonylandLocationData(93, LocationCategory.PICKUP, "Swampdog Lair"),
    "Save Halloween Hill":     LoonylandLocationData(94, LocationCategory.QUEST, "The Evilizer"),
    "Ghostbusting":     LoonylandLocationData(95, LocationCategory.QUEST, "The Witch's Cabin Front"),
    "Hairy Larry":     LoonylandLocationData(96, LocationCategory.QUEST, "A Cabin Larry"),
    "Scaredy Cat":     LoonylandLocationData(97, LocationCategory.QUEST, "Halloween Hill"),
    "Silver Bullet":     LoonylandLocationData(98, LocationCategory.QUEST, "Halloween Hill"),
    "Smashing Pumpkins":     LoonylandLocationData(99, LocationCategory.QUEST, "Halloween Hill"),
    "Sticky Shoes":     LoonylandLocationData(100, LocationCategory.QUEST, "Halloween Hill"),
    "The Collection":     LoonylandLocationData(101, LocationCategory.QUEST, "A Cabin Collector"),
    "The Rescue":     LoonylandLocationData(102, LocationCategory.QUEST, "A Gloomy Cavern"),
    "Tree Trimming":     LoonylandLocationData(103, LocationCategory.QUEST, "A Cabin Trees"),
    "Witch Mushrooms":     LoonylandLocationData(104, LocationCategory.QUEST, "The Witch's Cabin Front"),
    "Zombie Stomp":     LoonylandLocationData(105, LocationCategory.QUEST, "Halloween Hill")
    #todo the 40 badge locations
    }

loonyland_location_table = {
    f"{data.region} - {name}": data
    for name, data in loonyland_location_table.items()
}