from .Planets import *


class Addresses:
    def __init__(self, game_version: str):
        if game_version == "SCUS-97268":
            # Global addresses
            self.controller_input: int = 0x138320
            # self.endako_ratchet_freed: int = 0x1395C0
            # self.endako_apartment_visited: int = 0x1395C1
            # self.thermanator_tutorial_complete: int = 0x1395CA
            # self.bought_from_worker_bots: int = 0x1395CD
            # self.ship_shack_discovered: int = 0x1395CF
            self.weapon_subid_table = 0x139568
            # self.dobbo_defeat_thug_leader: int = 0x1395E6
            # self.electrolyzer_battle_victories: int = 0x1395E9
            # self.barlow_hoverbike_race_victories: int = 0x139605
            # self.joba_hoverbike_1_victories: int = 0x13960F
            self.feltzin_challenge_wins: int = 0x139619
            self.hrugis_challenge_wins: int = 0x13961E
            self.gorn_challenge_wins: int = 0x139623
            self.hypnomatic_part1: int = 0x13963C
            self.hypnomatic_part2: int = 0x13963E
            self.hypnomatic_part3: int = 0x139641
            self.current_ammo_table: int = 0x139688
            # self.unlocked_movie_field0: int = 0x139768
            # self.unlocked_movie_field1: int = 0x13976C
            # self.unlocked_movie_field2: int = 0x139770
            # self.siberius_thief_defeated: int = 0x139771
            self.cutscene_flags = [
                (0x13977E, 0x80),  # Flight cutscene on Maktar unlocked
                (0x139783, 0x08),  # First flight to Boldan special cutscene
                (0x13978C, 0x80),  # Cutscene when meeting Oozla scientist
                (0x1397AC, 0x10),  # Feltzin entrance cutscene
                (0x1397BE, 0x30),  # Tabora entrance cutscene
                (0x1397BA, 0x08),  # Tabora entrance cutscene
                (0x1397D1, 0x01),  # Hrugis entrance cutscene
                (0x1397E8, 0x02),  # Gorn entrance cutscene
                (0x1397B1, 0x02),  # Notak entrance cutscene
                (0x139811, 0x08),  # Flight cutscene on Gorn unlocked
                (0x139815, 0x60),  # Flight cutscene on Tabora unlocked
                (0x139815, 0x80),  # Flight cutscene on Boldan unlocked
            ]
            self.current_weapon_xp_table: int = 0x139868
            self.selectable_planets: int = 0x139948

            self.ratchet_position: int = 0x189EA0
            # self.held_weapon: int = 0x18B068
            self.current_moby_instance_pointer: int = 0x18C0B0
            self.ratchet_state: int = 0x18C0B4
            self.current_nanotech: int = 0x18C2EC
            self.clank_disabled: int = 0x18C31C

            self.platinum_bolt_table: int = 0x19B278
            # self.checkpoint_data: int = 0x19B2E8
            self.enemy_kill_count_table: int = 0x19B4A8

            self.equipped_weapon: int = 0x1A7398
            self.quickselect: int = 0x1A73B8
            self.easy_cutscene_skip: int = 0x1A7478
            self.current_planet: int = 0x1A79F0
            self.current_bolts: int = 0x1A79F8
            # self.raritanium_count: int = 0x1A79FC
            # self.challenge_mode_flag: int = 0x1A7A0A
            # self.current_ratchet_xp: int = 0x1A7A0C
            self.current_armor_level: int = 0x1A7A18
            self.nanotech_boost_table: int = 0x1A7A28
            # self.current_bolt_multiplier: int = 0x1A7A32
            # self.skill_point_table: int = 0x1A7A60
            # self.ship_upgrades: int = 0x1A7AF0
            self.inventory: int = 0x1A7AF8
            self.secondary_inventory: int = 0x1A7B30
            self.vendor_list: int = 0x1A7B68
            # self.savefile_play_time: int = 0x1A7BC0
            self.unlocked_planets: int = 0x1A7BC8
            self.loaded_flag: int = 0x1A7BE5
            self.highlighted_planets: int = 0x1A7BE8
            self.wupash_complete_flag: int = 0x1A7C01

            # Pause state is at 0x1A8F00 on all planets except for Oozla where it's at 0x1A8F40.
            self.pause_state: int = 0x1A8F00
            self.oozla_pause_state: int = 0x1A8F40

            # Addresses for data that only exists on certain planets
            # self.oozla_box_breaker_func: int = 0x416440
            # self.endako_free_ratchet_func: int = 0x3D20F8
            # self.hrugis_race_controller_func: int = 0x42D1F0

            # Addresses for data that exists on all/most planets but has a different address per planet
            self.planet: Dict[int, PlanetAddresses] = {
                -1: PlanetAddresses(
                    segment_pointers=0x1BAEC0,
                ),
                ARANOS_TUTORIAL.number: PlanetAddresses(
                    segment_pointers=0x1BF140,
                ),
                OOZLA.number: PlanetAddresses(
                    segment_pointers=0x1BF840,
                    planet_switch_trigger=0x1A8F14,
                    next_planet=0x1B2080,
                    skill_point_text=0x1A900A0,
                    spaceish_wars_func=0x3B0598,
                    display_skill_point_message_func=0x31BEC0,
                    equipment_data=0x2637A0,
                    vendor_slot_table=0x230000,
                ),
                MAKTAR_NEBULA.number: PlanetAddresses(
                    segment_pointers=0x1C0880,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B30C0,
                    skill_point_text=0x1B9A310,
                    spaceish_wars_func=0x3C1128,
                    display_skill_point_message_func=0x32B018,
                    equipment_data=0x264A70,
                    vendor_slot_table=0x231040,
                ),
                ENDAKO.number: PlanetAddresses(
                    segment_pointers=0x1BFD00,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2540,
                    skill_point_text=0x1C66600,
                    spaceish_wars_func=0x3BD338,
                    display_skill_point_message_func=0x326870,
                    equipment_data=0x266da0,
                    vendor_slot_table=0x230580,
                ),
                BARLOW.number: PlanetAddresses(
                    segment_pointers=0x1BFA00,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2000,
                    skill_point_text=0x1C8DF50,
                    spaceish_wars_func=0x3DDE78,
                    display_skill_point_message_func=0x348848,
                    equipment_data=0x27B470,
                    vendor_slot_table=0x2301C0,
                ),
                FELTZIN_SYSTEM.number: PlanetAddresses(
                    segment_pointers=0x1BFA40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2040,
                    skill_point_text=0x1874090,
                    camara_state=0x1B1B20,
                    spaceish_wars_func=0x3CB760,
                    display_skill_point_message_func=0x33CD60,
                    equipment_data=0x278A70,
                ),
                NOTAK.number: PlanetAddresses(
                    segment_pointers=0x1BFBC0,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2340,
                    skill_point_text=0x1C726D0,
                    spaceish_wars_func=0x3FEED0,
                    display_skill_point_message_func=0x3662A0,
                    equipment_data=0x26c7f0,
                    vendor_slot_table=0x230380,
                ),
                SIBERIUS.number: PlanetAddresses(
                    segment_pointers=0x1BF580,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B1E00,
                    skill_point_text=0x1981130,
                    spaceish_wars_func=0x3AD8E8,
                    display_skill_point_message_func=0x31CBC8,
                    equipment_data=0x2628A0,
                    vendor_slot_table=0x22FD40,
                ),
                TABORA.number: PlanetAddresses(
                    segment_pointers=0x1BFE80,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2500,
                    skill_point_text=0x1C601C0,
                    spaceish_wars_func=0x3CAEF0,
                    display_skill_point_message_func=0x334920,
                    equipment_data=0x26CCF0,
                    vendor_slot_table=0x230640,
                ),
                DOBBO.number: PlanetAddresses(
                    segment_pointers=0x1BFD80,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2380,
                    skill_point_text=0x1CCE990,
                    spaceish_wars_func=0x3B9790,
                    display_skill_point_message_func=0x3226B8,
                    equipment_data=0x2651F0,
                    vendor_slot_table=0x230540,
                ),
                HRUGIS_CLOUD.number: PlanetAddresses(
                    segment_pointers=0x1BFA00,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2040,
                    skill_point_text=0x1649420,
                    camara_state=0x1B1B20,
                    spaceish_wars_func=0x3CDE80,
                    display_skill_point_message_func=0x33EAC0,
                    equipment_data=0x27AE70,
                ),
                JOBA.number: PlanetAddresses(
                    segment_pointers=0x1C0C40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B30C0,
                    skill_point_text=0x1C4EAD0,
                    spaceish_wars_func=0x3CDC88,
                    display_skill_point_message_func=0x3384D8,
                    equipment_data=0x279BA0,
                    vendor_slot_table=0x231400,
                ),
                TODANO.number: PlanetAddresses(
                    segment_pointers=0x1C0180,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B29C0,
                    skill_point_text=0x1C44EF0,
                    spaceish_wars_func=0x3BF8A0,
                    display_skill_point_message_func=0x3297E8,
                    equipment_data=0x2636F0,
                    vendor_slot_table=0x230940,
                ),
                BOLDAN.number: PlanetAddresses(
                    segment_pointers=0x1BFC40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2440,
                    skill_point_text=0x1CCBA00,
                    spaceish_wars_func=0x3C3688,
                    display_skill_point_message_func=0x32F340,
                    equipment_data=0x26D270,
                    vendor_slot_table=0x230400,
                ),
                ARANOS_PRISON.number: PlanetAddresses(
                    segment_pointers=0x1BF880,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B20C0,
                    skill_point_text=0x1B5A240,
                    spaceish_wars_func=0x3C2F78,
                    display_skill_point_message_func=0x32E0B8,
                    equipment_data=0x2686F0,
                    vendor_slot_table=0x230040,
                ),
                GORN.number: PlanetAddresses(
                    segment_pointers=0x1BFB40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2140,
                    skill_point_text=0x16734E0,
                    camara_state=0x1B1BF0,
                    spaceish_wars_func=0x3D22C0,
                    display_skill_point_message_func=0x33E460,
                    equipment_data=0x276FF0,
                ),
                SNIVELAK.number: PlanetAddresses(
                    segment_pointers=0x1BFE80,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2640,
                    skill_point_text=0x1CD5660,
                    spaceish_wars_func=0x3B4828,
                    display_skill_point_message_func=0x31E9E8,
                    equipment_data=0x263DA0,
                    vendor_slot_table=0x230640,
                ),
                SMOLG.number: PlanetAddresses(
                    segment_pointers=0x1BFF40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2740,
                    skill_point_text=0x1CEA930,
                    spaceish_wars_func=0x3BE100,
                    display_skill_point_message_func=0x327FA8,
                    equipment_data=0x263470,
                    vendor_slot_table=0x230700,
                ),
                DAMOSEL.number: PlanetAddresses(
                    segment_pointers=0x1BFB40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2340,
                    skill_point_text=0x1C6B7F0,
                    spaceish_wars_func=0x3D7B40,
                    display_skill_point_message_func=0x340D18,
                    equipment_data=0x26BCF0,
                    vendor_slot_table=0x230300,
                ),
                GRELBIN.number: PlanetAddresses(
                    segment_pointers=0x1BFDC0,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2500,
                    skill_point_text=0x1C49920,
                    spaceish_wars_func=0x3BA820,
                    display_skill_point_message_func=0x323968,
                    equipment_data=0x265870,
                    vendor_slot_table=0x230580,
                ),
                YEEDIL.number: PlanetAddresses(
                    segment_pointers=0x1C0340,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2AC0,
                    skill_point_text=0x1C1B010,
                    spaceish_wars_func=0x3D6F20,
                    display_skill_point_message_func=0x33B2A8,
                    equipment_data=0x26D970,
                    vendor_slot_table=0x230B00,
                ),
                DOBBO_ORBIT.number: PlanetAddresses(
                    segment_pointers=0x1C0000,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B1C40,
                    skill_point_text=0x168B7D0,
                    spaceish_wars_func=0x3C3AA0,
                    display_skill_point_message_func=0x32AE80,
                ),
                DAMOSEL_ORBIT.number: PlanetAddresses(
                    segment_pointers=0x1C09C0,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B22C0,
                    skill_point_text=0x150F110,
                    spaceish_wars_func=0x3CB7A0,
                    display_skill_point_message_func=0x32F598,
                ),
                SHIP_SHACK.number: PlanetAddresses(
                    segment_pointers=0x1BEA40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B12C0,
                    skill_point_text=0xEDE4B0,
                    spaceish_wars_func=0x3AB298,
                    display_skill_point_message_func=0x321FD8,
                ),
                WUPASH_NEBULA.number: PlanetAddresses(
                    segment_pointers=0x1BF580,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B1BC0,
                    skill_point_text=0xE13140,
                    camara_state=0x1B1670,
                    spaceish_wars_func=0x3C4400,
                    display_skill_point_message_func=0x336F08,
                ),
                JAMMING_ARRAY.number: PlanetAddresses(
                    segment_pointers=0x1BEF00,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B1740,
                    skill_point_text=0x1171FF0,
                    spaceish_wars_func=0x3B5748,
                    display_skill_point_message_func=0x325908,
                ),
                INSOMNIAC_MUSEUM.number: PlanetAddresses(
                    segment_pointers=0x1C0140,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2840,
                ),
            }

            ################################################
            #  Custom addresses
            ################################################

            # We use secondary inventory for unused weapons to store "global" data that needs to be saved to memcard
            self.platinum_bolt_count: int = self.secondary_inventory + 0x0F     # Unused weapon 1
            self.nanotech_boost_count: int = self.secondary_inventory + 0x22    # Unused weapon 2
            self.hypnomatic_part_count: int = self.secondary_inventory + 0x23   # Unused weapon 3
            self.bolt_pack_count: int = self.secondary_inventory + 0x28         # Unused weapon 4

            # Put the new Tabora wrench cutscene flag inside the platinum bolt table for Tabora so it gets saved along
            # other planet specific data
            self.tabora_wrench_cutscene_flag: int = self.platinum_bolt_table + (TABORA.number * 4) + 3
            # Put the new Aranos Prison wrench cutscene flag inside the platinum bolt table for Aranos so it gets
            # saved along other planet specific data
            self.aranos_wrench_cutscene_flag: int = self.platinum_bolt_table + (ARANOS_PRISON.number * 4) + 1

            # The "enemy kill count table" is a 0x400 table for each, holding the number of times two enemies were
            # killed (one in the upper half, the other in the lower half of the byte).
            # We use Feltzin's table as a spot to put temporary data, since spaceship systems don't use that mechanic
            # at all but still have that table.
            self.temporary_data_table: int = self.enemy_kill_count_table + (FELTZIN_SYSTEM.number * 0x400)
            self.custom_text_notification_trigger: int = self.temporary_data_table


class PlanetAddresses(NamedTuple):
    segment_pointers: Optional[int] = None
    planet_switch_trigger: Optional[int] = None
    next_planet: Optional[int] = None
    skill_point_text: Optional[int] = None
    camara_state: Optional[int] = None
    spaceish_wars_func: Optional[int] = None
    display_skill_point_message_func: Optional[int] = None
    equipment_data: Optional[int] = None
    vendor_slot_table: Optional[int] = None
