from rule_builder.rules import Has, Rule

from ._context import RuleContext
from ._helpers import has_key_item_rule, has_offensive_magic_rule


def build_rules(ctx: RuleContext, enabled: bool) -> dict[str, Rule]:
    crystal_trident = has_key_item_rule("Crystal Trident")
    offensive_magic = has_offensive_magic_rule()
    ursula_2_rule = Has("Mermaid Kick") & offensive_magic & crystal_trident

    return {
        "Atlantica Ursula's Lair Use Fire on Urchin Chest": Has("Progressive Fire") & crystal_trident,
        "Atlantica Triton's Palace White Trinity Chest": Has("White Trinity"),
        "Atlantica Defeat Ursula I Mermaid Kick Event": offensive_magic & crystal_trident,
        "Atlantica Defeat Ursula II Thunder Event": ursula_2_rule,
        "Atlantica Seal Keyhole Crabclaw Event": ursula_2_rule,
        "Atlantica Undersea Gorge Blizzard Clam": Has("Progressive Blizzard"),
        "Atlantica Undersea Valley Fire Clam": Has("Progressive Fire"),
        "Atlantica Triton's Palace Thunder Clam": Has("Progressive Thunder"),
        "Atlantica Cavern Nook Clam": crystal_trident,
        "Atlantica Defeat Ursula II Ansem's Report 3": ursula_2_rule,
    } if enabled else {}
