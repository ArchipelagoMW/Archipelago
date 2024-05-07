from typing import Dict, List, Set
from worlds.generic.Rules import set_rule, add_rule
from BaseClasses import CollectionState


def total_fervour(state: CollectionState, player: int) -> int:
    totalFervour: int = 60 + (20 * state.count("Fervour Upgrade", player)) + (10 * state.count("Bead of Blue Wax", player))

    return totalFervour


def aubade(state: CollectionState, player: int) -> bool:
    return state.has("Aubade of the Nameless Guardian", player) if total_fervour(state, player) >= 90 else False


def tirana(state: CollectionState, player: int) -> bool:
    return state.has("Tirana of the Celestial Bastion", player) if total_fervour(state, player) >= 90 else False


def pillar(state: CollectionState, player: int) -> bool:
    return state.has_any({"Debla of the Lights", "Taranto to my Sister", "Cloistered Ruby"}, player)


def charge_beam(state: CollectionState, player: int) -> bool:
    return state.has("Charged Skill", player, 3)


def can_air_stall(state: CollectionState, logic: int, player: int) -> bool:
    return state.has("Ranged Skill", player) if logic >= 1 else False


def can_dawn_jump(state: CollectionState, logic: int, player: int) -> bool:
    return state.has_all({"Brilliant Heart of Dawn", "Dash Ability"}, player) if logic >= 1 else False


def can_water_jump(state: CollectionState, player: int) -> bool:
    return state.has_any({"Nail Uprooted from Dirt", "Purified Hand of the Nun"}, player)


def can_break_holes(state: CollectionState, player: int) -> bool:
    return (
        state.has_any({"Charged Skill", "Dive Skill"}, player) 
        or (
            state.has("Lunge Skill", player, 3)
            and state.has("Dash Ability", player)
        )
        or state.has_group("prayer", player)
        or aubade(state, player)
        or tirana(state, player)
    )


def can_break_tirana(state: CollectionState, logic: int, player: int) -> bool:
    return tirana(state, player) if logic >= 2 else False


def can_dive_laser(state: CollectionState, logic: int, player: int) -> bool:
    return state.has("Dive Skill", player, 3) if logic >= 2 else False


def can_walk_on_root(state: CollectionState, player: int) -> bool:
    return state.has("Three Gnarled Tongues", player)


def can_climb_on_root(state: CollectionState, player: int) -> bool:
    return state.has_all({"Three Gnarled Tongues", "Wall Climb Ability"}, player)


def can_survive_poison(state: CollectionState, logic: int, player: int, number: int) -> bool:
    if number == 1:
        if logic >= 2:
            return True
        elif logic == 1:
            return state.has_any({"Silvered Lung of Dolphos", "Tiento to your Thorned Hairs"}, player)
        elif logic == 0:
            return state.has("Silvered Lung of Dolphos", player)
    elif number == 2:
        if logic >= 1:
            return state.has_any({"Silvered Lung of Dolphos", "Tiento to your Thorned Hairs"}, player)
        else:
            return state.has("Silvered Lung of Dolphos", player)
    elif number == 3:
        if logic >= 2 and total_fervour(state, player) >= 120:
            return state.has_any({"Silvered Lung of Dolphos", "Tiento to your Thorned Hairs"}, player)
        else:
            return state.has("Silvered Lung of Dolphos", player)


def can_enemy_bounce(logic: int, enemy: int) -> bool: # TODO
    return enemy_skips_allowed(logic, enemy)


def can_enemy_upslash(state: CollectionState, logic: int, enemy: int, player: int) -> bool:
    return state.has("Combo Skill", player, 2) and \
        enemy_skips_allowed(logic, enemy)


def can_cross_gap(state: CollectionState, logic: int, player: int, number: int) -> bool:
    if number == 1:
        return (
            state.has_any({"Purified Hand of the Nun", "The Young Mason's Wheel"}, player)
            or can_dawn_jump(state, logic, player)
            or can_air_stall(state, logic, player)
        )
    elif number == 2:
        return (
            state.has_any({"Purified Hand of the Nun", "The Young Mason's Wheel"}, player)
            or can_dawn_jump(state, logic, player)
        )
    elif number == 3:
        return (
            state.has("Purified Hand of the Nun", player)
            or can_dawn_jump(state, logic, player)
            or (
                state.has("The Young Mason's Wheel", player)
                and can_air_stall(state, logic, player)
            )
        )
    elif number == 4:
        return (
            state.has("Purified Hand of the Nun", player)
            or can_dawn_jump(state, logic, player)
        )
    elif number == 5:
        return (
            state.has("Purified Hand of the Nun", player)
            or (
                can_dawn_jump(state, logic, player)
                and can_air_stall(state, logic, player))
        )
    elif number == 6:
        return state.has("Purified Hand of the Nun", player)
    elif number == 7:
        return (
            state.has("Purified Hand of the Nun", player)
            and (
                can_dawn_jump(state, logic, player)
                or state.has("The Young Mason's Wheel", player)
                or can_air_stall(state, logic, player)
            )
        )
    elif number == 8:
        return (
            state.has("Purified Hand of the Nun", player)
            and (
                can_dawn_jump(state, logic, player)
                or state.has("The Young Mason's Wheel", player)
            )
        )
    elif number == 9:
        return (
            state.has("Purified Hand of the Nun", player)
            and (
                can_dawn_jump(state, logic, player)
                or state.has("The Young Mason's Wheel", player)
                and can_air_stall(state, logic, player)
            )
        )
    elif number == 10:
        return (
            state.has("Purified Hand of the Nun", player)
            and can_dawn_jump(state, logic, player)
        )
    elif number == 11:
        return (
            state.has("Purified Hand of the Nun", player)
            and can_dawn_jump(state, logic, player)
            and can_air_stall(state, logic, player)
        )


def can_ride_albero_elevator(state: CollectionState, player: int) -> bool:
    return state.has_any({"D02Z02S11[NW]", "D02Z02S11[NE]", "D02Z02S11[W]", "D02Z02S11[E]", \
                            "D02Z02S11[SE]"}, player)


def opened_dc_gate_w(state: CollectionState, player: int) -> bool:
    return state.has_any({"D01Z05S24[W]", "D01Z05S24[E]"}, player)


def opened_dc_gate_e(state: CollectionState, player: int) -> bool:
    return state.has_any({"D01Z05S12[W]", "D01Z05S12[E]"}, player)


def opened_dc_ladder(state: CollectionState, player: int) -> bool:
    return state.has_any({"D01Z05S20[W]", "D01Z05S20[N]"}, player)


def opened_wotw_cave(state: CollectionState, player: int) -> bool:
    return (
        state.has("D02Z01S06[E]", player)
        or state.has("Wall Climb Ability", player)
        and (
            state.has("D02Z01S06[W]", player)
            or state.has("D02Z01S06[Cherubs]", player)
        )
    )


def rode_gotp_elevator(state: CollectionState, player: int) -> bool:
    return state.has_any({"D02Z02S11[NW]", "D02Z02S11[NE]", "D02Z02S11[W]", "D02Z02S11[E]", \
                            "D02Z02S11[SE]"}, player)


def opened_convent_ladder(state: CollectionState, player: int) -> bool:
    return state.has_any({"D02Z03S11[S]", "D02Z03S11[W]", "D02Z03S11[NW]", "D02Z03S11[E]", \
                            "D02Z03S11[NE]"}, player)


def broke_jondo_bell_w(state: CollectionState, player: int) -> bool:
    return (
        state.has("D03Z02S09[S]", player)
        or state.has("D03Z02S09[W]", player)
        and state.has("Dash Ability", player)
        or state.has("D03Z02S09[N]", player)
        or state.has("D03Z02S09[Cherubs]", player)
    )


def broke_jondo_bell_e(state: CollectionState, logic: int, enemy: int, player: int) -> bool:
    return (
        state.has("D03Z02S05[S]", player)
        or state.has("D03Z02S05[E]", player)
        or state.has("D03Z02S05[W]", player)
        and (
            can_cross_gap(state, logic, player, 5)
            or can_enemy_bounce(logic, enemy)
            and can_cross_gap(state, logic, player, 3)
        )
    )


def opened_mom_ladder(state: CollectionState, player: int) -> bool:
    return state.has_any({"D04Z02S06[NW]", "D04Z02S06[NE]", "D04Z02S06[N]", "D04Z02S06[S]"}, player)


def opened_tsc_gate(state: CollectionState, player: int) -> bool:
    return state.has_any({"D05Z02S11[W]", "D05Z02S11[Cherubs]"}, player)


def opened_ar_ladder(state: CollectionState, player: int) -> bool:
    return state.has_any({"D06Z01S23[Sword]", "D06Z01S23[E]", "D06Z01S23[S]", "D06Z01S23[Cherubs]"}, player)


def broke_bottc_statue(state: CollectionState, player: int) -> bool:
    return state.has_any({"D08Z01S02[NE]", "D08Z01S02[SE]"}, player)


def opened_wothp_gate(state: CollectionState, player: int) -> bool:
    return state.has_any({"D09Z01S05[W]", "D09Z01S05[SE]", "D09Z01S05[NE]"}, player)


def opened_botss_ladder(state: CollectionState, player: int) -> bool:
    return state.has_any({"D17Z01S04[N]", "D17Z01S04[FrontR]"}, player)


def upwarp_skips_allowed(logic: int) -> bool:
    return logic >= 2


def mourning_skips_allowed(logic: int) -> bool:
    return logic >= 2


def enemy_skips_allowed(logic: int, enemy: int) -> bool:
    return logic >= 2 and enemy == 0


def obscure_skips_allowed(logic):
    return logic >= 2


def precise_skips_allowed(logic):
    return logic >= 2


def can_beat_boss(state: CollectionState, boss: str, logic: int, player: int) -> bool:
    def has_boss_strength(name: str) -> bool:
        silver: int = state.count("Quicksilver", player) if state.has("D01Z05S27[E]", player) else 0
        flasks: int = state.count("Empty Bile Flask", player) if \
            state.has_any({"D01Z05S18[E]", "D02Z02S09[E]", "D03Z02S14[E]", "D03Z03S03[SE]", "D04Z02S13[W]", \
                "D05Z01S12[E]", "D20Z01S08[W]"}, player) else 0
        

        playerStrength: float = state.count("Life Upgrade", player) * 0.25 / 6 + \
            state.count("Mea Culpa Upgrade", player) * 0.25 / 7 + state.count("Fervour Upgrade", player) * 0.20 \
                / 6 + flasks * 0.15 / 8 + silver * 0.15 / 5
        
        bosses: Dict[str, int] = {
            "warden": -0.10,
            "ten-piedad": 0.05,
            "charred-visage": 0.20,
            "tres-angustias": 0.15,
            "esdras": 0.25,
            "melquiades": 0.25,
            "exposito": 0.30,
            "quirce": 0.35,
            "crisanta": 0.50,
            "isidora": 0.70,
            "sierpes": 0.70,
            "amanecida": 0.60,
            "laudes": 0.60,
            "perpetua": -0.05,
            "legionary": 0.20
        }

        bossStrength: int = bosses[name]

        return playerStrength >= (bossStrength - 0.10 if logic >= 2 else (bossStrength if logic >= 1 else bossStrength + 0.10))
    
    if boss == "Brotherhood":
        return (
            has_boss_strength("warden")
            and state.has_any({"D17Z01S11[W]", "D17Z01S11[E]"}, player)
        )
    elif boss == "Mercy":
        return (
            has_boss_strength("ten-piedad")
            and state.has_any({"D01Z04S18[W]", "D01Z04S18[E]"}, player)
        )
    elif boss == "Convent":
        return (
            has_boss_strength("charred-visage")
            and state.has_any({"D02Z03S20[W]", "D02Z03S20[E]"}, player)
        )
    elif boss == "Grievance":
        return (
            has_boss_strength("tres-angustias")
            and state.has_any({"Wall Climb Ability", "Purified Hand of the Nun"}, player)
            and state.has_any({"D03Z03S15[W]", "D03Z03S15[E]"}, player)
        )
    elif boss == "Bridge":
        return (
            has_boss_strength("esdras")
            and state.has_any({"D08Z01S01[W]", "D08Z01S01[E]"}, player)
        )
    elif boss == "Mothers":
        return (
            has_boss_strength("melquiades")
            and state.has_any({"D04Z02S22[W]", "D04Z02S22[E]"}, player)
        )
    elif boss == "Canvases":
        return (
            has_boss_strength("exposito")
            and state.has_any({"D05Z02S14[W]", "D05Z02S14[E]"}, player)
        )
    elif boss == "Prison":
        return (
            has_boss_strength("quirce")
            and state.has_any({"D09Z01S03[W]", "D09Z01S03[N]"}, player)
        )
    elif boss == "Rooftops":
        return (
            has_boss_strength("crisanta")
            and state.has_any({"D06Z01S25[W]", "D06Z01S25[E]"}, player)
        )
    elif boss == "Ossuary":
        return (
            has_boss_strength("isidora")
            and state.has("D01BZ08S01[W]", player)
        )
    elif boss == "Mourning":
        return (
            has_boss_strength("sierpes")
            and state.has("D20Z02S08[E]", player)
        )
    elif boss == "Graveyard":
        return (
            has_boss_strength("amanecida")
            and state.has_all({"D01Z06S01[Santos]", "D02Z03S23[E]", "D02Z02S14[W]", "Wall Climb Ability"}, player)
        )
    elif boss == "Jondo":
        return (
            has_boss_strength("amanecida")
            and state.has("D01Z06S01[Santos]", player)
            and state.has_any({"D20Z01S05[W]", "D20Z01S05[E]"}, player)
            and state.has_any({"D03Z01S03[W]", "D03Z01S03[SW]"}, player)
        )
    elif boss == "Patio":
        return (
            has_boss_strength("amanecida")
            and state.has_all({"D01Z06S01[Santos]", "D06Z01S18[E]"}, player)
            and state.has_any({"D04Z01S04[W]", "D04Z01S04[E]", "D04Z01S04[Cherubs]"}, player)
        )
    elif boss == "Wall":
        return (
            has_boss_strength("amanecida")
            and state.has_all({"D01Z06S01[Santos]", "D09BZ01S01[Cell24]"}, player)
            and state.has_any({"D09Z01S01[W]", "D09Z01S01[E]"}, player)
        )
    elif boss == "Hall":
        return (
            has_boss_strength("laudes")
            and state.has_any({"D08Z03S03[W]", "D08Z03S03[E]"}, player)
        )
    elif boss == "Perpetua":
        return has_boss_strength("perpetua")
    elif boss == "Legionary":
        return has_boss_strength("legionary")


def guilt_rooms(state: CollectionState, player: int, number: int) -> bool:
    doors: List[str] = [
        "D01Z04S17[W]",
        "D02Z02S06[E]",
        "D03Z03S14[W]",
        "D04Z02S17[W]",
        "D05Z01S17[W]",
        "D09Z01S13[E]",
        "D17Z01S12[E]"
    ]

    total: int = sum(state.has(item, player) for item in doors)

    return total >= number


def sword_rooms(state: CollectionState, player: int, number: int) -> bool:
    doors: List[Set[str]] = [
        {"D01Z02S06[W]", "D01Z02S06[E]"},
        {"D01Z05S24[W]", "D01Z05S24[E]"},
        {"D02Z03S13[W]"},
        {"D04Z02S12[W]"},
        {"D05Z01S13[E]"},
        {"D06Z01S11[W]"},
        {"D17Z01S08[E]"}
    ]

    total: int = sum(state.has_any(items, player) for items in doors)

    return total >= number


def redento(state: CollectionState, world, player: int, number: int) -> bool:
    if number == 1:
        return state.has_any({"D03Z01S03[W]", "D03Z01S03[SW]"}, player)
    elif number == 2:
        return (
            state.has_any({"D03Z01S03[W]", "D03Z01S03[SW]"}, player)
            and state.has("OpenedBOTSSLadder", player)
        )
    elif number == 3:
        return (
            state.has_any({"D03Z01S03[W]", "D03Z01S03[SW]"}, player)
            and state.has("OpenedBOTSSLadder", player)
            and state.can_reach(world.multiworld.get_region("D01Z03S06", player))
        )
    elif number == 4:
        return (
            state.has_any({"D03Z01S03[W]", "D03Z01S03[SW]"}, player)
            and state.has("OpenedBOTSSLadder", player)
            and state.can_reach(world.multiworld.get_region("D01Z03S06", player))
            and state.can_reach(world.multiworld.get_region("D04Z01S04", player))
        )
    elif number == 5:
        return (
            state.has_any({"D03Z01S03[W]", "D03Z01S03[SW]"}, player)
            and state.has("OpenedBOTSSLadder", player)
            and state.can_reach(world.multiworld.get_region("D01Z03S06", player))
            and state.can_reach(world.multiworld.get_region("D04Z01S04", player))
            and state.can_reach(world.multiworld.get_region("D04Z02S20", player))
            and state.has_all({"Little Toe made of Limestone", "Big Toe made of Limestone", \
                                "Fourth Toe made of Limestone", "D17Z01S09[E]"}, player)
            and state.has("Knot of Rosary Rope", player)
        )


def miriam(state: CollectionState, player: int) -> bool:
    return state.has_all({"D02Z03S24[E]", "D03Z03S19[E]", "D04Z04S02[W]", "D05Z01S24[E]", "D06Z01S26[W]"}, player)


def amanecida_rooms(state: CollectionState, logic: int, player: int, number: int) -> bool:
    bosses: List[str] = [
        "Graveyard",
        "Jondo",
        "Patio",
        "Wall"
    ]

    total = sum(can_beat_boss(state, boss, logic, player) for boss in bosses)

    return total >= number


def chalice_rooms(state: CollectionState, player: int, number: int) -> bool:
    doors: List[Set[str]] = [
        {"D03Z01S01[W]", "D03Z01S01[NE]", "D03Z01S01[S]"},
        {"D05Z02S01[W]", "D05Z02S01[E]"},
        {"D09Z01S07[SW]", "D09Z01S07[SE]", "D09Z01S07[W]", "D09Z01S07[E]"}
    ]

    total: int = sum(state.has_any(items, player) for items in doors)

    return total >= number


def rules(blasphemousworld):
    world = blasphemousworld.multiworld
    player = blasphemousworld.player
    logic = world.difficulty[player].value
    enemy = world.enemy_randomizer[player].value


    # D01Z01S01 (The Holy Line)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z01S01[S]", player),
        lambda state: (
            can_break_holes(state, player)
            or state.has("Purified Hand of the Nun", player)
        ))


    # D01Z01S02 (The Holy Line)
    # Items
    set_rule(world.get_location("THL: Across blood platforms", player),
        lambda state: (
            state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun"}, player)
        ))
    # No doors


    # D01Z01S03 (The Holy Line)
    # Items
    set_rule(world.get_location("THL: Underground chest", player),
        lambda state: (
            state.has_all({"Blood Perpetuated in Sand", "Dash Ability"}, player)
            and can_water_jump(state, player)
        ))
    # No doors


    # D01Z02S01 (Albero)
    # Items
    set_rule(world.get_location("Albero: Bless Linen Cloth", player),
        lambda state: state.has("Linen Cloth", player))
    set_rule(world.get_location("Albero: Bless Hatched Egg", player),
        lambda state: state.has("Hatched Egg of Deformity", player))
    set_rule(world.get_location("Albero: Bless Severed Hand", player),
        lambda state: state.has("Severed Hand", player))
    # No doors


    # D01Z02S02 (Albero)
    # Items
    set_rule(world.get_location("Albero: Tirso's 1st reward", player),
        lambda state: state.has_group("tirso", player, 1))
    set_rule(world.get_location("Albero: Tirso's 2nd reward", player),
        lambda state: state.has_group("tirso", player, 2))
    set_rule(world.get_location("Albero: Tirso's 3rd reward", player),
        lambda state: state.has_group("tirso", player, 3))
    set_rule(world.get_location("Albero: Tirso's 4th reward", player),
        lambda state: state.has_group("tirso", player, 4))
    set_rule(world.get_location("Albero: Tirso's 5th reward", player),
        lambda state: state.has_group("tirso", player, 5))
    set_rule(world.get_location("Albero: Tirso's 6th reward", player),
        lambda state: state.has_group("tirso", player, 6))
    set_rule(world.get_location("Albero: Tirso's final reward", player),
        lambda state: (
            state.has_group("tirso", player, 6)
            and can_beat_boss(state, "Mercy", logic, player)
            and can_beat_boss(state, "Convent", logic, player)
            and can_beat_boss(state, "Grievance", logic, player)
            and can_beat_boss(state, "Mothers", logic, player)
            and can_beat_boss(state, "Canvases", logic, player)
            and can_beat_boss(state, "Prison", logic, player)
        ))
    # No doors


    # D01Z02S03 (Albero)
    # Items
    set_rule(world.get_location("Albero: Child of Moonlight", player),
        lambda state: (
            state.has("RodeGOTPElevator", player)
            or pillar(state, player)
            or state.has("Cante Jondo of the Three Sisters", player)
            or state.has("Purified Hand of the Nun", player)
            or state.has("D01Z02S03[NW]", player) 
            and (
                can_cross_gap(state, logic, player, 2)
                or state.has("Lorquiana", player)
                or aubade(state, player)
                or state.has("Cantina of the Blue Rose", player)
                or charge_beam(state, player)
                or state.has("Ranged Skill", player)
            )
        ))
    set_rule(world.get_location("Albero: Lvdovico's 1st reward", player),
        lambda state: state.has_group("tentudia", player, 1))
    set_rule(world.get_location("Albero: Lvdovico's 2nd reward", player),
        lambda state: state.has_group("tentudia", player, 2))
    set_rule(world.get_location("Albero: Lvdovico's 3rd reward", player),
        lambda state: state.has_group("tentudia", player, 3))
    set_rule(world.get_location("Albero: First gift for Cleofas", player),
        lambda state: state.has("D04Z02S10[W]", player))
    # Doors
    set_rule(world.get_entrance("D01Z02S03[NW]", player),
        lambda state: (
            state.has("D02Z02S11[NW]", player)
            or state.has("D02Z02S11[NE]", player)
            or state.has("D02Z02S11[W]", player)
            or state.has("D02Z02S11[E]", player)
            or state.has("D02Z02S11[SE]", player)
        ))
    set_rule(world.get_entrance("D01Z02S03[church]", player),
        lambda state: (
            can_beat_boss(state, "Mercy", logic, player)
            or can_beat_boss(state, "Convent", logic, player)
            or can_beat_boss(state, "Grievance", logic, player)
        ))


    # D01BZ04S01 (Albero: Inside church)
    # Items
    set_rule(world.get_location("Albero: Final gift for Cleofas", player),
        lambda state: (
            state.has_group("marks", player, 3)
            and state.has("Cord of the True Burying", player)
            and state.has("D04Z02S10[W]", player)
            and state.has("D06Z01S18[E]", player)
        ))
    # No doors


    # D01BZ06S01 (Ossuary)
    # Items
    set_rule(world.get_location("Ossuary: 1st reward", player),
        lambda state: state.has_group("bones", player, 4))
    set_rule(world.get_location("Ossuary: 2nd reward", player),
        lambda state: state.has_group("bones", player, 8))
    set_rule(world.get_location("Ossuary: 3rd reward", player),
        lambda state: state.has_group("bones", player, 12))
    set_rule(world.get_location("Ossuary: 4th reward", player),
        lambda state: state.has_group("bones", player, 16))
    set_rule(world.get_location("Ossuary: 5th reward", player),
        lambda state: state.has_group("bones", player, 20))
    set_rule(world.get_location("Ossuary: 6th reward", player),
        lambda state: state.has_group("bones", player, 24))
    set_rule(world.get_location("Ossuary: 7th reward", player),
        lambda state: state.has_group("bones", player, 28))
    set_rule(world.get_location("Ossuary: 8th reward", player),
        lambda state: state.has_group("bones", player, 32))
    set_rule(world.get_location("Ossuary: 9th reward", player),
        lambda state: state.has_group("bones", player, 36))
    set_rule(world.get_location("Ossuary: 10th reward", player),
        lambda state: state.has_group("bones", player, 40))
    set_rule(world.get_location("Ossuary: 11th reward", player),
        lambda state: state.has_group("bones", player, 44))
    # Doors
    set_rule(world.get_entrance("D01BZ06S01[E]", player),
        lambda state: state.has_group("bones", player, 30))


    # D01BZ08S01 (Isidora)
    # Items
    set_rule(world.get_location("Ossuary: Isidora, Voice of the Dead", player),
        lambda state: can_beat_boss(state, "Ossuary", logic, player))
    # No doors


    # D01Z03S01 (Wasteland of the Buried Churches)
    # Items
    set_rule(world.get_location("WotBC: Lower log path", player),
        lambda state: state.has("D01Z03S01[SE]", player))
    # No doors


    # D01Z03S02 (Wasteland of the Buried Churches)
    # Items
    set_rule(world.get_location("WotBC: Hidden alcove", player),
        lambda state: state.has("Dash Ability", player))
    # No doors


    # D01Z03S03 (Wasteland of the Buried Churches)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z03S03[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D01Z03S05 (Wasteland of the Buried Churches)
    # Items
    set_rule(world.get_location("WotBC: Under broken bridge", player),
        lambda state: (
            state.has_any({"Blood Perpetuated in Sand", "Boots of Pleading"}, player)
            or can_cross_gap(state, logic, player, 3)
        ))
    # Doors
    set_rule(world.get_entrance("D01Z03S05[Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D01Z03S06 (Wasteland of the Buried Churches)
    # Items
    set_rule(world.get_location("WotBC: 3rd meeting with Redento", player),
        lambda state: redento(state, blasphemousworld, player, 3))
    # No doors


    # D01Z03S07 (Wasteland of the Buried Churches)
    # Items
    set_rule(world.get_location("WotBC: Cliffside Child of Moonlight", player),
        lambda state: (
            can_cross_gap(state, logic, player, 2)
            or aubade(state, player)
            or charge_beam(state, player)
            or state.has_any({"Lorquiana", "Cante Jondo of the Three Sisters", "Cantina of the Blue Rose", \
                              "Cloistered Ruby", "Ranged Skill"}, player)
            or precise_skips_allowed(logic)
        ))
    # Doors
    set_rule(world.get_entrance("D01Z03S07[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))

    
    # D01Z04S01 (Mercy Dreams)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z04S01[SE]", player),
        lambda state: state.has("D01Z04S01[S]", player))
    set_rule(world.get_entrance("D01Z04S01[S]", player),
        lambda state: state.has("D01Z04S01[SE]", player))


    # D01Z04S09 (Mercy Dreams)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z04S09[W]", player),
        lambda state: state.has("OpenedDCGateE", player))


    # D01Z04S13 (Mercy Dreams)
    # Items
    set_rule(world.get_location("MD: Behind gate to TSC", player),
        lambda state: (
            state.has("D01Z04S13[SE]", player)
            or can_dive_laser(state, logic, player) and (
                can_air_stall(state, logic, player)
                or state.has_any({"The Young Mason's Wheel", "Purified Hand of the Nun"}, player)
                or can_enemy_bounce(logic, enemy)
                )
        ))
    # Doors
    set_rule(world.get_entrance("D01Z04S13[SE]", player),
        lambda state: (
            can_dive_laser(state, logic, player) and (
                can_air_stall(state, logic, player)
                or state.has_any({"The Young Mason's Wheel", "Purified Hand of the Nun"}, player)
                or can_enemy_bounce(logic, enemy)
                )
        ))


    # D01Z04S14 (Mercy Dreams)
    # Items
    set_rule(world.get_location("MD: Sliding challenge", player),
        lambda state: state.has("Dash Ability", player))
    # No doors


    # D01Z04S15 (Mercy Dreams)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z04S15[W]", player),
        lambda state: (
            state.has("D01Z04S15[E]", player)
            or state.has("D01Z04S15[SW]", player)
            or state.has("D01Z04S15[SE]", player)
        ))
    set_rule(world.get_entrance("D01Z04S15[E]", player),
        lambda state: (
            state.has("D01Z04S15[W]", player)
            or state.has("D01Z04S15[SW]", player)
            or state.has("D01Z04S15[SE]", player)
        ))
    set_rule(world.get_entrance("D01Z04S15[SW]", player),
        lambda state: (
            state.has("D01Z04S15[W]", player)
            or state.has("D01Z04S15[E]", player)
            or state.has("D01Z04S15[SE]", player)
        ))
    set_rule(world.get_entrance("D01Z04S15[SE]", player),
        lambda state: (
            state.has("D01Z04S15[W]", player)
            or state.has("D01Z04S15[E]", player)
            or state.has("D01Z04S15[SW]", player)
        ))


    # D01Z04S16 (Mercy Dreams)
    # Items
    set_rule(world.get_location("MD: Cave Child of Moonlight", player),
        lambda state: (
            state.has_any({"Purified Hand of the Nun", "Cante Jondo of the Three Sisters"}, player)
            or pillar(state, player)
            or tirana(state, player)
        ))
    # No doors


    # D01Z04S18 (Ten Piedad)
    # Items
    set_rule(world.get_location("MD: Ten Piedad", player),
        lambda state: can_beat_boss(state, "Mercy", logic, player))
    # Doors
    set_rule(world.get_entrance("D01Z04S18[W]", player),
        lambda state: can_beat_boss(state, "Mercy", logic, player))
    set_rule(world.get_entrance("D01Z04S18[E]", player),
        lambda state: can_beat_boss(state, "Mercy", logic, player))


    # D01Z05S02 (Desecrated Cistern)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z05S02[S]", player),
        lambda state: state.has("OpenedDCLadder", player))


    # D01Z05S05 (Desecrated Cistern)
    # Items
    set_rule(world.get_location("DC: Hidden alcove near fountain", player),
        lambda state: (
            state.has("Dash Ability", player)
            and can_water_jump(state, player)
        ))
    # No doors


    # D01Z05S06 (Desecrated Cistern)
    # Items
    set_rule(world.get_location("DC: Upper east tunnel chest", player),
        lambda state: (
            state.has("D01Z05S06[Cherubs]", player)
            or can_water_jump(state, player)
        ))
    set_rule(world.get_location("DC: Upper east Child of Moonlight", player),
        lambda state: (
            state.has("D01Z05S06[Cherubs]", player)
            or can_water_jump(state, player)
            or pillar(state, player)
            or state.has("Cante Jondo of the Three Sisters", player)
            or aubade(state, player)
            or tirana(state, player)
            or can_air_stall(state, logic, player)
        ))
    # No doors


    # D01Z05S12 (Desecrated Cistern)
    # Event
    set_rule(world.get_location("OpenedDCGateE", player),
        lambda state: opened_dc_gate_e(state, player))


    # D01Z05S13 (Desecrated Cistern)
    # Items
    set_rule(world.get_location("DC: Child of Moonlight, behind pillar", player),
        lambda state: (
            state.has("D01Z05S13[SW]", player)
            or state.has("D01Z05S13[E]", player)
            and can_survive_poison(state, logic, player, 3)
            and can_water_jump(state, player)
        ))
    # Doors
    set_rule(world.get_entrance("D01Z05S13[SW]", player),
        lambda state: state.has("D01Z05S13[E]", player))
    add_rule(world.get_entrance("D01Z05S13[SW]", player),
        lambda state: (
            can_survive_poison(state, logic, player, 3)
            and can_water_jump(state, player)
        ))
    set_rule(world.get_entrance("D01Z05S13[N]", player),
        lambda state: state.has("D01Z05S13[E]", player))
    add_rule(world.get_entrance("D01Z05S13[N]", player),
        lambda state: (
            can_survive_poison(state, logic, player, 3)
            and can_water_jump(state, player)
        ))


    # D01Z05S17 (Desecrated Cistern)
    # Items
    set_rule(world.get_location("DC: High ledge near elevator shaft", player),
        lambda state: (
            state.has("D01Z05S17[E]", player)
            or can_water_jump(state, player)
            or can_cross_gap(state, logic, player, 5)
        ))
    # Doors
    set_rule(world.get_entrance("D01Z05S17[E]", player),
        lambda state: (
            state.has("Dash Ability", player) and (
                can_water_jump(state, player)
                or can_cross_gap(state, logic, player, 5)
            )
        ))
    

    # D01Z05S20 (Desecrated Cistern)
    # Event
    set_rule(world.get_location("OpenedDCLadder", player),
        lambda state: opened_dc_ladder(state, player))


    # D01Z05S21 (Desecrated Cistern)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z05S21[Reward]", player),
        lambda state: state.has("Shroud of Dreamt Sins", player))


    # D01Z05S23 (Desecrated Cistern)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z05S23[W]", player),
        lambda state: (
            chalice_rooms(state, player, 3)
            and state.has("Chalice of Inverted Verses", player)
        ))
    

    # D01Z05S24 (Desecrated Cistern)
    # Event
    set_rule(world.get_location("OpenedDCGateW", player),
        lambda state: opened_dc_gate_w(state, player))


    # D01Z05S25 (Desecrated Cistern)
    # Items
    set_rule(world.get_location("DC: Elevator shaft ledge", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            or (
                state.has("Purified Hand of the Nun", player)
                and state.has_any({"D01Z05S25[SW]", "D01Z05S25[SE]", "D01Z05S25[NE]"}, player)
            )
        ))
    set_rule(world.get_location("DC: Elevator shaft Child of Moonlight", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            or (
                obscure_skips_allowed(logic)
                and state.has_any({"D01Z05S25[SW]", "D01Z05S25[SE]", "D01Z05S25[NE]"}, player)
                and (
                    aubade(state, player)
                    or state.has("Cantina of the Blue Rose", player)
                )
            )
            or (
                pillar(state, player)
                and (
                    state.has("D01Z05S25[E]", player)
                    or state.has("D01Z05S25[W]", player)
                    and (
                        can_walk_on_root(state, player)
                        or can_cross_gap(state, logic, player, 3)
                    )
                )
            )
        ))
    # Doors
    set_rule(world.get_entrance("D01Z05S25[NE]", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            or state.has("D01Z05S25[SW]", player)
            or state.has("D01Z05S25[SE]", player)
        ))
    set_rule(world.get_entrance("D01Z05S25[W]", player),
        lambda state: (
            (
                state.has("Linen of Golden Thread", player)
                and (
                    can_walk_on_root(state, player)
                    or state.has("Purified Hand of the Nun", player)
                    or can_air_stall(state, logic, player)
                )
            )
            or (
                state.has("D01Z05S25[E]", player)
                and (
                    can_walk_on_root(state, player)
                    or can_cross_gap(state, logic, player, 3)
                )
            )
        ))
    set_rule(world.get_entrance("D01Z05S25[E]", player),
        lambda state: (
            can_break_tirana(state, logic, player)
            and (
                state.has("Linen of Golden Thread", player)
                or state.has("D01Z05S25[W]", player)
                and (
                    can_walk_on_root(state, player)
                    or can_cross_gap(state, logic, player, 3)
                )
            )
        ))
    set_rule(world.get_entrance("D01Z05S25[SW]", player),
        lambda state: (
            state.has("D01Z05S25[SE]", player)
            or state.has("D01Z05S25[NE]", player)
            or state.has("Linen of Golden Thread", player)
        ))
    set_rule(world.get_entrance("D01Z05S25[SE]", player),
        lambda state: (
            state.has("D01Z05S25[SW]", player)
            or state.has("D01Z05S25[NE]", player)
            or state.has("Linen of Golden Thread", player)
        ))
    set_rule(world.get_entrance("D01Z05S25[EchoesW]", player),
        lambda state: state.has("D01Z05S25[EchoesE]", player))
    add_rule(world.get_entrance("D01Z05S25[EchoesW]", player),
        lambda state: (
            state.has("D01Z05S25[EchoesE]", player)
            and (
                state.has("Blood Perpetuated in Sand", player)
                or can_cross_gap(state, logic, player, 8)
            )
            or state.has("Linen of Golden Thread", player)
            and (
                can_cross_gap(state, logic, player, 5)
                or can_air_stall(state, logic, player)
                and state.has("Blood Perpetuated in Sand", player)
            )
        ))
    set_rule(world.get_entrance("D01Z05S25[EchoesE]", player),
        lambda state: state.has("D01Z05S25[EchoesW]", player))
    add_rule(world.get_entrance("D01Z05S25[EchoesE]", player),
        lambda state: (
            state.has("D01Z05S25[EchoesW]", player)
            and (
                state.has("Blood Perpetuated in Sand", player)
                or can_cross_gap(state, logic, player, 8)
            )
            or state.has("Linen of Golden Thread", player)
            and (
                can_cross_gap(state, logic, player, 5)
                or can_air_stall(state, logic, player)
                and state.has("Blood Perpetuated in Sand", player)
            )
        ))


    # D01Z06S01 (Petrous)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z06S01[Santos]", player),
        lambda state: state.has("Petrified Bell", player))


    # D02Z01S01 (Where Olive Trees Wither)
    # Items
    set_rule(world.get_location("WOTW: Below Prie Dieu", player),
        lambda state: (
            state.has("D02Z01S01[W]", player)
            or state.has("D02Z01S01[CherubsL]", player)
            or state.has("D02Z01S01[SW]", player)
            or state.has("D02Z01S01[CherubsR]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))
    set_rule(world.get_location("WOTW: Gemino's gift", player),
        lambda state: (
            state.has("D02Z01S01[W]", player)
            or state.has("D02Z01S01[CherubsL]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
            or (
                (
                    state.has("D02Z01S01[SW]", player)
                    or state.has("D02Z01S01[CherubsR]", player)
                )
                and can_dawn_jump(state, logic, player)
            )
        ))
    set_rule(world.get_location("WOTW: Gemino's reward", player),
        lambda state: (
            state.has("Golden Thimble Filled with Burning Oil", player)
            and (
                state.has("D02Z01S01[W]", player)
                or state.has("D02Z01S01[CherubsL]", player)
                or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
                or (
                    (
                        state.has("D02Z01S01[SW]", player)
                        or state.has("D02Z01S01[CherubsR]", player)
                    )
                    and can_dawn_jump(state, logic, player)
                )
            )
        ))
    # Doors
    set_rule(world.get_entrance("D02Z01S01[SW]", player),
        lambda state: (
            state.has("OpenedWOTWCave", player)
            and (
                state.has("D02Z01S01[W]", player)
                or state.has("D02Z01S01[CherubsL]", player)
                or state.has("D02Z01S01[CherubsR]", player)
                or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
            )
        ))
    set_rule(world.get_entrance("D02Z01S01[W]", player),
        lambda state: (
            state.has("D02Z01S01[CherubsL]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
            or (
                (
                    state.has("D02Z01S01[SW]", player)
                    or state.has("D02Z01S01[CherubsR]", player)
                )
                and can_dawn_jump(state, logic, player)
            )
        ))


    # D02Z01S02 (Where Olive Trees Wither)
    # Items
    set_rule(world.get_location("WOTW: Upper east Child of Moonlight", player),
        lambda state: (
            state.has("D02Z01S02[NE]", player)
            or (
                state.has("D02Z01S02[NW]", player)
                or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
            )
            and (
                can_walk_on_root(state, player)
                or can_cross_gap(state, logic, player, 4)
                or pillar(state, player)
            )
        ))
    # Doors
    set_rule(world.get_entrance("D02Z01S02[NW]", player),
        lambda state: (
            state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
            or (
                state.has("D02Z01S02[NE]", player)
                and can_walk_on_root(state, player)
                and can_cross_gap(state, logic, player, 5)
            )
        ))
    set_rule(world.get_entrance("D02Z01S02[NE]", player),
        lambda state: (
            (
                state.has("Purified Hand of the Nun", player)
                and can_enemy_bounce(logic, enemy)
            )
            or (
                state.has("D02Z01S02[NW]", player)
                or state.has("Wall Climb Ability", player)
                or state.has("Purified Hand of the Nun", player)
            )
            and (
                can_walk_on_root(state, player)
                or can_cross_gap(state, logic, player, 10)
            )
        ))
    set_rule(world.get_entrance("D02Z01S02[]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D02Z01S03 (Where Olive Trees Wither)
    # No items
    # Doors
    set_rule(world.get_entrance("D02Z01S03[W]", player),
        lambda state: (
            state.has("D02Z01S03[SE]", player)
            or state.has("D02Z01S03[Cherubs]", player)
            or state.has("Wall Climb Ability", player)
        ))
    set_rule(world.get_entrance("D02Z01S03[SE]", player),
        lambda state: (
            state.has("D02Z01S03[W]", player)
            or state.has("D02Z01S03[Cherubs]", player)
            or state.has("Wall Climb Ability", player)
        ))


    # D02Z01S04 (Where Olive Trees Wither)
    # Items
    set_rule(world.get_location("WOTW: Gift for the tomb", player),
        lambda state: (
            state.has("Golden Thimble Filled with Burning Oil", player)
            and (
                state.has("D02Z01S01[W]", player)
                or state.has("D02Z01S01[CherubsL]", player)
                or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
                or (
                    (
                        state.has("D02Z01S01[SW]", player)
                        or state.has("D02Z01S01[CherubsR]", player)
                    )
                    and can_dawn_jump(state, logic, player)
                )
            )
        ))
    # Doors
    set_rule(world.get_entrance("D02Z01S04[-N]", player),
        lambda state: (
            state.has("Golden Thimble Filled with Burning Oil", player)
            and (
                state.has("D02Z01S01[W]", player)
                or state.has("D02Z01S01[CherubsL]", player)
                or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
                or (
                    (
                        state.has("D02Z01S01[SW]", player)
                        or state.has("D02Z01S01[CherubsR]", player)
                    ) 
                    and can_dawn_jump(state, logic, player)
                )
            )
        ))


    # D02Z01S06 (Where Olive Trees Wither)
    # Items
    set_rule(world.get_location("WOTW: Underground ledge", player),
        lambda state: (
            state.has("Wall Climb Ability", player)
            and (
                state.has("Purified Hand of the Nun", player)
                or state.has("Blood Perpetuated in Sand", player)
                and (
                    state.has("Dash Ability", player)
                    or state.has("D02Z01S06[Cherubs]", player)
                )
            )
        ))
    set_rule(world.get_location("WOTW: Underground Child of Moonlight", player),
        lambda state: (
            (
                state.has("D02Z01S06[W]", player)
                or state.has("Dash Ability", player)
                or state.has("Purified Hand of the Nun", player)
                and state.has("Wall Climb Ability", player)
            )
            and (
                pillar(state, player)
                or state.has("Cante Jondo of the Three Sisters", player)
                or can_dive_laser(state, logic, player)
            )
            or (
                state.has("Wall Climb Ability", player)
                and (
                    state.has("D02Z01S06[W]", player)
                    or state.has("Purified Hand of the Nun", player)
                    or state.has("Dash Ability", player)
                )
            )
            and (
                state.has("Lorquiana", player)
                or aubade(state, player)
                or state.has("Cantina of the Blue Rose", player)
                or can_air_stall(state, logic, player)
            )
        ))
    # Doors
    set_rule(world.get_entrance("D02Z01S06[W]", player),
        lambda state: (
            state.has("Dash Ability", player)
            or state.has_all({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))
    set_rule(world.get_entrance("D02Z01S06[E]", player),
        lambda state: state.has("Wall Climb Ability", player))
    # Event
    set_rule(world.get_location("OpenedWOTWCave", player),
        lambda state: opened_wotw_cave(state, player))


    # D02Z01S08 (Where Olive Trees Wither)
    # Items
    set_rule(world.get_location("WOTW: Underground tomb", player),
        lambda state: state.has("Dried Flowers bathed in Tears", player))
    # No doors


    # D02Z01S09 (Where Olive Trees Wither)
    # Items
    set_rule(world.get_location("WOTW: Upper east statue", player),
        lambda state: (
            can_walk_on_root(state, player)
            or can_cross_gap(state, logic, player, 11)
            or state.has("Purified Hand of the Nun", player)
            and can_enemy_bounce(logic, enemy)
        ))
    # Doors
    set_rule(world.get_entrance("D02Z01S09[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D02Z01S09[-CherubsR]", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            and (
                can_walk_on_root(state, player)
                or can_cross_gap(state, logic, player, 2)
                or can_enemy_bounce(logic, enemy)
                and can_air_stall(state, logic, player)
            )
        ))


    # D02Z02S01 (Graveyard of the Peaks)
    # No items
    # Doors
    set_rule(world.get_entrance("D02Z02S01[W]", player),
        lambda state: (
            state.has("D02Z02S01[NW]", player)
            or state.has("D02Z02S01[Cherubs]", player)
            or state.has("Dash Ability", player)
        ))
    set_rule(world.get_entrance("D02Z02S01[NW]", player),
        lambda state: (
            state.has("D02Z02S01[Cherubs]", player)
            or state.has("Wall Climb Ability", player)
            and (
                state.has("D02Z02S01[W]", player)
                or state.has("Dash Ability", player)
            )
        ))
    set_rule(world.get_entrance("D02Z02S01[E]", player),
        lambda state: (
            state.has("D02Z02S01[NW]", player)
            or state.has("D02Z02S01[Cherubs]", player)
            or state.has_any({"Wall Climb Ability", "Dash Ability"}, player)
        ))


    # D02Z02S02 (Graveyard of the Peaks)
    # Items
    set_rule(world.get_location("GotP: Center shaft Child of Moonlight", player),
        lambda state: (
            state.has("D02Z02S02[CherubsL]", player)
            or state.has("D02Z02S02[CherubsR]", player)
            or (
                (
                    state.has("D02Z02S02[NW]", player)
                    or state.has("D02Z02S02[NE]", player)
                    or state.has("Wall Climb Ability", player)
                )
                and (
                    state.has_any({"Purified Hand of the Nun", "Cante Jondo of the Three Sisters"}, player)
                    or pillar(state, player)
                    or tirana(state, player)
                    or can_dive_laser(state, logic, player)
                )
            )
        ))
    # Doors
    set_rule(world.get_entrance("D02Z02S02[NW]", player),
        lambda state: (
            state.has("D02Z02S02[NE]", player)
            or state.has("D02Z02S02[CherubsL]", player)
            or state.has("D02Z02S02[CherubsR]", player)
            or state.has("Wall Climb Ability", player)
        ))
    set_rule(world.get_entrance("D02Z02S02[NE]", player),
        lambda state: (
            state.has("D02Z02S02[NW]", player)
            or state.has("D02Z02S02[CherubsL]", player)
            or state.has("D02Z02S02[CherubsR]", player)
            or state.has("Wall Climb Ability", player)
        ))
    set_rule(world.get_entrance("D02Z02S02[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D02Z02S03 (Graveyard of the Peaks)
    # Items
    set_rule(world.get_location("GotP: Lower east shaft", player),
        lambda state: (
            state.has("D02Z02S03[NW]", player)
            or state.has("D02Z02S03[NE]", player)
            or state.has("Wall Climb Ability", player)
            or can_cross_gap(state, logic, player, 2)
        ))
    set_rule(world.get_location("GotP: Center east shaft", player),
        lambda state: (
            state.has("D02Z02S03[NW]", player)
            or state.has("D02Z02S03[NE]", player)
            or state.has_any({"Wall Climb Ability", "Purified Hand of the Nun"}, player)
        ))
    set_rule(world.get_location("GotP: Upper east shaft", player),
        lambda state: (
            can_climb_on_root(state, player)
            and (
                state.has("D02Z02S03[NE]", player)
                or state.has("Purified Hand of the Nun", player)
                or state.has("Blood Perpetuated in Sand", player)
            )
            or state.has_all({"Blood Perpetuated in Sand", "Purified Hand of the Nun"}, player)
        ))
    # Doors
    set_rule(world.get_entrance("D02Z02S03[NW]", player),
        lambda state: (
            state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
            or state.has("D02Z02S03[NE]", player)
            and can_walk_on_root(state, player)
        ))
    set_rule(world.get_entrance("D02Z02S03[NE]", player),
        lambda state: (
            state.has("Wall Climb Ability", player)
            and (
                can_cross_gap(state, logic, player, 11)
                or (
                    state.has("Blood Perpetuated in Sand", player)
                    and (
                        can_walk_on_root(state, player)
                        or can_cross_gap(state, logic, player, 7)
                    )
                )
                or (
                    can_walk_on_root(state, player)
                    and (
                        state.has("Purified Hand of the Nun", player)
                        or can_air_stall(state, logic, player)
                    )
                )
            )
        ))
    set_rule(world.get_entrance("D02Z02S03[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D02Z02S04 (Graveyard of the Peaks)
    # Items
    set_rule(world.get_location("GotP: Lower west shaft", player),
        lambda state: state.has("D02Z02S04[E]", player))
    set_rule(world.get_location("GotP: Upper west shaft", player),
        lambda state:
        (
            state.has("D02Z02S04[NE]", player)
            or (
                (
                    state.has("D02Z02S04[W]", player)
                    or state.has("D02Z02S04[E]", player)
                    and state.has("Dash Ability", player)
                )
                and (
                    state.has("Purified Hand of the Nun", player)
                    or state.has("Wall Climb Ability", player)
                )
            )
            or (
                state.has("D02Z02S04[SE]", player)
                and (
                    state.has("Wall Climb Ability", player)
                    or state.has("Purified Hand of the Nun", player)
                    and can_enemy_upslash(state, logic, enemy, player)
                )
            )
        ))
    set_rule(world.get_location("GotP: West shaft Child of Moonlight", player),
        lambda state: 
        (
            (
                state.has("D02Z02S04[NE]", player)
                or state.has("D02Z02S04[W]", player)
                or state.has("D02Z02S04[E]", player)
                and state.has("Dash Ability", player)
                or state.has("D02Z02S04[SE]", player)
                and (
                    state.has("Wall Climb Ability", player)
                    or state.has("Purified Hand of the Nun", player)
                    and can_enemy_upslash(state, logic, enemy, player)
                )
            )
            and (
                state.has("Blood Perpetuated in Sand", player)
                and state.has("Dash Ability", player)
                or state.has("Purified Hand of the Nun", player)
                and can_enemy_bounce(logic, enemy)
                or state.has_any({"Lorquiana", "Cante Jondo of the Three Sisters", "Verdiales of the Forsaken Hamlet", "Cantina of the Blue Rose"}, player)
                or aubade(state, player)
            )
            or (
                state.has("D02Z02S04[NE]", player)
                or state.has("D02Z02S04[W]", player)
                or state.has("D02Z02S04[E]", player)
                and state.has("Dash Ability", player)
                or state.has("D02Z02S04[SE]", player)
            )
            and pillar(state, player)
        ))
    # Doors
    set_rule(world.get_entrance("D02Z02S04[W]", player),
        lambda state: (
            state.has("D02Z02S04[NE]", player)
            or state.has("D02Z02S04[E]", player)
            and state.has("Dash Ability", player)
            or state.has("D02Z02S04[SE]", player)
            and (
                state.has("Wall Climb Ability", player)
                or state.has("Purified Hand of the Nun", player)
                and can_enemy_upslash(state, logic, enemy, player)
            )
        ))
    set_rule(world.get_entrance("D02Z02S04[SE]", player),
        lambda state: (
            state.has("D02Z02S04[NE]", player)
            or state.has("D02Z02S04[W]", player)
            or state.has("Dash Ability", player)
        ))
    set_rule(world.get_entrance("D02Z02S04[NE]", player),
        lambda state: (
            (
                (
                    state.has("D02Z02S04[W]", player)
                    or state.has("D02Z02S04[E]", player)
                    and state.has("Dash Ability", player)
                )
                and state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
            )
            or (
                state.has("D02Z02S04[SE]", player)
                and (
                    state.has("Wall Climb Ability", player)
                    or state.has("Purified Hand of the Nun", player)
                    and can_enemy_upslash(state, logic, enemy, player)
                )
            )
        ))
    set_rule(world.get_entrance("D02Z02S04[-CherubsL]", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            and (
                state.has("D02Z02S04[NE]", player)
                or state.has("D02Z02S04[W]", player)
                or state.has("D02Z02S04[SE]", player)
                or state.has("Dash Ability", player)
            )
        ))


    # D02Z02S05 (Graveyard of the Peaks)
    # Items
    set_rule(world.get_location("GotP: Center shaft ledge", player),
        lambda state: (
            state.has("D02Z02S05[NW]", player)
            or state.has("Wall Climb Ability", player)
        ))
    # Doors
    set_rule(world.get_entrance("D02Z02S05[W]", player),
        lambda state: (
            state.has("Purified Hand of the Nun", player)
            and can_enemy_bounce(logic, enemy)
        ))
    set_rule(world.get_entrance("D02Z02S05[E]", player),
        lambda state: (
            state.has("D02Z02S05[NW]", player)
            or state.has("D02Z02S05[E]", player)
            or state.has("Wall Climb Ability", player)
        ))
    set_rule(world.get_entrance("D02Z02S05[NW]", player),
        lambda state: (
            state.has("D02Z02S05[NW]", player)
            or state.has("Wall Climb Ability", player)
        ))
    set_rule(world.get_entrance("D02Z02S05[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D02Z02S05[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D02Z02S08 (Graveyard of the Peaks)
    # Items
    set_rule(world.get_location("GotP: Shop cave hidden hole", player),
        lambda state: (
            state.has("D02Z02S08[CherubsR]", player)
            or state.has("Blood Perpetuated in Sand", player)
            or can_break_holes(state, player)
            or can_cross_gap(state, logic, player, 8)
        ))
    set_rule(world.get_location("GotP: Shop cave Child of Moonlight", player),
        lambda state: (
            state.has("D02Z02S08[CherubsR]", player)
            or can_dive_laser(state, logic, player)
            or state.has("Blood Perpetuated in Sand", player)
            or pillar(state, player)
            or can_cross_gap(state, logic, player, 8)
        ))
    # No doors


    # D02Z02S11 (Graveyard of the Peaks)
    # No items
    # Doors
    set_rule(world.get_entrance("D02Z02S11[E]", player),
        lambda state: (
            state.has("D02Z02S11[NW]", player)
            or state.has("D02Z02S11[NE]", player)
            or can_cross_gap(state, logic, player, 6)
        ))
    set_rule(world.get_entrance("D02Z02S11[NW]", player),
        lambda state: state.has("D02Z02S11[NE]", player))
    set_rule(world.get_entrance("D02Z02S11[NE]", player),
        lambda state: state.has("D02Z02S11[NW]", player))
    set_rule(world.get_entrance("D02Z02S11[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D02Z02S14 (Graveyard of the Peaks)
    # Items
    set_rule(world.get_location("GotP: Amanecida of the Bejeweled Arrow", player),
        lambda state: can_beat_boss(state, "Graveyard", logic, player))
    # Doors
    set_rule(world.get_entrance("D02Z02S14[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D02Z03S02 (Convent of Our Lady of the Charred Visage)
    # No items
    # Doors
    set_rule(world.get_entrance("D02Z03S02[W]", player),
        lambda state: (
            state.has("D02Z03S02[NW]", player)
            or state.has("D02Z03S02[NE]", player)
            or state.has("D02Z03S02[N]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))
    set_rule(world.get_entrance("D02Z03S02[NW]", player),
        lambda state: (
            state.has("D02Z03S02[NE]", player)
            or state.has("D02Z03S02[N]", player)
        ))
    set_rule(world.get_entrance("D02Z03S02[NE]", player),
        lambda state: (
            state.has("D02Z03S02[NW]", player)
            or state.has("D02Z03S02[N]", player)
        ))
    set_rule(world.get_entrance("D02Z03S02[N]", player),
        lambda state: (
            state.has("D02Z03S02[NW]", player)
            or state.has("D02Z03S02[NE]", player)
        ))
    add_rule(world.get_entrance("D02Z03S02[N]", player),
        lambda state: state.has("OpenedConventLadder", player))


    # D02Z03S03 (Convent of Our Lady of the Charred Visage)
    # Items
    set_rule(world.get_location("CoOLotCV: Snowy window ledge", player),
        lambda state: (
            state.has("D02Z03S03[NW]", player)
            or state.has("Blood Perpetuated in Sand", player)
            or can_cross_gap(state, logic, player, 3)
        ))
    # Doors
    set_rule(world.get_entrance("D02Z03S03[NW]", player),
        lambda state: (
            state.has("Blood Perpetuated in Sand", player)
            or can_cross_gap(state, logic, player, 3)
        ))


    # D02Z03S05 (Convent of Our Lady of the Charred Visage)
    # Items
    set_rule(world.get_location("CoOLotCV: Center miasma room", player),
        lambda state: (
            state.has("Dash Ability", player)
            and (
                state.has("D02Z03S05[S]", player)
                or state.has("D02Z03S05[NE]", player)
                or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
            )
        ))
    # Doors
    set_rule(world.get_entrance("D02Z03S05[S]", player),
        lambda state: (
            state.has("D02Z03S05[NE]", player)
            or state.has("Wall Climb Ability", player)
        ))
    set_rule(world.get_entrance("D02Z03S05[NE]", player),
        lambda state: (
            state.has("D02Z03S05[S]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))


    # D02Z03S10 (Convent of Our Lady of the Charred Visage)
    # No items
    # Doors
    set_rule(world.get_entrance("D02Z03S10[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    

    # D02Z03S11 (Convent of Our Lady of the Charred Visage)
    # Event
    set_rule(world.get_location("OpenedConventLadder", player),
        lambda state: opened_convent_ladder(state, player))


    # D02Z03S12 (Convent of Our Lady of the Charred Visage)
    # Items
    set_rule(world.get_location("CoOLotCV: Lower west statue", player),
        lambda state: (
            can_survive_poison(state, logic, player, 1)
            and state.has("Dash Ability", player)
        ))
    # No doors


    # D02Z03S18 (Convent of Our Lady of the Charred Visage)
    # No items
    # Doors
    set_rule(world.get_entrance("D02Z03S18[NW]", player),
        lambda state: (
            state.has("D02Z03S18[NE]", player)
            or state.has("Wall Climb Ability", player)
        ))
    set_rule(world.get_entrance("D02Z03S18[NE]", player),
        lambda state: (
            state.has("D02Z03S18[NW]", player)
            or state.has("Wall Climb Ability", player)
        ))


    # D02Z03S20 (Convent of Our Lady of the Charred Visage)
    # Items
    set_rule(world.get_location("CoOLotCV: Our Lady of the Charred Visage", player),
        lambda state: can_beat_boss(state, "Convent", logic, player))
    # Doors
    set_rule(world.get_entrance("D02Z03S20[W]", player),
        lambda state: can_beat_boss(state, "Convent", logic, player))
    set_rule(world.get_entrance("D02Z03S20[E]", player),
        lambda state: can_beat_boss(state, "Convent", logic, player))


    # D02Z03S21 (Convent of Our Lady of the Charred Visage)
    # Items
    set_rule(world.get_location("CoOLotCV: Fountain of burning oil", player),
        lambda state: state.has("Empty Golden Thimble", player))
    # No doors


    # D03Z01S01 (Mountains of the Endless Dusk)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z01S01[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D03Z01S02 (Mountains of the Endless Dusk)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z01S02[W]", player),
        lambda state: (
            state.has("Wall Climb Ability", player)
            or can_cross_gap(state, logic, player, 3)
        ))
    set_rule(world.get_entrance("D03Z01S02[E]", player),
        lambda state: (
            state.has("Wall Climb Ability", player)
            or can_cross_gap(state, logic, player, 7)
        ))


    # D03Z01S03 (Mountains of the Endless Dusk)
    # Items
    set_rule(world.get_location("MotED: Platform above chasm", player),
        lambda state: (
            state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun"}, player)
            and (
                state.has("D03Z01S03[W]", player)
                or state.has("D03Z01S03[SW]", player)
                or can_cross_gap(state, logic, player, 9)
            )
        ))
    set_rule(world.get_location("MotED: 1st meeting with Redento", player),
        lambda state: (
            state.has("D03Z01S03[W]", player)
            or state.has("D03Z01S03[SW]", player)
            or can_cross_gap(state, logic, player, 9)
        ))
    set_rule(world.get_location("MotED: Child of Moonlight, above chasm", player),
        lambda state: (
            state.has("D03Z01S03[W]", player)
            or state.has("D03Z01S03[SW]", player)
            or can_cross_gap(state, logic, player, 9)
        ))
    set_rule(world.get_location("MotED: Amanecida of the Golden Blades", player),
        lambda state: (
            can_beat_boss(state, "Jondo", logic, player)
            and (
                state.has("D03Z01S03[W]", player)
                or state.has("D03Z01S03[SW]", player)
                or can_cross_gap(state, logic, player, 9)
            )
        ))
    # Doors
    set_rule(world.get_entrance("D03Z01S03[W]", player),
        lambda state: (
            state.has("Wall Climb Ability", player)
            and (
                state.has("D03Z01S03[SW]", player)
                or can_cross_gap(state, logic, player, 9)
            )
        ))
    set_rule(world.get_entrance("D03Z01S03[E]", player),
        lambda state: state.has("Wall Climb Ability", player))
    set_rule(world.get_entrance("D03Z01S03[SW]", player),
        lambda state: (
            state.has("D03Z01S03[W]", player)
            or can_cross_gap(state, logic, player, 9)
        ))
    set_rule(world.get_entrance("D03Z01S03[-WestL]", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            and (
                state.has("D03Z01S03[W]", player)
                or state.has("D03Z01S03[SW]", player)
                or can_cross_gap(state, logic, player, 9)
            )
        ))
    set_rule(world.get_entrance("D03Z01S03[-WestR]", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            and (
                state.has("D03Z01S03[W]", player)
                or state.has("D03Z01S03[SW]", player)
                or can_cross_gap(state, logic, player, 9)
            )
        ))
    set_rule(world.get_entrance("D03Z01S03[-EastL]", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            and (
                state.has("D03Z01S03[W]", player)
                or state.has("D03Z01S03[SW]", player)
                or can_cross_gap(state, logic, player, 5)
            )
        ))
    set_rule(world.get_entrance("D03Z01S03[-EastR]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D03Z01S04 (Mountains of the Endless Dusk)
    # Items
    set_rule(world.get_location("MotED: Blood platform alcove", player),
        lambda state: (
            state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun"}, player)
            or upwarp_skips_allowed(logic)
        ))
    # No doors


    # D03Z01S06 (Mountains of the Endless Dusk)
    # Items
    set_rule(world.get_location("MotED: Perpetva", player),
        lambda state: can_beat_boss(state, "Perpetua", logic, player))
    set_rule(world.get_location("MotED: Egg hatching", player),
        lambda state: can_beat_boss(state, "Perpetua", logic, player) and \
            state.has("Egg of Deformity", player))
    # Doors
    set_rule(world.get_entrance("D03Z01S06[W]", player),
        lambda state: can_beat_boss(state, "Perpetua", logic, player))
    set_rule(world.get_entrance("D03Z01S06[E]", player),
        lambda state: can_beat_boss(state, "Perpetua", logic, player))


    # D03Z02S01 (Jondo)
    # Items
    set_rule(world.get_location("Jondo: Upper east chest", player),
        lambda state: (
            state.has("D03Z02S01[Cherubs]", player)
            or can_climb_on_root(state, player)
            or can_cross_gap(state, logic, player, 8)
            or state.has("Purified Hand of the Nun", player)
            and can_enemy_bounce(logic, enemy)
        ))
    # Doors
    set_rule(world.get_entrance("D03Z02S01[W]", player),
        lambda state: (
            state.has("Wall Climb Ability", player)
            or state.has("Purified Hand of the Nun", player)
            and can_enemy_bounce(logic, enemy)
        ))
    set_rule(world.get_entrance("D03Z02S01[N]", player),
        lambda state: (
            state.has("Wall Climb Ability", player)
            or state.has("Purified Hand of the Nun", player)
        ))


    # D03Z02S02 (Jondo)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z02S02[W]", player),
        lambda state: (
            state.has("D03Z02S02[CherubsL]", player)
            or state.has("Purified Hand of the Nun", player)
            and (
                state.has("D03Z02S02[E]", player)
                or state.has("D03Z02S02[CherubsR]", player)
                or state.has("Wall Climb Ability", player)
                or can_enemy_bounce(logic, enemy)
            )
        ))
    set_rule(world.get_entrance("D03Z02S02[E]", player),
        lambda state: (
            state.has("Wall Climb Ability", player)
            or state.has("Purified Hand of the Nun", player)
            and can_enemy_bounce(logic, enemy)
        ))
    
    # D03Z02S03 (Jondo)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z02S03[W]", player),
        lambda state: (
            state.has("Dash Ability", player)
            and (
                state.has("D03Z02S03[E]", player)
                or state.has("D03Z02S03[N]", player)
                or state.has("D03Z02S03[SE2]", player)
            )
        ))
    set_rule(world.get_entrance("D03Z02S03[E]", player),
        lambda state: (
            (
                can_air_stall(state, logic, player)
                or state.has_any({"Purified Hand of the Nun", "Boots of Pleading"}, player)
            )
            and (
                state.has("Dash Ability", player)
                or state.has("D03Z02S03[N]", player)
                or state.has("D03Z02S03[SE2]", player)
            )
        ))
    set_rule(world.get_entrance("D03Z02S03[N]", player),
        lambda state: (
            state.has("D03Z02S03[W]", player)
            and state.has("Dash Ability", player)
            or state.has("D03Z02S03[E]", player)
            or state.has("D03Z02S03[SE2]", player)
        ))
    set_rule(world.get_entrance("D03Z02S03[SE2]", player),
        lambda state: (
            state.has("D03Z02S03[W]", player)
            and state.has("Dash Ability", player)
            or state.has("D03Z02S03[E]", player)
            or state.has("D03Z02S03[N]", player)
        ))
    set_rule(world.get_entrance("D03Z02S03[SW]", player),
        lambda state: (
            state.has("D03Z02S03[SE]", player)
            or state.has("D03Z02S03[SSL]", player)
            or state.has("D03Z02S03[SSR]", player)
            or state.has("BrokeJondoBellW", player)
            and state.has("BrokeJondoBellE", player)
            and (
                state.has("D03Z02S03[W]", player)
                and state.has("Dash Ability", player)
                or state.has("D03Z02S03[E]", player)
                or state.has("D03Z02S03[N]", player)
                or state.has("D03Z02S03[SE2]", player)
            )
        ))
    set_rule(world.get_entrance("D03Z02S03[SE]", player),
        lambda state: (
            state.has("D03Z02S03[SW]", player)
            or state.has("D03Z02S03[SSL]", player)
            or state.has("D03Z02S03[SSR]", player)
            or state.has("BrokeJondoBellW", player)
            and state.has("BrokeJondoBellE", player)
            and (
                state.has("D03Z02S03[W]", player)
                and state.has("Dash Ability", player)
                or state.has("D03Z02S03[E]", player)
                or state.has("D03Z02S03[N]", player)
                or state.has("D03Z02S03[SE2]", player)
            )
        ))
    set_rule(world.get_entrance("D03Z02S03[SSL]", player),
        lambda state: (
            state.has("D03Z02S03[SW]", player)
            or state.has("D03Z02S03[SE]", player)
            or state.has("D03Z02S03[SSR]", player)
            or state.has("BrokeJondoBellW", player)
            and state.has("BrokeJondoBellE", player)
            and (
                state.has("D03Z02S03[W]", player)
                and state.has("Dash Ability", player)
                or state.has("D03Z02S03[E]", player)
                or state.has("D03Z02S03[N]", player)
                or state.has("D03Z02S03[SE2]", player)
            )
        ))
    set_rule(world.get_entrance("D03Z02S03[SSC]", player),
        lambda state: (
            state.has("D03Z02S03[SW]", player)
            or state.has("D03Z02S03[SE]", player)
            or state.has("D03Z02S03[SSL]", player)
            or state.has("D03Z02S03[SSR]", player)
            or state.has("BrokeJondoBellW", player)
            and state.has("BrokeJondoBellE", player)
            and (
                state.has("D03Z02S03[W]", player)
                and state.has("Dash Ability", player)
                or state.has("D03Z02S03[E]", player)
                or state.has("D03Z02S03[N]", player)
                or state.has("D03Z02S03[SE2]", player)
            )
        ))
    set_rule(world.get_entrance("D03Z02S03[SSR]", player),
        lambda state: (
            state.has("D03Z02S03[SW]", player)
            or state.has("D03Z02S03[SE]", player)
            or state.has("D03Z02S03[SSL]", player)
            or state.has("BrokeJondoBellW", player)
            and state.has("BrokeJondoBellE", player)
            and (
                state.has("D03Z02S03[W]", player)
                and state.has("Dash Ability", player)
                or state.has("D03Z02S03[E]", player)
                or state.has("D03Z02S03[N]", player)
                or state.has("D03Z02S03[SE2]", player)
            )
        ))


    # D03Z02S04 (Jondo)
    # Items
    set_rule(world.get_location("Jondo: Lower east under chargers", player),
        lambda state: (
            state.has("D03Z02S04[NE]", player)
            or state.has("D03Z02S04[S]", player)
            or state.has("Wall Climb Ability", player)
        ))
    # Doors
    set_rule(world.get_entrance("D03Z02S04[NW]", player),
        lambda state: state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_entrance("D03Z02S04[NE]", player),
        lambda state: (
            state.has("Wall Climb Ability", player)
            or (
                state.has("D03Z02S04[S]", player)
                and state.has("Purified Hand of the Nun", player)
            )
        ))
    set_rule(world.get_entrance("D03Z02S04[S]", player),
        lambda state: (
            state.has("D03Z02S04[NE]", player)
            or state.has("Wall Climb Ability", player)
        ))


    # D03Z02S05 (Jondo)
    # Items
    set_rule(world.get_location("Jondo: Upper east Child of Moonlight", player),
        lambda state: (
            state.has("D03Z02S05[E]", player)
            or state.has("D03Z02S05[S]", player)
            or can_cross_gap(state, logic, player, 5)
            or (
                can_enemy_bounce(logic, enemy)
                and can_cross_gap(state, logic, player, 3)
            )
        ))
    # Doors
    set_rule(world.get_entrance("D03Z02S05[E]", player),
        lambda state: (
            state.has("D03Z02S05[S]", player)
            or can_cross_gap(state, logic, player, 5)
            or (
                can_enemy_bounce(logic, enemy)
                and can_cross_gap(state, logic, player, 3)
            )
        ))
    set_rule(world.get_entrance("D03Z02S05[S]", player),
        lambda state: (
            state.has("D03Z02S05[E]", player)
            or can_cross_gap(state, logic, player, 5)
            or (
                can_enemy_bounce(logic, enemy)
                and can_cross_gap(state, logic, player, 3)
            )
        ))
    # Event
    set_rule(world.get_location("BrokeJondoBellE", player),
        lambda state: broke_jondo_bell_e(state, logic, enemy, player))


    # D03Z02S08 (Jondo)
    # Items
    set_rule(world.get_location("Jondo: Lower west bell alcove", player),
        lambda state: (
            state.has("D03Z02S08[N]", player)
            or state.has("D03Z02S08[W]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))
    # Doors
    set_rule(world.get_entrance("D03Z02S08[W]", player),
        lambda state: (
            state.has("D03Z02S08[N]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))
    set_rule(world.get_entrance("D03Z02S08[N]", player),
        lambda state: (
            state.has("D03Z02S08[W]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))


    # D03Z02S09 (Jondo)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z02S09[W]", player),
        lambda state: state.has("Dash Ability", player))
    set_rule(world.get_entrance("D03Z02S09[N]", player),
        lambda state: (
            state.has("D03Z02S09[S]", player)
            or state.has("D03Z02S09[Cherubs]", player)
            or state.has("Dash Ability", player)
        ))
    set_rule(world.get_entrance("D03Z02S09[S]", player),
        lambda state: (
            state.has("D03Z02S09[N]", player)
            or state.has("D03Z02S09[Cherubs]", player)
            or state.has("Dash Ability", player)
        ))
    # Event
    set_rule(world.get_location("BrokeJondoBellW", player),
        lambda state: broke_jondo_bell_w(state, player))


    # D03Z02S10 (Jondo)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z02S10[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D03Z02S11 (Jondo)
    # Items
    set_rule(world.get_location("Jondo: Spike tunnel statue", player),
        lambda state: (
            state.has("D03Z02S11[W]", player)
            and state.has("Purified Hand of the Nun", player)
            or state.has("D03Z02S11[E]", player)
            and state.has("Dash Ability", player)
            and (
                state.has("Wall Climb Ability", player)
                or can_cross_gap(state, logic, player, 2)
                or precise_skips_allowed(logic)
                and can_cross_gap(state, logic, player, 1)
            )
        ))
    set_rule(world.get_location("Jondo: Spike tunnel Child of Moonlight", player),
        lambda state: (
            state.has("D03Z02S11[W]", player)
            and (
                state.has("Purified Hand of the Nun", player)
                or state.has("Dash Ability", player)
                and (
                    state.has("Wall Climb Ability", player)
                    or can_cross_gap(state, logic, player, 2)
                    and can_enemy_bounce(logic, enemy)
                    or can_cross_gap(state, logic, player, 3)
                )
            )
            or state.has("D03Z02S11[E]", player)
            and state.has("Dash Ability", player)
            and (
                can_cross_gap(state, logic, player, 1)
                or state.has("Wall Climb Ability", player)
                or can_enemy_bounce(logic, enemy)
            )
        ))
    # Doors
    set_rule(world.get_entrance("D03Z02S11[W]", player),
        lambda state: (
            state.has("Dash Ability", player)
            and (
                state.has("Wall Climb Ability", player)
                or can_cross_gap(state, logic, player, 2)
                or precise_skips_allowed(logic)
                and can_cross_gap(state, logic, player, 1)
            )
        ))
    set_rule(world.get_entrance("D03Z02S11[E]", player),
        lambda state: (
            state.has("Dash Ability", player)
            and (
                state.has("Wall Climb Ability", player)
                or state.has("Purified Hand of the Nun", player)
                or can_cross_gap(state, logic, player, 2)
                and can_enemy_bounce(logic, enemy)
            )
        ))

    # D03Z02S13 (Jondo)
    # Items
    set_rule(world.get_location("Jondo: Upper west tree root", player),
        lambda state: (
            can_walk_on_root(state, player)
            or can_cross_gap(state, logic, player, 3)
        ))
    # Doors
    set_rule(world.get_entrance("D03Z02S13[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D03Z03S01 (Grievance Ascends)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z03S01[NL]", player),
        lambda state: (
            state.has("D03Z03S01[NR]", player)
            or state.has("D03Z03S01[NC]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))
    set_rule(world.get_entrance("D03Z03S01[NR]", player),
        lambda state: (
            state.has("D03Z03S01[NL]", player)
            or state.has("D03Z03S01[NC]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))


    # D03Z03S02 (Grievance Ascends)
    # Items
    set_rule(world.get_location("GA: Lower west ledge", player),
        lambda state: can_survive_poison(state, logic, player, 1))
    # Doors
    set_rule(world.get_entrance("D03Z03S02[W]", player),
        lambda state: (
            state.has("D03Z03S02[NE]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))
    set_rule(world.get_entrance("D03Z03S02[NE]", player),
        lambda state: state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))


    # D03Z03S03 (Grievance Ascends)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z03S03[W]", player),
        lambda state: state.has("D03Z03S03[NE]", player))
    set_rule(world.get_entrance("D03Z03S03[NE]", player),
        lambda state: state.has("D03Z03S03[W]", player))


    # D03Z03S04 (Grievance Ascends)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z03S04[NW]", player),
        lambda state: (
            state.has("D03Z03S04[NE]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
            and (
                state.has("D03Z03S04[E]", player)
                or state.has("D03Z03S04[SW]", player)
                or state.has("Blood Perpetuated in Sand", player)
                or can_cross_gap(state, logic, player, 10)
            )
        ))
    set_rule(world.get_entrance("D03Z03S04[NE]", player),
        lambda state: (
            (
                state.has("Wall Climb Ability", player)
                or state.has("Purified Hand of the Nun", player)
                and can_enemy_bounce(logic, enemy)
            )
            and (
                state.has("D03Z03S04[NW]", player)
                or state.has("D03Z03S04[E]", player)
                or state.has("D03Z03S04[SW]", player)
                or state.has("Blood Perpetuated in Sand", player)
                or can_cross_gap(state, logic, player, 10)
            )
        ))
    set_rule(world.get_entrance("D03Z03S04[E]", player),
        lambda state: (
            state.has("D03Z03S04[NW]", player)
            or state.has("D03Z03S04[NE]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
            and (
                state.has("D03Z03S04[SW]", player)
                or state.has("Blood Perpetuated in Sand", player)
                or can_cross_gap(state, logic, player, 10)
            )
        ))
    set_rule(world.get_entrance("D03Z03S04[SW]", player),
        lambda state: (
            state.has("D03Z03S04[NW]", player)
            or state.has("D03Z03S04[NE]", player)
            or state.has("D03Z03S04[E]", player)
            or state.has("Blood Perpetuated in Sand", player)
            or can_cross_gap(state, logic, player, 10)
        ))
    set_rule(world.get_entrance("D03Z03S04[SE]", player),
        lambda state: state.has("Blood Perpetuated in Sand", player))
    set_rule(world.get_entrance("D03Z03S04[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D03Z03S05 (Grievance Ascends)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z03S05[NW]", player),
        lambda state: state.has("D03Z03S05[NE]", player))
    set_rule(world.get_entrance("D03Z03S05[NE]", player),
        lambda state: state.has("D03Z03S05[NW]", player))
    set_rule(world.get_entrance("D03Z03S05[SW]", player),
        lambda state: state.has("D03Z03S05[SE]", player) or \
            state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D03Z03S05[SE]", player),
        lambda state: state.has("D03Z03S05[SW]", player) or \
            state.has("Linen of Golden Thread", player))


    # D03Z03S06 (Grievance Ascends)
    # Items
    set_rule(world.get_location("GA: Miasma room floor", player),
        lambda state: can_survive_poison(state, logic, player, 1))
    set_rule(world.get_location("GA: Miasma room treasure", player),
        lambda state: state.has("Wall Climb Ability", player))
    set_rule(world.get_location("GA: Miasma room Child of Moonlight", player),
        lambda state: (
            state.has("Wall Climb Ability", player)
            or can_cross_gap(state, logic, player, 11)
            and state.has("Taranto to my Sister", player)
            and obscure_skips_allowed(logic)
        ))
    # No doors


    # D03Z03S07 (Grievance Ascends)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z03S07[NW]", player),
        lambda state: (
            state.has("D03Z03S07[NE]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))
    set_rule(world.get_entrance("D03Z03S07[NE]", player),
        lambda state: (
            state.has("D03Z03S07[NE]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))


    # D03Z03S08 (Grievance Ascends)
    # Items
    set_rule(world.get_location("GA: End of blood bridge", player),
        lambda state: (
            state.has("Blood Perpetuated in Sand", player)
            or can_cross_gap(state, logic, player, 11)
        ))
    set_rule(world.get_location("GA: Blood bridge Child of Moonlight", player),
        lambda state: (
            (
                state.has("Blood Perpetuated in Sand", player)
                or can_cross_gap(state, logic, player, 11)
            )
            and (
                state.has_any({"Purified Hand of the Nun", "Cante Jondo of the Three Sisters", "Verdiales of the Forsaken Hamlet"}, player)
                or pillar(state, player)
                or tirana(state, player)
                or aubade(state, player)
                and can_air_stall(state, logic, player)
            )
        ))
    # Doors
    set_rule(world.get_entrance("D03Z03S08[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D03Z03S08[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D03Z03S09 (Grievance Ascends)
    # Items
    set_rule(world.get_location("GA: Lower east Child of Moonlight", player),
        lambda state: (
            can_climb_on_root(state, player)
            or state.has_any({"Purified Hand of the Nun", "Lorquiana", "Zarabanda of the Safe Haven", "Cante Jondo of the Three Sisters"}, player)
            or pillar(state, player)
            or aubade(state, player)
            or tirana(state, player)
        ))
    # No doors


    # D03Z03S10 (Grievance Ascends)
    # Items
    set_rule(world.get_location("GA: Altasgracias' gift", player),
        lambda state: state.has_group("egg", player, 3))
    set_rule(world.get_location("GA: Empty giant egg", player),
        lambda state: (
            state.has_group("egg", player, 3)
            and state.has("Hatched Egg of Deformity", player)
            and (
                state.has("D01Z02S01[W]", player)
                or state.has("D01Z02S01[E]", player)
            )
        ))
    # No doors


    # D03Z03S15 (Grievance Ascends)
    # Items
    set_rule(world.get_location("GA: Tres Angustias", player),
        lambda state: can_beat_boss(state, "Grievance", logic, player))
    # Doors
    set_rule(world.get_entrance("D03Z03S15[W]", player),
        lambda state: can_beat_boss(state, "Grievance", logic, player))
    set_rule(world.get_entrance("D03Z03S15[E]", player),
        lambda state: can_beat_boss(state, "Grievance", logic, player))


    # D04Z01S01 (Patio of the Silent Steps)
    # Items
    set_rule(world.get_location("PotSS: First area ledge", player),
        lambda state: (
            state.has("D04Z01S01[NE]", player)
            or state.has("D04Z01S01[N]", player)
            or can_cross_gap(state, logic, player, 3)
        ))
    # Doors
    set_rule(world.get_entrance("D04Z01S01[NE]", player),
        lambda state: (
            state.has("D04Z01S01[N]", player)
            or can_cross_gap(state, logic, player, 3)
        ))
    set_rule(world.get_entrance("D04Z01S01[N]", player),
        lambda state: (
            state.has("D04Z01S01[NE]", player)
            or can_cross_gap(state, logic, player, 3)
        ))


    # D04Z01S02 (Patio of the Silent Steps)
    # Items
    set_rule(world.get_location("PotSS: Second area ledge", player),
        lambda state: (
            can_climb_on_root(state, player)
            or can_cross_gap(state, logic, player, 3)
        ))
    # No doors


    # D04Z01S03 (Patio of the Silent Steps)
    # Items
    set_rule(world.get_location("PotSS: Third area upper ledge", player),
        lambda state: (
            can_walk_on_root(state, player)
            or can_cross_gap(state, logic, player, 3)
        ))
    # No doors


    # D04Z01S04 (Patio of the Silent Steps)
    # Items
    set_rule(world.get_location("PotSS: 4th meeting with Redento", player),
        lambda state: redento(state, blasphemousworld, player, 4))
    set_rule(world.get_location("PotSS: Amanecida of the Chiselled Steel", player),
        lambda state: can_beat_boss(state, "Patio", logic, player))
    # No doors


    # D04Z01S05 (Patio of the Silent Steps)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z01S05[N]", player),
        lambda state: (
            (
                state.has("Blood Perpetuated in Sand", player)
                and can_climb_on_root(state, player)
            )
            or state.has("Purified Hand of the Nun", player)
            and (
                state.has("Blood Perpetuated in Sand", player)
                or can_climb_on_root(state, player)
            )
        ))
    set_rule(world.get_entrance("D04Z01S05[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D04Z01S06 (Patio of the Silent Steps)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z01S06[E]", player),
        lambda state: state.has("Purified Hand of the Nun", player))
    set_rule(world.get_entrance("D04Z01S06[Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D04Z02S01 (Mother of Mothers)
    # Items
    if world.purified_hand[player]:
        set_rule(world.get_location("MoM: Western room ledge", player),
            lambda state: (
                state.has("D04Z02S01[N]", player)
                or state.has("D04Z02S01[NE]", player)
                and state.has("Dash Ability", player)
                and state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
            ))
    set_rule(world.get_location("MoM: Lower west Child of Moonlight", player),
        lambda state: (
            state.has("D04Z02S01[N]", player)
            or pillar(state, player)
            or state.has("D04Z02S01[NE]", player)
            and state.has("Dash Ability", player)
            and (
                state.has("Wall Climb Ability", player)
                or can_cross_gap(state, logic, player, 1)
            )
        ))
    # Doors
    set_rule(world.get_entrance("D04Z02S01[N]", player),
        lambda state: (
            state.has("D04Z02S04[NE]", player)
            and state.has("Dash Ability", player)
            and state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))
    set_rule(world.get_entrance("D04Z02S01[NE]", player),
        lambda state: (
            state.has("D04Z02S01[N]", player)
            or state.has("Dash Ability", player)
            and can_cross_gap(state, logic, player, 1)
        ))


    # D04Z02S02 (Mother of Mothers)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z02S02[NE]", player),
        lambda state: (
            (
                state.has("Purified Hand of the Nun", player)
                and upwarp_skips_allowed(logic)
            )
            or (
                state.has("Purified Hand of the Nun", player)
                and can_enemy_upslash(state, logic, enemy, player)
            )
            or (
                can_enemy_upslash(state, logic, enemy, player)
                and upwarp_skips_allowed(logic)
                and (
                    state.has("Wall Climb Ability", player)
                    or state.has("D04Z02S02[N]", player)
                )
            )
        ))
    set_rule(world.get_entrance("D04Z02S02[N]", player),
        lambda state: (
            state.has("D04Z02S02[NE]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))


    # D04Z02S04 (Mother of Mothers)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z02S04[NW]", player),
        lambda state: (
            state.has("D04Z02S04[NE]", player)
            or state.has("D04Z02S04[N]", player)
            or state.has("D04Z02S04[Cherubs]", player)
            or state.has_all({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))
    set_rule(world.get_entrance("D04Z02S04[NE]", player),
        lambda state: (
            state.has("D04Z02S04[NW]", player)
            or state.has("D04Z02S04[N]", player)
            or state.has("D04Z02S04[Cherubs]", player)
            or state.has_all({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))
    set_rule(world.get_entrance("D04Z02S04[N]", player),
        lambda state: (
            (
                state.has("D04Z02S04[NW]", player)
                or state.has("D04Z02S04[NE]", player)
                or state.has("D04Z02S04[Cherubs]", player)
                or state.has_all({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
            )
            and state.has("OpenedMOMLadder", player)
        ))


    # D04Z02S06 (Mother of Mothers)
    # Items
    set_rule(world.get_location("MoM: Outside Cleofas' room", player),
        lambda state: (
            state.has("D04Z02S06[NW]", player)
            or state.has("D04Z02S06[N]", player)
            or state.has("D04Z02S06[NE]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))
    # Doors
    set_rule(world.get_entrance("D04Z02S06[NW]", player),
        lambda state: (
            state.has("D04Z02S06[N]", player)
            or state.has("D04Z02S06[NE]", player)
            or state.has("Wall Climb Ability", player)
        ))
    set_rule(world.get_entrance("D04Z02S06[N]", player),
        lambda state: (
            (
                state.has("D04Z02S06[NW]", player)
                or state.has("D04Z02S06[NE]", player)
                or state.has("Wall Climb Ability", player)
            )
            and state.has("OpenedARLadder", player)
        ))
    set_rule(world.get_entrance("D04Z02S06[NE]", player),
        lambda state: (
            state.has("D04Z02S06[NW]", player)
            or state.has("D04Z02S06[N]", player)
            or state.has("Wall Climb Ability", player)
        ))
    set_rule(world.get_entrance("D04Z02S06[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    # Event
    set_rule(world.get_location("OpenedMOMLadder", player),
        lambda state: opened_mom_ladder(state, player))


    # D04Z02S07 (Mother of Mothers)
    # Items
    set_rule(world.get_location("MoM: East chandelier platform", player),
        lambda state: (
            state.has("Dash Ability", player)
            and (
                state.has("Blood Perpetuated in Sand", player)
                or can_cross_gap(state, logic, player, 3)
            )
        ))
    # No doors


    # D04Z02S09 (Mother of Mothers)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z02S09[NE]", player),
        lambda state: state.has("Blood Perpetuated in Sand", player))


    # D04Z02S16 (Mother of Mothers)
    # Items
    set_rule(world.get_location("MoM: Giant chandelier statue", player),
        lambda state: (
            state.has("Wall Climb Ability", player)
            and state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun"}, player)
        ))
    # Doors
    set_rule(world.get_entrance("D04Z02S16[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D04Z02S20 (Mother of Mothers)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z02S20[Redento]", player),
        lambda state: redento(state, blasphemousworld, player, 5))


    # D04Z02S21 (Mother of Mothers)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z02S21[W]", player),
        lambda state: (
            state.has("D04Z02S21[NE]", player)
            or state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)
        ))
    set_rule(world.get_entrance("D04Z02S21[NE]", player),
        lambda state: state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))


    # D04Z02S22 (Mother of Mothers)
    # Items
    set_rule(world.get_location("MoM: Melquiades, The Exhumed Archbishop", player),
        lambda state: can_beat_boss(state, "Mothers", logic, player))
    # Doors
    set_rule(world.get_entrance("D04Z02S22[W]", player),
        lambda state: can_beat_boss(state, "Mothers", logic, player))
    set_rule(world.get_entrance("D04Z02S22[E]", player),
        lambda state: can_beat_boss(state, "Mothers", logic, player))


    # D04BZ02S01 (Mother of Mothers - Redento)
    # Items
    set_rule(world.get_location("MoM: Final meeting with Redento", player),
        lambda state: redento(state, blasphemousworld, player, 5))
    # No doors


    # D04Z03S02 (Knot of the Three Words)
    # Items
    set_rule(world.get_location("KotTW: Gift from the Traitor", player),
        lambda state: state.has_all({"Severed Right Eye of the Traitor", "Broken Left Eye of the Traitor"}, player))
    # No doors


    # D04Z04S01 (All the Tears of the Sea)
    # Items
    set_rule(world.get_location("AtTotS: Miriam's gift", player),
        lambda state: (
            miriam(state, player)
            and state.has("Dash Ability", player)
            and state.has("Wall Climb Ability", player)
        ))
    # No doors


    # D05Z01S03 (Library of the Negated Words)
    # No items
    # Doors
    set_rule(world.get_entrance("D05Z01S03[Frontal]", player),
        lambda state: (
            state.has("Key Grown from Twisted Wood", player)
            and state.has("D05Z01S23[E]", player)
            and (
                state.has("D05Z01S11[NW]", player)
                or state.has("D05Z01S11[NE]", player)
            )
        ))


    # D05Z01S05 (Library of the Negated Words)
    # Items
    set_rule(world.get_location("LotNW: Hidden floor", player),
        lambda state: can_break_holes(state, player))
    set_rule(world.get_location("LotNW: Root ceiling platform", player),
        lambda state: (
            (
                can_climb_on_root(state, player)
                or state.has("Purified Hand of the Nun", player)
            )
            and (
                state.has("D05Z01S05[NE]", player)
                or state.has("Blood Perpetuated in Sand", player)
            )
        ))
    # Doors
    set_rule(world.get_entrance("D05Z01S05[NE]", player),
        lambda state: state.has("Blood Perpetuated in Sand", player))


    # D05Z01S06 (Library of the Negated Words)
    # Items
    set_rule(world.get_location("LotNW: Miasma hallway chest", player),
        lambda state: (
            state.has("D05Z01S06[W]", player)
            or can_survive_poison(state, logic, player, 3)
        ))
    # Doors
    set_rule(world.get_entrance("D05Z01S06[W]", player),
        lambda state: can_survive_poison(state, logic, player, 3))
    set_rule(world.get_entrance("D05Z01S06[E]", player),
        lambda state: can_survive_poison(state, logic, player, 3))


    # D05Z01S07 (Library of the Negated Words)
    # No items
    # Doors
    set_rule(world.get_entrance("D05Z01S07[NW]", player),
        lambda state: (
            state.has("Blood Perpetuated in Sand", player)
            and (
                can_climb_on_root(state, player)
                or state.has("Purified Hand of the Nun", player)
            )
            or (
                can_climb_on_root(state, player)
                and can_cross_gap(state, logic, player, 3)
            )
            or can_cross_gap(state, logic, player, 7)
        ))


    # D05Z01S10 (Library of the Negated Words)
    # Items
    set_rule(world.get_location("LotNW: Platform puzzle chest", player),
        lambda state: (
            state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun"}, player)
            or can_enemy_bounce(logic, enemy)
            and can_cross_gap(state, logic, player, 2)
        ))
    # No doors


    # D05Z01S11 (Library of the Negated Words)
    # Items
    set_rule(world.get_location("LotNW: Silence for Diosdado", player),
        lambda state: (
            (
                state.has("D05Z01S11[NW]", player)
                or state.has("D05Z01S11[NE]", player)
            )
            and state.has("D05Z01S23[E]", player)
        ))
    set_rule(world.get_location("LotNW: Lowest west upper ledge", player),
        lambda state: (
            state.has("D05Z01S11[NW]", player)
            or state.has("D05Z01S11[NE]", player)
        ))
    # Doors
    set_rule(world.get_entrance("D05Z01S11[SW]", player),
        lambda state: can_break_tirana(state, logic, player))
    set_rule(world.get_entrance("D05Z01S11[NW]", player),
        lambda state: state.has("D05Z01S11[NE]", player))
    set_rule(world.get_entrance("D05Z01S11[NE]", player),
        lambda state: state.has("D05Z01S11[NW]", player))


    # D05Z01S21 (Library of the Negated Words)
    # Items
    set_rule(world.get_location("LotNW: Elevator Child of Moonlight", player),
        lambda state: (
            state.has("Blood Perpetuated in Sand", player)
            and (
                can_walk_on_root(state, player)
                or state.has("Purified Hand of the Nun", player)
                or can_cross_gap(state, logic, player, 5)
                and pillar(state, player)
            )
            or obscure_skips_allowed(logic)
            and (
                state.has("Zarabanda of the Safe Haven", player)
                or aubade(state, player)
                or state.has("Cantina of the Blue Rose", player)
            )
        ))
    # Doors
    set_rule(world.get_entrance("D05Z01S21[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D05Z02S06 (The Sleeping Canvases)
    # No items
    # Doors
    set_rule(world.get_entrance("D05Z02S06[SE]", player),
        lambda state: state.has("OpenedTSCGate", player))


    # D05Z02S09 (The Sleeping Canvases)
    # No items
    # Doors
    set_rule(world.get_entrance("D05Z02S09[E]", player),
        lambda state: (
            state.has("Bead of Red Wax", player, 3)
            and state.has("Bead of Blue Wax", player, 3)
        ))


    # D05Z02S10 (The Sleeping Canvases)
    # Items
    set_rule(world.get_location("TSC: Jocinero's 1st reward", player),
        lambda state: state.has("Child of Moonlight", player, 20))
    set_rule(world.get_location("TSC: Jocinero's final reward", player),
        lambda state: state.has("Child of Moonlight", player, 38))
    # Doors
    set_rule(world.get_entrance("D05Z02S10[W]", player),
        lambda state: state.has("Dash Ability", player))
    

    # D05Z02S11 (The Sleeping Canvases)
    # Event
    set_rule(world.get_location("OpenedTSCGate", player),
        lambda state: opened_tsc_gate(state, player))


    # D05Z02S13 (The Sleeping Canvases)
    # No items
    # Doors
    set_rule(world.get_entrance("D05Z02S13[E]", player),
        lambda state: state.has("Dash Ability", player))


    # D05Z02S14 (The Sleeping Canvases)
    # Items
    set_rule(world.get_location("TSC: Exposito, Scion of Abjuration", player),
        lambda state: can_beat_boss(state, "Canvases", logic, player))
    # Doors
    set_rule(world.get_entrance("D05Z02S14[W]", player),
        lambda state: can_beat_boss(state, "Canvases", logic, player))
    set_rule(world.get_entrance("D05Z02S14[E]", player),
        lambda state: can_beat_boss(state, "Canvases", logic, player))


    # D05Z02S15 (The Sleeping Canvases)
    # Items
    set_rule(world.get_location("TSC: Swinging blade tunnel", player),
        lambda state: state.has("Dash Ability", player))
    # No doors


    # D06Z01S01 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S01[SW]", player),
        lambda state: (
            (
                state.has("D06Z01S01[SE]", player)
                or state.has("D06Z01S01[W]", player)
                or state.has("D06Z01S01[E]", player)
                or state.has("D06Z01S01[NNW]", player)
                or state.has("D06Z01S01[NNE]", player)
                or state.has("D06Z01S01[N]", player)
            )
            or state.has("Linen of Golden Thread", player)
            and (
                state.has("D06Z01S01[NW]", player)
                or state.has("D06Z01S01[NE]", player)
            )
        ))
    set_rule(world.get_entrance("D06Z01S01[SE]", player),
        lambda state: (
            (
                state.has("D06Z01S01[SW]", player)
                or state.has("D06Z01S01[W]", player)
                or state.has("D06Z01S01[E]", player)
                or state.has("D06Z01S01[NNW]", player)
                or state.has("D06Z01S01[NNE]", player)
                or state.has("D06Z01S01[N]", player)
            )
            or state.has("Linen of Golden Thread", player)
            and (
                state.has("D06Z01S01[NW]", player)
                or state.has("D06Z01S01[NE]", player)
            )
        ))
    set_rule(world.get_entrance("D06Z01S01[W]", player),
        lambda state: (
            (
                state.has("D06Z01S01[E]", player)
                or state.has("D06Z01S01[NNW]", player)
                or state.has("D06Z01S01[NNE]", player)
                or state.has("D06Z01S01[N]", player)
            )
            or state.has_group("masks", player, 1)
            and (
                state.has("D06Z01S01[SW]", player)
                or state.has("D06Z01S01[SE]", player)
            )
            or state.has("Linen of Golden Thread", player)
            and (
                state.has("D06Z01S01[NW]", player)
                or state.has("D06Z01S01[NE]", player)
                and (
                    can_walk_on_root(state, player)
                    or can_cross_gap(state, logic, player, 1)
                )
            )
        ))
    set_rule(world.get_entrance("D06Z01S01[E]", player),
        lambda state: (
            (
                state.has("D06Z01S01[W]", player)
                or state.has("D06Z01S01[NNW]", player)
                or state.has("D06Z01S01[NNE]", player)
                or state.has("D06Z01S01[N]", player)
            )
            or state.has_group("masks", player, 1)
            and (
                state.has("D06Z01S01[SW]", player)
                or state.has("D06Z01S01[SE]", player)
            )
            or state.has("Linen of Golden Thread", player)
            and (
                state.has("D06Z01S01[NW]", player)
                or state.has("D06Z01S01[NE]", player)
                and (
                    can_walk_on_root(state, player)
                    or can_cross_gap(state, logic, player, 1)
                )
            )
        ))
    set_rule(world.get_entrance("D06Z01S01[NW]", player),
        lambda state: (
            state.has("D06Z01S01[NE]", player)
            and (
                can_walk_on_root(state, player)
                or can_cross_gap(state, logic, player, 8)
            )
            or state.has("Linen of Golden Thread", player)
            and (
                state.has("D06Z01S01[NNW]", player)
                or state.has("D06Z01S01[NNE]", player)
                and (
                    can_walk_on_root(state, player)
                    or can_cross_gap(state, logic, player, 3)
                )
            )
        ))
    set_rule(world.get_entrance("D06Z01S01[NE]", player),
        lambda state: (
            state.has("D06Z01S01[NW]", player)
            or (
                can_walk_on_root(state, player)
                or can_cross_gap(state, logic, player, 8)
            )
            or state.has("Linen of Golden Thread", player)
            and (
                state.has("D06Z01S01[NNW]", player)
                or state.has("D06Z01S01[NNE]", player)
                and (
                    can_walk_on_root(state, player)
                    or can_cross_gap(state, logic, player, 3)
                )
            )
        ))
    set_rule(world.get_entrance("D06Z01S01[NNW]", player),
        lambda state: (
            (
                state.has("D06Z01S01[NNE]", player)
                or state.has("D06Z01S01[N]", player)
            )
            or state.has_group("masks", player, 2)
            and (
                state.has("D06Z01S01[SW]", player)
                or state.has("D06Z01S01[SE]", player)
                or state.has("D06Z01S01[W]", player)
                or state.has("D06Z01S01[E]", player)
                or state.has("Linen of Golden Thread", player)
                and (
                    state.has("D06Z01S01[NW]", player)
                    or state.has("D06Z01S01[NE]", player)
                )
            )
        ))
    set_rule(world.get_entrance("D06Z01S01[NNE]", player),
        lambda state: (
            (
                state.has("D06Z01S01[NNW]", player)
                or state.has("D06Z01S01[N]", player)
            )
            or state.has_group("masks", player, 2)
            and (
                state.has("D06Z01S01[SW]", player)
                or state.has("D06Z01S01[SE]", player)
                or state.has("D06Z01S01[W]", player)
                or state.has("D06Z01S01[E]", player)
                or state.has("Linen of Golden Thread", player)
                and (
                    state.has("D06Z01S01[NW]", player)
                    or state.has("D06Z01S01[NE]", player)
                )
            )
        ))
    set_rule(world.get_entrance("D06Z01S01[N]", player),
        lambda state: (
            state.has_group("masks", player, 3)
            and (
                state.has("D06Z01S01[SW]", player)
                or state.has("D06Z01S01[SE]", player)
                or state.has("D06Z01S01[W]", player)
                or state.has("D06Z01S01[E]", player)
                or state.has("D06Z01S01[NNW]", player)
                or state.has("D06Z01S01[NNE]", player)
                or state.has("Linen of Golden Thread", player)
                and (
                    state.has("D06Z01S01[NW]", player)
                    or state.has("D06Z01S01[NE]", player)
                )
            )
        ))
    set_rule(world.get_entrance("D06Z01S01[-Cherubs]", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            and (
                state.has("D06Z01S01[SW]", player)
                or state.has("D06Z01S01[SE]", player)
                or state.has("D06Z01S01[W]", player)
                or state.has("D06Z01S01[E]", player)
                or state.has("D06Z01S01[NW]", player)
                or state.has("D06Z01S01[NE]", player)
                or state.has("D06Z01S01[NNW]", player)
                or state.has("D06Z01S01[NNE]", player))
        ))


    # D06Z01S03 (Archcathedral Rooftops)
    # Items
    set_rule(world.get_location("AR: First soldier fight", player),
        lambda state: can_beat_boss(state, "Legionary", logic, player))
    # Doors
    set_rule(world.get_entrance("D06Z01S03[W]", player),
        lambda state: can_beat_boss(state, "Legionary", logic, player))
    set_rule(world.get_entrance("D06Z01S03[E]", player),
        lambda state: can_beat_boss(state, "Legionary", logic, player))


    # D06Z01S04 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S04[SW]", player),
        lambda state: (
            state.has("D06Z01S04[W]", player)
            or state.has("D06Z01S04[Health]", player)
        ))
    set_rule(world.get_entrance("D06Z01S04[W]", player),
        lambda state: (
            state.has("D06Z01S04[SW]", player)
            or state.has("D06Z01S04[Health]", player)
        ))
    set_rule(world.get_entrance("D06Z01S04[Health]", player),
        lambda state: (
            state.has("D06Z01S04[SW]", player)
            or state.has("D06Z01S04[W]", player)
        ))
    add_rule(world.get_entrance("D06Z01S04[Health]", player),
        lambda state: (
            (
                state.has("Wall Climb Ability", player)
                and can_survive_poison(state, logic, player, 2)
                and (
                    state.has("Purified Hand of the Nun", player)
                    or (
                        state.has("Blood Perpetuated in Sand", player)
                        and can_climb_on_root(state, player)
                    )
                )
            )
        ))
    set_rule(world.get_entrance("D06Z01S04[NW]", player),
        lambda state: (
            state.has("D06Z01S04[NE]", player)
            or state.has("D06Z01S04[Cherubs]", player)
        ))
    add_rule(world.get_entrance("D06Z01S04[NW]", player),
        lambda state: (
            state.has("D06Z01S04[Cherubs]", player)
            or (
                state.has("D06Z01S04[SW]", player)
                or state.has("D06Z01S04[W]", player)
                or state.has("D06Z01S04[Health]", player)
            )
            and state.has("Wall Climb Ability", player)
            and can_survive_poison(state, logic, player, 2)
            and (
                state.has_any({"Dash Ability", "Purified Hand of the Nun"}, player)
                and (
                    can_dawn_jump(state, logic, player)
                    or can_climb_on_root(state, player)
                )
            )
        ))
    set_rule(world.get_entrance("D06Z01S04[NE]", player),
        lambda state: (
            state.has("D06Z01S04[NW]", player)
            or state.has("D06Z01S04[Cherubs]", player)
        ))
    add_rule(world.get_entrance("D06Z01S04[NE]", player),
        lambda state: (
            (
                state.has("D06Z01S04[SW]", player)
                or state.has("D06Z01S04[W]", player)
                or state.has("D06Z01S04[Health]", player)
            )
            and state.has("Wall Climb Ability", player)
            and can_survive_poison(state, logic, player, 2)
            and (
                state.has_any({"Dash Ability", "Purified Hand of the Nun"}, player)
                and (
                    can_dawn_jump(state, logic, player)
                    or can_climb_on_root(state, player)
                )
            )
        ))


    # D06Z01S06 (Archcathedral Rooftops)
    # Items
    set_rule(world.get_location("AR: Second soldier fight", player),
        lambda state: (
            can_beat_boss(state, "Legionary", logic, player)
            and (
                state.has("D06Z01S06[WW]", player)
                or state.has("D06Z01S06[E]", player)
            )
        ))
    # Doors
    set_rule(world.get_entrance("D06Z01S06[WW]", player),
        lambda state: state.has("D06Z01S06[E]", player))
    add_rule(world.get_entrance("D06Z01S06[WW]", player),
        lambda state: can_beat_boss(state, "Legionary", logic, player))
    set_rule(world.get_entrance("D06Z01S06[E]", player),
        lambda state: state.has("D06Z01S06[WW]", player))
    add_rule(world.get_entrance("D06Z01S06[E]", player),
        lambda state: can_beat_boss(state, "Legionary", logic, player))
    set_rule(world.get_entrance("D06Z01S06[W]", player),
        lambda state: state.has("D06Z01S06[EE]", player))
    set_rule(world.get_entrance("D06Z01S06[EE]", player),
        lambda state: state.has("D06Z01S06[W]", player))


    # D06Z01S08 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S08[E]", player),
        lambda state: state.has("D06Z01S08[N]", player) or \
            state.has("Wall Climb Ability", player))


    # D06Z01S09 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S09[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D06Z01S09[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D06Z01S10 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S10[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D06Z01S10[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D06Z01S12 (Archcathedral Rooftops)
    # Items
    set_rule(world.get_location("AR: Upper west shaft ledge", player),
        lambda state: (
            state.has("D06Z01S12[NW]", player)
            or state.has("D06Z01S12[NE]", player)
            or state.has("D06Z01S12[NE2]", player)
            or state.has("D06Z01S12[W]", player)
            or state.has("D06Z01S12[E]", player)
            or state.has("Wall Climb Ability", player)
        ))
    set_rule(world.get_location("AR: Upper west shaft chest", player),
        lambda state: (
            state.has("D06Z01S12[NE2]", player)
            or (
                state.has("D06Z01S12[NW]", player)
                or state.has("D06Z01S12[NE]", player)
            )
            and state.has("Purified Hand of the Nun", player)
        ))
    set_rule(world.get_location("AR: Upper west shaft Child of Moonlight", player),
        lambda state: (
            state.has("D06Z01S12[W]", player)
            or state.has("D06Z01S12[E]", player)
            or state.has("D06Z01S12[NW]", player)
            or state.has("D06Z01S12[NE]", player)
            or state.has("D06Z01S12[NE2]", player)
            or state.has("Wall Climb Ability", player)
            and state.has_any({"Purified Hand of the Nun", "Taranto to my Sister"}, player)
        ))
    # Doors
    set_rule(world.get_entrance("D06Z01S12[W]", player),
        lambda state: (
            state.has("D06Z01S12[NW]", player)
            or state.has("D06Z01S12[NE]", player)
            or state.has("D06Z01S12[NE2]", player)
            or state.has("D06Z01S12[E]", player)
            or state.has_all({"Wall Climb Ability", "Purified Hand of the Nun"}, player)
        ))
    set_rule(world.get_entrance("D06Z01S12[E]", player),
        lambda state: (
            state.has("D06Z01S12[NW]", player)
            or state.has("D06Z01S12[NE]", player)
            or state.has("D06Z01S12[NE2]", player)
            or state.has("D06Z01S12[W]", player)
            or state.has_all({"Wall Climb Ability", "Purified Hand of the Nun"}, player)
        ))
    set_rule(world.get_entrance("D06Z01S12[NW]", player),
        lambda state: (
            state.has("D06Z01S12[NE]", player)
            or state.has("D06Z01S12[NE2]", player)
        ))
    add_rule(world.get_entrance("D06Z01S12[NW]", player),
        lambda state: (
            state.has("D06Z01S12[NE]", player)
            or state.has_any({"Wall Climb Ability", "Purified Hand of the Nun"}, player)
        ))
    set_rule(world.get_entrance("D06Z01S12[NE]", player),
        lambda state: (
            state.has("D06Z01S12[NW]", player)
            or state.has("D06Z01S12[NE2]", player)
        ))
    add_rule(world.get_entrance("D06Z01S12[NE]", player),
        lambda state: (
            state.has("D06Z01S12[NW]", player)
            or state.has_any({"Wall Climb Ability", "Purified Hand of the Nun"}, player)
        ))


    # D06Z01S15 (Archcathedral Rooftops)
    # Items
    set_rule(world.get_location("AR: Upper east shaft ledge", player),
        lambda state: (
            state.has("D06Z01S15[SW]", player)
            and state.has("Wall Climb Ability", player)
            and (
                can_cross_gap(state, logic, player, 10)
                or can_climb_on_root(state, player)
                and (
                    state.has("Blood Perpetuated in Sand", player)
                    or state.has("Purified Hand of the Nun", player)
                    and can_air_stall(state, logic, player)
                )
            )
        ))
    # Doors
    set_rule(world.get_entrance("D06Z01S15[NW]", player),
        lambda state: state.has("D06Z01S15[NE]", player))
    add_rule(world.get_entrance("D06Z01S15[NW]", player),
        lambda state: (
            state.has("D06Z01S15[SW]", player)
            or state.has("Wall Climb Ability", player)
        ))
    set_rule(world.get_entrance("D06Z01S15[NE]", player),
        lambda state: state.has("D06Z01S15[NW]", player))
    add_rule(world.get_entrance("D06Z01S15[NE]", player),
        lambda state: (
            state.has("D06Z01S15[SW]", player)
            or state.has("Wall Climb Ability", player)
        ))


    # D06Z01S16 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S16[W]", player),
        lambda state: (
            (
                state.has("D06Z01S16[CherubsL]", player)
                and (
                    state.has("Purified Hand of the Nun", player)
                    or state.has("Wall Climb Ability", player)
                    and (
                        can_walk_on_root(state, player)
                        or can_air_stall(state, logic, player)
                    )
                )
            )
            or (
                state.has("D06Z01S16[CherubsR]", player)
                and (
                    state.has("Purified Hand of the Nun", player)
                    or can_air_stall(state, logic, player)
                    and (
                        can_walk_on_root(state, player)
                        or state.has("The Young Mason's Wheel", player)
                    )
                    and (
                        state.has("Wall Climb Ability", player)
                        or can_dawn_jump(state, logic, player)
                    )
                )
            )
            or (
                state.has("D06Z01S16[E]", player)
                and (
                    can_walk_on_root(state, player)
                    or can_cross_gap(state, logic, player, 7)
                )
                and (
                    state.has("Wall Climb Ability", player) or 
                    can_cross_gap(state, logic, player, 5)
                )
            )
        ))
    set_rule(world.get_entrance("D06Z01S16[E]", player),
        lambda state: (
            (
                (
                    state.has("D06Z01S16[W]", player)
                    or state.has("D06Z01S16[CherubsL]", player)
                )
                and (
                    can_walk_on_root(state, player)
                    or can_cross_gap(state, logic, player, 5)
                )
            )
            or (
                state.has("D06Z01S16[CherubsR]", player)
                and (
                    state.has("Purified Hand of the Nun", player)
                    or can_air_stall(state, logic, player)
                    and (
                        can_walk_on_root(state, player)
                        and state.has("The Young Mason's Wheel", player)
                    )
                )
            )
        ))
    set_rule(world.get_entrance("D06Z01S16[-CherubsL]", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            and (
                state.has("D06Z01S16[W]", player)
                or (
                    state.has("D06Z01S16[CherubsR]", player)
                    and (
                        state.has("Purified Hand of the Nun", player)
                        or can_air_stall(state, logic, player)
                        and (
                            can_walk_on_root(state, player)
                            or state.has("The Young Mason's Wheel", player)
                        )
                    )
                )
                or (
                    state.has("D06Z01S16[E]", player)
                    and (
                        can_walk_on_root(state, player)
                        or can_cross_gap(state, logic, player, 7)
                    )
                )
            )
        ))
    set_rule(world.get_entrance("D06Z01S16[-CherubsR]", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            and (
                state.has("D06Z01S16[E]", player)
                or (
                    state.has("D06Z01S16[CherubsL]", player)
                    and (
                        can_air_stall(state, logic, player)
                        or can_walk_on_root(state, player)
                        or state.has("Purified Hand of the Nun", player)
                    )
                )
                or (
                    state.has("D06Z01S16[W]", player)
                    and (
                        can_walk_on_root(state, player)
                        or can_cross_gap(state, logic, player, 1)
                    )
                )
            )
        ))


    # D06Z01S17 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S17[W]", player),
        lambda state: (
            (
                state.has("D06Z01S17[E]", player)
                or state.has("D06Z01S17[CherubsR]", player)
            )
            and state.has("Blood Perpetuated in Sand", player)
            or state.has("D06Z01S17[CherubsL]", player)
            and state.has("Purified Hand of the Nun", player)
        ))
    set_rule(world.get_entrance("D06Z01S17[E]", player),
        lambda state: (
            state.has("D06Z01S17[CherubsR]", player)
            or state.has("Blood Perpetuated in Sand", player)
            and (
                state.has("D06Z01S17[W]", player)
                or state.has("D06Z01S17[CherubsL]", player)
                and state.has("Purified Hand of the Nun", player)
            )
        ))
    set_rule(world.get_entrance("D06Z01S17[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D06Z01S18 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S18[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))

    # D06Z01S21 (Archcathedral Rooftops)
    # Items
    set_rule(world.get_location("AR: Third soldier fight", player),
        lambda state: can_beat_boss(state, "Legionary", logic, player))
    # Doors
    set_rule(world.get_entrance("D06Z01S21[W]", player),
        lambda state: can_beat_boss(state, "Legionary", logic, player))
    set_rule(world.get_entrance("D06Z01S21[E]", player),
        lambda state: can_beat_boss(state, "Legionary", logic, player))
    

    # D06Z01S23 (Archcathedral Rooftops)
    # Event
    set_rule(world.get_location("OpenedARLadder", player),
        lambda state: opened_ar_ladder(state, player))


    # D06Z01S25 (Archcathedral Rooftops)
    # Items
    set_rule(world.get_location("AR: Crisanta of the Wrapped Agony", player),
        lambda state: can_beat_boss(state, "Rooftops", logic, player))
    # Doors
    set_rule(world.get_entrance("D06Z01S25[W]", player),
        lambda state: can_beat_boss(state, "Rooftops", logic, player))
    set_rule(world.get_entrance("D06Z01S25[E]", player),
        lambda state: can_beat_boss(state, "Rooftops", logic, player))


    # D08Z01S01 (Bridge of the Three Cavalries)
    # Items
    set_rule(world.get_location("BotTC: Esdras, of the Anointed Legion", player),
        lambda state: (
            state.has_group("wounds", player, 3)
            and can_beat_boss(state, "Bridge", logic, player)
        ))
    set_rule(world.get_location("BotTC: Esdras' gift", player),
        lambda state: (
            state.has_group("wounds", player, 3)
            and can_beat_boss(state, "Bridge", logic, player)
        ))
    # Doors
    set_rule(world.get_entrance("D08Z01S01[W]", player),
        lambda state: can_beat_boss(state, "Bridge", logic, player))
    set_rule(world.get_entrance("D08Z01S01[E]", player),
        lambda state: (
            state.has_group("wounds", player, 3)
            and (
                state.has("D08Z01S01[Cherubs]", player)
                or can_beat_boss(state, "Bridge", logic, player)
            )
        ))


    # D08Z01S02 (Bridge of the Three Cavalries)
    # No items
    # Items
    set_rule(world.get_entrance("D08Z01S02[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    # Event
    set_rule(world.get_location("BrokeBOTTCStatue", player),
        lambda state: broke_bottc_statue(state, player))


    # D08Z02S03 (Ferrous Tree)
    # No items
    # Doors
    set_rule(world.get_entrance("D08Z02S03[W]", player),
        lambda state: state.has("OpenedBOTTCStatue", player))


    # D08Z03S01 (Hall of the Dawning)
    # No items
    # Doors
    set_rule(world.get_entrance("D08Z03S01[E]", player),
        lambda state: state.has("Verses Spun from Gold", player, 4))


    # D08Z03S02 (Hall of the Dawning)
    # No items
    # Doors
    set_rule(world.get_entrance("D08Z03S02[NW]", player),
        lambda state: state.has("Wall Climb Ability", player))


    # D08Z03S03 (Hall of the Dawning)
    # Items
    set_rule(world.get_location("HotD: Laudes, the First of the Amanecidas", player),
        lambda state: can_beat_boss(state, "Hall", logic, player))
    # Doors
    set_rule(world.get_entrance("D08Z03S03[W]", player),
        lambda state: can_beat_boss(state, "Hall", logic, player))
    set_rule(world.get_entrance("D08Z03S03[E]", player),
        lambda state: can_beat_boss(state, "Hall", logic, player))


    # D09Z01S01 (Wall of the Holy Prohibitions)
    # Items
    set_rule(world.get_location("WotHP: Amanecida of the Molten Thorn", player),
        lambda state: can_beat_boss(state, "Wall", logic, player))
    # No doors


    # D09Z01S02 (Wall of the Holy Prohibitions)
    # Items
    set_rule(world.get_location("WotHP: Upper east room, center gold cell", player),
        lambda state: state.has("D09Z01S02[Cell5]", player))
    set_rule(world.get_location("WotHP: Upper east room, lift puzzle", player),
        lambda state: (
            state.has("D09Z01S02[NW]", player)
            or state.has("D09Z01S02[N]", player)
            or state.has("D09Z01S02[Cell1]", player)
            or state.has("D09Z01S02[Cell6]", player)
            or state.has("D09Z01S02[Cell4]", player)
            or state.has("D09Z01S02[Cell3]", player)
            or state.has("D09Z01S02[Cell22]", player)
            or state.has("D09Z01S02[Cell23]", player)
        ))
    # Doors
    set_rule(world.get_entrance("D09Z01S02[SW]", player),
        lambda state: state.has("D09Z01S02[Cell2]", player))
    set_rule(world.get_entrance("D09Z01S02[NW]", player),
        lambda state: (
            state.has("D09Z01S02[N]", player)
            or state.has("D09Z01S02[Cell1]", player)
            or state.has("D09Z01S02[Cell6]", player)
            or state.has("D09Z01S02[Cell4]", player)
            or state.has("D09Z01S02[Cell3]", player)
            or state.has("D09Z01S02[Cell22]", player)
            or state.has("D09Z01S02[Cell23]", player)
        ))
    set_rule(world.get_entrance("D09Z01S02[N]", player),
        lambda state: (
            state.has("D09Z01S02[NW]", player)
            or state.has("D09Z01S02[Cell1]", player)
            or state.has("D09Z01S02[Cell6]", player)
            or state.has("D09Z01S02[Cell4]", player)
            or state.has("D09Z01S02[Cell3]", player)
            or state.has("D09Z01S02[Cell22]", player)
            or state.has("D09Z01S02[Cell23]", player)
        ))
    set_rule(world.get_entrance("D09Z01S02[Cell1]", player),
        lambda state: (
            state.has("D09Z01S02[NW]", player)
            or state.has("D09Z01S02[N]", player)
            or state.has("D09Z01S02[Cell6]", player)
            or state.has("D09Z01S02[Cell4]", player)
            or state.has("D09Z01S02[Cell3]", player)
            or state.has("D09Z01S02[Cell22]", player)
            or state.has("D09Z01S02[Cell23]", player)
        ))
    add_rule(world.get_entrance("D09Z01S02[Cell1]", player),
        lambda state: state.has("Key of the Secular", player))
    set_rule(world.get_entrance("D09Z01S02[Cell6]", player),
        lambda state: (
            state.has("D09Z01S02[NW]", player)
            or state.has("D09Z01S02[N]", player)
            or state.has("D09Z01S02[Cell1]", player)
            or state.has("D09Z01S02[Cell4]", player)
            or state.has("D09Z01S02[Cell3]", player)
            or state.has("D09Z01S02[Cell22]", player)
            or state.has("D09Z01S02[Cell23]", player)
        ))
    add_rule(world.get_entrance("D09Z01S02[Cell6]", player),
        lambda state: state.has("Key of the Scribe", player))
    set_rule(world.get_entrance("D09Z01S02[Cell4]", player),
        lambda state: (
            state.has("D09Z01S02[NW]", player)
            or state.has("D09Z01S02[N]", player)
            or state.has("D09Z01S02[Cell1]", player)
            or state.has("D09Z01S02[Cell6]", player)
            or state.has("D09Z01S02[Cell3]", player)
            or state.has("D09Z01S02[Cell22]", player)
            or state.has("D09Z01S02[Cell23]", player)
        ))
    add_rule(world.get_entrance("D09Z01S02[Cell4]", player),
        lambda state: state.has("Key of the Inquisitor", player))
    set_rule(world.get_entrance("D09Z01S02[Cell2]", player),
        lambda state: state.has("D09Z01S02[SW]", player))
    set_rule(world.get_entrance("D09Z01S02[Cell3]", player),
        lambda state: (
            state.has("D09Z01S02[NW]", player)
            or state.has("D09Z01S02[N]", player)
            or state.has("D09Z01S02[Cell1]", player)
            or state.has("D09Z01S02[Cell6]", player)
            or state.has("D09Z01S02[Cell4]", player)
            or state.has("D09Z01S02[Cell22]", player)
            or state.has("D09Z01S02[Cell23]", player)
        ))
    add_rule(world.get_entrance("D09Z01S02[Cell3]", player),
        lambda state: state.has("Key of the Secular", player))
    set_rule(world.get_entrance("D09Z01S02[Cell22]", player),
        lambda state: (
            state.has("D09Z01S02[NW]", player)
            or state.has("D09Z01S02[N]", player)
            or state.has("D09Z01S02[Cell1]", player)
            or state.has("D09Z01S02[Cell6]", player)
            or state.has("D09Z01S02[Cell4]", player)
            or state.has("D09Z01S02[Cell3]", player)
            or state.has("D09Z01S02[Cell23]", player)
        ))
    set_rule(world.get_entrance("D09Z01S02[Cell23]", player),
        lambda state: (
            state.has("D09Z01S02[NW]", player)
            or state.has("D09Z01S02[N]", player)
            or state.has("D09Z01S02[Cell1]", player)
            or state.has("D09Z01S02[Cell6]", player)
            or state.has("D09Z01S02[Cell4]", player)
            or state.has("D09Z01S02[Cell3]", player)
            or state.has("D09Z01S02[Cell22]", player)
        ))
    add_rule(world.get_entrance("D09Z01S02[Cell23]", player),
        lambda state: state.has("Key of the Secular", player))


    # D09Z01S03 (Wall of the Holy Prohibitions)
    # Items
    set_rule(world.get_location("WotHP: Quirce, Returned By The Flames", player),
        lambda state: can_beat_boss(state, "Prison", logic, player))
    # Doors
    set_rule(world.get_entrance("D09Z01S03[W]", player),
        lambda state: (
            state.has("D09Z01S03[N]", player)
            and can_beat_boss(state, "Prison", logic, player)
        ))
    

    # D09Z01S05 (Wall of the Holy Prohibitions)
    # Event
    set_rule(world.get_location("OpenedWOTHPGate", player),
        lambda state: opened_wothp_gate(state, player))


    # D09Z01S06 (Wall of the Holy Prohibitions)
    # No items
    # Doors
    set_rule(world.get_entrance("D09Z01S06[-E]", player),
        lambda state: state.has("Key of the High Peaks", player))


    # D09Z01S07 (Wall of the Holy Prohibitions)
    # No items
    # Doors
    set_rule(world.get_entrance("D09Z01S07[SW]", player),
        lambda state: (
            state.has("D09Z01S07[SE]", player)
            or state.has("D09Z01S07[W]", player)
            or state.has("D09Z01S07[E]", player)
        ))
    set_rule(world.get_entrance("D09Z01S07[SE]", player),
        lambda state: (
            state.has("D09Z01S07[SW]", player)
            or state.has("D09Z01S07[W]", player)
            or state.has("D09Z01S07[E]", player)
        ))
    set_rule(world.get_entrance("D09Z01S07[W]", player),
        lambda state: (
            state.has("D09Z01S07[SW]", player)
            or state.has("D09Z01S07[SE]", player)
            or state.has("D09Z01S07[E]", player)
        ))
    set_rule(world.get_entrance("D09Z01S07[E]", player),
        lambda state: (
            state.has("D09Z01S07[SW]", player)
            or state.has("D09Z01S07[SE]", player)
            or state.has("D09Z01S07[W]", player)
        ))
    set_rule(world.get_entrance("D09Z01S07[NW]", player),
        lambda state: state.has("D09Z01S07[N]", player))
    set_rule(world.get_entrance("D09Z01S07[N]", player),
        lambda state: state.has("D09Z01S07[NW]", player))
    set_rule(world.get_entrance("D09Z01S07[NE]", player),
        lambda state: (
            state.has("D09Z01S07[SW]", player)
            or state.has("D09Z01S07[SE]", player)
            or state.has("D09Z01S07[W]", player)
            or state.has("D09Z01S07[E]", player)
        ))
    add_rule(world.get_entrance("D09Z01S07[NE]", player),
        lambda state: state.has("Blood Perpetuated in Sand", player))


    # D09Z01S08 (Wall of the Holy Prohibitions)
    # Items
    set_rule(world.get_location("WotHP: Collapsing floor ledge", player),
        lambda state: (
            (
                state.has("D09Z01S08[W]", player)
                or state.has("D09Z01S08[Cell18]", player)
            )
            and state.has("OpenedWOTHPGate", player)
        ))
    # Doors
    set_rule(world.get_entrance("D09Z01S08[W]", player),
        lambda state: state.has("D09Z01S08[Cell14]", player))
    add_rule(world.get_entrance("D09Z01S08[W]", player),
        lambda state: state.has("OpenedWOTHPGate", player))
    set_rule(world.get_entrance("D09Z01S08[S]", player),
        lambda state: (
            state.has("D09Z01S08[W]", player)
            or state.has("D09Z01S08[Cell14]", player)
        ))
    set_rule(world.get_entrance("D09Z01S08[SE]", player),
        lambda state: (
            state.has("D09Z01S08[Cell15]", player)
            or state.has("D09Z01S08[Cell16]", player)
            or state.has("D09Z01S08[Cell18]", player)
            or state.has("D09Z01S08[Cell17]", player)
            and state.has("Dash Ability", player)
        ))
    set_rule(world.get_entrance("D09Z01S08[NE]", player),
        lambda state: (
            state.has("D09Z01S08[Cell7]", player)
            or state.has("D09Z01S08[Cell17]", player)
            and state.has("Dash Ability", player)
        ))
    set_rule(world.get_entrance("D09Z01S08[Cell14]", player),
        lambda state: state.has("D09Z01S08[W]", player))
    set_rule(world.get_entrance("D09Z01S08[Cell15]", player),
        lambda state: (
            state.has("Key of the Scribe", player)
            and (
                state.has("D09Z01S08[SE]", player)
                or state.has("D09Z01S08[Cell16]", player)
                or state.has("D09Z01S08[Cell18]", player)
                or state.has("D09Z01S08[Cell17]", player)
                and state.has("Dash Ability", player)
            )
        ))
    set_rule(world.get_entrance("D09Z01S08[Cell7]", player),
        lambda state: (
            state.has("Key of the Inquisitor", player)
            and (
                state.has("D09Z01S08[NE]", player)
                or state.has("D09Z01S08[Cell17]", player)
                and state.has("Dash Ability", player)
            )
        ))
    set_rule(world.get_entrance("D09Z01S08[Cell16]", player),
        lambda state: (
            state.has("Key of the Inquisitor", player)
            and (
                state.has("D09Z01S08[SE]", player)
                or state.has("D09Z01S08[Cell15]", player)
                or state.has("D09Z01S08[Cell18]", player)
                or state.has("D09Z01S08[Cell17]", player)
                and state.has("Dash Ability", player)
            )
        ))
    set_rule(world.get_entrance("D09Z01S08[Cell18]", player),
        lambda state: (
            state.has("Key of the Scribe", player)
            and (
                state.has("D09Z01S08[SE]", player)
                or state.has("D09Z01S08[Cell15]", player)
                or state.has("D09Z01S08[Cell16]", player)
                or state.has("D09Z01S08[Cell17]", player)
                and state.has("Dash Ability", player)
            )
        ))


    # D09Z01S09 (Wall of the Holy Prohibitions)
    # Items
    set_rule(world.get_location("WotHP: Lower west room, top ledge", player),
        lambda state: (
            state.has("D09Z01S09[Cell24]", player)
            or state.has("Dash Ability", player)
            and (
                state.has("D09Z01S09[NW]", player)
                or state.has("D09Z01S09[Cell19]", player)
                or state.has("Purified Hand of the Nun", player)
                and (
                    can_air_stall(state, logic, player)
                    or can_dawn_jump(state, logic, player)
                )
            )
        ))
    # Doors
    set_rule(world.get_entrance("D09Z01S09[SW]", player),
        lambda state: (
            state.has("D09Z01S09[Cell21]", player)
            or state.has("D09Z01S09[Cell20]", player)
            or state.has("D09Z01S09[E]", player)
            or state.has("Dash Ability", player)
        ))
    set_rule(world.get_entrance("D09Z01S09[NW]", player),
        lambda state: (
            state.has("D09Z01S09[Cell19]", player)
            or state.has("D09Z01S09[Cell24]", player)
        ))
    add_rule(world.get_entrance("D09Z01S09[NW]", player),
        lambda state: (
            state.has("D09Z01S09[Cell19]", player)
            or state.has("Dash Ability", player)
            and (
                state.has("D09Z01S09[Cell24]", player)
                or state.has("Purified Hand of the Nun", player)
                and (
                    can_air_stall(state, logic, player)
                    or can_dawn_jump(state, logic, player)
                )
            )
        ))
    set_rule(world.get_entrance("D09Z01S09[E]", player),
        lambda state: (
            state.has("D09Z01S09[Cell21]", player)
            or state.has("D09Z01S09[Cell20]", player)
            or state.has("D09Z01S09[SW]", player)
            or state.has("Dash Ability", player)
        ))
    set_rule(world.get_entrance("D09Z01S09[Cell24]", player),
        lambda state: (
            state.has("D09Z01S09[NW]", player)
            or state.has("D09Z01S09[Cell19]", player)
        ))
    add_rule(world.get_entrance("D09Z01S09[Cell24]", player),
        lambda state: (
            state.has("Dash Ability", player)
            and (
                state.has("D09Z01S09[NW]", player)
                or state.has("D09Z01S09[Cell19]", player)
                or state.has("Purified Hand of the Nun", player)
                and (
                    can_air_stall(state, logic, player)
                    or can_dawn_jump(state, logic, player)
                )
            )
        ))
    set_rule(world.get_entrance("D09Z01S09[Cell19]", player),
        lambda state: (
            state.has("D09Z01S09[NW]", player)
            or state.has("D09Z01S09[Cell24]", player)
        ))
    add_rule(world.get_entrance("D09Z01S09[Cell19]", player),
        lambda state: (
            state.has("D09Z01S09[NW]", player)
            or state.has("Dash Ability", player)
            and (
                state.has("D09Z01S09[Cell24]", player)
                or state.has("Purified Hand of the Nun", player)
                and (
                    can_air_stall(state, logic, player)
                    or can_dawn_jump(state, logic, player)
                )
            )
        ))
    set_rule(world.get_entrance("D09Z01S09[Cell20]", player),
        lambda state: (
            state.has("Key of the Scribe", player)
            and (
                state.has("D09Z01S09[Cell21]", player)
                or state.has("D09Z01S09[SW]", player)
                or state.has("D09Z01S09[E]", player)
                or state.has("Dash Ability", player)
            )
        ))
    set_rule(world.get_entrance("D09Z01S09[Cell21]", player),
        lambda state: (
            state.has("Key of the Inquisitor", player)
            and (
                state.has("D09Z01S09[Cell20]", player)
                or state.has("D09Z01S09[SW]", player)
                or state.has("D09Z01S09[E]", player)
                or state.has("Dash Ability", player)
            )
        ))


    # D09Z01S10 (Wall of the Holy Prohibitions)
    # Items
    set_rule(world.get_location("WotHP: Lower east room, top bronze cell", player),
        lambda state: state.has("D09Z01S10[Cell13]", player))
    set_rule(world.get_location("WotHP: Lower east room, hidden ledge", player),
        lambda state: (
            state.has("D09Z01S10[W]", player)
            or state.has("D09Z01S10[Cell12]", player)
            or state.has("D09Z01S10[Cell10]", player)
            or state.has("D09Z01S10[Cell11]", player)
        ))
    # Doors
    set_rule(world.get_entrance("D09Z01S10[W]", player),
        lambda state: (
            state.has("D09Z01S10[Cell12]", player)
            or state.has("D09Z01S10[Cell10]", player)
            or state.has("D09Z01S10[Cell11]", player)
        ))
    set_rule(world.get_entrance("D09Z01S10[Cell12]", player),
        lambda state: (
            state.has("D09Z01S10[W]", player) or \
            state.has("D09Z01S10[Cell10]", player) or \
                state.has("D09Z01S10[Cell11]", player)
        ))
    add_rule(world.get_entrance("D09Z01S10[Cell12]", player),
        lambda state: state.has("Key of the Secular", player))
    set_rule(world.get_entrance("D09Z01S10[Cell10]", player),
        lambda state: (
            state.has("D09Z01S10[W]", player)
            or state.has("D09Z01S10[Cell12]", player)
            or state.has("D09Z01S10[Cell11]", player)
        ))
    add_rule(world.get_entrance("D09Z01S10[Cell10]", player),
        lambda state: state.has("Key of the Scribe", player))
    set_rule(world.get_entrance("D09Z01S10[Cell11]", player),
        lambda state: (
            state.has("D09Z01S10[W]", player)
            or state.has("D09Z01S10[Cell12]", player)
            or state.has("D09Z01S10[Cell10]", player)
        ))
    add_rule(world.get_entrance("D09Z01S10[Cell11]", player),
        lambda state: state.has("Key of the Scribe", player))
    
    # D09BZ01S01 (Wall of the Holy Prohibitions - Inside cells)
    # Items
    set_rule(world.get_location("WotHP: Upper east room, center cell ledge", player),
        lambda state: state.has("D09BZ01S01[Cell22]", player))
    set_rule(world.get_location("WotHP: Upper east room, center cell floor", player),
        lambda state: (
            state.has("D09BZ01S01[Cell22]", player)
            or state.has("D09BZ01S01[Cell23]", player)
        ))
    set_rule(world.get_location("WotHP: Upper east room, top bronze cell", player),
        lambda state: state.has("D09BZ01S01[Cell1]", player))
    set_rule(world.get_location("WotHP: Upper east room, top silver cell", player),
        lambda state: state.has("D09BZ01S01[Cell6]", player))
    set_rule(world.get_location("WotHP: Upper west room, top silver cell", player),
        lambda state: (
            state.has("D09BZ01S01[Cell14]", player)
            or state.has("D09BZ01S01[Cell15]", player)
        ))
    set_rule(world.get_location("WotHP: Upper west room, center gold cell", player),
        lambda state: state.has("D09BZ01S01[Cell16]", player))
    set_rule(world.get_location("WotHP: Lower west room, bottom gold cell", player),
        lambda state: (
            state.has("D09BZ01S01[Cell21]", player)
            and state.has("Blood Perpetuated in Sand", player)
            and can_climb_on_root(state, player)
            and can_survive_poison(state, logic, player, 2)
            and state.has("Dash Ability", player)
        ))
    set_rule(world.get_location("WotHP: Lower east room, top silver cell", player),
        lambda state: state.has("D09BZ01S01[Cell10]", player))
    set_rule(world.get_location("WotHP: Lower east room, bottom silver cell", player),
        lambda state: (
            state.has("D09BZ01S01[Cell11]", player)
            and (
                can_survive_poison(state, logic, player, 1)
                and state.has("Dash Ability", player)
                or state.has_any({"Debla of the Lights", "Taranto to my Sister", "Cante Jondo of the Three Sisters", "Verdiales of the Forsaken Hamlet", "Cantina of the Blue Rose"}, player)
                or aubade(state, player)
            )
        ))
    # Doors
    set_rule(world.get_entrance("D09BZ01S01[Cell2]", player),
        lambda state: state.has("D09BZ01S01[Cell3]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell3]", player),
        lambda state: state.has("D09BZ01S01[Cell2]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell4]", player),
        lambda state: state.has("D09BZ01S01[Cell5]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell5]", player),
        lambda state: state.has("D09BZ01S01[Cell5]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell12]", player),
        lambda state: state.has("D09BZ01S01[Cell13]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell13]", player),
        lambda state: state.has("D09BZ01S01[Cell12]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell14]", player),
        lambda state: state.has("D09BZ01S01[Cell15]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell15]", player),
        lambda state: state.has("D09BZ01S01[Cell14]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell17]", player),
        lambda state: state.has("D09BZ01S01[Cell18]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell19]", player),
        lambda state: state.has("D09BZ01S01[Cell20]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell20]", player),
        lambda state: state.has("D09BZ01S01[Cell19]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell23]", player),
        lambda state: state.has("D09BZ01S01[Cell22]", player))
    add_rule(world.get_entrance("D09BZ01S01[Cell23]", player),
        lambda state: state.has("Key of the Secular", player))


    # D17Z01S01 (Brotherhood of the Silent Sorrow)
    set_rule(world.get_location("BotSS: Starting room ledge", player),
        lambda state: state.has("D17Z01S01[Cherubs3]", player))
    set_rule(world.get_location("BotSS: Starting room Child of Moonlight", player),
        lambda state: (
            state.has("D17Z01S01[Cherubs1]", player)
            or state.has("Taranto to my Sister", player)
            or (
                can_climb_on_root(state, player)
                or can_cross_gap(state, logic, player, 9)
            )
            and (
                state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun", "Debla of the Lights", "Verdiales of the Forsaken Hamlet", "Cloistered Ruby"}, player)
                or tirana(state, player)
            )
        ))


    # D17Z01S02 (Brotherhood of the Silent Sorrow)
    # No items
    # Doors
    set_rule(world.get_entrance("D17Z01S02[W]", player),
        lambda state: state.has("Dash Ability", player))
    set_rule(world.get_entrance("D17Z01S02[E]", player),
        lambda state: (
            state.has("D17Z01S02[N]", player)
            or state.has("Dash Ability", player)
        ))
    set_rule(world.get_entrance("D17Z01S02[N]", player),
        lambda state: (
            state.has("Blood Perpetuated in Sand", player)
            and (
                state.has("D17Z01S02[E]", player)
                or state.has("D17Z01S02[W]", player)
                and state.has("Dash Ability", player)
            )
        ))


    # D17Z01S03 (Brotherhood of the Silent Sorrow)
    # No items
    # Doors
    set_rule(world.get_entrance("D17Z01S03[relic]", player),
        lambda state: state.has("Key to the Chamber of the Eldest Brother", player))


    # D17Z01S04 (Brotherhood of the Silent Sorrow)
    # Items
    if world.boots_of_pleading[player]:
        set_rule(world.get_location("BotSS: 2nd meeting with Redento", player),
            lambda state: redento(state, blasphemousworld, player, 2))
    # Doors
    set_rule(world.get_entrance("D17Z01S04[N]", player),
        lambda state: state.has("D17Z01S04[FrontR]", player))
    set_rule(world.get_entrance("D17Z01S04[FrontR]", player),
        lambda state: state.has("D17Z01S04[N]", player))
    # Event
    set_rule(world.get_location("OpenedBOTSSLadder", player),
        lambda state: opened_botss_ladder(state, player))


    # D17Z01S05 (Brotherhood of the Silent Sorrow)
    # No items
    # Doors
    set_rule(world.get_entrance("D17Z01S05[S]", player),
        lambda state: state.has("OpenedBOTSSLadder", player))


    # D17Z01S10 (Brotherhood of the Silent Sorrow)
    # No items
    # Doors
    set_rule(world.get_entrance("D17Z01S10[W]", player),
        lambda state: state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun"}, player))


    # D17Z01S11 (Brotherhood of the Silent Sorrow)
    # Items
    set_rule(world.get_location("BotSS: Warden of the Silent Sorrow", player),
        lambda state: can_beat_boss(state, "Brotherhood", logic, player))
    # Doors
    set_rule(world.get_entrance("D17Z01S11[W]", player),
        lambda state: can_beat_boss(state, "Brotherhood", logic, player))
    set_rule(world.get_entrance("D17Z01S11[E]", player),
        lambda state: can_beat_boss(state, "Brotherhood", logic, player))


    # D17Z01S14 (Brotherhood of the Silent Sorrow)
    # Items
    set_rule(world.get_location("BotSS: Outside church", player),
        lambda state: (
            state.has("D17Z01S14[W]", player)
            or state.has("Blood Perpetuated in Sand", player)
        ))
    # Doors
    set_rule(world.get_entrance("D17Z01S14[W]", player),
        lambda state: (
            state.has("Incomplete Scapular", player)
            and state.has("Blood Perpetuated in Sand", player)
        ))
    set_rule(world.get_entrance("D17Z01S14[E]", player),
        lambda state: state.has("Blood Perpetuated in Sand", player))
    set_rule(world.get_entrance("D17Z01S14[-Cherubs1]", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            and (
                state.has("D17Z01S14[W]", player)
                or state.has("Blood Perpetuated in Sand", player)
                or can_cross_gap(state, logic, player, 11)
            )
        ))
    set_rule(world.get_entrance("D17Z01S14[-Cherubs2]", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            and (
                state.has("D17Z01S14[E]", player)
                and can_cross_gap(state, logic, player, 8)
                or state.has("D17Z01S14[W]", player)
                and can_cross_gap(state, logic, player, 10)
                or state.has("Blood Perpetuated in Sand", player)
            )
        ))
    set_rule(world.get_entrance("D17Z01S14[-Cherubs3]", player),
        lambda state: (
            state.has("Linen of Golden Thread", player)
            and (
                state.has("D17Z01S14[E]", player)
                or state.has("Blood Perpetuated in Sand", player)
            )
        ))


    # D17Z01S15 (Brotherhood of the Silent Sorrow)
    # Items
    set_rule(world.get_location("BotSS: Esdras' final gift", player),
        lambda state: (
            can_beat_boss(state, "Bridge", logic, player)
            and state.has_group("wounds", player, 3)
        ))
    set_rule(world.get_location("BotSS: Crisanta's gift", player),
        lambda state: (
            can_beat_boss(state, "Rooftops", logic, player)
            and state.has("Apodictic Heart of Mea Culpa", player)
        ))
    # No doors


    # D17BZ02S01 (Brotherhood of the Silent Sorrow - Platforming challenge)
    # Items
    set_rule(world.get_location("BotSS: Platforming gauntlet", player),
        lambda state: (
            #state.has("D17BZ02S01[FrontR]", player) or
            # TODO: actually fix this once door rando is real
            state.has_all({"Dash Ability", "Wall Climb Ability"}, player) 
        ))
    # Doors
    set_rule(world.get_entrance("D17BZ02S01[FrontR]", player),
        lambda state: state.has_all({"Dash Ability", "Wall Climb Ability"}, player))


    # D20Z01S04 (Echoes of Salt)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z01S04[E]", player),
        lambda state: state.has("OpenedDCGateW", player))


    # D20Z01S09 (Echoes of Salt)
    # Items
    set_rule(world.get_location("EoS: Lantern jump near elevator", player),
        lambda state: (
            state.has("D20Z01S09[W]", player)
            or state.has("Dash Ability", player)
        ))
    # Doors
    set_rule(world.get_entrance("D20Z01S09[W]", player),
        lambda state: state.has("Dash Ability", player))
    set_rule(world.get_entrance("D20Z01S09[E]", player),
        lambda state: state.has_all({"Blood Perpetuated in Sand", "Dash Ability"}, player))


    # D20Z01S10 (Echoes of Salt)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z01S10[W]", player),
        lambda state: state.has_all({"Blood Perpetuated in Sand", "Dash Ability"}, player))
    set_rule(world.get_entrance("D20Z01S10[E]", player),
        lambda state: state.has_all({"Blood Perpetuated in Sand", "Dash Ability"}, player))


    # D20Z02S03 (Mourning and Havoc)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z02S03[NE]", player),
        lambda state: (
            can_walk_on_root(state, player)
            or can_cross_gap(state, logic, player, 5)
        ))


    # D20Z02S04 (Mourning and Havoc)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z02S04[W]", player),
        lambda state: state.has("Dash Ability", player))
    set_rule(world.get_entrance("D20Z02S04[E]", player),
        lambda state: state.has("Dash Ability", player))


    # D20Z02S05 (Mourning and Havoc)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z02S05[NW]", player),
        lambda state: (
            state.has("Nail Uprooted from Dirt", player)
            or can_cross_gap(state, logic, player, 3)
        ))


    # D20Z02S06 (Mourning and Havoc)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z02S06[NW]", player),
        lambda state: (
            state.has("D20Z02S06[NE]", player)
            or state.has("Purified Hand of the Nun", player)
            or can_climb_on_root(state, player)
            or can_dive_laser(state, logic, player)
        ))
    set_rule(world.get_entrance("D20Z02S06[NE]", player),
        lambda state: (
            state.has("D20Z02S06[NW]", player)
            or state.has("Purified Hand of the Nun", player)
            or can_climb_on_root(state, player)
            or can_dive_laser(state, logic, player)
        ))


    # D20Z02S08 (Mourning and Havoc)
    # Items
    set_rule(world.get_location("MaH: Sierpes", player),
        lambda state: can_beat_boss(state, "Mourning", logic, player))
    set_rule(world.get_location("MaH: Sierpes' eye", player),
        lambda state: can_beat_boss(state, "Mourning", logic, player))
    # No doors


    # D20Z02S11 (Mourning and Havoc)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z02S11[NW]", player),
        lambda state: state.has("D20Z02S11[E]", player))
    set_rule(world.get_entrance("D20Z02S11[NW]", player),
        lambda state: (
            mourning_skips_allowed(logic)
            and (
                state.has("Purified Hand of the Nun", player)
                or can_break_tirana(state, logic, player)
                or state.has("D20Z02S11[E]", player)
            )
        ))
    set_rule(world.get_entrance("D20Z02S11[E]", player),
        lambda state: (
            mourning_skips_allowed(logic)
            and (
                state.has("Purified Hand of the Nun", player)
                or can_break_tirana(state, logic, player)
                or state.has("D20Z02S11[NW]", player)
                and can_cross_gap(state, logic, player, 5)
            )
        ))
    

    # Misc Items
    set_rule(world.get_location("Second red candle", player),
        lambda state: (
            state.has("Bead of Red Wax", player)
            and (
                state.can_reach(world.get_region("D02Z03S06", player), player)
                or state.has("D05Z01S02[W]", player)
            )
        ))
    set_rule(world.get_location("Third red candle", player),
        lambda state: (
            state.has("Bead of Red Wax", player)
            and state.has("D05Z01S02[W]", player)
            and state.can_reach(world.get_region("D02Z03S06", player), player)
        ))
    set_rule(world.get_location("Second blue candle", player),
        lambda state: (
            state.has("Bead of Blue Wax", player)
            and (
                state.has("OpenedBOTSSLadder", player)
                or state.can_reach(world.get_region("D01Z04S16", player), player)
            )
        ))
    set_rule(world.get_location("Third blue candle", player),
        lambda state: (
            state.has("Bead of Blue Wax", player)
            and state.has("OpenedBOTSSLadder", player)
            and state.can_reach(world.get_region("D01Z04S16", player), player)
        ))
    set_rule(world.get_location("Defeat 1 Amanecida", player),
        lambda state: amanecida_rooms(state, logic, player, 1))
    set_rule(world.get_location("Defeat 2 Amanecidas", player),
        lambda state: amanecida_rooms(state, logic, player, 2))
    set_rule(world.get_location("Defeat 3 Amanecidas", player),
        lambda state: amanecida_rooms(state, logic, player, 3))
    set_rule(world.get_location("Defeat 4 Amanecidas", player),
        lambda state: amanecida_rooms(state, logic, player, 4))
    set_rule(world.get_location("Defeat all Amanecidas", player),
        lambda state: amanecida_rooms(state, logic, player, 4))
    set_rule(world.get_location("Confessor Dungeon 1 main", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 1)
        ))
    set_rule(world.get_location("Confessor Dungeon 2 main", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 2)
        ))
    set_rule(world.get_location("Confessor Dungeon 3 main", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 3)
        ))
    set_rule(world.get_location("Confessor Dungeon 4 main", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 4)
        ))
    set_rule(world.get_location("Confessor Dungeon 5 main", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 5)
        ))
    set_rule(world.get_location("Confessor Dungeon 6 main", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 6)
        ))
    set_rule(world.get_location("Confessor Dungeon 7 main", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 7)
        ))
    set_rule(world.get_location("Confessor Dungeon 1 extra", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 1)
        ))
    set_rule(world.get_location("Confessor Dungeon 2 extra", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 2)
        ))
    set_rule(world.get_location("Confessor Dungeon 3 extra", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 3)
        ))
    set_rule(world.get_location("Confessor Dungeon 4 extra", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 4)
        ))
    set_rule(world.get_location("Confessor Dungeon 5 extra", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 5)
        ))
    set_rule(world.get_location("Confessor Dungeon 6 extra", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 6)
        ))
    set_rule(world.get_location("Confessor Dungeon 7 extra", player),
        lambda state: (
            state.has("Weight of True Guilt", player)
            and guilt_rooms(state, player, 7)
        ))
    set_rule(world.get_location("Skill 1, Tier 1", player),
        lambda state: sword_rooms(state, player, 1))
    set_rule(world.get_location("Skill 1, Tier 2", player),
        lambda state: sword_rooms(state, player, 2))
    set_rule(world.get_location("Skill 1, Tier 3", player),
        lambda state: sword_rooms(state, player, 4))
    set_rule(world.get_location("Skill 2, Tier 1", player),
        lambda state: sword_rooms(state, player, 1))
    set_rule(world.get_location("Skill 2, Tier 2", player),
        lambda state: sword_rooms(state, player, 3))
    set_rule(world.get_location("Skill 2, Tier 3", player),
        lambda state: sword_rooms(state, player, 6))
    set_rule(world.get_location("Skill 3, Tier 1", player),
        lambda state: sword_rooms(state, player, 2))
    set_rule(world.get_location("Skill 3, Tier 2", player),
        lambda state: sword_rooms(state, player, 5))
    set_rule(world.get_location("Skill 3, Tier 3", player),
        lambda state: sword_rooms(state, player, 7))
    set_rule(world.get_location("Skill 4, Tier 1", player),
        lambda state: sword_rooms(state, player, 1))
    set_rule(world.get_location("Skill 4, Tier 2", player),
        lambda state: sword_rooms(state, player, 3))
    set_rule(world.get_location("Skill 4, Tier 3", player),
        lambda state: sword_rooms(state, player, 6))
    set_rule(world.get_location("Skill 5, Tier 1", player),
        lambda state: sword_rooms(state, player, 1))
    set_rule(world.get_location("Skill 5, Tier 2", player),
        lambda state: sword_rooms(state, player, 2))
    set_rule(world.get_location("Skill 5, Tier 3", player),
        lambda state: sword_rooms(state, player, 4))