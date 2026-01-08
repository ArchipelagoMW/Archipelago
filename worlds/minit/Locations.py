from worlds.AutoWorld import World
from typing import NamedTuple, Callable  # Dict


class MinitLocationData(NamedTuple):
    region: str
    er_region: str
    offset: int | None = None
    locked_item: str | None = None

    show_in_spoiler: bool = True
    can_create: Callable[[World], bool] = lambda world: True
    # unused for now but keeping the structure for later

    @property
    def code(self):
        if self.offset is None:
            return None
        return 60600 + self.offset


location_table = {

    # Dog House
    "Dog House - ItemCoffee": MinitLocationData(
        offset=0,
        region="Dog House",
        er_region="coffee shop inside",),
    "Dog House - ItemFlashLight": MinitLocationData(
        offset=1,
        region="Dog House",
        er_region="lighthouse lookout",),
    "Dog House - ItemKey": MinitLocationData(
        offset=2,
        region="Dog House",
        er_region="key room",),
    "Dog House - ItemWateringCan": MinitLocationData(
        offset=3,
        region="Dog House",
        er_region="watering can",),
    "Dog house - ItemBoat": MinitLocationData(
        offset=4,
        region="Dog House",
        er_region="boattree main",),
    "Dog House - ItemBasement": MinitLocationData(
        offset=5,
        region="Dog House",
        er_region="Overworld island shack",),
    "Dog House - ItemPressPass": MinitLocationData(
        offset=6,
        region="Dog House",
        er_region="camera house inside",),
    "Dog House - House Pot Coin": MinitLocationData(
        # coin1 - coin
        offset=7,
        region="Dog House",
        er_region="dog house inside",),
    "Dog House - Sewer Island Coin": MinitLocationData(
        # coin2 - chest
        offset=8,
        region="Dog House",
        er_region="sewer island",),
    "Dog House - Sewer Coin": MinitLocationData(
        # coin3 - chest
        offset=9,
        region="Dog House",
        er_region="sewer upper",),
    "Dog House - Land is Great Coin": MinitLocationData(
        # coin4 - chest
        offset=10,
        region="Dog House",
        er_region="above lighthouse land",),
    "Dog House - Hidden Snake Coin": MinitLocationData(
        # coin5 - chest
        offset=11,
        region="Dog House",
        er_region="snake west",),
    "Dog House - Waterfall Coin": MinitLocationData(
        # coin6 - chest
        offset=12,
        region="Dog House",
        er_region="waterfall cave",),
    "Dog House - Treasure Island Coin": MinitLocationData(
        # coin7 - chest
        offset=13,
        region="Dog House",
        er_region="Overworld treasure island",),
    "Dog House - Plant Heart": MinitLocationData(
        # heartPiece1
        offset=14,
        region="Dog House",
        er_region="plant tile",),
    "Dog House - Bull Heart": MinitLocationData(
        # heartPiece2
        offset=15,
        region="Dog House",
        er_region="bull room",),
    "Dog House - Boat Tentacle": MinitLocationData(
        # tentacle1
        offset=16,
        region="Dog House",
        er_region="boat tile",),
    "Dog House - Treasure Island Tentacle": MinitLocationData(
        # tentacle2
        offset=17,
        region="Dog House",
        er_region="Overworld treasure island",),
    "Dog House - Sword Toss Tentacle": MinitLocationData(
        # tentacle3
        offset=18,
        region="Dog House",
        er_region="throwcheck box",),
    "Dog House - Sewer Tentacle": MinitLocationData(
        # tentacle4
        offset=19,
        region="Dog House",
        er_region="sewer tentacle",),

    # Desert RV
    "Desert RV - ItemThrow": MinitLocationData(
        offset=20,
        region="Desert RV",
        er_region="Overworld desert",),
    "Desert RV - ItemShoes": MinitLocationData(
        offset=21,
        region="Desert RV",
        er_region="shoe shop inside",),
    "Desert RV - ItemGlove": MinitLocationData(
        offset=22,
        region="Desert RV",
        er_region="glove inside",),
    "Desert RV - ItemTurboInk": MinitLocationData(
        offset=23,
        region="Desert RV",
        er_region="temple octopus",),
    "Desert RV - Temple Coin": MinitLocationData(
        # coin8 - chest
        offset=24,
        region="Desert RV",
        er_region="temple coin chest",),
    "Desert RV - Fire Bat Coin": MinitLocationData(
        # coin9 - chest
        offset=25,
        region="Desert RV",
        er_region="temple firebat chest",),
    "Desert RV - Truck Supplies Coin": MinitLocationData(
        # coin10 - chest
        offset=26,
        region="Desert RV",
        er_region="factory loading lower shortcut",),
    "Desert RV - Broken Truck": MinitLocationData(
        # coin13 - chest
        offset=27,
        region="Desert RV",
        er_region="Overworld desert",),
    "Desert RV - Quicksand Coin": MinitLocationData(
        # coin16 - chest
        offset=28,
        region="Desert RV",
        er_region="quicksand main",),
    "Desert RV - Dumpster": MinitLocationData(
        # coin19 - coin but you need to hit it
        offset=29,
        region="Desert RV",
        er_region="shoe shop outside",),
    "Desert RV - Temple Heart": MinitLocationData(
        # heartPiece3
        offset=30,
        region="Desert RV",
        er_region="temple heart",),
    "Desert RV - Shop Heart": MinitLocationData(
        # heartPiece4
        offset=31,
        region="Desert RV",
        er_region="shoe shop downstairs",),
    "Desert RV - Octopus Tentacle": MinitLocationData(
        # tentacle5
        offset=32,
        region="Desert RV",
        er_region="temple tentacle",),
    "Desert RV - Beach Tentacle": MinitLocationData(
        # tentacle8
        offset=33,
        region="Desert RV",
        er_region="desert beach tile",),

    # Hotel Room
    "Hotel Room - ItemSwim": MinitLocationData(
        offset=34,
        region="Hotel Room",
        er_region="hotel outside",),
    "Hotel Room - ItemGrinder": MinitLocationData(
        offset=35,
        region="Hotel Room",
        er_region="grinder tile",),
    "Hotel Room - Shrub Arena Coin": MinitLocationData(
        # coin11 - coin but you need to stab them
        offset=36,
        region="Hotel Room",
        er_region="arena tile",),
    "Hotel Room - Miner's Chest Coin": MinitLocationData(
        # coin12 - chest
        offset=37,
        region="Hotel Room",
        er_region="miner chest tile",),
    "Factory Main - Inside Truck": MinitLocationData(
        # coin14 - coin
        offset=38,
        region="Factory Main",
        er_region="factory loading upper",),
    "Hotel Room - Queue": MinitLocationData(
        # coin15 - coin
        offset=39,
        region="Hotel Room",
        er_region="factory queue",),
    "Hotel Room - Hotel Backroom Coin": MinitLocationData(
        # coin17 - chest
        offset=40,
        region="Hotel Room",
        er_region="hotel backroom",),
    "Factory Main - Drill Coin": MinitLocationData(
        # coin18 - coin
        offset=41,
        region="Factory Main",
        er_region="factory drill",),
    "Hotel Room - Crow Heart": MinitLocationData(
        # heartPiece5
        offset=42,
        region="Hotel Room",
        er_region="crowroom",),
    "Hotel Room - Dog Heart": MinitLocationData(
        # heartPiece6
        offset=43,
        region="Hotel Room",
        er_region="bone room",),
    "Factory Main - Cooler Tentacle": MinitLocationData(
        # tentacle7
        offset=44,
        region="Factory Main",
        er_region="factory cooler tile",),

    # Island Shack
    "Island Shack - Teleporter Tentacle": MinitLocationData(
        # tentacle6
        offset=45,
        region="Island Shack",
        er_region="teleporter tentacle",),

    # Underground Tent
    "Underground Tent - ItemTrophy": MinitLocationData(
        offset=46,
        region="Underground Tent",
        er_region="trophy room",),

    # Undefined
    # "REGION - ItemCamera": MinitLocationData(
    #     # logic:
    #     offset=47,
    #     region="Dog House",
    #    er_region="camera house inside",),
    # itemCamera location is replaced by press pass,
    # - will be handled the same in game

    "Factory Main - ItemMegaSword": MinitLocationData(
        offset=48,
        region="Factory Main",
        er_region="megasword lower",),
    "Dog House - ItemSword": MinitLocationData(
        offset=49,
        region="Dog House",
        er_region="sword east",),
    "Dog House - Dolphin Heart": MinitLocationData(
        offset=51,
        region="Dog House",
        er_region="dolphin tile",),

    "Fight the Boss": MinitLocationData(
        region="Boss Fight",
        er_region="Boss Fight",
        locked_item="Boss dead",
        ),
    "Flush the Sword": MinitLocationData(
        region="Factory Main",
        er_region="factory toilet",
        locked_item="Sword Flushed",
        ),
    "generator smashed": MinitLocationData(
        region="Factory Main",
        er_region="factory machine generator",
        locked_item="generator smashed",
        ),
    "drill smacked": MinitLocationData(
        region="Factory Main",
        er_region="factory drill",
        locked_item="drill smacked",
        ),
    "swimmer saved": MinitLocationData(
        region="Hotel Room",
        er_region="diver room",
        locked_item="swimmer saved",
        ),
    "hostage saved": MinitLocationData(
        region="Hotel Room",
        er_region="arena tile",
        locked_item="hostage saved",
        ),
    "wallet saved": MinitLocationData(
        region="Hotel Room",
        er_region="wallet room",
        locked_item="wallet saved",
        ),
    "ninja saved": MinitLocationData(
        region="Hotel Room",
        er_region="tree resident",
        locked_item="ninja saved",
        ),
    "bridge on": MinitLocationData(
        region="Hotel Room",
        er_region="bridge switch right",
        locked_item="bridge on",
        ),
    "bridge saved": MinitLocationData(
        region="Hotel Room",
        er_region="bridge right",
        locked_item="bridge saved",
        ),
    "hidden saved": MinitLocationData(
        region="Hotel Room",
        er_region="bridge switch left",
        locked_item="hidden saved",
        ),
    "teleporter switch1": MinitLocationData(
        region="Island Shack",
        er_region="teleporter switch1",
        locked_item="teleporter switch1",
        ),
    "teleporter switch4": MinitLocationData(
        region="Island Shack",
        er_region="Overworld island shack",
        locked_item="teleporter switch4",
        ),
    "teleporter switch6": MinitLocationData(
        region="Island Shack",
        er_region="Overworld island shack",
        locked_item="teleporter switch6",
        ),
    "boatguy watered": MinitLocationData(
        region="Desert RV",
        er_region="Overworld desert",
        locked_item="boatguy watered",
        ),
    "left machine": MinitLocationData(
        region="Factory Main",
        er_region="grinder tile",
        locked_item="left machine",
        ),
    "right machine": MinitLocationData(
        region="Factory Main",
        er_region="factory switch tile",
        locked_item="right machine",
        ),
    "bombs exploded": MinitLocationData(
        region="Hotel Room",
        er_region="mine entrance bombs",
        locked_item="bombs exploded",
        )
}
