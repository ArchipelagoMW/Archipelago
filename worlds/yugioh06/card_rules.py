import logging
from typing import List, NamedTuple, Callable, Dict

from worlds.yugioh06 import cards, banlists
from worlds.yugioh06.boosterpack_contents import not_in_standard_pool
from worlds.yugioh06.card_data import nomi_monsters
from worlds.yugioh06.fusions import fusions, fusion_subs
from worlds.yugioh06.ritual import rituals
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
    subs_in_start = [x for x in fusion_subs if x in starting_cards.keys()]
    if len(subs_in_start):
        world.fusion_sub_of_choice = world.random.choice(subs_in_start)
    else:
        world.fusion_sub_of_choice = world.random.choice(fusion_subs)

    evergreen_rules = {
        "Max ATK Bonus": raise_attack,
        "No Spell Cards Bonus": non_spell_monster_removal(),
        "No Trap Cards Bonus": non_trap_monster_removal(),
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
        "Tribute Summon Bonus": CardRule(cards=lambda: find_cards_with(min_level=5, max_level=6), min_amount=1),
        "Fusion Summon Bonus": any_fusion(world),
        "Ritual Summon Bonus": any_ritual(),
        "Low LP Bonus":
            CardRule(["Wall of Revealing Light"], 1),
        "Extremely Low LP Bonus":
            CardRule(["Wall of Revealing Light", "Messenger of Peace"], 1, "each",
                     additional_cards=InnerCardRule(
                         lambda: {name for name, c in cards.items() if c.attack % 100 != 0 and c.level <= 4}, 1)),
        "Effect Damage Only Bonus":
            [CardRule(["Solar Flare Dragon", "UFO Turtle"], 2, "each"),
             CardRule(["Wave-Motion Cannon"], 3)],
        "Opponent's Turn Finish Bonus": opponents_turn(),
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
            CardRule(["Ojama Delta Hurricane!!", "Ojama Green", "Ojama Yellow",
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
                      "Alpha The Magnet Warrior", "Beta The Magnet Warrior",
                      "Gamma The Magnet Warrior"], 1, amount_protocol="each"),
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
                      "Right Leg of the Forbidden One"], min_amount=1,
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
        # All removal is always progression
        "Backrow Removal": backrow_removal(),
        "Monster Removal": monster_removal(),
        # for deck strength
        "Beaters": CardRule(find_cards_with(min_attack=1800, max_attack=2000, max_level=4), 15)
    }

    challenge_rules = {
        # Limited
        "LD01 All except Level 4 forbidden":
            CardRule(cards=lambda: find_cards_with(min_attack=1700, max_attack=2000,
                                                   min_level=4, max_level=4), min_amount=12),
        "LD02 Medium/high Level forbidden":
            CardRule(cards=lambda: find_cards_with(min_attack=1700, max_attack=2000,
                                                   max_level=4), min_amount=12),
        "LD03 ATK 1500 or more forbidden":
            CardRule(cards=lambda: find_cards_with(min_attack=1300, max_attack=1500,
                                                   max_level=4), min_amount=12),
        "LD10 All except LV monsters forbidden": only_level(),
        "LD11 All except Fairies forbidden": only_fairy(),
        "LD12 All except Wind forbidden": only_wind(),
        "LD14 Level 3 or below forbidden":
            CardRule(cards=lambda: find_cards_with(min_attack=1700, max_attack=2000,
                                                   min_level=4, max_level=4), min_amount=12),
        "LD15 DEF 1500 or less forbidden":
            CardRule(cards=lambda: find_cards_with(min_attack=1500, max_attack=2000,
                                                   min_defence=1550, max_level=4), min_amount=12),
        "LD16 Effect Monsters forbidden": only_normal(),
        "LD18 Attacks forbidden":
            CardRule(["Wave-Motion Cannon", "Stealth Bird"], 3, "each",
                     InnerCardRule(["Dark World Lightning", "Nobleman of Crossout",
                                    "Shield Crash", "Tribute to The Doomed"], 4)),
        "LD19 All except E-Hero's forbidden": hero_gate_deck(world),
        "LD20 All except Warriors forbidden": only_warrior(),
        "LD21 All except Dark forbidden": only_dark(),
        "LD26 All except Toons forbidden": only_toons(),
        "LD27 All except Spirits forbidden": only_spirit(),
        "LD28 All except Dragons forbidden": only_dragon(),
        "LD29 All except Spellcasters forbidden": only_spellcaster(),
        "LD30 All except Light forbidden": only_light(),
        "LD31 All except Fire forbidden": only_fire(),
        "LD34 Normal Summons forbidden": [hero_gate_deck(world), pacman_deck()],
        "LD35 All except Zombies forbidden": only_zombie(),
        "LD36 All except Earth forbidden": only_earth(),
        "LD37 All except Water forbidden": only_water(),
        "LD39 Monsters forbidden":
            CardRule(["Skull Zoma", "Embodiment of Apophis"], 3, "each"),
        "TD02 Deflected Damage":
            CardRule("Fairy Box", 3, additional_cards=InnerCardRule(find_cards_with(min_defence=2000, max_level=4), 6)),
        "TD04 Ritual Summon": ritual_deck(),
        "TD05 Special Summon A": recruiters(),
        "TD06 20x Spell":
            CardRule("Magical Blast", 3),
        "TD07 10x Trap":
            CardRule(find_cards_with(card_type="Trap", spell_trap_type="None"), 15),
        "TD08 Draw":
            CardRule(["Self-Destruct Button", "Dark Snake Syndrome"], 3),
        "TD09 Hand Destruction":
            CardRule([
                "Cyber Jar",
                "Morphing Jar",
                "Book of Moon",
                "Book of Taiyou",
                "Card Destruction",
                "Serial Spell",
                "Spell Reproduction",
                "The Shallow Grave"
            ], 3, "each"),
        "TD10 During Opponent's Turn": opponents_turn(),
        "TD12 Remove Monsters by Effect":
            CardRule("Soul Release", 3),
        "TD13 Flip Summon": pacman_deck(),
        "TD14 Special Summon B": [
            CardRule(["Manticore of Darkness"], 3, "each", InnerCardRule("Foolish Burial", 3)),
            CardRule(["Treeborn Frog"], 3, "each", InnerCardRule("Foolish Burial", 3)),
        ],
        "TD15 Token": CardRule(["Dandylion", "Ojama Trio", "Stray Lambs"], 3, "each"),
        "TD16 Union": equip_unions(),
        "TD17 10x Quick Spell": quick_plays(),
        "TD20 Deck Destruction":
            CardRule([
                "Morphing Jar",
                "Morphing Jar #2",
                "Needle Worm"
            ], 3, additional_cards=[
                InnerCardRule(["Spear Cretin", "The Shallow Grave"], 3),
            ]),
        "TD21 Victory D.":
            CardRule("Victory D.", 1, additional_cards=only_dragon(True)),
        "TD22 The Preventers Fight Back":
            CardRule(["Rescue Cat", "Enchanting Fitting Room", "Jerry Beans Man"], 3, "each"),
        "TD23 Huge Revolution":
            CardRule([
                "Enchanting Fitting Room", "Jerry Beans Man"
            ], 3, "each"),
        "TD24 Victory in 5 Turns":
            CardRule(["Snatch Steal", "Lightning Vortex"], 4),
        "TD25 Moth Grows Up":
            CardRule(["Gokipon", "Howling Insect"], 3, "each"),
        "TD27 Dark Sage":
            CardRule(["Skilled Dark Magician", "Dark Magic Curtain"], 3),
        "TD30 Tribute Summon":
            CardRule(["Treeborn Frog"], 3, "each",
                     additional_cards=InnerCardRule(["Dark Dust Spirit", "Great Long Nose"], 3)),
        "TD31 Special Summon C":
            CardRule([
                "Aqua Spirit", "The Rock Spirit", "Spirit of Flames",
                "Garuda the Wind Spirit", "Gigantes", "Inferno",
                "Megarock Dragon", "Silpheed"
            ], 12),
        "TD32 Toon": only_toons(),
        "TD33 10x Counter": counter_traps(),
        "TD34 Destiny Board": CardRule("A Cat of Ill Omen", 3),
        "TD35 Huge Damage in a Turn":
            CardRule([
            "Cyber-Stein",
            "Cyber Twin Dragon",
            "Megamorph"], 3, "each"),
        "TD37 Uria, Lord of Searing Flames":
            CardRule([
                "Uria, Lord of Searing Flames",
                "Embodiment of Apophis",
                "Skull Zoma",
                "Metal Reflect Slime"
            ], 3, "each"),
        "TD38 Hamon, Lord of Striking Thunder":
            CardRule("Hamon, Lord of Striking Thunder", 3,
                     additional_cards=countinous_spells()),
        "TD39 Raviel, Lord of Phantasms":
            CardRule(["Raviel, Lord of Phantasms", "Giant Germ"], 3, "each",
                     additional_cards=InnerCardRule([
                         "Archfiend Soldier",
                         "Skull Descovery Knight",
                         "Slate Warrior",
                         "D. D. Trainer",
                         "Earthbound Spirit"
                     ], 9)),
        "TD40 Make a Chain":
            CardRule("Ultimate Offering", 1),
        "TD41 The Gatekeeper Stands Tall":
            CardRule(["Treeborn Frog", "Tribute Doll"], 3, "each"),
        "TD43 Return Monsters with Effects":
            CardRule(["Penguin Soldier", "Messenger of Peace"], 3, "each"),
        "TD44 Fusion Summon": hero_gate_deck(world),
        "TD45 Big Damage at once":
            CardRule(["Wave-Motion Cannon"], 3),
        "TD46 XYZ In the House":
            CardRule(["Dimension Fusion", "Return from the Different Dimension"], 3),
        "TD47 Spell Counter":
            CardRule("Pitch-Black Power Stone", 3,
                     additional_cards=InnerCardRule([
                         "Blast Magician",
                         "Magical Marionette",
                         "Mythical Beast Cerberus",
                         "Royal Magical Library",
                     ], 6)),
        "TD48 Destroy Monsters with Effects":
            CardRule(["Blade Rabbit", "Dream Clown"], 3, "each"),
        "TD49 Plunder":
            CardRule([
                "Aussa the Earth Charmer",
                "Jowls of Dark Demise",
                "Brain Control",
                "Creature Swap",
                "Enemy Controller",
                "Mind Control",
                "Magician of Faith"
            ], 15),
        "TD50 Dark Scorpion Combination":
            CardRule([
                "Reinforcement of the Army",
                "Mystic Tomato"
            ], 3, "each")
    }

    rules = {**evergreen_rules, **{k: v for k, v in challenge_rules.items() if k not in world.removed_challenges}}

    for location, rule in rules.items():
        if isinstance(rule, List):
            world.random.shuffle(rule)
            chosen_rule = None
            # chose a rule that uses cards in the starting cards.
            # Only works as intended if an all elements in list have 1 card in main rule
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
        # Exception for Yata cause it needs a specific banlist
        if location != "Can Yata Lock":
            chosen_cards, chosen_starters = resolve_rule(world, chosen_rule, starting_cards)
            progression_cards[location] = chosen_cards
            progression_cards[location].extend(chosen_starters)
            cards_in_booster.extend(chosen_cards)
            cards_in_starter.extend(chosen_starters)
        else:
            progression_cards[location] = chosen_rule.cards
            cards_in_booster.extend(chosen_rule.cards)
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
    banned_cards = banlists[world.options.banlist.current_key]["Forbidden"]
    if isinstance(rule.cards, str):
        potential_cards.append(rule.cards)
    if isinstance(rule.cards, Callable):
        potential_cards.extend(rule.cards())
    if isinstance(rule.cards, List):
        potential_cards.extend(rule.cards)
    if rule.amount_protocol == "total" and len(potential_cards) > 1:
        overlap = [x for x in potential_cards if x in starter_cards.keys()]
        potential_cards = [x for x in potential_cards if (x in overlap or x not in not_in_standard_pool)
                           and x not in banned_cards]
        a = 0
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
    ]
    big_beaters = [
        "Thestalos the Firestorm Monarch",
        "Horus the Black Flame Dragon LV6",
    ]
    utility = [
        "Solar Flare Dragon",
        "Tenkabito Shien",
        "Ultimate Baseball Kid",
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
        "Gearfried the Iron Knight",
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


def only_dragon(inner: bool = False):
    beaters = [
        "Luster Dragon",
        "Spear Dragon",
        "Cave Dragon",
        "Armed Dragon LV3",
        "Masked Dragon",
        "Twin-Headed Behemoth",
        "Element Dragon",
        "Troop Dragon",
        "Horus the Black Flame Dragon LV4",
        "Stamping Destruction",
    ]
    big_beaters = [
        "Luster Dragon #2",
        "Armed Dragon LV5",
        "Kaiser Glider",
        "Horus the Black Flame Dragon LV6",
    ]
    if inner:
        return InnerCardRule(beaters, min_amount=9)
    else:
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
        "Breaker the Magical Warrior",
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


def only_toons():
    good_toons = [
        "Toon Gemini Elf",
        "Toon Goblin Attack Force",
        "Toon Masked Sorcerer",
        "Toon Mermaid",
        "Toon Dark Magician Girl",
        "Toon World"
    ]
    return CardRule(good_toons, 3, "each")


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
    # one pair and  a bunch of lose LV monsters
    for pair in lv_pairs:
        inner_cards = list(lv_pairs)
        inner_cards.remove(pair)
        inner_cards = sum(inner_cards, [])
        rule = CardRule(pair, 6, additional_cards=[level_up_rule, InnerCardRule(inner_cards, 6)])
        card_rules.append(rule)
    return card_rules


def only_normal():
    beaters = find_cards_with(min_attack=1800, max_level=4, card_type="None")
    big_beaters = find_cards_with(min_attack=2400, min_level=5, max_level=6, card_type="None")
    return CardRule(beaters, min_amount=9, additional_cards=InnerCardRule(big_beaters, min_amount=1))


def only_spirit():
    good_spirits = [
        "Asura Priest",
        "Fushi No Tori",
        "Maharaghi",
        "Susa Soldier"
    ]
    return CardRule(good_spirits, 3, "each")


def ritual_deck():
    return CardRule([
        "Contract with the Abyss",
        "Manju of the Ten Thousand Hands",
        "Senju of the Thousand Hands",
        "Sonic Bird",
        "Pot of Avarice",
        "Dark Master - Zorc",
        "Demise, King of Armageddon",
        "The Masked Beast",
        "Magician of Black Chaos",
        "Dark Magic Ritual"
    ], 3, "each")


def pacman_deck():
    return CardRule([
        "Des Lacooda",
        "Swarm of Locusts",
        "Swarm of Scarabs",
        "Wandering Mummy",
        "Golem Sentry",
        "Great Spirit",
        "Royal Keeper",
        "Stealth Bird"
    ], 12)


def recruiters():
    all_recruiters = [
        "Flying Kamakiri #1",
        "Giant Rat",
        "Masked Dragon",
        "Mother Grizzly",
        "Mystic Tomato",
        "Shining Angel",
        "UFO Turtle",
        "Howling Insect",
        "Pyramid Turtle"
    ]
    return CardRule(all_recruiters, 12)


def opponents_turn():
    combat_tricks: List[str] = [
        "Blast with Chain",
        "Covering Fire",
        "Curse of Aging",
        "Deal of Phantom",
        "Energy Drain",
        "Fairy Box",
        "Kunai with Chain",
        "Mask of Weakness",
        "Mirror Wall",
        # "Reinforcements", starter only
        "Collapse",
        "Rush Recklessly",
    ]
    burn: List[str] = [
        "Poison of the Old Man",
        "Attack and Receive",
        "Ceasefire",
        "Cemetary Bomb",
        "Chthonian Blast",
        "Destruction Ring",
        "Dimension Wall",
        "Full Salvo",
        "Just Desserts",
        "Magic Cylinder",
        "Minor Goblin Official",
        "Ring of Destruction",
        "Secret Barrel",
        "Skull Zoma",
        "Type Zero Magic Crusher",
    ]
    return CardRule(combat_tricks + burn, 3)


def equip_unions():
    support = InnerCardRule(["Frontline Base", "Formation Union", "Roll Out!"], 3)
    return [
        CardRule("Mother Grizzly", 3, "each", [
            InnerCardRule(["Burning Beast", "Freezing Beast",
                           "Metallizing Parasite - Lunatite"], 3, "each"),
            support
            ]),
        CardRule("Mystic Tomato", 3, "each", [
            InnerCardRule(["Dark Blade", "Pitch-Dark Dragon",
                           "Giant Orc", "Second Goblin"], 3, "each"),
            support
        ]),
        CardRule("Giant Rat", 3, "each", [
            InnerCardRule(["Decayed Commander", "Zombie Tiger",
                           "Vampire Orchis", "Des Dendle"], 3, "each"),
            support
        ]),
        CardRule("Shining Angel", 3, "each", [
            InnerCardRule(["Indomitable Fighter Lei Lei", "Protective Soul Ailin",
                           "V-Tiger Jet", "W-Wing Catapult"], 3, "each"),
            support
        ]),
        CardRule("Shining Angel", 3, "each", [
            InnerCardRule(["X-Head Cannon", "Y-Dragon Head", "Z-Metal Tank"], 3, "each"),
            support
        ])
    ]


def quick_plays():
    quickplays = [
        "Collapse",
        "Emergency Provisions",
        "Enemy Controller",
        "Graceful Dice",
        "Mystik Wok",
        "Offerings to the Doomed",
        "Poison of the Old Man",
        "Reload",
        "Rush Recklessly",
        "The Reliable Guardian",
    ]
    return CardRule(quickplays, 12)


def counter_traps():
    c_traps = [
        "Cursed Seal of the Forbidden Spell",
        "Divine Wrath",
        "Horn of Heaven",
        "Magic Drain",
        "Magic Jammer",
        "Negate Attack",
        "Seven Tools of the Bandit",
        "Solemn Judgment",
        "Spell Shield Type-8"
    ]
    return CardRule(c_traps, 15)


def countinous_spells():
    blacklist = [
        "Spirit Message 'I'",
        "Spirit Message 'N'"
        "Spirit Message 'A'"
        "Spirit Message 'L'"
    ]
    c_spells = find_cards_with(card_type="Spell", spell_trap_type="Continuous")
    c_spells = [c for c in c_spells if c not in blacklist]
    return InnerCardRule(c_spells, 9)


def monster_removal():
    unlimted_removal = [
        "Blast Sphere",
        "Man-Eater Bug",
        "Sakuretsu Armor",
        "Smashing Ground",
        "Dark Core",
        "Zaborg the Thunder Monarch",
        "D. D. Assailant",
        "Fissure",
        "Dimensional Warrior",
        "Hammer Shot",
        "Michizure",
        "Raigeki Break",
        "Soul Taker",
        "Yomi Ship",
        "Tribute to The Doomed",
        "Newdoria",
        "Widespread Ruin",
        "Old Vindictive Magician",
        "Offerings to the Doomed",
    ]
    limited_removal = [
        "D.D. Warrior Lady",
        "Night Assailant",
        "Torrential Tribute",
        "Exiled Force",
        "Lightning Vortex",
    ]
    return CardRule(unlimted_removal, 5, "total", InnerCardRule(limited_removal, 1))


def non_spell_monster_removal():
    removal = [
        "Blast Sphere",
        "Man-Eater Bug",
        "Sakuretsu Armor",
        "Zaborg the Thunder Monarch",
        "D. D. Assailant",
        "Dimensional Warrior",
        "Michizure",
        "Raigeki Break",
        "Yomi Ship",
        "Newdoria",
        "Widespread Ruin",
        "Old Vindictive Magician",
    ]
    return CardRule(removal, 3)


def non_trap_monster_removal():
    removal = [
        "Blast Sphere",
        "Man-Eater Bug",
        "Smashing Ground",
        "Dark Core",
        "Zaborg the Thunder Monarch",
        "D. D. Assailant",
        "Fissure",
        "Dimensional Warrior",
        "Hammer Shot",
        "Soul Taker",
        "Yomi Ship",
        "Tribute to The Doomed",
        "Newdoria",
        "Old Vindictive Magician",
        "Offerings to the Doomed",
    ]
    return CardRule(removal, 3)


def backrow_removal():
    unlimited_removal = [
        "Mobius the Frost Monarch",
        "Anteatereatingant",
        "B.E.S. Tetran",
        "Chiron the Mage",
        "Raigeki Break",
        "Calamity of the Wicked",
        "Dust Tornado",
    ]
    limited_removal = [
        "Mystical Space Typhoon",
        "Breaker the Magical Warrior",
        "Heavy Storm",
    ]
    return CardRule(unlimited_removal, 5, additional_cards=InnerCardRule(limited_removal, 1))


def any_fusion(world):
    fusion_rules = [build_card_rule_for_fusion(world, f) for f, r in fusions.items()
                    if f not in not_in_standard_pool and not r.contact_fusion]
    return [r for r in fusion_rules if r]


def build_card_rule_for_fusion(world, fusion_monster: str):
    fusion_data = fusions[fusion_monster]
    materials = list(fusion_data.materials)
    number_of_materials = len(materials)
    invalid_materials = []
    for mat in materials:
        if mat in not_in_standard_pool or cards[mat].card_type == "Fusion":
            invalid_materials.append(mat)
    for mat in invalid_materials:
        materials.remove(mat)
    if fusion_data.replaceable:
        materials.append(world.fusion_sub_of_choice)
        world.random.shuffle(materials)
    if not fusion_data.generic:
        if len(materials) >= number_of_materials:
            materials = materials[0:number_of_materials]
        else:
            return False
        return CardRule(fusion_monster, 1, additional_cards=[
            InnerCardRule(materials, 1, "each"),
            InnerCardRule(["Polymerization", "Fusion Gate"] + fusion_data.additional_spells, 1)
        ])
    elif fusion_data.generic == "Dragon":
        return CardRule(fusion_monster, 1, additional_cards=[
            only_dragon(True),
            InnerCardRule(["Dragon's Mirror"], 1)
        ])
    elif fusion_data.generic == "Warrior":
        InnerCardRule(find_cards_with(types=["Warrior"]), 1),
        InnerCardRule(["Polymerization", "Fusion Gate"] + fusion_data.additional_spells, 1)


def hero_gate_deck(world):
    return CardRule(["Fusion Gate", "Terraforming", "Dimension Fusion",
                    "Return from the Different Dimension"], 3, "each", [
        InnerCardRule([
            "Elemental Hero Flame Wingman",
            "Elemental Hero Madballman",
            "Elemental Hero Rampart Blaster",
            "Elemental Hero Steam Healer"
        ], 2, "each"),
        InnerCardRule([
            "Elemental Hero Avian",
            "Elemental Hero Burstinatrix",
            "Elemental Hero Bubbleman",
            "Elemental Hero Clayman",
            world.fusion_sub_of_choice
        ], 3, "each"),
    ])


def any_ritual():
    return [build_card_rule_for_rituals(f) for f in rituals if len(rituals[f].ritual_spells) > 0]


def build_card_rule_for_rituals(ritual_monster: str):
    ritual_data = rituals[ritual_monster]
    return CardRule(ritual_monster, 2, additional_cards=InnerCardRule(ritual_data.ritual_spells, 1))


def find_cards_with(min_attack: int = None, max_attack: int = None, min_defence: int = None,
                    min_level: int = None, max_level: int = None, attribute: str = None, types: List[str] = None,
                    card_type: str = None, spell_trap_type: str = None, no_nomi: bool = True):
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
        if types and card.type not in types:
            continue
        if card_type and card.card_type != card_type:
            continue
        if spell_trap_type and card.spell_trap_type != spell_trap_type:
            continue
        if no_nomi and (card.card_type == "Fusion" or card.card_type == "Ritual" or name in nomi_monsters):
            continue
        result.append(name)
    return result


raise_attack = [
    CardRule("A Legendary Ocean", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2850, attribute="WATER"), 1)),
    CardRule("Ancient Gear Castle", 1,
             additional_cards=InnerCardRule("Ancient Gear Golem", 1)),
    CardRule("Axe of Despair", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2050), 1)),
    CardRule("Ballista of Rampart Smashing", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=1550), 1)),
    CardRule("Banner of Courage", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2850), 1)),
    CardRule("Big Bang Shot", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2650), 1)),
    CardRule("Black Pendant", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550), 1)),
    CardRule("Bladefly", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, attribute="WIND"), 1)),
    CardRule("Blast with Chain", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550), 1)),
    CardRule("Bright Castle", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2350, attribute="LIGHT"), 1)),
    CardRule("Cestus of Dagla", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, types=["Fairy"]), 1)),
    CardRule("Command Knight", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2650, types=["Warrior"]), 1)),
    CardRule("Dark Magician's Tome of Black Magic", 1, additional_cards=InnerCardRule(
        "Dark Magician", 1)),
    CardRule("Divine Sword - Phoenix Blade", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2750, types=["Warrior"]), 1)),
    CardRule("Emes the Infinity", 1),
    CardRule("Fusion Sword Murasame Blade", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2250, types=["Warrior"]), 1)),
    CardRule("Gaia Power", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, attribute="EARTH"), 1)),
    CardRule("Gravity Axe - Grarl", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550), 1)),
    CardRule("Heavy Mech Support Platform", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, types=["Machine"]), 1)),
    CardRule("Horn of the Unicorn", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2350), 1)),
    CardRule("Hoshiningen", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, attribute="LIGHT"), 1)),
    CardRule("Injection Fairy Lily", 1),
    CardRule("Insect Armor with Laser Cannon", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2350, types=["Insect"]), 1)),
    CardRule("Blast with Chain", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550), 1)),
    CardRule("Kunai with Chain", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550), 1)),
    CardRule("Lightning Blade", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2250, types=["Warrior"]), 1)),
    CardRule("Limiter Removal", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=1550, types=["Machine"]), 1)),
    CardRule("Little Chimera", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, attribute="FIRE"), 1)),
    CardRule("Luminous Spark", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, attribute="LIGHT"), 1)),
    CardRule("Mage Power", 1),
    CardRule("Maju Garzett", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=1550), 2)),
    CardRule("Malevolent Nuzzler", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2350), 1)),
    CardRule("Mask of Brutality", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2050), 1)),
    CardRule("Megamorph", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=1550), 1)),
    CardRule("Metalmorph", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=1850), 1)),
    CardRule("Milus Radiant", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, attribute="EARTH"), 1)),
    CardRule("Molten Destruction", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, attribute="FIRE"), 1)),
    CardRule("Mountain", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2850, types=["Dragon", "Winged Beast", "Thunder"]), 1)),
    CardRule("Mystic Plasma Zone", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, attribute="DARK"), 1)),
    CardRule("Nightmare Penguin", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2850, attribute="WATER"), 1)),
    CardRule("Rare Metalmorph", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, types=["Machine"]), 1)),
    CardRule("Rising Air Current", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, attribute="WIND"), 1)),
    CardRule("Rising Energy", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=1550), 1)),
    CardRule("Rush Recklessly", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2350), 1)),
    CardRule("Salamandra", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2350, attribute="FIRE"), 1)),
    CardRule("Star Boy", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550), 1)),
    CardRule("Stim-Pack", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2350), 1)),
    CardRule("Sword of Deep-Seated", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550), 1)),
    CardRule("Sword of Dragon's Soul", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2350, types=["Warrior"]), 1)),
    CardRule("Umiiruka", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, attribute="WATER"), 1)),
    CardRule("United We Stand", 1),
    CardRule("Wicked-Breaking Flamberge - Baou", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550), 1)),
    CardRule("Winged Minion", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2350, types=["Fiend"]), 1)),
    CardRule("Witch's Apprentice", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2550, attribute="DARK"), 1)),
    CardRule("Yami", 1, additional_cards=InnerCardRule(
        lambda: find_cards_with(min_attack=2850, types=["Fiend", "Spellcaster"]), 1)),
]
