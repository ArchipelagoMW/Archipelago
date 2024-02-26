import os
import hashlib
import Utils
import bsdiff4
import pkgutil
from worlds.Files import APDeltaPatch
from .text import encode_text
from .items import item_table
from .pokemon import set_mon_palettes
from .rock_tunnel import randomize_rock_tunnel
from .rom_addresses import rom_addresses
from .regions import PokemonRBWarp, map_ids
from . import poke_data

def write_quizzes(self, data, random):

    def get_quiz(q, a):
        if q == 0:
            r = random.randint(0, 3)
            if r == 0:
                mon = self.trade_mons["Trade_Dux"]
                text = "A woman in<LINE>Vermilion City<CONT>"
            elif r == 1:
                mon = self.trade_mons["Trade_Lola"]
                text = "A man in<LINE>Cerulean City<CONT>"
            elif r == 2:
                mon = self.trade_mons["Trade_Marcel"]
                text = "Someone on Route 2<LINE>"
            elif r == 3:
                mon = self.trade_mons["Trade_Spot"]
                text = "Someone on Route 5<LINE>"
            if not a:
                answers.append(0)
                old_mon = mon
                while old_mon == mon:
                    mon = random.choice(list(poke_data.pokemon_data.keys()))

            return encode_text(f"{text}was looking for<CONT>{mon}?<DONE>")
        elif q == 1:
            for location in self.multiworld.get_filled_locations():
                if location.item.name == "Secret Key" and location.item.player == self.player:
                    break
            player_name = self.multiworld.player_name[location.player]
            if not a:
                if len(self.multiworld.player_name) > 1:
                    old_name = player_name
                    while old_name == player_name:
                        player_name = random.choice(list(self.multiworld.player_name.values()))
                else:
                    return encode_text("You're playing<LINE>in a multiworld<CONT>with other<CONT>players?<DONE>")
            if player_name == self.multiworld.player_name[self.player]:
                player_name = "yourself"
            player_name = encode_text(player_name, force=True, safety=True)
            return encode_text(f"The Secret Key was<LINE>found by<CONT>") + player_name + encode_text("<DONE>")
        elif q == 2:
            if a:
                return encode_text(f"#mon is<LINE>pronounced<CONT>Po-kay-mon?<DONE>")
            else:
                if random.randint(0, 1):
                    return encode_text(f"#mon is<LINE>pronounced<CONT>Po-key-mon?<DONE>")
                else:
                    return encode_text(f"#mon is<LINE>pronounced<CONT>Po-kuh-mon?<DONE>")
        elif q == 3:
            starters = [" ".join(self.multiworld.get_location(
                f"Oak's Lab - Starter {i}", self.player).item.name.split(" ")[1:]) for i in range(1, 4)]
            mon = random.choice(starters)
            nots = random.choice(range(8, 16, 2))
            if random.randint(0, 1):
                while mon in starters:
                    mon = random.choice(list(poke_data.pokemon_data.keys()))
                    if a:
                        nots += 1
            elif not a:
                nots += 1
            text = f"{mon} was<LINE>"
            while nots > 0:
                i = random.randint(1, min(4, nots))
                text += ("not " * i) + "<CONT>"
                nots -= i
            text += "a starter choice?<DONE>"
            return encode_text(text)
        elif q == 4:
            if a:
                tm_text = self.local_tms[27]
            else:
                if self.multiworld.randomize_tm_moves[self.player]:
                    wrong_tms = self.local_tms.copy()
                    wrong_tms.pop(27)
                    tm_text = random.choice(wrong_tms)
                else:
                    tm_text = "TOMBSTONER"
            return encode_text(f"TM28 contains<LINE>{tm_text.upper()}?<DONE>")
        elif q == 5:
            i = 8
            while not a and i in [1, 8]:
                i = random.randint(0, int("99999999"[random.randint(0, 7):]))
            return encode_text(f"There are {i}<LINE>certified #MON<CONT>LEAGUE BADGEs?<DONE>")
        elif q == 6:
            i = 2
            while not a and i in [1, 2]:
                i = random.randint(0, random.choice([9, 99]))
            return encode_text(f"POLIWAG evolves {i}<LINE>times?<DONE>")
        elif q == 7:
            entity = "Motor Carrier"
            if not a:
                entity = random.choice(["Driver", "Shipper"])
            return encode_text("Title 49 of the<LINE>U.S. Code of<CONT>Federal<CONT>Regulations part<CONT>397.67 states"
                               f"<CONT>that the<CONT>{entity}<CONT>is responsible<CONT>for planning<CONT>routes when"
                               "<CONT>hazardous<CONT>materials are<CONT>transported?<DONE>")
        elif q == 8:
            mon = random.choice(list(poke_data.evolution_levels.keys()))
            level = poke_data.evolution_levels[mon]
            if not a:
                level += random.choice(range(1, 6)) * random.choice((-1, 1))
            return encode_text(f"{mon} evolves<LINE>at level {level}?<DONE>")
        elif q == 9:
            move = random.choice(list(self.local_move_data.keys()))
            actual_type = self.local_move_data[move]["type"]
            question_type = actual_type
            while question_type == actual_type and not a:
                question_type = random.choice(list(poke_data.type_ids.keys()))
            return encode_text(f"{move} is<LINE>{question_type} type?<DONE>")
        elif q == 10:
            mon = random.choice(list(poke_data.pokemon_data.keys()))
            actual_type = self.local_poke_data[mon][random.choice(("type1", "type2"))]
            question_type = actual_type
            while question_type in [self.local_poke_data[mon]["type1"], self.local_poke_data[mon]["type2"]] and not a:
                question_type = random.choice(list(poke_data.type_ids.keys()))
            return encode_text(f"{mon} is<LINE>{question_type} type?<DONE>")
        elif q == 11:
            equation = ""
            while "*" not in equation:
                equation = f"{random.randint(0, 9)} {random.choice(['+', '-', '*'])} {random.randint(0, 9)} {random.choice(['+', '-', '*'])} {random.randint(0, 9)} {random.choice(['+', '-', '*'])} {random.randint(0, 9)}"
            result = eval(equation)
            question_result = result
            if not a:
                modifiers = random.sample(range(3), 3)
                for modifier in modifiers:
                    question_result = eval(equation[:modifier * 4] + "(" + equation[modifier * 4:(modifier * 4) + 5]
                                           + ")" + equation[5 + (modifier * 4):])
                    if question_result != result:
                        break
                else:
                    question_result += random.choice(range(1, 6)) * random.choice((-1, 1))

            return encode_text(f"{equation}<LINE>= {question_result}?<DONE>")
        elif q == 12:
            route = random.choice((12, 16))
            actual_mon = self.multiworld.get_location(f"Route {route} - Sleeping Pokemon",
                                                      self.player).item.name.split("Static ")[1]
            question_mon = actual_mon
            while question_mon == actual_mon and not a:
                question_mon = random.choice(list(poke_data.pokemon_data.keys()))
            return encode_text(f"{question_mon} was<LINE>sleeping on route<CONT>{route}?<DONE>")
        elif q == 13:
            type1 = random.choice(list(poke_data.type_ids.keys()))
            type2 = random.choice(list(poke_data.type_ids.keys()))
            eff_msgs = ["super effective<CONT>", "no ", "not very<CONT>effective<CONT>", "normal "]
            for matchup in self.type_chart:
                if matchup[0] == type1 and matchup[1] == type2:
                    if matchup[2] > 10:
                        eff = eff_msgs[0]
                    elif matchup[2] == 0:
                        eff = eff_msgs[1]
                    elif matchup[2] < 10:
                        eff = eff_msgs[2]
                    else:
                        eff = eff_msgs[3]
                    break
            else:
                eff = eff_msgs[3]
            if not a:
                eff_msgs.remove(eff)
                eff = random.choice(eff_msgs)
            return encode_text(f"{type1} deals<LINE>{eff}damage to<CONT>{type2} type?<DONE>")
        elif q == 14:
            fossil_level = self.multiworld.get_location("Fossil Level - Trainer Parties",
                                                        self.player).party_data[0]['level']
            if not a:
                fossil_level += random.choice((-5, 5))
            return encode_text(f"Fossil #MON<LINE>revive at level<CONT>{fossil_level}?<DONE>")

    answers = [random.randint(0, 1) for _ in range(6)]

    questions = random.sample((range(0, 15)), 6)
    question_texts = []
    for i, question in enumerate(questions):
        question_texts.append(get_quiz(question, answers[i]))

    for i, quiz in enumerate(["A", "B", "C", "D", "E", "F"]):
        data[rom_addresses[f"Quiz_Answer_{quiz}"]] = int(not answers[i]) << 4 | (i + 1)
        write_bytes(data, question_texts[i], rom_addresses[f"Text_Quiz_{quiz}"])


def generate_output(self, output_directory: str):
    random = self.multiworld.per_slot_randoms[self.player]
    game_version = self.multiworld.game_version[self.player].current_key
    data = bytes(get_base_rom_bytes(game_version))

    base_patch = pkgutil.get_data(__name__, f'basepatch_{game_version}.bsdiff4')

    data = bytearray(bsdiff4.patch(data, base_patch))

    basemd5 = hashlib.md5()
    basemd5.update(data)

    lab_loc = self.multiworld.get_entrance("Oak's Lab to Pallet Town", self.player).target
    paths = None
    if lab_loc == 0:  # Player's House
        paths = ((0x00, 4, 0x80, 5, 0x40, 1, 0xE0, 1, 0xFF), (0x40, 2, 0x20, 5, 0x80, 5, 0xFF))
    elif lab_loc == 1:  # Rival's House
        paths = ((0x00, 4, 0xC0, 3, 0x40, 1, 0xE0, 1, 0xFF), (0x40, 2, 0x10, 3, 0x80, 5, 0xFF))
    if paths:
        write_bytes(data, paths[0], rom_addresses["Path_Pallet_Oak"])
        write_bytes(data, paths[1], rom_addresses["Path_Pallet_Player"])
    home_loc = self.multiworld.get_entrance("Player's House 1F to Pallet Town", self.player).target
    if home_loc == 1:  # Rival's House
        write_bytes(data, [0x2F, 0xC7, 0x06, 0x0D, 0x00, 0x01], rom_addresses["Pallet_Fly_Coords"])
    elif home_loc == 2:  # Oak's Lab
        write_bytes(data, [0x5F, 0xC7, 0x0C, 0x0C, 0x00, 0x00], rom_addresses["Pallet_Fly_Coords"])

    for region in self.multiworld.get_regions(self.player):
        for entrance in region.exits:
            if isinstance(entrance, PokemonRBWarp):
                self.multiworld.spoiler.set_entrance(entrance.name, entrance.connected_region.name, "entrance",
                                                     self.player)
                warp_ids = (entrance.warp_id,) if isinstance(entrance.warp_id, int) else entrance.warp_id
                warp_to_ids = (entrance.target,) if isinstance(entrance.target, int) else entrance.target
                for i, warp_id in enumerate(warp_ids):
                    address = rom_addresses[entrance.address]
                    if "Elevator" in entrance.parent_region.name:
                        address += (2 * warp_id)
                    else:
                        address += (4 * warp_id)
                    while i > len(warp_to_ids) - 1:
                        i -= len(warp_to_ids)
                    connected_map_name = entrance.connected_region.name.split("-")[0]
                    data[address] = 0 if "Elevator" in connected_map_name else warp_to_ids[i]
                    data[address + 1] = map_ids[connected_map_name]

    if not self.multiworld.key_items_only[self.player]:
        for i, gym_leader in enumerate(("Pewter Gym - Brock TM", "Cerulean Gym - Misty TM",
                                        "Vermilion Gym - Lt. Surge TM", "Celadon Gym - Erika TM",
                                        "Fuchsia Gym - Koga TM", "Saffron Gym - Sabrina TM",
                                        "Cinnabar Gym - Blaine TM", "Viridian Gym - Giovanni TM")):
            item_name = self.multiworld.get_location(gym_leader, self.player).item.name
            if item_name.startswith("TM"):
                try:
                    tm = int(item_name[2:4])
                    move = poke_data.moves[self.local_tms[tm - 1]]["id"]
                    data[rom_addresses["Gym_Leader_Moves"] + (2 * i)] = move
                except KeyError:
                    pass

    def set_trade_mon(address, loc):
        mon = self.multiworld.get_location(loc, self.player).item.name
        data[rom_addresses[address]] = poke_data.pokemon_data[mon]["id"]
        self.trade_mons[address] = mon

    if game_version == "red":
        set_trade_mon("Trade_Terry", "Safari Zone Center - Wild Pokemon - 5")
        set_trade_mon("Trade_Spot", "Safari Zone East - Wild Pokemon - 1")
    else:
        set_trade_mon("Trade_Terry", "Safari Zone Center - Wild Pokemon - 7")
        set_trade_mon("Trade_Spot", "Safari Zone East - Wild Pokemon - 7")
    set_trade_mon("Trade_Marcel", "Route 24 - Wild Pokemon - 6")
    set_trade_mon("Trade_Sailor", "Pokemon Mansion 1F - Wild Pokemon - 3")
    set_trade_mon("Trade_Dux", "Route 3 - Wild Pokemon - 2")
    set_trade_mon("Trade_Marc", "Route 23/Cerulean Cave Fishing - Super Rod Pokemon - 1")
    set_trade_mon("Trade_Lola", "Route 10/Celadon Fishing - Super Rod Pokemon - 1")
    set_trade_mon("Trade_Doris", "Cerulean Cave 1F - Wild Pokemon - 9")
    set_trade_mon("Trade_Crinkles", "Route 12 - Wild Pokemon - 4")

    data[rom_addresses['Fly_Location']] = self.fly_map_code
    data[rom_addresses['Map_Fly_Location']] = self.town_map_fly_map_code

    if self.multiworld.fix_combat_bugs[self.player]:
        data[rom_addresses["Option_Fix_Combat_Bugs"]] = 1
        data[rom_addresses["Option_Fix_Combat_Bugs_Focus_Energy"]] = 0x28  # jr z
        data[rom_addresses["Option_Fix_Combat_Bugs_HP_Drain_Dream_Eater"]] = 0x1A  # ld a, (de)
        data[rom_addresses["Option_Fix_Combat_Bugs_PP_Restore"]] = 0xe6  # and a, direct
        data[rom_addresses["Option_Fix_Combat_Bugs_PP_Restore"] + 1] = 0b0011111
        data[rom_addresses["Option_Fix_Combat_Bugs_Struggle"]] = 0xe6  # and a, direct
        data[rom_addresses["Option_Fix_Combat_Bugs_Struggle"] + 1] = 0x3f
        data[rom_addresses["Option_Fix_Combat_Bugs_Dig_Fly"]] = 0b10001100
        data[rom_addresses["Option_Fix_Combat_Bugs_Heal_Effect"]] = 0x20  # jr nz,
        data[rom_addresses["Option_Fix_Combat_Bugs_Heal_Effect"] + 1] = 5  # 5 bytes ahead
        data[rom_addresses["Option_Fix_Combat_Bugs_Heal_Stat_Modifiers"]] = 1

    if self.multiworld.poke_doll_skip[self.player] == "in_logic":
        data[rom_addresses["Option_Silph_Scope_Skip"]] = 0x00      # nop
        data[rom_addresses["Option_Silph_Scope_Skip"] + 1] = 0x00  # nop
        data[rom_addresses["Option_Silph_Scope_Skip"] + 2] = 0x00  # nop

    if self.multiworld.bicycle_gate_skips[self.player] == "patched":
        data[rom_addresses["Option_Route_16_Gate_Fix"]] = 0x00     # nop
        data[rom_addresses["Option_Route_16_Gate_Fix"] + 1] = 0x00 # nop
        data[rom_addresses["Option_Route_18_Gate_Fix"]] = 0x00     # nop
        data[rom_addresses["Option_Route_18_Gate_Fix"] + 1] = 0x00 # nop

    if self.multiworld.door_shuffle[self.player]:
        data[rom_addresses["Entrance_Shuffle_Fuji_Warp"]] = 1  # prevent warping to Fuji's House from Pokemon Tower 7F

    if self.multiworld.all_elevators_locked[self.player]:
        data[rom_addresses["Option_Locked_Elevator_Celadon"]] = 0x20  # jr nz
        data[rom_addresses["Option_Locked_Elevator_Silph"]] = 0x20    # jr nz

    if self.multiworld.tea[self.player].value:
        data[rom_addresses["Option_Tea"]] = 1
        data[rom_addresses["Guard_Drink_List"]] = 0x54
        data[rom_addresses["Guard_Drink_List"] + 1] = 0
        data[rom_addresses["Guard_Drink_List"] + 2] = 0
        write_bytes(data, encode_text("<LINE>Gee, I have the<CONT>worst caffeine<CONT>headache though."
                                      "<PARA>Oh wait there,<LINE>the road's closed.<DONE>"),
                    rom_addresses["Text_Saffron_Gate"])

    data[rom_addresses["Fossils_Needed_For_Second_Item"]] = (
        self.multiworld.second_fossil_check_condition[self.player].value)

    data[rom_addresses["Option_Lose_Money"]] = int(not self.multiworld.lose_money_on_blackout[self.player].value)

    if self.multiworld.extra_key_items[self.player]:
        data[rom_addresses['Option_Extra_Key_Items_A']] = 1
        data[rom_addresses['Option_Extra_Key_Items_B']] = 1
        data[rom_addresses['Option_Extra_Key_Items_C']] = 1
        data[rom_addresses['Option_Extra_Key_Items_D']] = 1
    data[rom_addresses["Option_Split_Card_Key"]] = self.multiworld.split_card_key[self.player].value
    data[rom_addresses["Option_Blind_Trainers"]] = round(self.multiworld.blind_trainers[self.player].value * 2.55)
    data[rom_addresses["Option_Cerulean_Cave_Badges"]] = self.multiworld.cerulean_cave_badges_condition[self.player].value
    data[rom_addresses["Option_Cerulean_Cave_Key_Items"]] = self.multiworld.cerulean_cave_key_items_condition[self.player].total
    write_bytes(data, encode_text(str(self.multiworld.cerulean_cave_badges_condition[self.player].value)), rom_addresses["Text_Cerulean_Cave_Badges"])
    write_bytes(data, encode_text(str(self.multiworld.cerulean_cave_key_items_condition[self.player].total) + " key items."), rom_addresses["Text_Cerulean_Cave_Key_Items"])
    data[rom_addresses['Option_Encounter_Minimum_Steps']] = self.multiworld.minimum_steps_between_encounters[self.player].value
    data[rom_addresses['Option_Route23_Badges']] = self.multiworld.victory_road_condition[self.player].value
    data[rom_addresses['Option_Victory_Road_Badges']] = self.multiworld.route_22_gate_condition[self.player].value
    data[rom_addresses['Option_Elite_Four_Pokedex']] = self.multiworld.elite_four_pokedex_condition[self.player].total
    data[rom_addresses['Option_Elite_Four_Key_Items']] = self.multiworld.elite_four_key_items_condition[self.player].total
    data[rom_addresses['Option_Elite_Four_Badges']] = self.multiworld.elite_four_badges_condition[self.player].value
    write_bytes(data, encode_text(str(self.multiworld.elite_four_badges_condition[self.player].value)), rom_addresses["Text_Elite_Four_Badges"])
    write_bytes(data, encode_text(str(self.multiworld.elite_four_key_items_condition[self.player].total) + " key items, and"), rom_addresses["Text_Elite_Four_Key_Items"])
    write_bytes(data, encode_text(str(self.multiworld.elite_four_pokedex_condition[self.player].total) + " #MON"), rom_addresses["Text_Elite_Four_Pokedex"])
    write_bytes(data, encode_text(str(self.total_key_items), length=2), rom_addresses["Trainer_Screen_Total_Key_Items"])

    data[rom_addresses['Option_Viridian_Gym_Badges']] = self.multiworld.viridian_gym_condition[self.player].value
    data[rom_addresses['Option_EXP_Modifier']] = self.multiworld.exp_modifier[self.player].value
    if not self.multiworld.require_item_finder[self.player]:
        data[rom_addresses['Option_Itemfinder']] = 0  # nop
    if self.multiworld.extra_strength_boulders[self.player]:
        for i in range(0, 3):
            data[rom_addresses['Option_Boulders'] + (i * 3)] = 0x15
    if self.multiworld.extra_key_items[self.player]:
        for i in range(0, 4):
            data[rom_addresses['Option_Rock_Tunnel_Extra_Items'] + (i * 3)] = 0x15
    if self.multiworld.old_man[self.player] == "open_viridian_city":
        data[rom_addresses['Option_Old_Man']] = 0x11
        data[rom_addresses['Option_Old_Man_Lying']] = 0x15
    data[rom_addresses['Option_Route3_Guard_B']] = self.multiworld.route_3_condition[self.player].value
    if self.multiworld.route_3_condition[self.player] == "open":
        data[rom_addresses['Option_Route3_Guard_A']] = 0x11
    if not self.multiworld.robbed_house_officer[self.player]:
        data[rom_addresses['Option_Trashed_House_Guard_A']] = 0x15
        data[rom_addresses['Option_Trashed_House_Guard_B']] = 0x11
    if self.multiworld.require_pokedex[self.player]:
        data[rom_addresses["Require_Pokedex_A"]] = 1
        data[rom_addresses["Require_Pokedex_B"]] = 1
        data[rom_addresses["Require_Pokedex_C"]] = 1
    else:
        data[rom_addresses["Require_Pokedex_D"]] = 0x18  # jr
    if self.multiworld.dexsanity[self.player]:
        data[rom_addresses["Option_Dexsanity_A"]] = 1
        data[rom_addresses["Option_Dexsanity_B"]] = 1
    if self.multiworld.all_pokemon_seen[self.player]:
        data[rom_addresses["Option_Pokedex_Seen"]] = 1
    money = str(self.multiworld.starting_money[self.player].value).zfill(6)
    data[rom_addresses["Starting_Money_High"]] = int(money[:2], 16)
    data[rom_addresses["Starting_Money_Middle"]] = int(money[2:4], 16)
    data[rom_addresses["Starting_Money_Low"]] = int(money[4:], 16)
    data[rom_addresses["Text_Badges_Needed_Viridian_Gym"]] = encode_text(
        str(self.multiworld.viridian_gym_condition[self.player].value))[0]
    data[rom_addresses["Text_Rt23_Badges_A"]] = encode_text(
        str(self.multiworld.victory_road_condition[self.player].value))[0]
    data[rom_addresses["Text_Rt23_Badges_B"]] = encode_text(
        str(self.multiworld.victory_road_condition[self.player].value))[0]
    data[rom_addresses["Text_Rt23_Badges_C"]] = encode_text(
        str(self.multiworld.victory_road_condition[self.player].value))[0]
    data[rom_addresses["Text_Rt23_Badges_D"]] = encode_text(
        str(self.multiworld.victory_road_condition[self.player].value))[0]
    data[rom_addresses["Text_Badges_Needed"]] = encode_text(
        str(self.multiworld.elite_four_badges_condition[self.player].value))[0]
    write_bytes(data, encode_text(
        " ".join(self.multiworld.get_location("Route 4 Pokemon Center - Pokemon For Sale", self.player).item.name.upper().split()[1:])),
                rom_addresses["Text_Magikarp_Salesman"])

    if self.multiworld.badges_needed_for_hm_moves[self.player].value == 0:
        for hm_move in poke_data.hm_moves:
            write_bytes(data, bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
                        rom_addresses["HM_" + hm_move + "_Badge_a"])
    elif self.extra_badges:
        written_badges = {}
        for hm_move, badge in self.extra_badges.items():
            data[rom_addresses["HM_" + hm_move + "_Badge_b"]] = {"Boulder Badge": 0x47, "Cascade Badge": 0x4F,
                                                                 "Thunder Badge": 0x57, "Rainbow Badge": 0x5F,
                                                                 "Soul Badge": 0x67, "Marsh Badge": 0x6F,
                                                                 "Volcano Badge": 0x77, "Earth Badge": 0x7F}[badge]
            move_text = hm_move
            if badge not in ["Marsh Badge", "Volcano Badge", "Earth Badge"]:
                move_text = ", " + move_text
            rom_address = rom_addresses["Badge_Text_" + badge.replace(" ", "_")]
            if badge in written_badges:
                rom_address += len(written_badges[badge])
                move_text = ", " + move_text
            write_bytes(data, encode_text(move_text.upper()), rom_address)
            written_badges[badge] = move_text
        for badge in ["Marsh Badge", "Volcano Badge", "Earth Badge"]:
            if badge not in written_badges:
                write_bytes(data, encode_text("Nothing"), rom_addresses["Badge_Text_" + badge.replace(" ", "_")])

    type_loc = rom_addresses["Type_Chart"]
    for matchup in self.type_chart:
        if matchup[2] != 10:  # don't needlessly divide damage by 10 and multiply by 10
            data[type_loc] = poke_data.type_ids[matchup[0]]
            data[type_loc + 1] = poke_data.type_ids[matchup[1]]
            data[type_loc + 2] = matchup[2]
            type_loc += 3
    data[type_loc] = 0xFF
    data[type_loc + 1] = 0xFF
    data[type_loc + 2] = 0xFF

    if self.multiworld.normalize_encounter_chances[self.player].value:
        chances = [25, 51, 77, 103, 129, 155, 180, 205, 230, 255]
        for i, chance in enumerate(chances):
            data[rom_addresses['Encounter_Chances'] + (i * 2)] = chance

    for mon, mon_data in self.local_poke_data.items():
        if mon == "Mew":
            address = rom_addresses["Base_Stats_Mew"]
        else:
            address = rom_addresses["Base_Stats"] + (28 * (mon_data["dex"] - 1))
        data[address + 1] = self.local_poke_data[mon]["hp"]
        data[address + 2] = self.local_poke_data[mon]["atk"]
        data[address + 3] = self.local_poke_data[mon]["def"]
        data[address + 4] = self.local_poke_data[mon]["spd"]
        data[address + 5] = self.local_poke_data[mon]["spc"]
        data[address + 6] = poke_data.type_ids[self.local_poke_data[mon]["type1"]]
        data[address + 7] = poke_data.type_ids[self.local_poke_data[mon]["type2"]]
        data[address + 8] = self.local_poke_data[mon]["catch rate"]
        data[address + 15] = poke_data.moves[self.local_poke_data[mon]["start move 1"]]["id"]
        data[address + 16] = poke_data.moves[self.local_poke_data[mon]["start move 2"]]["id"]
        data[address + 17] = poke_data.moves[self.local_poke_data[mon]["start move 3"]]["id"]
        data[address + 18] = poke_data.moves[self.local_poke_data[mon]["start move 4"]]["id"]
        write_bytes(data, self.local_poke_data[mon]["tms"], address + 20)
        if mon in self.learnsets and self.learnsets[mon]:
                address = rom_addresses["Learnset_" + mon.replace(" ", "")]
                for i, move in enumerate(self.learnsets[mon]):
                    data[(address + 1) + i * 2] = poke_data.moves[move]["id"]

    data[rom_addresses["Option_Aide_Rt2"]] = self.multiworld.oaks_aide_rt_2[self.player].value
    data[rom_addresses["Option_Aide_Rt11"]] = self.multiworld.oaks_aide_rt_11[self.player].value
    data[rom_addresses["Option_Aide_Rt15"]] = self.multiworld.oaks_aide_rt_15[self.player].value

    if self.multiworld.safari_zone_normal_battles[self.player].value == 1:
        data[rom_addresses["Option_Safari_Zone_Battle_Type"]] = 255

    if self.multiworld.reusable_tms[self.player].value:
        data[rom_addresses["Option_Reusable_TMs"]] = 0xC9

    for i in range(1, 10):
        data[rom_addresses[f"Option_Trainersanity{i}"]] = self.multiworld.trainersanity[self.player].value

    data[rom_addresses["Option_Always_Half_STAB"]] = int(not self.multiworld.same_type_attack_bonus[self.player].value)

    if self.multiworld.better_shops[self.player]:
        inventory = ["Poke Ball", "Great Ball", "Ultra Ball"]
        if self.multiworld.better_shops[self.player].value == 2:
            inventory.append("Master Ball")
        inventory += ["Potion", "Super Potion", "Hyper Potion", "Max Potion", "Full Restore", "Revive", "Antidote",
                      "Awakening", "Burn Heal", "Ice Heal", "Paralyze Heal", "Full Heal", "Repel", "Super Repel",
                      "Max Repel", "Escape Rope"]
        shop_data = bytearray([0xFE, len(inventory)])
        shop_data += bytearray([item_table[item].id - 172000000 for item in inventory])
        shop_data.append(0xFF)
        for shop in range(1, 11):
            write_bytes(data, shop_data, rom_addresses[f"Shop{shop}"])
    if self.multiworld.stonesanity[self.player]:
        write_bytes(data, bytearray([0xFE, 1, item_table["Poke Doll"].id - 172000000, 0xFF]), rom_addresses[f"Shop_Stones"])

    price = str(self.multiworld.master_ball_price[self.player].value).zfill(6)
    price = bytearray([int(price[:2], 16), int(price[2:4], 16), int(price[4:], 16)])
    write_bytes(data, price, rom_addresses["Price_Master_Ball"])  # Money values in Red and Blue are weird

    for item in reversed(self.multiworld.precollected_items[self.player]):
        if data[rom_addresses["Start_Inventory"] + item.code - 172000000] < 255:
            data[rom_addresses["Start_Inventory"] + item.code - 172000000] += 1

    set_mon_palettes(self, random, data)

    for move_data in self.local_move_data.values():
        if move_data["id"] == 0:
            continue
        address = rom_addresses["Move_Data"] + ((move_data["id"] - 1) * 6)
        write_bytes(data, bytearray([move_data["id"], move_data["effect"], move_data["power"],
                    poke_data.type_ids[move_data["type"]], round(move_data["accuracy"] * 2.55), move_data["pp"]]), address)

    TM_IDs = bytearray([poke_data.moves[move]["id"] for move in self.local_tms])
    write_bytes(data, TM_IDs, rom_addresses["TM_Moves"])

    if self.multiworld.randomize_rock_tunnel[self.player]:
        seed = randomize_rock_tunnel(data, random)
        write_bytes(data, encode_text(f"SEED: <LINE>{seed}"), rom_addresses["Text_Rock_Tunnel_Sign"])

    mons = [mon["id"] for mon in poke_data.pokemon_data.values()]
    random.shuffle(mons)
    data[rom_addresses['Title_Mon_First']] = mons.pop()
    for mon in range(0, 16):
        data[rom_addresses['Title_Mons'] + mon] = mons.pop()
    if self.multiworld.game_version[self.player].value:
        mons.sort(key=lambda mon: 0 if mon == self.multiworld.get_location("Oak's Lab - Starter 1", self.player).item.name
                  else 1 if mon == self.multiworld.get_location("Oak's Lab - Starter 2", self.player).item.name else
                  2 if mon == self.multiworld.get_location("Oak's Lab - Starter 3", self.player).item.name else 3)
    else:
        mons.sort(key=lambda mon: 0 if mon == self.multiworld.get_location("Oak's Lab - Starter 2", self.player).item.name
                  else 1 if mon == self.multiworld.get_location("Oak's Lab - Starter 1", self.player).item.name else
                  2 if mon == self.multiworld.get_location("Oak's Lab - Starter 3", self.player).item.name else 3)
    write_bytes(data, encode_text(self.multiworld.seed_name[-20:], 20, True), rom_addresses['Title_Seed'])

    slot_name = self.multiworld.player_name[self.player]
    slot_name.replace("@", " ")
    slot_name.replace("<", " ")
    slot_name.replace(">", " ")
    write_bytes(data, encode_text(slot_name, 16, True, True), rom_addresses['Title_Slot_Name'])

    if self.trainer_name == "choose_in_game":
        data[rom_addresses["Skip_Player_Name"]] = 0
    else:
        write_bytes(data, self.trainer_name, rom_addresses['Player_Name'])
    if self.rival_name == "choose_in_game":
        data[rom_addresses["Skip_Rival_Name"]] = 0
    else:
        write_bytes(data, self.rival_name, rom_addresses['Rival_Name'])

    data[0xFF00] = 2  # client compatibility version
    rom_name = bytearray(f'AP{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0',
                         'utf8')[:21]
    rom_name.extend([0] * (21 - len(rom_name)))
    write_bytes(data, rom_name, 0xFFC6)
    write_bytes(data, self.multiworld.seed_name.encode(), 0xFFDB)
    write_bytes(data, self.multiworld.player_name[self.player].encode(), 0xFFF0)

    self.finished_level_scaling.wait()

    write_quizzes(self, data, random)

    for location in self.multiworld.get_locations(self.player):
        if location.party_data:
            for party in location.party_data:
                if not isinstance(party["party_address"], list):
                    addresses = [rom_addresses[party["party_address"]]]
                    parties = [party["party"]]
                else:
                    addresses = [rom_addresses[address] for address in party["party_address"]]
                    parties = party["party"]
                levels = party["level"]
                for address, party in zip(addresses, parties):
                    if isinstance(levels, int):
                        data[address] = levels
                        address += 1
                        for mon in party:
                            data[address] = poke_data.pokemon_data[mon]["id"]
                            address += 1
                    else:
                        address += 1
                        for level, mon in zip(levels, party):
                            data[address] = level
                            data[address + 1] = poke_data.pokemon_data[mon]["id"]
                            address += 2
                    assert data[address] == 0 or location.name == "Fossil Level - Trainer Parties"
            continue
        elif location.rom_address is None:
            continue
        if location.item and location.item.player == self.player:
            if location.rom_address:
                rom_address = location.rom_address
                if not isinstance(rom_address, list):
                    rom_address = [rom_address]
                for address in rom_address:
                    if location.item.name in poke_data.pokemon_data.keys():
                        data[address] = poke_data.pokemon_data[location.item.name]["id"]
                    elif " ".join(location.item.name.split()[1:]) in poke_data.pokemon_data.keys():
                        data[address] = poke_data.pokemon_data[" ".join(location.item.name.split()[1:])]["id"]
                    else:
                        item_id = self.item_name_to_id[location.item.name] - 172000000
                        if item_id > 255:
                            item_id -= 256
                        data[address] = item_id
                    if location.level:
                        data[location.level_address] = location.level

        else:
            rom_address = location.rom_address
            if not isinstance(rom_address, list):
                rom_address = [rom_address]
            for address in rom_address:
                data[address] = 0x2C  # AP Item

    outfilepname = f'_P{self.player}'
    outfilepname += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}" \
        if self.multiworld.player_name[self.player] != 'Player%d' % self.player else ''
    rompath = os.path.join(output_directory, f'AP_{self.multiworld.seed_name}{outfilepname}.gb')
    with open(rompath, 'wb') as outfile:
        outfile.write(data)
    if self.multiworld.game_version[self.player].current_key == "red":
        patch = RedDeltaPatch(os.path.splitext(rompath)[0] + RedDeltaPatch.patch_file_ending, player=self.player,
                              player_name=self.multiworld.player_name[self.player], patched_path=rompath)
    else:
        patch = BlueDeltaPatch(os.path.splitext(rompath)[0] + BlueDeltaPatch.patch_file_ending, player=self.player,
                               player_name=self.multiworld.player_name[self.player], patched_path=rompath)

    patch.write()
    os.unlink(rompath)


def write_bytes(data, byte_array, address):
    for byte in byte_array:
        data[address] = byte
        address += 1


def get_base_rom_bytes(game_version: str, hash: str="") -> bytes:
    file_name = get_base_rom_path(game_version)
    with open(file_name, "rb") as file:
        base_rom_bytes = bytes(file.read())
    if hash:
        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if hash != basemd5.hexdigest():
            raise Exception(f"Supplied Base Rom does not match known MD5 for Pokémon {game_version.title()} UE "
                            "release. Get the correct game and version, then dump it")
    return base_rom_bytes


def get_base_rom_path(game_version: str) -> str:
    options = Utils.get_options()
    file_name = options["pokemon_rb_options"][f"{game_version}_rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


class BlueDeltaPatch(APDeltaPatch):
    patch_file_ending = ".apblue"
    hash = "50927e843568814f7ed45ec4f944bd8b"
    game_version = "blue"
    game = "Pokemon Red and Blue"
    result_file_ending = ".gb"
    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes(cls.game_version, cls.hash)


class RedDeltaPatch(APDeltaPatch):
    patch_file_ending = ".apred"
    hash = "3d45c1ee9abd5738df46d2bdda8b57dc"
    game_version = "red"
    game = "Pokemon Red and Blue"
    result_file_ending = ".gb"
    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes(cls.game_version, cls.hash)
