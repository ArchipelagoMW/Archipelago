import os
import pkgutil
import struct
import typing
from collections.abc import Callable

from settings import get_settings

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from .options import Laws, StatGrowth

from .data import (FFTAData, UnitOffsets, MissionOffsets, JobOffsets, JobID, ItemOffsets, laws, music_id,
                   music_addresses, human_abilities, nu_mou_abilities, bangaa_abilities, viera_abilities,
                   moogle_abilities, get_random_job)
from .items import (MissionUnlockItems)
from .fftaabilities import master_abilities, get_job_abilities, set_mastered_ability
from .fftautils import textDict


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().ffta_options.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes


class FFTAProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Final Fantasy Tactics Advance"
    hash = "cd99cdde3d45554c1b36fbeb8863b7bd"
    patch_file_ending = ".apffta"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_bsdiff4", ["progressive_shop_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def unlock_mission(ffta_data, index: int, patch: FFTAProcedurePatch):
    patch.write_token(APTokenTypes.WRITE, ffta_data.missions[index].memory + MissionOffsets.unlockflag1,
                      bytes([0x00, 0x00, 0x00]))
    patch.write_token(APTokenTypes.WRITE, ffta_data.missions[index].memory + MissionOffsets.unlockflag2,
                      bytes([0x00, 0x00, 0x00]))
    patch.write_token(APTokenTypes.WRITE, ffta_data.missions[index].memory + MissionOffsets.unlockflag3,
                      bytes([0x00, 0x00, 0x00]))


def randomize_unit(ffta_data, index: int, world, patch: FFTAProcedurePatch):
    # These were all 2 before, changing to 1 to see
    patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.job,
                      struct.pack("<H", world.randomized_jobs[index]))
    patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.unit_item1,
                      struct.pack("<H", world.randomized_weapons[index]))
    patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.unit_item2,
                      struct.pack("<H", world.randomized_equip[index]))
    patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.unit_item3,
                      bytes([0x00, 0x00]))


def randomize_judge(ffta_data, index: int, random_index: int, world, patch: FFTAProcedurePatch):
    # Randomizing the judge encounters
    # Remove later
    patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.job,
                      struct.pack("<H", world.randomized_judge[random_index]))
    patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.unit_item1,
                      struct.pack("<H", world.judge_weapon[random_index]))
    patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.unit_item2,
                      struct.pack("<H", world.judge_equip[random_index]))
    patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.unit_item3, bytes([0x00]))


def generate_output(world, player: int, output_directory: str, player_names) -> None:
    patch = FFTAProcedurePatch(player=player, player_name=world.multiworld.player_name[player])

    patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "ffta_data/base_patch.bsdiff4"))
    patch.write_file("progressive_shop_patch.bsdiff4",
                     pkgutil.get_data(__name__, "ffta_data/progressive_shop_patch.bsdiff4"))

    ffta_data = FFTAData()

    # Fix Present day
    patch.write_token(APTokenTypes.WRITE, 0x563b79, bytes([0x4b]))

    # Skip cutscenes, maybe move this into the diff file later
    patch.write_token(APTokenTypes.WRITE, 0x9a87d9, bytes([0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9a8c4c, bytes([0x1a, 0x02, 0x02, 0x01, 0x1d, 0x04, 0x17, 0x05]))
    patch.write_token(APTokenTypes.WRITE, 0x9a9784, bytes([0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9a9a7c, bytes([0x17, 0x05]))
    patch.write_token(APTokenTypes.WRITE, 0x9a9f48, bytes([0x1a, 0x04, 0x02, 0x01, 0x1d, 0x06, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9aa198, bytes([0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9aa88a, bytes([0x1a, 0x05, 0x02, 0x01, 0x1d, 0x07, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9ab0b9, bytes([0x1a, 0x06, 0x02, 0x01, 0x1d, 0x08, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9ab656, bytes([0x17, 0x05]))
    patch.write_token(APTokenTypes.WRITE, 0x9abce5, bytes([0x1a, 0x07, 0x02, 0x01, 0x1d, 0x09, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9ac2bc, bytes([0x1a, 0x08, 0x02, 0x01, 0x1d, 0x0a, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9ac7ef, bytes([0x1a, 0x09, 0x02, 0x01, 0x1d, 0x0b, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9ace68, bytes([0x1a, 0x0a, 0x02, 0x01, 0x1d, 0x0c, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9ad3dc, bytes([0x1a, 0x0b, 0x02, 0x01, 0x1d, 0x0d, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9ad89b, bytes([0x1a, 0x0c, 0x02, 0x01, 0x1d, 0x0e, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9adbc3, bytes([0x17, 0x05]))
    patch.write_token(APTokenTypes.WRITE, 0x9ae0e6, bytes([0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9af115, bytes([0x1a, 0x0f, 0x02, 0x01, 0x1d, 0x12, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9af74c, bytes([0x17, 0x05]))
    patch.write_token(APTokenTypes.WRITE, 0x9afe8d,
                      bytes([0x1a, 0x10, 0x02, 0x01, 0x1d, 0x13, 0x0d, 0x1c, 0x38, 0x00, 0x17, 0x02]))

    patch.write_token(APTokenTypes.WRITE, 0x9b07e4, bytes([0x1e, 0x03, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9b0b76, bytes([0x1a, 0x11, 0x02, 0x01, 0x1d, 0x14, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9b12b4, bytes([0x1a, 0x12, 0x02, 0x01, 0x1d, 0x15, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9b19c8, bytes([0x1a, 0x13, 0x02, 0x01, 0x1d, 0x16, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9b2694, bytes([0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9b2915, bytes([0x1a, 0x15, 0x02, 0x01, 0x1d, 0x18, 0x17, 0x05]))
    patch.write_token(APTokenTypes.WRITE, 0x9b2915, bytes([0x1a, 0x16, 0x02, 0x01, 0x1d, 0x19, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9b45c0, bytes([0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9b4750, bytes([0x1a, 0x18, 0x02, 0x01, 0x1d, 0x1b, 0x17, 0x05]))
    patch.write_token(APTokenTypes.WRITE, 0x9b4848, bytes([0x17, 0x05]))
    patch.write_token(APTokenTypes.WRITE, 0x9b4e2f, bytes([0x1a, 0x19, 0x02, 0x01, 0x1d, 0x1c, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9b52de, bytes([0x17, 0x05]))
    patch.write_token(APTokenTypes.WRITE, 0x9b5835, bytes([0x1a, 0x1a, 0x02, 0x01, 0x1d, 0x1d, 0x17, 0x05]))

    patch.write_token(APTokenTypes.WRITE, 0x9b5835, bytes([0x1a, 0x1b, 0x02, 0x01, 0x1d, 0x1e, 0x17, 0x05]))

    # Enable random clan battles
    patch.write_token(APTokenTypes.WRITE, 0xcf802, bytes([0x28, 0x04]))
    patch.write_token(APTokenTypes.WRITE, 0xcf807, bytes([0x0F]))

    # Set max level to 99
    patch.write_token(APTokenTypes.WRITE, 0x0c9bae, bytes([0x63]))
    patch.write_token(APTokenTypes.WRITE, 0x0c9baa, bytes([0x63]))
    patch.write_token(APTokenTypes.WRITE, 0x12e672, bytes([0x62]))

    # Remove judges / laws if option is selected
    if world.options.laws == Laws.option_disable_laws:
        patch.write_token(APTokenTypes.WRITE, 0xBAC5A, bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE, 0xBAC5B, bytes([0x20]))
        patch.write_token(APTokenTypes.WRITE, 0xBC7BE, bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE, 0xBC7BF, bytes([0x20]))
        patch.write_token(APTokenTypes.WRITE, 0xCED86, bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE, 0xCED87, bytes([0x20]))

    # Randomize the laws found in the different law sets
    if world.options.laws == Laws.option_random_laws:
        law_memory = 0x528e1c
        law_offset = 0

        shuffled_laws = laws.copy()
        world.random.shuffle(shuffled_laws)
        for i in range(140):
            patch.write_token(APTokenTypes.WRITE, law_memory + law_offset, bytes([shuffled_laws[i]]))
            law_offset = law_offset + 2

    # Set quick options to on
    if world.options.quick_options.value == 1:
        patch.write_token(APTokenTypes.WRITE, 0x51ba4e, bytes([0xc8, 0x03]))

    if world.options.fast_receive.value == 1:
        patch.write_token(APTokenTypes.WRITE, 0x0003a1cc, bytes([0x04, 0xE0]))
        patch.write_token(APTokenTypes.WRITE, 0x0003a1f2, bytes([0x00, 0xE0]))
        patch.write_token(APTokenTypes.WRITE, 0x0003a0dc, bytes([0xA6, 0xE0]))
        patch.write_token(APTokenTypes.WRITE, 0x0003a6c0, bytes([0x00, 0xE0]))

    # Guarantee recruitment option
    if world.options.force_recruitment.value == 1 or world.options.force_recruitment.value == 2 \
            or world.options.force_recruitment.value == 3:
        patch.write_token(APTokenTypes.WRITE, 0xd2494, bytes([0x00, 0x20]))

    # Scale to the highest unit
    if world.options.scaling.value == 1:
        patch.write_token(APTokenTypes.WRITE, 0xca088, bytes([0x50, 0x79, 0xa0, 0x42]))

        patch.write_token(APTokenTypes.WRITE, 0xca08d, bytes([0xdd, 0x04, 0x1c, 0x00, 0x00, 0x00, 0x00]))
        patch.write_token(APTokenTypes.WRITE, 0xca0aa, bytes([0x20, 0x1c]))

    if world.options.exp_multiplier.value > 0:
        base_opcode = 0x0825  # lsr r5, r4, 0 (Logical left shift register 4 by 0 into register 5)
        exponent = world.options.exp_multiplier.value  # Base is 2. Exponent of 12+ will cause overflow-ish behaviour
        shiftby = 0x10 - exponent
        opcode = base_opcode | (shiftby << 6)  # lsr r5, r4, shiftby
        patch.write_token(APTokenTypes.WRITE, 0x12e658, struct.pack("<H", opcode))

    # Make all missions game over instead of fail
    # patch.write_token(APTokenTypes.WRITE, 0x122258, 2, 0x2001)

    # This works for removing all missions, maybe do this in the diff file
    if isinstance(world.options.gil_rewards.value, int):
        gil_reward = struct.pack("<B", int(world.options.gil_rewards.value / 200))
        randomized_gil = False
    else:
        random_func_dict: dict[str, Callable[[], int]] = {
            "individually-randomized": lambda: world.random.randint(1, 255),
            "individually-randomized-low": lambda: int(round(world.random.triangular(1, 255, 1), 0)),
            "individually-randomized-middle": lambda: int(round(world.random.triangular(1, 255), 0)),
            "individually-randomized-high": lambda: int(round(world.random.triangular(1, 255, 255), 0)),
        }
        get_random_reward = random_func_dict[world.options.gil_rewards.value]
        randomized_gil = True
    for mission in ffta_data.missions:
        if randomized_gil:
            gil_reward = struct.pack("<B", get_random_reward())

        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.unlockflag1, bytes([0x02]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.unlockflag1 + 1, bytes([0x03]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.unlockflag1 + 2, bytes([0x01]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.unlockflag2, bytes([0x02]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.unlockflag2 + 1, bytes([0x03]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.unlockflag2 + 2, bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.unlockflag3, bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.unlockflag3 + 1, bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.unlockflag3 + 2, bytes([0x00]))

        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.rank, bytes([0x30, 0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.ap_reward, bytes([0x05]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.gil_reward, gil_reward)
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.rewardItem1, bytes([0x00, 0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.rewardItem2, bytes([0x00, 0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.cardItem1, bytes([0x00, 0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.cardItem2, bytes([0x00, 0x00]))
        # patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.clan_reward, 0x0A)
        # patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.clan_reward + 0x07, 0x0A)

        if world.options.force_recruitment.value == 1 or world.options.force_recruitment.value == 3 \
                and mission.recruit < 0x8a:
            random_recruit = world.random.choice(world.recruit_units)
            patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.recruit,
                              bytes([random_recruit]))

        elif world.options.force_recruitment.value == 2:
            random_recruit = world.random.choice(world.recruit_secret)

            # Remove from list if it's a secret unit
            if random_recruit >= 0x8a:
                world.recruit_secret.remove(random_recruit)

            patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.recruit,
                              bytes([random_recruit]))

        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.required_item1, bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.required_item2, bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.price, bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.pub_visibility, bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.days_available, bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.timeout_days, bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.required_job, bytes([0x00, 0x00]))
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.required_skill, bytes([0x00, 0x00]))

        # Make all dispatch missions guarantee success
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.dispatch_ability, bytes([0x00, 0x00]))

        # Hiding mission rewards with ??? bags, also making missions not cancelable
        patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.mission_display, bytes([0xC0]))

        # Hide ??? cards
        # patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.mission_display + 1, bytes([0x00]))
        # Show extra items if enabled
        reward_display = 0x00 if world.options.mission_reward_num.value == 2 \
            else 0x01 if world.options.mission_reward_num.value == 3 \
            else 0x03

        patch.write_token(APTokenTypes.WRITE,
                          mission.memory + MissionOffsets.mission_display + 1,
                          bytes([reward_display]))

        # patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.type, 2, 0x00)
        if mission.mission_type == 0x0D:
            patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.type, bytes([0x0A]))

        # Dispatch missions
        elif mission.mission_type == 0x00:
            patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.type, bytes([0x00]))
            patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.dispatch_ability, bytes([0x00]))
        #    patch.write_token(APTokenTypes.WRITE, mission.memory + 0x10, 1, 0x03)

        elif mission.mission_type == 0x02:
            patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.type, bytes([0x02]))

        # Make free missions all dispatch missions for now. mission.other is the win condition. Maybe randomize for dispatch missions later?
        elif mission.mission_type >= 0x10 and mission.other != 0x00:
            patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.type, bytes([0x00]))
            patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.dispatch_ability, bytes([0x00]))

        else:
            # was 0x0A before
            patch.write_token(APTokenTypes.WRITE, mission.memory + MissionOffsets.type, bytes([0x0A]))

    # Job unlock options
    # Unlock all jobs
    if world.options.job_unlock_req.value == 1:
        for jobs in ffta_data.jobs:
            patch.write_token(APTokenTypes.WRITE, jobs.memory + JobOffsets.job_requirement, bytes([0x00]))

    # Lock all jobs
    elif world.options.job_unlock_req.value == 2 or world.options.job_unlock_req.value == 3:
        for jobs in ffta_data.jobs:
            patch.write_token(APTokenTypes.WRITE, jobs.memory + JobOffsets.job_requirement, bytes([0xFF]))

    # Unlock starting job based on if the requirements are vanilla and units are randomized
    if world.options.job_unlock_req.value == 0 and world.options.starting_units.value == 1 or \
            world.options.job_unlock_req.value == 0 and world.options.starting_units.value == 2 or \
            world.options.job_unlock_req.value == 0 and world.options.starting_units.value == 3:
        patch.write_token(APTokenTypes.WRITE,
                          ffta_data.jobs[world.randomized_jobs[0]].memory + JobOffsets.job_requirement,
                          bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE,
                          ffta_data.jobs[world.randomized_jobs[1]].memory + JobOffsets.job_requirement,
                          bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE,
                          ffta_data.jobs[world.randomized_jobs[2]].memory + JobOffsets.job_requirement,
                          bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE,
                          ffta_data.jobs[world.randomized_jobs[3]].memory + JobOffsets.job_requirement,
                          bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE,
                          ffta_data.jobs[world.randomized_jobs[4]].memory + JobOffsets.job_requirement,
                          bytes([0x00]))
        patch.write_token(APTokenTypes.WRITE,
                          ffta_data.jobs[world.randomized_jobs[5]].memory + JobOffsets.job_requirement,
                          bytes([0x00]))

    # All abilities cost 0
    # for abilities in ffta_data.abilities:
    #    patch.write_token(APTokenTypes.WRITE, abilities.memory + AbilityOffsets.mp_cost, 1, 0x00)

    gate_number = world.options.gate_num.value
    if gate_number > 30 and world.options.goal.value == 1:
        gate_number = 30

    set_up_gates(ffta_data, gate_number, world.options.gate_items.value,
                 world.options.goal.value, world.options.final_mission.value,
                 world.options.dispatch.value, world, patch)

    # Totema goal
    if world.options.goal.value == 1:
        unlock_mission(ffta_data, 4, patch)

        # Totema goal required items
        set_required_items(ffta_data, 4, 0x1d1, 0x00, patch)
        set_required_items(ffta_data, 7, 0x1d0, 0x00, patch)
        set_required_items(ffta_data, 10, 0x1d2, 0x00, patch)
        set_required_items(ffta_data, 14, 0x1d3, 0x00, patch)
        set_required_items(ffta_data, 17, 0x1c9, 0x00, patch)

        set_mission_requirement(ffta_data, 7, 4, patch)
        set_mission_requirement(ffta_data, 10, 7, patch)
        set_mission_requirement(ffta_data, 14, 10, patch)
        set_mission_requirement(ffta_data, 17, 14, patch)

        # Set Royal Valley to be the final mission if it is chosen in the options
        if world.options.final_mission.value == 0:
            set_mission_requirement(ffta_data, 23, 17, patch)

        # Set Decision Time to be the final mission
        elif world.options.final_mission.value == 1:
            set_mission_requirement(ffta_data, 393, 17, patch)

    if world.options.starting_special_chance.value > 0:

        for index in range(2, 6):
            # Have a chance to randomize to special unit

            special_unit = world.random.choice(world.special_units)
            world.special_units.remove(special_unit)
            special_chance = world.options.starting_special_chance.value / 10
            normal_unit_chance = 1 - special_chance
            unit_selected = world.random.choices(population=[special_unit, 0x01], weights=[special_chance, normal_unit_chance])

            patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory,
                              bytes([unit_selected[0]]))

            if unit_selected == special_unit:
                world.special_units.remove(special_unit)

    # Randomize starting units and set mastered abilities
    if world.options.starting_units.value != 0:
        for index in range(6):

            randomize_unit(ffta_data, index, world, patch)

            # Master all abilities if the unit is a monster type
            if world.randomized_jobs[index] >= 0x2C:
                master_abilities(ffta_data, index, get_job_abilities(world.randomized_jobs[index]),
                                 10, patch, world)
            else:
                master_abilities(ffta_data, index, get_job_abilities(world.randomized_jobs[index]),
                                 world.options.starting_abilities.value, patch, world)

            # Set the basic weapons and equipment if the option is selected
            if world.options.starting_unit_equip.value == 0:
                patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.unit_item1,
                                  struct.pack("<H", world.basic_weapon[index]))
                patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.unit_item2,
                                  struct.pack("<H", world.basic_equip[index]))
                patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.unit_item3,
                                  bytes([0x00, 0x00]))

    # Master abilities if units aren't randomized
    if world.options.starting_units.value == 0:
        master_abilities(ffta_data, 0, get_job_abilities(JobID.soldier),
                         world.options.starting_abilities.value, patch, world)

        master_abilities(ffta_data, 1, get_job_abilities(JobID.blackmagemog),
                         world.options.starting_abilities.value, patch, world)

        master_abilities(ffta_data, 2, get_job_abilities(JobID.soldier),
                         world.options.starting_abilities.value, patch, world)

        master_abilities(ffta_data, 3, get_job_abilities(JobID.whitemonk),
                         world.options.starting_abilities.value, patch, world)

        master_abilities(ffta_data, 4, get_job_abilities(JobID.whitemagemou),
                         world.options.starting_abilities.value, patch, world)

        master_abilities(ffta_data, 5, get_job_abilities(JobID.archervra),
                         world.options.starting_abilities.value, patch, world)

        if world.options.starting_unit_equip == 1:
            for index in range(6):
                patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.unit_item1,
                                  struct.pack("<H", world.randomized_weapons[index]))
                patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.unit_item2,
                                  struct.pack("<H", world.randomized_equip[index]))
                patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.unit_item3,
                                  bytes([0x00, 0x00]))

    # Randomize enemies

    for index in range(6, 0xA46):

        patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.level, bytes([0x00]))

        if world.options.randomize_enemies.value == 1:
            if ffta_data.formations[index].formation_type == 0x01:
                randomize_unit(ffta_data, index, world, patch)
                master_abilities(ffta_data, index, get_job_abilities(world.randomized_jobs[index]),
                                 world.random.randint(1, 10), patch, world)

                # Disable reaction and support abilities for now
                #patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.ability_reaction,
                #                  bytes([0x00]))
                #patch.write_token(APTokenTypes.WRITE, ffta_data.formations[index].memory + UnitOffsets.ability_support,
                #                  bytes([0x00]))

    # Randomize judge units when laws are disabled

    """
    if world.options.laws == 0:
        randomize_judge(ffta_data, 0xa10, 0, world, patch)
        randomize_judge(ffta_data, 0xa21, 1, world, patch)
        randomize_judge(ffta_data, 0xa30, 2, world, patch)
        randomize_judge(ffta_data, 0xa31, 3, world, patch)
        randomize_judge(ffta_data, 0xa32, 4, world, patch)

        # Have the judges master all the abilities
        master_abilities(ffta_data, 0xa10, get_job_abilities(world.randomized_judge[0]), 10, patch, world)
        master_abilities(ffta_data, 0xa21, get_job_abilities(world.randomized_judge[1]), 10, patch, world)
        master_abilities(ffta_data, 0xa30, get_job_abilities(world.randomized_judge[2]), 10, patch, world)
        master_abilities(ffta_data, 0xa31, get_job_abilities(world.randomized_judge[3]), 10, patch, world)
        master_abilities(ffta_data, 0xa32, get_job_abilities(world.randomized_judge[4]), 10, patch, world)

    """

    # Remove Llednar's weapon on present day to make it more survivable
    patch.write_token(APTokenTypes.WRITE, 0x52eaf8, bytes([0x00]))

    # Make Llednar not invincible
    patch.write_token(APTokenTypes.WRITE, 0x130870, struct.pack("<i", 0x00200000))

    # Remove Marche's combo ability
    patch.write_token(APTokenTypes.WRITE, 0x0CA066, bytes([0x00]))

    # Randomize locations on map
    for i in range(0, len(world.location_ids)):
        patch.write_token(APTokenTypes.WRITE, 0xb390dc + i, bytes([world.location_ids[i]]))

    set_items(world.multiworld, player, patch)

    write_progressive_lists(world, patch)
    write_progressive_shop(ffta_data, world, patch)
    write_display_only_items(patch)

    # Set the starting gil amount
    starting_gil = world.options.starting_gil.value
    patch.write_token(APTokenTypes.WRITE, 0x986c, struct.pack("<i", starting_gil))

    # Set slot name in rom
    # TO DO. Fix this to work on procedure patch
    # patch.write_token(APTokenTypes.WRITE, 0xAAABD0, world.multiworld.player_name[player].encode("utf-8"))

    # Set unit names from players in the multiworld

    if world.options.unit_names.value == 1:
        pointer_address = 0x5680DC
        name_address = 0xD00000

        # Check if player names exceed the number of unit name pointers
        if len(player_names) > 500:
            player_names = player_names[:500]

        for name in player_names:

            if len(name) > 12:
                name = name[:12]

            name_hex = []
            for char in name:
                if char in textDict:
                    name_hex.append(textDict[char])
                elif char == ' ':
                    name_hex.append(0xF0)
                else:
                    name_hex.append(0xEB)

            patch.write_token(APTokenTypes.WRITE, pointer_address, struct.pack("<i", (name_address + 0x8000000)))
            patch.write_token(APTokenTypes.WRITE, name_address, bytes([0x01]))
            patch.write_token(APTokenTypes.WRITE, name_address + 0x01, bytes(name_hex))
            patch.write_token(APTokenTypes.WRITE, name_address + len(name_hex) + 0x01, bytes([0x00]))
            # Update name and pointer addresses
            name_address += len(name_hex) + 0x02
            pointer_address += 0x04

    last_index = 0
    for i in range(0, len(human_abilities)):
        patch.write_token(APTokenTypes.WRITE, 0x51bb6c + (8 * i), bytes(world.all_abilities[i]))

        if world.options.ability_ap.value != 65:
            # Set AP
            patch.write_token(APTokenTypes.WRITE, 0x51bb6c + (8 * i) + 0x07, bytes([world.options.ability_ap.value]))
        last_index += 1

    for i in range(0, len(bangaa_abilities)):
        patch.write_token(APTokenTypes.WRITE, 0x51bfdc + (8 * i), bytes(world.all_abilities[last_index]))

        if world.options.ability_ap.value != 65:
            # Set AP
            patch.write_token(APTokenTypes.WRITE, 0x51bfdc + (8 * i) + 0x07, bytes([world.options.ability_ap.value]))
        last_index += 1

    for i in range(0, len(nu_mou_abilities)):
        patch.write_token(APTokenTypes.WRITE, 0x51c244 + (8 * i), bytes(world.all_abilities[last_index]))

        if world.options.ability_ap.value != 65:
            # Set AP
            patch.write_token(APTokenTypes.WRITE, 0x51c244 + (8 * i) + 0x07, bytes([world.options.ability_ap.value]))
        last_index += 1

    for i in range(0, len(viera_abilities)):
        patch.write_token(APTokenTypes.WRITE, 0x51c53c + (8 * i), bytes(world.all_abilities[last_index]))

        if world.options.ability_ap.value != 65:
            # Set AP
            patch.write_token(APTokenTypes.WRITE, 0x51c53c + (8 * i) + 0x07, bytes([world.options.ability_ap.value]))
        last_index += 1

    for i in range(0, len(moogle_abilities)):
        patch.write_token(APTokenTypes.WRITE, 0x51c7e4 + (8 * i), bytes(world.all_abilities[last_index]))

        if world.options.ability_ap.value != 65:
            # Set AP
            patch.write_token(APTokenTypes.WRITE, 0x51c7e4 + (8 * i) + 0x07, bytes([world.options.ability_ap.value]))
        last_index += 1

    """
    # Randomize jobs
    race_jobs = []
    for i in range(0, 42):
        race_jobs.append(0x521a80 + (0x34 * i))

    world.random.shuffle(race_jobs)

    last_index = 0
    for i in range(11):
        patch.write_token(APTokenTypes.WRITE, race_jobs[last_index], bytes([0x01]))
        last_index += 1

    for i in range(7):
        patch.write_token(APTokenTypes.WRITE, race_jobs[last_index], bytes([0x02]))
        last_index += 1

    for i in range(8):
        patch.write_token(APTokenTypes.WRITE, race_jobs[last_index], bytes([0x03]))
        last_index += 1

    for i in range(8):
        patch.write_token(APTokenTypes.WRITE, race_jobs[last_index], bytes([0x04]))
        last_index += 1

    for i in range(8):
        patch.write_token(APTokenTypes.WRITE, race_jobs[last_index], bytes([0x05]))
        last_index += 1

    """
    # Average stat growth
    job_memory = 0x521a7c

    if world.options.stat_growth == StatGrowth.option_average:
        for i in range(0x2B):
            patch.write_token(APTokenTypes.WRITE, job_memory + 0x20, bytes([0x3C]))
            patch.write_token(APTokenTypes.WRITE, job_memory + 0x21, bytes([0x3C]))
            patch.write_token(APTokenTypes.WRITE, job_memory + 0x22, bytes([0x0B]))
            patch.write_token(APTokenTypes.WRITE, job_memory + 0x23, bytes([0x3C]))
            patch.write_token(APTokenTypes.WRITE, job_memory + 0x24, bytes([0x3C]))
            patch.write_token(APTokenTypes.WRITE, job_memory + 0x25, bytes([0x3C]))
            patch.write_token(APTokenTypes.WRITE, job_memory + 0x26, bytes([0x3C]))

            job_memory += 0x34

    # Add monsters to recruitment pool if option is selected
    if world.options.force_recruitment == 3:
        recruitment_memory = 0x529788
        for i in range(0, 47):
            # Class in recruitment list
            job = get_random_job(world.random, 7)
            patch.write_token(APTokenTypes.WRITE, recruitment_memory + 3 + (i * 12), bytes([job]))

    # Randomize music
    # for address in music_addresses:
    #    patch.write_token(APTokenTypes.WRITE, address, bytes([world.random.choice(music_id)]))

    patch.write_file("token_data.bin", patch.get_token_binary())

    # Write Output
    out_file_name = world.multiworld.get_out_file_name_base(world.player)

    patch.write(
        os.path.join(output_directory,
                     f"{out_file_name}{patch.patch_file_ending}"))


def set_up_gates(ffta_data: FFTAData, num_gates: int, req_items, final_unlock: int, final_mission: int, dispatch: int,
                 world, patch: FFTAProcedurePatch) -> None:
    unlock_mission(ffta_data, world.MissionGroups[0][0][0].mission_id, patch)
    unlock_mission(ffta_data, world.MissionGroups[1][0][0].mission_id, patch)
    unlock_mission(ffta_data, world.MissionGroups[2][0][0].mission_id, patch)

    for i in range(0, dispatch):
        unlock_mission(ffta_data, world.DispatchMissionGroups[i][0][0].mission_id, patch)

    req_item2 = 0

    for path in range(0, world.options.gate_paths.value):
        unlock_mission(ffta_data, world.MissionGroups[3 + path * 4][0][0].mission_id, patch)

        # Add second required mission item if options are selected
        if req_items == 1 or req_items == 2:
            req_item2 = MissionUnlockItems[1 + path * 2].itemID

        if world.options.gate_items.value == 2:
            set_required_items(ffta_data,
                               world.MissionGroups[3 + path * 4][0][0].mission_id, MissionUnlockItems[path * 2].itemID,
                               0, patch)
            if path == 0:
                set_required_items(ffta_data,
                                   world.DispatchMissionGroups[dispatch - 1][0][0].mission_id, req_item2,
                                   0, patch)

        else:
            set_required_items(ffta_data,
                               world.MissionGroups[3 + path * 4][0][0].mission_id, MissionUnlockItems[path * 2].itemID,
                               req_item2, patch)

    mission_index = 4
    mission_unlock = 3
    dispatch_index = dispatch
    dispatch_unlock = dispatch - 1
    item_index = 2

    if num_gates == 1 and final_unlock == 0:

        # Unlock Royal Valley for one gate setting
        if final_mission == 0:
            set_mission_requirement(ffta_data, 23, world.MissionGroups[3][0][0].mission_id, patch)

        # Unlock Decision Time for one gate setting
        elif final_mission == 1:
            set_mission_requirement(ffta_data, 393, world.MissionGroups[3][0][0].mission_id, patch)

        return

    if world.options.gate_paths.value == 1:
        for i in range(2, num_gates + 1):

            for j in range(4):
                set_mission_requirement(ffta_data, world.MissionGroups[mission_index][0][0].mission_id,
                                        world.MissionGroups[mission_unlock][0][0].mission_id, patch)
                mission_index += 1

            # Add dispatch missions based on settings
            for k in range(0, dispatch):

                if world.options.gate_items.value == 2:
                    set_mission_requirement(ffta_data, world.DispatchMissionGroups[dispatch_index][0][0].mission_id,
                                            world.DispatchMissionGroups[dispatch_unlock][0][0].mission_id, patch)

                else:
                    set_mission_requirement(ffta_data, world.DispatchMissionGroups[dispatch_index][0][0].mission_id,
                                            world.MissionGroups[mission_unlock][0][0].mission_id, patch)

                dispatch_index += 1

            mission_unlock += 4
            dispatch_unlock += dispatch

            if req_items == 1 or req_items == 2:
                req_item2 = MissionUnlockItems[item_index + 1].itemID

            # Add required item to dispatch mission gates if option is selected
            if world.options.gate_items.value == 2:
                set_required_items(ffta_data, world.DispatchMissionGroups[dispatch_unlock][0][0].mission_id,
                                   req_item2,
                                   0, patch)
                set_required_items(ffta_data, world.MissionGroups[mission_unlock][0][0].mission_id,
                                   MissionUnlockItems[item_index].itemID,
                                   0, patch)

            else:
                set_required_items(ffta_data, world.MissionGroups[mission_unlock][0][0].mission_id,
                                   MissionUnlockItems[item_index].itemID,
                                   req_item2, patch)

            item_index += 2
    elif world.options.gate_paths.value > 1:
        path_lengths = [
            world.path1_length,
            world.path2_length,
            world.path3_length,
        ]
        req_item2 = 0
        final_path_unlocks = []
        for path in range(0, world.options.gate_paths.value):
            path_index = mission_index + path * 4
            path_unlock = mission_unlock + path * 4
            path_item = item_index + (world.options.gate_paths.value - 1) * 2 + path * 2
            path_dispatch = dispatch_index + path * dispatch

            for i in range(1, path_lengths[path]):

                for j in range(3):
                    set_mission_requirement(ffta_data, world.MissionGroups[path_index][0][0].mission_id,
                                            world.MissionGroups[path_unlock][0][0].mission_id, patch)
                    path_index += 1

                next_gate = path_index + 4 * (world.options.gate_paths.value - 1)
                set_mission_requirement(ffta_data,
                                        world.MissionGroups[next_gate][0][0].mission_id,
                                        world.MissionGroups[path_unlock][0][0].mission_id, patch)

                # Only if Dispatch Gates are not enabled
                if world.options.gate_items.value != 2:
                    for k in range(0, dispatch):
                        set_mission_requirement(ffta_data, world.DispatchMissionGroups[path_dispatch][0][0].mission_id,
                                                world.MissionGroups[path_unlock][0][0].mission_id, patch)
                        path_dispatch += 1
                    path_dispatch += (world.options.gate_paths.value - 1) * dispatch

                path_index += (world.options.gate_paths.value - 1) * 4 + 1
                path_unlock += (world.options.gate_paths.value * 4)

                # Set second required item if option is selected and Dispatch Gates are not enabled
                if world.options.gate_items.value == 1:
                    req_item2 = MissionUnlockItems[path_item + 1].itemID

                # Set required items
                set_required_items(ffta_data, world.MissionGroups[path_unlock][0][0].mission_id,
                                   MissionUnlockItems[path_item].itemID,
                                   req_item2, patch)

                path_item += world.options.gate_paths.value * 2

            final_path_unlocks.append(path_unlock)

        # Set dispatch gates if enabled
        if world.options.gate_items.value == 2:
            for i in range(1, sum(path_lengths) + 1):
                for k in range(0, dispatch):
                    set_mission_requirement(ffta_data, world.DispatchMissionGroups[dispatch_index][0][0].mission_id,
                                            world.DispatchMissionGroups[dispatch_unlock][0][0].mission_id, patch)
                    dispatch_index += 1
                dispatch_unlock += dispatch
                req_item2 = MissionUnlockItems[item_index + 1].itemID
                set_required_items(ffta_data, world.DispatchMissionGroups[dispatch_unlock][0][0].mission_id,
                                   req_item2,
                                   0, patch)
                item_index += 2

    # Set final mission to unlock after all the gates if all mission gates option is selected
    if final_unlock == 0:
        # 0 = Royal Valley, 1 = Decision Time
        final_mission_list = [23, 393]
        final_mission_id = final_mission_list[final_mission]

        if world.options.gate_paths.value == 1:

            set_mission_requirement(ffta_data, final_mission_id,
                                    world.MissionGroups[mission_unlock][0][0].mission_id, patch)

        # Set all final missions in paths to unlock the final mission
        elif world.options.gate_paths.value > 1:
            unlockFlags = [
                MissionOffsets.unlockflag1,
                MissionOffsets.unlockflag2,
                MissionOffsets.unlockflag3,
            ]

            for path in range(0, 3):
                if path < world.options.gate_paths.value:
                    patch.write_token(APTokenTypes.WRITE,
                                      ffta_data.missions[final_mission_id].memory + unlockFlags[path],
                                      struct.pack("<H",
                                                  world.MissionGroups[final_path_unlocks[path]][0][0].mission_id + 2))

                    if world.MissionGroups[final_path_unlocks[path]][0][0].mission_id > 253:
                        patch.write_token(APTokenTypes.WRITE,
                                          ffta_data.missions[final_mission_id].memory + unlockFlags[path] + 0x01,
                                          bytes([0x04]))
                    else:
                        patch.write_token(APTokenTypes.WRITE,
                                          ffta_data.missions[final_mission_id].memory + unlockFlags[path] + 0x01,
                                          bytes([0x03]))

                    patch.write_token(APTokenTypes.WRITE,
                                      ffta_data.missions[final_mission_id].memory + unlockFlags[path] + 0x02,
                                      bytes([0x01]))
                else:
                    patch.write_token(APTokenTypes.WRITE,
                                      ffta_data.missions[final_mission_id].memory + unlockFlags[path],
                                      bytes([0x00]))
                    patch.write_token(APTokenTypes.WRITE,
                                      ffta_data.missions[final_mission_id].memory + unlockFlags[path] + 0x01,
                                      bytes([0x00]))
                    patch.write_token(APTokenTypes.WRITE,
                                      ffta_data.missions[final_mission_id].memory + unlockFlags[path] + 0x02,
                                      bytes([0x00]))


def set_mission_requirement(ffta_data: FFTAData, current_mission_ID: int, previous_mission_ID: int,
                            patch: FFTAProcedurePatch) -> None:

    # Set the mission requirements to the specified mission ID
    patch.write_token(APTokenTypes.WRITE, ffta_data.missions[current_mission_ID].memory + MissionOffsets.unlockflag1,
                      struct.pack("<H", previous_mission_ID + 2))

    # Hacky way to account for missions that are two bytes. Try and use bitwise operations to consolidate
    if previous_mission_ID > 253:
        patch.write_token(APTokenTypes.WRITE,
                          ffta_data.missions[current_mission_ID].memory + MissionOffsets.unlockflag1 + 0x01,
                          bytes([0x04]))

    else:
        patch.write_token(APTokenTypes.WRITE,
                          ffta_data.missions[current_mission_ID].memory + MissionOffsets.unlockflag1 + 0x01,
                          bytes([0x03]))

    patch.write_token(APTokenTypes.WRITE,
                      ffta_data.missions[current_mission_ID].memory + MissionOffsets.unlockflag1 + 0x02, bytes([0x01]))
    patch.write_token(APTokenTypes.WRITE, ffta_data.missions[current_mission_ID].memory + MissionOffsets.unlockflag2,
                      bytes([0x00]))
    patch.write_token(APTokenTypes.WRITE,
                      ffta_data.missions[current_mission_ID].memory + MissionOffsets.unlockflag2 + 1, bytes([0x00]))
    patch.write_token(APTokenTypes.WRITE,
                      ffta_data.missions[current_mission_ID].memory + MissionOffsets.unlockflag2 + 2, bytes([0x00]))
    patch.write_token(APTokenTypes.WRITE, ffta_data.missions[current_mission_ID].memory + MissionOffsets.unlockflag3,
                      bytes([0x00]))
    patch.write_token(APTokenTypes.WRITE,
                      ffta_data.missions[current_mission_ID].memory + MissionOffsets.unlockflag3 + 1, bytes([0x00]))
    patch.write_token(APTokenTypes.WRITE,
                      ffta_data.missions[current_mission_ID].memory + MissionOffsets.unlockflag3 + 2, bytes([0x00]))


def set_items(multiworld, player, patch: FFTAProcedurePatch) -> None:
    offset = 41234532

    for location in multiworld.get_filled_locations(player):

        if location.item.code is not None:
            if location.item.player != player:
                item_id = 0x185
            else:
                item_id = location.item.code - offset

            item_id = item_id << location.offset
            byte1 = item_id & 0x00ff
            byte2 = ((item_id & 0xff00) >> 8)
            patch.write_token(APTokenTypes.OR_8, location.address, byte1)
            patch.write_token(APTokenTypes.OR_8, location.address + 1, byte2)


def write_progressive_shop(ffta_data: FFTAData, world, patch: FFTAProcedurePatch):
    if world.options.progressive_shop.value == 0:
        patch.write_token(APTokenTypes.WRITE, 0x00b30950, struct.pack("<B", 0))
        patch.write_token(APTokenTypes.WRITE, 0x00b30951, struct.pack("<B", 1))
        return
    shop_tier_num = len(world.shop_tiers) - 1
    patch.write_token(APTokenTypes.WRITE, 0x00b30950, struct.pack("<B", shop_tier_num))
    patch.write_token(APTokenTypes.WRITE, 0x00b30951,
                      struct.pack("<B", world.options.progressive_shop_battle_unlock.value))

    item_tiers = [0] * len(ffta_data.items)
    for tier, tier_data in enumerate(world.shop_tiers):
        for item, price in tier_data:
            if price >= 0:
                sell_price = max(1, price // 2)  # Might not be necessary. 0 seems to be 1 anyway
                patch.write_token(APTokenTypes.WRITE, ffta_data.items[item.itemID - 1].memory + ItemOffsets.buy_price,
                                  struct.pack("<H", price))
                patch.write_token(APTokenTypes.WRITE, ffta_data.items[item.itemID - 1].memory + ItemOffsets.sell_price,
                                  struct.pack("<H", sell_price))
            item_tiers[item.itemID-1] = tier+1

    tier_list_address = 0x00b30954
    patch.write_token(APTokenTypes.WRITE, tier_list_address, struct.pack(f"<{len(item_tiers)}B", *item_tiers))


def write_progressive_lists(world, patch: FFTAProcedurePatch):
    # Making sure unused paths still exist, so if an unused path item is received it won't break anything.

    excess_item_id = world.options.progressive_excess.value
    path_pointers = []
    path_lengths = []
    current_address = 0x00b30630
    for path in range(0, len(world.path_items)):
        path_pointers.append(current_address + 0x08000000)
        path_lengths.append(0)
        for item in world.path_items[path]:
            patch.write_token(APTokenTypes.WRITE, current_address, struct.pack("<H", item.itemID))
            current_address += 2
            path_lengths[path] += 1
        # Add a last item. This item is received each time an excess path item is received.
        patch.write_token(APTokenTypes.WRITE, current_address, struct.pack("<H", excess_item_id))
        current_address += 8

    pointerLocation = 0x00b30608
    for path in path_pointers:
        patch.write_token(APTokenTypes.WRITE, pointerLocation, struct.pack("<L", path))
        pointerLocation += 4

    for path in path_lengths:
        patch.write_token(APTokenTypes.WRITE, pointerLocation, struct.pack("<B", path))
        pointerLocation += 1

    # Initial state must be non-zero, unlikely to be generated but possible
    initial_state = 0
    while (initial_state == 0):
        initial_state = world.random.getrandbits(32)
    patch.write_token(APTokenTypes.WRITE, 0x00b30604, struct.pack("<L", initial_state))


def set_required_items(ffta_data: FFTAData, index: int, itemid1, itemid2, patch: FFTAProcedurePatch):
    patch.write_token(APTokenTypes.WRITE, ffta_data.missions[index].memory + MissionOffsets.required_item1,
                      bytes([itemid1 - 0x177]))

    if itemid2 != 0:
        patch.write_token(APTokenTypes.WRITE, ffta_data.missions[index].memory + MissionOffsets.required_item2,
                          bytes([itemid2 - 0x177]))

    else:
        patch.write_token(APTokenTypes.WRITE, ffta_data.missions[index].memory + MissionOffsets.required_item2,
                          bytes([itemid2]))


def write_display_only_items(patch: FFTAProcedurePatch):
    # Items that should be displayed when found, but not put into inventory
    display_items = [0x185, 0x1BD]
    # End list with 0
    display_items += [0x00]

    address = 0x00b31100
    patch.write_token(APTokenTypes.WRITE, address, struct.pack(f"<{len(display_items)}H", *display_items))
