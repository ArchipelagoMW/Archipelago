from ...locations.birdKey import BirdKey
from ...locations.chest import Chest
from ...locations.faceKey import FaceKey
from ...locations.goldLeaf import GoldLeaf
from ...locations.heartPiece import HeartPiece
from ...locations.madBatter import MadBatter
from ...locations.song import Song
from ...locations.startItem import StartItem
from ...locations.tradeSequence import TradeSequenceItem
from ...locations.seashell import Seashell
from ...locations.shop import ShopItem
from ...locations.droppedKey import DroppedKey
from ...locations.witch import Witch
from ...logic import *
from ...logic.dungeon1 import Dungeon1
from ...logic.dungeon2 import Dungeon2
from ...logic.dungeon3 import Dungeon3
from ...logic.dungeon4 import Dungeon4
from ...logic.dungeon5 import Dungeon5
from ...logic.dungeon6 import Dungeon6
from ...logic.dungeon7 import Dungeon7
from ...logic.dungeon8 import Dungeon8
from ...logic.dungeonColor import DungeonColor


def one_way(loc, req=None):
    res = Location()
    loc.connect(res, req, one_way=True)
    return res


class EntranceInfo:
    def __init__(self, *, items=None, logic=None, exits=None):
        self.items = items
        self.logic = logic
        self.exits = exits


INFO = {
    "start_house": EntranceInfo(items={None: 1}, logic=lambda c, w, r: Location().add(StartItem())),
    "d0": EntranceInfo(
        items={None: 2, KEY9: 3, MAP9: 1, COMPASS9: 1, STONE_BEAK9: 1, NIGHTMARE_KEY9: 1},
        logic=lambda c, w, r: DungeonColor(c, w, r).entrance
    ),
    "d1": EntranceInfo(
        items={None: 3, KEY1: 3, MAP1: 1, COMPASS1: 1, STONE_BEAK1: 1, NIGHTMARE_KEY1: 1, HEART_CONTAINER: 1, INSTRUMENT1: 1},
        logic=lambda c, w, r: Dungeon1(c, w, r).entrance
    ),
    "d2": EntranceInfo(
        items={None: 3, KEY2: 5, MAP2: 1, COMPASS2: 1, STONE_BEAK2: 1, NIGHTMARE_KEY2: 1, HEART_CONTAINER: 1, INSTRUMENT2: 1},
        logic=lambda c, w, r: Dungeon2(c, w, r).entrance
    ),
    "d3": EntranceInfo(
        items={None: 4, KEY3: 9, MAP3: 1, COMPASS3: 1, STONE_BEAK3: 1, NIGHTMARE_KEY3: 1, HEART_CONTAINER: 1, INSTRUMENT3: 1},
        logic=lambda c, w, r: Dungeon3(c, w, r).entrance
    ),
    "d4": EntranceInfo(
        items={None: 4, KEY4: 5, MAP4: 1, COMPASS4: 1, STONE_BEAK4: 1, NIGHTMARE_KEY4: 1, HEART_CONTAINER: 1, INSTRUMENT4: 1},
        logic=lambda c, w, r: Dungeon4(c, w, r).entrance
    ),
    "d5": EntranceInfo(
        items={None: 5, KEY5: 3, MAP5: 1, COMPASS5: 1, STONE_BEAK5: 1, NIGHTMARE_KEY5: 1, HEART_CONTAINER: 1, INSTRUMENT5: 1},
        logic=lambda c, w, r: Dungeon5(c, w, r).entrance
    ),
    "d6": EntranceInfo(
        items={None: 6, KEY6: 3, MAP6: 1, COMPASS6: 1, STONE_BEAK6: 1, NIGHTMARE_KEY6: 1, HEART_CONTAINER: 1, INSTRUMENT6: 1},
        logic=lambda c, w, r: Dungeon6(c, w, r, raft_game_chest=False).entrance
    ),
    "d7": EntranceInfo(
        items={None: 4, KEY7: 3, MAP7: 1, COMPASS7: 1, STONE_BEAK7: 1, NIGHTMARE_KEY7: 1, HEART_CONTAINER: 1, INSTRUMENT7: 1},
        logic=lambda c, w, r: Dungeon7(c, w, r).entrance
    ),
    "d8": EntranceInfo(
        items={None: 6, KEY8: 7, MAP8: 1, COMPASS8: 1, STONE_BEAK8: 1, NIGHTMARE_KEY8: 1, HEART_CONTAINER: 1, INSTRUMENT8: 1},
        logic=lambda c, w, r: Dungeon8(c, w, r, back_entrance_heartpiece=False).entrance
    ),

    "writes_cave_left": EntranceInfo(
        items={None: 2},
        logic=lambda c, w, r: Location().connect(
                Location().add(Chest(0x2AE)), OR(FEATHER, ROOSTER, HOOKSHOT)
            ).connect(
                Location().add(Chest(0x2AF)), POWER_BRACELET
            ),
        exits=[("writes_cave_right", lambda loc: loc)],
    ),
    "writes_cave_right": EntranceInfo(),

    "castle_main_entrance": EntranceInfo(
        items={None: 2},
        logic=lambda c, w, r: Location().connect(
                Location().add(GoldLeaf(0x2D2)), r.attack_hookshot_powder    # in the castle, kill enemies
            ).connect(
                Location().add(GoldLeaf(0x2C5)), AND(BOMB, r.attack_hookshot_powder)   # in the castle, bomb wall to show enemy
            ),
        exits=[("castle_upper_left", lambda loc: loc)],
    ),
    "castle_upper_left": EntranceInfo(),

    "castle_upper_right": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(GoldLeaf(0x2C6)), AND(POWER_BRACELET, r.attack_hookshot)),
    ),

    "right_taltal_connector1": EntranceInfo(
        logic=lambda c, w, r: Location(),
        exits=[("right_taltal_connector2", lambda loc: loc)],
    ),
    "right_taltal_connector2": EntranceInfo(),

    "fire_cave_entrance": EntranceInfo(
        logic=lambda c, w, r: Location(),
        exits=[("fire_cave_exit", lambda loc: Location().connect(loc, COUNT(SHIELD, 2)))],
    ),
    "fire_cave_exit": EntranceInfo(),

    "graveyard_cave_left": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(HeartPiece(0x2DF)), OR(AND(BOMB, OR(HOOKSHOT, PEGASUS_BOOTS), FEATHER), ROOSTER)),
        exits=[("graveyard_cave_right", lambda loc: Location().connect(loc, OR(FEATHER, ROOSTER)))],
    ),
    "graveyard_cave_right": EntranceInfo(),

    "raft_return_enter": EntranceInfo(
        logic=lambda c, w, r: Location(),
        exits=[("raft_return_exit", one_way)],
    ),
    "raft_return_exit": EntranceInfo(),

    "prairie_right_cave_top": EntranceInfo(
        logic=lambda c, w, r: Location(),
        exits=[("prairie_right_cave_bottom", lambda loc: loc), ("prairie_right_cave_high", lambda loc: Location().connect(loc, AND(BOMB, OR(FEATHER, ROOSTER))))],
    ),
    "prairie_right_cave_bottom": EntranceInfo(),
    "prairie_right_cave_high": EntranceInfo(),

    "armos_maze_cave": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().add(Chest(0x2FC)),
    ),
    "right_taltal_connector3": EntranceInfo(
        logic=lambda c, w, r: Location(),
        exits=[("right_taltal_connector4", lambda loc: one_way(loc, AND(OR(FEATHER, ROOSTER), HOOKSHOT)))],
    ),
    "right_taltal_connector4": EntranceInfo(),

    "obstacle_cave_entrance": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(Chest(0x2BB)), AND(SWORD, OR(HOOKSHOT, ROOSTER))),
        exits=[
            ("obstacle_cave_outside_chest", lambda loc: Location().connect(loc, SWORD)),
            ("obstacle_cave_exit", lambda loc: Location().connect(loc, AND(SWORD, OR(PEGASUS_BOOTS, ROOSTER))))
        ],
    ),
    "obstacle_cave_outside_chest": EntranceInfo(),
    "obstacle_cave_exit": EntranceInfo(),

    "d6_connector_entrance": EntranceInfo(
        logic=lambda c, w, r: Location(),
        exits=[("d6_connector_exit", lambda loc: Location().connect(loc, OR(AND(HOOKSHOT, OR(FLIPPERS, AND(FEATHER, PEGASUS_BOOTS))), ROOSTER)))],
    ),
    "d6_connector_exit": EntranceInfo(),

    "multichest_left": EntranceInfo(
        logic=lambda c, w, r: Location(),
        exits=[
            ("multichest_right", lambda loc: loc),
            ("multichest_top", lambda loc: Location().connect(loc, BOMB)),
        ],
    ),
    "multichest_right": EntranceInfo(),
    "multichest_top": EntranceInfo(),

    "prairie_madbatter_connector_entrance": EntranceInfo(
        logic=lambda c, w, r: Location(),
        exits=[("prairie_madbatter_connector_exit", lambda loc: Location().connect(loc, FLIPPERS))],
    ),
    "prairie_madbatter_connector_exit": EntranceInfo(),

    "papahl_house_left": EntranceInfo(
        logic=lambda c, w, r: Location(),
        exits=[("papahl_house_right", lambda loc: loc)],
    ),
    "papahl_house_right": EntranceInfo(),

    "prairie_to_animal_connector": EntranceInfo(
        logic=lambda c, w, r: Location(),
        exits=[("animal_to_prairie_connector", lambda loc: Location().connect(loc, PEGASUS_BOOTS))],
    ),
    "animal_to_prairie_connector": EntranceInfo(),

    "castle_secret_entrance": EntranceInfo(
        logic=lambda c, w, r: Location(),
        exits=[("castle_secret_exit", lambda loc: Location().connect(loc, FEATHER))],
    ),
    "castle_secret_exit": EntranceInfo(),

    "papahl_entrance": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().add(Chest(0x28A)),
        exits=[("papahl_exit", lambda loc: loc)],
    ),
    "papahl_exit": EntranceInfo(),

    "right_taltal_connector5": EntranceInfo(
        logic=lambda c, w, r: Location(),
        exits=[("right_taltal_connector6", lambda loc: loc)],
    ),
    "right_taltal_connector6": EntranceInfo(),

    "toadstool_entrance": EntranceInfo(
        items={None: 2},
        logic=lambda c, w, r: Location().connect(Location().add(Chest(0x2BD)), SWORD).connect(  # chest in forest cave on route to mushroom
            Location().add(HeartPiece(0x2AB), POWER_BRACELET)),  # piece of heart in the forest cave on route to the mushroom
        exits=[("right_taltal_connector6", lambda loc: loc)],
    ),
    "toadstool_exit": EntranceInfo(),

    "richard_house": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(Chest(0x2C8)), AND(COUNT(GOLD_LEAF, 5), OR(FEATHER, HOOKSHOT, ROOSTER))),
        exits=[("richard_maze", lambda loc: Location().connect(loc, COUNT(GOLD_LEAF, 5)))],
    ),
    "richard_maze": EntranceInfo(),

    "left_to_right_taltalentrance": EntranceInfo(
        exits=[("left_taltal_entrance", lambda loc: one_way(loc, OR(HOOKSHOT, ROOSTER)))],
    ),
    "left_taltal_entrance": EntranceInfo(),

    "boomerang_cave": EntranceInfo(),  # TODO boomerang gift
    "trendy_shop": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(TradeSequenceItem(0x2A0, TRADING_ITEM_YOSHI_DOLL)), FOUND("RUPEES", 50))
    ),
    "moblin_cave": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(Chest(0x2E2)), AND(r.attack_hookshot_powder, r.miniboss_requirements[w.miniboss_mapping["moblin_cave"]]))
    ),
    "prairie_madbatter": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(MadBatter(0x1E0)), MAGIC_POWDER)
    ),
    "ulrira": EntranceInfo(),
    "rooster_house": EntranceInfo(),
    "animal_house2": EntranceInfo(),
    "animal_house4": EntranceInfo(),
    "armos_fairy": EntranceInfo(),
    "right_fairy": EntranceInfo(),
    "photo_house": EntranceInfo(),

    "bird_cave": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(BirdKey()), OR(AND(FEATHER, COUNT(POWER_BRACELET, 2)), ROOSTER))
    ),
    "mamu": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(Song(0x2FB)), AND(OCARINA, COUNT("RUPEES", 300)))
    ),
    "armos_temple": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(FaceKey()), r.miniboss_requirements[w.miniboss_mapping["armos_temple"]])
    ),
    "animal_house1": EntranceInfo(),
    "madambowwow": EntranceInfo(),
    "library": EntranceInfo(),
    "kennel": EntranceInfo(
        items={None: 1, TRADING_ITEM_RIBBON: 1},
        logic=lambda c, w, r: Location().connect(Location().add(Seashell(0x2B2)), SHOVEL).connect(Location().add(TradeSequenceItem(0x2B2, TRADING_ITEM_DOG_FOOD)), TRADING_ITEM_RIBBON)
    ),
    "dream_hut": EntranceInfo(
        items={None: 2},
        logic=lambda c, w, r: Location().connect(Location().add(Chest(0x2BF)), OR(SWORD, BOOMERANG, HOOKSHOT, FEATHER)).connect(Location().add(Chest(0x2BE)), AND(OR(SWORD, BOOMERANG, HOOKSHOT, FEATHER), PEGASUS_BOOTS))
    ),
    "hookshot_cave": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(Chest(0x2B3)), OR(HOOKSHOT, ROOSTER))
    ),
    "madbatter_taltal": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(MadBatter(0x1E2)), MAGIC_POWDER)
    ),
    "forest_madbatter": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(MadBatter(0x1E1)), MAGIC_POWDER)
    ),
    "banana_seller": EntranceInfo(
        items={TRADING_ITEM_DOG_FOOD: 1},
        logic=lambda c, w, r: Location().connect(Location().add(TradeSequenceItem(0x2FE, TRADING_ITEM_BANANAS)), TRADING_ITEM_DOG_FOOD)
    ),
    "shop": EntranceInfo(
        items={None: 2},
        logic=lambda c, w, r: Location().connect(Location().add(ShopItem(0)), COUNT("RUPEES", 200)).connect(Location().add(ShopItem(1)), COUNT("RUPEES", 980))
    ),
    "ghost_house": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(Seashell(0x1E3)), POWER_BRACELET)
    ),
    "writes_house": EntranceInfo(
        items={TRADING_ITEM_LETTER: 1},
        logic=lambda c, w, r: Location().connect(Location().add(TradeSequenceItem(0x2A8, TRADING_ITEM_BROOM)), TRADING_ITEM_LETTER)
    ),
    "animal_house3": EntranceInfo(
        items={TRADING_ITEM_HIBISCUS: 1},
        logic=lambda c, w, r: Location().connect(Location().add(TradeSequenceItem(0x2D9, TRADING_ITEM_LETTER)), TRADING_ITEM_HIBISCUS)
    ),
    "animal_house5": EntranceInfo(
        items={TRADING_ITEM_HONEYCOMB: 1},
        logic=lambda c, w, r: Location().connect(Location().add(TradeSequenceItem(0x2D7, TRADING_ITEM_PINEAPPLE)), TRADING_ITEM_HONEYCOMB)
    ),
    "crazy_tracy": EntranceInfo(
        items={"MEDICINE2": 1},
        logic=lambda c, w, r: Location().connect(Location().add(KeyLocation("MEDICINE2")), FOUND("RUPEES", 50))
    ),
    "rooster_grave": EntranceInfo(
        logic=lambda c, w, r: Location().connect(Location().add(DroppedKey(0x1E4)), AND(OCARINA, SONG3))
    ),
    "desert_cave": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().connect(Location().add(HeartPiece(0x1E8)), BOMB)
    ),
    "witch": EntranceInfo(
        items={TOADSTOOL: 1},
        logic=lambda c, w, r: Location().connect(Location().add(Witch()), TOADSTOOL)
    ),
    "prairie_left_cave1": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().add(Chest(0x2CD))
    ),
    "prairie_left_cave2": EntranceInfo(
        items={None: 2},
        logic=lambda c, w, r: Location().connect(Location().add(Chest(0x2F4)), PEGASUS_BOOTS).connect(Location().add(HeartPiece(0x2E5)), AND(BOMB, PEGASUS_BOOTS))
    ),
    "castle_jump_cave": EntranceInfo(
        items={None: 1},
        logic=lambda c, w, r: Location().add(Chest(0x1FD))
    ),
    "raft_house": EntranceInfo(),
    "prairie_left_fairy": EntranceInfo(),
    "seashell_mansion": EntranceInfo(),  # TODO: Not sure if we can guarantee enough shells
}
