from typing import Dict, NamedTuple, List, Optional, TYPE_CHECKING
from enum import IntEnum

if TYPE_CHECKING:
    from . import TunicWorld


# the direction you go to enter a portal
class Direction(IntEnum):
    none = 0  # for when the direction isn't relevant
    north = 1
    south = 2
    east = 3
    west = 4
    floor = 5
    ladder_up = 6
    ladder_down = 7


class Portal(NamedTuple):
    name: str  # human-readable name
    region: str  # AP region
    destination: str  # vanilla destination scene
    tag: str  # vanilla tag
    direction: int  # the direction you go to enter a portal

    def scene(self) -> str:  # the actual scene name in Tunic
        if self.region.startswith("Shop"):
            return tunic_er_regions["Shop"].game_scene
        return tunic_er_regions[self.region].game_scene

    def scene_destination(self) -> str:  # full, nonchanging name to interpret by the mod
        return self.scene() + ", " + self.destination + self.tag

    def destination_scene(self) -> str:  # the vanilla connection
        return self.destination + ", " + self.scene() + self.tag


portal_mapping: List[Portal] = [
    Portal(name="Stick House Entrance", region="Overworld",
           destination="Sword Cave", tag="_", direction=Direction.north),
    Portal(name="Windmill Entrance", region="Overworld",
           destination="Windmill", tag="_", direction=Direction.north),
    Portal(name="Well Ladder Entrance", region="Overworld Well Ladder",
           destination="Sewer", tag="_entrance", direction=Direction.ladder_down),
    Portal(name="Entrance to Well from Well Rail", region="Overworld Well to Furnace Rail",
           destination="Sewer", tag="_west_aqueduct", direction=Direction.north),
    Portal(name="Old House Door Entrance", region="Overworld Old House Door",
           destination="Overworld Interiors", tag="_house", direction=Direction.east),
    Portal(name="Old House Waterfall Entrance", region="Overworld",
           destination="Overworld Interiors", tag="_under_checkpoint", direction=Direction.east),
    Portal(name="Entrance to Furnace from Well Rail", region="Overworld Well to Furnace Rail",
           destination="Furnace", tag="_gyro_upper_north", direction=Direction.south),
    Portal(name="Entrance to Furnace under Windmill", region="Overworld",
           destination="Furnace", tag="_gyro_upper_east", direction=Direction.west),
    Portal(name="Entrance to Furnace near West Garden", region="Overworld to West Garden from Furnace",
           destination="Furnace", tag="_gyro_west", direction=Direction.east),
    Portal(name="Entrance to Furnace from Beach", region="Overworld Tunnel Turret",
           destination="Furnace", tag="_gyro_lower", direction=Direction.north),
    Portal(name="Caustic Light Cave Entrance", region="Overworld Swamp Lower Entry",
           destination="Overworld Cave", tag="_", direction=Direction.north),
    Portal(name="Swamp Upper Entrance", region="Overworld Swamp Upper Entry",
           destination="Swamp Redux 2", tag="_wall", direction=Direction.south),
    Portal(name="Swamp Lower Entrance", region="Overworld Swamp Lower Entry",
           destination="Swamp Redux 2", tag="_conduit", direction=Direction.south),
    Portal(name="Ruined Passage Not-Door Entrance", region="After Ruined Passage",
           destination="Ruins Passage", tag="_east", direction=Direction.north),
    Portal(name="Ruined Passage Door Entrance", region="Overworld Ruined Passage Door",
           destination="Ruins Passage", tag="_west", direction=Direction.east),
    Portal(name="Atoll Upper Entrance", region="Overworld to Atoll Upper",
           destination="Atoll Redux", tag="_upper", direction=Direction.south),
    Portal(name="Atoll Lower Entrance", region="Overworld Beach",
           destination="Atoll Redux", tag="_lower", direction=Direction.south),
    Portal(name="Special Shop Entrance", region="Overworld Special Shop Entry",
           destination="ShopSpecial", tag="_", direction=Direction.east),
    Portal(name="Maze Cave Entrance", region="Overworld Beach",
           destination="Maze Room", tag="_", direction=Direction.north),
    Portal(name="West Garden Entrance near Belltower", region="Overworld to West Garden Upper",
           destination="Archipelagos Redux", tag="_upper", direction=Direction.west),
    Portal(name="West Garden Entrance from Furnace", region="Overworld to West Garden from Furnace",
           destination="Archipelagos Redux", tag="_lower", direction=Direction.west),
    Portal(name="West Garden Laurels Entrance", region="Overworld West Garden Laurels Entry",
           destination="Archipelagos Redux", tag="_lowest", direction=Direction.west),
    Portal(name="Temple Door Entrance", region="Overworld Temple Door",
           destination="Temple", tag="_main", direction=Direction.north),
    Portal(name="Temple Rafters Entrance", region="Overworld after Temple Rafters",
           destination="Temple", tag="_rafters", direction=Direction.east),
    Portal(name="Ruined Shop Entrance", region="Overworld",
           destination="Ruined Shop", tag="_", direction=Direction.east),
    Portal(name="Patrol Cave Entrance", region="Overworld at Patrol Cave",
           destination="PatrolCave", tag="_", direction=Direction.north),
    Portal(name="Hourglass Cave Entrance", region="Overworld Beach",
           destination="Town Basement", tag="_beach", direction=Direction.north),
    Portal(name="Changing Room Entrance", region="Overworld",
           destination="Changing Room", tag="_", direction=Direction.south),
    Portal(name="Cube Cave Entrance", region="Cube Cave Entrance Region",
           destination="CubeRoom", tag="_", direction=Direction.north),
    Portal(name="Stairs from Overworld to Mountain", region="Upper Overworld",
           destination="Mountain", tag="_", direction=Direction.north),
    Portal(name="Overworld to Fortress", region="East Overworld",
           destination="Fortress Courtyard", tag="_", direction=Direction.east),
    Portal(name="Fountain HC Door Entrance", region="Overworld Fountain Cross Door",
           destination="Town_FiligreeRoom", tag="_", direction=Direction.north),
    Portal(name="Southeast HC Door Entrance", region="Overworld Southeast Cross Door",
           destination="EastFiligreeCache", tag="_", direction=Direction.north),
    Portal(name="Overworld to Quarry Connector", region="Overworld Quarry Entry",
           destination="Darkwoods Tunnel", tag="_", direction=Direction.north),
    Portal(name="Dark Tomb Main Entrance", region="Overworld",
           destination="Crypt Redux", tag="_", direction=Direction.north),
    Portal(name="Overworld to Forest Belltower", region="East Overworld",
           destination="Forest Belltower", tag="_", direction=Direction.east),
    Portal(name="Town to Far Shore", region="Overworld Town Portal",
           destination="Transit", tag="_teleporter_town", direction=Direction.floor),
    Portal(name="Spawn to Far Shore", region="Overworld Spawn Portal",
           destination="Transit", tag="_teleporter_starting island", direction=Direction.floor),
    Portal(name="Secret Gathering Place Entrance", region="Overworld",
           destination="Waterfall", tag="_", direction=Direction.north),

    Portal(name="Secret Gathering Place Exit", region="Secret Gathering Place",
           destination="Overworld Redux", tag="_", direction=Direction.south),

    Portal(name="Windmill Exit", region="Windmill",
           destination="Overworld Redux", tag="_", direction=Direction.south),
    Portal(name="Windmill Shop", region="Windmill",
           destination="Shop", tag="_", direction=Direction.north),

    Portal(name="Old House Door Exit", region="Old House Front",
           destination="Overworld Redux", tag="_house", direction=Direction.west),
    Portal(name="Old House to Glyph Tower", region="Old House Front",
           destination="g_elements", tag="_", direction=Direction.south),  # portal drops you on north side
    Portal(name="Old House Waterfall Exit", region="Old House Back",
           destination="Overworld Redux", tag="_under_checkpoint", direction=Direction.west),

    Portal(name="Glyph Tower Exit", region="Relic Tower",
           destination="Overworld Interiors", tag="_", direction=Direction.north),

    Portal(name="Changing Room Exit", region="Changing Room",
           destination="Overworld Redux", tag="_", direction=Direction.north),

    Portal(name="Fountain HC Room Exit", region="Fountain Cross Room",
           destination="Overworld Redux", tag="_", direction=Direction.south),

    Portal(name="Cube Cave Exit", region="Cube Cave",
           destination="Overworld Redux", tag="_", direction=Direction.south),

    Portal(name="Guard Patrol Cave Exit", region="Patrol Cave",
           destination="Overworld Redux", tag="_", direction=Direction.south),

    Portal(name="Ruined Shop Exit", region="Ruined Shop",
           destination="Overworld Redux", tag="_", direction=Direction.west),

    Portal(name="Furnace Exit towards Well", region="Furnace Fuse",
           destination="Overworld Redux", tag="_gyro_upper_north", direction=Direction.north),
    Portal(name="Furnace Exit to Dark Tomb", region="Furnace Walking Path",
           destination="Crypt Redux", tag="_", direction=Direction.east),
    Portal(name="Furnace Exit towards West Garden", region="Furnace Walking Path",
           destination="Overworld Redux", tag="_gyro_west", direction=Direction.west),
    Portal(name="Furnace Exit to Beach", region="Furnace Ladder Area",
           destination="Overworld Redux", tag="_gyro_lower", direction=Direction.south),
    Portal(name="Furnace Exit under Windmill", region="Furnace Ladder Area",
           destination="Overworld Redux", tag="_gyro_upper_east", direction=Direction.east),

    Portal(name="Stick House Exit", region="Stick House",
           destination="Overworld Redux", tag="_", direction=Direction.south),

    Portal(name="Ruined Passage Not-Door Exit", region="Ruined Passage",
           destination="Overworld Redux", tag="_east", direction=Direction.south),
    Portal(name="Ruined Passage Door Exit", region="Ruined Passage",
           destination="Overworld Redux", tag="_west", direction=Direction.west),

    Portal(name="Southeast HC Room Exit", region="Southeast Cross Room",
           destination="Overworld Redux", tag="_", direction=Direction.south),

    Portal(name="Caustic Light Cave Exit", region="Caustic Light Cave",
           destination="Overworld Redux", tag="_", direction=Direction.south),

    Portal(name="Maze Cave Exit", region="Maze Cave",
           destination="Overworld Redux", tag="_", direction=Direction.south),

    Portal(name="Hourglass Cave Exit", region="Hourglass Cave",
           destination="Overworld Redux", tag="_beach", direction=Direction.south),

    Portal(name="Special Shop Exit", region="Special Shop",
           destination="Overworld Redux", tag="_", direction=Direction.west),

    Portal(name="Temple Rafters Exit", region="Sealed Temple Rafters",
           destination="Overworld Redux", tag="_rafters", direction=Direction.west),
    Portal(name="Temple Door Exit", region="Sealed Temple",
           destination="Overworld Redux", tag="_main", direction=Direction.south),

    Portal(name="Forest Belltower to Fortress", region="Forest Belltower Main behind bushes",
           destination="Fortress Courtyard", tag="_", direction=Direction.north),
    Portal(name="Forest Belltower to Forest", region="Forest Belltower Lower",
           destination="East Forest Redux", tag="_", direction=Direction.south),
    Portal(name="Forest Belltower to Overworld", region="Forest Belltower Main",
           destination="Overworld Redux", tag="_", direction=Direction.west),
    Portal(name="Forest Belltower to Guard Captain Room", region="Forest Belltower Upper",
           destination="Forest Boss Room", tag="_", direction=Direction.south),

    Portal(name="Forest to Belltower", region="East Forest",
           destination="Forest Belltower", tag="_", direction=Direction.north),
    Portal(name="Forest Guard House 1 Lower Entrance", region="East Forest",
           destination="East Forest Redux Laddercave", tag="_lower", direction=Direction.north),
    Portal(name="Forest Guard House 1 Gate Entrance", region="East Forest",
           destination="East Forest Redux Laddercave", tag="_gate", direction=Direction.north),
    Portal(name="Forest Dance Fox Outside Doorway", region="East Forest Dance Fox Spot",
           destination="East Forest Redux Laddercave", tag="_upper", direction=Direction.east),
    Portal(name="Forest to Far Shore", region="East Forest Portal",
           destination="Transit", tag="_teleporter_forest teleporter", direction=Direction.floor),
    Portal(name="Forest Guard House 2 Lower Entrance", region="Lower Forest",
           destination="East Forest Redux Interior", tag="_lower", direction=Direction.north),
    Portal(name="Forest Guard House 2 Upper Entrance", region="East Forest",
           destination="East Forest Redux Interior", tag="_upper", direction=Direction.east),
    Portal(name="Forest Grave Path Lower Entrance", region="East Forest",
           destination="Sword Access", tag="_lower", direction=Direction.east),
    Portal(name="Forest Grave Path Upper Entrance", region="East Forest",
           destination="Sword Access", tag="_upper", direction=Direction.east),

    Portal(name="Forest Grave Path Upper Exit", region="Forest Grave Path Upper",
           destination="East Forest Redux", tag="_upper", direction=Direction.west),
    Portal(name="Forest Grave Path Lower Exit", region="Forest Grave Path Main",
           destination="East Forest Redux", tag="_lower", direction=Direction.west),
    Portal(name="East Forest Hero's Grave", region="Forest Hero's Grave",
           destination="RelicVoid", tag="_teleporter_relic plinth", direction=Direction.floor),

    Portal(name="Guard House 1 Dance Fox Exit", region="Guard House 1 West",
           destination="East Forest Redux", tag="_upper", direction=Direction.west),
    Portal(name="Guard House 1 Lower Exit", region="Guard House 1 West",
           destination="East Forest Redux", tag="_lower", direction=Direction.south),
    Portal(name="Guard House 1 Upper Forest Exit", region="Guard House 1 East",
           destination="East Forest Redux", tag="_gate", direction=Direction.south),
    Portal(name="Guard House 1 to Guard Captain Room", region="Guard House 1 East",
           destination="Forest Boss Room", tag="_", direction=Direction.north),

    Portal(name="Guard House 2 Lower Exit", region="Guard House 2 Lower",
           destination="East Forest Redux", tag="_lower", direction=Direction.south),
    Portal(name="Guard House 2 Upper Exit", region="Guard House 2 Upper before bushes",
           destination="East Forest Redux", tag="_upper", direction=Direction.west),

    Portal(name="Guard Captain Room Non-Gate Exit", region="Forest Boss Room",
           destination="East Forest Redux Laddercave", tag="_", direction=Direction.south),
    Portal(name="Guard Captain Room Gate Exit", region="Forest Boss Room",
           destination="Forest Belltower", tag="_", direction=Direction.north),

    Portal(name="Well Ladder Exit", region="Beneath the Well Ladder Exit",
           destination="Overworld Redux", tag="_entrance", direction=Direction.ladder_up),
    Portal(name="Well to Well Boss", region="Beneath the Well Back",
           destination="Sewer_Boss", tag="_", direction=Direction.east),
    Portal(name="Well Exit towards Furnace", region="Beneath the Well Back",
           destination="Overworld Redux", tag="_west_aqueduct", direction=Direction.south),

    Portal(name="Well Boss to Well", region="Well Boss",
           destination="Sewer", tag="_", direction=Direction.west),
    Portal(name="Checkpoint to Dark Tomb", region="Dark Tomb Checkpoint",
           destination="Crypt Redux", tag="_", direction=Direction.ladder_up),

    Portal(name="Dark Tomb to Overworld", region="Dark Tomb Entry Point",
           destination="Overworld Redux", tag="_", direction=Direction.south),
    Portal(name="Dark Tomb to Furnace", region="Dark Tomb Dark Exit",
           destination="Furnace", tag="_", direction=Direction.west),
    Portal(name="Dark Tomb to Checkpoint", region="Dark Tomb Entry Point",
           destination="Sewer_Boss", tag="_", direction=Direction.ladder_down),

    Portal(name="West Garden Exit near Hero's Grave", region="West Garden before Terry",
           destination="Overworld Redux", tag="_lower", direction=Direction.east),
    Portal(name="West Garden to Magic Dagger House", region="West Garden at Dagger House",
           destination="archipelagos_house", tag="_", direction=Direction.east),
    Portal(name="West Garden Exit after Boss", region="West Garden after Boss",
           destination="Overworld Redux", tag="_upper", direction=Direction.east),
    Portal(name="West Garden Shop", region="West Garden before Terry",
           destination="Shop", tag="_", direction=Direction.east),
    Portal(name="West Garden Laurels Exit", region="West Garden Laurels Exit Region",
           destination="Overworld Redux", tag="_lowest", direction=Direction.east),
    Portal(name="West Garden Hero's Grave", region="West Garden Hero's Grave Region",
           destination="RelicVoid", tag="_teleporter_relic plinth", direction=Direction.floor),
    Portal(name="West Garden to Far Shore", region="West Garden Portal",
           destination="Transit", tag="_teleporter_archipelagos_teleporter", direction=Direction.floor),

    Portal(name="Magic Dagger House Exit", region="Magic Dagger House",
           destination="Archipelagos Redux", tag="_", direction=Direction.west),

    Portal(name="Fortress Courtyard to Fortress Grave Path Lower", region="Fortress Courtyard",
           destination="Fortress Reliquary", tag="_Lower", direction=Direction.east),
    Portal(name="Fortress Courtyard to Fortress Grave Path Upper", region="Fortress Courtyard Upper",
           destination="Fortress Reliquary", tag="_Upper", direction=Direction.east),
    Portal(name="Fortress Courtyard to Fortress Interior", region="Fortress Courtyard",
           destination="Fortress Main", tag="_Big Door", direction=Direction.north),
    Portal(name="Fortress Courtyard to East Fortress", region="Fortress Courtyard Upper",
           destination="Fortress East", tag="_", direction=Direction.north),
    Portal(name="Fortress Courtyard to Beneath the Vault", region="Beneath the Vault Entry",
           destination="Fortress Basement", tag="_", direction=Direction.ladder_down),
    Portal(name="Fortress Courtyard to Forest Belltower", region="Fortress Exterior from East Forest",
           destination="Forest Belltower", tag="_", direction=Direction.south),
    Portal(name="Fortress Courtyard to Overworld", region="Fortress Exterior from Overworld",
           destination="Overworld Redux", tag="_", direction=Direction.west),
    Portal(name="Fortress Courtyard Shop", region="Fortress Exterior near cave",
           destination="Shop", tag="_", direction=Direction.north),

    Portal(name="Beneath the Vault to Fortress Interior", region="Beneath the Vault Back",
           destination="Fortress Main", tag="_", direction=Direction.east),
    Portal(name="Beneath the Vault to Fortress Courtyard", region="Beneath the Vault Ladder Exit",
           destination="Fortress Courtyard", tag="_", direction=Direction.ladder_up),

    Portal(name="Fortress Interior Main Exit", region="Eastern Vault Fortress",
           destination="Fortress Courtyard", tag="_Big Door", direction=Direction.south),
    Portal(name="Fortress Interior to Beneath the Earth", region="Eastern Vault Fortress",
           destination="Fortress Basement", tag="_", direction=Direction.west),
    Portal(name="Fortress Interior to Siege Engine Arena", region="Eastern Vault Fortress Gold Door",
           destination="Fortress Arena", tag="_", direction=Direction.north),
    Portal(name="Fortress Interior Shop", region="Eastern Vault Fortress",
           destination="Shop", tag="_", direction=Direction.north),
    Portal(name="Fortress Interior to East Fortress Upper", region="Eastern Vault Fortress",
           destination="Fortress East", tag="_upper", direction=Direction.east),
    Portal(name="Fortress Interior to East Fortress Lower", region="Eastern Vault Fortress",
           destination="Fortress East", tag="_lower", direction=Direction.east),

    Portal(name="East Fortress to Interior Lower", region="Fortress East Shortcut Lower",
           destination="Fortress Main", tag="_lower", direction=Direction.west),
    Portal(name="East Fortress to Courtyard", region="Fortress East Shortcut Upper",
           destination="Fortress Courtyard", tag="_", direction=Direction.south),
    Portal(name="East Fortress to Interior Upper", region="Fortress East Shortcut Upper",
           destination="Fortress Main", tag="_upper", direction=Direction.west),

    Portal(name="Fortress Grave Path Lower Exit", region="Fortress Grave Path Entry",
           destination="Fortress Courtyard", tag="_Lower", direction=Direction.west),
    Portal(name="Fortress Hero's Grave", region="Fortress Hero's Grave Region",
           destination="RelicVoid", tag="_teleporter_relic plinth", direction=Direction.floor),
    Portal(name="Fortress Grave Path Upper Exit", region="Fortress Grave Path Upper",
           destination="Fortress Courtyard", tag="_Upper", direction=Direction.west),
    Portal(name="Fortress Grave Path Dusty Entrance", region="Fortress Grave Path Dusty Entrance Region",
           destination="Dusty", tag="_", direction=Direction.north),

    Portal(name="Dusty Exit", region="Fortress Leaf Piles",
           destination="Fortress Reliquary", tag="_", direction=Direction.south),

    Portal(name="Siege Engine Arena to Fortress", region="Fortress Arena",
           destination="Fortress Main", tag="_", direction=Direction.south),
    Portal(name="Fortress to Far Shore", region="Fortress Arena Portal",
           destination="Transit", tag="_teleporter_spidertank", direction=Direction.floor),

    Portal(name="Atoll Upper Exit", region="Ruined Atoll",
           destination="Overworld Redux", tag="_upper", direction=Direction.north),
    Portal(name="Atoll Lower Exit", region="Ruined Atoll Lower Entry Area",
           destination="Overworld Redux", tag="_lower", direction=Direction.north),
    Portal(name="Atoll Shop", region="Ruined Atoll",
           destination="Shop", tag="_", direction=Direction.north),
    Portal(name="Atoll to Far Shore", region="Ruined Atoll Portal",
           destination="Transit", tag="_teleporter_atoll", direction=Direction.floor),
    Portal(name="Atoll Statue Teleporter", region="Ruined Atoll Statue",
           destination="Library Exterior", tag="_", direction=Direction.floor),
    Portal(name="Frog Stairs Eye Entrance", region="Ruined Atoll Frog Eye",
           destination="Frog Stairs", tag="_eye", direction=Direction.south),  # camera rotates, it's fine
    Portal(name="Frog Stairs Mouth Entrance", region="Ruined Atoll Frog Mouth",
           destination="Frog Stairs", tag="_mouth", direction=Direction.east),

    Portal(name="Frog Stairs Eye Exit", region="Frog Stairs Eye Exit",
           destination="Atoll Redux", tag="_eye", direction=Direction.north),
    Portal(name="Frog Stairs Mouth Exit", region="Frog Stairs Upper",
           destination="Atoll Redux", tag="_mouth", direction=Direction.west),
    Portal(name="Frog Stairs to Frog's Domain's Entrance", region="Frog Stairs to Frog's Domain",
           destination="frog cave main", tag="_Entrance", direction=Direction.ladder_down),
    Portal(name="Frog Stairs to Frog's Domain's Exit", region="Frog Stairs Lower",
           destination="frog cave main", tag="_Exit", direction=Direction.east),

    Portal(name="Frog's Domain Ladder Exit", region="Frog's Domain Entry",
           destination="Frog Stairs", tag="_Entrance", direction=Direction.ladder_up),
    Portal(name="Frog's Domain Orb Exit", region="Frog's Domain Back",
           destination="Frog Stairs", tag="_Exit", direction=Direction.west),

    Portal(name="Library Exterior Tree", region="Library Exterior Tree Region",
           destination="Atoll Redux", tag="_", direction=Direction.floor),
    Portal(name="Library Exterior Ladder", region="Library Exterior Ladder Region",
           destination="Library Hall", tag="_", direction=Direction.west),  # camera rotates

    Portal(name="Library Hall Bookshelf Exit", region="Library Hall Bookshelf",
           destination="Library Exterior", tag="_", direction=Direction.east),
    Portal(name="Library Hero's Grave", region="Library Hero's Grave Region",
           destination="RelicVoid", tag="_teleporter_relic plinth", direction=Direction.floor),
    Portal(name="Library Hall to Rotunda", region="Library Hall to Rotunda",
           destination="Library Rotunda", tag="_", direction=Direction.ladder_up),

    Portal(name="Library Rotunda Lower Exit", region="Library Rotunda to Hall",
           destination="Library Hall", tag="_", direction=Direction.ladder_down),
    Portal(name="Library Rotunda Upper Exit", region="Library Rotunda to Lab",
           destination="Library Lab", tag="_", direction=Direction.ladder_up),

    Portal(name="Library Lab to Rotunda", region="Library Lab Lower",
           destination="Library Rotunda", tag="_", direction=Direction.ladder_down),
    Portal(name="Library to Far Shore", region="Library Portal",
           destination="Transit", tag="_teleporter_library teleporter", direction=Direction.floor),
    Portal(name="Library Lab to Librarian Arena", region="Library Lab to Librarian",
           destination="Library Arena", tag="_", direction=Direction.ladder_up),

    Portal(name="Librarian Arena Exit", region="Library Arena",
           destination="Library Lab", tag="_", direction=Direction.ladder_down),

    Portal(name="Stairs to Top of the Mountain", region="Lower Mountain Stairs",
           destination="Mountaintop", tag="_", direction=Direction.north),
    Portal(name="Mountain to Quarry", region="Lower Mountain",
           destination="Quarry Redux", tag="_", direction=Direction.south),  # connecting is north
    Portal(name="Mountain to Overworld", region="Lower Mountain",
           destination="Overworld Redux", tag="_", direction=Direction.south),

    Portal(name="Top of the Mountain Exit", region="Top of the Mountain",
           destination="Mountain", tag="_", direction=Direction.south),

    Portal(name="Quarry Connector to Overworld", region="Quarry Connector",
           destination="Overworld Redux", tag="_", direction=Direction.south),
    Portal(name="Quarry Connector to Quarry", region="Quarry Connector",
           destination="Quarry Redux", tag="_", direction=Direction.north),  # rotates, it's fine

    Portal(name="Quarry to Overworld Exit", region="Quarry Entry",
           destination="Darkwoods Tunnel", tag="_", direction=Direction.south),  # rotates, it's fine
    Portal(name="Quarry Shop", region="Quarry Entry",
           destination="Shop", tag="_", direction=Direction.north),
    Portal(name="Quarry to Monastery Front", region="Quarry Monastery Entry",
           destination="Monastery", tag="_front", direction=Direction.north),
    Portal(name="Quarry to Monastery Back", region="Monastery Rope",
           destination="Monastery", tag="_back", direction=Direction.east),
    Portal(name="Quarry to Mountain", region="Quarry Back",
           destination="Mountain", tag="_", direction=Direction.north),
    Portal(name="Quarry to Ziggurat", region="Lower Quarry Zig Door",
           destination="ziggurat2020_0", tag="_", direction=Direction.north),
    Portal(name="Quarry to Far Shore", region="Quarry Portal",
           destination="Transit", tag="_teleporter_quarry teleporter", direction=Direction.floor),

    Portal(name="Monastery Rear Exit", region="Monastery Back",
           destination="Quarry Redux", tag="_back", direction=Direction.west),
    Portal(name="Monastery Front Exit", region="Monastery Front",
           destination="Quarry Redux", tag="_front", direction=Direction.south),
    Portal(name="Monastery Hero's Grave", region="Monastery Hero's Grave Region",
           destination="RelicVoid", tag="_teleporter_relic plinth", direction=Direction.floor),

    Portal(name="Ziggurat Entry Hallway to Ziggurat Upper", region="Rooted Ziggurat Entry",
           destination="ziggurat2020_1", tag="_", direction=Direction.north),
    Portal(name="Ziggurat Entry Hallway to Quarry", region="Rooted Ziggurat Entry",
           destination="Quarry Redux", tag="_", direction=Direction.south),

    Portal(name="Ziggurat Upper to Ziggurat Entry Hallway", region="Rooted Ziggurat Upper Entry",
           destination="ziggurat2020_0", tag="_", direction=Direction.south),
    Portal(name="Ziggurat Upper to Ziggurat Tower", region="Rooted Ziggurat Upper Back",
           destination="ziggurat2020_2", tag="_", direction=Direction.north),  # connecting is south

    Portal(name="Ziggurat Tower to Ziggurat Upper", region="Rooted Ziggurat Middle Top",
           destination="ziggurat2020_1", tag="_", direction=Direction.south),
    Portal(name="Ziggurat Tower to Ziggurat Lower", region="Rooted Ziggurat Middle Bottom",
           destination="ziggurat2020_3", tag="_", direction=Direction.south),

    Portal(name="Ziggurat Lower to Ziggurat Tower", region="Rooted Ziggurat Lower Entry",
           destination="ziggurat2020_2", tag="_", direction=Direction.north),
    Portal(name="Ziggurat Portal Room Entrance", region="Rooted Ziggurat Portal Room Entrance",
           destination="ziggurat2020_FTRoom", tag="_", direction=Direction.north),
    # only if fixed shop is on, removed otherwise
    Portal(name="Ziggurat Lower Falling Entrance", region="Zig Skip Exit",  # not a real region
           destination="ziggurat2020_1", tag="_zig2_skip", direction=Direction.none),

    Portal(name="Ziggurat Portal Room Exit", region="Rooted Ziggurat Portal Room Exit",
           destination="ziggurat2020_3", tag="_", direction=Direction.south),
    Portal(name="Ziggurat to Far Shore", region="Rooted Ziggurat Portal",
           destination="Transit", tag="_teleporter_ziggurat teleporter", direction=Direction.floor),

    Portal(name="Swamp Lower Exit", region="Swamp Front",
           destination="Overworld Redux", tag="_conduit", direction=Direction.north),
    Portal(name="Swamp to Cathedral Main Entrance", region="Swamp to Cathedral Main Entrance Region",
           destination="Cathedral Redux", tag="_main", direction=Direction.north),
    Portal(name="Swamp to Cathedral Secret Legend Room Entrance", region="Swamp to Cathedral Treasure Room",
           destination="Cathedral Redux", tag="_secret", direction=Direction.south),  # feels a little weird
    Portal(name="Swamp to Gauntlet", region="Back of Swamp",
           destination="Cathedral Arena", tag="_", direction=Direction.north),
    Portal(name="Swamp Shop", region="Swamp Front",
           destination="Shop", tag="_", direction=Direction.north),
    Portal(name="Swamp Upper Exit", region="Back of Swamp Laurels Area",
           destination="Overworld Redux", tag="_wall", direction=Direction.north),
    Portal(name="Swamp Hero's Grave", region="Swamp Hero's Grave Region",
           destination="RelicVoid", tag="_teleporter_relic plinth", direction=Direction.floor),

    Portal(name="Cathedral Main Exit", region="Cathedral Entry",
           destination="Swamp Redux 2", tag="_main", direction=Direction.south),
    Portal(name="Cathedral Elevator", region="Cathedral to Gauntlet",
           destination="Cathedral Arena", tag="_", direction=Direction.ladder_down),  # elevators are ladders, right?
    Portal(name="Cathedral Secret Legend Room Exit", region="Cathedral Secret Legend Room",
           destination="Swamp Redux 2", tag="_secret", direction=Direction.north),

    Portal(name="Gauntlet to Swamp", region="Cathedral Gauntlet Exit",
           destination="Swamp Redux 2", tag="_", direction=Direction.south),
    Portal(name="Gauntlet Elevator", region="Cathedral Gauntlet Checkpoint",
           destination="Cathedral Redux", tag="_", direction=Direction.ladder_up),
    Portal(name="Gauntlet Shop", region="Cathedral Gauntlet Checkpoint",
           destination="Shop", tag="_", direction=Direction.east),

    Portal(name="Hero's Grave to Fortress", region="Hero Relic - Fortress",
           destination="Fortress Reliquary", tag="_teleporter_relic plinth", direction=Direction.floor),
    Portal(name="Hero's Grave to Monastery", region="Hero Relic - Quarry",
           destination="Monastery", tag="_teleporter_relic plinth", direction=Direction.floor),
    Portal(name="Hero's Grave to West Garden", region="Hero Relic - West Garden",
           destination="Archipelagos Redux", tag="_teleporter_relic plinth", direction=Direction.floor),
    Portal(name="Hero's Grave to East Forest", region="Hero Relic - East Forest",
           destination="Sword Access", tag="_teleporter_relic plinth", direction=Direction.floor),
    Portal(name="Hero's Grave to Library", region="Hero Relic - Library",
           destination="Library Hall", tag="_teleporter_relic plinth", direction=Direction.floor),
    Portal(name="Hero's Grave to Swamp", region="Hero Relic - Swamp",
           destination="Swamp Redux 2", tag="_teleporter_relic plinth", direction=Direction.floor),

    Portal(name="Far Shore to West Garden", region="Far Shore to West Garden Region",
           destination="Archipelagos Redux", tag="_teleporter_archipelagos_teleporter", direction=Direction.floor),
    Portal(name="Far Shore to Library", region="Far Shore to Library Region",
           destination="Library Lab", tag="_teleporter_library teleporter", direction=Direction.floor),
    Portal(name="Far Shore to Quarry", region="Far Shore to Quarry Region",
           destination="Quarry Redux", tag="_teleporter_quarry teleporter", direction=Direction.floor),
    Portal(name="Far Shore to East Forest", region="Far Shore to East Forest Region",
           destination="East Forest Redux", tag="_teleporter_forest teleporter", direction=Direction.floor),
    Portal(name="Far Shore to Fortress", region="Far Shore to Fortress Region",
           destination="Fortress Arena", tag="_teleporter_spidertank", direction=Direction.floor),
    Portal(name="Far Shore to Atoll", region="Far Shore",
           destination="Atoll Redux", tag="_teleporter_atoll", direction=Direction.floor),
    Portal(name="Far Shore to Ziggurat", region="Far Shore",
           destination="ziggurat2020_FTRoom", tag="_teleporter_ziggurat teleporter", direction=Direction.floor),
    Portal(name="Far Shore to Heir", region="Far Shore",
           destination="Spirit Arena", tag="_teleporter_spirit arena", direction=Direction.floor),
    Portal(name="Far Shore to Town", region="Far Shore",
           destination="Overworld Redux", tag="_teleporter_town", direction=Direction.floor),
    Portal(name="Far Shore to Spawn", region="Far Shore to Spawn Region",
           destination="Overworld Redux", tag="_teleporter_starting island", direction=Direction.floor),

    Portal(name="Heir Arena Exit", region="Spirit Arena",
           destination="Transit", tag="_teleporter_spirit arena", direction=Direction.floor),

    Portal(name="Purgatory Bottom Exit", region="Purgatory",
           destination="Purgatory", tag="_bottom", direction=Direction.south),
    Portal(name="Purgatory Top Exit", region="Purgatory",
           destination="Purgatory", tag="_top", direction=Direction.north),
]


class RegionInfo(NamedTuple):
    game_scene: str  # the name of the scene in the actual game
    dead_end: int = 0  # if a region has only one exit
    outlet_region: Optional[str] = None
    is_fake_region: bool = False


# gets the outlet region name if it exists, the region if it doesn't
def get_portal_outlet_region(portal: Portal, world: "TunicWorld") -> str:
    return world.er_regions[portal.region].outlet_region or portal.region


class DeadEnd(IntEnum):
    free = 0  # not a dead end
    all_cats = 1  # dead end in every logic category
    restricted = 2  # dead end only in restricted
    special = 3  # special handling for secret gathering place and zig skip exit
    # there's no dead ends that are only in unrestricted


# key is the AP region name. "Fake" in region info just means the mod won't receive that info at all
tunic_er_regions: Dict[str, RegionInfo] = {
    "Menu": RegionInfo("Fake", dead_end=DeadEnd.all_cats, is_fake_region=True),
    "Overworld": RegionInfo("Overworld Redux"),  # main overworld, the central area
    "Overworld Holy Cross": RegionInfo("Fake", dead_end=DeadEnd.all_cats, is_fake_region=True),  # main overworld holy cross checks
    "Overworld Belltower": RegionInfo("Overworld Redux"),  # the area with the belltower and chest
    "Overworld Belltower at Bell": RegionInfo("Overworld Redux"),  # being able to ring the belltower, basically
    "Overworld Swamp Upper Entry": RegionInfo("Overworld Redux"),  # upper swamp entry spot
    "Overworld Swamp Lower Entry": RegionInfo("Overworld Redux"),  # lower swamp entrance, rotating lights entrance
    "After Ruined Passage": RegionInfo("Overworld Redux"),  # just the door and chest
    "Above Ruined Passage": RegionInfo("Overworld Redux"),  # one ladder up from ruined passage
    "East Overworld": RegionInfo("Overworld Redux"),  # where the east forest and fortress entrances are
    "Overworld Special Shop Entry": RegionInfo("Overworld Redux"),  # special shop entry spot
    "Upper Overworld": RegionInfo("Overworld Redux"),  # where the mountain stairs are
    "Overworld above Quarry Entrance": RegionInfo("Overworld Redux"),  # top of the ladder where the chest is
    "Overworld after Temple Rafters": RegionInfo("Overworld Redux"),  # the ledge after the rafters exit, before ladder
    "Overworld Quarry Entry": RegionInfo("Overworld Redux"),  # at the top of the ladder, to darkwoods
    "Overworld after Envoy": RegionInfo("Overworld Redux"),  # after the envoy on the thin bridge to quarry
    "Overworld at Patrol Cave": RegionInfo("Overworld Redux"),  # right at the patrol cave entrance
    "Overworld above Patrol Cave": RegionInfo("Overworld Redux"),  # where the hook is, and one ladder up from patrol
    "Overworld West Garden Laurels Entry": RegionInfo("Overworld Redux"),  # west garden laurels entry
    "Overworld to West Garden Upper": RegionInfo("Overworld Redux"),  # usually leads to garden knight
    "Overworld to West Garden from Furnace": RegionInfo("Overworld Redux"),  # isolated stairway with one chest
    "Overworld Well Ladder": RegionInfo("Overworld Redux"),  # just the ladder entrance itself as a region
    "Overworld Well Entry Area": RegionInfo("Overworld Redux"),  # the page, the bridge, etc.
    "Overworld Tunnel to Beach": RegionInfo("Overworld Redux"),  # the tunnel with the chest
    "Overworld Beach": RegionInfo("Overworld Redux"),  # from the two turrets to invisble maze, and lower atoll entry
    "Overworld Tunnel Turret": RegionInfo("Overworld Redux"),  # the tunnel turret by the southwest beach ladder
    "Overworld to Atoll Upper": RegionInfo("Overworld Redux"),  # the little ledge before the ladder
    "Overworld Well to Furnace Rail": RegionInfo("Overworld Redux"),  # the rail hallway, bane of unrestricted logic
    "Overworld Ruined Passage Door": RegionInfo("Overworld Redux"),  # the small space betweeen the door and the portal
    "Overworld Old House Door": RegionInfo("Overworld Redux"),  # the too-small space between the door and the portal
    "Overworld Southeast Cross Door": RegionInfo("Overworld Redux"),  # the small space betweeen the door and the portal
    "Overworld Fountain Cross Door": RegionInfo("Overworld Redux", outlet_region="Overworld"),
    "Overworld Temple Door": RegionInfo("Overworld Redux"),  # the small space betweeen the door and the portal
    "Overworld Town Portal": RegionInfo("Overworld Redux", outlet_region="Overworld"),
    "Overworld Spawn Portal": RegionInfo("Overworld Redux", outlet_region="Overworld"),
    "Cube Cave Entrance Region": RegionInfo("Overworld Redux", outlet_region="Overworld"),  # other side of the bomb wall
    "Stick House": RegionInfo("Sword Cave", dead_end=DeadEnd.all_cats),
    "Windmill": RegionInfo("Windmill"),
    "Old House Back": RegionInfo("Overworld Interiors"),  # part with the hc door
    "Old House Front": RegionInfo("Overworld Interiors"),  # part with the bedroom
    "Relic Tower": RegionInfo("g_elements", dead_end=DeadEnd.all_cats),
    "Furnace Fuse": RegionInfo("Furnace"),  # top of the furnace
    "Furnace Ladder Area": RegionInfo("Furnace"),  # the two portals accessible by the ladder
    "Furnace Walking Path": RegionInfo("Furnace"),  # dark tomb to west garden
    "Secret Gathering Place": RegionInfo("Waterfall", dead_end=DeadEnd.special),
    "Changing Room": RegionInfo("Changing Room", dead_end=DeadEnd.all_cats),
    "Patrol Cave": RegionInfo("PatrolCave", dead_end=DeadEnd.all_cats),
    "Ruined Shop": RegionInfo("Ruined Shop", dead_end=DeadEnd.all_cats),
    "Ruined Passage": RegionInfo("Ruins Passage"),
    "Special Shop": RegionInfo("ShopSpecial", dead_end=DeadEnd.all_cats),
    "Caustic Light Cave": RegionInfo("Overworld Cave", dead_end=DeadEnd.all_cats),
    "Maze Cave": RegionInfo("Maze Room", dead_end=DeadEnd.all_cats),
    "Cube Cave": RegionInfo("CubeRoom", dead_end=DeadEnd.all_cats),
    "Southeast Cross Room": RegionInfo("EastFiligreeCache", dead_end=DeadEnd.all_cats),
    "Fountain Cross Room": RegionInfo("Town_FiligreeRoom", dead_end=DeadEnd.all_cats),
    "Hourglass Cave": RegionInfo("Town Basement", dead_end=DeadEnd.all_cats),
    "Hourglass Cave Tower": RegionInfo("Town Basement", dead_end=DeadEnd.all_cats),  # top of the tower
    "Sealed Temple": RegionInfo("Temple"),
    "Sealed Temple Rafters": RegionInfo("Temple"),
    "Forest Belltower Upper": RegionInfo("Forest Belltower"),
    "Forest Belltower Main": RegionInfo("Forest Belltower"),
    "Forest Belltower Main behind bushes": RegionInfo("Forest Belltower"),
    "Forest Belltower Lower": RegionInfo("Forest Belltower"),
    "East Forest": RegionInfo("East Forest Redux"),
    "East Forest Dance Fox Spot": RegionInfo("East Forest Redux"),
    "East Forest Portal": RegionInfo("East Forest Redux", outlet_region="East Forest"),
    "Lower Forest": RegionInfo("East Forest Redux"),  # bottom of the forest
    "Guard House 1 East": RegionInfo("East Forest Redux Laddercave"),
    "Guard House 1 West": RegionInfo("East Forest Redux Laddercave"),
    "Guard House 2 Upper before bushes": RegionInfo("East Forest Redux Interior"),
    "Guard House 2 Upper after bushes": RegionInfo("East Forest Redux Interior"),
    "Guard House 2 Lower": RegionInfo("East Forest Redux Interior"),
    "Forest Boss Room": RegionInfo("Forest Boss Room"),
    "Forest Grave Path Main": RegionInfo("Sword Access"),
    "Forest Grave Path Upper": RegionInfo("Sword Access"),
    "Forest Grave Path by Grave": RegionInfo("Sword Access"),
    "Forest Hero's Grave": RegionInfo("Sword Access", outlet_region="Forest Grave Path by Grave"),
    "Dark Tomb Entry Point": RegionInfo("Crypt Redux"),  # both upper exits
    "Dark Tomb Upper": RegionInfo("Crypt Redux"),  # the part with the casket and the top of the ladder
    "Dark Tomb Main": RegionInfo("Crypt Redux"),
    "Dark Tomb Dark Exit": RegionInfo("Crypt Redux"),
    "Dark Tomb Checkpoint": RegionInfo("Sewer_Boss"),
    "Well Boss": RegionInfo("Sewer_Boss"),
    "Beneath the Well Ladder Exit": RegionInfo("Sewer"),  # just the ladder
    "Beneath the Well Front": RegionInfo("Sewer"),  # the front, to separate it from the weapon requirement in the mid
    "Beneath the Well Main": RegionInfo("Sewer"),  # the main section of it, requires a weapon
    "Beneath the Well Back": RegionInfo("Sewer"),  # the back two portals, and all 4 upper chests
    "West Garden before Terry": RegionInfo("Archipelagos Redux"),  # the lower entry point, near hero grave
    "West Garden after Terry": RegionInfo("Archipelagos Redux"),  # after Terry, up until next chompignons
    "West Garden West Combat": RegionInfo("Archipelagos Redux"),  # for grass rando basically
    "West Garden at Dagger House": RegionInfo("Archipelagos Redux"),  # just outside magic dagger house
    "West Garden South Checkpoint": RegionInfo("Archipelagos Redux"),  # the checkpoint and the blue lines area
    "Magic Dagger House": RegionInfo("archipelagos_house", dead_end=DeadEnd.all_cats),
    "West Garden Portal": RegionInfo("Archipelagos Redux", dead_end=DeadEnd.restricted,
                                     outlet_region="West Garden by Portal"),
    "West Garden by Portal": RegionInfo("Archipelagos Redux", dead_end=DeadEnd.restricted),
    "West Garden Portal Item": RegionInfo("Archipelagos Redux", dead_end=DeadEnd.restricted),
    "West Garden Laurels Exit Region": RegionInfo("Archipelagos Redux"),
    "West Garden before Boss": RegionInfo("Archipelagos Redux"),  # up the ladder before garden knight
    "West Garden after Boss": RegionInfo("Archipelagos Redux"),
    "West Garden Hero's Grave Region": RegionInfo("Archipelagos Redux", outlet_region="West Garden before Terry"),
    "Ruined Atoll": RegionInfo("Atoll Redux"),
    "Ruined Atoll Lower Entry Area": RegionInfo("Atoll Redux"),
    "Ruined Atoll Ladder Tops": RegionInfo("Atoll Redux"),  # at the top of the 5 ladders in south Atoll
    "Ruined Atoll Frog Mouth": RegionInfo("Atoll Redux"),
    "Ruined Atoll Frog Eye": RegionInfo("Atoll Redux"),
    "Ruined Atoll Portal": RegionInfo("Atoll Redux", outlet_region="Ruined Atoll"),
    "Ruined Atoll Statue": RegionInfo("Atoll Redux", outlet_region="Ruined Atoll"),
    "Frog Stairs Eye Exit": RegionInfo("Frog Stairs"),
    "Frog Stairs Upper": RegionInfo("Frog Stairs"),
    "Frog Stairs Lower": RegionInfo("Frog Stairs"),
    "Frog Stairs to Frog's Domain": RegionInfo("Frog Stairs"),
    "Frog's Domain Entry": RegionInfo("frog cave main"),  # just the ladder
    "Frog's Domain Front": RegionInfo("frog cave main"),  # before combat
    "Frog's Domain Main": RegionInfo("frog cave main"),
    "Frog's Domain Back": RegionInfo("frog cave main"),
    "Library Exterior Tree Region": RegionInfo("Library Exterior", outlet_region="Library Exterior by Tree"),
    "Library Exterior by Tree": RegionInfo("Library Exterior"),
    "Library Exterior Ladder Region": RegionInfo("Library Exterior"),
    "Library Hall Bookshelf": RegionInfo("Library Hall"),
    "Library Hall": RegionInfo("Library Hall"),
    "Library Hero's Grave Region": RegionInfo("Library Hall", outlet_region="Library Hall"),
    "Library Hall to Rotunda": RegionInfo("Library Hall"),
    "Library Rotunda to Hall": RegionInfo("Library Rotunda"),
    "Library Rotunda": RegionInfo("Library Rotunda"),
    "Library Rotunda to Lab": RegionInfo("Library Rotunda"),
    "Library Lab": RegionInfo("Library Lab"),
    "Library Lab Lower": RegionInfo("Library Lab"),
    "Library Lab on Portal Pad": RegionInfo("Library Lab"),
    "Library Portal": RegionInfo("Library Lab", outlet_region="Library Lab on Portal Pad"),
    "Library Lab to Librarian": RegionInfo("Library Lab"),
    "Library Arena": RegionInfo("Library Arena", dead_end=DeadEnd.all_cats),
    "Fortress Exterior from East Forest": RegionInfo("Fortress Courtyard"),
    "Fortress Exterior from Overworld": RegionInfo("Fortress Courtyard"),
    "Fortress Exterior near cave": RegionInfo("Fortress Courtyard"),  # where the shop and beneath the earth entry are
    "Beneath the Vault Entry": RegionInfo("Fortress Courtyard"),
    "Fortress Courtyard": RegionInfo("Fortress Courtyard"),
    "Fortress Courtyard Upper": RegionInfo("Fortress Courtyard"),
    "Beneath the Vault Ladder Exit": RegionInfo("Fortress Basement"),
    "Beneath the Vault Main": RegionInfo("Fortress Basement"),  # the vanilla entry point
    "Beneath the Vault Back": RegionInfo("Fortress Basement"),  # the vanilla exit point
    "Eastern Vault Fortress": RegionInfo("Fortress Main"),
    "Eastern Vault Fortress Gold Door": RegionInfo("Fortress Main"),
    "Fortress East Shortcut Upper": RegionInfo("Fortress East"),
    "Fortress East Shortcut Lower": RegionInfo("Fortress East"),
    "Fortress Grave Path Entry": RegionInfo("Fortress Reliquary"),
    "Fortress Grave Path Combat": RegionInfo("Fortress Reliquary"),  # the combat is basically just a barrier here
    "Fortress Grave Path by Grave": RegionInfo("Fortress Reliquary"),
    "Fortress Grave Path Upper": RegionInfo("Fortress Reliquary", dead_end=DeadEnd.restricted),
    "Fortress Grave Path Dusty Entrance Region": RegionInfo("Fortress Reliquary"),
    "Fortress Hero's Grave Region": RegionInfo("Fortress Reliquary", outlet_region="Fortress Grave Path by Grave"),
    "Fortress Leaf Piles": RegionInfo("Dusty", dead_end=DeadEnd.all_cats),
    "Fortress Arena": RegionInfo("Fortress Arena"),
    "Fortress Arena Portal": RegionInfo("Fortress Arena", outlet_region="Fortress Arena"),
    "Lower Mountain": RegionInfo("Mountain"),
    "Lower Mountain Stairs": RegionInfo("Mountain"),
    "Top of the Mountain": RegionInfo("Mountaintop", dead_end=DeadEnd.all_cats),
    "Quarry Connector": RegionInfo("Darkwoods Tunnel"),
    "Quarry Entry": RegionInfo("Quarry Redux"),
    "Quarry": RegionInfo("Quarry Redux"),
    "Quarry Portal": RegionInfo("Quarry Redux", outlet_region="Quarry Entry"),
    "Quarry Back": RegionInfo("Quarry Redux"),
    "Quarry Monastery Entry": RegionInfo("Quarry Redux"),
    "Monastery Front": RegionInfo("Monastery"),
    "Monastery Back": RegionInfo("Monastery"),
    "Monastery Hero's Grave Region": RegionInfo("Monastery", outlet_region="Monastery Back"),
    "Monastery Rope": RegionInfo("Quarry Redux"),
    "Lower Quarry": RegionInfo("Quarry Redux"),
    "Even Lower Quarry": RegionInfo("Quarry Redux"),
    "Even Lower Quarry Isolated Chest": RegionInfo("Quarry Redux"),  # a region for that one chest
    "Lower Quarry Zig Door": RegionInfo("Quarry Redux"),
    "Rooted Ziggurat Entry": RegionInfo("ziggurat2020_0"),
    "Rooted Ziggurat Upper Entry": RegionInfo("ziggurat2020_1"),
    "Rooted Ziggurat Upper Front": RegionInfo("ziggurat2020_1"),
    "Rooted Ziggurat Upper Back": RegionInfo("ziggurat2020_1"),  # after the administrator
    "Rooted Ziggurat Middle Top": RegionInfo("ziggurat2020_2"),
    "Rooted Ziggurat Middle Bottom": RegionInfo("ziggurat2020_2"),
    "Rooted Ziggurat Lower Entry": RegionInfo("ziggurat2020_3"),  # the vanilla entry point side
    "Rooted Ziggurat Lower Front": RegionInfo("ziggurat2020_3"),  # the front for combat logic
    "Rooted Ziggurat Lower Mid Checkpoint": RegionInfo("ziggurat2020_3"),  # the mid-checkpoint before double admin
    "Rooted Ziggurat Lower Back": RegionInfo("ziggurat2020_3"),  # the boss side
    "Zig Skip Exit": RegionInfo("ziggurat2020_3", dead_end=DeadEnd.special, outlet_region="Rooted Ziggurat Lower Entry", is_fake_region=True),  # for use with fixed shop on
    "Rooted Ziggurat Portal Room Entrance": RegionInfo("ziggurat2020_3", outlet_region="Rooted Ziggurat Lower Back"),  # the door itself on the zig 3 side
    "Rooted Ziggurat Portal": RegionInfo("ziggurat2020_FTRoom", outlet_region="Rooted Ziggurat Portal Room"),
    "Rooted Ziggurat Portal Room": RegionInfo("ziggurat2020_FTRoom"),
    "Rooted Ziggurat Portal Room Exit": RegionInfo("ziggurat2020_FTRoom", outlet_region="Rooted Ziggurat Portal Room"),
    "Swamp Front": RegionInfo("Swamp Redux 2"),  # from the main entry to the top of the ladder after south
    "Swamp Mid": RegionInfo("Swamp Redux 2"),  # from the bottom of the ladder to the cathedral door
    "Swamp Ledge under Cathedral Door": RegionInfo("Swamp Redux 2"),  # the ledge with the chest and secret door
    "Swamp to Cathedral Treasure Room": RegionInfo("Swamp Redux 2", outlet_region="Swamp Ledge under Cathedral Door"),  # just the door
    "Swamp to Cathedral Main Entrance Region": RegionInfo("Swamp Redux 2"),  # just the door
    "Back of Swamp": RegionInfo("Swamp Redux 2"),  # the area with hero grave and gauntlet entrance
    "Swamp Hero's Grave Region": RegionInfo("Swamp Redux 2", outlet_region="Back of Swamp"),
    "Back of Swamp Laurels Area": RegionInfo("Swamp Redux 2"),  # the spots you need laurels to traverse
    "Cathedral Entry": RegionInfo("Cathedral Redux"),  # the checkpoint and easily-accessible chests
    "Cathedral Main": RegionInfo("Cathedral Redux"),  # the majority of Cathedral
    "Cathedral to Gauntlet": RegionInfo("Cathedral Redux"),  # the elevator
    "Cathedral Secret Legend Room": RegionInfo("Cathedral Redux", dead_end=DeadEnd.all_cats),
    "Cathedral Gauntlet Checkpoint": RegionInfo("Cathedral Arena"),
    "Cathedral Gauntlet": RegionInfo("Cathedral Arena"),
    "Cathedral Gauntlet Exit": RegionInfo("Cathedral Arena"),
    "Far Shore": RegionInfo("Transit"),
    "Far Shore to Spawn Region": RegionInfo("Transit"),
    "Far Shore to East Forest Region": RegionInfo("Transit"),
    "Far Shore to Quarry Region": RegionInfo("Transit", outlet_region="Far Shore"),
    "Far Shore to Fortress Region": RegionInfo("Transit", outlet_region="Far Shore"),
    "Far Shore to Library Region": RegionInfo("Transit", outlet_region="Far Shore"),
    "Far Shore to West Garden Region": RegionInfo("Transit", outlet_region="Far Shore"),
    "Hero Relic - Fortress": RegionInfo("RelicVoid", dead_end=DeadEnd.all_cats),
    "Hero Relic - Quarry": RegionInfo("RelicVoid", dead_end=DeadEnd.all_cats),
    "Hero Relic - West Garden": RegionInfo("RelicVoid", dead_end=DeadEnd.all_cats),
    "Hero Relic - East Forest": RegionInfo("RelicVoid", dead_end=DeadEnd.all_cats),
    "Hero Relic - Library": RegionInfo("RelicVoid", dead_end=DeadEnd.all_cats),
    "Hero Relic - Swamp": RegionInfo("RelicVoid", dead_end=DeadEnd.all_cats),
    "Purgatory": RegionInfo("Purgatory"),
    "Shop": RegionInfo("Shop", dead_end=DeadEnd.all_cats),
    "Spirit Arena": RegionInfo("Spirit Arena", dead_end=DeadEnd.all_cats),
    "Spirit Arena Victory": RegionInfo("Spirit Arena", dead_end=DeadEnd.all_cats, is_fake_region=True),
}


# this is essentially a pared down version of the region connections in rules.py, with some minor differences
# the main purpose of this is to make it so that you can access every region
# most items are excluded from the rules here, since we can assume Archipelago will properly place them
# laurels (hyperdash) can be locked at 10 fairies, requiring access to secret gathering place
# so until secret gathering place has been paired, you do not have hyperdash, so you cannot use hyperdash entrances
# Zip means you need the laurels zips option enabled
# IG# refers to ice grappling difficulties
# LS# refers to ladder storage difficulties
# LS rules are used for region connections here regardless of whether you have being knocked out of the air in logic
# this is because it just means you can reach the entrances in that region via ladder storage
traversal_requirements: Dict[str, Dict[str, List[List[str]]]] = {
    "Overworld": {
        "Overworld Beach":
            [],
        "Overworld Tunnel to Beach":
            [],
        "Overworld to Atoll Upper":
            [["Hyperdash"]],
        "Overworld Belltower":
            [["Hyperdash"], ["LS1"]],
        "Overworld Swamp Upper Entry":
            [["Hyperdash"], ["LS1"]],
        "Overworld Swamp Lower Entry":
            [],
        "Overworld Special Shop Entry":
            [["Hyperdash"], ["LS1"]],
        "Overworld Well Entry Area":
            [],
        "Overworld Ruined Passage Door":
            [],
        "After Ruined Passage":
            [],
        "Above Ruined Passage":
            [],
        "East Overworld":
            [],
        "Overworld above Patrol Cave":
            [],
        "Overworld above Quarry Entrance":
            [],
        "Overworld after Envoy":
            [],
        "Overworld Quarry Entry":
            [["IG2"], ["LS1"]],
        "Overworld Tunnel Turret":
            [["IG1"], ["LS1"], ["Hyperdash"]],
        "Overworld Temple Door":
            [["IG2"], ["LS3"], ["Forest Belltower Upper", "Overworld Belltower"]],
        "Overworld Southeast Cross Door":
            [],
        "Overworld Fountain Cross Door":
            [],
        "Overworld Town Portal":
            [],
        "Overworld Spawn Portal":
            [],
        "Overworld Well to Furnace Rail":
            [["LS2"]],
        "Overworld Old House Door":
            [],
        "Cube Cave Entrance Region":
            [],
        # drop a rudeling, icebolt or ice bomb
        "Overworld to West Garden from Furnace":
            [["IG3"], ["LS1"]],
    },
    "East Overworld": {
        "Above Ruined Passage":
            [],
        "After Ruined Passage":
            [["IG1"], ["LS1"]],
        # "Overworld":
        #     [],
        "Overworld at Patrol Cave":
            [],
        "Overworld above Patrol Cave":
            [],
        "Overworld Special Shop Entry":
            [["Hyperdash"], ["LS1"]]
    },
    "Overworld Special Shop Entry": {
        "East Overworld":
            [["Hyperdash"]]
    },
    "Overworld Belltower": {
        "Overworld Belltower at Bell":
            [],
        # "Overworld":
        #     [],
        "Overworld to West Garden Upper":
            [],
    },
    "Overworld to West Garden Upper": {
        "Overworld Belltower":
            [],
    },
    # "Overworld Swamp Upper Entry": {
    #     "Overworld":
    #         [],
    # },
    # "Overworld Swamp Lower Entry": {
    #     "Overworld":
    #         [],
    # },
    "Overworld Tunnel to Beach": {
        # "Overworld":
        #     [],
        "Overworld Beach":
            [],
    },
    "Overworld Beach": {
        # "Overworld":
        #     [],
        "Overworld West Garden Laurels Entry":
            [["Hyperdash"], ["LS1"]],
        "Overworld to Atoll Upper":
            [],
        "Overworld Tunnel Turret":
            [],
    },
    "Overworld West Garden Laurels Entry": {
        "Overworld Beach":
            [["Hyperdash"]],
    },
    "Overworld to Atoll Upper": {
        # "Overworld":
        #     [],
        "Overworld Beach":
            [],
    },
    "Overworld Tunnel Turret": {
        # "Overworld":
        #     [],
        "Overworld Beach":
            [],
    },
    "Overworld Well Entry Area": {
        # "Overworld":
        #     [],
        "Overworld Well Ladder":
            [],
    },
    "Overworld Well Ladder": {
        "Overworld Well Entry Area":
            [],
    },
    "Overworld at Patrol Cave": {
        "East Overworld":
            [["Hyperdash"], ["LS1"], ["IG1"]],
        "Overworld above Patrol Cave":
            [],
    },
    "Overworld above Patrol Cave": {
        # "Overworld":
        #     [],
        "East Overworld":
            [],
        "Upper Overworld":
            [],
        "Overworld at Patrol Cave":
            [],
        # readd long dong if we ever do a misc tricks option
    },
    "Upper Overworld": {
        "Overworld above Patrol Cave":
            [],
        "Overworld above Quarry Entrance":
            [],
        "Overworld after Temple Rafters":
            [],
    },
    "Overworld after Temple Rafters": {
        "Upper Overworld":
            [],
    },
    "Overworld above Quarry Entrance": {
        # "Overworld":
        #     [],
        "Upper Overworld":
            [],
    },
    "Overworld Quarry Entry": {
        "Overworld after Envoy":
            [],
        # "Overworld":
        #     [["IG1"]],
    },
    "Overworld after Envoy": {
        # "Overworld":
        #     [],
        "Overworld Quarry Entry":
            [],
    },
    "After Ruined Passage": {
        # "Overworld":
        #     [],
        "Above Ruined Passage":
            [],
    },
    "Above Ruined Passage": {
        # "Overworld":
        #     [],
        "After Ruined Passage":
            [],
        "East Overworld":
            [],
    },
    # "Overworld Ruined Passage Door": {
    #     "Overworld":
    #         [["Hyperdash", "Zip"]],
    # },
    # "Overworld Town Portal": {
    #     "Overworld":
    #         [],
    # },
    # "Overworld Spawn Portal": {
    #     "Overworld":
    #         [],
    # },
    "Cube Cave Entrance Region": {
        "Overworld":
            [],
    },

    "Old House Front": {
        "Old House Back":
            [],
    },
    "Old House Back": {
        "Old House Front":
            [["Hyperdash", "Zip"]],
    },

    "Furnace Fuse": {
        "Furnace Ladder Area":
            [["Hyperdash"]],
    },
    "Furnace Ladder Area": {
        "Furnace Fuse":
            [["Hyperdash"], ["LS1"]],
        "Furnace Walking Path":
            [["Hyperdash"], ["LS1"]],
    },
    "Furnace Walking Path": {
        "Furnace Ladder Area":
            [["Hyperdash"]],
    },

    "Sealed Temple": {
        "Sealed Temple Rafters":
            [],
    },
    "Sealed Temple Rafters": {
        "Sealed Temple":
            [["Hyperdash"]],
    },

    "Hourglass Cave": {
        "Hourglass Cave Tower":
            [],
    },

    "Forest Belltower Upper": {
        "Forest Belltower Main":
            [],
    },
    "Forest Belltower Main": {
        "Forest Belltower Lower":
            [],
        "Forest Belltower Main behind bushes":
            [],
    },
    "Forest Belltower Main behind bushes": {
        "Forest Belltower Main":
            [],
    },

    "East Forest": {
        "East Forest Dance Fox Spot":
            [["Hyperdash"], ["IG1"], ["LS1"]],
        "East Forest Portal":
            [],
        "Lower Forest":
            [],
    },
    "East Forest Dance Fox Spot": {
        "East Forest":
            [["Hyperdash"], ["IG1"]],
    },
    "East Forest Portal": {
        "East Forest":
            [],
    },
    "Lower Forest": {
        "East Forest":
            [],
    },

    "Guard House 1 East": {
        "Guard House 1 West":
            [],
    },
    "Guard House 1 West": {
        "Guard House 1 East":
            [["Hyperdash"], ["LS1"]],
    },
    "Guard House 2 Upper before bushes": {
        "Guard House 2 Upper after bushes":
            [],
    },
    "Guard House 2 Upper after bushes": {
        "Guard House 2 Lower":
            [],
        "Guard House 2 Upper before bushes":
            [],
    },
    "Guard House 2 Lower": {
        "Guard House 2 Upper after bushes":
            [],
    },

    "Forest Grave Path Main": {
        "Forest Grave Path Upper":
            [["Hyperdash"], ["LS2"], ["IG3"]],
        "Forest Grave Path by Grave":
            [],
    },
    "Forest Grave Path Upper": {
        "Forest Grave Path Main":
            [["Hyperdash"], ["IG1"]],
    },
    "Forest Grave Path by Grave": {
        "Forest Hero's Grave":
            [],
        "Forest Grave Path Main":
            [["IG1"]],
    },
    "Forest Hero's Grave": {
        "Forest Grave Path by Grave":
            [],
    },

    "Beneath the Well Ladder Exit": {
        "Beneath the Well Front":
            [],
    },
    "Beneath the Well Front": {
        "Beneath the Well Ladder Exit":
            [],
        "Beneath the Well Main":
            [],
    },
    "Beneath the Well Main": {
        "Beneath the Well Front":
            [],
        "Beneath the Well Back":
            [],
    },
    "Beneath the Well Back": {
        "Beneath the Well Main":
            [],
    },

    "Well Boss": {
        "Dark Tomb Checkpoint":
            [],
    },
    "Dark Tomb Checkpoint": {
        "Well Boss":
            [["Hyperdash", "Zip"]],
    },

    "Dark Tomb Entry Point": {
        "Dark Tomb Upper":
            [],
    },
    "Dark Tomb Upper": {
        "Dark Tomb Entry Point":
            [],
        "Dark Tomb Main":
            [],
    },
    "Dark Tomb Main": {
        "Dark Tomb Upper":
            [],
        "Dark Tomb Dark Exit":
            [],
    },
    "Dark Tomb Dark Exit": {
        "Dark Tomb Main":
            [],
    },

    "West Garden before Terry": {
        "West Garden after Terry":
            [],
        "West Garden Hero's Grave Region":
            [],
    },
    "West Garden Hero's Grave Region": {
        "West Garden before Terry":
            [],
    },
    "West Garden after Terry": {
        "West Garden before Terry":
            [],
        "West Garden West Combat":
            [],
        "West Garden South Checkpoint":
            [["Hyperdash"]],
        "West Garden Laurels Exit Region":
            [["LS1"]],
    },
    "West Garden South Checkpoint": {
        "West Garden before Boss":
            [],
        "West Garden at Dagger House":
            [],
        "West Garden after Terry":
            [["Hyperdash"]],
        "West Garden West Combat":
            [],
    },
    "West Garden before Boss": {
        "West Garden after Boss":
            [],
        "West Garden South Checkpoint":
            [],
    },
    "West Garden after Boss": {
        "West Garden before Boss":
            [["Hyperdash"]],
    },
    "West Garden at Dagger House": {
        "West Garden Laurels Exit Region":
            [["Hyperdash"]],
        "West Garden South Checkpoint":
            [],
        "West Garden Portal Item":
            [["IG2"]],
    },
    "West Garden Laurels Exit Region": {
        "West Garden at Dagger House":
            [["Hyperdash"]],
    },
    "West Garden Portal Item": {
        "West Garden at Dagger House":
            [["IG1"]],
        "West Garden by Portal":
            [["Hyperdash"]],
    },
    "West Garden by Portal": {
        "West Garden Portal":
            [["West Garden South Checkpoint"]],
        "West Garden Portal Item":
            [["Hyperdash"]],
    },
    "West Garden Portal": {
        "West Garden by Portal":
            [],
    },

    "Ruined Atoll": {
        "Ruined Atoll Lower Entry Area":
            [["Hyperdash"], ["LS1"]],
        "Ruined Atoll Ladder Tops":
            [],
        "Ruined Atoll Frog Mouth":
            [],
        "Ruined Atoll Frog Eye":
            [],
        "Ruined Atoll Portal":
            [],
        "Ruined Atoll Statue":
            [],
    },
    "Ruined Atoll Lower Entry Area": {
        "Ruined Atoll":
            [],
    },
    "Ruined Atoll Ladder Tops": {
        "Ruined Atoll":
            [],
    },
    "Ruined Atoll Frog Mouth": {
        "Ruined Atoll":
            [],
    },
    "Ruined Atoll Frog Eye": {
        "Ruined Atoll":
            [],
    },
    "Ruined Atoll Portal": {
        "Ruined Atoll":
            [],
    },
    "Ruined Atoll Statue": {
        "Ruined Atoll":
            [],
    },

    "Frog Stairs Eye Exit": {
        "Frog Stairs Upper":
            [],
    },
    "Frog Stairs Upper": {
        "Frog Stairs Eye Exit":
            [],
        "Frog Stairs Lower":
            [],
    },
    "Frog Stairs Lower": {
        "Frog Stairs Upper":
            [],
        "Frog Stairs to Frog's Domain":
            [],
    },
    "Frog Stairs to Frog's Domain": {
        "Frog Stairs Lower":
            [],
    },

    "Frog's Domain Entry": {
        "Frog's Domain Front":
            [],
    },
    "Frog's Domain Front": {
        "Frog's Domain Entry":
            [],
        "Frog's Domain Main":
            [],
    },
    "Frog's Domain Main": {
        "Frog's Domain Front":
            [],
        "Frog's Domain Back":
            [],
    },

    "Library Exterior Ladder Region": {
        "Library Exterior by Tree":
            [],
    },
    "Library Exterior by Tree": {
        "Library Exterior Tree Region":
            [],
        "Library Exterior Ladder Region":
            [],
    },
    "Library Exterior Tree Region": {
        "Library Exterior by Tree":
            [],
    },

    "Library Hall Bookshelf": {
        "Library Hall":
            [],
    },
    "Library Hall": {
        "Library Hall Bookshelf":
            [],
        "Library Hero's Grave Region":
            [],
        "Library Hall to Rotunda":
            [],
    },
    "Library Hero's Grave Region": {
        "Library Hall":
            [],
    },
    "Library Hall to Rotunda": {
        "Library Hall":
            [],
    },

    "Library Rotunda to Hall": {
        "Library Rotunda":
            [],
    },
    "Library Rotunda": {
        "Library Rotunda to Hall":
            [],
        "Library Rotunda to Lab":
            [],
    },
    "Library Rotunda to Lab": {
        "Library Rotunda":
            [],
    },

    "Library Lab Lower": {
        "Library Lab":
            [],
    },
    "Library Lab": {
        "Library Lab Lower":
            [["Hyperdash"]],
        "Library Lab on Portal Pad":
            [],
        "Library Lab to Librarian":
            [],
    },
    "Library Lab on Portal Pad": {
        "Library Portal":
            [],
        "Library Lab":
            [],
    },
    "Library Portal": {
        "Library Lab on Portal Pad":
            [],
    },
    "Library Lab to Librarian": {
        "Library Lab":
            [],
    },

    "Fortress Exterior from East Forest": {
        "Fortress Exterior from Overworld":
            [],
        "Fortress Courtyard Upper":
            [["LS2"]],
        "Fortress Courtyard":
            [["LS1"]],
    },
    "Fortress Exterior from Overworld": {
        "Fortress Exterior from East Forest":
            [["Hyperdash"]],
        "Fortress Exterior near cave":
            [],
        "Fortress Courtyard":
            [["Hyperdash"], ["IG1"], ["LS1"]],
    },
    "Fortress Exterior near cave": {
        "Fortress Exterior from Overworld":
            [["Hyperdash"], ["LS1"]],
        "Fortress Courtyard":  # ice grapple hard: shoot far fire pot, it aggros one of the enemies over to you
            [["IG3"], ["LS1"]],
        "Fortress Courtyard Upper":
            [["LS2"]],
        "Beneath the Vault Entry":
            [],
    },
    "Beneath the Vault Entry": {
        "Fortress Exterior near cave":
            [],
    },
    "Fortress Courtyard": {
        "Fortress Courtyard Upper":
            [["IG1"]],
        "Fortress Exterior from Overworld":
            [["Hyperdash"]],
    },
    "Fortress Courtyard Upper": {
        "Fortress Courtyard":
            [],
    },

    "Beneath the Vault Ladder Exit": {
        "Beneath the Vault Main":
            [],
    },
    "Beneath the Vault Main": {
        "Beneath the Vault Ladder Exit":
            [],
        "Beneath the Vault Back":
            [],
    },
    "Beneath the Vault Back": {
        "Beneath the Vault Main":
            [],
        "Beneath the Vault Ladder Exit":
            [],
    },

    "Fortress East Shortcut Lower": {
        "Fortress East Shortcut Upper":
            [["IG1"]],
    },
    "Fortress East Shortcut Upper": {
        "Fortress East Shortcut Lower":
            [],
    },

    "Eastern Vault Fortress": {
        "Eastern Vault Fortress Gold Door":
            [["IG2"], ["Fortress Exterior from Overworld", "Beneath the Vault Back", "Fortress Courtyard Upper"]],
    },
    "Eastern Vault Fortress Gold Door": {
        "Eastern Vault Fortress":
            [["IG1"]],
    },

    "Fortress Grave Path Entry": {
        "Fortress Grave Path Combat":
            [],
        # redundant here, keeping a comment to show it's intentional
        # "Fortress Grave Path Dusty Entrance Region":
        #     [["Hyperdash"]],
    },
    "Fortress Grave Path Combat": {
        "Fortress Grave Path Entry":
            [],
        "Fortress Grave Path by Grave":
            [],
    },
    "Fortress Grave Path by Grave": {
        "Fortress Grave Path Entry":
            [],
        # unnecessary, you can just skip it
        # "Fortress Grave Path Combat":
        #     [],
        "Fortress Hero's Grave Region":
            [],
        "Fortress Grave Path Dusty Entrance Region":
            [["Hyperdash"]],
    },
    "Fortress Grave Path Upper": {
        "Fortress Grave Path Entry":
            [["IG1"]],
    },
    "Fortress Grave Path Dusty Entrance Region": {
        "Fortress Grave Path by Grave":
            [["Hyperdash"]],
    },
    "Fortress Hero's Grave Region": {
        "Fortress Grave Path by Grave":
            [],
    },

    "Fortress Arena": {
        "Fortress Arena Portal":
            [["Fortress Exterior from Overworld", "Beneath the Vault Back", "Eastern Vault Fortress"]],
    },
    "Fortress Arena Portal": {
        "Fortress Arena":
            [],
    },

    "Lower Mountain": {
        "Lower Mountain Stairs":
            [],
    },
    "Lower Mountain Stairs": {
        "Lower Mountain":
            [],
    },

    "Monastery Back": {
        "Monastery Front":
            [["Hyperdash", "Zip"]],
        "Monastery Hero's Grave Region":
            [],
    },
    "Monastery Hero's Grave Region": {
        "Monastery Back":
            [],
    },
    "Monastery Front": {
        "Monastery Back":
            [],
    },

    "Quarry Entry": {
        "Quarry Portal":
            [["Quarry Connector"]],
        "Quarry":
            [],
        "Monastery Rope":
            [["LS2"]],
    },
    "Quarry Portal": {
        "Quarry Entry":
            [],
    },
    "Quarry Monastery Entry": {
        "Quarry":
            [],
        "Quarry Back":
            [["Hyperdash"]],
        "Monastery Rope":
            [["LS2"]],
    },
    "Quarry Back": {
        "Quarry":
            [],
        "Quarry Monastery Entry":
            [["Hyperdash"]],
    },
    "Quarry": {
        "Lower Quarry":
            [],
        "Quarry Entry":
            [],
        "Quarry Back":
            [],
        "Quarry Monastery Entry":
            [],
    },
    "Lower Quarry": {
        "Even Lower Quarry":
            [],
    },
    "Even Lower Quarry": {
        "Even Lower Quarry Isolated Chest":
            [],
    },
    "Even Lower Quarry Isolated Chest": {
        "Even Lower Quarry":
            [],
        "Lower Quarry Zig Door":
            [["Quarry", "Quarry Connector"], ["IG3"]],
    },
    "Monastery Rope": {
        "Quarry Back":
            [],
    },

    "Rooted Ziggurat Upper Entry": {
        "Rooted Ziggurat Upper Front":
            [],
    },
    "Rooted Ziggurat Upper Front": {
        "Rooted Ziggurat Upper Back":
            [],
    },
    "Rooted Ziggurat Upper Back": {
        "Rooted Ziggurat Upper Front":
            [["Hyperdash"]],
    },

    "Rooted Ziggurat Middle Top": {
        "Rooted Ziggurat Middle Bottom":
            [],
    },

    "Rooted Ziggurat Lower Entry": {
        "Rooted Ziggurat Lower Front":
            [],
        # can zip through to the checkpoint
        "Rooted Ziggurat Lower Mid Checkpoint":
            [["Hyperdash"]],
    },
    "Rooted Ziggurat Lower Front": {
        "Rooted Ziggurat Lower Entry":
            [],
        "Rooted Ziggurat Lower Mid Checkpoint":
            [],
    },
    "Rooted Ziggurat Lower Mid Checkpoint": {
        "Rooted Ziggurat Lower Entry":
            [["Hyperdash"]],
        "Rooted Ziggurat Lower Front":
            [],
        "Rooted Ziggurat Lower Back":
            [],
    },
    "Rooted Ziggurat Lower Back": {
        "Rooted Ziggurat Lower Entry":
            [["LS2"]],
        "Rooted Ziggurat Lower Mid Checkpoint":
            [["Hyperdash"], ["IG1"]],
        "Rooted Ziggurat Portal Room Entrance":
            [],
    },
    "Rooted Ziggurat Portal Room Entrance": {
        "Rooted Ziggurat Lower Back":
            [],
    },

    "Rooted Ziggurat Portal Room Exit": {
        "Rooted Ziggurat Portal Room":
            [],
    },
    "Rooted Ziggurat Portal Room": {
        "Rooted Ziggurat Portal Room Exit":
            [["Rooted Ziggurat Lower Back"]],
        "Rooted Ziggurat Portal":
            [],
    },
    "Rooted Ziggurat Portal": {
        "Rooted Ziggurat Portal Room":
            [],
    },

    "Swamp Front": {
        "Swamp Mid":
            [],
        # get one pillar from the gate, then dash onto the gate, very tricky
        "Back of Swamp Laurels Area":
            [["Hyperdash", "Zip"]],
    },
    "Swamp Mid": {
        "Swamp Front":
            [],
        "Swamp to Cathedral Main Entrance Region":
            [["Hyperdash"], ["IG2"], ["LS3"]],
        "Swamp Ledge under Cathedral Door":
            [],
        "Back of Swamp":
            [["LS1"]],  # ig3 later?
    },
    "Swamp Ledge under Cathedral Door": {
        "Swamp Mid":
            [],
        "Swamp to Cathedral Treasure Room":
            [],
    },
    "Swamp to Cathedral Treasure Room": {
        "Swamp Ledge under Cathedral Door":
            [],
    },
    "Swamp to Cathedral Main Entrance Region": {
        "Swamp Mid":
            [["IG1"]],
    },
    "Back of Swamp": {
        "Back of Swamp Laurels Area":
            [["Hyperdash"], ["LS2"]],
        "Swamp Hero's Grave Region":
            [],
        "Swamp Mid":
            [["LS2"]],
        "Swamp Front":
            [["LS1"]],
        "Swamp to Cathedral Main Entrance Region":
            [["LS3"]],
        "Swamp to Cathedral Treasure Room":
            [["LS3"]]
    },
    "Back of Swamp Laurels Area": {
        "Back of Swamp":
            [["Hyperdash"]],
        # get one pillar from the gate, then dash onto the gate, very tricky
        "Swamp Mid":
            [["IG1", "Hyperdash"], ["Hyperdash", "Zip"]],
    },
    "Swamp Hero's Grave Region": {
        "Back of Swamp":
            [],
    },

    "Cathedral Entry": {
        "Cathedral to Gauntlet":
            [],
        "Cathedral Main":
            [],
    },
    "Cathedral Main": {
        "Cathedral Entry":
            [],
        "Cathedral to Gauntlet":
            [],
    },
    "Cathedral to Gauntlet": {
        "Cathedral Entry":
            [],
        "Cathedral Main":
            [],
    },

    "Cathedral Gauntlet Checkpoint": {
        "Cathedral Gauntlet":
            [],
    },
    "Cathedral Gauntlet": {
        "Cathedral Gauntlet Exit":
            [["Hyperdash"]],
    },
    "Cathedral Gauntlet Exit": {
        "Cathedral Gauntlet":
            [["Hyperdash"]],
    },

    "Far Shore": {
        "Far Shore to Spawn Region":
            [["Hyperdash"]],
        "Far Shore to East Forest Region":
            [["Hyperdash"]],
        "Far Shore to Quarry Region":
            [["Quarry Connector", "Quarry"]],
        "Far Shore to Library Region":
            [["Library Lab"]],
        "Far Shore to West Garden Region":
            [["West Garden South Checkpoint"]],
        "Far Shore to Fortress Region":
            [["Fortress Exterior from Overworld", "Beneath the Vault Back", "Eastern Vault Fortress"]],
    },
    "Far Shore to Spawn Region": {
        "Far Shore":
            [["Hyperdash"]],
    },
    "Far Shore to East Forest Region": {
        "Far Shore":
            [["Hyperdash"]],
    },
    "Far Shore to Quarry Region": {
        "Far Shore":
            [],
    },
    "Far Shore to Library Region": {
        "Far Shore":
            [],
    },
    "Far Shore to West Garden Region": {
        "Far Shore":
            [],
    },
    "Far Shore to Fortress Region": {
        "Far Shore":
            [],
    },
}
