from rule_builder.rules import Has, Or, Rule, True_

from ._option_filters import ABOVE_BEGINNER, ABOVE_NORMAL
from ._context import RuleContext
from ._helpers import has_key_item_rule


def build_rules(ctx: RuleContext, jungle_slider: bool) -> dict[str, Rule]:
    slides = has_key_item_rule("Slides")

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

        "Deep Jungle Hippo's Lagoon Right Chest": Or(
            ctx.hj_glide_all, ctx.hj_glide_any & ABOVE_BEGINNER, True_() & ABOVE_NORMAL,
        ),
        "Deep Jungle Tree House Rooftop Chest": Or(ctx.hj1, True_() & ABOVE_NORMAL),
        "Deep Jungle Tree House Suspended Boat Chest": Or(ctx.glide, True_() & ABOVE_NORMAL),

        **({
            "Deep Jungle Jungle Slider 10 Fruits": slides,
            "Deep Jungle Jungle Slider 20 Fruits": slides,
            "Deep Jungle Jungle Slider 30 Fruits": slides,
            "Deep Jungle Jungle Slider 40 Fruits": slides,
            "Deep Jungle Jungle Slider 50 Fruits": slides,
        } if jungle_slider else {}),
    }
