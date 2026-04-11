from typing import TYPE_CHECKING

from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames
from ..Rules import has_soup_ingerdients, moon_cave_fire_rule, moon_cave_fire_rule_4f
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.MOON_CAVE_BROKEN_STAIRS: [ExitData("Jump into the hole", RegionNames.MOON_CAVE_UNDERGROUND_ENTRANCE)],
    RegionNames.MOON_CAVE_UNDERGROUND_ENTRANCE: [ExitData("To Calcified Cavern", RegionNames.CALCIFIED_CAVERN)],
    RegionNames.MOON_CAVE: [ExitData("Enter 1F Locked Cave", RegionNames.MOON_CAVE_1F_LOCKED_CAVE,
                                     has_events=["Moon Cave - 1F Free Ajimi from soup"]),
                            ExitData("Moon Cave - Take lift to B2F", RegionNames.MOON_CAVE_B2F_LIFT,
                                     has_events=["Moon Cave - 1F Main room disturb lift"]),
                            ExitData("Moon Cave - Access Kitchen Back", RegionNames.MOON_CAVE_KITCHEN_BACK),
                            ExitData("Moon Cave - lift to Orochi", RegionNames.MOON_CAVE_OROCHI,has_events=["Moon Cave - 1F Give all ingredients to Ajimi"])],
    RegionNames.MOON_CAVE_1F_LOCKED_CAVE: [ExitData("To 1F locked cave back", RegionNames.MOON_CAVE_1F_LOCKED_CAVE_BACK,
                                                    has_events=['Moon Cave - 1F Locked Cave open eye door']),
                                           ExitData("To 2F geyser rafters", RegionNames.MOON_CAVE_2F_GEYSER_RAFTER,
                                                    has_events=["Moon Cave - 1F Locked Cave geyser"])],
    RegionNames.MOON_CAVE_2F_GEYSER_RAFTER: [
        ExitData("To 2F main", RegionNames.MOON_CAVE_2F, has_events=["Moon cave - 2F rafter's geyser"])],
    RegionNames.MOON_CAVE_2F: [ExitData("Moon Cave - Fall Down 2F bridge", RegionNames.MOON_CAVE_B1F_LAKE),
                               ExitData("Moon Cave - To 2F Ice Eye", RegionNames.MOON_CAVE_2F_FIRE_EYE,
                                        has_events=["Moon Cave - 2F Melt Ice block after bridge"]),
                               ExitData("Moon Cave - To 2F sand room", RegionNames.MOON_CAVE_2F_SAND,
                                        has_events=["Moon Cave - 2F Open door to Sand room"])
                               ],
    RegionNames.MOON_CAVE_B1F_LAKE: [ExitData("Moon Cave - Climb to under lift", RegionNames.MOON_CAVE_B1F_UNDER_LIFT,
                                              has_events=["Moon Cave - B1F Lake geyser"])],
    RegionNames.MOON_CAVE_B1F_UNDER_LIFT: [ExitData("Moon Cave - Climb to main room", RegionNames.MOON_CAVE,
                                                    has_events=["Moon Cave - B1F under lift geyser"])],
    RegionNames.MOON_CAVE_B2F_LIFT: [
        ExitData("Moon Cave - Enter Frozen Statue room", RegionNames.MOON_CAVE_B2F_FROZEN_STATUE,
                 has_events=["Moon Cave - B2F oepn eyes door"])],
    RegionNames.MOON_CAVE_B2F_FROZEN_STATUE: [
        ExitData("Moon Cave - To B2F lift back", RegionNames.MOON_CAVE_B2F_OTHER_LIFT,
                 has_events=["Moon Cave - B2F Melt Ice block to other lift"])],
    RegionNames.MOON_CAVE_B2F_OTHER_LIFT: [
        ExitData("Moon Cave - to B2F room beihnd bombable wall", RegionNames.MOON_CAVE_B2F_BOMBABLE,
                 has_events=["Moon Cave - B2F Explode wall behind lift"]),
        ExitData("Moon Cave - Take lift back to kitchen", RegionNames.MOON_CAVE_KITCHEN_BACK)
    ],
    RegionNames.MOON_CAVE_2F_SAND: [ExitData("Moon Cave - to 2F/3F Rafters", RegionNames.MOON_CAVE_2F_3F_RAFTERS,
                                             has_events=["Moon Cave - 2F Push the ball"])],
    RegionNames.MOON_CAVE_2F_3F_RAFTERS: [ExitData("Moon Cave - to 4F rafters", RegionNames.MOON_CAVE_4F_RAFTERS,
                                                   has_events=["Moon Cave - 3F Rafters use flower"])],
    RegionNames.MOON_CAVE_4F_RAFTERS: [ExitData("Moon Cave - to 4F canon", RegionNames.MOON_CAVE_4F_CANON,
                                                has_events=["Moon Cave - 4F Rafters cross banners"]),
                                       ExitData("Moon Cave - 4f behind the blown up wall",
                                                RegionNames.MOON_CAVE_4F_AFTER_CANON,
                                                has_events=["Moon Cave - 4F Mandatory Fight"])]
}
events = {
    RegionNames.MOON_CAVE: {
        "Moon Cave - 1F Free Ajimi from soup": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),
        "Moon Cave - 1F Main room geyser": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT],
                                                     special_rule=lambda s, w: has_soup_ingerdients(s, w, 1)),
        "Moon Cave - 1F Main room disturb lift": EventData(power_slash_level=1,
                                                           required_items_events=["Moon Cave - B1F Open lift hatch"]),
        "Moon Cave - 1F Melt Kitchen Ice from front": EventData(required_brush_techniques=[BrushTechniques.INFERNO],
                                                                event_item_name="Moon Cave - Melt Kicthen Ice"),
        "Moon Cave - 1F Blue Flower to 2F accessible": EventData(
            special_rule=lambda s, w: has_soup_ingerdients(s, w, 2)),
        "Moon Cave - 1F Give all ingredients to Ajimi": EventData(
            special_rule=lambda s, w: has_soup_ingerdients(s, w, 4))
    },
    RegionNames.MOON_CAVE_1F_LOCKED_CAVE: {
        "Moon Cave - Cross 1F Locked Cave": EventData(required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),
        "Moon Cave - 1F Locked Cave Blow up wall": EventData(cherry_bomb_level=1),
        "Moon Cave - 1F Locked Cave open eye door": EventData(power_slash_level=1, required_items_events=[
            "Moon Cave - Cross 1F Locked Cave"]),
        # Does this require Ogre Liver ?
        "Moon Cave - 1F Locked Cave geyser": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT]),
    },
    RegionNames.MOON_CAVE_1F_LOCKED_CAVE_BACK: {
        "Moon Cave - Mandatory Ogre Encounter": EventData(mandatory_enemies=[]),
        "Moon Cave - Get Ogre Liver": EventData(event_item_name="Ogre Liver")
    },
    RegionNames.MOON_CAVE_2F_GEYSER_RAFTER: {
        "Moon cave - 2F rafter's geyser": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT])
    },
    RegionNames.MOON_CAVE_2F: {
        "Moon Cave - 2F repair Bridge": EventData(required_brush_techniques=[BrushTechniques.REJUVENATION]),
        "Moon Cave - 2F Melt Ice block after bridge": EventData(required_brush_techniques=[BrushTechniques.INFERNO],
                                                                required_items_events=["Moon Cave - 2F repair Bridge"]),
        "Moon Cave - 2F Open door to Sand room": EventData(
            required_items_events=["Moon Cave - 2F Cursed Fire Eye Torii"])
    },
    RegionNames.MOON_CAVE_B1F_LAKE: {
        # FIXME: Fill ennemies
        "Moon Cave - B1F Lake cursed Torii": EventData(mandatory_enemies=[]),
        "Moon Cave - B1F Lake open valve": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT]),
        "Moon Cave - B1F Lake geyser": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT],
                                                 required_items_events=["Moon Cave - B1F Lake open valve"]),
    },
    RegionNames.MOON_CAVE_B1F_UNDER_LIFT: {
        "Moon Cave - B1F Open lift hatch": EventData(power_slash_level=1),
        "Moon Cave - B1F under lift geyser": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT])
    },
    RegionNames.MOON_CAVE_B2F_LIFT: {
        "Moon Cave - B2F oepn eyes door": EventData(power_slash_level=1)
    },
    RegionNames.MOON_CAVE_B2F_FROZEN_STATUE: {
        "Moon Cave - B2F Defeat Ice Lips": EventData(mandatory_enemies=[]),
        "Moon Cave - B2F Melt Ice block to other lift": EventData(required_brush_techniques=[BrushTechniques.INFERNO])
    },
    RegionNames.MOON_CAVE_B2F_OTHER_LIFT: {
        "Moon Cave - B2F Melt Ice Block behind lift": EventData(required_brush_techniques=[BrushTechniques.INFERNO]),
        "Moon Cave - B2F Explode wall behind lift": EventData(cherry_bomb_level=1, required_items_events=[
            "Moon Cave - B2F Melt Ice Block behind lift"])
    },
    RegionNames.MOON_CAVE_KITCHEN_BACK: {
        "Moon Cave - 1F Cursed Door in kitchen back": EventData(mandatory_enemies=[]),
        "Moon Cave - 1F Get Ice Lips": EventData(required_items_events=["Moon Cave - 1F Cursed Door in kitchen back"],
                                                 event_item_name="Ice Lips"),
        # Can be done from the other way too;
        "Moon Cave - 1F Melt Ice kitchen Ice form behind": EventData(
            required_brush_techniques=[BrushTechniques.INFERNO], event_item_name="Moon Cave - Melt Kicthen Ice")
    },
    RegionNames.MOON_CAVE_2F_FIRE_EYE: {
        "Moon Cave - 2F Cursed Fire Eye Torii": EventData(mandatory_enemies=[OkamiEnemies.FIRE_EYE]),
        "Moon Cave - 2F Get Fire Eye": EventData(required_items_events=["Moon Cave - 2F Cursed Fire Eye Torii"],
                                                 event_item_name="Fire Eye")
    },
    RegionNames.MOON_CAVE_2F_SAND: {
        # Pretty sure the invisible part of the path isn't solid when it's invisible
        # Lights the fireball torches in this dungeon
        "Moon Cave - 2F Push the ball": EventData(required_brush_techniques=[BrushTechniques.GALESTORM]),
    },
    RegionNames.MOON_CAVE_2F_3F_RAFTERS: {
        "Moon Cave - 3F Rafters use flower": EventData(required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE])
    },
    RegionNames.MOON_CAVE_4F_RAFTERS: {
        "Moon Cave - 4F Rafters cross banners": EventData(required_brush_techniques=[BrushTechniques.GALESTORM])
    },
    RegionNames.MOON_CAVE_4F_CANON: {
        "Moon Cave - 4F Fire the canon!": EventData(required_brush_techniques=[BrushTechniques.INFERNO],special_rule=lambda s, w: moon_cave_fire_rule(s, w)),
        # FIXME: Add enemies
        "Moon Cave - 4F Mandatory Fight": EventData(mandatory_enemies=[],
                                                    required_items_events=['Moon Cave - 4F Fire the canon!']),
    },
    RegionNames.MOON_CAVE_4F_AFTER_CANON: {
        "Moon Cave - 4F Move Fireball": EventData(required_brush_techniques=[BrushTechniques.GALESTORM]),
        "Moon Cave - 4F Melt Ice Blocks": EventData(required_brush_techniques=[BrushTechniques.INFERNO],special_rule=lambda s, w: moon_cave_fire_rule_4f(s, w)),
        "Moon Cave - 4F Black Demon Horn Torii": EventData(mandatory_enemies=[],
                                                           required_items_events=["Moon Cave - 4F Melt Ice Blocks"]),
        "Moon Cave - 4F Get Black Demon Horn": EventData(
            required_items_events=["Moon Cave - 4F Black Demon Horn Torii"], event_item_name="Black Demon Horn")
    },
    RegionNames.MOON_CAVE_OROCHI: {
        "Moon Cave - Defeat Orochi": EventData(mandatory_enemies=[OkamiEnemies.OROCHI_1],
                                               required_brush_techniques=[BrushTechniques.CRESCENT],
                                               power_slash_level=1)
    }
}
#TODO: Check basment chest, there's probably one or two missing
locations = {
    RegionNames.MOON_CAVE: {
        "Moon Cave - 1F Chest on ledge in the kitchen": LocData(969640),
        "Moon Cave - 1F Frozen Chest after 3 ingredients": LocData(969639, type=LocationType.FROZEN_CHEST, special_rule=
            lambda s, w: has_soup_ingerdients(s, w, 3) ),
        "Moon Cave - 1F Chest after 4 ingredients": LocData(969642,
                                                            special_rule=(lambda s, w: has_soup_ingerdients(s, w, 4))),
    },
    RegionNames.MOON_CAVE_1F_LOCKED_CAVE: {
        "Moon Cave - 1F locked cave Treasure bud behind bombable wall": LocData(176, type=LocationType.TREASURE_BUD)
    },
    RegionNames.MOON_CAVE_B2F_LIFT: {
        "Moon Cave - B2F Chest on ledge near eyes door": LocData(969647)
    },
    RegionNames.MOON_CAVE_B2F_FROZEN_STATUE: {
        "Moon Cave - Moegami": LocData(200010, type=LocationType.CONSTELLATION)  # bit 10
    },
    RegionNames.MOON_CAVE_B2F_BOMBABLE: {
        "Moon Cave - B2F Chest behind bombable wall": LocData(969636)
    },
    RegionNames.MOON_CAVE_2F_SAND: {
        # Made this logically require cherry bomb as it's required to exit this area.
        "Moon Cave - 2F Chest in sand pit": LocData(969648, cherry_bomb_level=1),
        "Moon Cave - 2F Map Chest after ball puzzle": LocData(969637)
    },
    RegionNames.MOON_CAVE_2F_3F_RAFTERS: {
        "Moon Cave - 3F Frozen Chest near merchant": LocData(969644, type=LocationType.FROZEN_CHEST, special_rule=lambda s, w: moon_cave_fire_rule(s, w)),
        "Moon Cave - 2F Rafters Chest under 3F Rafters": LocData(969643),
    },
    RegionNames.MOON_CAVE_2F_FIRE_EYE: {
        "Moon Cave - 2F Left Frozen Chest after Fire eye room": LocData(969651,
                                                                        type=LocationType.FROZEN_CHEST,
                                                                        special_rule=lambda s, w: moon_cave_fire_rule(s,
                                                                                                                      w)),
        "Moon Cave - 2F Middle Frozen Chest after Fire eye room": LocData(969649,
                                                                          type=LocationType.FROZEN_CHEST,
                                                                          special_rule=lambda s, w: moon_cave_fire_rule(s,
                                                                                                                      w)),
        "Moon Cave - 2F Right Frozen Chest after Fire eye room": LocData(969650,
                                                                         type=LocationType.FROZEN_CHEST,
                                                                         special_rule=lambda s, w: moon_cave_fire_rule(s,
                                                                                                                      w)),
    },
    RegionNames.MOON_CAVE_4F_AFTER_CANON: {
        "Moon Cave - 4F Lower ledge Frozen Chest": LocData(969652, type=LocationType.FROZEN_CHEST,
                                                           special_rule=lambda s, w: moon_cave_fire_rule_4f(s, w)),
        "Moon Cave - 4F Upper ledge Frozen Chest": LocData(969653, type=LocationType.FROZEN_CHEST,
                                                           special_rule=lambda s, w: moon_cave_fire_rule_4f(s, w))
    }
}
