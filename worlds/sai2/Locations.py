from typing import List, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    rule: Callable = lambda state: True


def get_locations(world) -> Tuple[LocationData, ...]:

    location_table: Tuple[LocationData, ...] = [

    LocationData('Poka-Poka Island', 'Poka-Poka Lake Chest', 0x5A1000),
    LocationData('Poka-Poka East', 'Poka-Poka Tree Chest', 0x5A1001),
    LocationData('Poka-Poka Island', 'Poka-Poka Digging Chest', 0x5A1002),
    LocationData('Poka-Poka East', 'Poka-Poka Pushable Rock Chest', 0x5A1003),
    LocationData('Poka-Poka East', 'Poka-Poka Sun Blocks Chest', 0x5A1004),
    LocationData('Poka-Poka East', 'Poka-Poka East Cave Chest', 0x5A1005),
    LocationData('Poka-Poka Island', 'Poka-Poka West Cave Chest', 0x5A1006),
    LocationData('Poka-Poka East', 'Poka-Poka Moon Alcove Chest', 0x5A1007),
    LocationData('Poka-Poka East', 'Poka-Poka Down Blocks Chest', 0x5A1008),
    LocationData('Poka-Poka East', 'Poka-Poka Shrine Chest', 0x5A1009),
    LocationData('Poka-Poka East', 'Evil Tree Chest', 0x5A100A),

    LocationData('Boa-Boa Island', 'Boa-Boa Clouds Chest', 0x5A100B),
    LocationData('Boa-Boa Island', 'Boa-Boa Sun Alcove Chest', 0x5A100C),
    LocationData('Boa-Boa Island', 'Boa-Boa Sun Block Chest', 0x5A100D),
    LocationData('Boa-Boa Island', 'Boa-Boa Lava Lake West Chest', 0x5A100E),
    LocationData('Boa-Boa Island', 'Boa-Boa Lava Lake East Chest', 0x5A100F),
    LocationData('Boa-Boa Island', 'Boa-Boa Western Shaft Chest', 0x5A1010),
    LocationData('Boa-Boa Island', 'Boa-Boa Eastern Shaft Chest', 0x5A1011),
    LocationData('Boa-Boa Island', 'Boa-Boa Shrine Chest', 0x5A1012),
    LocationData('Boa-Boa Island', 'Tortoise Chest', 0x5A1013),

    LocationData('Hiya-Hiya Entrance', 'Hiya-Hiya Clouds Chest', 0x5A1014),
    LocationData('Hiya-Hiya Underside', 'Hiya-Hiya Underground Chest', 0x5A1015),
    LocationData('Hiya-Hiya Entrance', 'Hiya-Hiya Sun Blocks Chest', 0x5A1016),
    LocationData('Hiya-Hiya Main', 'Hiya-Hiya Hidden Alcove Chest', 0x5A1017),
    LocationData('Hiya-Hiya Main', 'Hiya-Hiya Up Block Alcove Chest', 0x5A1018),
    LocationData('Hiya-Hiya Main', 'Hiya-Hiya Trapped Chest', 0x5A1019),
    LocationData('Hiya-Hiya Main', 'Hiya-Hiya Ice Cubes Chest', 0x5A101A),
    LocationData('Hiya-Hiya Main', 'Hiya-Hiya Long Fall Chest', 0x5A101B),
    LocationData('Hiya-Hiya Back', 'Hiya-Hiya Vines Chest', 0x5A101C),
    LocationData('Hiya-Hiya Back', 'Hiya-Hiya Shrine Chest', 0x5A101D),
    LocationData('Hiya-Hiya Main', 'Mammoth Chest', 0x5A101E),

    LocationData('Puka-Puka Island', 'Puka-Puka Light Blocks Chest', 0x5A101F),
    LocationData('Puka-Puka Island', 'Puka-Puka Down Jab Chest', 0x5A1020),
    LocationData('Puka-Puka Island', 'Puka-Puka Star Blocks Chest', 0x5A1021),
    LocationData('Puka-Puka Island', 'Puka-Puka Up Jab Chest', 0x5A1022),
    LocationData('Puka-Puka Island', 'Puka-Puka Underwater Chest', 0x5A1023),
    LocationData('Puka-Puka Island', 'Puka-Puka Aqua Blocks Chest', 0x5A1024),
    LocationData('Puka-Puka Island', 'Puka-Puka Spike Maze Upper Chest', 0x5A1025),
    LocationData('Puka-Puka Island', 'Puka-Puka Spike Maze Lower Chest', 0x5A1026),
    LocationData('Puka-Puka Island', 'Puka-Puka Moving Platforms Chest', 0x5A1027),
    LocationData('Puka-Puka Island', 'Puka-Puka Springs Chest', 0x5A1028),
    LocationData('Puka-Puka Island', 'Puka-Puka Shrine Chest', 0x5A1029),
    LocationData('Puka-Puka Island', 'Octopus Chest', 0x5A102A),

    LocationData('Sala-Sala Island', 'Sala-Sala Near Entrance Chest', 0x5A102B),
    LocationData('Sala-Sala Island', 'Sala-Sala Up Jab Chest', 0x5A102C),
    LocationData('Sala-Sala Island', 'Sala-Sala Star Alcove Chest', 0x5A102D),
    LocationData('Sala-Sala Island', 'Sala-Sala Top of the Pyramid Chest', 0x5A102E),
    LocationData('Sala-Sala Backside', 'Sala-Sala All Blocks Chest', 0x5A102F),
    LocationData('Sala-Sala Backside', 'Sala-Sala Farthest Chest', 0x5A1030),
    LocationData('Sala-Sala Island', 'Sala-Sala Pyramid Center Chest', 0x5A1031),
    LocationData('Sala-Sala Backside', 'Sala-Sala Elevator Chest', 0x5A1032),
    LocationData('Sala-Sala Backside', 'Sala-Sala Shrine Chest', 0x5A1033),
    LocationData('Sala-Sala Backside', 'Mummy Chest', 0x5A1034),

    LocationData('Fuwa-Fuwa Island', 'Fuwa-Fuwa Block Maze Chest', 0x5A1035),
    LocationData('Fuwa-Fuwa Island', 'Fuwa-Fuwa Moon Block Chest', 0x5A1036),
    LocationData('Fuwa-Fuwa Island', 'Fuwa-Fuwa Light Block Chest', 0x5A1037),
    LocationData('Fuwa-Fuwa Island', 'Fuwa-Fuwa Bridge Room Chest', 0x5A1038),
    LocationData('Fuwa-Fuwa Island', 'Fuwa-Fuwa Balance Platforms Chest', 0x5A1039),
    LocationData('Fuwa-Fuwa Island', 'Hawk Chest', 0x5A103A),

    LocationData('Western Sea', 'Muscle Lizard Chest', 0x5A103B),
    LocationData('Northwestern Sea', 'Ice Cave Chest', 0x5A103C),
    LocationData('Northwestern Sea', '100 Coin Shop', 0x5A103D),
    LocationData('Northeastern Sea', 'Desert Island Chest', 0x5A103E),
    LocationData('Northeastern Sea', 'Overworld Tomb Chest', 0x5A103F),
    LocationData('Eastern Sea', 'Saber Tooth Chest', 0x5A1040),
    LocationData('Eastern Sea', 'Northern Cave Chest', 0x5A1041),
    LocationData('Eastern Sea', '300 Coin Shop', 0x5A1042),
    LocationData('Eastern Sea', '500 Coin Shop', 0x5A1043),
    #LocationData('Southern Sea', "Waku-Waku King's Gift", 0x5A1044),
    LocationData("Curly's Casino", "Casino 500 Coin Purchase", 0x5A1045),
    LocationData("Curly's Casino", "Casino 1000 Coin Purchase", 0x5A1046),
    LocationData("Curly's Casino", "Casino 2000 Coin Purchase", 0x5A1047),
    LocationData("Curly's Casino", "Casino 3000 Coin Purchase", 0x5A1048),
    LocationData("Curly's Casino", "Casino 5000 Coin Purchase", 0x5A1049),

    LocationData("Poka-Poka Island", 'Poka-Poka First Cave', None),
    LocationData("Boa-Boa Island", 'Boa-Boa Hidden Wall', None),
    LocationData("Hiya-Hiya Main", 'Hiya-Hiya Top Level', None),
    LocationData("Puka-Puka Switch Room", 'Puka-Puka Switch Room', None),
    LocationData("Sala-Sala Island", 'Sala-Sala Switch Room', None),
    LocationData("Puka-Puka Island", 'Puka-Puka Water Control', None),
    LocationData("Fuwa-Fuwa Island", 'Phantom Defeat', None),

    LocationData("Boa-Boa Island", 'Boa-Hiya Shortcut Room', None),
    LocationData("Sala-Sala Backside", 'Sala-Hiya Shortcut Room', None),
    LocationData("Sala-Sala Island", 'Sala-Puka Shortcut Room', None),
    LocationData("Fuwa-Fuwa Island", 'Fuwa-Puka Shortcut Room', None),
    LocationData("Fuwa-Fuwa Island", 'Fuwa-Poka Shortcut Room', None),

    LocationData("Southern Sea", 'Light Gate', None),
    LocationData("Western Sea", 'Sun Gate', None),
    LocationData("Northwestern Sea", 'Star Gate', None),
    LocationData("Southern Sea", 'Aqua Gate', None),
    LocationData("Southeastern Sea", 'Moon Gate', None)
    ]
        
    return location_table