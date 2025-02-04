from typing import Set
from .items import (
    tier_1_opponents,
    tier_2_opponents,
    tier_3_opponents,
    tier_4_opponents,
    tier_5_opponents,
    core_booster,
    challenges, booster_packs,
    Banlist_Items,
)

from .locations import (
    Bonuses, Campaign_Opponents, special, Limited_Duels, Theme_Duels, Required_Cards,
)

trivial_bonus: Set = {
    "Duelist Bonus Level 1",
    "Duelist Bonus Level 2",
    "Duelist Bonus Level 3",
    "Duelist Bonus Level 4",
    "Duelist Bonus Level 5",
    "Battle Damage",
    "Battle Damage Only Bonus",
    "Destroyed in Battle Bonus",
    "Spell Card Bonus",
    "Trap Card Bonus",
}

easy_bonus: Set = {
    "Max ATK Bonus",
    "Tribute Summon Bonus",
    "No Special Summon Bonus",
    "No Spell Cards Bonus",
    "No Trap Cards Bonus",
    "No Damage Bonus",
    "Exactly 0 LP Bonus",
    "Reversal Finish Bonus",
    "Quick Finish Bonus"
}

medium_bonus: Set = {
    "Max Damage Bonus",
    "Fusion Summon Bonus",
    "Ritual Summon Bonus",
    "Low LP Bonus",
    "Opponent's Turn Finish Bonus",
    "Skull Servant Finish Bonus"
}

hard_bonus: Set = {
    "Over 20000 LP Bonus",
    "Extremely Low LP Bonus",
    "Low Deck Bonus",
    "Extremely Low Deck Bonus",
    "Effect Damage Only Bonus",
    "No More Cards Bonus",
    "Exodia Finish Bonus",
    "Last Turn Finish Bonus",
    "Final Countdown Finish Bonus",
    "Destiny Board Finish Bonus",
    "Yata-Garasu Finish Bonus",
    "Konami Bonus"
}

item_groups = {
    "Core Booster": frozenset(core_booster),
    "Campaign Boss Beaten": {"Tier 1 Beaten", "Tier 2 Beaten", "Tier 3 Beaten", "Tier 4 Beaten", "Tier 5 Beaten"},
    "Booster Pack": frozenset(booster_packs),
    "Banlist": frozenset(Banlist_Items),
    "Challenge": frozenset(challenges),
    "Tier 1 Opponent": frozenset(tier_1_opponents),
    "Tier 2 Opponent": frozenset(tier_2_opponents),
    "Tier 3 Opponent": frozenset(tier_3_opponents),
    "Tier 4 Opponent": frozenset(tier_4_opponents),
    "Tier 5 Opponent": frozenset(tier_5_opponents),
    "Campaign Opponent": frozenset(tier_1_opponents + tier_2_opponents + tier_3_opponents +
                             tier_4_opponents + tier_5_opponents)
}

easy_challenge = {
    "LD01 All except Level 4 forbidden",
    "LD02 Medium/high Level forbidden",
    "LD04 Flip Effects forbidden",
    "LD05 Tributes forbidden",
    "LD06 Traps forbidden",
    "LD07 Large Deck A",
    "LD08 Large Deck B",
    "LD14 Level 3 or below forbidden",
    "LD23 Refer to Mar 05 Banlist",
    "LD24 Refer to Sept 04 Banlist",
    "LD25 Low Life Points",
    "LD33 Special Summons forbidden",
    "LD38 Refer to Mar 04 Banlist",
    "LD40 Refer to Sept 05 Banlist",
    "LD41 Refer to Sept 03 Banlist",
    "TD01 Battle Damage",
    "TD03 Normal Summon",
    "TD10 During Opponent's Turn",
    "TD29 Destroy Monsters in Battle",
}

medium_challenge = {
    "LD03 ATK 1500 or more forbidden",
    "LD09 Sets Forbidden",
    "LD12 All except Wind forbidden",
    "LD11 All except Fairies forbidden",
    "LD13 All except monsters forbidden",
    "LD15 DEF 1500 or less forbidden",
    "LD16 Effect Monsters forbidden",
    "LD17 Spells forbidden",
    "LD20 All except Warriors forbidden",
    "LD21 All except Dark forbidden",
    "LD22 All limited cards forbidden",
    "LD28 All except Dragons forbidden",
    "LD29 All except Spellcasters forbidden",
    "LD30 All except Light forbidden",
    "LD31 All except Fire forbidden",
    "LD32 Decks with multiples forbidden",
    "LD35 All except Zombies forbidden",
    "LD36 All except Earth forbidden",
    "LD37 All except Water forbidden",
    "TD02 Deflected Damage",
    "TD05 Special Summon A",
    "TD06 20x Spell",
    "TD07 10x Trap",
    "TD08 Draw",
    "TD11 Recover",
    "TD12 Remove Monsters by Effect",
    "TD13 Flip Summon",
    "TD14 Special Summon B",
    "TD15 Token",
    "TD16 Union",
    "TD28 Direct Damage",
    "TD30 Tribute Summon",
    "TD40 Make a Chain",
    "TD42 Serious Damage",
    "TD43 Return Monsters with Effects",
    "TD45 Big Damage at once",
    "TD47 Spell Counter",
    "TD48 Destroy Monsters with Effects"
}

hard_challenge = {
    "LD10 All except LV monsters forbidden",
    "LD18 Attacks forbidden",
    "LD19 All except E-Hero's forbidden",
    "LD26 All except Toons forbidden",
    "LD27 All except Spirits forbidden",
    "LD34 Normal Summons forbidden",
    "LD39 Monsters forbidden",
    "TD04 Ritual Summon",
    "TD09 Hand Destruction",
    "TD17 10x Quick Spell",
    "TD18 The Forbidden",
    "TD19 20 Turns",
    "TD20 Deck Destruction",
    "TD21 Victory D.",
    "TD22 The Preventers Fight Back",
    "TD23 Huge Revolution",
    "TD24 Victory in 5 Turns",
    "TD25 Moth Grows Up",
    "TD26 Magnetic Power",
    "TD27 Dark Sage",
    "TD31 Special Summon C",
    "TD32 Toon",
    "TD33 10x Counter",
    "TD34 Destiny Board",
    "TD35 Huge Damage in a Turn",
    "TD36 V-Z In the House",
    "TD37 Uria, Lord of Searing Flames",
    "TD38 Hamon, Lord of Striking Thunder",
    "TD39 Raviel, Lord of Phantasms",
    "TD41 The Gatekeeper Stands Tall",
    "TD44 Fusion Summon",
    "TD46 XYZ In the House",
    "TD49 Plunder",
    "TD50 Dark Scorpion Combination"
}

location_groups = {
    "Campaign Bonus": set(Bonuses.keys()),
    "Limited Duel": set(Limited_Duels.keys()),
    "Theme Duel": set(Theme_Duels.keys()),
    "Challenge": set(list(Limited_Duels.keys()) + list(Theme_Duels.keys())),
    "Campaign Opponent": set(list(Campaign_Opponents.keys()) + list(special.keys())),
    "Card Requirement": set(Required_Cards.keys()),
    "Trivial Bonus": trivial_bonus,
    "Easy Bonus": easy_bonus,
    "Medium Bonus": medium_bonus,
    "Hard Bonus": hard_bonus,
    "Easy Challenge": easy_challenge,
    "Medium Challenge": medium_challenge,
    "Hard Challenge": hard_challenge
}
