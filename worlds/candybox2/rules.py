from worlds.candybox2 import CandyBox2Options, CandyBox2World
from worlds.generic.Rules import set_rule


def set_rules(world: CandyBox2World, options: CandyBox2Options, player: int):
    set_rule(world.multiworld.get_entrance("candy_box_to_village", player), lambda state: True)
    pass