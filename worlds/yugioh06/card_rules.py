import logging
from typing import List, NamedTuple, Callable, Dict

from worlds.yugioh06 import cards
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
    additional_cards: InnerCardRule | List[InnerCardRule] | Callable = []
    amount_protocol: str = "total"


def find_cards_with(min_attack: int = None, attribute: str = None, no_nomi: bool = True):
    result: List[str] = []
    for name, card in cards.items():
        if min_attack and not card.attack >= min_attack:
            continue
        if attribute and card.attribute != attribute:
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
]


def set_card_rules(world):
    rules = {
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
                         cards=lambda: {name for name, c in cards.items() if c.attack % 100 != 0},
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
        "Can Gain LP Every Turn":
            CardRule(["Solemn Wishes", "Cure Mermaid",
                      "Dancing Fairy", "Princess Pikeru", "Kiseitai"], 9),
        "Can Self Mill":
            CardRule(["Reasoning", "Monster Gate", "Magical Merchant"], 3),

        # Limited
        "LD20 All except Warriors forbidden": only_warrior()
    }
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
        for card in world.structure_deck:
            if card.name in starting_cards:
                starting_cards[card.name] += world.structure_deck[card]
            else:
                starting_cards[card.name] = world.structure_deck[card]
    else:
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
        a = 0
        chosen_starters: List[str] = []
        potential_starters: List[str] = []
        for c in overlap:
            a += starter_cards[c]
            if starter_cards[c] == 3:
                potential_cards.remove(c)
                chosen_starters.append(c)
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
                overlap.remove(potential_cards[i])
            else:
                a += 3
            i += 1
        return chosen_cards, overlap
    else:
        chosen_starters: List[str] = []
        chosen_cards: List[str] = []
        for card in potential_cards:
            if card in starter_cards and starter_cards[card] >= rule.min_amount:
                chosen_starters.append(card)
            else:
                chosen_cards.append(card)
        return chosen_cards, chosen_starters


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
        "Silent Swordsman Lv5"
    ]
    utility = [
        "Warrior Lady of the Wasteland",
        "Exiled Force",
        "Mystic Swordsman LV2",
        "Dimensional Warrior",
        "Dandylion",
        "D.D. Assailant",
        "Blade Knight",
        "D.D. Warrior Lady",
        "Marauding Captain",
        "Command Knight",
        "Reinforcement of the Army"
    ]
    return CardRule(utility, min_amount=12, additional_cards=[
        InnerCardRule(beaters, min_amount=3),
        InnerCardRule(big_beaters, min_amount=1)
    ])
