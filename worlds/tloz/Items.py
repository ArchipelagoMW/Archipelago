from BaseClasses import ItemClassification
import typing
from typing import Dict

progression = ItemClassification.progression
filler = ItemClassification.filler
useful = ItemClassification.useful
trap = ItemClassification.trap


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification


item_table: Dict[str, ItemData] = {
    "Boomerang": ItemData(100, useful),
    "Bow": ItemData(101, progression),
    "Magical Boomerang": ItemData(102, useful),
    "Raft": ItemData(103, progression),
    "Stepladder": ItemData(104, progression),
    "Recorder": ItemData(105, progression),
    "Magical Rod": ItemData(106, progression),
    "Red Candle": ItemData(107, progression),
    "Book of Magic": ItemData(108, progression),
    "Magical Key": ItemData(109, useful),
    "Red Ring": ItemData(110, progression),
    "Silver Arrow": ItemData(111, progression),
    "Sword": ItemData(112, progression),
    "White Sword": ItemData(113, progression),
    "Magical Sword": ItemData(114, progression),
    "Heart Container": ItemData(115, progression),
    "Letter": ItemData(116, progression),
    "Magical Shield": ItemData(117, useful),
    "Candle": ItemData(118, progression),
    "Arrow": ItemData(119, progression),
    "Food": ItemData(120, progression),
    "Water of Life (Blue)": ItemData(121, useful),
    "Water of Life (Red)": ItemData(122, useful),
    "Blue Ring": ItemData(123, progression),
    "Triforce Fragment": ItemData(124, progression),
    "Power Bracelet": ItemData(125, useful),
    "Small Key": ItemData(126, filler),
    "Bomb": ItemData(127, filler),
    "Recovery Heart": ItemData(128, filler),
    "Five Rupees": ItemData(129, filler),
    "Rupee": ItemData(130, filler),
    "Clock": ItemData(131, filler),
    "Fairy": ItemData(132, filler)

}

item_game_ids = {
    "Bomb": 0x00,
    "Sword": 0x01,
    "White Sword": 0x02,
    "Magical Sword": 0x03,
    "Food": 0x04,
    "Recorder": 0x05,
    "Candle": 0x06,
    "Red Candle": 0x07,
    "Arrow": 0x08,
    "Silver Arrow": 0x09,
    "Bow": 0x0A,
    "Magical Key": 0x0B,
    "Raft": 0x0C,
    "Stepladder": 0x0D,
    "Five Rupees": 0x0F,
    "Magical Rod": 0x10,
    "Book of Magic": 0x11,
    "Blue Ring": 0x12,
    "Red Ring": 0x13,
    "Power Bracelet": 0x14,
    "Letter": 0x15,
    "Small Key": 0x19,
    "Heart Container": 0x1A,
    "Triforce Fragment": 0x1B,
    "Magical Shield": 0x1C,
    "Boomerang": 0x1D,
    "Magical Boomerang": 0x1E,
    "Water of Life (Blue)": 0x1F,
    "Water of Life (Red)": 0x20,
    "Recovery Heart": 0x22,
    "Rupee": 0x18,
    "Clock": 0x21,
    "Fairy": 0x23
}

# Item prices are going to get a bit of a writeup here, because these are some seemingly arbitrary
# design decisions and future contributors may want to know how these were arrived at.

# First, I based everything off of the Blue Ring. Since the Red Ring is twice as good as the Blue Ring,
# logic dictates it should cost twice as much. Since you can't make something cost 500 rupees, the only
# solution was to halve the price of the Blue Ring. Correspondingly, everything else sold in shops was
# also cut in half.

# Then, I decided on a factor for swords. Since each sword does double the damage of its predecessor, each
# one should be at least double. Since the sword saves so much time when upgraded (as, unlike other items,
# you don't need to switch to it), I wanted a bit of a premium on upgrades. Thus, a 4x multiplier was chosen,
# allowing the basic Sword to stay cheap while making the Magical Sword be a hefty upgrade you'll
# feel the price of.

# Since arrows do the same amount of damage as the White Sword and silver arrows are the same with the Magical Sword.
# they were given corresponding costs.

# Utility items were based on the prices of the shield, keys, and food. Broadly useful utility items should cost more,
# while limited use utility items should cost less. After eyeballing those, a few editorial decisions were made as
# deliberate thumbs on the scale of game balance. Those exceptions will be noted below. In general, prices were chosen
# based on how a player would feel spending that amount of money as opposed to how useful an item actually is.

item_prices = {
    "Bomb": 10,
    "Sword": 10,
    "White Sword": 40,
    "Magical Sword": 160,
    "Food": 30,
    "Recorder": 45,
    "Candle": 30,
    "Red Candle": 60,
    "Arrow": 40,
    "Silver Arrow": 160,
    "Bow": 40,
    "Magical Key": 250,  # Replacing all small keys commands a high premium
    "Raft": 80,
    "Stepladder": 80,
    "Five Rupees": 255,  # This could cost anything above 5 Rupees and be fine, but 255 is the funniest
    "Magical Rod": 100,  # White Sword with forever beams should cost at least more than the White Sword itself
    "Book of Magic": 60,
    "Blue Ring": 125,
    "Red Ring": 250,
    "Power Bracelet": 25,
    "Letter": 20,
    "Small Key": 40,
    "Heart Container": 80,
    "Triforce Fragment": 200,  # Since I couldn't make Zelda 1 track shop purchases, this is how to discourage repeat
    # Triforce purchases. The punishment for endless Rupee grinding to avoid searching out
    # Triforce pieces is that you're doing endless Rupee grinding to avoid playing the game
    "Magical Shield": 45,
    "Boomerang": 5,
    "Magical Boomerang": 20,
    "Water of Life (Blue)": 20,
    "Water of Life (Red)": 34,
    "Recovery Heart": 5,
    "Rupee": 50,
    "Clock": 0,
    "Fairy": 10
}
