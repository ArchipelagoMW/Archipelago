from rule_builder.rules import Has, HasAll, HasAllCounts, Or, Rule

from worlds.generic.Rules import add_item_rule
from ._constants import ALL_ARTS, ALL_SUMMON_GEMS
from ._option_filters import ABOVE_BEGINNER, ABOVE_NORMAL, ABOVE_PROUD
from ._context import RuleContext
from ._helpers import has_all_magic_lvx_rule, has_item_workshop_rule, has_puppies_rule, has_x_worlds_rule_pinned_to_beginner


def build_rules(ctx: RuleContext, kh1world) -> dict[str, Rule]:
    player = kh1world.player
    item_workshop = has_item_workshop_rule()
    secret_waterway_rule = Has("Red Trinity")  # Alleyway gate to the Secret Waterway
    synth_items_rule = HasAllCounts({"Orichalcum": 17, "Mythril": 16}) & item_workshop

    inner_normal = (
        ctx.dumbo_summon
        | ctx.hj3
        | (ctx.combo_master & (ctx.dodge_airguard_all | ctx.hj2 | (ctx.hj1 & Has("Air Combo Plus", count=2))))
    )
    inner_proud = (
        Has("Mermaid Kick")
        | ctx.dodge_airguard_all
        | (ctx.combo_master & (ctx.hj1 | Has("Air Combo Plus", count=2)))
    )

    for i in range(33):
        add_item_rule(
            kh1world.get_location(f"Traverse Town Synth Item {i + 1:02}"),
            lambda item, _player=player: (item.player != _player or item.name not in ("Orichalcum", "Mythril")),
        )

    return {
        "Traverse Town 1st District Candle Puzzle Chest": Has("Progressive Blizzard"),
        "Traverse Town 1st District Accessory Shop Roof Chest": ctx.hj1,
        "Traverse Town Secret Waterway White Trinity Chest": secret_waterway_rule & Has("White Trinity"),
        "Traverse Town Secret Waterway Near Stairs Chest": secret_waterway_rule,
        "Traverse Town Leon Secret Waterway Earthshine Event": secret_waterway_rule,
        "Traverse Town Geppetto's House Chest": ctx.parasite_cage,
        "Traverse Town Item Workshop Right Chest": item_workshop,
        "Traverse Town Item Workshop Left Chest": item_workshop,
        "Traverse Town Alleyway Behind Crates Chest": Has("Red Trinity"),
        "Traverse Town Defeat Opposite Armor Aero Event": Has("Red Trinity"),
        "Traverse Town Defeat Opposite Armor Navi-G Piece Event": Has("Red Trinity"),
        "Traverse Town Magician's Study Obtained All LV1 Magic": has_all_magic_lvx_rule(1),
        "Traverse Town Magician's Study Obtained All LV3 Magic": has_all_magic_lvx_rule(3),
        "Traverse Town Gizmo Shop Postcard 1": Has("Progressive Thunder"),
        "Traverse Town Gizmo Shop Postcard 2": Has("Progressive Thunder"),
        "Traverse Town Item Workshop Postcard": item_workshop,
        "Traverse Town Geppetto's House Postcard": ctx.parasite_cage,
        "Traverse Town 1st District Blue Trinity by Exit Door": Has("Blue Trinity"),
        "Traverse Town 3rd District Blue Trinity": Has("Blue Trinity"),
        "Traverse Town Magician's Study Blue Trinity": HasAll("Blue Trinity", "Progressive Fire"),
        "Traverse Town Magician's Study Earthshine Event": HasAll("Progressive Fire", "Earthshine"),
        "Traverse Town Magician's Study Naturespark Event": HasAll("Progressive Fire", "Naturespark"),
        "Traverse Town Magician's Study Watergleam Event": HasAll("Progressive Fire", "Watergleam"),
        "Traverse Town Magician's Study Fireglow Event": HasAll("Progressive Fire", "Fireglow"),
        "Traverse Town Magician's Study Lord Fortune Event": HasAll("Progressive Fire", *ALL_SUMMON_GEMS),

        "Traverse Town Mystical House Yellow Trinity Chest": Has("Progressive Fire") & Or(
            Has("Yellow Trinity"),
            ctx.hj2 & ABOVE_BEGINNER,
            ctx.hj1 & ABOVE_NORMAL,
            ctx.dumbo_summon,
        ),
        "Traverse Town 1st District Blue Trinity Balcony Chest": Or(
            Has("Blue Trinity") & ctx.glide,
            ctx.glide & ABOVE_NORMAL,
            ctx.dumbo_summon & ABOVE_PROUD,
        ),
        "Traverse Town Mystical House Glide Chest": Has("Progressive Fire") & Or(
            ctx.glide,
            inner_normal & ABOVE_NORMAL,
            inner_proud & ABOVE_PROUD,
        ),
        "Traverse Town Kairi Secret Waterway Oathkeeper Event": secret_waterway_rule,
        "Traverse Town Secret Waterway Navi Gummi Event": secret_waterway_rule,
        "Traverse Town Geppetto's House Geppetto Reward Hyperion Blueprint": (
            ctx.parasite_cage & HasAll("Progressive Fire", *ALL_SUMMON_GEMS)
        ),
        "Traverse Town Geppetto's House Pinocchio Reward Chocobo Blueprint": ctx.parasite_cage,
        "Traverse Town Magician's Study Obtained All Arts Items": (
            has_all_magic_lvx_rule(1)
            & HasAll(*ALL_ARTS)
            & has_x_worlds_rule_pinned_to_beginner(8)
        ),
        "Traverse Town Synth 15 Items": Or(
            HasAllCounts({"Orichalcum": 6, "Mythril": 9}),
            HasAllCounts({"Orichalcum": 7, "Mythril": 8}),
            HasAllCounts({"Orichalcum": 8, "Mythril": 7}),
            HasAllCounts({"Orichalcum": 9, "Mythril": 6}),
        ) & item_workshop,

        **{f"Traverse Town Mail Postcard {i:02} Event": Has("Postcard", count=i) for i in range(1, 11)},
        **{
            f"Traverse Town Geppetto's House Geppetto Reward {blueprint} Blueprint": ctx.parasite_cage
            for blueprint in ("Cid", "Geppetto", "Aerith", "Yuffie", "Leon", "Cactaur")
        },
        **{
            f"Traverse Town Piano Room {suffix}": has_puppies_rule(amount)
            for amount, suffix in (
                (10, "Return 10 Puppies"), (20, "Return 20 Puppies"), (30, "Return 30 Puppies"),
                (40, "Return 40 Puppies"), (50, "Return 50 Puppies Reward 1"), (50, "Return 50 Puppies Reward 2"),
                (60, "Return 60 Puppies"), (70, "Return 70 Puppies"), (80, "Return 80 Puppies"),
                (90, "Return 90 Puppies"), (99, "Return 99 Puppies Reward 1"), (99, "Return 99 Puppies Reward 2"),
            )
        },
        **{f"Traverse Town Synth Item {i + 1:02}": synth_items_rule for i in range(33)},
    }
