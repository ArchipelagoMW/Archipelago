tmx_map_tags = ("Race","FullSpeed","Tech","RPG","LOL","Press Forward","SpeedTech","MultiLap",
               "Offroad","Trial","ZrT","SpeedFun","Competitive","Ice","Dirt","Stunt","Reactor",
               "Platform","Slow Motion","Bumper","Fragile","Scenery","Kacky","Endurance","Mini",
               "Remake","Mixed","Nascar","SpeedDrift","Minigame","Obstacle","Transitional","Grass",
               "Backwards","EngineOff","Signature","Royal","Water","Plastic","Arena","Freestyle",
               "Educational","Sausage","Bobsleigh","Pathfinding","FlagRush","Puzzle","Freeblocking",
               "Altered Nadeo","SnowCar","Wood","Underwater","Turtle","RallyCar","MixedCar",
               "Bugslide","Mudslide","Moving Items","DesertCar","SpeedMapping","NoBrake","CruiseControl",
               "NoSteer","RPG-Immersive","Pipes","Magnet","NoGrip")

tmx_default_excluded_tags = ("Kacky, Royal, Arena")

def GetAllMapTags() -> tuple[str]:
    return tmx_map_tags

def GetExcludedMapTags() -> tuple[str]:
    return tmx_default_excluded_tags


