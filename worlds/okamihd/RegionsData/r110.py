from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from rule_builder.rules import HasGroup, And, Has
from ..CheckIds import brush_check_id, container_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Rules import has_soup_ingerdients, moon_cave_fire_rule, moon_cave_4f_fire_rule, moon_cave_canon_rule
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    # Not setting this as one way on purpose since we want to be able to exit moon cave
    RegionNames.MOON_CAVE_BROKEN_STAIRS: [
        ExitData(RegionNames.MOON_CAVE_UNDERGROUND_ENTRANCE)
    ],
    RegionNames.MOON_CAVE_UNDERGROUND_ENTRANCE: [
        ExitData(RegionNames.CALCIFIED_CAVERN)
    ],
    RegionNames.MOON_CAVE: [
        ExitData(RegionNames.MOON_CAVE_1F_LOCKED_CAVE,
                 required_items_events=["Moon Cave - 1F Free Ajimi from soup"], loading_screen=False,
                 one_way=True),
        ExitData(RegionNames.MOON_CAVE_B2F_LIFT,
                 required_items_events=["Moon Cave - 1F Main room disturb lift"], loading_screen=False),
        ExitData(RegionNames.MOON_CAVE_KITCHEN_BACK, loading_screen=False,
                 required_items_events=["Moon Cave - 1F Melt Kitchen Ice"]),
        ExitData(RegionNames.MOON_CAVE_OROCHI,
                 required_items_events=["Moon Cave - 1F Give all ingredients to Ajimi"]),
        ExitData(RegionNames.MOON_CAVE_2F_GEYSER_RAFTER,
                 required_items_events=["Moon Cave - 1F Blue Flower to 2F accessible"],
                 loading_screen=False, one_way=True),
        ExitData(RegionNames.MOON_CAVE_B1F_UNDER_LIFT, loading_screen=False, one_way=True,
                 required_items_events=["Moon Cave - B1F Lake open valve"]),
        ExitData(RegionNames.MOON_CAVE_2F_RAFTERS_CHEST,
                 required_items_events=["Moon Cave - 1F Main room geyser"], loading_screen=False, one_way=True)
    ],
    RegionNames.MOON_CAVE_1F_LOCKED_CAVE: [
        ExitData(RegionNames.MOON_CAVE_1F_LOCKED_CAVE_BACK,
                 required_items_events=['Moon Cave - 1F Locked Cave open eye door'],
                 loading_screen=False),
        ExitData(RegionNames.MOON_CAVE_2F_GEYSER_RAFTER,
                 required_items_events=["Moon Cave - 1F Locked Cave geyser"],
                 loading_screen=False)
    ],
    RegionNames.MOON_CAVE_2F_GEYSER_RAFTER: [
        ExitData(RegionNames.MOON_CAVE_3F, required_items_events=["Moon cave - 2F rafter's geyser"], loading_screen=False),
        ExitData(RegionNames.MOON_CAVE, one_way=True, loading_screen=False)
    ],
    RegionNames.MOON_CAVE_2F_RAFTERS_CHEST: [
        ExitData(RegionNames.MOON_CAVE, loading_screen=False, one_way=True)
    ],
    RegionNames.MOON_CAVE_3F: [
        ExitData(RegionNames.MOON_CAVE_B1F_LAKE, loading_screen=False, one_way=True),
        # Ensure the player can repair the bridge to access this
        ExitData(RegionNames.MOON_CAVE_3F_FIRE_EYE,
                 required_items_events=["Moon Cave - 3F Melt Ice block after bridge",
                             "Moon Cave - 3F repair Bridge"],
                 loading_screen=False),
        ExitData(RegionNames.MOON_CAVE_3F_SAND,
                 required_items_events=["Moon Cave - 3F Open door to Sand room"], loading_screen=False,
                 one_way=True),
        ExitData(RegionNames.MOON_CAVE, one_way=True, loading_screen=False)
    ],
    RegionNames.MOON_CAVE_B1F_LAKE: [
        ExitData(RegionNames.MOON_CAVE_B1F_UNDER_LIFT,
                 required_items_events=["Moon Cave - B1F Lake geyser"], loading_screen=False)
    ],
    RegionNames.MOON_CAVE_B1F_UNDER_LIFT: [
        ExitData(RegionNames.MOON_CAVE,
                 required_items_events=["Moon Cave - B1F under lift geyser"],
                 loading_screen=False, one_way=True)
    ],
    RegionNames.MOON_CAVE_B2F_LIFT: [
        ExitData(RegionNames.MOON_CAVE_B2F_FROZEN_STATUE,
                 required_items_events=["Moon Cave - B2F oepn eyes door"], loading_screen=False)],
    RegionNames.MOON_CAVE_B2F_FROZEN_STATUE: [
        ExitData(RegionNames.MOON_CAVE_B2F_OTHER_LIFT,
                 required_items_events=["Moon Cave - B2F Melt Ice block to other lift"], loading_screen=False)],
    RegionNames.MOON_CAVE_B2F_OTHER_LIFT: [
        ExitData(RegionNames.MOON_CAVE_B2F_BOMBABLE,
                 required_items_events=["Moon Cave - B2F Explode wall behind lift"], loading_screen=False),
        ExitData(RegionNames.MOON_CAVE_KITCHEN_BACK, loading_screen=False, one_way=True)
    ],
    RegionNames.MOON_CAVE_KITCHEN_BACK: [
        ExitData(RegionNames.MOON_CAVE_B2F_OTHER_LIFT, one_way=True, loading_screen=False,
                 required_items_events=["Moon Cave - 1F Disrupt lift in kitchen back"])
    ],
    RegionNames.MOON_CAVE_3F_SAND: [
        ExitData(RegionNames.MOON_CAVE_3F_RAFTERS_AFTER_SAND, loading_screen=False, one_way=True),
        ExitData(RegionNames.MOON_CAVE_2F_SAND_PIT, one_way=True, loading_screen=False),
        ExitData(RegionNames.MOON_CAVE, loading_screen=False, one_way=True)
    ],
    RegionNames.MOON_CAVE_2F_SAND_PIT: [
        ExitData(RegionNames.MOON_CAVE_3F_SAND, one_way=True, loading_screen=False,
                 required_items_events=["Moon Cave - 3F Blow up Sand pit wall"])
    ],
    RegionNames.MOON_CAVE_3F_RAFTERS_AFTER_SAND: [
        ExitData(RegionNames.MOON_CAVE_4F_RAFTERS,
                 required_items_events=["Moon Cave - 3F Rafters use flower"],
                 loading_screen=False, one_way=True)
    ],
    RegionNames.MOON_CAVE_4F_RAFTERS: [
        ExitData(RegionNames.MOON_CAVE_3F_RAFTERS_AFTER_SAND, required_items_events=["Moon Cave - 4F Rafters use flower"],
                 loading_screen=False, one_way=True),
        ExitData(RegionNames.MOON_CAVE, one_way=True, loading_screen=False),
        ExitData(RegionNames.MOON_CAVE_4F_CANON,
                 required_items_events=["Moon Cave - 4F Rafters cross banners"],
                 loading_screen=False),
        ExitData(
            RegionNames.MOON_CAVE_4F_AFTER_CANON,
            required_items_events=["Moon Cave - 4F Mandatory Fight"], loading_screen=False)
    ],
    RegionNames.MOON_CAVE_4F_CANON: [
        ExitData(RegionNames.MOON_CAVE, one_way=True, loading_screen=False)
    ]

}
events = {
    RegionNames.MOON_CAVE: {
        "Moon Cave - 1F Free Ajimi from soup": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),
        "Moon Cave - 1F Main room geyser": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT],
                                                     special_rule=moon_cave_fire_rule),
        "Moon Cave - 1F Main room disturb lift": EventData(power_slash_level=1,
                                                           required_items_events=["Moon Cave - B1F Open lift hatch"]),
        "Moon Cave - 1F Melt Kitchen Ice from front": EventData(required_brush_techniques=[BrushTechniques.INFERNO],
                                                                event_item_name="Moon Cave - 1F Melt Kitchen Ice"),
        "Moon Cave - 1F Blue Flower to 2F accessible": EventData(
            required_items_events=["Moon Cave - Mandatory Ogre Encounter"]),
        "Moon Cave - 1F Give all ingredients to Ajimi": EventData(
            special_rule=HasGroup("soup_ingredients", count=4))
    },
    RegionNames.MOON_CAVE_1F_LOCKED_CAVE: {
        "Moon Cave - Cross 1F Locked Cave": EventData(required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),
        "Moon Cave - 1F Locked Cave Blow up wall": EventData(cherry_bomb_level=1),
        "Moon Cave - 1F Locked Cave open eye door": EventData(power_slash_level=1, required_items_events=[
            "Moon Cave - Cross 1F Locked Cave"]),
        "Moon Cave - 1F Locked Cave geyser": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT],
                                                       required_items_events=["Moon Cave - Mandatory Ogre Encounter"]),
    },
    RegionNames.MOON_CAVE_1F_LOCKED_CAVE_BACK: {
        "Moon Cave - Mandatory Ogre Encounter": EventData(
            mandatory_enemies=[OkamiEnemies.RED_IMP, OkamiEnemies.BUD_OGRE]),
    },
    RegionNames.MOON_CAVE_2F_GEYSER_RAFTER: {
        "Moon cave - 2F rafter's geyser": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT])
    },
    RegionNames.MOON_CAVE_3F: {
        "Moon Cave - 3F repair Bridge": EventData(required_brush_techniques=[BrushTechniques.REJUVENATION]),
        "Moon Cave - 3F Melt Ice block after bridge": EventData(required_brush_techniques=[BrushTechniques.INFERNO],
                                                                required_items_events=["Moon Cave - 3F repair Bridge"]),
        # FIXME: Pretty sure this is wrong and you don't need to do the torii to grab the key
        "Moon Cave - 3F Open door to Sand room": EventData(
            required_items_events=["Moon Cave - 3F Cursed Fire Eye Torii"])
    },
    RegionNames.MOON_CAVE_B1F_LAKE: {
        "Moon Cave - B1F Lake cursed Torii": EventData(
            mandatory_enemies=[OkamiEnemies.RED_IMP, OkamiEnemies.BLACK_IMP]),
        "Moon Cave - B1F Lake open valve": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT]),
        "Moon Cave - B1F Lake geyser": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT],
                                                 required_items_events=["Moon Cave - B1F Lake open valve"]),
    },
    RegionNames.MOON_CAVE_B1F_UNDER_LIFT: {
        "Moon Cave - B1F Mandatory Fight": EventData(mandatory_enemies=[OkamiEnemies.BLACK_IMP]),
        "Moon Cave - B1F Open lift hatch": EventData(power_slash_level=1,
                                                     required_items_events=["Moon Cave - B1F Mandatory Fight"]),
        "Moon Cave - B1F under lift geyser": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT],
                                                       required_items_events=["Moon Cave - B1F Mandatory Fight"])
    },
    RegionNames.MOON_CAVE_B2F_LIFT: {
        "Moon Cave - B2F oepn eyes door": EventData(power_slash_level=1)
    },
    RegionNames.MOON_CAVE_B2F_FROZEN_STATUE: {
        "Moon Cave - B2F Defeat Ice Lips": EventData(mandatory_enemies=[OkamiEnemies.ICE_LIPS]),
        "Moon Cave - B2F Melt Ice block to other lift": EventData(required_brush_techniques=[BrushTechniques.INFERNO])
    },
    RegionNames.MOON_CAVE_B2F_OTHER_LIFT: {
        "Moon Cave - B2F Melt Ice Block behind lift": EventData(required_brush_techniques=[BrushTechniques.INFERNO]),
        "Moon Cave - B2F Explode wall behind lift": EventData(cherry_bomb_level=1, required_items_events=[
            "Moon Cave - B2F Melt Ice Block behind lift"])
    },
    RegionNames.MOON_CAVE_KITCHEN_BACK: {
        "Moon Cave - 1F Disrupt lift in kitchen back": EventData(power_slash_level=1),
        "Moon Cave - 1F Cursed Door in kitchen back": EventData(mandatory_enemies=[OkamiEnemies.ICE_LIPS]),

        # Can be done from the other way too;
        "Moon Cave - 1F Melt kitchen Ice form behind": EventData(
            required_brush_techniques=[BrushTechniques.INFERNO], event_item_name="Moon Cave - 1F Melt Kitchen Ice")
    },
    RegionNames.MOON_CAVE_3F_FIRE_EYE: {
        "Moon Cave - 3F Cursed Fire Eye Torii": EventData(
            mandatory_enemies=[OkamiEnemies.FIRE_EYE, OkamiEnemies.ICE_LIPS]),

    },
    RegionNames.MOON_CAVE_3F_SAND: {
        # Lights the fireball torches in this dungeon
        "Moon Cave - 3F Push the ball": EventData(required_brush_techniques=[BrushTechniques.GALESTORM]),
    },
    RegionNames.MOON_CAVE_2F_SAND_PIT: {
        "Moon Cave - 3F Blow up Sand pit wall": EventData(cherry_bomb_level=1)
    },
    RegionNames.MOON_CAVE_3F_RAFTERS_AFTER_SAND: {
        "Moon Cave - 3F Rafters use flower": EventData(required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE])
    },
    RegionNames.MOON_CAVE_4F_RAFTERS: {
        "Moon Cave - 4F Rafters use flower": EventData(required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),
        "Moon Cave - 4F Rafters cross banners": EventData(required_brush_techniques=[BrushTechniques.GALESTORM]),
        "Moon Cave - 4F Mandatory Fight": EventData(mandatory_enemies=[OkamiEnemies.BLACK_IMP],
                                                    required_items_events=['Moon Cave - 4F Fire the canon!']),
    },
    RegionNames.MOON_CAVE_4F_CANON: {
        "Moon Cave - 4F Fire the canon!": EventData(special_rule=moon_cave_canon_rule),
    },
    RegionNames.MOON_CAVE_4F_AFTER_CANON: {
        "Moon Cave - 4F Move Fireball": EventData(required_brush_techniques=[BrushTechniques.GALESTORM]),
        "Moon Cave - 4F Melt Ice Blocks": EventData(special_rule=moon_cave_4f_fire_rule),
        "Moon Cave - 4F Black Demon Horn Torii": EventData(
            mandatory_enemies=[OkamiEnemies.BLACK_IMP, OkamiEnemies.RED_IMP],
            required_items_events=["Moon Cave - 4F Melt Ice Blocks"]),

    },
    RegionNames.MOON_CAVE_OROCHI: {
        "Moon Cave - Defeat Orochi": EventData(mandatory_enemies=[OkamiEnemies.OROCHI_1],
                                               required_brush_techniques=[BrushTechniques.CRESCENT],
                                               power_slash_level=1)
    }
}

locations = {
    RegionNames.MOON_CAVE: {
        "Moon Cave - 1F Chest on ledge in the kitchen": LocData(container_check_id(MapIds.MOON_CAVE, 11),
                                                                required_items_events=[
                                                                    "Moon Cave - 1F Free Ajimi from soup"]),
        "Moon Cave - 1F Frozen Chest after Black Demon Horn": LocData(container_check_id(MapIds.MOON_CAVE, 7),
                                                                      type=LocationType.FROZEN_CHEST_SPECIAL_SOURCE,
                                                                      special_rule=moon_cave_fire_rule,
                                                                      required_items_events=[
                                                                          "Moon Cave - 4F Black Demon Horn Torii"]),
        "Moon Cave - 1F Chest after fire eye": LocData(container_check_id(MapIds.MOON_CAVE, 8),
                                                       required_items_events=["Moon Cave - 3F Cursed Fire Eye Torii"]),
    },
    RegionNames.MOON_CAVE_B1F_LAKE: {
        "Moon Cave - B1F Chest on other side of Lake": LocData(container_check_id(MapIds.MOON_CAVE, 13),
                                                               needs_long_swim=True),
        "Moon Cave - B1F Chest behind ice": LocData(container_check_id(MapIds.MOON_CAVE, 14), needs_long_swim=True,
                                                    special_rule=moon_cave_fire_rule)
    },
    RegionNames.MOON_CAVE_1F_LOCKED_CAVE: {
        "Moon Cave - 1F locked cave Treasure bud behind bombable wall": LocData(
            container_check_id(MapIds.MOON_CAVE, 10), type=LocationType.TREASURE_BUD)
    },
    RegionNames.MOON_CAVE_1F_LOCKED_CAVE_BACK: {
        "Moon Cave - Ogre Liver Chest": LocData(container_check_id(MapIds.MOON_CAVE, 0),
                                                required_items_events=["Moon Cave - Mandatory Ogre Encounter"])

    },
    RegionNames.MOON_CAVE_B2F_LIFT: {
        "Moon Cave - B2F Chest on ledge near eyes door": LocData(container_check_id(MapIds.MOON_CAVE, 15))
    },
    RegionNames.MOON_CAVE_KITCHEN_BACK: {
        "Moon Cave - Ice Lips Chest": LocData(container_check_id(MapIds.MOON_CAVE, 2),
                                              required_items_events=["Moon Cave - 1F Cursed Door in kitchen back"]),
    },
    RegionNames.MOON_CAVE_B2F_FROZEN_STATUE: {
        "Moon Cave - Moegami": LocData(brush_check_id(10), type=LocationType.CONSTELLATION,
                                       progress_type=LocationProgressType.EXCLUDED)  # bit 10
    },
    RegionNames.MOON_CAVE_B2F_BOMBABLE: {
        "Moon Cave - B2F Chest behind bombable wall": LocData(container_check_id(MapIds.MOON_CAVE, 4))
    },
    RegionNames.MOON_CAVE_3F_SAND: {
        "Moon Cave - 3F Map Chest after ball puzzle": LocData(container_check_id(MapIds.MOON_CAVE, 9))
    },
    RegionNames.MOON_CAVE_2F_SAND_PIT: {
        "Moon Cave - 3F Chest in sand pit": LocData(container_check_id(MapIds.MOON_CAVE, 16)),
    },
    RegionNames.MOON_CAVE_2F_RAFTERS_CHEST: {
        "Moon Cave - 2F Rafters Chest": LocData(container_check_id(MapIds.MOON_CAVE, 5)),
    },
    RegionNames.MOON_CAVE_3F_RAFTERS_AFTER_SAND: {
        "Moon Cave - 3F Frozen Chest near merchant": LocData(container_check_id(MapIds.MOON_CAVE, 12),
                                                             type=LocationType.FROZEN_CHEST_SPECIAL_SOURCE,
                                                             special_rule=moon_cave_fire_rule),

    },
    RegionNames.MOON_CAVE_3F_FIRE_EYE: {
        "Moon Cave - 3F Left Frozen Chest after Fire eye room": LocData(container_check_id(MapIds.MOON_CAVE, 19),
                                                                        type=LocationType.FROZEN_CHEST_SPECIAL_SOURCE,
                                                                        special_rule=moon_cave_fire_rule),
        "Moon Cave - 3F Middle Frozen Chest after Fire eye room": LocData(container_check_id(MapIds.MOON_CAVE, 17),
                                                                          type=LocationType.FROZEN_CHEST_SPECIAL_SOURCE,
                                                                          special_rule=moon_cave_fire_rule),
        "Moon Cave - 3F Right Frozen Chest after Fire eye room": LocData(container_check_id(MapIds.MOON_CAVE, 18),
                                                                         type=LocationType.FROZEN_CHEST_SPECIAL_SOURCE,
                                                                         special_rule=moon_cave_fire_rule),
        "Moon Cave - 3F Fire Eye Chest": LocData(container_check_id(MapIds.MOON_CAVE, 3),
                                                 required_items_events=["Moon Cave - 3F Cursed Fire Eye Torii"])
    },
    RegionNames.MOON_CAVE_4F_AFTER_CANON: {
        "Moon Cave - 4F Lower ledge Frozen Chest": LocData(container_check_id(MapIds.MOON_CAVE, 20),
                                                           type=LocationType.FROZEN_CHEST_SPECIAL_SOURCE,
                                                           special_rule=moon_cave_4f_fire_rule),
        "Moon Cave - 4F Upper ledge Frozen Chest": LocData(container_check_id(MapIds.MOON_CAVE, 21),
                                                           type=LocationType.FROZEN_CHEST_SPECIAL_SOURCE,
                                                           special_rule=moon_cave_4f_fire_rule),
        "Moon Cave - 4F Black Demon Horn Chest": LocData(container_check_id(MapIds.MOON_CAVE, 1),
                                                         required_items_events=[
                                                             "Moon Cave - 4F Black Demon Horn Torii"])
    },
    RegionNames.MOON_CAVE_OROCHI: {
        ## Cutscene
        "Moon Cave - Orochi Reward": LocData(container_check_id(MapIds.MOON_CAVE, 22),
                                             progress_type=LocationProgressType.EXCLUDED)
    }
}

shop_locations = {
    RegionNames.MOON_CAVE_3F_RAFTERS_AFTER_SAND: {
        "Moon Cave - 3F merchant Shop Slot 1": LocData(shop_check_id(9, 0), type=LocationType.SHOP),
        "Moon Cave - 3F merchant Shop Slot 2": LocData(shop_check_id(9, 1), type=LocationType.SHOP),
        "Moon Cave - 3F merchant Shop Slot 3": LocData(shop_check_id(9, 2), type=LocationType.SHOP),
        "Moon Cave - 3F merchant Shop Slot 4": LocData(shop_check_id(9, 3), type=LocationType.SHOP),
        "Moon Cave - 3F merchant Shop Slot 5": LocData(shop_check_id(9, 4), type=LocationType.SHOP),
        "Moon Cave - 3F merchant Shop Slot 6": LocData(shop_check_id(9, 5), type=LocationType.SHOP),
        "Moon Cave - 3F merchant Shop Slot 7": LocData(shop_check_id(9, 6), type=LocationType.SHOP),
        "Moon Cave - 3F merchant Shop Slot 8": LocData(shop_check_id(9, 7), type=LocationType.SHOP),
        "Moon Cave - 3F merchant Shop Slot 9": LocData(shop_check_id(9, 8), type=LocationType.SHOP),
        "Moon Cave - 3F merchant Shop Slot 10": LocData(shop_check_id(9, 9), type=LocationType.SHOP),
        "Moon Cave - 3F merchant Shop Slot 11": LocData(shop_check_id(9, 10), type=LocationType.SHOP),
        "Moon Cave - 3F merchant Shop Slot 12": LocData(shop_check_id(9, 11), type=LocationType.SHOP),
    },
    RegionNames.MOON_CAVE_OROCHI: {
        "Moon Cave - Merchant Before Orochi Shop Slot 1": LocData(shop_check_id(10, 0), type=LocationType.SHOP),
        "Moon Cave - Merchant Before Orochi Shop Slot 2": LocData(shop_check_id(10, 1), type=LocationType.SHOP),
        "Moon Cave - Merchant Before Orochi Shop Slot 3": LocData(shop_check_id(10, 2), type=LocationType.SHOP),
        "Moon Cave - Merchant Before Orochi Shop Slot 4": LocData(shop_check_id(10, 3), type=LocationType.SHOP),
        "Moon Cave - Merchant Before Orochi Shop Slot 5": LocData(shop_check_id(10, 4), type=LocationType.SHOP),
        "Moon Cave - Merchant Before Orochi Shop Slot 6": LocData(shop_check_id(10, 5), type=LocationType.SHOP),
        "Moon Cave - Merchant Before Orochi Shop Slot 7": LocData(shop_check_id(10, 6), type=LocationType.SHOP),
        "Moon Cave - Merchant Before Orochi Shop Slot 8": LocData(shop_check_id(10, 7), type=LocationType.SHOP),
        "Moon Cave - Merchant Before Orochi Shop Slot 9": LocData(shop_check_id(10, 8), type=LocationType.SHOP),
        "Moon Cave - Merchant Before Orochi Shop Slot 10": LocData(shop_check_id(10, 9), type=LocationType.SHOP),
        "Moon Cave - Merchant Before Orochi Shop Slot 11": LocData(shop_check_id(10, 10), type=LocationType.SHOP),
        "Moon Cave - Merchant Before Orochi Shop Slot 12": LocData(shop_check_id(10, 11), type=LocationType.SHOP),
    }
}
