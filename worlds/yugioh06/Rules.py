from worlds.generic.Rules import set_rule, add_rule
from .Fusions import count_has_materials
from worlds.yugioh06 import Limited_Duels, Theme_Duels, booster_packs


def set_rules(world):
    player = world.player
    world = world.multiworld

    # Campaign
    add_rule(world.get_location("Campaign Tier 1: 1 Win", player), lambda state: state.has("Tier 1 Beaten", player))
    add_rule(world.get_location("Campaign Tier 1: 3 Wins A", player),
             lambda state: state.has("Tier 1 Beaten", player, 3))
    add_rule(world.get_location("Campaign Tier 1: 3 Wins B", player),
             lambda state: state.has("Tier 1 Beaten", player, 3))
    add_rule(world.get_location("Campaign Tier 1: 5 Wins A", player),
             lambda state: state.has("Tier 1 Beaten", player, 5))
    add_rule(world.get_location("Campaign Tier 1: 5 Wins B", player),
             lambda state: state.has("Tier 1 Beaten", player, 5))
    add_rule(world.get_location("Campaign Tier 2: 1 Win", player), lambda state: state.has("Tier 2 Beaten", player))
    add_rule(world.get_location("Campaign Tier 2: 3 Wins A", player),
             lambda state: state.has("Tier 2 Beaten", player, 3))
    add_rule(world.get_location("Campaign Tier 2: 3 Wins B", player),
             lambda state: state.has("Tier 2 Beaten", player, 3))
    add_rule(world.get_location("Campaign Tier 2: 5 Wins A", player),
             lambda state: state.has("Tier 2 Beaten", player, 5))
    add_rule(world.get_location("Campaign Tier 2: 5 Wins B", player),
             lambda state: state.has("Tier 2 Beaten", player, 5))
    add_rule(world.get_location("Campaign Tier 3: 1 Win", player), lambda state: state.has("Tier 3 Beaten", player))
    add_rule(world.get_location("Campaign Tier 3: 3 Wins A", player),
             lambda state: state.has("Tier 3 Beaten", player, 3))
    add_rule(world.get_location("Campaign Tier 3: 3 Wins B", player),
             lambda state: state.has("Tier 3 Beaten", player, 3))
    add_rule(world.get_location("Campaign Tier 3: 5 Wins A", player),
             lambda state: state.has("Tier 3 Beaten", player, 5))
    add_rule(world.get_location("Campaign Tier 3: 5 Wins B", player),
             lambda state: state.has("Tier 3 Beaten", player, 5))
    add_rule(world.get_location("Campaign Tier 4: 5 Wins A", player),
             lambda state: state.has("Tier 4 Beaten", player, 5))
    add_rule(world.get_location("Campaign Tier 4: 5 Wins B", player),
             lambda state: state.has("Tier 4 Beaten", player, 5))

    # Bonuses
    add_rule(world.get_location("Duelist Bonus Level 1", player), lambda state: state.has("Tier 1 Beaten", player))
    add_rule(world.get_location("Duelist Bonus Level 2", player), lambda state: state.has("Tier 2 Beaten", player))
    add_rule(world.get_location("Duelist Bonus Level 3", player), lambda state: state.has("Tier 3 Beaten", player))
    add_rule(world.get_location("Duelist Bonus Level 4", player), lambda state: state.has("Tier 4 Beaten", player))
    add_rule(world.get_location("Duelist Bonus Level 5", player), lambda state: state.has("Tier 5 Beaten", player))
    add_rule(world.get_location("Max ATK Bonus", player), lambda state: state.yugioh06_difficulty(player, 2))
    add_rule(world.get_location("No Spell Cards Bonus", player), lambda state: state.yugioh06_difficulty(player, 2))
    add_rule(world.get_location("No Trap Cards Bonus", player), lambda state: state.yugioh06_difficulty(player, 2))
    add_rule(world.get_location("Low Deck Bonus", player),
             lambda state: state.has_any(["Reasoning", "Monster Gate", "Magical Merchant"], player) and
                           state.yugioh06_difficulty(player, 3))
    add_rule(world.get_location("Extremely Low Deck Bonus", player),
             lambda state: state.has_any(["Reasoning", "Monster Gate", "Magical Merchant"], player) and
                           state.yugioh06_difficulty(player, 5))
    add_rule(world.get_location("Exactly 0 LP Bonus", player), lambda state: state.yugioh06_difficulty(player, 2))
    add_rule(world.get_location("Quick Finish Bonus", player), lambda state: state.has("Quick-Finish", player))
    add_rule(world.get_location("Exodia Finish Bonus", player), lambda state: state.yugioh06_can_exodia_win(player))
    add_rule(world.get_location("Last Turn Finish Bonus", player),
             lambda state: state.yugioh06_can_last_turn_win(player))
    add_rule(world.get_location("Yata-Garasu Finish Bonus", player),
             lambda state: state.yugioh06_can_yata_lock(player))
    add_rule(world.get_location("Skull Servant Finish Bonus", player),
             lambda state: state.has("Skull Servant", player) and state.yugioh06_difficulty(player, 3))
    add_rule(world.get_location("Konami Bonus", player), lambda state: state.yugioh06_can_get_konami_bonus(player))
    # placeholder
    # TODO: Add more ways to do over 4000 at once
    add_rule(world.get_location("Max Damage Bonus", player),
             lambda state: state.has_any(["Wave-Motion Cannon", "Megamorph", "United We Stand"], player))
    # TODO: Special Summon Collection C isn't handled yet
    add_rule(world.get_location("Fusion Summon Bonus", player),
             lambda state: state.has_any(["Polymerization", "Fusion Gate", "Power Bond"], player))
    # TODO: Probably missing some from side sets
    add_rule(world.get_location("Ritual Summon Bonus", player), lambda state: state.has("Ritual", player))
    add_rule(world.get_location("Over 20000 LP Bonus", player),
             lambda state: can_gain_lp_every_turn(state, player) and state.yugioh06_can_stall_with_st(player))
    add_rule(world.get_location("Low LP Bonus", player),
             lambda state: state.has("Wall of Revealing Light", player) and state.yugioh06_difficulty(player, 2))
    add_rule(world.get_location("Extremely Low LP Bonus", player),
             lambda state: state.has_all(["Wall of Revealing Light", "Messenger of Peace"], player)
             and state.yugioh06_difficulty(player, 4))
    add_rule(world.get_location("Effect Damage Only Bonus", player),
             lambda state: state.has_all(["Solar Flare Dragon", "UFO Turtle"], player)
             or state.has("Wave-Motion Cannon", player)
             or state.can_reach("Final Countdown Finish Bonus", 'Location', player)
             or state.can_reach("Destiny Board Finish Bonus", 'Location', player)
             or state.can_reach("Exodia Finish Bonus", 'Location', player)
             or state.can_reach("Last Turn Finish Bonus", 'Location', player))
    add_rule(world.get_location("No More Cards Bonus", player),
             lambda state: state.has_any(["Cyber Jar", "Morphing Jar", "Morphing Jar #2", "Needle Worm"], player)
             and state.has_any(["The Shallow Grave", "Spear Cretin"], player) and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_location("Final Countdown Finish Bonus", player),
             lambda state: state.has("Final Countdown", player) and state.yugioh06_can_stall_with_st(player))
    add_rule(world.get_location("Destiny Board Finish Bonus", player),
             lambda state: state.yugioh06_can_stall_with_monsters(player) and state.yugioh06_has_destiny_board(player)
             and state.has("A Cat of Ill Omen", player))

    # Cards
    add_rule(world.get_location("Obtain all pieces of Exodia", player),
             lambda state: state.has("Exodia", player))
    add_rule(world.get_location("Obtain Final Countdown", player),
             lambda state: state.has("Final Countdown", player))
    add_rule(world.get_location("Obtain Victory Dragon", player),
             lambda state: state.has("Victory D.", player))
    add_rule(world.get_location("Obtain Ojama Delta Hurricane and its required cards", player),
             lambda state: state.yugioh06_has_ojama_delta_hurricane(player))
    add_rule(world.get_location("Obtain Huge Revolution and its required cards", player),
             lambda state: state.yugioh06_has_huge_revolution(player))
    add_rule(world.get_location("Obtain Perfectly Ultimate Great Moth and its required cards", player),
             lambda state: state.yugioh06_has_perfectly_ultimate_great_moth(player))
    add_rule(world.get_location("Obtain Valkyrion the Magna Warrior and its pieces", player),
             lambda state: state.yugioh06_has_valkyrion_the_magna_warrior(player))
    add_rule(world.get_location("Dark Sage and its required cards", player),
             lambda state: state.yugioh06_has_dark_sage(player))
    add_rule(world.get_location("Obtain Destiny Board and its letters", player),
             lambda state: state.yugioh06_has_destiny_board(player))
    add_rule(world.get_location("Obtain all XYZ-Dragon Cannon fusions and their materials", player),
             lambda state: state.yugioh06_has_all_xyz_dragon_cannon_fusions(player))
    add_rule(world.get_location("Obtain VWXYZ-Dragon Catapult Cannon and the fusion materials", player),
             lambda state: state.yugioh06_has_vwxyz_dragon_catapult_cannon(player))
    add_rule(world.get_location("Obtain Hamon, Lord of Striking Thunder", player),
             lambda state: state.has("Hamon, Lord of Striking Thunder", player))
    add_rule(world.get_location("Obtain Raviel, Lord of Phantasms", player),
             lambda state: state.has("Raviel, Lord of Phantasms", player))
    add_rule(world.get_location("Obtain Uria, Lord of Searing Flames", player),
             lambda state: state.has("Uria, Lord of Searing Flames", player))
    add_rule(world.get_location("Obtain Gate Guardian and its pieces", player),
             lambda state: state.yugioh06_has_gate_guardian(player))
    add_rule(world.get_location("Dark Scorpion Combination and its required cards", player),
             lambda state: state.yugioh06_has_dark_scorpion_combination(player))

    # Limited
    add_rule(world.get_entrance("LD01 All except Level 4 forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("LD02 Medium/high Level forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 2))
    add_rule(world.get_entrance("LD03 ATK 1500 or more forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 6))
    add_rule(world.get_entrance("LD04 Flip Effects forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 4))
    add_rule(world.get_entrance("LD05 Tributes forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 2))
    add_rule(world.get_entrance("LD06 Traps forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 2))
    add_rule(world.get_entrance("LD07 Large Deck A", player),
             lambda state: state.yugioh06_difficulty(player, 2))
    add_rule(world.get_entrance("LD08 Large Deck B", player),
             lambda state: state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("LD09 Sets Forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 2))
    add_rule(world.get_entrance("LD10 All except LV monsters forbidden", player),
             lambda state: only_level(state, player) and state.yugioh06_difficulty(player, 4))
    add_rule(world.get_entrance("LD11 All except Fairies forbidden", player),
             lambda state: only_fairy(state, player) and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("LD12 All except Wind forbidden", player),
             lambda state: only_wind(state, player) and state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("LD13 All except monsters forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("LD14 Level 3 or below forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 6))
    add_rule(world.get_entrance("LD15 DEF 1500 or less forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("LD16 Effect Monsters forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("LD17 Spells forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("LD18 Attacks forbidden", player),
             lambda state: state.has_all(["Wave-Motion Cannon", "Stealth Bird"], player)
             and state.yugioh06_has_individual(["Dark World Lightning", "Nobleman of Crossout",
                                                "Shield Crash", "Tribute to the Doomed"], player) >= 2
             and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("LD19 All except E-Hero's forbidden", player),
             lambda state: state.has_any(["Polymerization", "Fusion Gate"], player) and
             count_has_materials(state, ["Elemental Hero Flame Wingman",
                                         "Elemental Hero Madballman",
                                         "Elemental Hero Rampart Blaster",
                                         "Elemental Hero Steam Healer",
                                         "Elemental Hero Shining Flare Wingman",
                                         "Elemental Hero Wildedge"], player) >= 3 and
             state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("LD20 All except Warriors forbidden", player),
             lambda state: only_warrior(state, player) and state.yugioh06_difficulty(player, 4))
    add_rule(world.get_entrance("LD21 All except Dark forbidden", player),
             lambda state: only_dark(state, player) and state.yugioh06_difficulty(player, 2))
    add_rule(world.get_entrance("LD22 All limited cards forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 4))
    add_rule(world.get_entrance("LD23 Refer to Mar 05 Banlist", player),
             lambda state: state.yugioh06_difficulty(player, 7))
    add_rule(world.get_entrance("LD24 Refer to Sept 04 Banlist", player),
             lambda state: state.yugioh06_difficulty(player, 7))
    add_rule(world.get_entrance("LD25 Low Life Points", player),
             lambda state: state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("LD26 All except Toons forbidden", player),
             lambda state: only_toons(state, player) and state.yugioh06_difficulty(player, 4))
    add_rule(world.get_entrance("LD27 All except Spirits forbidden", player),
             lambda state: only_spirit(state, player) and state.yugioh06_difficulty(player, 7))
    add_rule(world.get_entrance("LD28 All except Dragons forbidden", player),
             lambda state: only_dragon(state, player) and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("LD29 All except Spellcasters forbidden", player),
             lambda state: only_spellcaster(state, player) and state.yugioh06_difficulty(player, 9))
    add_rule(world.get_entrance("LD30 All except Light forbidden", player),
             lambda state: only_light(state, player) and state.yugioh06_difficulty(player, 4))
    add_rule(world.get_entrance("LD31 All except Fire forbidden", player),
             lambda state: only_fire(state, player) and state.yugioh06_difficulty(player, 4))
    add_rule(world.get_entrance("LD32 Decks with multiples forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 7))
    add_rule(world.get_entrance("LD33 Special Summons forbidden", player),
             lambda state: state.yugioh06_difficulty(player, 7))
    add_rule(world.get_entrance("LD34 Normal Summons forbidden", player),
             lambda state: state.has_all(["Polymerization", "King of the Swamp"], player) and
             count_has_materials(state, ["Elemental Hero Flame Wingman",
                                         "Elemental Hero Madballman",
                                         "Elemental Hero Rampart Blaster",
                                         "Elemental Hero Steam Healer",
                                         "Elemental Hero Shining Flare Wingman",
                                         "Elemental Hero Wildedge"], player) >= 3 and
             state.yugioh06_difficulty(player, 7))
    add_rule(world.get_entrance("LD35 All except Zombies forbidden", player),
             lambda state: only_zombie(state, player) and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("LD36 All except Earth forbidden", player),
             lambda state: only_earth(state, player) and state.yugioh06_difficulty(player, 4))
    add_rule(world.get_entrance("LD37 All except Water forbidden", player),
             lambda state: only_water(state, player) and state.yugioh06_difficulty(player, 4))
    add_rule(world.get_entrance("LD38 Refer to Mar 04 Banlist", player),
             lambda state: state.yugioh06_difficulty(player, 8))
    add_rule(world.get_entrance("LD39 Monsters forbidden", player),
             lambda state: state.has_all(["Skull Zoma", "Embodiment of Apophis"], player)
             and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("LD40 Refer to Sept 05 Banlist", player),
             lambda state: state.yugioh06_difficulty(player, 8))
    add_rule(world.get_entrance("LD41 Refer to Sept 03 Banlist", player),
             lambda state: state.yugioh06_difficulty(player, 8))
    # Theme Duels
    add_rule(world.get_entrance("TD01 Battle Damage", player),
             lambda state: state.yugioh06_difficulty(player, 1))
    add_rule(world.get_entrance("TD02 Deflected Damage", player),
             lambda state: state.has("Fairy Box", player) and state.yugioh06_difficulty(player, 1))
    add_rule(world.get_entrance("TD03 Normal Summon", player),
             lambda state: only_normal(state, player) and state.yugioh06_difficulty(player, 3))
    # TODO: Need Specific deck
    add_rule(world.get_entrance("TD04 Ritual Summon", player),
             lambda state: state.yugioh06_difficulty(player, 18))
    add_rule(world.get_entrance("TD05 Special Summon A", player),
             lambda state: state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("TD06 20x Spell", player),
             lambda state: state.has("Magical Blast", player) and state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("TD07 10x Trap", player),
             lambda state: state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("TD08 Draw", player),
             lambda state: state.has_any(["Self-Destruct Button", "Dark Snake Syndrome"], player) and
                           state.yugioh06_difficulty(player, 3))
    # TODO: Add more ways
    add_rule(world.get_entrance("TD09 Hand Destruction", player),
             lambda state: state.has_all(["Cyber Jar",
                                          "Morphing Jar",
                                          "Book of Moon",
                                          "Book of Taiyou",
                                          "Card Destruction",
                                          "Serial Spell",
                                          "Spell Reproduction",
                                          "The Shallow Grave"], player) and state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("TD10 During Opponent's Turn", player),
             lambda state: state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("TD11 Recover", player),
             lambda state: can_gain_lp_every_turn(state, player) and state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("TD12 Remove Monsters by Effect", player),
             lambda state: state.has("Soul Release", player) and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD13 Flip Summon", player),
             lambda state: pacman_deck(state, player) and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD14 Special Summon B", player),
             lambda state: state.has_any(["Manticore of Darkness", "Treeborn Frog"], player) and
                           state.has("Foolish Burial", player) and
                           state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD15 Token", player),
             lambda state: state.has_all(["Dandylion", "Ojama Trio", "Stray Lambs"], player) and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD16 Union", player),
             lambda state: equip_unions(state, player) and
                           state.yugioh06_difficulty(player, 2))
    add_rule(world.get_entrance("TD17 10x Quick Spell", player),
             lambda state: quick_plays(state, player) and
                           state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("TD18 The Forbidden", player),
             lambda state: state.yugioh06_can_exodia_win(player))
    add_rule(world.get_entrance("TD19 20 Turns", player),
             lambda state: state.has("Final Countdown", player) and state.yugioh06_can_stall_with_st(player) and
                           state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("TD20 Deck Destruction", player),
             lambda state: state.has_any(["Cyber Jar", "Morphing Jar", "Morphing Jar #2", "Needle Worm"], player)
             and state.has_any(["The Shallow Grave", "Spear Cretin"], player) and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD21 Victory D.", player),
             lambda state: state.has("Victory D.", player) and only_dragon(state, player)
             and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD22 The Preventers Fight Back", player),
             lambda state: state.yugioh06_has_ojama_delta_hurricane(player) and
                           state.has_all(["Rescue Cat", "Enchanting Fitting Room", "Jerry Beans Man"], player) and
                           state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("TD23 Huge Revolution", player),
             lambda state: state.yugioh06_has_huge_revolution(player) and
                           state.has_all(["Enchanting Fitting Room", "Jerry Beans Man"], player) and
                           state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("TD24 Victory in 5 Turns", player),
             lambda state: state.yugioh06_difficulty(player, 6))
    add_rule(world.get_entrance("TD25 Moth Grows Up", player),
             lambda state: state.yugioh06_has_perfectly_ultimate_great_moth(player) and
                           state.has_all(["Gokipon", "Howling Insect"], player) and
                           state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD26 Magnetic Power", player),
             lambda state: state.yugioh06_has_valkyrion_the_magna_warrior(player) and
                           state.yugioh06_difficulty(player, 4))
    add_rule(world.get_entrance("TD27 Dark Sage", player),
             lambda state: state.yugioh06_has_dark_sage(player) and
                           state.has_any(["Skilled Dark Magician", "Dark Magic Curtain"], player) and
                           state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD28 Direct Damage", player),
             lambda state: state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD29 Destroy Monsters in Battle", player),
             lambda state: state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD30 Tribute Summon", player),
             lambda state: state.has("Treeborn Frog", player) and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD31 Special Summon C", player),
             lambda state: state.yugioh06_has_individual(
                 ["Aqua Spirit", "Rock Spirit", "Spirit of Flames",
                  "Garuda the Wind Spirit", "Gigantes", "Inferno", "Megarock Dragon", "Silpheed"],
                 player) > 4 and state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("TD32 Toon", player),
             lambda state: only_toons(state, player) and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD33 10x Counter", player),
             lambda state: counter_traps(state, player) and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD34 Destiny Board", player),
             lambda state: state.yugioh06_has_destiny_board(player)
                           and state.yugioh06_can_stall_with_monsters(player)
                           and state.has("A Cat of Ill Omen", player)
                           and state.yugioh06_difficulty(player, 2))
    # TODO: Add more OTKs
    add_rule(world.get_entrance("TD35 Huge Damage in a Turn", player),
             lambda state: state.has_all(["Cyber-Stein", "Cyber Twin Dragon", "Megamorph"], player)
                           and state.yugioh06_difficulty(player, 7))
    add_rule(world.get_entrance("TD36 V-Z In the House", player),
             lambda state: state.yugioh06_has_vwxyz_dragon_catapult_cannon(player)
                           and state.yugioh06_difficulty(player, 7))
    add_rule(world.get_entrance("TD37 Uria, Lord of Searing Flames", player),
             lambda state: state.has_all(["Uria, Lord of Searing Flames",
                                          "Embodiment of Apophis",
                                          "Skull Zoma",
                                          "Metal Reflect Slime"], player)
                           and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD38 Hamon, Lord of Striking Thunder", player),
             lambda state: state.has("Hamon, Lord of Striking Thunder", player)
                           and state.yugioh06_difficulty(player, 7))
    add_rule(world.get_entrance("TD39 Raviel, Lord of Phantasms", player),
             lambda state: state.has_all(["Raviel, Lord of Phantasms", "Giant Germ"], player) and
                           state.yugioh06_has_individual(["Archfiend Soldier",
                                                          "Skull Descovery Knight",
                                                          "Slate Warrior",
                                                          "D. D. Trainer",
                                                          "Earthbound Spirit"], player) >= 3
                           and state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD40 Make a Chain", player),
             lambda state: state.has("Ultimate Offering", player)
                           and state.yugioh06_difficulty(player, 7))
    add_rule(world.get_entrance("TD41 The Gatekeeper Stands Tall", player),
             lambda state: state.yugioh06_has_gate_guardian(player) and
                           state.has_all(["Treeborn Frog", "Tribute Doll"], player)
                           and state.yugioh06_difficulty(player, 9))
    add_rule(world.get_entrance("TD42 Serious Damage", player),
             lambda state: state.yugioh06_difficulty(player, 9))
    add_rule(world.get_entrance("TD43 Return Monsters with Effects", player),
             lambda state: state.has_all(["Penguin Soldier", "Messenger of Peace"], player)
                           and state.yugioh06_difficulty(player, 9))
    add_rule(world.get_entrance("TD44 Fusion Summon", player),
             lambda state: state.has_all(["Fusion Gate", "Terraforming", "Dimension Fusion",
                                          "Return from the Different Dimension"], player) and
             count_has_materials(state, ["Elemental Hero Flame Wingman",
                                         "Elemental Hero Madballman",
                                         "Elemental Hero Rampart Blaster",
                                         "Elemental Hero Steam Healer",
                                         "Elemental Hero Shining Flare Wingman",
                                         "Elemental Hero Wildedge"], player) >= 4 and
             state.yugioh06_difficulty(player, 7))
    add_rule(world.get_entrance("TD45 Big Damage at once", player),
             lambda state: state.has("Wave-Motion Cannon", player)
                           and state.yugioh06_difficulty(player, 7))
    add_rule(world.get_entrance("TD46 XYZ In the House", player),
             lambda state: state.yugioh06_has_all_xyz_dragon_cannon_fusions(player)
                           and state.has("Dimension Fusion", player))
    add_rule(world.get_entrance("TD47 Spell Counter", player),
             lambda state: spell_counter(state, player) and state.yugioh06_difficulty(player, 3))
    add_rule(world.get_entrance("TD48 Destroy Monsters with Effects", player),
             lambda state: state.has_all(["Blade Rabbit", "Dream Clown"], player) and
                           state.yugioh06_can_stall_with_st(player) and
                           state.yugioh06_difficulty(player, 5))
    add_rule(world.get_entrance("TD49 Plunder", player),
             lambda state: take_control(state, player) and state.yugioh06_difficulty(player, 7))
    add_rule(world.get_entrance("TD50 Dark Scorpion Combination", player),
             lambda state: state.yugioh06_has_dark_scorpion_combination(player) and
                           state.has_all(["Reinforcement of the Army", "Mystic Tomato"], player) and
                           state.yugioh06_difficulty(player, 4))
    world.completion_condition[player] = lambda state: state.has("Goal", player)


def only_light(state, player):
    return state.yugioh06_has_individual([
        "Dunames Dark Witch",
        "X-Head Cannon",
        "Homunculus the Alchemic Being",
        "Hysteric Fairy",
        "Ninja Grandmaster Sasuke"], player) >= 2 \
           and state.yugioh06_has_individual([
        "Chaos Command Magician",
        "Cybernetic Magician",
        "Kaiser Glider",
        "The Agent of Judgment - Saturn",
        "Zaborg the Thunder Monarch",
        "Cyber Dragon"], player) >= 1 \
           and state.yugioh06_has_individual([
        "D.D. Warrior Lady",
        "Mystic Swordsman LV2",
        "Y-Dragon Head",
        "Z-Metal Tank",
    ], player) >= 2 and state.has("Shining Angel", player)


def only_dark(state, player):
    return state.yugioh06_has_individual([
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
    ], player) >= 2 \
           and state.yugioh06_has_individual([
        "Summoned Skull",
        "Skull Archfiend of Lightning",
        "The End of Anubis",
        "Dark Ruler Ha Des",
        "Beast of Talwar",
        "Inferno Hammer",
        "Jinzo",
        "Ryu Kokki"
    ], player) >= 1 \
           and state.yugioh06_has_individual([
        "Legendary Fiend",
        "Don Zaloog",
        "Newdoria",
        "Sangan",
        "Spirit Reaper",
        "Giant Germ"
    ], player) >= 2 and state.has("Mystic Tomato", player)


def only_earth(state, player):
    return state.yugioh06_has_individual([
        "Berserk Gorilla",
        "Gemini Elf",
        "Insect Knight",
        "Toon Gemini Elf",
        "Familiar-Possessed - Aussa",
        "Neo Bug",
        "Blindly Loyal Goblin",
        "Chiron the Mage",
        "Gearfried the Iron Knight"
    ], player) >= 2 and state.yugioh06_has_individual([
        "Dark Driceratops",
        "Granmarg the Rock Monarch",
        "Hieracosphinx",
        "Saber Beetle"
    ], player) >= 1 and state.yugioh06_has_individual([
        "Hyper Hammerhead",
        "Green Gadget",
        "Red Gadget",
        "Yellow Gadget",
        "Dimensional Warrior",
        "Enraged Muka Muka",
        "Exiled Force"
    ], player) >= 2 and state.has("Giant Rat", player)


def only_water(state, player):
    return state.yugioh06_has_individual([
        "Gagagigo",
        "Familiar-Possessed - Eri",
        "7 Colored Fish",
        "Sea Serpent Warrior of Darkness",
        "Abyss Soldier"
    ], player) >= 2 and state.yugioh06_has_individual([
        "Giga Gagagigo",
        "Amphibian Beast",
        "Terrorking Salmon",
        "Mobius the Frost Monarch"
    ], player) >= 1 and state.yugioh06_has_individual([
        "Revival Jam",
        "Yomi Ship",
        "Treeborn Frog"
    ], player) >= 2 and state.has("Mother Grizzly", player)


def only_fire(state, player):
    return state.yugioh06_has_individual([
        "Blazing Inpachi",
        "Familia-Possesed - Hiita",
        "Great Angus",
        "Fire Beaters"
    ], player) >= 2 and state.yugioh06_has_individual([
        "Thestalos the Firestorm Monarch",
        "Horus the Black Flame Dragon LV6"
    ], player) >= 1 and state.yugioh06_has_individual([
        "Solar Flare Dragon",
        "Tenkabito Shien",
        "Ultimate Baseball Kid"
    ], player) >= 2 and state.has("UFO Turtle", player)


def only_wind(state, player):
    return state.yugioh06_has_individual([
        "Luster Dragon",
        "Slate Warrior",
        "Spear Dragon",
        "Familiar-Possed - Wyn",
        "Harpie's Brother",
        "Nin-Ken Dog",
        "Cyber Harpie Lady",
        "Oxygeddon"
    ], player) >= 2 and state.yugioh06_has_individual([
        "Cyber-Tech Alligator",
        "Luster Dragon #2",
        "Armed Dragon LV5",
        "Roc from the Valley of Haze"
    ], player) >= 1 and state.yugioh06_has_individual([
        "Armed Dragon LV3",
        "Twin-Headed Behemoth",
        "Harpie Lady 1"
    ], player) >= 2 and state.has("Flying Kamakiri 1", player)


def only_fairy(state, player):
    return state.yugioh06_has_individual([
        "Dunames Dark Witch",
        "Hysteric Fairy"
    ], player) >= 1 and (state.yugioh06_has_individual([
        "Dunames Dark Witch",
        "Hysteric Fairy",
        "Dancing Fairy",
        "Zolga",
        "Shining Angel",
        "Kelbek",
        "Mudora",
        "Asura Priest",
        "Cestus of Dagla"
    ], player) + (state.yugioh06_has_individual([
        "The Agent of Judgment - Saturn",
        "Airknight Parshath"
    ], player) >= 1)) >= 7


def only_warrior(state, player):
    return state.yugioh06_has_individual([
        "Dark Blade",
        "Blindly Loyal Goblin",
        "D.D. Survivor",
        "Gearfried the Iron knight",
        "Ninja Grandmaster Sasuke",
        "Warrior Beaters"
    ], player) >= 1 and (state.yugioh06_has_individual([
        "Dark Blade",
        "Blindly Loyal Goblin",
        "D.D. Survivor",
        "Gearfried the Iron knight",
        "Ninja Grandmaster Sasuke",
        "Warrior Beaters",
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
    ], player) + (state.yugioh06_has_individual([
        "Freed the Matchless General",
        "Holy Knight Ishzark",
        "Silent Swordsman Lv5"
    ], player) >= 1)) >= 7


def only_zombie(state, player):
    return state.has("Pyramid Turtle", player) \
           and state.yugioh06_has_individual([
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
    ], player) >= 6


def only_dragon(state, player):
    return state.yugioh06_has_individual([
        "Luster Dragon",
        "Spear Dragon",
        "Cave Dragon"
    ], player) >= 1 and (state.yugioh06_has_individual([
        "Luster Dragon",
        "Spear Dragon",
        "Cave Dragon"
        "Armed Dragon LV3",
        "Masked Dragon",
        "Twin-Headed Behemotha",
        "Element Dragon",
        "Troop Dragon",
        "Horus the Black Flame Dragon LV4",
        "Stamping Destruction"
    ], player) + (state.yugioh06_has_individual([
        "Luster Dragon #2",
        "Armed Dragon Lv5",
        "Kaiser Glider",
        "Horus the Black Flame Dragon Lv6"
    ], player) >= 1)) >= 7


def only_spellcaster(state, player):
    return state.yugioh06_has_individual([
        "Dark Elf",
        "Gemini Elf",
        "Skilled Dark Magician",
        "Toon Gemini Elf",
        "Kycoo the Ghost Destroyer",
        "Familiar-Possessed - Aussa"
    ], player) >= 1 and (state.yugioh06_has_individual([
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
    return (state.has("Burning Beast", player) and state.has("Freezing Beast", player) and
            state.has("Metallizing Parasite - Lunatite", player) and state.has("Mother Grizzly", player) or \
            state.has("Dark Blade", player) and state.has("Pitch-Dark Dragon", player) and
            state.has("Giant Orc", player) and state.has("Second Goblin", player) and
            state.has("Mystic Tomato", player) or
            state.has("Decayed Commander", player) and state.has("Zombie Tiger", player) and
            state.has("Vampire Orchis", player) and state.has("Des Dendle", player) and
            state.has("Giant Rat", player) or
            state.has("Indomitable Fighter Lei Lei", player) and state.has("Protective Soul Ailin", player) and \
            state.has("V-Tiger Jet", player) and state.has("W-Wing Catapult", player) and
            state.has("Shining Angel", player) or
            state.has("X-Head Cannon", player) and state.has("Y-Dragon Head", player) and
            state.has("Z-Metal Tank", player) and state.has("Shining Angel", player)) and \
           state.yugioh06_has_individual(["Frontline Base", "Formation Union", "Roll Out!"], player) > 0


def can_gain_lp_every_turn(state, player):
    return state.yugioh06_has_individual([
        "Solemn Wishes",
        "Cure Mermaid",
        "Dancing Fairy",
        "Princess Pikeru",
        "Kiseitai"], player) >= 3


def only_normal(state, player):
    return (state.yugioh06_has_individual([
        "Archfiend Soldier",
        "Gemini Elf",
        "Insect Knight",
        "Luster Dragon",
        "Mad Dog of Darkness",
        "Vorse Raider",
        "Blazing Inpachi",
        "Gagagigo",
        "Mechanical Chaser",
        "7 Colored Fish",
        "Dark Blade",
        "Dunames Dark Witch",
        "Giant Red Snake",
        "Gil Garth",
        "Great Agnus",
        "Harpie's Brother",
        "La Jinn the Mystical Genie of the Lamp",
        "Neo Bug",
        "Nin-Ken Dog",
        "Opticlops",
        "Sea Serpent Warrior of Darkness",
        "X-Head Cannon",
        "Zure, Knight of Dark World"], player) >= 6 and
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
            state.yugioh06_has_individual(["Blast Magician",
                                           "Magical Marionette",
                                           "Mythical Beast Cerberus",
                                           "Royal Magical Library",
                                           "Spell-Counter Cards"], player) >= 2)


def take_control(state, player):
    return state.yugioh06_has_individual(["Aussa the Earth Charmer",
                                          "Jowls of Dark Demise",
                                          "Brain Control",
                                          "Creature Swap",
                                          "Enemy Controller",
                                          "Mind Control",
                                          "Magician of Faith"], player) >= 5


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
    return state.yugioh06_has_individual(["Des Lacooda",
                                          "Swarm of Locusts",
                                          "Swarm of Scarabs",
                                          "Wandering Mummy",
                                          "Golem Sentry",
                                          "Great Spirit",
                                          "Royal Keeper",
                                          "Stealth Bird"], player) >= 4


def quick_plays(state, player):
    return state.yugioh06_has_individual(["Collapse",
                                          "Emergency Provisions",
                                          "Enemy controller",
                                          "Graceful Dice",
                                          "Mystik Wok",
                                          "Offerings to the Doomed",
                                          "Poison of the Old Man",
                                          "Reload",
                                          "Rush Recklessly",
                                          "The Reliable Guardian"], player) >= 4


def counter_traps(state, player):
    return state.yugioh06_has_individual(["Cursed Seal of the Forbidden Spell",
                                          "Divine Wrath",
                                          "Horn of Heaven",
                                          "Magic Drain",
                                          "Magic Jammer",
                                          "Negate Attack",
                                          "Seven Tools of the Bandit",
                                          "Solemn Judgment",
                                          "Spell Shield Type-8"], player) >= 5

