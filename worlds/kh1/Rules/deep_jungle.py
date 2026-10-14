from rule_builder.rules import Has, Rule

from ._helpers import GLIDE, HIGH_JUMP, HIGH_JUMP_AND_GLIDE
from ._helpers import HIGH_JUMP_OR_GLIDE, by_difficulty, has_key_item_rule


def build_rules() -> dict[str, Rule]:
    slides = has_key_item_rule("Slide 1")

    hippos_lagoon_right_chest_rule = by_difficulty(
        beginner=HIGH_JUMP_AND_GLIDE,
        normal=HIGH_JUMP_OR_GLIDE,
        proud=True,
    )

    return {
        "Deep Jungle Climbing Trees Blue Trinity Chest": Has("Blue Trinity"),
        "Deep Jungle Cavern of Hearts White Trinity Chest": Has("White Trinity") & slides,
        "Deep Jungle Camp Blue Trinity Chest": Has("Blue Trinity"),
        "Deep Jungle Waterfall Cavern Low Chest": slides,
        "Deep Jungle Waterfall Cavern Middle Chest": slides,
        "Deep Jungle Waterfall Cavern High Wall Chest": slides,
        "Deep Jungle Waterfall Cavern High Middle Chest": slides,
        "Deep Jungle Defeat Sabor White Fang Event": slides,
        "Deep Jungle Defeat Clayton Cure Event": slides,
        "Deep Jungle Seal Keyhole Jungle King Event": slides,
        "Deep Jungle Seal Keyhole Red Trinity Event": slides,
        "Deep Jungle Camp Hi-Potion Experiment": Has("Progressive Fire"),
        "Deep Jungle Camp Ether Experiment": Has("Progressive Blizzard"),
        "Deep Jungle Camp Replication Experiment": Has("Progressive Blizzard"),
        "Deep Jungle Cliff Save Gorillas": slides,
        "Deep Jungle Tree House Save Gorillas": slides,
        "Deep Jungle Camp Save Gorillas": slides,
        "Deep Jungle Bamboo Thicket Save Gorillas": slides,
        "Deep Jungle Climbing Trees Save Gorillas": slides,
        "Deep Jungle Cavern of Hearts Navi-G Piece Event": slides,
        "Deep Jungle Treetop Green Trinity": Has("Green Trinity"),
        "Deep Jungle Hippo's Lagoon Right Chest": hippos_lagoon_right_chest_rule,
        "Deep Jungle Tree House Rooftop Chest": by_difficulty(beginner=HIGH_JUMP, proud=True),
        "Deep Jungle Tree House Suspended Boat Chest": by_difficulty(beginner=GLIDE, proud=True),
        "Deep Jungle Jungle Slider 10 Fruits": slides,
        "Deep Jungle Jungle Slider 20 Fruits": slides,
        "Deep Jungle Jungle Slider 30 Fruits": slides,
        "Deep Jungle Jungle Slider 40 Fruits": slides,
        "Deep Jungle Jungle Slider 50 Fruits": slides,
    }
