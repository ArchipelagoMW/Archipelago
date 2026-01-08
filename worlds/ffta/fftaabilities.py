from .data import UnitOffsets, JobID, human_abilities, bangaa_abilities, nu_mou_abilities, viera_abilities, \
    moogle_abilities
from typing import List, Tuple
from itertools import chain
from worlds.Files import APTokenTypes


def set_mastered_ability(address, index, patch) -> None:

    patch.write_token(APTokenTypes.OR_8, address, (1 << index))


class JobAbilities:
    # First number is the address index, second is the bit index

    # Job ability memory locations
    soldier = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (1, 1), (1, 2)]
    paladin = [(1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5)]
    fighter = [(2, 6), (2, 7), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 0), (4, 1)]
    thiefhum = [(4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)]
    ninja = [(5, 6), (5, 7), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (7, 0)]
    whitemagehum = [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (8, 0), (8, 1), (8, 2), (8, 3)]
    blackmagehum = [(8, 4), (8, 5), (8, 6), (8, 7), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7)]
    illusionisthum = [(10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (11, 0), (11, 1), (11, 2)]
    bluemage = [(11, 3), (11, 4), (11, 5), (11, 6), (11, 7), (12, 0), (12, 1), (12, 2), (12, 3), (12, 4), (12, 5),
                (12, 6), (12, 7), (13, 0), (13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (14, 0),
                (14, 1), (14, 2), (14, 3), (14, 4)]
    archerhum = [(14, 5), (14, 6), (14, 7), (15, 0), (15, 1), (15, 2), (15, 3), (15, 4), (15, 5), (15, 6), (15, 7)]
    hunter = [(16, 0), (16, 1), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6), (16, 7), (17, 0), (17, 1), (17, 2),
              (17, 3)]

    # Bangaa jobs
    warrior = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (1, 1), (1, 2)]
    dragoon = [(1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]
    defender = [(2, 5), (2, 6), (2, 7), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7)]
    gladiator = [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (5, 0), (5, 1), (5, 2)]
    white_monk = [(5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5)]
    bishop = [(6, 6), (6, 7), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (8, 0)]
    templar = [(8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (9, 0), (9, 1), (9, 2), (9, 3)]

    # Nu Mou jobs
    whitemagemou = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (1, 1), (1, 2)]
    blackmagemou = [(1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)]
    timemagemou = [(2, 7), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 0)]
    illusionistmou = [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (5, 0), (5, 1), (5, 2), (5, 3)]
    alchemist = [(5, 4), (5, 5), (5, 6), (5, 7), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]
    beastmaster = [(6, 7), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (8, 0), (8, 1), (8, 2),
                   (8, 3), (8, 4), (8, 5), (8, 6)]
    morpher = [(8, 7), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (10, 0), (10, 1)]
    sage = [(10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (11, 0), (11, 1), (11, 2), (11, 3), (11, 4), (11, 5)]

    # Viera jobs
    fencer = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (1, 1), (1, 2)]
    elementalist = [(1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]
    redmage = [(2, 5), (2, 6), (2, 7), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7)]
    whitemageviera = [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (5, 0), (5, 1), (5, 2)]
    summoner = [(5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4)]
    archerviera = [(6, 5), (6, 6), (6, 7), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
    assassin = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (9, 0), (9, 1)]
    sniper = [(9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (10, 0), (10, 1), (10, 2), (10, 3)]

    # Moogle jobs
    animist = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (1, 1)]
    mogknight = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]
    gunner = [(2, 5), (2, 6), (2, 7), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)]
    thiefmog = [(3, 7), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (5, 0), (5, 1), (5, 2)]
    juggler = [(5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5)]
    gadgeteer = [(6, 6), (6, 7), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (8, 0)]
    blackmagemog = [(8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4)]
    timemagemog = [(9, 5), (9, 6), (9, 7), (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6)]

    # Monsters
    goblin = [(0, 0), (0, 1), (0, 2)]
    red_cap = [(0, 3), (0, 4), (0, 5), (0, 6)]
    jelly = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]
    ice_flan = [(0, 7), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
    cream = [(1, 6), (1, 7), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]
    bomb = [(0, 0), (0, 1), (0, 2), (0, 3)]
    grenade = [(0, 4), (0, 5), (0, 6), (0, 7)]
    icedrake = [(0, 0), (0, 1), (0, 2), (0, 3)]
    firewyrm = [(0, 4), (0, 5), (0, 6), (0, 7)]
    thundrake = [(1, 0), (1, 1), (1, 2), (1, 3)]
    lamia = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    lilith = [(0, 5), (0, 6), (0, 7), (1, 0), (1, 1)]
    antlion = [(0, 0), (0, 1), (0, 2), (0, 3)]
    jawbreaker = [(0, 4), (0, 5), (0, 6), (0, 7), (1, 0)]
    toughskin = [(0, 0), (0, 1), (0, 2), (0, 3)]
    blade_biter = [(0, 4), (0, 5), (0, 6), (0, 7), (1, 0)]
    tonberry = [(0, 0), (0, 1), (0, 2), (0, 3)]
    masterberry = [(0, 4), (0, 5), (0, 6), (0, 7)]
    red_panther = [(0, 0), (0, 1), (0, 2), (0, 3)]
    coeurl = [(0, 4), (0, 5), (0, 6), (0, 7)]
    malboro = [(0, 0), (0, 1), (0, 2), (0, 3)]
    big_malboro = [(0, 4), (0, 5), (0, 6), (0, 7)]
    floateye = [(0, 0), (0, 1), (0, 2), (0, 3)]
    ahriman = [(0, 4), (0, 5), (0, 6), (0, 7)]
    zombie = [(0, 0), (0, 1), (0, 2), (0, 3)]
    vampire = [(0, 4), (0, 5), (0, 6), (0, 7), (1, 0)]
    sprite = [(0, 0), (0, 1), (0, 2), (0, 3)]
    titania = [(0, 4), (0, 5), (0, 6), (0, 7)]


def master_abilities(data, index: int, ability_list: List[Tuple], percent: float, patch, world):
    ability_set: int
    ability: int
    master_amount: int

    if ability_list == 0:
        return

    # Always master learn for blue mage if vanilla abilities are on
    elif ability_list == JobAbilities.bluemage and world.options.randomize_abilities == 0:
        set_mastered_ability(data.formations[index].memory + UnitOffsets.abilities + 14,
                             3, patch)

    # Shuffle the abilities
    world.random.shuffle(ability_list)

    reaction_abilities = []
    support_abilities = []
    ability_dict = {}
    abilities = []

    if 0x02 <= world.randomized_jobs[index] <= 0x0C:
        ability_dict = world.human_ability_dict
        abilities = world.new_human_abilities

    elif 0x0D <= world.randomized_jobs[index] <= 0x13:
        ability_dict = world.bangaa_ability_dict
        abilities = world.new_bangaa_abilities

    elif 0x14 <= world.randomized_jobs[index] <= 0x1B:
        ability_dict = world.nu_mou_ability_dict
        abilities = world.new_nu_mou_abilities

    elif 0x1C <= world.randomized_jobs[index] <= 0x23:
        ability_dict = world.viera_ability_dict
        abilities = world.new_viera_abilities

    elif 0x24 <= world.randomized_jobs[index] <= 0x2B:
        ability_dict = world.moogle_ability_dict
        abilities = world.new_moogle_abilities

    master_amount = int((percent / 10) * len(ability_list))
    for x in range(master_amount):
        ability_set = ability_list[x][0]
        ability = ability_list[x][1]

        # Check if ability dictionary is not empty
        if ability_dict:

            ability_data = ability_dict[ability_list[x]]

            if ability_data[6] == 0x03:
                support_abilities.append(abilities.index(ability_data) + 1)

            elif ability_data[6] == 0x02:
                reaction_abilities.append(abilities.index(ability_data) + 1)

        set_mastered_ability(data.formations[index].memory + UnitOffsets.abilities + ability_set, ability, patch)

    # Add random support and reaction abilities to unit if they have learned the ability
    if len(support_abilities) > 0:
        patch.write_token(APTokenTypes.WRITE, data.formations[index].memory + UnitOffsets.ability_support,
                          bytes([world.random.choice(support_abilities)]))

    else:
        patch.write_token(APTokenTypes.WRITE, data.formations[index].memory + UnitOffsets.ability_support,
                          bytes([0x00]))

    if len(reaction_abilities) > 0:
        patch.write_token(APTokenTypes.WRITE, data.formations[index].memory + UnitOffsets.ability_reaction,
                          bytes([world.random.choice(reaction_abilities)]))

    else:
        patch.write_token(APTokenTypes.WRITE, data.formations[index].memory + UnitOffsets.ability_reaction,
                          bytes([0x00]))


def get_job_abilities(job: int):

    if job == JobID.soldier:
        return JobAbilities.soldier

    elif job == JobID.paladin:
        return JobAbilities.paladin

    elif job == JobID.fighter:
        return JobAbilities.fighter

    elif job == JobID.thiefhum:
        return JobAbilities.thiefhum

    elif job == JobID.ninja:
        return JobAbilities.ninja

    elif job == JobID.whitemagehum:
        return JobAbilities.whitemagehum

    elif job == JobID.blackmagehum:
        return JobAbilities.blackmagehum

    elif job == JobID.illusionisthum:
        return JobAbilities.illusionisthum

    elif job == JobID.bluemage:
        return JobAbilities.bluemage

    elif job == JobID.archerhum:
        return JobAbilities.archerhum

    elif job == JobID.hunter:
        return JobAbilities.hunter

    elif job == JobID.warrior:
        return JobAbilities.warrior

    elif job == JobID.dragoon:
        return JobAbilities.dragoon

    elif job == JobID.defender:
        return JobAbilities.defender

    elif job == JobID.gladiator:
        return JobAbilities.gladiator

    elif job == JobID.whitemonk:
        return JobAbilities.white_monk

    elif job == JobID.bishop:
        return JobAbilities.bishop

    elif job == JobID.templar:
        return JobAbilities.templar

    elif job == JobID.whitemagemou:
        return JobAbilities.whitemagemou

    elif job == JobID.blackmagemou:
        return JobAbilities.blackmagemou

    elif job == JobID.timemagemou:
        return JobAbilities.timemagemou

    elif job == JobID.illusionistmou:
        return JobAbilities.illusionistmou

    elif job == JobID.alchemist:
        return JobAbilities.alchemist

    elif job == JobID.beastmaster:
        return JobAbilities.beastmaster

    elif job == JobID.morpher:
        return JobAbilities.morpher

    elif job == JobID.sage:
        return JobAbilities.sage

    elif job == JobID.fencer:
        return JobAbilities.fencer

    elif job == JobID.elementalist:
        return JobAbilities.elementalist

    elif job == JobID.redmage:
        return JobAbilities.redmage

    elif job == JobID.whitemagevra:
        return JobAbilities.whitemageviera

    elif job == JobID.summoner:
        return JobAbilities.summoner

    elif job == JobID.archervra:
        return JobAbilities.archerviera

    elif job == JobID.assassin:
        return JobAbilities.assassin

    elif job == JobID.sniper:
        return JobAbilities.sniper

    elif job == JobID.animist:
        return JobAbilities.animist

    elif job == JobID.mogknight:
        return JobAbilities.mogknight

    elif job == JobID.gunner:
        return JobAbilities.gunner

    elif job == JobID.thiefmog:
        return JobAbilities.thiefmog

    elif job == JobID.juggler:
        return JobAbilities.juggler

    elif job == JobID.gadgeteer:
        return JobAbilities.gadgeteer

    elif job == JobID.blackmagemog:
        return JobAbilities.blackmagemog

    elif job == JobID.timemagemog:
        return JobAbilities.timemagemog

    elif job == JobID.goblin:
        return JobAbilities.goblin

    elif job == JobID.red_cap:
        return JobAbilities.red_cap

    elif job == JobID.jelly:
        return JobAbilities.jelly

    elif job == JobID.ice_flan:
        return JobAbilities.ice_flan

    elif job == JobID.cream:
        return JobAbilities.cream

    elif job == JobID.bomb:
        return JobAbilities.bomb

    elif job == JobID.grenade:
        return JobAbilities.grenade

    elif job == JobID.icedrake:
        return JobAbilities.icedrake

    elif job == JobID.firewyrm:
        return JobAbilities.firewyrm

    elif job == JobID.thundrake:
        return JobAbilities.thundrake

    elif job == JobID.lamia:
        return JobAbilities.lamia

    elif job == JobID.lilith:
        return JobAbilities.lilith

    elif job == JobID.antlion:
        return JobAbilities.antlion

    elif job == JobID.jawbreaker:
        return JobAbilities.jawbreaker

    elif job == JobID.toughskin:
        return JobAbilities.toughskin

    elif job == JobID.blade_biter:
        return JobAbilities.blade_biter

    elif job == JobID.tonberry:
        return JobAbilities.tonberry

    elif job == JobID.masterberry:
        return JobAbilities.masterberry

    elif job == JobID.red_panther:
        return JobAbilities.red_panther

    elif job == JobID.coeurl:
        return JobAbilities.coeurl

    elif job == JobID.malboro:
        return JobAbilities.malboro

    elif job == JobID.big_malboro:
        return JobAbilities.big_malboro

    elif job == JobID.floateye:
        return JobAbilities.floateye

    elif job == JobID.ahriman:
        return JobAbilities.ahriman

    elif job == JobID.zombie:
        return JobAbilities.zombie

    elif job == JobID.vampire:
        return JobAbilities.vampire

    elif job == JobID.sprite:
        return JobAbilities.sprite

    elif job == JobID.titania:
        return JobAbilities.titania

    else:
        return 0


human_abilities_bitflags = list(chain(JobAbilities.soldier, JobAbilities.paladin, JobAbilities.fighter,
                                      JobAbilities.thiefhum, JobAbilities.ninja, JobAbilities.whitemagehum,
                                      JobAbilities.blackmagehum, JobAbilities.illusionisthum, JobAbilities.bluemage,
                                      JobAbilities.archerhum, JobAbilities.hunter))


bangaa_abilities_bitflags = list(chain(JobAbilities.warrior, JobAbilities.dragoon, JobAbilities.defender,
                                       JobAbilities.gladiator, JobAbilities.white_monk, JobAbilities.bishop,
                                       JobAbilities.templar))

nu_mou_abilities_bitflags = list(chain(JobAbilities.whitemagemou, JobAbilities.blackmagemou, JobAbilities.timemagemou,
                                       JobAbilities.illusionistmou, JobAbilities.alchemist, JobAbilities.beastmaster,
                                       JobAbilities.morpher, JobAbilities.sage))

viera_abilities_bitflags = list(chain(JobAbilities.fencer, JobAbilities.elementalist, JobAbilities.redmage,
                                      JobAbilities.whitemageviera, JobAbilities.summoner, JobAbilities.archerviera,
                                      JobAbilities.assassin, JobAbilities.sniper))

moogle_abilities_bitflags = list(chain(JobAbilities.animist, JobAbilities.mogknight, JobAbilities.gunner,
                                       JobAbilities.thiefmog, JobAbilities.juggler, JobAbilities.gadgeteer,
                                       JobAbilities.blackmagemog, JobAbilities.timemagemog))
