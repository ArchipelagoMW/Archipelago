import logging
from typing import List, NamedTuple, Callable, Dict

from worlds.yugioh06 import cards
from worlds.yugioh06.boosterpack_contents import not_in_standard_pool
from worlds.yugioh06.card_data import nomi_monsters
from worlds.yugioh06.structure_deck import structure_contents

logger = logging.getLogger("card_rules")


class InnerCardRule(NamedTuple):
    cards: str | List[str] | Callable
    min_amount: int
    amount_protocol: str = "total"


class CardRule(NamedTuple):
    cards: str | List[str] | Callable
    min_amount: int
    amount_protocol: str = "total"
    additional_cards: InnerCardRule | List[InnerCardRule] | Callable = []


def set_card_rules(world):
    evergreen_rules = {
        "Max ATK Bonus": raise_attack,
        "Skull Servant Finish Bonus":
            CardRule("Skull Servant", 1),
        "Konami Bonus":
            [CardRule(["Messenger of Peace", "Castle of Dark Illusions", "Mystik Wok"], 1,
                      amount_protocol="each"),
             CardRule(["Mystik Wok", "Barox", "Cyber-Stein",
                       "Poison of the Old Man"], 1, amount_protocol="each")],
        "Max Damage Bonus":
            CardRule(["Wave-Motion Cannon", "Megamorph", "United We Stand",
                      "Mage Power"], 1),
        "Low LP Bonus":
            CardRule(["Wall of Revealing Light"], 1),
        "Extremely Low LP Bonus":
            CardRule(["Wall of Revealing Light", "Messenger of Peace"], 1, amount_protocol="each",
                     additional_cards=InnerCardRule(
                         cards=lambda: {name for name, c in cards.items() if c.attack % 100 != 0 and c.level <= 4},
                         min_amount=1)),
        "Effect Damage Only Bonus":
            [CardRule(["Solar Flare Dragon", "UFO Turtle"], 2, amount_protocol="each"),
             CardRule(["Wave-Motion Cannon"], 3)],
        "No More Cards Bonus":
            CardRule(["Morphing Jar", "Morphing Jar #2", "Needle Worm"], 1,
                     additional_cards=InnerCardRule(["The Shallow Grave", "Spear Cretin"], 2)),
        "Final Countdown Finish Bonus":
            CardRule(["Final Countdown"], 1),
        "Destiny Board Finish Bonus":
            CardRule(["A Cat of Ill Omen"], 3),

        # Cards
        "Obtain Final Countdown":
            CardRule(["Final Countdown"], 1),
        "Obtain Victory Dragon":
            CardRule(["Victory D."], 1),
        "Obtain Hamon, Lord of Striking Thunder":
            CardRule(["Hamon, Lord of Striking Thunder"], 1),
        "Obtain Raviel, Lord of Phantasms":
            CardRule(["Raviel, Lord of Phantasms"], 1),
        "Obtain Uria, Lord of Searing Flames":
            CardRule(["Uria, Lord of Searing Flames"], 1),

        # Collection Events
        "Ojama Delta Hurricane and required cards":
            CardRule(["Ojama Delta Hurricane", "Ojama Green", "Ojama Yellow",
                      "Ojama Black"], 1, amount_protocol="each"),
        "Huge Revolution and its required cards":
            CardRule(["Huge Revolution", "Oppressed People", "United Resistance",
                      "People Running About"], 1, amount_protocol="each"),
        "Perfectly Ultimate Great Moth and its required cards":
            CardRule(["Perfectly Ultimate Great Moth", "Petit Moth",
                      "Cocoon of Evolution"], 1,
                     amount_protocol="each"),
        "Valkyrion the Magna Warrior and its pieces":
            CardRule(["Valkyrion the Magna Warrior",
                      "Alpha the Magnet Warrior", "Beta the Magnet Warrior",
                      "Gamma the Magnet Warrior"], 1, amount_protocol="each"),
        "Dark Sage and its required cards":
            CardRule(["Dark Sage", "Dark Magician", "Time Wizard"], 1, amount_protocol="each"),
        "Destiny Board and its letters":
            CardRule(["Destiny Board", "Spirit Message 'I'", "Spirit Message 'N'",
                      "Spirit Message 'A'", "Spirit Message 'L'"], 1, amount_protocol="each"),
        "XYZ-Dragon Cannon fusions and their materials":
            CardRule(["X-Head Cannon", "Y-Dragon Head", "Z-Metal Tank",
                      "XY-Dragon Cannon", "XZ-Tank Cannon",
                      "YZ-Tank Dragon", "XYZ-Dragon Cannon"], 1,
                     amount_protocol="each"),
        "VWXYZ-Dragon Catapult Cannon and the fusion materials":
            CardRule(["X-Head Cannon", "Y-Dragon Head",
                      "Z-Metal Tank", "XYZ-Dragon Cannon",
                      "V-Tiger Jet", "W-Wing Catapult",
                      "VW-Tiger Catapult",
                      "VWXYZ-Dragon Catapult Cannon"], 1,
                     amount_protocol="each"),
        "Gate Guardian and its pieces":
            CardRule(["Gate Guardian", "Kazejin", "Suijin", "Sanga of the Thunder"], 1,
                     amount_protocol="each"),
        "Dark Scorpion Combination and its required cards":
            CardRule(["Dark Scorpion Combination", "Don Zaloog",
                      "Dark Scorpion - Chick the Yellow",
                      "Dark Scorpion - Meanae the Thorn",
                      "Dark Scorpion - Gorg the Strong",
                      "Cliff the Trap Remover"], 1,
                     amount_protocol="each"),

        # Events
        "Exodia":
            CardRule(["Exodia the Forbidden One", "Left Arm of the Forbidden One",
                      "Right Arm of the Forbidden One", "Left Leg of the Forbidden One",
                      "Right Leg of the Forbidden One", "Heart of the Underdog"], min_amount=1,
                     amount_protocol="each"),
        "Can Exodia Win":
            CardRule(["Heart of the Underdog"], min_amount=1,
                     amount_protocol="each"),
        "Can Last Turn Win":
            [CardRule(["Last Turn", "Wall of Revealing Light"], 1, "each",
                      InnerCardRule(["Jowgen the Spiritualist", "Jowls of Dark Demise", "Non Aggression Area"], 3)),
             CardRule(["Last Turn", "Wall of Revealing Light"], 1, "each",
                      InnerCardRule(["Cyber-Stein", "The Last Warrior from Another Planet"], 3)),
             ],
        "Can Yata Lock": CardRule(["Yata-Garasu", "Chaos Emperor Dragon - Envoy of the End", "Sangan"], 1, "each"),
        "Can Stall with Monsters": CardRule(["Spirit Reaper", "Giant Germ", "Marshmallon", "Nimble Momonga"], 6),
        "Can Stall with ST": CardRule(["Level Limit - Area B", "Gravity Bind", "Messenger of Peace"], 4),
        "Can Gain LP Every Turn":
            CardRule(["Solemn Wishes", "Cure Mermaid",
                      "Dancing Fairy", "Princess Pikeru", "Kiseitai"], 9),
        "Can Self Mill":
            CardRule(["Reasoning", "Monster Gate", "Magical Merchant"], 3),
    }

    challenge_rules = {
        # Limited
        "LD01 All except Level 4 forbidden": CardRule(cards=lambda: find_cards_with(min_attack=1700, max_attack=2000,
                                                                                    min_level=4, max_level=4),
                                                      min_amount=12),
        "LD02 Medium/high Level forbidden": CardRule(cards=lambda: find_cards_with(min_attack=1700, max_attack=2000,
                                                                                   max_level=4), min_amount=12),
        "LD03 ATK 1500 or more forbidden": CardRule(cards=lambda: find_cards_with(min_attack=1300, max_attack=1500,
                                                                                  max_level=4), min_amount=12),
        "LD10 All except LV monsters forbidden": only_level(),
        "LD11 All except Fairies forbidden": only_fairy(),
        "LD12 All except Wind forbidden": only_wind(),
        "LD14 Level 3 or below forbidden": CardRule(cards=lambda: find_cards_with(min_attack=1700, max_attack=2000,
                                                                                  min_level=4, max_level=4), min_amount=12),
        "LD15 DEF 1500 or less forbidden": CardRule(cards=lambda: find_cards_with(min_attack=1500, max_attack=2000,
                                                                                  min_defence=1550, max_level=4),
                                                    min_amount=12),
        "LD16 Effect Monsters forbidden": only_normal(),
        "LD18 Attacks forbidden": CardRule(["Wave-Motion Cannon", "Stealth Bird"], 3,"each",
                                           InnerCardRule(["Dark World Lightning", "Nobleman of Crossout",
                                                          "Shield Crash", "Tribute to the Doomed"], 4)),
        "LD20 All except Warriors forbidden": only_warrior(),
        "LD21 All except Dark forbidden": only_dark(),
        "LD30 All except Light forbidden": only_light(),
    }

    rules = {**evergreen_rules, **{k: v for k, v in challenge_rules.items() if k not in world.removed_challenges}}

    progression_cards = world.progression_cards
    cards_in_booster = world.progression_cards_in_booster
    cards_in_starter = world.progression_cards_in_start

    # gather cards from starter and structure
    starting_cards: Dict[str, int] = {}
    if world.structure_deck:
        for card in world.structure_deck:
            starting_cards[card.name] = world.structure_deck[card]
    else:
        starting_cards = structure_contents[world.options.structure_deck.current_key]
    if world.starter_deck:
        for card in world.starter_deck:
            if card.name in starting_cards:
                starting_cards[card.name] += world.starter_deck[card]
            else:
                starting_cards[card.name] = world.starter_deck[card]
    elif world.options.starter_deck.value != world.options.starter_deck.option_remove:
        for card, amount in structure_contents["starter"].items():
            if card in starting_cards:
                starting_cards[card] += amount
            else:
                starting_cards[card] = amount

    for location, rule in rules.items():
        if isinstance(rule, List):
            world.random.shuffle(rule)
            chosen_rule = None
            # chose a rule that uses cards in the starting cards.
            # Only works as intended if a all elements in list have 1 card in main rule
            for r in rule:
                rule_cards = []
                if isinstance(r.cards, str):
                    rule_cards.append(r.cards)
                if isinstance(r.cards, List):
                    rule_cards = r.cards
                overlap = [x for x in rule_cards if x in starting_cards.keys()]
                if len(overlap) > 0:
                    chosen_rule = r
                    break
            if chosen_rule is None:
                chosen_rule = world.random.choice(rule)
        elif isinstance(rule, CardRule):
            chosen_rule = rule
        elif isinstance(rule, Callable):
            chosen_rule = rule()
        else:
            logger.critical("Rule for \"" + location + "\" was skipped")
            continue
        chosen_cards, chosen_starters = resolve_rule(world, chosen_rule, starting_cards)
        progression_cards[location] = chosen_cards
        progression_cards[location].extend(chosen_starters)
        cards_in_booster.extend(chosen_cards)
        cards_in_starter.extend(chosen_starters)
        if chosen_rule.additional_cards:
            if isinstance(chosen_rule.additional_cards, List):
                for a_rule in chosen_rule.additional_cards:
                    chosen_cards, chosen_starters = resolve_rule(world, a_rule, starting_cards)
                    progression_cards[location].extend(chosen_cards)
                    progression_cards[location].extend(chosen_starters)
                    cards_in_booster.extend(chosen_cards)
                    cards_in_starter.extend(chosen_starters)
            else:
                chosen_rule = chosen_rule.additional_cards
                chosen_cards, chosen_starters = resolve_rule(world, chosen_rule, starting_cards)
                progression_cards[location].extend(chosen_cards)
                progression_cards[location].extend(chosen_starters)
                cards_in_booster.extend(chosen_cards)
                cards_in_starter.extend(chosen_starters)


def resolve_rule(world, rule, starter_cards: Dict[str, int]):
    potential_cards: List[str] = []
    if isinstance(rule.cards, str):
        potential_cards.append(rule.cards)
    if isinstance(rule.cards, Callable):
        potential_cards.extend(rule.cards())
    if isinstance(rule.cards, List):
        potential_cards.extend(rule.cards)
    if rule.amount_protocol == "total":
        overlap = [x for x in potential_cards if x in starter_cards.keys()]
        potential_cards = [x for x in potential_cards if x in overlap or x not in not_in_standard_pool]
        a = 0
        chosen_starters: List[str] = []
        potential_starters: List[str] = []
        for c in overlap:
            a += starter_cards[c]
            if starter_cards[c] == 3:
                potential_cards.remove(c)
            potential_starters.append(c)
            if a >= rule.min_amount:
                return [], potential_starters
        world.random.shuffle(potential_cards)
        chosen_cards = []
        i = 0
        while a < rule.min_amount and i < len(potential_cards):
            chosen_cards.append(potential_cards[i])
            if potential_cards[i] in overlap:
                a += 3 - starter_cards[potential_cards[i]]
                potential_starters.remove(potential_cards[i])
            else:
                a += 3
            i += 1
        return chosen_cards, potential_starters
    else:
        chosen_starters: List[str] = []
        chosen_cards: List[str] = []
        for card in potential_cards:
            if card in starter_cards and starter_cards[card] >= rule.min_amount:
                chosen_starters.append(card)
            else:
                chosen_cards.append(card)
        return chosen_cards, chosen_starters


def only_light():
    beaters = [
        "Dunames Dark Witch",
        "X-Head Cannon",
        "Homunculus the Alchemic Being",
        "Hysteric Fairy",
        "Ninja Grandmaster Sasuke"
    ]
    big_beaters = [
        "Chaos Command Magician",
        "Cybernetic Magician",
        "Kaiser Glider",
        "The Agent of Judgment - Saturn",
        "Zaborg the Thunder Monarch",
        "Cyber Dragon"
    ]
    utility = [
        "D.D. Warrior Lady",
        "Mystic Swordsman LV2",
        "Y-Dragon Head",
        "Z-Metal Tank",
    ]
    return CardRule(utility + beaters, min_amount=6, additional_cards=[
        InnerCardRule(big_beaters, min_amount=1),
        InnerCardRule(["Shining Angel"], min_amount=3),
    ])


def only_dark():
    beaters = [
        "Dark Elf",
        "Archfiend Soldier",
        "Mad Dog of Darkness",
        "Vorse Raider",
        "Skilled Dark Magician",
        "Skull Descovery Knight",
        "Mechanicalchaser",
        "Dark Blade",
        "Gil Garth",
        "La Jinn the Mystical Genie of the Lamp",
        "Opticlops",
        "Zure, Knight of Dark World",
        "Brron, Mad King of Dark World",
        "D.D. Survivor",
        "Exarion Universe",
        "Kycoo the Ghost Destroyer",
        "Regenerating Mummy"
    ]
    big_beaters = [
        "Summoned Skull",
        "Skull Archfiend of Lightning",
        "The End of Anubis",
        "Dark Ruler Ha Des",
        "Beast of Talwar",
        "Inferno Hammer",
        "Jinzo",
        "Ryu Kokki"
    ]
    utility = [
        "Legendary Fiend",
        "Don Zaloog",
        "Newdoria",
        "Sangan",
        "Spirit Reaper",
        "Giant Germ"
    ]
    return CardRule(utility + beaters, min_amount=9, additional_cards=[
        InnerCardRule(big_beaters, min_amount=1),
        InnerCardRule(["Mystic Tomato"], min_amount=3),
    ])


def only_earth():
    beaters = [
        "Berserk Gorilla",
        "Gemini Elf",
        "Insect Knight",
        "Toon Gemini Elf",
        "Familiar-Possessed - Aussa",
        "Neo Bug",
        "Blindly Loyal Goblin",
        "Chiron the Mage",
        "Gearfried the Iron Knight"
    ]
    big_beaters = [
        "Dark Driceratops",
        "Granmarg the Rock Monarch",
        "Hieracosphinx",
        "Saber Beetle"
    ]
    utility = [
        "Hyper Hammerhead",
        "Green Gadget",
        "Red Gadget",
        "Yellow Gadget",
        "Dimensional Warrior",
        "Enraged Muka Muka",
        "Exiled Force"
    ]
    return CardRule(utility + beaters, min_amount=6, additional_cards=[
        InnerCardRule(big_beaters, min_amount=1),
        InnerCardRule(["Giant Rat"], min_amount=3),
    ])


def only_water():
    beaters = [
        "Gagagigo",
        "Familiar-Possessed - Eria",
        "7 Colored Fish",
        "Sea Serpent Warrior of Darkness",
        "Abyss Soldier"
    ]
    big_beaters = [
        "Giga Gagagigo",
        "Amphibian Beast",
        "Terrorking Salmon",
        "Mobius the Frost Monarch"
    ]
    utility = [
        "Revival Jam",
        "Yomi Ship",
        "Treeborn Frog"
    ]
    return CardRule(utility + beaters, min_amount=6, additional_cards=[
        InnerCardRule(big_beaters, min_amount=1),
        InnerCardRule(["Mother Grizzly"], min_amount=3),
    ])


def only_fire():
    beaters = [
        "Blazing Inpachi",
        "Familiar-Possessed - Hiita",
        "Great Angus",
        "Fire Beaters"
    ]
    big_beaters = [
        "Thestalos the Firestorm Monarch",
        "Horus the Black Flame Dragon LV6"
    ]
    utility = [
        "Solar Flare Dragon",
        "Tenkabito Shien",
        "Ultimate Baseball Kid"
    ]
    return CardRule(utility + beaters, min_amount=6, additional_cards=[
        InnerCardRule(big_beaters, min_amount=1),
        InnerCardRule(["UFO Turtle"], min_amount=3),
    ])


def only_wind():
    beaters = [
        "Luster Dragon",
        "Slate Warrior",
        "Spear Dragon",
        "Familiar-Possessed - Wynn",
        "Harpie's Brother",
        "Nin-Ken Dog",
        "Cyber Harpie Lady",
        "Oxygeddon"
    ]
    big_beaters = [
        "Cyber-Tech Alligator",
        "Luster Dragon #2",
        "Armed Dragon LV5",
        "Roc from the Valley of Haze"
    ]
    utility = [
        "Armed Dragon LV3",
        "Twin-Headed Behemoth",
        "Harpie Lady 1"
    ]
    return CardRule(utility + beaters, min_amount=6, additional_cards=[
        InnerCardRule(big_beaters, min_amount=1),
        InnerCardRule(["UFO Turtle"], min_amount=3),
    ])


def only_warrior():
    beaters = [
        "Dark Blade",
        "Blindly Loyal Goblin",
        "D.D. Survivor",
        "Gearfried the Iron knight",
        "Ninja Grandmaster Sasuke",
    ]
    big_beaters = [
        "Freed the Matchless General",
        "Holy Knight Ishzark",
        "Silent Swordsman LV5"
    ]
    utility = [
        "Warrior Lady of the Wasteland",
        "Exiled Force",
        "Mystic Swordsman LV2",
        "Dimensional Warrior",
        "Dandylion",
        "D. D. Assailant",
        "Blade Knight",
        "D.D. Warrior Lady",
        "Marauding Captain",
        "Command Knight",
        "Reinforcement of the Army"
    ]
    return CardRule(utility + beaters, min_amount=9, additional_cards=InnerCardRule(big_beaters, min_amount=1))


def only_fairy():
    beaters = [
        "Dunames Dark Witch",
        "Hysteric Fairy",
    ]
    big_beaters = [
        "The Agent of Judgment - Saturn",
        "Airknight Parshath"
    ]
    utility = [
        "Dancing Fairy",
        "Zolga",
        "Shining Angel",
        "Kelbek",
        "Mudora",
        "Asura Priest",
        "Cestus of Dagla"
    ]
    return CardRule(utility + beaters, min_amount=9, additional_cards=InnerCardRule(big_beaters, min_amount=1))


def only_zombie():
    return CardRule([
        "Regenerating Mummy",
        "Ryu Kokki",
        "Spirit Reaper",
        "Master Kyonshee",
        "Curse of Vampire",
        "Vampire Lord",
        "Goblin Zombie",
        "Curse of Vampire",
        "Vampire Lord",
        "Goblin Zombie",
        "Book of Life",
        "Call of the Mummy"
    ], 12, additional_cards=InnerCardRule(["Pyramid Turtle"], 3))


def only_dragon():
    beaters = [
        "Luster Dragon",
        "Spear Dragon",
        "Cave Dragon"
        "Armed Dragon LV3",
        "Masked Dragon",
        "Twin-Headed Behemoth",
        "Element Dragon",
        "Troop Dragon",
        "Horus the Black Flame Dragon LV4",
        "Stamping Destruction"
    ]
    big_beaters = [
        "Luster Dragon #2",
        "Armed Dragon LV5",
        "Kaiser Glider",
        "Horus the Black Flame Dragon LV6"
    ]
    return CardRule(beaters, min_amount=9, additional_cards=InnerCardRule(big_beaters, min_amount=1))


def only_spellcaster():
    beaters = [
        "Dark Elf",
        "Gemini Elf",
        "Skilled Dark Magician",
        "Toon Gemini Elf",
        "Kycoo the Ghost Destroyer",
        "Familiar-Possessed - Aussa",
        "Familiar-Possessed - Eria",
        "Familiar-Possessed - Hiita",
        "Familiar-Possessed - Wynn",
    ]
    big_beaters = [
        "Chaos Command Magician",
        "Cybernetic Magician"
    ]
    utility = [
        "Breaker the magical Warrior",
        "The Tricky",
        "Injection Fairy Lily",
        "Magician of Faith",
        "Tsukuyomi",
        "Gravekeeper's Spy",
        "Gravekeeper's Guard",
        "Summon Priest",
        "Old Vindictive Magician",
        "Apprentice Magician",
        "Magical Dimension"
    ]
    return CardRule(utility + beaters, min_amount=9, additional_cards=InnerCardRule(big_beaters, min_amount=1))


def only_level():
    lv_pairs = [
        ["Armed Dragon LV3", "Armed Dragon LV5"],
        ["Horus the Black Flame Dragon LV4", "Horus the Black Flame Dragon LV6"],
        ["Mystic Swordsman LV4", "Mystic Swordsman LV6"],
        ["Silent Swordsman LV3", "Silent Swordsman LV5"],
        ["Ultimate Insect LV3", "Ultimate Insect LV5"],
    ]
    card_rules: List[CardRule] = []
    level_up_rule = InnerCardRule(["Level Up!"], 3)
    # one pair and bunch of lose LV monsters
    for pair in lv_pairs:
        inner_cards = list(lv_pairs)
        inner_cards.remove(pair)
        inner_cards = sum(inner_cards, [])
        rule = CardRule(pair, 6, additional_cards=[level_up_rule, InnerCardRule(inner_cards, 6)])
        card_rules.append(rule)
    return card_rules


def only_normal():
    beaters = find_cards_with(min_attack=1800, max_level=4, card_type="None")
    big_beaters = find_cards_with(min_attack=2400, min_level=5,  max_level=6, card_type="None")
    return CardRule(beaters, min_amount=9, additional_cards=InnerCardRule(big_beaters, min_amount=1))


def find_cards_with(min_attack: int = None, max_attack: int = None, min_defence:int = None,
                    min_level: int = None, max_level: int = None, attribute: str = None,
                    card_type: str = None, no_nomi: bool = True):
    result: List[str] = []
    for name, card in cards.items():
        if min_attack and not card.attack >= min_attack:
            continue
        if max_attack and not card.attack <= max_attack:
            continue
        if min_level and not card.level >= min_level:
            continue
        if max_level and not card.level <= max_level:
            continue
        if min_defence and not card.defence >= min_defence:
            continue
        if attribute and card.attribute != attribute:
            continue
        if card_type and card.card_type != card_type:
            continue
        if no_nomi and (card.card_type == "Fusion" or card.card_type == "Ritual" or name in nomi_monsters):
            continue
        result.append(name)
    return result


raise_attack = [
    CardRule("A Legendary Ocean", additional_cards=InnerCardRule(
        cards=lambda: find_cards_with(min_attack=2850, attribute="WATER"), min_amount=1), min_amount=1),
    CardRule("Ancient Gear Castle", min_amount=1,
             additional_cards=InnerCardRule(cards="Ancient Gear Golem", min_amount=1)),
    CardRule("Axe of Despair", min_amount=1, additional_cards=InnerCardRule(
        cards=lambda: find_cards_with(min_attack=2050), min_amount=1)),
    CardRule("Ballista of Rampart Smashing", min_amount=1, additional_cards=InnerCardRule(
        cards=lambda: find_cards_with(min_attack=1550), min_amount=1)),
    CardRule("Banner of Courage", min_amount=1, additional_cards=InnerCardRule(
        cards=lambda: find_cards_with(min_attack=2850), min_amount=1)),
    CardRule("Banner of Courage", min_amount=1, additional_cards=InnerCardRule(
        cards=lambda: find_cards_with(min_attack=2650), min_amount=1)),
    CardRule("Black Pendant", min_amount=1, additional_cards=InnerCardRule(
        cards=lambda: find_cards_with(min_attack=2550), min_amount=1)),
    # todo
]
