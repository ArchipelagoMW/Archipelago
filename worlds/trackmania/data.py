from enum import Enum

base_id = 24000

tmx_map_tags = ["Race","FullSpeed","Tech","RPG","LOL","Press Forward","SpeedTech","MultiLap",
               "Offroad","Trial","ZrT","SpeedFun","Competitive","Ice","Dirt","Stunt","Reactor",
               "Platform","Slow Motion","Bumper","Fragile","Scenery","Kacky","Endurance","Mini",
               "Remake","Mixed","Nascar","SpeedDrift","Minigame","Obstacle","Transitional","Grass",
               "Backwards","EngineOff","Signature","Royal","Water","Plastic","Arena","Freestyle",
               "Educational","Sausage","Bobsleigh","Pathfinding","FlagRush","Puzzle","Freeblocking",
               "Altered Nadeo","SnowCar","Wood","Underwater","Turtle","RallyCar","MixedCar",
               "Bugslide","Mudslide","Moving Items","DesertCar","SpeedMapping","NoBrake","CruiseControl",
               "NoSteer","RPG-Immersive","Pipes","Magnet","NoGrip",
                #tm2 exclusive tags
                "Glass","Sand","Cobblestone","ForceAccel"]

tmx_map_difficulties = ["Beginner","Intermediate","Advanced","Expert","Lunatic","Impossible"]

tmx_default_excluded_tags = ["Kacky", "Royal", "Arena"]

tmx_default_map_difficulties = ["Beginner","Intermediate","Advanced","Expert"]

class MapCheckTypes(Enum):
    Bronze = 0
    Silver = 1
    Gold   = 2
    Author = 3
    Target = 4


def get_all_map_tags() -> list[str]:
    return tmx_map_tags

def get_excluded_map_tags() -> list[str]:
    return tmx_default_excluded_tags

def get_all_map_difficulties() -> list[str]:
    return tmx_map_difficulties

def get_default_map_difficulties() -> list[str]:
    return tmx_default_map_difficulties


