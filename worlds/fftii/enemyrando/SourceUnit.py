from .Job import Job, monster_families
from .SpriteSet import SpriteSet
from worlds.fftii.patchersuite.Unit import UnitGender


class SourceUnit:
    sprite_set: SpriteSet
    job: Job
    gender: UnitGender

    def __init__(self, sprite_set: SpriteSet, job: Job, gender: UnitGender):
        self.sprite_set = sprite_set
        self.job = job
        self.gender = gender

    def to_json(self):
        return {
            "SpriteSet": self.sprite_set.value,
            "Job": self.job.value,
            "Gender": self.gender.value
        }

    def __repr__(self):
        return f"Sprite: {self.sprite_set.name}, Job: {self.job.name}, Gender: {self.gender.name}"

    def __eq__(self, other):
        if self.sprite_set != other.sprite_set:
            return False
        if self.job != other.job:
            if self.job in monster_families.keys():
                if other.job not in monster_families[self.job]:
                    return False
            else:
                return False
        if self.gender != other.gender:
            return False
        return True

    def __hash__(self):
        return hash((self.sprite_set.value, self.job.value, self.gender.value))