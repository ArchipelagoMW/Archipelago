from worlds.generic.Rules import add_rule

from . import yugioh06_difficulty


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
        "Max ATK Bonus": lambda state: state.has_all(world.progression_cards["Max ATK Bonus"], player),
        "No Spell Cards Bonus": lambda state: state.has_all(world.progression_cards["No Spell Cards Bonus"], player),
        "No Trap Cards Bonus": lambda state: state.has_all(world.progression_cards["No Trap Cards Bonus"], player),
        "No Damage Bonus": lambda state: state.has_group("Campaign Boss Beaten", player, 3),
        "Low Deck Bonus": lambda state: state.has("Can Self Mill", player),
        "Extremely Low Deck Bonus": lambda state: state.has("Can Self Mill", player),
        "Opponent's Turn Finish Bonus": lambda state:state.has_all(
            world.progression_cards["Opponent's Turn Finish Bonus"], player),
        "Exactly 0 LP Bonus": lambda state: state.has_group("Campaign Boss Beaten", player, 3),
        "Reversal Finish Bonus": lambda state: state.has_group("Campaign Boss Beaten", player, 3),
        "Quick Finish Bonus": lambda state: state.has("Quick-Finish", player) or
                                            state.has_group("Campaign Boss Beaten", player, 6),
        "Exodia Finish Bonus": lambda state: state.has("Can Exodia Win", player),
        "Last Turn Finish Bonus": lambda state: state.has("Can Last Turn Win", player),
        "Yata-Garasu Finish Bonus": lambda state: state.has("Can Yata Lock", player),
        "Skull Servant Finish Bonus": lambda state: state.has_all(world.progression_cards["Skull Servant Finish Bonus"],
                                                                  player),
        "Konami Bonus": lambda state: state.has_all(world.progression_cards["Konami Bonus"], player),
        "Max Damage Bonus": lambda state: state.has_all(world.progression_cards["Max Damage Bonus"], player),
        "Tribute Summon Bonus": lambda state: state.has_all(world.progression_cards["Tribute Summon Bonus"], player),
        "Fusion Summon Bonus": lambda state: state.has_all(world.progression_cards["Fusion Summon Bonus"], player),
        "Ritual Summon Bonus": lambda state: state.has_all(world.progression_cards["Ritual Summon Bonus"], player),
        "Over 20000 LP Bonus": lambda state: state.has("Can Gain LP Every Turn", player) and state.has(
            "Can Stall with ST", player),
        "Low LP Bonus": lambda state: state.has_all(world.progression_cards["Low LP Bonus"], player),
        "Extremely Low LP Bonus": lambda state: state.has_all(world.progression_cards["Extremely Low LP Bonus"],
                                                              player),
        "Effect Damage Only Bonus": lambda state: state.has_all(world.progression_cards["Effect Damage Only Bonus"],
                                                                player)
                                                  or state.can_reach("Destiny Board Finish Bonus", "Location", player)
                                                  or state.has("Can Exodia Win", player)
                                                  or state.has("Can Last Turn Win", player),
        "No More Cards Bonus": lambda state: state.has_all(world.progression_cards["No More Cards Bonus"], player),
        "Final Countdown Finish Bonus": lambda state: state.has_all(
            world.progression_cards["Final Countdown Finish Bonus"], player)
                                                      and state.has("Can Stall with ST", player),
        "Destiny Board Finish Bonus": lambda state: state.has("Can Stall with Monsters", player) and
                                                    state.has("Destiny Board and its letters", player) and
                                                    state.has_all(world.progression_cards["Destiny Board Finish Bonus"],
                                                                  player),

        # Cards
        "Obtain all pieces of Exodia": lambda state: state.has("Exodia", player),
        "Obtain Final Countdown": lambda state: state.has_all(world.progression_cards["Obtain Final Countdown"],
                                                              player),
        "Obtain Victory Dragon": lambda state: state.has_all(world.progression_cards["Obtain Victory Dragon"], player),
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
            lambda state: state.has_all(world.progression_cards["Obtain Hamon, Lord of Striking Thunder"], player),
        "Obtain Raviel, Lord of Phantasms":
            lambda state: state.has_all(world.progression_cards["Obtain Raviel, Lord of Phantasms"], player),
        "Obtain Uria, Lord of Searing Flames":
            lambda state: state.has_all(world.progression_cards["Obtain Uria, Lord of Searing Flames"], player),
        "Obtain Gate Guardian and its pieces":
            lambda state: state.has("Gate Guardian and its pieces", player),
        "Obtain Dark Scorpion Combination and its required cards":
            lambda state: state.has("Dark Scorpion Combination and its required cards", player),
        # Collection Events
        "Ojama Delta Hurricane and required cards":
            lambda state: state.has_all(world.progression_cards["Ojama Delta Hurricane and required cards"], player),
        "Huge Revolution and its required cards":
            lambda state: state.has_all(world.progression_cards["Huge Revolution and its required cards"], player),
        "Perfectly Ultimate Great Moth and its required cards":
            lambda state: state.has_all(world.progression_cards["Perfectly Ultimate Great Moth and its required cards"],
                                        player),
        "Valkyrion the Magna Warrior and its pieces":
            lambda state: state.has_all(world.progression_cards["Valkyrion the Magna Warrior and its pieces"], player),
        "Dark Sage and its required cards":
            lambda state: state.has_all(world.progression_cards["Dark Sage and its required cards"], player),
        "Destiny Board and its letters":
            lambda state: state.has_all(world.progression_cards["Destiny Board and its letters"], player),
        "XYZ-Dragon Cannon fusions and their materials":
            lambda state: state.has_all(world.progression_cards["XYZ-Dragon Cannon fusions and their materials"],
                                        player),
        "VWXYZ-Dragon Catapult Cannon and the fusion materials":
            lambda state: state.has_all(
                world.progression_cards["VWXYZ-Dragon Catapult Cannon and the fusion materials"], player),
        "Gate Guardian and its pieces":
            lambda state: state.has_all(world.progression_cards["Gate Guardian and its pieces"], player),
        "Dark Scorpion Combination and its required cards":
            lambda state: state.has_all(world.progression_cards["Dark Scorpion Combination and its required cards"],
                                        player),
        # Events
        "Exodia": lambda state: state.has_all(world.progression_cards["Exodia"], player),
        "Can Exodia Win":
            lambda state: state.has("Exodia", player) and state.has_all(world.progression_cards["Can Exodia Win"],
                                                                        player),
        "Can Last Turn Win":
            lambda state: state.has_all(world.progression_cards["Can Last Turn Win"], player),
        "Can Yata Lock":
            lambda state: state.has_all(world.progression_cards["Can Yata Lock"], player) and state.has_any(["No Banlist", "Banlist September 2003"], player),
        "Can Stall with Monsters":
            lambda state: state.has_all(world.progression_cards["Can Stall with Monsters"], player),
        "Can Stall with ST":
            lambda state: state.has_all(world.progression_cards["Can Stall with ST"], player),
        "Can Gain LP Every Turn": lambda state: state.has_all(world.progression_cards["Can Gain LP Every Turn"],
                                                              player),
        "Can Self Mill": lambda state: state.has_all(world.progression_cards["Can Self Mill"], player),
        "Has Back-row removal":
            lambda state: state.has_all(world.progression_cards["Backrow Removal"], player),

    }
    access_rules = {
        # Limited
        "LD01 All except Level 4 forbidden":
            lambda state: state.has_all(world.progression_cards["LD01 All except Level 4 forbidden"], player),
        "LD02 Medium/high Level forbidden":
            lambda state: state.has_all(world.progression_cards["LD02 Medium/high Level forbidden"], player),
        "LD03 ATK 1500 or more forbidden":
            lambda state: state.has_all(world.progression_cards["LD03 ATK 1500 or more forbidden"], player),
        "LD04 Flip Effects forbidden":
            lambda state: True,
        "LD05 Tributes forbidden":
            lambda state: True,
        "LD06 Traps forbidden":
            lambda state: state.has_all(world.progression_cards["No Trap Cards Bonus"], player),
        "LD07 Large Deck A":
            lambda state: yugioh06_difficulty(world, state, player, 2),
        "LD08 Large Deck B":
            lambda state: yugioh06_difficulty(world, state, player, 2),
        "LD09 Sets Forbidden":
            lambda state: True,
        "LD10 All except LV monsters forbidden":
            lambda state: state.has_all(world.progression_cards["LD10 All except LV monsters forbidden"], player),
        "LD11 All except Fairies forbidden":
            lambda state: state.has_all(world.progression_cards["LD11 All except Fairies forbidden"], player),
        "LD12 All except Wind forbidden":
            lambda state: state.has_all(world.progression_cards["LD12 All except Wind forbidden"], player),
        "LD13 All except monsters forbidden":
            lambda state: yugioh06_difficulty(world, state, player, 2),
        "LD14 Level 3 or below forbidden":
            lambda state: state.has_all(world.progression_cards["LD14 Level 3 or below forbidden"], player),
        "LD15 DEF 1500 or less forbidden":
            lambda state: state.has_all(world.progression_cards["LD15 DEF 1500 or less forbidden"], player),
        "LD16 Effect Monsters forbidden":
            lambda state: state.has_all(world.progression_cards["LD16 Effect Monsters forbidden"], player),
        "LD17 Spells forbidden":
            lambda state: state.has_all(world.progression_cards["No Spell Cards Bonus"], player),
        "LD18 Attacks forbidden":
            lambda state: state.has_all(world.progression_cards["LD18 Attacks forbidden"], player),
        "LD19 All except E-Hero's forbidden":
            lambda state: state.has_all(world.progression_cards["LD19 All except E-Hero's forbidden"], player),
        "LD20 All except Warriors forbidden":
            lambda state: state.has_all(world.progression_cards["LD20 All except Warriors forbidden"], player),
        "LD21 All except Dark forbidden":
            lambda state: state.has_all(world.progression_cards["LD21 All except Dark forbidden"], player),
        "LD22 All limited cards forbidden":
            lambda state: yugioh06_difficulty(world, state, player, 2),
        "LD23 Refer to Mar 05 Banlist":
            lambda state: yugioh06_difficulty(world, state, player, 3),
        "LD24 Refer to Sept 04 Banlist":
            lambda state: yugioh06_difficulty(world, state, player, 3),
        "LD25 Low Life Points":
            lambda state: yugioh06_difficulty(world, state, player, 2),
        "LD26 All except Toons forbidden":
            lambda state: state.has_all(world.progression_cards["LD26 All except Toons forbidden"], player),
        "LD27 All except Spirits forbidden":
            lambda state: state.has_all(world.progression_cards["LD27 All except Spirits forbidden"], player),
        "LD28 All except Dragons forbidden":
            lambda state: state.has_all(world.progression_cards["LD28 All except Dragons forbidden"], player),
        "LD29 All except Spellcasters forbidden":
            lambda state: state.has_all(world.progression_cards["LD29 All except Spellcasters forbidden"], player),
        "LD30 All except Light forbidden":
            lambda state: state.has_all(world.progression_cards["LD30 All except Light forbidden"], player),
        "LD31 All except Fire forbidden":
            lambda state: state.has_all(world.progression_cards["LD31 All except Fire forbidden"], player),
        "LD32 Decks with multiples forbidden":
            lambda state: yugioh06_difficulty(world, state, player, 2),
        "LD33 Special Summons forbidden":
            lambda state: yugioh06_difficulty(world, state, player, 1),
        "LD34 Normal Summons forbidden":
            lambda state: state.has_all(world.progression_cards["LD34 Normal Summons forbidden"], player),
        "LD35 All except Zombies forbidden":
            lambda state: state.has_all(world.progression_cards["LD35 All except Zombies forbidden"], player),
        "LD36 All except Earth forbidden":
            lambda state: state.has_all(world.progression_cards["LD36 All except Earth forbidden"], player),
        "LD37 All except Water forbidden":
            lambda state: state.has_all(world.progression_cards["LD37 All except Water forbidden"], player),
        "LD38 Refer to Mar 04 Banlist":
            lambda state: yugioh06_difficulty(world, state, player, 2),
        "LD39 Monsters forbidden":
            lambda state: state.has_all(world.progression_cards["LD39 Monsters forbidden"], player),
        "LD40 Refer to Sept 05 Banlist":
            lambda state: yugioh06_difficulty(world, state, player, 3),
        "LD41 Refer to Sept 03 Banlist":
            lambda state: yugioh06_difficulty(world, state, player, 3),
        # Theme Duels
        "TD01 Battle Damage":
            lambda state: True,
        "TD02 Deflected Damage":
            lambda state: state.has_all(world.progression_cards["TD02 Deflected Damage"], player),
        "TD03 Normal Summon":
            lambda state: yugioh06_difficulty(world, state, player, 2),
        "TD04 Ritual Summon":
            lambda state: state.has_all(world.progression_cards["TD04 Ritual Summon"], player),
        "TD05 Special Summon A":
            lambda state: state.has_all(world.progression_cards["TD05 Special Summon A"], player),
        "TD06 20x Spell":
            lambda state: state.has_all(world.progression_cards["TD06 20x Spell"], player),
        "TD07 10x Trap":
            lambda state: state.has_all(world.progression_cards["TD07 10x Trap"], player),
        "TD08 Draw":
            lambda state: state.has_all(world.progression_cards["TD08 Draw"], player),
        "TD09 Hand Destruction":
            lambda state: state.has_all(world.progression_cards["TD09 Hand Destruction"], player),
        "TD10 During Opponent's Turn":
            lambda state: state.has_all(world.progression_cards["TD10 During Opponent's Turn"], player),
        "TD11 Recover":
            lambda state: state.has_all(world.progression_cards["Can Gain LP Every Turn"], player),
        "TD12 Remove Monsters by Effect":
            lambda state: state.has_all(world.progression_cards["TD12 Remove Monsters by Effect"], player),
        "TD13 Flip Summon":
            lambda state: state.has_all(world.progression_cards["TD13 Flip Summon"], player),
        "TD14 Special Summon B":
            lambda state: state.has_all(world.progression_cards["TD14 Special Summon B"], player),
        "TD15 Token":
            lambda state: state.has_all(world.progression_cards["TD15 Token"], player),
        "TD16 Union":
            lambda state: state.has_all(world.progression_cards["TD16 Union"], player),
        "TD17 10x Quick Spell":
            lambda state: state.has_all(world.progression_cards["TD17 10x Quick Spell"], player),
        "TD18 The Forbidden":
            lambda state: state.has("Can Exodia Win", player),
        "TD19 20 Turns":
            lambda state: state.has_all(world.progression_cards["Final Countdown Finish Bonus"], player) and state.has(
                "Can Stall with ST", player),
        "TD20 Deck Destruction":
            lambda state: state.has_all(world.progression_cards["TD20 Deck Destruction"], player),
        "TD21 Victory D.":
            lambda state: state.has_all(world.progression_cards["TD21 Victory D."], player),
        "TD22 The Preventers Fight Back":
            lambda state: state.has("Ojama Delta Hurricane and required cards", player) and
                          state.has_all(world.progression_cards["TD22 The Preventers Fight Back"], player),
        "TD23 Huge Revolution":
            lambda state: state.has("Huge Revolution and its required cards", player) and
                          state.has_all(world.progression_cards["TD23 Huge Revolution"], player),
        "TD24 Victory in 5 Turns":
            lambda state: state.has_all(world.progression_cards["TD24 Victory in 5 Turns"], player) and
                          yugioh06_difficulty(world, state, player, 2),
        "TD25 Moth Grows Up":
            lambda state: state.has("Perfectly Ultimate Great Moth and its required cards", player) and
                          state.has_all(world.progression_cards["TD25 Moth Grows Up"], player),
        "TD26 Magnetic Power":
            lambda state: state.has("Valkyrion the Magna Warrior and its pieces", player),
        "TD27 Dark Sage":
            lambda state: state.has("Dark Sage and its required cards", player) and
                          state.has_all(world.progression_cards["TD27 Dark Sage"], player),
        "TD28 Direct Damage":
            lambda state: yugioh06_difficulty(world, state, player, 2),
        "TD29 Destroy Monsters in Battle":
            lambda state: True,
        "TD30 Tribute Summon":
            lambda state: state.has_all(world.progression_cards["TD30 Tribute Summon"], player),
        "TD31 Special Summon C":
            lambda state: state.has_all(world.progression_cards["TD31 Special Summon C"], player),
        "TD32 Toon":
            lambda state: state.has_all(world.progression_cards["TD32 Toon"], player),
        "TD33 10x Counter":
            lambda state: state.has_all(world.progression_cards["TD33 10x Counter"], player),
        "TD34 Destiny Board":
            lambda state: state.has("Destiny Board and its letters", player)
                          and state.has("Can Stall with Monsters", player)
                          and state.has_all(world.progression_cards["TD34 Destiny Board"], player),
        "TD35 Huge Damage in a Turn":
            lambda state: state.has_all(world.progression_cards["TD35 Huge Damage in a Turn"], player),
        "TD36 V-Z In the House":
            lambda state: state.has("VWXYZ-Dragon Catapult Cannon and the fusion materials", player),
        "TD37 Uria, Lord of Searing Flames":
            lambda state: state.has_all(world.progression_cards["TD37 Uria, Lord of Searing Flames"], player),
        "TD38 Hamon, Lord of Striking Thunder":
            lambda state: state.has_all(world.progression_cards["TD38 Hamon, Lord of Striking Thunder"], player),
        "TD39 Raviel, Lord of Phantasms":
            lambda state: state.has_all(world.progression_cards["TD39 Raviel, Lord of Phantasms"], player),
        "TD40 Make a Chain":
            lambda state: state.has_all(world.progression_cards["TD40 Make a Chain"], player),
        "TD41 The Gatekeeper Stands Tall":
            lambda state: state.has("Gate Guardian and its pieces", player) and
                          state.has_all(world.progression_cards["TD41 The Gatekeeper Stands Tall"], player),
        "TD42 Serious Damage":
            lambda state: yugioh06_difficulty(world, state, player, 3),
        "TD43 Return Monsters with Effects":
            lambda state: state.has_all(world.progression_cards["TD43 Return Monsters with Effects"], player),
        "TD44 Fusion Summon":
            lambda state: state.has_all(world.progression_cards["TD44 Fusion Summon"], player),
        "TD45 Big Damage at once":
            lambda state: state.has_all(world.progression_cards["TD45 Big Damage at once"], player),
        "TD46 XYZ In the House":
            lambda state: state.has("XYZ-Dragon Cannon fusions and their materials", player) and
                          state.has_all(world.progression_cards["TD46 XYZ In the House"], player),
        "TD47 Spell Counter":
            lambda state: state.has_all(world.progression_cards["TD47 Spell Counter"], player),
        "TD48 Destroy Monsters with Effects":
            lambda state: state.has_all(world.progression_cards["TD48 Destroy Monsters with Effects"], player) and
                          state.has("Can Stall with ST", player),
        "TD49 Plunder":
            lambda state: state.has_all(world.progression_cards["TD49 Plunder"], player),
        "TD50 Dark Scorpion Combination":
            lambda state: state.has("Dark Scorpion Combination and its required cards", player) and
                          state.has_all(world.progression_cards["TD50 Dark Scorpion Combination"], player),
    }
    multiworld.completion_condition[player] = lambda state: state.has("Goal", player)

    for loc in multiworld.get_locations(player):
        if loc.name in location_rules:
            add_rule(loc, location_rules[loc.name])
        if loc.name in access_rules:
            add_rule(multiworld.get_entrance(loc.name, player), access_rules[loc.name])
