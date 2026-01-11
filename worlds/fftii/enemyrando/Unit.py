from copy import copy
from enum import Enum

from worlds.fftii.enemyrando.Job import all_jobs, UnlockedJob
from worlds.fftii.enemyrando.SpriteSet import sprite_sets


class UnitGender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    MONSTER = "Monster"
    NONE = "None"

class UnitTeam(Enum):
    BLUE = 0x40
    RED = 1

class Unit:
    unit_data: bytearray

    job_offset = 0x0A
    job: int
    job_name: str

    sprite_set_offset = 0x00
    sprite_set: int
    sprite_set_name: str

    flags_offset = 0x01
    flags: int
    gender: UnitGender

    flags2_offset = 0x18
    flags2: int
    team: UnitTeam

    birthday_month_offset = 0x04
    birthday_month: int

    birthday_day_offset = 0x05
    birthday_day: int

    brave_offset = 0x06
    brave: int

    faith_offset = 0x07
    faith: int

    unlocked_job_offset = 0x08
    unlocked_job: int
    unlocked_job_level_offset = 0x09
    unlocked_job_level: int

    primary_offset = 0x1D
    primary: int

    secondary_offset = 0x0B
    secondary: int

    reaction_offset = 0x0C
    reaction: int

    support_offset = 0x0E
    support: int

    movement_offset = 0x10
    movement: int

    head_offset = 0x12
    head: int

    body_offset = 0x13
    body: int

    accessory_offset = 0x14
    accessory: int

    right_hand_offset = 0x15
    right_hand: int

    left_hand_offset = 0x16
    left_hand: int

    def __init__(self, unit_data):
        self.unit_data = copy(unit_data)
        self.job = unit_data[self.job_offset]
        self.sprite_set = unit_data[self.sprite_set_offset]
        self.flags = unit_data[self.flags_offset]
        self.flags2 = unit_data[self.flags2_offset]
        self.birthday_month = unit_data[self.birthday_month_offset]
        self.birthday_day = unit_data[self.birthday_day_offset]
        self.brave = unit_data[self.brave_offset]
        self.faith = unit_data[self.faith_offset]
        self.unlocked_job = unit_data[self.unlocked_job_offset]
        self.unlocked_job_level = unit_data[self.unlocked_job_level_offset]
        self.primary = unit_data[self.primary_offset]
        self.secondary = unit_data[self.secondary_offset]
        self.reaction = int.from_bytes(unit_data[self.reaction_offset:self.reaction_offset + 2])
        self.support = int.from_bytes(unit_data[self.support_offset:self.support_offset + 2])
        self.movement = int.from_bytes(unit_data[self.movement_offset:self.movement_offset + 2])
        self.head = unit_data[self.head_offset]
        self.body = unit_data[self.body_offset]
        self.accessory = unit_data[self.accessory_offset]
        self.right_hand = unit_data[self.right_hand_offset]
        self.left_hand = unit_data[self.left_hand_offset]
        if self.job in all_jobs.keys():
            self.job_name = all_jobs[self.job]
        else:
            if self.job == 0:
                self.job_name = "None"
            else:
                self.job_name = f"Unknown Job {str(hex(self.job))}"
        if self.sprite_set in sprite_sets.keys():
            self.sprite_set_name = sprite_sets[self.sprite_set]
        else:
            if self.job == 0:
                self.sprite_set_name = "None"
            else:
                self.sprite_set_name = "Unknown sprite set"
        self.gender = self.get_gender()
        self.team = self.get_team()
        self.apply_unit_data()
        for i in range(len(self.unit_data)):
            assert self.unit_data[i] == unit_data[i], (hex(i), self.unit_data[i], unit_data[i])
        assert self.unit_data == unit_data

    def get_gender(self):
        male = self.flags & 0x80
        female = self.flags & 0x40
        monster = self.flags & 0x20
        if male > 0:
            assert female == 0
            assert monster == 0
            return UnitGender.MALE
        if female > 0:
            assert male == 0
            assert monster == 0
            return UnitGender.FEMALE
        if monster > 0:
            assert male == 0
            assert female == 0
            return UnitGender.MONSTER
        return UnitGender.NONE

    def get_team(self):
        team_bits = (self.flags2 & 0x30) >> 4
        if team_bits == 0:
            return UnitTeam.BLUE
        if team_bits == 1:
            return UnitTeam.RED
        raise ValueError(str(bin(self.flags2)))

    def apply_unit_data(self):
        self.unit_data[self.job_offset] = self.job
        self.unit_data[self.sprite_set_offset] = self.sprite_set
        self.unit_data[self.flags_offset] = self.flags
        self.unit_data[self.flags2_offset] = self.flags2
        self.unit_data[self.unlocked_job_offset] = self.unlocked_job
        self.unit_data[self.unlocked_job_level_offset] = self.unlocked_job_level
        self.unit_data[self.birthday_month_offset] = self.birthday_month
        self.unit_data[self.birthday_day_offset] = self.birthday_day
        self.unit_data[self.brave_offset] = self.brave
        self.unit_data[self.faith_offset] = self.faith
        self.unit_data[self.primary_offset] = self.primary
        self.unit_data[self.secondary_offset] = self.secondary
        self.unit_data[self.reaction_offset] = self.reaction // 256
        self.unit_data[self.reaction_offset + 1] = self.reaction % 256
        self.unit_data[self.support_offset] = self.support // 256
        self.unit_data[self.support_offset + 1] = self.support % 256
        self.unit_data[self.movement_offset] = self.movement // 256
        self.unit_data[self.movement_offset + 1] = self.movement % 256
        self.unit_data[self.head_offset] = self.head
        self.unit_data[self.body_offset] = self.body
        self.unit_data[self.accessory_offset] = self.accessory
        self.unit_data[self.right_hand_offset] = self.right_hand
        self.unit_data[self.left_hand_offset] = self.left_hand


    def __repr__(self):
        try:
            return_string = f"{self.job_name} ({UnlockedJob(self.unlocked_job).name} {self.unlocked_job_level})"
        except:
            return_string = self.job_name
        return return_string
