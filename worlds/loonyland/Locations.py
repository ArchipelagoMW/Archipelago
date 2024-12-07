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
    "Swamp Mud Path": LoonylandLocationData(0, LocationCategory.PICKUP, "Halloween Hill"),
    "Bog Beast Home": LoonylandLocationData(1, LocationCategory.PICKUP, "Halloween Hill"),
    "Rocky Cliffs below Upper Caverns":     LoonylandLocationData(2, LocationCategory.PICKUP, "Halloween Hill"),
    "Sapling Shrine":     LoonylandLocationData(3, LocationCategory.PICKUP, "Halloween Hill"),
    "Terror Glade":     LoonylandLocationData(4, LocationCategory.PICKUP, "Halloween Hill"),
    "Rocky Cliffs Vine":     LoonylandLocationData(5, LocationCategory.PICKUP, "Halloween Hill"),
    "Rocky Cliffs Grand Pharoh":     LoonylandLocationData(6, LocationCategory.PICKUP, "Halloween Hill"),
    "Rocky Cliffs Rock Corner":     LoonylandLocationData(7, LocationCategory.PICKUP, "Halloween Hill"),
    "Mushroom outside town":     LoonylandLocationData(8, LocationCategory.PICKUP, "Halloween Hill"),
    "North of UG Passage":     LoonylandLocationData(9, LocationCategory.PICKUP, "Halloween Hill"),
    "Top left mushroom spot":   LoonylandLocationData(10, LocationCategory.PICKUP, "Halloween Hill"),
    "NE of UG Passage":     LoonylandLocationData(11, LocationCategory.PICKUP, "Halloween Hill"),
    "East Woods":     LoonylandLocationData(12, LocationCategory.PICKUP, "Halloween Hill"),
    "Rocky Cliffs Ledge":     LoonylandLocationData(13, LocationCategory.PICKUP, "Halloween Hill"),
    "Rocky Cliffs Peak":     LoonylandLocationData(14, LocationCategory.PICKUP, "Halloween Hill"),
    "Cat Tree":     LoonylandLocationData(15, LocationCategory.PICKUP, "Halloween Hill"),
    "Bedroom":     LoonylandLocationData(16, LocationCategory.PICKUP, "The Witch's Cabin"),
    "Backroom":     LoonylandLocationData(17, LocationCategory.PICKUP, "The Witch's Cabin"),
    "Barrel Maze":     LoonylandLocationData(18, LocationCategory.PICKUP, "Bonita's Cabin"),
    "Top Door":     LoonylandLocationData(19, LocationCategory.PICKUP, "The Bog Pit"),
    "Post Room":     LoonylandLocationData(20, LocationCategory.PICKUP, "The Bog Pit"),
    "Window Drip":     LoonylandLocationData(21, LocationCategory.PICKUP, "The Bog Pit"),
    "Green room":     LoonylandLocationData(22, LocationCategory.PICKUP, "The Bog Pit"),
    "Arena":     LoonylandLocationData(23, LocationCategory.PICKUP, "The Bog Pit"),
    "Kill Wall":     LoonylandLocationData(24, LocationCategory.PICKUP, "The Bog Pit"),
    "Swampdog Door":     LoonylandLocationData(25, LocationCategory.PICKUP, "Underground Tunnel"),
    "Scribble Wall":     LoonylandLocationData(26, LocationCategory.PICKUP, "Underground Tunnel"),
    "Tiny Passage":     LoonylandLocationData(27, LocationCategory.PICKUP, "Underground Tunnel"),
    "fire frogs":     LoonylandLocationData(28, LocationCategory.PICKUP, "Underground Tunnel"),
    "Torch Island":     LoonylandLocationData(29, LocationCategory.PICKUP, "Underground Tunnel"),
    "Small Room":     LoonylandLocationData(30, LocationCategory.PICKUP, "Underground Tunnel"),
    "Scratch Wall":     LoonylandLocationData(31, LocationCategory.PICKUP, "Swamp Gas Cavern"),
    "Bat Mound":     LoonylandLocationData(32, LocationCategory.PICKUP, "Swamp Gas Cavern"),
    "Stair room":     LoonylandLocationData(33, LocationCategory.PICKUP, "Swamp Gas Cavern"),
    "Rock Prison":     LoonylandLocationData(34, LocationCategory.PICKUP, "Swamp Gas Cavern"),
    "Tiny Cabin":     LoonylandLocationData(35, LocationCategory.PICKUP, "A Tiny Cabin"),
    "Bedside ":     LoonylandLocationData(36, LocationCategory.PICKUP, "A Cabin"),
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
    "Bombulus":     LoonylandLocationData(53, LocationCategory.PICKUP, "The Shrine of Bombulus"),
    "Lockpick":     LoonylandLocationData(54, LocationCategory.PICKUP, "A Gloomy Cavern"),
    "Happy Stick Hidden":     LoonylandLocationData(55, LocationCategory.PICKUP, "Happy Stick Woods"),
    "Happy Stick Reward":     LoonylandLocationData(56, LocationCategory.PICKUP, "Happy Stick Woods"),
    "Wolf Top Left":     LoonylandLocationData(57, LocationCategory.PICKUP, "The Wolf Den"),
    "Pumpkin Door":     LoonylandLocationData(58, LocationCategory.PICKUP, "The Wolf Den"),
    "Grow Room":     LoonylandLocationData(59, LocationCategory.PICKUP, "The Wolf Den"),
    "The Three ombres":     LoonylandLocationData(60, LocationCategory.PICKUP, "Upper Creepy Cavern"),
    "Left Vine":     LoonylandLocationData(61, LocationCategory.PICKUP, "Under the Ravine"),
    "Right Vine":     LoonylandLocationData(62, LocationCategory.PICKUP, "Under the Ravine"),
    "M Pharoh bat Room":     LoonylandLocationData(63, LocationCategory.PICKUP, "Creepy Caverns"),
    "E 2 blue Pharos":     LoonylandLocationData(64, LocationCategory.PICKUP, "Creepy Caverns"),
    "M GARGOYLE ROOM":     LoonylandLocationData(65, LocationCategory.PICKUP, "Creepy Caverns"),
    "Vampire Guard":     LoonylandLocationData(66, LocationCategory.PICKUP, "Castle Vampy"),
    "maze top left":     LoonylandLocationData(67, LocationCategory.PICKUP, "Castle Vampy"),
    "Top Right Gauntlet":     LoonylandLocationData(68, LocationCategory.PICKUP, "Castle Vampy"),
    "Bat Closet":     LoonylandLocationData(69, LocationCategory.PICKUP, "Castle Vampy"),
    "Candle Room":     LoonylandLocationData(70, LocationCategory.PICKUP, "Castle Vampy II"),
    "Top Right Top":     LoonylandLocationData(71, LocationCategory.PICKUP, "Castle Vampy II"),
    "Bottom Right Middle":     LoonylandLocationData(72, LocationCategory.PICKUP, "Castle Vampy II"),
    "Bat room":     LoonylandLocationData(73, LocationCategory.PICKUP, "Castle Vampy II"),
    "Gold Skull":     LoonylandLocationData(74, LocationCategory.PICKUP, "Cabin In The Woods"),
    "Middle":     LoonylandLocationData(75, LocationCategory.PICKUP, "Castle Vampy III"),
    "Behind the Pews":     LoonylandLocationData(76, LocationCategory.PICKUP, "Castle Vampy III"),
    "AMBUSH!":     LoonylandLocationData(77, LocationCategory.PICKUP, "Castle Vampy III"),
    "Halloween":     LoonylandLocationData(78, LocationCategory.PICKUP, "Castle Vampy III"),
    "So many bats":     LoonylandLocationData(79, LocationCategory.PICKUP, "Castle Vampy III"),
    "Right Path":     LoonylandLocationData(80, LocationCategory.PICKUP, "Castle Vampy IV"),
    "Left Path":     LoonylandLocationData(81, LocationCategory.PICKUP, "Castle Vampy IV"),
    "Ballroom Right":     LoonylandLocationData(82, LocationCategory.PICKUP, "Castle Vampy IV"),
    "Right Secret Wall":     LoonylandLocationData(83, LocationCategory.PICKUP, "Castle Vampy IV"),
    "Ballroom Left":     LoonylandLocationData(84, LocationCategory.PICKUP, "Castle Vampy IV"),
    "Gutsy the Elder":     LoonylandLocationData(85, LocationCategory.PICKUP, "Castle Vampy Roof"),
    "Stoney the Elder":     LoonylandLocationData(86, LocationCategory.PICKUP, "Castle Vampy Roof"),
    "Drippy the Elder":     LoonylandLocationData(87, LocationCategory.PICKUP, "Castle Vampy Roof"),
    "Toasty the Elder":     LoonylandLocationData(88, LocationCategory.PICKUP, "Castle Vampy Roof"),
    "Bonkula":     LoonylandLocationData(89, LocationCategory.PICKUP, "Heart of Terror"),
    "Bat Door":     LoonylandLocationData(90, LocationCategory.PICKUP, "A Hidey-Hole"),
    "Pebbles":     LoonylandLocationData(91, LocationCategory.PICKUP, "A Hidey-Hole"),
    "Entrance":     LoonylandLocationData(92, LocationCategory.PICKUP, "Swampdog Lair"),
    "End":     LoonylandLocationData(93, LocationCategory.PICKUP, "Swampdog Lair"),
    "Save Halloween Hill":     LoonylandLocationData(94, LocationCategory.QUEST, "The Evilizer"),
    "Ghostbusting":     LoonylandLocationData(95, LocationCategory.QUEST, "The Witch's Cabin"),
    "Hairy Larry":     LoonylandLocationData(96, LocationCategory.QUEST, "A Cabin3"),
    "Scaredy Cat":     LoonylandLocationData(97, LocationCategory.QUEST, "Halloween Hill"),
    "Silver Bullet":     LoonylandLocationData(98, LocationCategory.QUEST, "Halloween Hill"),
    "Smashing Pumpkins":     LoonylandLocationData(99, LocationCategory.QUEST, "Halloween Hill"),
    "Sticky Shoes":     LoonylandLocationData(100, LocationCategory.QUEST, "Halloween Hill"),
    "The Collection":     LoonylandLocationData(101, LocationCategory.QUEST, "A Cabin4"),
    "The Rescue":     LoonylandLocationData(102, LocationCategory.QUEST, "A Gloomy Cavern"),
    "Tree Trimming":     LoonylandLocationData(103, LocationCategory.QUEST, "A Cabin"),
    "Witch Mushrooms":     LoonylandLocationData(104, LocationCategory.QUEST, "The Witch's Cabin"),
    "Zombie Stomp":     LoonylandLocationData(105, LocationCategory.QUEST, "Halloween Hill")
    #todo the 40 badge locations
    }

loonyland_location_table = {
    f"{data.region} - {name}": data
    for name, data in loonyland_location_table.items()
}