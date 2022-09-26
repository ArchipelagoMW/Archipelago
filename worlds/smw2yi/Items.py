import typing
from BaseClasses import Item, ItemClassification
from .Names import ItemName

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    quantity: int = 1
    event: bool = False


class YoshiItem(Item): 
    game: str = "Yoshis Island"


level_panels = {
    ItemName.flip_cards: ItemData(0x16001, True),
    ItemName.scratch_cards: ItemData(0x16002, False),
    ItemName.draw_lots: ItemData(0x16003, False),
    ItemName.match_cards: ItemData(0x16004, True),
    ItemName.roulette: ItemData(0x16005, False),
    ItemName.slot_machine: ItemData(0x16006, False),
    ItemName.extra_panels: ItemData(0x16007, True),

}

sprite_item_table = {
    ItemName.spring_ball: ItemData(0x16008, True),
    ItemName.large_spring: ItemData(0x16009, True),
    ItemName.push_switch: ItemData(0x1600A, True),
    ItemName.dashed_platform: ItemData(0x1600B, True),
    ItemName.dashed_stairs: ItemData(0x1600C, True),
    ItemName.bean_stalk: ItemData(0x1600D, True),
    ItemName.helicopter: ItemData(0x1600E, True),
    ItemName.mole_tank: ItemData(0x1600F, True),
    ItemName.car: ItemData(0x16010, False),
    ItemName.submarine: ItemData(0x16011, True),
    ItemName.train: ItemData(0x16012, True),
    ItemName.arrow_wheel: ItemData(0x16013, True),
    ItemName.v_wheel: ItemData(0x16014, True),
    ItemName.water_melon: ItemData(0x16015, True),
    ItemName.fire_melon: ItemData(0x16016, True),
    ItemName.ice_melon: ItemData(0x16017, True),
    ItemName.super_star: ItemData(0x16018, True),
    ItemName.flashing_egg: ItemData(0x16019, True),
    ItemName.giant_egg: ItemData(0x1601A, True),
    ItemName.egg_launcher: ItemData(0x1601B, True),
    ItemName.egg_plant: ItemData(0x1601C, True),
    ItemName.chomp_rock: ItemData(0x1601D, True),
    ItemName.poochy: ItemData(0x1601E, True),
    ItemName.platform_ghost: ItemData(0x1601F, True),
    ItemName.skis: ItemData(0x16020, True),
    ItemName.key: ItemData(0x16021, True),
    ItemName.mid_ring: ItemData(0x16022, False),
    ItemName.tulip: ItemData(0x16023, True),
    ItemName.bucket: ItemData(0x16024, True),
}

ability_table = {
    ItemName.egg_upgrade: ItemData(0x16025, True),
    #ItemName.spike_breaker: ItemData(0x16026, True),
    #ItemName.flutter: ItemData(0x16027, True),
    #ItemName.ground_pound: ItemData(0x16028, True),
    #ItemName.egg_strength: ItemData(0x16029, True),
}

pause_item_table = {
    ItemName.full_eggs: ItemData(0x1602A, False),
    ItemName.any_pow: ItemData(0x1602B, False),
    ItemName.winged_cloud: ItemData(0x1602C, False),
    ItemName.super_melon: ItemData(0x1602D, False),
    ItemName.super_fire_melon: ItemData(0x1602E, False),
    ItemName.super_ice_melon: ItemData(0x1602F, False),
    ItemName.magnifying_glass: ItemData(0x16031, False),
    ItemName.ten_stars: ItemData(0x16032, False),
    ItemName.twenty_stars: ItemData(0x16033, False),

}

trap_table = {
    ItemName.fuzzy_trap: ItemData(0x16034, False),
    ItemName.reverse_trap: ItemData(0x16035, False),
    ItemName.ten_trap: ItemData(0x16036, False),
    ItemName.twenty_trap: ItemData(0x16037, False),
}

world_gates = {
    ItemName.world1_gate: ItemData(0x16038, True),
    ItemName.world2_gate: ItemData(0x16039, True),
    ItemName.world3_gate: ItemData(0x1603A, True),
    ItemName.world4_gate: ItemData(0x1603B, True),
    ItemName.world5_gate: ItemData(0x1603C, True),
    ItemName.world6_gate: ItemData(0x1603D, True),
}

event_goals = {
    ItemName.bc_unlock: ItemData(0x1603E, True),
    ItemName.bc_door: ItemData(0x1603F, True),
    ItemName.victory: ItemData(0x16040, True),
}

item_table = {
    **level_panels,
    **sprite_item_table,
    **ability_table,
    **pause_item_table,
    **trap_table,
    **world_gates,
    **event_goals,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}