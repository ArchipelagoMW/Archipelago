from worlds.generic.Rules import add_rule

from . import yugioh06_difficulty
from .fusions import count_has_materials


def set_rules(world):
    player = world.player
    multiworld = world.multiworld

    location_rules = {
        # Campaign
        "Campaign Tier 1: 1 Win": lambda state: state.has("Tier 1 Beaten", player),
        "Campaign Tier 1: 3 Wins A": lambda state: state.has("Tier 1 Beaten", player, 3),
        "Campaign Tier 1: 3 Wins B": lambda state: state.has("Tier 1 Beaten", player, 3),
        "Campaign Tier 1: 5 Wins A": lambda state: state.has("Tier 1 Beaten", player, 5),
        "Campaign Tier 1: 5 Wins B": lambda state: state.has("Tier 1 Beaten", player, 5),
        "Campaign Tier 2: 1 Win": lambda state: state.has("Tier 2 Beaten", player),
        "Campaign Tier 2: 3 Wins A": lambda state: state.has("Tier 2 Beaten", player, 3),
        "Campaign Tier 2: 3 Wins B": lambda state: state.has("Tier 2 Beaten", player, 3),
        "Campaign Tier 2: 5 Wins A": lambda state: state.has("Tier 2 Beaten", player, 5),
        "Campaign Tier 2: 5 Wins B": lambda state: state.has("Tier 2 Beaten", player, 5),
        "Campaign Tier 3: 1 Win": lambda state: state.has("Tier 3 Beaten", player),
        "Campaign Tier 3: 3 Wins A": lambda state: state.has("Tier 3 Beaten", player, 3),
        "Campaign Tier 3: 3 Wins B": lambda state: state.has("Tier 3 Beaten", player, 3),
        "Campaign Tier 3: 5 Wins A": lambda state: state.has("Tier 3 Beaten", player, 5),
        "Campaign Tier 3: 5 Wins B": lambda state: state.has("Tier 3 Beaten", player, 5),
        "Campaign Tier 4: 5 Wins A": lambda state: state.has("Tier 4 Beaten", player, 5),
        "Campaign Tier 4: 5 Wins B": lambda state: state.has("Tier 4 Beaten", player, 5),

        # Bonuses
        "Duelist Bonus Level 1": lambda state: state.has("Tier 1 Beaten", player),
        "Duelist Bonus Level 2": lambda state: state.has("Tier 2 Beaten", player),
        "Duelist Bonus Level 3": lambda state: state.has("Tier 3 Beaten", player),
        "Duelist Bonus Level 4": lambda state: state.has("Tier 4 Beaten", player),
        "Duelist Bonus Level 5": lambda state: state.has("Tier 5 Beaten", player),
        "Max ATK Bonus": lambda state: yugioh06_difficulty(state, player, 2),
        "No Spell Cards Bonus": lambda state: yugioh06_difficulty(state, player, 2),
        "No Trap Cards Bonus": lambda state: yugioh06_difficulty(state, player, 2),
        "No Damage Bonus": lambda state: state.has_group("Campaign Boss Beaten", player, 3),
        "Low Deck Bonus": lambda state: state.has_any(["Reasoning", "Monster Gate", "Magical Merchant"], player) and
                                        yugioh06_difficulty(state, player, 2),
        "Extremely Low Deck Bonus":
            lambda state: state.has_any(["Reasoning", "Monster Gate", "Magical Merchant"], player) and
                          yugioh06_difficulty(state, player, 3),
        "Opponent's Turn Finish Bonus": lambda state: yugioh06_difficulty(state, player, 2),
        "Exactly 0 LP Bonus": lambda state: yugioh06_difficulty(state, player, 2),
        "Reversal Finish Bonus": lambda state: yugioh06_difficulty(state, player, 2),
        "Quick Finish Bonus": lambda state: state.has("Quick-Finish", player) or yugioh06_difficulty(state, player, 6),
        "Exodia Finish Bonus": lambda state: state.has("Can Exodia Win", player),
        "Last Turn Finish Bonus": lambda state: state.has("Can Last Turn Win", player),
        "Yata-Garasu Finish Bonus": lambda state: state.has("Can Yata Lock", player),
        "Skull Servant Finish Bonus": lambda state: state.has("Skull Servant", player) and
                                                    yugioh06_difficulty(state, player, 3),
        "Konami Bonus": lambda state: state.has_all(["Messenger of Peace", "Castle of Dark Illusions", "Mystik Wok"],
                                                    player) or (state.has_all(["Mystik Wok", "Barox", "Cyber-Stein",
                                                                              "Poison of the Old Man"],
                                                                             player) and yugioh06_difficulty(state,
            player, 8)),
        "Max Damage Bonus": lambda state: state.has_any(["Wave-Motion Cannon", "Megamorph", "United We Stand",
                                                         "Mage Power"], player),
        "Fusion Summon Bonus": lambda state: state.has_any(["Polymerization", "Fusion Gate", "Power Bond"], player),
        "Ritual Summon Bonus": lambda state: state.has("Ritual", player),
        "Over 20000 LP Bonus": lambda state: can_gain_lp_every_turn(state, player)
                                             and state.has("Can Stall with ST", player),
        "Low LP Bonus": lambda state: state.has("Wall of Revealing Light", player) and yugioh06_difficulty(state, player,
                                                                                                                 2),
        "Extremely Low LP Bonus": lambda state: state.has_all(["Wall of Revealing Light", "Messenger of Peace"], player)
                                                and yugioh06_difficulty(state, player, 4),
        "Effect Damage Only Bonus": lambda state: state.has_all(["Solar Flare Dragon", "UFO Turtle"], player)
                                                  or state.has("Wave-Motion Cannon", player)
                                                  or state.can_reach("Final Countdown Finish Bonus", "Location", player)
                                                  or state.can_reach("Destiny Board Finish Bonus", "Location", player)
                                                  or state.has("Can Exodia Win", player)
                                                  or state.has("Can Last Turn Win", player),
        "No More Cards Bonus": lambda state: state.has_any(["Cyber Jar", "Morphing Jar",
                                                            "Morphing Jar #2", "Needle Worm"], player)
                                             and state.has_any(["The Shallow Grave", "Spear Cretin"],
                                                               player) and yugioh06_difficulty(state, player, 5),
        "Final Countdown Finish Bonus": lambda state: state.has("Final Countdown", player)
                                                      and state.has("Can Stall with ST", player),
        "Destiny Board Finish Bonus": lambda state: state.has("Can Stall with Monsters", player) and
                                                    state.has("Destiny Board and its letters", player) and
                                                    state.has("A Cat of Ill Omen", player),

        # Cards
        "Obtain all pieces of Exodia": lambda state: state.has("Exodia", player),
        "Obtain Final Countdown": lambda state: state.has("Final Countdown", player),
        "Obtain Victory Dragon": lambda state: state.has("Victory D.", player),
        "Obtain Ojama Delta Hurricane and its required cards":
            lambda state: state.has("Ojama Delta Hurricane and required cards", player),
        "Obtain Huge Revolution and its required cards":
            lambda state: state.has("Huge Revolution and its required cards", player),
        "Obtain Perfectly Ultimate Great Moth and its required cards":
            lambda state: state.has("Perfectly Ultimate Great Moth and its required cards", player),
        "Obtain Valkyrion the Magna Warrior and its pieces":
            lambda state: state.has("Valkyrion the Magna Warrior and its pieces", player),
        "Obtain Dark Sage and its required cards": lambda state: state.has("Dark Sage and its required cards", player),
        "Obtain Destiny Board and its letters": lambda state: state.has("Destiny Board and its letters", player),
        "Obtain all XYZ-Dragon Cannon fusions and their materials":
            lambda state: state.has("XYZ-Dragon Cannon fusions and their materials", player),
        "Obtain VWXYZ-Dragon Catapult Cannon and the fusion materials":
            lambda state: state.has("VWXYZ-Dragon Catapult Cannon and the fusion materials", player),
        "Obtain Hamon, Lord of Striking Thunder":
            lambda state: state.has("Hamon, Lord of Striking Thunder", player),
        "Obtain Raviel, Lord of Phantasms":
            lambda state: state.has("Raviel, Lord of Phantasms", player),
        "Obtain Uria, Lord of Searing Flames":
            lambda state: state.has("Uria, Lord of Searing Flames", player),
        "Obtain Gate Guardian and its pieces":
            lambda state: state.has("Gate Guardian and its pieces", player),
        "Obtain Dark Scorpion Combination and its required cards":
            lambda state: state.has("Dark Scorpion Combination and its required cards", player),
        # Collection Events
        "Ojama Delta Hurricane and required cards":
            lambda state: state.has_all(["Ojama Delta Hurricane", "Ojama Green", "Ojama Yellow", "Ojama Black"],
                                        player),
        "Huge Revolution and its required cards":
            lambda state: state.has_all(["Huge Revolution", "Oppressed People", "United Resistance",
                                         "People Running About"], player),
        "Perfectly Ultimate Great Moth and its required cards":
            lambda state: state.has_all(["Perfectly Ultimate Great Moth", "Petit Moth", "Cocoon of Evolution"], player),
        "Valkyrion the Magna Warrior and its pieces":
            lambda state: state.has_all(["Valkyrion the Magna Warrior", "Alpha the Magnet Warrior",
                                         "Beta the Magnet Warrior", "Gamma the Magnet Warrior"], player),
        "Dark Sage and its required cards":
            lambda state: state.has_all(["Dark Sage", "Dark Magician", "Time Wizard"], player),
        "Destiny Board and its letters":
            lambda state: state.has_all(["Destiny Board", "Spirit Message 'I'", "Spirit Message 'N'",
                                         "Spirit Message 'A'", "Spirit Message 'L'"], player),
        "XYZ-Dragon Cannon fusions and their materials":
            lambda state: state.has_all(["X-Head Cannon", "Y-Dragon Head", "Z-Metal Tank",
                                         "XY-Dragon Cannon", "XZ-Tank Cannon", "YZ-Tank Dragon", "XYZ-Dragon Cannon"],
                                        player),
        "VWXYZ-Dragon Catapult Cannon and the fusion materials":
            lambda state: state.has_all(["X-Head Cannon", "Y-Dragon Head", "Z-Metal Tank", "XYZ-Dragon Cannon",
                                         "V-Tiger Jet", "W-Wing Catapult", "VW-Tiger Catapult",
                                         "VWXYZ-Dragon Catapult Cannon"],
                                        player),
        "Gate Guardian and its pieces":
            lambda state: state.has_all(["Gate Guardian", "Kazejin", "Suijin", "Sanga of the Thunder"], player),
        "Dark Scorpion Combination and its required cards":
            lambda state: state.has_all(["Dark Scorpion Combination", "Don Zaloog", "Dark Scorpion - Chick the Yellow",
                                         "Dark Scorpion - Meanae the Thorn", "Dark Scorpion - Gorg the Strong",
                                         "Cliff the Trap Remover"], player),
        "Can Exodia Win":
            lambda state: state.has_all(["Exodia", "Heart of the Underdog"], player),
        "Can Last Turn Win":
            lambda state: state.has_all(["Last Turn", "Wall of Revealing Light"], player) and
                          (state.has_any(["Jowgen the Spiritualist", "Jowls of Dark Demise", "Non Aggression Area"],
                                         player)
                           or state.has_all(["Cyber-Stein", "The Last Warrior from Another Planet"], player)),
        "Can Yata Lock":
            lambda state: state.has_all(["Yata-Garasu", "Chaos Emperor Dragon - Envoy of the End", "Sangan"], player)
                          and state.has_any(["No Banlist", "Banlist September 2003"], player),
        "Can Stall with Monsters":
            lambda state: state.count_from_list_unique(
                ["Spirit Reaper", "Giant Germ", "Marshmallon", "Nimble Momonga"], player) >= 2,
        "Can Stall with ST":
            lambda state: state.count_from_list_unique(["Level Limit - Area B", "Gravity Bind", "Messenger of Peace"],
                                                       player) >= 2,
        "Has Back-row removal":
            lambda state: back_row_removal(state, player)

    }
    access_rules = {
        # Limited
        "LD01 All except Level 4 forbidden":
            lambda state: yugioh06_difficulty(state, player, 2),
        "LD02 Medium/high Level forbidden":
            lambda state: yugioh06_difficulty(state, player, 1),
        "LD03 ATK 1500 or more forbidden":
            lambda state: yugioh06_difficulty(state, player, 4),
        "LD04 Flip Effects forbidden":
            lambda state: yugioh06_difficulty(state, player, 1),
        "LD05 Tributes forbidden":
            lambda state: yugioh06_difficulty(state, player, 1),
        "LD06 Traps forbidden":
            lambda state: yugioh06_difficulty(state, player, 1),
        "LD07 Large Deck A":
            lambda state: yugioh06_difficulty(state, player, 4),
        "LD08 Large Deck B":
            lambda state: yugioh06_difficulty(state, player, 4),
        "LD09 Sets Forbidden":
            lambda state: yugioh06_difficulty(state, player, 1),
        "LD10 All except LV monsters forbidden":
            lambda state: only_level(state, player) and yugioh06_difficulty(state, player, 2),
        "LD11 All except Fairies forbidden":
            lambda state: only_fairy(state, player) and yugioh06_difficulty(state, player, 2),
        "LD12 All except Wind forbidden":
            lambda state: only_wind(state, player) and yugioh06_difficulty(state, player, 2),
        "LD13 All except monsters forbidden":
            lambda state: yugioh06_difficulty(state, player, 3),
        "LD14 Level 3 or below forbidden":
            lambda state: yugioh06_difficulty(state, player, 1),
        "LD15 DEF 1500 or less forbidden":
            lambda state: yugioh06_difficulty(state, player, 3),
        "LD16 Effect Monsters forbidden":
            lambda state: only_normal(state, player) and yugioh06_difficulty(state, player, 4),
        "LD17 Spells forbidden":
            lambda state: yugioh06_difficulty(state, player, 3),
        "LD18 Attacks forbidden":
            lambda state: state.has_all(["Wave-Motion Cannon", "Stealth Bird"], player)
                          and state.count_from_list_unique(["Dark World Lightning", "Nobleman of Crossout",
                                                            "Shield Crash", "Tribute to the Doomed"], player) >= 2
                          and yugioh06_difficulty(state, player, 3),
        "LD19 All except E-Hero's forbidden":
            lambda state: state.has_any(["Polymerization", "Fusion Gate"], player) and
                          count_has_materials(state, ["Elemental Hero Flame Wingman",
                                                      "Elemental Hero Madballman",
                                                      "Elemental Hero Rampart Blaster",
                                                      "Elemental Hero Steam Healer",
                                                      "Elemental Hero Shining Flare Wingman",
                                                      "Elemental Hero Wildedge"], player) >= 3 and
                          yugioh06_difficulty(state, player, 3),
        "LD20 All except Warriors forbidden":
            lambda state: only_warrior(state, player) and yugioh06_difficulty(state, player, 2),
        "LD21 All except Dark forbidden":
            lambda state: only_dark(state, player) and yugioh06_difficulty(state, player, 2),
        "LD22 All limited cards forbidden":
            lambda state: yugioh06_difficulty(state, player, 3),
        "LD23 Refer to Mar 05 Banlist":
            lambda state: yugioh06_difficulty(state, player, 5),
        "LD24 Refer to Sept 04 Banlist":
            lambda state: yugioh06_difficulty(state, player, 5),
        "LD25 Low Life Points":
            lambda state: yugioh06_difficulty(state, player, 5),
        "LD26 All except Toons forbidden":
            lambda state: only_toons(state, player) and yugioh06_difficulty(state, player, 2),
        "LD27 All except Spirits forbidden":
            lambda state: only_spirit(state, player) and yugioh06_difficulty(state, player, 2),
        "LD28 All except Dragons forbidden":
            lambda state: only_dragon(state, player) and yugioh06_difficulty(state, player, 2),
        "LD29 All except Spellcasters forbidden":
            lambda state: only_spellcaster(state, player) and yugioh06_difficulty(state, player, 2),
        "LD30 All except Light forbidden":
            lambda state: only_light(state, player) and yugioh06_difficulty(state, player, 2),
        "LD31 All except Fire forbidden":
            lambda state: only_fire(state, player) and yugioh06_difficulty(state, player, 2),
        "LD32 Decks with multiples forbidden":
            lambda state: yugioh06_difficulty(state, player, 4),
        "LD33 Special Summons forbidden":
            lambda state: yugioh06_difficulty(state, player, 2),
        "LD34 Normal Summons forbidden":
            lambda state: state.has_all(["Polymerization", "King of the Swamp"], player) and
                          count_has_materials(state, ["Elemental Hero Flame Wingman",
                                                      "Elemental Hero Madballman",
                                                      "Elemental Hero Rampart Blaster",
                                                      "Elemental Hero Steam Healer",
                                                      "Elemental Hero Shining Flare Wingman",
                                                      "Elemental Hero Wildedge"], player) >= 3 and
                          yugioh06_difficulty(state, player, 4),
        "LD35 All except Zombies forbidden":
            lambda state: only_zombie(state, player) and yugioh06_difficulty(state, player, 2),
        "LD36 All except Earth forbidden":
            lambda state: only_earth(state, player) and yugioh06_difficulty(state, player, 2),
        "LD37 All except Water forbidden":
            lambda state: only_water(state, player) and yugioh06_difficulty(state, player, 2),
        "LD38 Refer to Mar 04 Banlist":
            lambda state: yugioh06_difficulty(state, player, 4),
        "LD39 Monsters forbidden":
            lambda state: state.has_all(["Skull Zoma", "Embodiment of Apophis"], player)
                          and yugioh06_difficulty(state, player, 5),
        "LD40 Refer to Sept 05 Banlist":
            lambda state: yugioh06_difficulty(state, player, 5),
        "LD41 Refer to Sept 03 Banlist":
            lambda state: yugioh06_difficulty(state, player, 5),
        # Theme Duels
        "TD01 Battle Damage":
            lambda state: yugioh06_difficulty(state, player, 1),
        "TD02 Deflected Damage":
            lambda state: state.has("Fairy Box", player) and yugioh06_difficulty(state, player, 1),
        "TD03 Normal Summon":
            lambda state: yugioh06_difficulty(state, player, 3),
        "TD04 Ritual Summon":
            lambda state: yugioh06_difficulty(state, player, 3) and
                          state.has_all(["Contract with the Abyss",
                                         "Manju of the Ten Thousand Hands",
                                         "Senju of the Thousand Hands",
                                         "Sonic Bird",
                                         "Pot of Avarice",
                                         "Dark Master - Zorc",
                                         "Demise, King of Armageddon",
                                         "The Masked Beast",
                                         "Magician of Black Chaos",
                                         "Dark Magic Ritual"], player),
        "TD05 Special Summon A":
            lambda state: yugioh06_difficulty(state, player, 3),
        "TD06 20x Spell":
            lambda state: state.has("Magical Blast", player) and yugioh06_difficulty(state, player, 3),
        "TD07 10x Trap":
            lambda state: yugioh06_difficulty(state, player, 3),
        "TD08 Draw":
            lambda state: state.has_any(["Self-Destruct Button", "Dark Snake Syndrome"], player) and
                          yugioh06_difficulty(state, player, 3),
        "TD09 Hand Destruction":
            lambda state: state.has_all(["Cyber Jar",
                                         "Morphing Jar",
                                         "Book of Moon",
                                         "Book of Taiyou",
                                         "Card Destruction",
                                         "Serial Spell",
                                         "Spell Reproduction",
                                         "The Shallow Grave"], player) and yugioh06_difficulty(state, player, 3),
        "TD10 During Opponent's Turn":
            lambda state: yugioh06_difficulty(state, player, 3),
        "TD11 Recover":
            lambda state: can_gain_lp_every_turn(state, player) and yugioh06_difficulty(state, player, 3),
        "TD12 Remove Monsters by Effect":
            lambda state: state.has("Soul Release", player) and yugioh06_difficulty(state, player, 2),
        "TD13 Flip Summon":
            lambda state: pacman_deck(state, player) and yugioh06_difficulty(state, player, 2),
        "TD14 Special Summon B":
            lambda state: state.has_any(["Manticore of Darkness", "Treeborn Frog"], player) and
                          state.has("Foolish Burial", player) and
                          yugioh06_difficulty(state, player, 2),
        "TD15 Token":
            lambda state: state.has_all(["Dandylion", "Ojama Trio", "Stray Lambs"], player) and
                          yugioh06_difficulty(state, player, 3),
        "TD16 Union":
            lambda state: equip_unions(state, player) and
                          yugioh06_difficulty(state, player, 2),
        "TD17 10x Quick Spell":
            lambda state: quick_plays(state, player) and
                          yugioh06_difficulty(state, player, 3),
        "TD18 The Forbidden":
            lambda state: state.has("Can Exodia Win", player),
        "TD19 20 Turns":
            lambda state: state.has("Final Countdown", player) and state.has("Can Stall with ST", player) and
                          yugioh06_difficulty(state, player, 3),
        "TD20 Deck Destruction":
            lambda state: state.has_any(["Cyber Jar", "Morphing Jar", "Morphing Jar #2", "Needle Worm"], player)
                          and state.has_any(["The Shallow Grave", "Spear Cretin"],
                                            player) and yugioh06_difficulty(state, player, 2),
        "TD21 Victory D.":
            lambda state: state.has("Victory D.", player) and only_dragon(state, player)
                          and yugioh06_difficulty(state, player, 3),
        "TD22 The Preventers Fight Back":
            lambda state: state.has("Ojama Delta Hurricane and required cards", player) and
                          state.has_all(["Rescue Cat", "Enchanting Fitting Room", "Jerry Beans Man"], player) and
                          yugioh06_difficulty(state, player, 3),
        "TD23 Huge Revolution":
            lambda state: state.has("Huge Revolution and its required cards", player) and
                          state.has_all(["Enchanting Fitting Room", "Jerry Beans Man"], player) and
                          yugioh06_difficulty(state, player, 3),
        "TD24 Victory in 5 Turns":
            lambda state: yugioh06_difficulty(state, player, 3),
        "TD25 Moth Grows Up":
            lambda state: state.has("Perfectly Ultimate Great Moth and its required cards", player) and
                          state.has_all(["Gokipon", "Howling Insect"], player) and
                          yugioh06_difficulty(state, player, 3),
        "TD26 Magnetic Power":
            lambda state: state.has("Valkyrion the Magna Warrior and its pieces", player) and
                          yugioh06_difficulty(state, player, 2),
        "TD27 Dark Sage":
            lambda state: state.has("Dark Sage and its required cards", player) and
                          state.has_any(["Skilled Dark Magician", "Dark Magic Curtain"], player) and
                          yugioh06_difficulty(state, player, 2),
        "TD28 Direct Damage":
            lambda state: yugioh06_difficulty(state, player, 2),
        "TD29 Destroy Monsters in Battle":
            lambda state: yugioh06_difficulty(state, player, 2),
        "TD30 Tribute Summon":
            lambda state: state.has("Treeborn Frog", player) and yugioh06_difficulty(state, player, 2),
        "TD31 Special Summon C":
            lambda state: state.count_from_list_unique(
                ["Aqua Spirit", "Rock Spirit", "Spirit of Flames",
                 "Garuda the Wind Spirit", "Gigantes", "Inferno", "Megarock Dragon", "Silpheed"],
                player) > 4 and yugioh06_difficulty(state, player, 3),
        "TD32 Toon":
            lambda state: only_toons(state, player) and yugioh06_difficulty(state, player, 3),
        "TD33 10x Counter":
            lambda state: counter_traps(state, player) and yugioh06_difficulty(state, player, 2),
        "TD34 Destiny Board":
            lambda state: state.has("Destiny Board and its letters", player)
                          and state.has("Can Stall with Monsters", player)
                          and state.has("A Cat of Ill Omen", player)
                          and yugioh06_difficulty(state, player, 2),
        "TD35 Huge Damage in a Turn":
            lambda state: state.has_all(["Cyber-Stein", "Cyber Twin Dragon", "Megamorph"], player)
                          and yugioh06_difficulty(state, player, 3),
        "TD36 V-Z In the House":
            lambda state: state.has("VWXYZ-Dragon Catapult Cannon and the fusion materials", player)
                          and yugioh06_difficulty(state, player, 3),
        "TD37 Uria, Lord of Searing Flames":
            lambda state: state.has_all(["Uria, Lord of Searing Flames",
                                         "Embodiment of Apophis",
                                         "Skull Zoma",
                                         "Metal Reflect Slime"], player)
                          and yugioh06_difficulty(state, player, 3),
        "TD38 Hamon, Lord of Striking Thunder":
            lambda state: state.has("Hamon, Lord of Striking Thunder", player)
                          and yugioh06_difficulty(state, player, 3),
        "TD39 Raviel, Lord of Phantasms":
            lambda state: state.has_all(["Raviel, Lord of Phantasms", "Giant Germ"], player) and
                          state.count_from_list_unique(["Archfiend Soldier",
                                                        "Skull Descovery Knight",
                                                        "Slate Warrior",
                                                        "D. D. Trainer",
                                                        "Earthbound Spirit"], player) >= 3
                          and yugioh06_difficulty(state, player, 3),
        "TD40 Make a Chain":
            lambda state: state.has("Ultimate Offering", player)
                          and yugioh06_difficulty(state, player, 4),
        "TD41 The Gatekeeper Stands Tall":
            lambda state: state.has("Gate Guardian and its pieces", player) and
                          state.has_all(["Treeborn Frog", "Tribute Doll"], player)
                          and yugioh06_difficulty(state, player, 4),
        "TD42 Serious Damage":
            lambda state: yugioh06_difficulty(state, player, 3),
        "TD43 Return Monsters with Effects":
            lambda state: state.has_all(["Penguin Soldier", "Messenger of Peace"], player)
                          and yugioh06_difficulty(state, player, 4),
        "TD44 Fusion Summon":
            lambda state: state.has_all(["Fusion Gate", "Terraforming", "Dimension Fusion",
                                         "Return from the Different Dimension"], player) and
                          count_has_materials(state, ["Elemental Hero Flame Wingman",
                                                      "Elemental Hero Madballman",
                                                      "Elemental Hero Rampart Blaster",
                                                      "Elemental Hero Steam Healer",
                                                      "Elemental Hero Shining Flare Wingman",
                                                      "Elemental Hero Wildedge"], player) >= 4 and
                          yugioh06_difficulty(state, player, 7),
        "TD45 Big Damage at once":
            lambda state: state.has("Wave-Motion Cannon", player)
                          and yugioh06_difficulty(state, player, 3),
        "TD46 XYZ In the House":
            lambda state: state.has("XYZ-Dragon Cannon fusions and their materials", player) and
                          state.has("Dimension Fusion", player),
        "TD47 Spell Counter":
            lambda state: spell_counter(state, player) and yugioh06_difficulty(state, player, 3),
        "TD48 Destroy Monsters with Effects":
            lambda state: state.has_all(["Blade Rabbit", "Dream Clown"], player) and
                          state.has("Can Stall with ST", player) and
                          yugioh06_difficulty(state, player, 3),
        "TD49 Plunder":
            lambda state: take_control(state, player) and yugioh06_difficulty(state, player, 5),
        "TD50 Dark Scorpion Combination":
            lambda state: state.has("Dark Scorpion Combination and its required cards", player) and
                          state.has_all(["Reinforcement of the Army", "Mystic Tomato"], player) and
                          yugioh06_difficulty(state, player, 3)
    }
    multiworld.completion_condition[player] = lambda state: state.has("Goal", player)

    for loc in multiworld.get_locations(player):
        if loc.name in location_rules:
            add_rule(loc, location_rules[loc.name])
        if loc.name in access_rules:
            add_rule(multiworld.get_entrance(loc.name, player), access_rules[loc.name])


def only_light(state, player):
    return state.has_from_list_unique([
        "Dunames Dark Witch",
        "X-Head Cannon",
        "Homunculus the Alchemic Being",
        "Hysteric Fairy",
        "Ninja Grandmaster Sasuke"], player, 2)\
           and state.has_from_list_unique([
        "Chaos Command Magician",
        "Cybernetic Magician",
        "Kaiser Glider",
        "The Agent of Judgment - Saturn",
        "Zaborg the Thunder Monarch",
        "Cyber Dragon"], player, 1) \
           and state.has_from_list_unique([
        "D.D. Warrior Lady",
        "Mystic Swordsman LV2",
        "Y-Dragon Head",
        "Z-Metal Tank",
    ], player, 2) and state.has("Shining Angel", player)


def only_dark(state, player):
    return state.has_from_list_unique([
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
    ], player, 2) \
           and state.has_any([
        "Summoned Skull",
        "Skull Archfiend of Lightning",
        "The End of Anubis",
        "Dark Ruler Ha Des",
        "Beast of Talwar",
        "Inferno Hammer",
        "Jinzo",
        "Ryu Kokki"
    ], player) \
           and state.has_from_list_unique([
        "Legendary Fiend",
        "Don Zaloog",
        "Newdoria",
        "Sangan",
        "Spirit Reaper",
        "Giant Germ"
    ], player, 2) and state.has("Mystic Tomato", player)


def only_earth(state, player):
    return state.has_from_list_unique([
        "Berserk Gorilla",
        "Gemini Elf",
        "Insect Knight",
        "Toon Gemini Elf",
        "Familiar-Possessed - Aussa",
        "Neo Bug",
        "Blindly Loyal Goblin",
        "Chiron the Mage",
        "Gearfried the Iron Knight"
    ], player, 2) and state.has_any([
        "Dark Driceratops",
        "Granmarg the Rock Monarch",
        "Hieracosphinx",
        "Saber Beetle"
    ], player) and state.has_from_list_unique([
        "Hyper Hammerhead",
        "Green Gadget",
        "Red Gadget",
        "Yellow Gadget",
        "Dimensional Warrior",
        "Enraged Muka Muka",
        "Exiled Force"
    ], player, 2) and state.has("Giant Rat", player)


def only_water(state, player):
    return state.has_from_list_unique([
        "Gagagigo",
        "Familiar-Possessed - Eria",
        "7 Colored Fish",
        "Sea Serpent Warrior of Darkness",
        "Abyss Soldier"
    ], player, 2) and state.has_any([
        "Giga Gagagigo",
        "Amphibian Beast",
        "Terrorking Salmon",
        "Mobius the Frost Monarch"
    ], player) and state.has_from_list_unique([
        "Revival Jam",
        "Yomi Ship",
        "Treeborn Frog"
    ], player, 2) and state.has("Mother Grizzly", player)


def only_fire(state, player):
    return state.has_from_list_unique([
        "Blazing Inpachi",
        "Familiar-Possessed - Hiita",
        "Great Angus",
        "Fire Beaters"
    ], player, 2) and state.has_any([
        "Thestalos the Firestorm Monarch",
        "Horus the Black Flame Dragon LV6"
    ], player) and state.has_from_list_unique([
        "Solar Flare Dragon",
        "Tenkabito Shien",
        "Ultimate Baseball Kid"
    ], player, 2) and state.has("UFO Turtle", player)


def only_wind(state, player):
    return state.has_from_list_unique([
        "Luster Dragon",
        "Slate Warrior",
        "Spear Dragon",
        "Familiar-Possessed - Wynn",
        "Harpie's Brother",
        "Nin-Ken Dog",
        "Cyber Harpie Lady",
        "Oxygeddon"
    ], player, 2) and state.has_any([
        "Cyber-Tech Alligator",
        "Luster Dragon #2",
        "Armed Dragon LV5",
        "Roc from the Valley of Haze"
    ], player) and state.has_from_list_unique([
        "Armed Dragon LV3",
        "Twin-Headed Behemoth",
        "Harpie Lady 1"
    ], player, 2) and state.has("Flying Kamakiri 1", player)


def only_fairy(state, player):
    return state.has_any([
        "Dunames Dark Witch",
        "Hysteric Fairy"
    ], player) and (state.count_from_list_unique([
        "Dunames Dark Witch",
        "Hysteric Fairy",
        "Dancing Fairy",
        "Zolga",
        "Shining Angel",
        "Kelbek",
        "Mudora",
        "Asura Priest",
        "Cestus of Dagla"
    ], player) + (state.has_any([
        "The Agent of Judgment - Saturn",
        "Airknight Parshath"
    ], player))) >= 7


def only_warrior(state, player):
    return state.has_any([
        "Dark Blade",
        "Blindly Loyal Goblin",
        "D.D. Survivor",
        "Gearfried the Iron knight",
        "Ninja Grandmaster Sasuke",
        "Warrior Beaters"
    ], player) and (state.count_from_list_unique([
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
    ], player) + (state.has_any([
        "Freed the Matchless General",
        "Holy Knight Ishzark",
        "Silent Swordsman Lv5"
    ], player))) >= 7


def only_zombie(state, player):
    return state.has("Pyramid Turtle", player) \
           and state.has_from_list_unique([
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
    ], player, 6)


def only_dragon(state, player):
    return state.has_any([
        "Luster Dragon",
        "Spear Dragon",
        "Cave Dragon"
    ], player) and (state.count_from_list_unique([
        "Luster Dragon",
        "Spear Dragon",
        "Cave Dragon",
        "Armed Dragon LV3",
        "Masked Dragon",
        "Twin-Headed Behemoth",
        "Element Dragon",
        "Troop Dragon",
        "Horus the Black Flame Dragon LV4",
        "Stamping Destruction"
    ], player) + (state.has_any([
        "Luster Dragon #2",
        "Armed Dragon LV5",
        "Kaiser Glider",
        "Horus the Black Flame Dragon LV6"
    ], player))) >= 7


def only_spellcaster(state, player):
    return state.has_any([
        "Dark Elf",
        "Gemini Elf",
        "Skilled Dark Magician",
        "Toon Gemini Elf",
        "Kycoo the Ghost Destroyer",
        "Familiar-Possessed - Aussa"
    ], player) and (state.count_from_list_unique([
        "Dark Elf",
        "Gemini Elf",
        "Skilled Dark Magician",
        "Toon Gemini Elf",
        "Kycoo the Ghost Destroyer",
        "Familiar-Possessed - Aussa",
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
    ], player) + (state.has_any([
        "Chaos Command Magician",
        "Cybernetic Magician"
    ], player))) >= 7


def equip_unions(state, player):
    return (state.has_all(["Burning Beast", "Freezing Beast",
                           "Metallizing Parasite - Lunatite", "Mother Grizzly"], player) or
            state.has_all(["Dark Blade", "Pitch-Dark Dragon",
                           "Giant Orc", "Second Goblin", "Mystic Tomato"], player) or
            state.has_all(["Decayed Commander", "Zombie Tiger",
                           "Vampire Orchis", "Des Dendle", "Giant Rat"], player) or
            state.has_all(["Indomitable Fighter Lei Lei", "Protective Soul Ailin",
                           "V-Tiger Jet", "W-Wing Catapult", "Shining Angel"], player) or
            state.has_all(["X-Head Cannon", "Y-Dragon Head", "Z-Metal Tank", "Shining Angel"], player)) and\
           state.has_any(["Frontline Base", "Formation Union", "Roll Out!"], player)


def can_gain_lp_every_turn(state, player):
    return state.count_from_list_unique([
        "Solemn Wishes",
        "Cure Mermaid",
        "Dancing Fairy",
        "Princess Pikeru",
        "Kiseitai"], player) >= 3


def only_normal(state, player):
    return (state.has_from_list_unique([
        "Archfiend Soldier",
        "Gemini Elf",
        "Insect Knight",
        "Luster Dragon",
        "Mad Dog of Darkness",
        "Vorse Raider",
        "Blazing Inpachi",
        "Gagagigo",
        "Mechanicalchaser",
        "7 Colored Fish",
        "Dark Blade",
        "Dunames Dark Witch",
        "Giant Red Snake",
        "Gil Garth",
        "Great Angus",
        "Harpie's Brother",
        "La Jinn the Mystical Genie of the Lamp",
        "Neo Bug",
        "Nin-Ken Dog",
        "Opticlops",
        "Sea Serpent Warrior of Darkness",
        "X-Head Cannon",
        "Zure, Knight of Dark World"], player, 6) and
            state.has_any([
                "Cyber-Tech Alligator",
                "Summoned Skull",
                "Giga Gagagigo",
                "Amphibian Beast",
                "Beast of Talwar",
                "Luster Dragon #2",
                "Terrorking Salmon"], player))


def only_level(state, player):
    return (state.has("Level Up!", player) and
            (state.has_all(["Armed Dragon LV3", "Armed Dragon LV5"], player) +
             state.has_all(["Horus the Black Flame Dragon LV4", "Horus the Black Flame Dragon LV6"], player) +
             state.has_all(["Mystic Swordsman LV4", "Mystic Swordsman LV6"], player) +
             state.has_all(["Silent Swordsman Lv3", "Silent Swordsman Lv5"], player) +
             state.has_all(["Ultimate Insect Lv3", "Ultimate Insect Lv5"], player)) >= 3)


def spell_counter(state, player):
    return (state.has("Pitch-Black Power Stone", player) and
            state.has_from_list_unique(["Blast Magician",
                                        "Magical Marionette",
                                        "Mythical Beast Cerberus",
                                        "Royal Magical Library",
                                        "Spell-Counter Cards"], player, 2))


def take_control(state, player):
    return state.has_from_list_unique(["Aussa the Earth Charmer",
                                       "Jowls of Dark Demise",
                                       "Brain Control",
                                       "Creature Swap",
                                       "Enemy Controller",
                                       "Mind Control",
                                       "Magician of Faith"], player, 5)


def only_toons(state, player):
    return state.has_all(["Toon Gemini Elf",
                          "Toon Goblin Attack Force",
                          "Toon Masked Sorcerer",
                          "Toon Mermaid",
                          "Toon Dark Magician Girl",
                          "Toon World"], player)


def only_spirit(state, player):
    return state.has_all(["Asura Priest",
                          "Fushi No Tori",
                          "Maharaghi",
                          "Susa Soldier"], player)


def pacman_deck(state, player):
    return state.has_from_list_unique(["Des Lacooda",
                                       "Swarm of Locusts",
                                       "Swarm of Scarabs",
                                       "Wandering Mummy",
                                       "Golem Sentry",
                                       "Great Spirit",
                                       "Royal Keeper",
                                       "Stealth Bird"], player, 4)


def quick_plays(state, player):
    return state.has_from_list_unique(["Collapse",
                                       "Emergency Provisions",
                                       "Enemy Controller",
                                       "Graceful Dice",
                                       "Mystik Wok",
                                       "Offerings to the Doomed",
                                       "Poison of the Old Man",
                                       "Reload",
                                       "Rush Recklessly",
                                       "The Reliable Guardian"], player, 4)


def counter_traps(state, player):
    return state.has_from_list_unique(["Cursed Seal of the Forbidden Spell",
                                       "Divine Wrath",
                                       "Horn of Heaven",
                                       "Magic Drain",
                                       "Magic Jammer",
                                       "Negate Attack",
                                       "Seven Tools of the Bandit",
                                       "Solemn Judgment",
                                       "Spell Shield Type-8"], player, 5)


def back_row_removal(state, player):
    return state.has_from_list_unique(["Anteatereatingant",
                                       "B.E.S. Tetran",
                                       "Breaker the Magical Warrior",
                                       "Calamity of the Wicked",
                                       "Chiron the Mage",
                                       "Dust Tornado",
                                       "Heavy Storm",
                                       "Mystical Space Typhoon",
                                       "Mobius the Frost Monarch",
                                       "Raigeki Break",
                                       "Stamping Destruction",
                                       "Swarm of Locusts"], player, 2)
